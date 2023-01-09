from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'WalletTransaction',
    'WalletTransactionResponse',
    'WalletTransactionRoute',
]


class WalletTransaction(BaseResource):
    wallet_id: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]


class WalletTransactionResponse(BaseResource):
    lago_id: str
    lago_wallet_id: str
    status: str
    transaction_type: str
    amount: str
    credit_amount: str
    settled_at: Optional[str]
    created_at: str


class WalletTransactionRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = WalletTransaction
    response_model: Optional[Type[BaseResource]] = WalletTransactionResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'wallet_transactions'

    @lazyproperty
    def root_name(self):
        return 'wallet_transaction'

