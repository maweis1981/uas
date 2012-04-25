from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, get_list_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from oauthost.decorators import oauth_required

from oauthost.models import Client, AuthorizationCode, Token
from oauthost.utils import *
from oauthost.config import *

from oauthost.models import Client

from rates.rates_utils import checkRates

"""

oauth_consumer_key : Get From Application Data
oauth_consumer_secret : Get From Application Data
oauth_nonce : Random Generated
oauth_signature_method : HMAC-SHA1, PLAIN
oauth_timestamp : Now
oauth_version : 2.0

"""

def create(request):
    if request.method == "POST":
        pass
    else:
        return render_to_response('auth/create.html',locals())
        

def clients(request):
    clients = Client.objects.order_by('-date_registered')
    return render_to_response('auth/list.html', locals())


def token(request):
    token = request.GET['access_token']
    return render_to_response('auth/token.html', locals())


def validate(request):
    """
    interaction with APIs Server for check the request is valid.
    check access_token
    check scope
    check rates limited
    """

    token = request.GET['access_token']
    endpoint = request.GET['endpoint']
    #    ip =  request.META['HTTP_X_FORWARDED_FOR']
    ip = request.META['REMOTE_ADDR']
    #    ip = '127.0.0.1'
    if checkRates(token, endpoint, ip):
        code = 400
        message = 'X-FeatureRateLimit-Limit'
        return render_to_response('auth/validate.json', locals())
    code = 200
    message = 'successful'
    return render_to_response('auth/validate.json', locals())


def authorize(request):
    pass


@oauth_required(scope_auto=True)
def test(request):
    return HttpResponse('Hello Test API')


def authenticate(request):
    pass


def oauth_callback(request):
    pass


def access_token(request):
    pass


def request_token(request):
    pass