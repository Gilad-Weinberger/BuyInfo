from django.db import models
from base.models import Expense, Expense_type
from accounts.models import User
from decimal import Decimal
import os

def shops_net_logo_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"net_{instance.name}{ext}"
    return os.path.join('shops_net_logos', new_filename)

def receipt_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"receipt_{instance.user}{instance.date}{ext}"
    return os.path.join('receipts/images', new_filename)

def receipt_pdf_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"receipt_{instance.user}{instance.date}{ext}"
    return os.path.join('receipts/pdfs', new_filename)

class Shops_net(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=shops_net_logo_upload_path)

    @property
    def branches(self):
        return Shop.objects.filter(Shop.shops_net==self.name)

    @property
    def branches_count(self):
        return branches(self).count

    def __str__(self):
        return self.name

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    shop_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100, null=True)
    shops_net = models.ForeignKey(Shops_net, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.shops_net} ({self.shop_id}) -- {self.name}"

class Payment_type(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class Measurement_unit(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Unit_of_measurement(models.Model):
    name = models.ForeignKey(Measurement_unit, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.count}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    shops_net = models.ForeignKey(Shops_net, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    measurement_unit = models.ForeignKey(Measurement_unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=50, decimal_places=2)
    unit_of_measurement = models.ForeignKey(Unit_of_measurement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    unit_of_measurement_price = models.DecimalField(max_digits=50, decimal_places=4)

    @property
    def calculate_unit_of_measurement_price(self):
        calculation = (self.price / self.quantity) - self.unit_of_measurement_price
        return (calculation >= -1 and calculation <= 1)

    def __str__(self):
        return f"{self.name} - {self.price} | {self.shops_net}"


class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to=receipt_pdf_upload_path)
    image = models.ImageField(upload_to=receipt_image_upload_path)
    payment_type = models.ForeignKey(Payment_type, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def receipt_products(self):
        return ReceiptProduct.objects.filter(receipt=self)
    
    @property
    def total_price(self):
        total = Decimal(0)
        for receipt_product in self.receipt_products:
            total += receipt_product.total_price()
        return total
    
    def __str__(self):
        return f"{self.user} | {self.shop} | {self.date}"

    def reduce_receipt_products(self):
        products_in_receipt = self.receipt_products.values_list('product', flat=True).distinct()

        for product_id in products_in_receipt:
            products_to_reduce = self.receipt_products.filter(product_id=product_id)

            if products_to_reduce.count() > 1:
                total_count = products_to_reduce.aggregate(models.Sum('count'))['count__sum']
                first_product = products_to_reduce.first()
                first_product.count = total_count
                first_product.save()
                products_to_reduce.exclude(pk=first_product.pk).delete()

class ReceiptProduct(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product} x{self.count}"

    def total_price(self):
        return self.count * self.product.price