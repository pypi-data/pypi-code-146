import json

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response


class CheckUserStatusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if isinstance(request.user, AnonymousUser) or request.user.is_active:
            response = self.get_response(request)
        else:
            response = HttpResponse(json.dumps({
                'message': 'Current user is not active'
            }), status=status.HTTP_403_FORBIDDEN)

        return response
