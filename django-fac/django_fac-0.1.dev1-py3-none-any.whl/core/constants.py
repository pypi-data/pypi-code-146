from django.conf import settings
from enum import Enum

FAC_ID = settings.FAC_ID    
FAC_PASSWORD = settings.FAC_PASSWORD
FAC_DEFAULT_CURRENCY = settings.FAC_DEFAULT_CURRENCY
FAC_V2_BASE_URL = settings.FAC_V2_BASE_URL

FAC_V2_HEADERS_JSON = {
    "PowerTranz-PowerTranzId": FAC_ID, 
    "PowerTranz-PowerTranzPassword" : FAC_PASSWORD,
    "Content-Type" : 'application/json',
    'Accept' : 'application/json'
}

FAC_V2_HEADERS_PLAIN_TEXT = FAC_V2_HEADERS_JSON
FAC_V2_HEADERS_PLAIN_TEXT['Accept'] = "text/plain"

class TransactionType(Enum):
    AUTH = 1
    SALE = 2
    CAPTURE = 3
    VOID = 4
    REFUND = 5

class ISOResponseCode(str, Enum):
    AUTH_COMPLETE = '3D0'
    AUTH_3DS_NOT_SUPPORTED = '3D1'
    AUTH_ERROR = '3D3'
    SPI_COMPLETE = 'SP4'
    TRANS_APPROVED = '00'
    TOKENIZE_COMPLETE ='TK0'
    FRAUD_CHECK_COMPLETE = 'FC0'

class AuthStatus(str, Enum):
    SUCCESS = 'Y'
    ATTEMPTED = 'A'
    NOT_AUTHENTICATED = 'N'
    UNAVAILABLE = 'U'
    REJECTED = 'R'
