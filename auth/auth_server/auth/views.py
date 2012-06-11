from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, get_list_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.contrib.auth.forms import UserCreationForm

from oauthost.decorators import oauth_required

from oauthost.models import Client, AuthorizationCode, Token,RedirectionEndpoint
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
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/accounts/login")
    elif request.user.is_authenticated():
        return redirect("/auth/list")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    },context_instance=RequestContext(request))

@login_required	
def create(request):
    if request.method == "POST":
	    client = Client.objects.create(title=request.POST['title'],
			description=request.POST['description'],
			user=request.user,
			link=request.POST['link'])
	    RedirectionEndpoint.objects.create(client=client,uri='/auth/token?')
	    return redirect("/auth/list")
    else:
        return render_to_response('auth/create.html',context_instance=RequestContext(request))
        
@login_required
def clients(request):
    client_list = Client.objects.filter(user=request.user).order_by('-date_registered')
    paginator = Paginator(client_list, 2)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    return render_to_response('auth/list.html', locals(),context_instance=RequestContext(request))

@login_required
def detail(request,id):
	client = Client.objects.get(id=int(id))
	uri = client.redirectionendpoint_set.values_list('uri')
	return render_to_response('auth/detail.html', locals(),context_instance=RequestContext(request))

def token(request):
    token = request.GET['access_token']
    scopes = Token.objects.get(access_token=token).scopes.all()
    #print Token.objects.get(access_token=token).scopes
    #print Token.objects.get(access_token=token).scopes
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
    try:
        tk = Token.objects.get(access_token=token)
    except Token.DoesNotExist:
        code = 400
        message = 'token error'
        return render_to_response('auth/validate.json', locals())

    if tk.expires_at is not None:
        code = 400
        message = 'token expired'
        return render_to_response('auth/validate.json', locals())
    scope = tk.scopes.filter(title=request.GET['endpoint'])
    if not scope:
        code = 400
        message = 'unauthorized'
        return render_to_response('auth/validate.json', locals())
    if False and checkRates(token, endpoint, ip):
        code = 400
        message = 'X-FeatureRateLimit-Limit'
        return render_to_response('auth/validate.json', locals())
    code = 200
    message = 'successful'
    return render_to_response('auth/validate.json', locals())


def authorize(request):
    pass


#@oauth_required(scope_auto=True)
def test(request):
    return validate(request)
    #return HttpResponse('Hello Test API')


def authenticate(request):
    pass


def oauth_callback(request):
    pass


def access_token(request):
    pass


def request_token(request):
    pass