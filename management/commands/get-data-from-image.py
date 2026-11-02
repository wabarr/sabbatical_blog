from django.core.management.base import BaseCommand
from sabbatical_blog.models import LegacyWPMedia
from django.conf import settings
import os
import io

from google.cloud import storage

class Command(BaseCommand):

    def handle(self, *args, **options):
        from PIL import Image
        from PIL.ExifTags import TAGS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GS_CREDENTIALS_FILE_PATH
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        for medium in LegacyWPMedia.objects.all():
            name = medium.google_storage_url.split('/')[-1]
            blob = bucket.get_blob(name)
            image_bytes = blob.download_as_bytes()
            image = Image.open(io.BytesIO(image_bytes))
            exif_data = image.getexif()
            if not exif_data:
                print("No EXIF data found in this image.")
            for tag_id in exif_data:
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "Make":
                    print(exif_data[tag_id])
                if tag_name == 'DateTime':
                    print(exif_data[tag_id])  # Format typically looks like: 'YYYY:MM:DD HH:MM:SS'
                if tag_name == 'DateTimeOriginal':
                    print(exif_data[tag_id])  # Format typically looks like: 'YYYY:MM:DD HH:MM:SS'

            ##time zone is in local time. I have no idea what the time zone is for the camera so maybe
            print("EXIF data found, but 'DateTime' tag is missing.")



