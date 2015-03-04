# coding: utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

import mptt_urls


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^gallery/(?P<path>.*)', mptt_urls.view(model='gallery.models.Category', view='gallery.views.category', slug_field='slug'), {'extra': 'You may also pass extra options as usual!'}, name='gallery'),

    url(r'^admin/', include(admin.site.urls)),
)
