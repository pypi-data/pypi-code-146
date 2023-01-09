import warnings

from django.db import models


from ..core.constants import PaymentPayer
from ..core.base_models import BaseModelNew
from . import APP_LABEL


class Coupon(BaseModelNew):
    '''
    优惠券
    '''

    def __init__(self, *args, **kwargs):
        warnings.warn("Coupon 须解耦, 请使用服务间调用请求积分数据", DeprecationWarning)
        return super().__init__(self, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        warnings.warn("Coupon 须解耦, 请使用服务间调用请求积分数据", DeprecationWarning)
        return super().__new__(cls, *args, **kwargs)

    title = models.CharField(
        "优惠券名字", max_length=100, blank=True, null=True)
    # description会给用户展示
    description = models.CharField(
        "优惠券描述", max_length=500, blank=True, null=True)
    discount_amount = models.PositiveIntegerField(
        '折扣金额',
        blank=True, null=True)
    # image = models.ImageField("logo", upload_to=settings.SPARROW_COUPON, blank=True, null=True)
    image_id = models.PositiveIntegerField("优惠券图片", blank=True, null=True)
    # 条件
    c_payment = models.DecimalField(
        "金额条件",
        decimal_places=2, max_digits=12,
        default=0.00)
    # 库存
    count = models.PositiveIntegerField('优惠券总数', default=0)
    # 费用承担方
    payer = models.CharField(
        "费用承担方", max_length=10,
        choices=PaymentPayer.PAYER_CHOICES,
        default=PaymentPayer.HG)
    # 有效期
    start_time = models.DateField("开始时间", blank=True, null=True)
    end_time = models.DateField("结束时间", blank=True, null=True)
    created_time = models.DateTimeField("Created Time",
                                        auto_now_add=True)

    class Meta:
        app_label = APP_LABEL

    # TODO: @property

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.id, self.title, self.description)
