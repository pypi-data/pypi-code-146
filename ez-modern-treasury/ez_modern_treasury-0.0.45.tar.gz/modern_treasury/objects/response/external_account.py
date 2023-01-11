from .address import AddressResponse
from .account_details import AccountDetailsResponse
from .routing_details import RoutingDetailsResponse


class ExternalAccountResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def name(self):
        return self.json.get('name')

    @property
    def party_name(self):
        return self.json.get('party_name')

    @property
    def account_type(self):
        return self.json.get('account_type')

    @property
    def counterparty_id(self):
        return self.json.get('counterparty_id')

    @property
    def party_type(self):
        return self.json.get('party_type')

    @property
    def party_identifier(self):
        return self.json.get('party_identifier')

    @property
    def party_address(self):
        address = self.json.get('party_address')
        return AddressResponse(address)

    @property
    def routing_details(self):
        result = []
        for routing_detail in self.json.get('routing_details'):
            result.append(RoutingDetailsResponse(json=routing_detail))
        return result

    @property
    def account_details(self):
        result = []
        for account_detail in self.json.get('account_details'):
            result.append(AccountDetailsResponse(json=account_detail))
        return result
