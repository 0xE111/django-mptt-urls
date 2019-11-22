from django.contrib import admin
from django.urls import re_path, path
from django.views.generic import TemplateView

import mptt_urls

admin.autodiscover()


urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='home.html')),
    re_path(r'^gallery/(?P<path>.*)', mptt_urls.view(model='gallery.models.Category', view='gallery.views.category', slug_field='slug', trailing_slash=False), {'extra': 'You may also pass extra options as usual!'}, name='gallery'),

    path(r'admin/', admin.site.urls),
]
