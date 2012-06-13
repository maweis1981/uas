from django.conf.urls.defaults import *

urlpatterns = patterns('auth.views',
    #    url(r'^authorize$','authorize', name='authorize'),
    #    url(r'^request_token','request_token', name='request_token'),
    #    url(r'^access_token','access_token', name='access_token'),
    #    url(r'^oauth_callback','oauth_callback', name='oauth_callback'),
    #    url(r'^authenticate$','authenticate', name='authenticate'),
    url(r'^create$', 'create', name='create'),
    url(r'^list$', 'clients', name='clients'),
	url(r'^detail/(\d+)/$', 'detail', name='detail'),
	url(r'^register/$', 'register', name='register'),

    url(r'^test$', 'test', name='test'),
    url(r'^token$', 'token', name='token'),
    url(r'^validate$', 'validate', name='validate'),
)

