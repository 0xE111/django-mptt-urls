from django.conf.urls import patterns, include, url
import mptt_urls
from django.views.generic import TemplateView

from django.contrib import admin
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
mptt_urls.register('gallery', mptt_urls_gallery_settings)

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^gallery/', include('mptt_urls.urls'), {'settings': mptt_urls_gallery_settings}),

    url(r'^admin/', include(admin.site.urls)),
)
