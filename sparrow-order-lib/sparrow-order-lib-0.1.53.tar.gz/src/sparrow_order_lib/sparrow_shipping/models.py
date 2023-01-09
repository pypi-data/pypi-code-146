import logging

from django.db import models

from ..core.common_utils import get_uuid4_hex
from ..core.constants import PaymentPayer
from ..core.base_models import BaseModelNew
from ..core.base_models import BaseModelTimeAndDeleted
from .constants import ShippingPartnerCodes
from .constants import PrintStatus
from .constants import express_pay_method
from . import APP_LABEL

logger = logging.getLogger(__name__)


class ExpressPartner(models.Model):
    '''
    快递公司/类型
    '''

    SHIPPING_PARTNER_CHOICES = (
        (ShippingPartnerCodes.SF, "顺丰"),
        (ShippingPartnerCodes.YTO, "圆通"),
        (ShippingPartnerCodes.ZTO, "中通"),
        (ShippingPartnerCodes.STO, "申通"),
    )

    name = models.CharField("快递供应商", max_length=10)
    code = models.CharField(
        "快递代码", max_length=64, choices=SHIPPING_PARTNER_CHOICES,
        default=ShippingPartnerCodes.ZTO)
    default_postage = models.DecimalField(
        '默认邮费', max_digits=8, decimal_places=2, default=12.00)
    insurance = models.DecimalField(
        '保价费率', max_digits=12, decimal_places=4, default=0)
    if_default_partner = models.BooleanField('默认合伙人', default=False)
    default_pay_card_number = models.CharField("默认月结卡号", max_length=528, blank=True, null=True, default="")
    # default_user_code = models.CharField("默认顾客编码", max_length=528, blank=True, null=True, default="")
    # default_check_code = models.CharField("默认校验码", max_length=528, blank=True, null=True, default="")
    # 排列顺序
    seq = models.IntegerField('排序', default=99)
    if_auto = models.BooleanField('是否已对接自动下单', default=False)

    class Meta:
        app_label = APP_LABEL


class ExpressOrder(BaseModelNew):
    '''
    运单，暂时不留和订单的关系，只留存和发货单的一对一关系
    '''
    PRINTED_STATUS = (
        (PrintStatus.NEW, "新运单"),
        (PrintStatus.PRINTING, "发起打印"),
        (PrintStatus.PRINTED, "已打印"),
    )
    assignment_id = models.PositiveIntegerField("发货单ID", unique=True, db_index=True, blank=True, null=True)
    expresspartner_id = models.PositiveIntegerField("ExpressPartner Id", db_index=True, blank=True, null=True)
    # 这两条要存，是因为运单需要是快照，不随其他表的变动而变动
    express_name = models.CharField("快递供应商", max_length=20, blank=True, null=True)
    express_code = models.CharField(
        "快递代码", max_length=64, blank=True, null=True)
    shipping_number = models.CharField("快递单号/母单号", max_length=64, blank=True, null=True)
    # 邮费 —— 用来给财务统计的实际包裹到底收取了多少邮费。和用户订单无关
    postage = models.DecimalField(
        "邮费",
        decimal_places=2, max_digits=12, blank=True, null=True)
    insurance = models.DecimalField(
        "保费",
        decimal_places=4, max_digits=14, blank=True, null=True)
    print_status = models.CharField(
        "是否打印运单",
        choices=PRINTED_STATUS,
        max_length=20,
        default=PrintStatus.NEW,
    )
    printed_time = models.DateTimeField("运单打印时间", auto_now=True)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("更新时间", auto_now=True)
    # 订单号，用来配合serial_number发给快递公司生成快递单号
    order_number = models.CharField("麻雀订单号", max_length=64, blank=True, null=True)
    # 用来对快递公司接口下单的时候，需要填入订单号时候用，传入的应该是 get_express_order_number 以后的值
    # 每次调用接口下单之前都调用 generate_serial_number 更新 serial_number 再下单
    # 如果手动填的快递单号，不需要对serial_number进行任何更改。就算对同一个订单邮寄了5个包裹，填入了5个快递单号，
    # 也不需要更改 serial_number，就都是1就行了。只有当调用快递接口自动下单的时候再调 generate_serial_number 修改。
    serial_number = models.PositiveSmallIntegerField("同一个麻雀订单用快递公司接口下单时候的序列数", default=1)

    class Meta:
        app_label = APP_LABEL


