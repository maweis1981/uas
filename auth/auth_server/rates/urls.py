from django.conf.urls.defaults import *

urlpatterns = patterns('rates.views',
    url(r'^status$', 'status', name='status'),
)

