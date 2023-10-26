from django.core.management.base import BaseCommand
from shops.models import Product

class Command(BaseCommand):
    help = 'Remove duplicate products'

    def handle(self, *args, **options):
        # Retrieve all products
        products = Product.objects.all()

        # Define a dictionary to track unique product details
        unique_products = {}

        # Iterate through all products
        for product in products:
            # Define a unique key based on all product details
            product_key = (
                product.shops_net,
                product.code,
                product.name,
                product.measurement_unit_id,
                product.quantity,
                product.unit_of_measurement_id,
                product.price,
                product.unit_of_measurement_price
            )

            # Check if the product details already exist in the dictionary
            if product_key in unique_products:
                # Delete the duplicate product
                product.delete()
                self.stdout.write(self.style.ERROR(f'Removed duplicate product: {product.name}'))
            else:
                # Add the product details to the dictionary
                unique_products[product_key] = True
                self.stdout.write(self.style.SUCCESS(f'Processed product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Duplicate products removed successfully'))
