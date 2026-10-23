from django.core.management.base import BaseCommand

from django_comments.models import Comment
from sabbatical_blog.models import Post

import html

class Command(BaseCommand):

    def handle(self, *args, **options):
        for comment in Comment.objects.all():
            comment.comment = html.unescape(comment.comment)
            comment.save()
        for post in Post.objects.all():
            post.content = html.unescape(post.content)
            post.save()



