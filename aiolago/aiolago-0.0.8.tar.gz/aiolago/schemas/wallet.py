from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'Wallet',
    'WalletResponse',
    'WalletRoute',
]

class Wallet(BaseResource):
    name: Optional[str]
    external_customer_id: Optional[str]
    rate_amount: Optional[str] = '1.0'
    currency: Optional[str] = 'USD'
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    expiration_date: Optional[str]


class WalletResponse(BaseResource):
    lago_id: str
    lago_customer_id: str
    external_customer_id: str
    status: str
    currency: str
    name: Optional[str]
    rate_amount: str
    credits_balance: str
    balance: str
    consumed_credits: str
    created_at: str
    expiration_date: Optional[str]
    last_balance_sync_at: Optional[str]
    last_consumed_credit_at: Optional[str]
    terminated_at: Optional[str]

class WalletRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Wallet
    response_model: Optional[Type[BaseResource]] = WalletResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'wallets'

    @lazyproperty
    def root_name(self):
        return 'wallet'