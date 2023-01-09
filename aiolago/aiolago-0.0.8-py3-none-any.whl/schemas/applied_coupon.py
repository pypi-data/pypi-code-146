from typing import Optional, Type
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty

__all__ = [
    'AppliedCoupon',
    'AppliedCouponResponse',
    'AppliedCouponRoute',
]

class AppliedCoupon(BaseResource):
    external_customer_id: str
    coupon_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    percentage_rate: Optional[float]
    frequency: Optional[str]
    frequency_duration: Optional[int]


class AppliedCouponResponse(BaseResource):
    lago_id: str
    lago_coupon_id: str
    coupon_code: str
    external_customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_currency: str
    expiration_date: Optional[str]
    created_at: str
    terminated_at: Optional[str]
    percentage_rate: Optional[float]
    frequency: Optional[str]
    frequency_duration: Optional[int]

class AppliedCouponRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = AppliedCoupon
    response_model: Optional[Type[BaseResource]] = AppliedCouponResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'applied_coupons'

    @lazyproperty
    def root_name(self):
        return 'applied_coupon'