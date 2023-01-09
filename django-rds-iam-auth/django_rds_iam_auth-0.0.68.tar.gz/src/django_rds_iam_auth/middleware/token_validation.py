import datetime
import json

import jwt

from django.conf import settings
from django.http import HttpResponse
from django.urls import resolve
from rest_framework import status

from django_rds_iam_auth.middleware.jwt_exposer import local
from django_rds_iam_auth.exceptions import InvalidTokenException, TokenExpiredException


class CheckTokenValidation:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if (
                not hasattr(settings, 'NON_SECURE_ROUTES') or url_name not in settings.NON_SECURE_ROUTES and
                not request.path_info.startswith('/admin') and
                not request.path_info.startswith('/manufacture')
        ):
            try:
                access_token_payload = jwt.decode(local.ibrag_access_token, verify=False)
                id_token_payload = jwt.decode(local.ibrag_idToken, verify=False)
                if (
                        access_token_payload['exp'] < datetime.datetime.now().timestamp() or
                        id_token_payload['exp'] < datetime.datetime.now().timestamp()
                ):
                    return HttpResponse(json.dumps({
                        'message': 'Token expired',
                        'code': 'Token expired'
                    }), status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return HttpResponse(json.dumps({
                    'message': 'Invalid token',
                    'code': 'Invalid token'
                }), status=status.HTTP_403_FORBIDDEN)
        else:
            local.ibrag_access_token = None
            local.ibrag_idToken = None

        response = self.get_response(request)
        return response
