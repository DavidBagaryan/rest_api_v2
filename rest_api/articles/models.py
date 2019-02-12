from django.db import models

from .utils import DisplayNameMixin


class Article(DisplayNameMixin, models.Model):
    class Meta:
        ordering = ['-pub_date']

    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField(blank=True, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=150, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')


class Tag(DisplayNameMixin, models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50, db_index=True, unique=True)
