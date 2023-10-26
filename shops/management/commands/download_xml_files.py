import requests
import gzip
import shutil
import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Download and extract files from a series of URLs'

    def handle(self, *args, **options):
        # Base URL and destination directory
        base_url = "https://url.publishedprices.co.il/file/d/PriceFull7290058140886-{number}-202310261556.gz"
        dest_dir = os.path.join(settings.BASE_DIR, 'data_files/xml_data')

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Generate a range of numbers from 1 to 10 (001 to 010)
        for number in range(3, 29):
            # Format the number with leading zeros (e.g., 1 -> 001)
            number_str = str(number).zfill(3)

            # Construct the URL with the updated number
            url = base_url.format(number=number_str)

            # Define the destination file path
            dest_file = os.path.join(dest_dir, f"PriceFull_RamiLevi_{number_str}.xml")

            try:
                # Download the .gz file
                response = requests.get(url, stream=True)
                response.raise_for_status()

                # Save the .gz file to the destination directory
                with open(dest_file + '.gz', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Extract the .gz file to get the XML file
                with gzip.open(dest_file + '.gz', 'rb') as f_in, open(dest_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                
                # Delete the original .gz file
                os.remove(gz_file_path)
                
                self.stdout.write(self.style.SUCCESS(f"Downloaded and extracted: {dest_file}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error while processing {url}: {e}"))

        self.stdout.write(self.style.SUCCESS("All files downloaded and extracted."))
