from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<url>.*)$', 'mptt_urls.views.process_url'),
)
