from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Tag(models.Model):
    tag = models.SlugField(max_length=20)

    def __str__(self):
        return self.tag


class Article(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    url = models.SlugField(max_length=20)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    version = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        version = kwargs.pop('version')

        # Incrementing based on whether save was a major revision or minor revision
        self.version += 1.0 if version == 1 else 0.1

        return super(Article, self).save(*args, **kwargs)
