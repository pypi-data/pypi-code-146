from rest_framework.exceptions import APIException


class InvalidTokenException(APIException):

    status_code = 403
    default_detail = 'Invalid token'
    default_code = 'Invalid token'
