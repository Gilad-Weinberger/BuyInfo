from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from shops.models import Shops_net, Shop, Measurement_unit, Unit_of_measurement, Product

class Command(BaseCommand):
    help = 'Import XML data into Django models'

    def add_arguments(self, parser):
        parser.add_argument('file_number', type=int, help='The file number to import (e.g., 049)')

    def handle(self, *args, **options):
        file_number = str(options['file_number']).zfill(3)  # Ensure it has 3 characters with leading zeros
        xml_file_path = f'data_files/xml_data/PriceFull_RamiLevi_{file_number}.xml'

        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            shops_net = Shops_net.objects.first()
            shop_name = root.find('StoreId').text  # Extract shop name from XML
            shop, created = Shop.objects.get_or_create(
                shop_id=root.find('StoreId').text,
                name=shop_name,  # Set the shop name based on the XML data
                shops_net=shops_net,
            )

            for item_elem in root.find('Items').iter('Item'):

                unit_qty = item_elem.find('UnitQty').text
                if unit_qty.isnumeric():
                    measurement_unit, created = Measurement_unit.objects.get_or_create(name=unit_qty)
                else:
                    measurement_unit, created = Measurement_unit.objects.get_or_create(name="יחידות")

                unit_of_measure_text = item_elem.find('UnitOfMeasure').text

                # Remove leading and trailing whitespace, if any
                unit_of_measure_text = unit_of_measure_text.strip()

                unit_of_measure_parts = unit_of_measure_text.split()
                if len(unit_of_measure_parts) == 2:
                    unit_of_measure_number, unit_of_measure_name = unit_of_measure_parts
                    unit_of_measure_name = unit_of_measure_name.strip()

                    # Check if the number part is numeric
                    if unit_of_measure_number.isnumeric():
                        unit_of_measure_number = float(unit_of_measure_number)
                    else:
                        unit_of_measure_number = 1.0

                    measurement_unit, created = Measurement_unit.objects.get_or_create(name=unit_of_measure_name)

                    unit_of_measurement, created = Unit_of_measurement.objects.get_or_create(
                        name=measurement_unit,
                        count=unit_of_measure_number
                    )

                elif len(unit_of_measure_parts) == 1:
                    # Handle cases where there is only text in the UnitOfMeasure value
                    unit_of_measure_name = unit_of_measure_parts[0].strip()

                    # Set the number value to 1
                    unit_of_measure_number = 1.0

                    # Check if the unit of measurement is numeric
                    if unit_of_measure_name.isnumeric():
                        unit_of_measure_number = float(unit_of_measure_name)
                        unit_of_measure_name = "יחידות"

                    measurement_unit, created = Measurement_unit.objects.get_or_create(name=unit_of_measure_name)

                    unit_of_measurement, created = Unit_of_measurement.objects.get_or_create(
                        name=measurement_unit,
                        count=unit_of_measure_number
                    )

                else:
                    print("Invalid UnitOfMeasure value in XML")

                product = Product.objects.create(
                    shops_net=shops_net,
                    code=item_elem.find('ItemCode').text,
                    name=item_elem.find('ItemName').text,
                    measurement_unit=measurement_unit,
                    quantity=float(item_elem.find('Quantity').text),
                    unit_of_measurement=unit_of_measurement,
                    price=float(item_elem.find('ItemPrice').text),
                    unit_of_measurement_price=float(item_elem.find('UnitOfMeasurePrice').text),
                )

                self.stdout.write(self.style.SUCCESS(f"{item_elem.find('ItemName').text} item was created successfully"))

            self.stdout.write(self.style.SUCCESS('XML data imported successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
