import json
from datetime import timedelta
from typing import Tuple, Iterable

import requests
from django.conf import settings
from django.utils import timezone

from velait.velait_django.velait_users.exceptions import UserAuthenticationError


def authorize_user(grant_type: str, auth_data: Iterable[Tuple[str, str]]):
    try:
        auth_response = requests.post(
            url=settings.MIO_SSO_TOKEN_URL,
            data=[
                ("grant_type", grant_type),
                ("scope", " ".join(settings.MIO_SSO_SCOPES)),
                ("client_id", settings.MIO_SSO_CLIENT_KEY),
                ("client_secret", settings.MIO_SSO_CLIENT_SECRET),
                *auth_data,
            ],
        )

        if not auth_response.ok:
            raise requests.RequestException()

        json_data = auth_response.json()
        access_token = json_data['access_token']
        refresh_token = json_data['refresh_token']
        expires_in = json_data['expires_in']
    except (json.JSONDecodeError, KeyError, requests.RequestException):
        raise UserAuthenticationError()

    return access_token, refresh_token, timezone.now() + timedelta(seconds=expires_in)
