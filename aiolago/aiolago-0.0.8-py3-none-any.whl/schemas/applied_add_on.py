from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'AppliedAddOn',
    'AppliedAddOnResponse',
    'AppliedAddOnRoute',
]

class AppliedAddOn(BaseResource):
    external_customer_id: str
    add_on_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]


class AppliedAddOnResponse(BaseResource):
    lago_id: str
    lago_add_on_id: str
    add_on_code: str
    external_customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_currency: str
    created_at: str

class AppliedAddOnRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = AppliedAddOn
    response_model: Optional[Type[BaseResource]] = AppliedAddOnResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'applied_add_ons'

    @lazyproperty
    def root_name(self):
        return 'applied_add_on'
    