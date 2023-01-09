from spackle.customer import Customer
from spackle.exceptions import SpackleException
from spackle.dynamodb import get_client

api_key = None
api_base = "https://api.spackle.so"


def bootstrap():
    global api_key
    if api_key:
        get_client()
