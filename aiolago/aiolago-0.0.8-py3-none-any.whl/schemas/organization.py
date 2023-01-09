from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'Organization',
    'OrganizationResponse',
    'OrganizationRoute',
]


class Organization(BaseResource):
    webhook_url: Optional[str]
    vat_rate: Optional[float]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    invoice_footer: Optional[str]


class OrganizationResponse(BaseResource):
    name: str
    created_at: str
    webhook_url: Optional[str]
    vat_rate: Optional[float]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    invoice_footer: Optional[str]


class OrganizationRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Organization
    response_model: Optional[Type[BaseResource]] = OrganizationResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'organizations'

    @lazyproperty
    def root_name(self):
        return 'organization'