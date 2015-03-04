# coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField('category name', max_length=32)
    # ... some other fields
    parent = TreeForeignKey('self', null=True, blank=True, verbose_name='parent category', related_name='categories')
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField('number of page views', default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gallery', kwargs={'path': self.get_path()})


class Photo(models.Model):
    name = models.CharField('photo name', max_length=32)
    # ... some other fields
    parent = TreeForeignKey(Category, verbose_name='parent category', related_name='photos')
    slug = models.SlugField()

    class Meta:
        unique_together = ('slug', 'parent')

    def __unicode__(self):
        return self.name
