from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from pyjsconnect import make_jsconnect_response
from hashlib import sha1


def jsconnect(request, hash_func=None):

    if hash_func is None:
        hash_func = sha1

    user_data = {}

    if request.user.is_authenticated and hasattr(request.user, "profile"):
        user_data['uniqueid'] = request.user.id
        user_data['name'] = request.user.profile.username
        user_data['email'] = request.user.email
        user_data["roles"] = ",".join(request.user.profile.community_roles)
        user_data['photourl'] = ""

    json_response, content_type = make_jsconnect_response(
        client_id = settings.JSCONNECT["client_id"],
        secret = settings.JSCONNECT["secret"],
        request_data = request.GET.dict(),
        user_data = user_data,
        hash_func = hash_func,
    )

    return HttpResponse(json_response, content_type=content_type)
