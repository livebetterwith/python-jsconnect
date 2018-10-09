from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from pyjsconnect import make_jsconnect_response
from hashlib import sha1


try:
    JSCONNECT_CLIENT_ID = getattr(settings, 'JSCONNECT_CLIENT_ID')
    JSCONNECT_SECRET = getattr(settings, 'JSCONNECT_SECRET')
except AttributeError:
    raise ImproperlyConfigured(
        "JSCONNECT_CLIENT_ID and JSCONNECT_SECRET must be specified in "
        "settings"
    )


def jsconnect(request, hash_func=None):

    if hash_func is None:
        hash_func = sha1

    user_data = {}

    if request.user.is_authenticated():
        user_data['uniqueid'] = request.user.id
        user_data['name'] = request.user.username
        user_data['email'] = request.user.email
        user_data['photourl'] = ""

    json_response, content_type = make_jsconnect_response(
        client_id = JSCONNECT_CLIENT_ID,
        secret = JSCONNECT_SECRET,
        request_data = request.GET.dict(),
        user_data = user_data,
        hash_func = hash_func,
    )

    return HttpResponse(json_response, content_type=content_type)
