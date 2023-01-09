from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'AddOn',
    'AddOnResponse',
    'AddOnRoute',
]

class AddOn(BaseResource):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    description: Optional[str]


class AddOnResponse(BaseResource):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    description: Optional[str]


class AddOnRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = AddOn
    response_model: Optional[Type[BaseResource]] = AddOnResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'add_ons'

    @lazyproperty
    def root_name(self):
        return 'add_on'
    