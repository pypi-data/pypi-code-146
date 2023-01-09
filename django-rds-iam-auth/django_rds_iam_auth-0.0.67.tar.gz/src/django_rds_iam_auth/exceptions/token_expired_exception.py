from rest_framework.exceptions import APIException


class TokenExpiredException(APIException):

    status_code = 401
    default_detail = 'Token expired'
    default_code = 'Token expired'
