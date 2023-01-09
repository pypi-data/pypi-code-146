import jwt
from django_rds_iam_auth.middleware.jwt_exposer import local

from django_rds_iam_auth.models import User


class UserInjector:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user_sub = jwt.decode(local.ibrag_access_token, verify=False).get('sub', None)
            request.user = User.objects.get(id=user_sub)
        except jwt.DecodeError:
            pass

        response = self.get_response(request)

        return response