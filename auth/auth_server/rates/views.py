from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, get_list_or_404
from django.shortcuts import redirect
from django.http import HttpResponse

import redis
from auth_server import settings

"""

oauth_consumer_key : Get From Application Data
oauth_consumer_secret : Get From Application Data
oauth_nonce : Random Generated
oauth_signature_method : HMAC-SHA1, PLAIN
oauth_timestamp : Now
oauth_version : 2.0

"""


def status(request):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
    status = r.get('status')
    return render_to_response('rates/status.html', locals())