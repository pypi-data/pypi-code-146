from typing import List

from .account_details import AccountDetailsResponse
from .routing_details import RoutingDetailsResponse


class VirtualAccountResponse:
    def __init__(self, json):
       self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def name(self):
        return self.json.get('name')

    @property
    def internal_account_id(self):
        return self.json.get('internal_account_id')

    @property
    def credit_ledger_account_id(self):
        return self.json.get('credit_ledger_account_id')

    @property
    def debit_ledger_account_id(self):
        return self.json.get('debit_ledger_account_id')

    @property
    def counterparty_id(self):
        return self.json.get('counterparty_id')

    @property
    def account_details(self) -> List[AccountDetailsResponse]:
        result = self.json.get('account_details')
        return [AccountDetailsResponse(account_detail) for account_detail in result]

    @property
    def routing_details(self) -> List[RoutingDetailsResponse]:
        result = self.json.get('routing_details')
        return [RoutingDetailsResponse(routing_detail) for routing_detail in result]

    @property
    def metadata(self):
        return self.json.get('metadata')
