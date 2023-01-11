from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from velait.velait_django.velait_users.services import authorize_user
from velait.velait_django.main.services.utils import create_random_str


def user_logout_view(request):
    response = HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


def user_login_view(request):
    request_args = urlencode({
        "response_type": "code",
        "state": create_random_str(getattr(settings, 'USER_LOGIN_STATE_LEN', 64)),
        "nonce": create_random_str(getattr(settings, 'USER_LOGIN_NONCE_LEN', 64)),
        "scope": " ".join(settings.MIO_SSO_SCOPES),
        "client_id": settings.MIO_SSO_CLIENT_KEY,
        "redirect_uri": settings.MIO_SSO_REDIRECT_URL,
    })

    return redirect(f"{settings.MIO_SSO_AUTHORIZATION_URL}?{request_args}")


def user_authentication_view(request):
    try:
        access_token, refresh_token, expiration_time = authorize_user(
            grant_type="authorization_code",
            auth_data=[('code', request.GET.get('code'))]
        )
    except ValueError:
        raise BadRequest(_("Ошибка авторизации"))

    response = HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    response.set_cookie(
        key='access_token',
        value=access_token,
        expires=expiration_time,
        httponly=True,
        secure=True,
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        expires=expiration_time,
        httponly=True,
        secure=True,
    )
    return response
