from typing import Optional, Type, List
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty, Field

__all__ = [
    'Metric',
    'ChargeObject',
    'ChargeUsage',
    'CustomerUsageResponse',
    'BillingConfiguration',
    'Customer',
    'CustomerResponse',
    'CustomerRoute',
]

## Usage Models
class Metric(BaseResource):
    lago_id: str
    name: str
    code: str
    aggregation_type: str

class ChargeObject(BaseResource):
    lago_id: str
    charge_model: str


class ChargeGroup(BaseResource):
    key: Optional[str] = None
    units: Optional[float] = None
    value: Optional[str] = None
    lago_id: Optional[str] = None
    amount_cents: Optional[float] = None

class ChargeUsage(BaseResource):
    units: float
    amount_cents: int
    amount_currency: str
    charge: ChargeObject
    billable_metric: Metric
    groups: Optional[List[ChargeGroup]] = None


class CustomerUsageResponse(BaseResource):
    from_date: str
    to_date: str
    issuing_date: str
    amount_cents: int
    amount_currency: str
    total_amount_cents: int
    total_amount_currency: str
    vat_amount_cents: int
    vat_amount_currency: str
    charges_usage: List[ChargeUsage]

## Customer Models

class BillingConfiguration(BaseResource):
    payment_provider: Optional[str]
    provider_customer_id: Optional[str]
    vat_rate: Optional[float] = Field(None, alias='tax_rate')
    sync_with_provider: Optional[bool]

class Customer(BaseResource):
    external_id: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    email: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    logo_url: Optional[str]
    name: str
    phone: Optional[str]
    state: Optional[str]
    url: Optional[str]
    zipcode: Optional[str]
    billing_configuration: Optional[BillingConfiguration]


class CustomerResponse(BaseResource):
    lago_id: str
    external_id: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    email: Optional[str]
    created_at: str
    legal_name: Optional[str]
    legal_number: Optional[str]
    logo_url: Optional[str]
    name: str
    phone: Optional[str]
    state: Optional[str]
    url: Optional[str]
    # vat_rate: Optional[float]
    zipcode: Optional[str]
    billing_configuration: Optional[BillingConfiguration]


class CustomerRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Customer
    response_model: Optional[Type[BaseResource]] = CustomerResponse
    usage_model: Optional[Type[BaseResource]] = CustomerUsageResponse
    
    @lazyproperty
    def api_resource(self):
        return 'customers'
    
    @lazyproperty
    def root_name(self):
        return 'customer'
    
    @lazyproperty
    def usage_enabled(self):
       return True
    

