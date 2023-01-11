from dataclasses import dataclass
from .address import AddressRequest
from .account_details import AccountDetailsRequest
from .routing_details import RoutingDetailsRequest
from typing import List, Optional


@dataclass
class ExternalAccountRequest():
    counterparty_id: str
    account_details: Optional[List[AccountDetailsRequest]] = None
    routing_details: Optional[List[RoutingDetailsRequest]] = None
    account_type: Optional[str] = None
    party_address: Optional[AddressRequest] = None
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        self.account_details = self.account_details if self.account_details else []
        self.routing_details = self.routing_details if self.routing_details else []
        self.idempotency_key  = f"external_account_{self.idempotency_key}" if self.idempotency_key else None

    def to_json(self):
        account_details_json = [account_detail.to_json() for account_detail in self.account_details]
        routing_details_json = [routing_detail.to_json() for routing_detail in self.routing_details]
        result = {
            'counterparty_id': self.counterparty_id,
            'account_details': account_details_json,
            'routing_details': routing_details_json,
        }
        if self.account_type:
            result['account_type'] = self.account_type
        if self.party_address:
            result['party_address'] = self.party_address.to_json()

        return result
