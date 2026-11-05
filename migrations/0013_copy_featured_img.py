
from django.db import migrations, models

def copy_featured_img(apps, schema_editor):
    #copies over the full URL field, strips out just the blob name and saves to the new featured_img field
    Post = apps.get_model('sabbatical_blog', 'Post')
    for post in Post.objects.all():
        blobname=post.featured_img_URL.split("/")[-1]
        post.featured_img=blobname
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sabbatical_blog', '0012_post_featured_img'),
    ]

    operations = [
        migrations.RunPython(copy_featured_img)
    ]
