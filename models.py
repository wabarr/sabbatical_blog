from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    legacy_WP_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class LegacyWPMedia(models.Model):
    legacyWPID = models.IntegerField(null=True, blank=True)
    media_url = models.URLField(null=True, blank=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    legacy_WP_id = models.IntegerField(null=True, blank=True)

    featured_img_URL = models.URLField(null=True, blank=True)

    # Author field linked to Django's built-in User model
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', limit_choices_to={'is_staff': True})

    # Category field linking to our Category model
    category = models.ManyToManyField(Category)

    content = CKEditor5Field('Text', config_name='default')
    map_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_popup_label = models.CharField(max_length=50, null=True, blank=True)

    # Date fields: published handles the actual date, created tracks the entry
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

