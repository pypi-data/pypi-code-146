from ..shared import mask_number
from .address import AddressResponse


class RoutingDetailsResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def bank_name(self):
        return self.json.get('bank_name')

    @property
    def routing_number(self):
        return self.json.get('routing_number')

    @property
    def routing_number_type(self):
        return self.json.get('routing_number_type')

    @property
    def bank_address(self):
        result = self.json.get('bank_address')
        if result:
            return AddressResponse(result)
        return None

    def __str__(self) -> str:
        return (
            f"id: { self.id }, bank_name: { self.bank_name }, routing_number: { mask_number(self.routing_number) },"
            f" routing_number_type: { self.routing_number_type }, bank_address: { str(self.bank_address) }"
        )
