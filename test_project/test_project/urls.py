# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from mptt_urls import url_mptt


admin.autodiscover()

# Mptt_urls gallery settings
mptt_urls_gallery_settings = {
    'node': {
        'model': 'gallery.models.Category',
        'view': 'gallery.views.category',
        'slug_field': 'slug',
    },
    'leaf': {
        'model': 'gallery.models.Photo',
        'template': 'gallery/photo.html',
        'slug_field': 'slug',
    }
}

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url_mptt(r'^gallery/(?P<url>.*)', name='gallery', settings=mptt_urls_gallery_settings),  # Here we add special mptt url

    url(r'^admin/', include(admin.site.urls)),
)