class NewExpressOrder(BaseModelTimeAndDeleted):
    '''
    运单，暂时不留和订单的关系，只留存和发货单的一对一关系
    '''
    PRINTED_STATUS = (
        (PrintStatus.NEW, "新运单"),
        (PrintStatus.PRINTING, "发起打印"),
        (PrintStatus.PRINTED, "已打印"),
    )
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # 快递公司中文
    express_name = models.CharField("快递供应商", max_length=20, blank=True, null=True)
    # 快递公司编码
    express_code = models.CharField("快递代码", max_length=64, blank=True, null=True)
    # 运单号
    shipping_number = models.CharField("快递单号/母单号", max_length=64, blank=True, null=True)
    # 邮费 —— 用来给财务统计的实际包裹到底收取了多少邮费。和用户订单无关
    postage = models.DecimalField("邮费", decimal_places=2, max_digits=12, blank=True, null=True)
    # 投保金额
    insurance_price = models.DecimalField("保价金额", decimal_places=2, max_digits=12, blank=True, null=True)
    # 保费(汉光交给第三方快递按保价金额计算的保费)
    insurance = models.DecimalField("保费",decimal_places=4, max_digits=14, blank=True, null=True)
    # 费用承担方
    payer = models.CharField("费用承担方", max_length=10, choices=PaymentPayer.PAYER_CHOICES, default=PaymentPayer.HG)
    # 付费方式（到付、寄付）
    pay_method = models.CharField("付费方式", max_length=50, choices=express_pay_method.EXPRESS_PAY_METHOD_CHOISE, default=express_pay_method.SENDER_PAY)
    # 打印状态
    print_status = models.CharField("是否打印运单",choices=PRINTED_STATUS,max_length=20,default=PrintStatus.NEW,)
    # 打印时间
    printed_time = models.DateTimeField("运单打印时间", auto_now=True)
    #支付账号
    pay_card_number = models.CharField("支付账号", max_length=64, blank=True, null=True)
    # 账号名称
    account = models.CharField("账号名称", max_length=64, blank=True, null=True, default="")
    # 下订单使用的id
    source_id = models.CharField('源ID', max_length=100,  blank=True, null=True)
    # 是否已揽收
    if_delivered = models.BooleanField("是否已揽收", default=False)
    # 揽收时间
    delivered_time = models.DateTimeField("揽收时间", blank=True, null=True, default=None)
    # 邮件地址
    shipping_address_province = models.CharField("邮件省", max_length=64, blank=True, null=True)
    shipping_address_city = models.CharField("邮件市", max_length=64, blank=True, null=True)
    shipping_address_district = models.CharField("邮件区", max_length=64, blank=True, null=True)
    shipping_address_detail = models.CharField("邮件详细地址", max_length=512, blank=True, null=True)
    shipping_address_name = models.CharField("邮件收件人", max_length=64, blank=True, null=True)
    shipping_address_phone = models.CharField("邮件收件人手机号", max_length=64, blank=True, null=True)
    # 同步信息
    sync_status = models.BooleanField('同步状态', default=False)
    sync_time = models.DateTimeField('同步时间', null=True, blank=True)

    class Meta:
        app_label = APP_LABEL


class ExpressSpecialPayConfig(BaseModelTimeAndDeleted):
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # 快递公司编码
    express_code = models.CharField("快递代码", max_length=64, blank=True, null=True)
    # 快递公司名称
    express_name = models.CharField("快递名称", max_length=64, blank=True, null=True)
    # 账号编码
    pay_card_number = models.CharField("账号编码", max_length=528, blank=True, null=True, default="")
    # 账号名称
    account = models.CharField("账号名称", max_length=64, blank=True, null=True, default="")
    # 顾客编码
    # pay_user_code = models.CharField("顾客编码", max_length=528, blank=True, null=True, default="")
    # 校验码
    # pay_check_code = models.CharField("校验码", max_length=528, blank=True, null=True, default="")
    # shop_id(专柜id)
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True)
    # shop_num(专柜号)
    shop_num = models.CharField("Shop number", max_length=128, blank=True)
    # shop_name(专柜名称)
    shop_name = models.CharField("Shop Name", max_length=128, blank=True)
    # operator_id(操作人ID)
    operator_id = models.CharField("操作人ID", max_length=128, blank=True)
    # operator_name（操作人姓名）
    operator_name = models.CharField("操作人姓名", max_length=128, blank=True)

    class Meta:
        app_label = APP_LABEL
