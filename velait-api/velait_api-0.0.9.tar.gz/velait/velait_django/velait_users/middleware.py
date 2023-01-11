import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from velait.velait_django.velait_users.services import authorize_user


User = get_user_model()


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_user_data(self, access_token):
        try:
            response = requests.get(
                settings.MIO_SSO_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if not response.ok:
                return None

            user_data = response.json()
            return User(
                business=user_data.get('business'),
                id=user_data.get('sub'),
                uuid=user_data.get('uuid'),
                username=user_data.get('preferred_username'),
                email=user_data.get('email'),
                first_name=user_data.get('given_name'),
                last_name=user_data.get('family_name'),
                is_staff=user_data.get('is_staff'),
                #   "groups": response_data['groups'],
            )
        except (json.JSONDecodeError, requests.RequestException):
            return None

    def _refresh_user(self, request):
        try:
            access_token, refresh_token, expiration_time = authorize_user(
                grant_type="refresh_token",
                auth_data=(
                    ('refresh_token', request.COOKIES.get('refresh_token')),
                ),
            )
        except ValueError:
            return self.get_response(request)

        request.user = self.get_user_data(access_token)

        response = self.get_response(request)
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

    def __call__(self, request):
        if not request.COOKIES.get('access_token') and not request.COOKIES.get('access_token'):
            return self.get_response(request)

        user_data = self.get_user_data(request.COOKIES.get('access_token'))
        if user_data is None:
            return self._refresh_user(request)

        request.user = user_data
        return self.get_response(request)
