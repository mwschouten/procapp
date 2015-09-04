from django.conf.urls import patterns, url
from web.views import index

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
)

