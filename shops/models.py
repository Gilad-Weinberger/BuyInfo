from django.db import models
from base.models import Expense, Expense_type
from accounts.models import User
import os

def shops_net_logo_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"net_{instance.name}{ext}"
    return os.path.join('shops_net_logos', new_filename)

def recipet_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"recipet_{instance.name}{ext}"
    return os.path.join('recipet_images', new_filename)

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

class Recipet(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=recipet_image_upload_path)

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

class RecipetProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    recipet = models.ForeignKey(Recipet, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)