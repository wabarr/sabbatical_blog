
from django.db import migrations, models

def copy_legacy_image(apps, schema_editor):
    #copies over the full URL field, strips out just the blob name and saves to the new featured_img field
    Img = apps.get_model('sabbatical_blog', 'LegacyWPMedia')
    for img in Img.objects.all():
        blobname=img.google_storage_url.split("/")[-1]
        img.google_storage_img=blobname
        img.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sabbatical_blog', '0015_legacywpmedia_google_storage_img'),
    ]

    operations = [
        migrations.RunPython(copy_legacy_image)
    ]
