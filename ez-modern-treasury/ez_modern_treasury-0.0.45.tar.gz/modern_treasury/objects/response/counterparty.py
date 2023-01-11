from typing import List

from .account import AccountResponse
from .routing_details import RoutingDetailsResponse


class CounterPartyResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self) -> str:
        return self.json.get("id")

    @property
    def name(self) -> str:
        return self.json.get("name")

    @property
    def accounts(self) -> List[AccountResponse]:
        account_details = self.json.get("accounts")
        if account_details:
            return [AccountResponse(account_detail) for account_detail in account_details]
        else:
            return []

    @property
    def routing_details(self) -> List[RoutingDetailsResponse]:
        routing_details = self.json.get("routing_details")
        if routing_details:
            return [RoutingDetailsResponse(routing_detail) for routing_detail in routing_details]
        else:
            return []

    @property
    def metadata(self) -> str:
        return self.json.get("metadata")

    def __str__(self) -> str:
        return (
            f"id: { self.id }, name: { self.name }, accounts: { [str(account) for account in self.accounts] },"
            f"routing_details: { [str(routing_detail) for routing_detail in self.routing_details] }, "
            f"metadata: { self.metadata }"
        )
