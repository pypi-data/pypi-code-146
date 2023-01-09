from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'InvoiceStatusChange',
    'InvoiceResponse',
    'InvoiceRoute',
]

class InvoiceStatusChange(BaseResource):
    status: str

class InvoiceResponse(BaseResource):
    lago_id: str
    sequential_id: int
    issuing_date: Optional[str]
    invoice_type: str
    status: str
    amount_cents: int
    amount_currency: str
    vat_amount_cents: int
    vat_amount_currency: str
    total_amount_cents: int
    total_amount_currency: str
    file_url: Optional[str]

class InvoiceRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = InvoiceStatusChange
    response_model: Optional[Type[BaseResource]] = InvoiceResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'invoices'

    @lazyproperty
    def root_name(self):
        return 'invoice'
    
    @lazyproperty
    def download_enabled(self):
        return True
