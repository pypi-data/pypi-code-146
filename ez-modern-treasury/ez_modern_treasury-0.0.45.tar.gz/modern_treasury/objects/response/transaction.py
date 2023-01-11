from typing import List

from .account_details import AccountDetailsResponse
from .routing_details import RoutingDetailsResponse


class TransactionResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')
