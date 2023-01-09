from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST

from ..sparrow_parcel.constants import PARCEL_ERROR_CODE_PREFIX


class ParcelException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = 'Bad_request'
    default_code = 'error'
    error_code = PARCEL_ERROR_CODE_PREFIX + 1


class ParcelRepeatScanException(ParcelException):
    error_code = PARCEL_ERROR_CODE_PREFIX + 2
