from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'Coupon',
    'CouponResponse',
    'CouponRoute',
]

class Coupon(BaseResource):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    expiration: Optional[str]
    expiration_date: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    frequency: Optional[str]
    frequency_duration: Optional[int]


class CouponResponse(BaseResource):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    expiration: str
    expiration_date: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    frequency: Optional[str]
    frequency_duration: Optional[int]


class CouponRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Coupon
    response_model: Optional[Type[BaseResource]] = CouponResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'coupons'

    @lazyproperty
    def root_name(self):
        return 'coupon'
