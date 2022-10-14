from django.db import models

class BlogPosts(models.Model):
    content = models.TextField()
