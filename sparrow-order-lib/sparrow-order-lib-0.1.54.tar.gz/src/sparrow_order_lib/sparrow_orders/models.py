import time
import random
import datetime
import logging
from decimal import Decimal
from collections import defaultdict


from django.db import models
from django.db.models import Sum
from django.db import transaction
from django.conf import settings
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from ..core.model_function import get_object_or_None
from ..core.common_utils import get_setting_value
from ..core.common_utils import get_uuid4_hex
from ..core.base_models import BaseModelTimeAndDeleted
from ..core.base_models import BaseModelNew
from ..core.base_models import AbstractAddress
from ..core.constants import ShippingMethod
from ..core.constants import MemberLevel
from ..core.constants import PayType
from ..core.constants import LogLevel
from ..sparrow_promotions.models import Coupon
from .constants import OrderShippingStatus
from .constants import OrderPayStatus
from .constants import OrderAssignStatus
from .constants import OrderAftersaleStatus
from .constants import OrderGroupStatus
from .constants import OrderTypes
from .constants import OrderExchangeStatus
from .constants import PayMethod
from .constants import DeliverTimeStatus
from .constants import CouponSource
from .constants import PayStepType
from .constants import ReversedStockStatus
from .constants import ReversedStockType
from .constants import ReversedStockActions
from .constants import AssignmentStatus
from .constants import AssignmentActions
from ..sparrow_aftersale.constants import AftersaleStatus
from ..sparrow_aftersale.constants import AftersaleFinanceStatus
from ..sparrow_aftersale.constants import AftersaleRefundStatus
from ..sparrow_aftersale.constants import AftersaleFinanceType
from ..sparrow_aftersale.constants import AftersaleSource
from ..sparrow_aftersale.constants import AftersaleCancelSource
from ..sparrow_aftersale.constants import AfterSaleType
from ..sparrow_aftersale.constants import AftersaleActions
from .constants import OrderActions
from .constants import SettingsLabel
from .constants import BatchAssignTaskStatus
from .constants import BatchAssignType
from .constants import DeliverTimeType
from .constants import HGVendingStatus
from .constants import Order_Number_Pay_Status
from . import APP_LABEL
from . import APP_LABEL_AFS


# 限制在 sparrow_orders 里面可以创建的 models
# 包含 APP_LABEL='sparrow_orders' 和 'sparrow_orders_afs'
__all__ = ['OrderNumber',
           'ShippingAddress',
           'OrderContact',
           'Order',
           'OrderPayment',
           'LineOrderPayment',
           'ReversedStock',
           'ReversedStockNote',
           'Assignment',
           'LineAssignment',
           'OrderPromotionGiftAssignment',
           'AssignmentNote',
           'AfterSale',
           'LineAfterSale',
           'CouponToCharge',
           'CouponToReturn',
           'AfterSaleNote',
           'AfterSaleHgIncomeDetail',
           'AfterSaleHgIncomeType',
           'Line',
           'OrderPromotion',
           'OrderPromotionCoupon',
           'OrderPromotionGiftProduct',
           'OrderPromotionGift',
           'OrderPromotionFixedPriceProduct',
           'LineOrderPromotion',
           'OrderNote',
           'Inventory',
           'Settings',
           'AfterSalePayment',
           'AfterSalePaymentCharge',
           'AfterSalePaymentReturn',
           'LineAfterSalePayment',
           'LineAfterSalePaymentReturn',
           'AfterSaleAlipayRefund',
           'BatchAssignTask',
           'GroupPickUpRecord',
           'OrderPaymentInst',
           'LineOrderPaymentInst',
           # 以下为 sparrow_orders_afs
           'InventoryV3',
           'VendingHROrder',
           'HGVending',
           'OrderScene',
           'OrderStepPay',
           'LineStepPay',
           'LineDeliverTime',
           ]


logger = logging.getLogger(__name__)


SPARROW_ORDER_NUMBER_NAME = "SPARROW_ORDER_NUMBER_NAME"
SPARROW_AFTERSALE_NUMBER = "SPARROW_AFTERSALE_NUMBER"
SPARROW_DISTRIBUTE_NUMBER = "SPARROW_DISTRIBUTE_NUMBER"


def generate_order_number():
    '''
    该函数没有用了，但是不能动，migration文件里面有引用。
    '''
    order_number = str(int(time.time() * 100)) + str(int(random.random() * 1000))
    return order_number


def generate_aftersale_number():
    '''
    退货单店内系统也需要单号
    '''
    '''注册单号, 避免并发事务冲突'''
    # order_number_model, is_created = OrderNumber.objects.get_or_create(
    #     name=SPARROW_AFTERSALE_NUMBER,
    # )
    # order_number = order_number_model.create_aftersale_number()
    # return order_number
    created_time, sn = update_serial_number_or_incr(name=SPARROW_AFTERSALE_NUMBER)
    order_number = created_time.strftime('%y%m%d') + get_setting_value("SPARROW_AFTERSALE_NUMBER") + sn
    return order_number


def get_sparrow_order_number():
    '''注册订单号, 避免并发事务冲突'''
    order_number_model, is_created = OrderNumber.objects.get_or_create(
        name=SPARROW_ORDER_NUMBER_NAME,
    )
    order_number = order_number_model.create_order_number()
    return order_number


def get_sparrow_distribute_number():
    '''注册发货单号, 避免并发事务冲突'''
    order_number_model, is_created = OrderNumber.objects.get_or_create(
        name=SPARROW_AFTERSALE_NUMBER,
    )
    order_number = order_number_model.create_distribute_number()
    return order_number


def update_serial_number_or_incr(name):
    OrderNumber.objects.get_or_create(name=name)
    with transaction.atomic():
        order_number_model = OrderNumber.objects.filter(name=name).select_for_update().first()
        if order_number_model.created_time.date() == datetime.date.today():
            # 今天
            order_number_model.serial_number += 1
        else:
            order_number_model.created_time = datetime.datetime.now()
            order_number_model.serial_number = 1
        if get_setting_value("IS_TEST_ENV"):
            sn = str(order_number_model.serial_number).zfill(8)
        else:
            sn = str(order_number_model.serial_number).zfill(5)
        order_number_model.save()
    return order_number_model.created_time, sn


class OrderNumber(models.Model):
    '''由于线下订单采用的是顺序生成订单号，并且跟日期相关，这里采用数据库共享的方式来生成订单号'''
    name = models.CharField("order name", max_length=30)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    serial_number = models.PositiveIntegerField('serial number', default=0)

    class Meta:
        app_label = APP_LABEL

    def create_order_number(self):
        # import pdb; pdb.set_trace()
        order_number = ""
        if self.created_time.date() == datetime.date.today():
            # 今天
            self.serial_number += 1
        else:
            # 重新开始序号和日期
            self.created_time = datetime.datetime.now()
            self.serial_number = 1
        self.save()
        if get_setting_value("IS_TEST_ENV"):
            sn = str(self.serial_number).zfill(8)
        else:
            sn = str(self.serial_number).zfill(5)
        order_number = self.created_time.strftime('%y%m%d') + get_setting_value("SPARROW_ORDER_NUMBER") + sn
        return order_number

    def create_aftersale_number(self):
        # import pdb; pdb.set_trace()
        order_number = ""
        if self.created_time.date() == datetime.date.today():
            # 今天
            self.serial_number += 1
        else:
            # 重新开始序号和日期
            self.created_time = datetime.datetime.now()
            self.serial_number = 1
        self.save()
        if get_setting_value("IS_TEST_ENV"):
            sn = str(self.serial_number).zfill(8)
        else:
            sn = str(self.serial_number).zfill(5)
        order_number = self.created_time.strftime('%y%m%d') + get_setting_value("SPARROW_AFTERSALE_NUMBER") + sn
        return order_number

    def create_distribute_number(self):
        # import pdb; pdb.set_trace()
        order_number = ""
        if self.created_time.date() == datetime.date.today():
            # 今天
            self.serial_number += 1
        else:
            # 重新开始序号和日期
            self.created_time = datetime.datetime.now()
            self.serial_number = 1
        self.save()
        if get_setting_value("IS_TEST_ENV"):
            sn = str(self.serial_number).zfill(8)
        else:
            sn = str(self.serial_number).zfill(5)
        order_number = self.created_time.strftime('%y%m%d') + get_setting_value("SPARROW_DISTRIBUTE_NUMBER") + sn
        return order_number


class ShippingAddress(AbstractAddress):
    '''
    订单的地址快照
    这个表有数据！！不要认为pass就没用！有数据的在base表里！
    '''

    class Meta:
        app_label = APP_LABEL


class OrderContact(models.Model):
    '''到店自提和闪购的联系人订单快照表'''

    PHONE_NUMBER_REGEX = r"1[0-9]{10}"

    name = models.CharField(
        '姓名',
        max_length=64,
        blank=True,
        null=True
    )
    phone = models.CharField(
        '联系人手机号',
        max_length=11,
        unique=False,
        validators=[
            validators.RegexValidator(
                PHONE_NUMBER_REGEX,
                '手机号输入有误，请重新输入',
            ),
        ],
    )

    class Meta:
        app_label = APP_LABEL


class Order(BaseModelTimeAndDeleted):
    '''
    订单
    '''
    # 支付状态
    PAY_STATUS = (
        (OrderPayStatus.UNPAID, "未支付"),
        (OrderPayStatus.PAY_FINISHED, "支付已完成"),
        (OrderPayStatus.CLOSED, "订单关闭"),
    )
    # 配货状态
    ASSIGN_STATUS = (
        (OrderAssignStatus.INIT, "无配货"),
        (OrderAssignStatus.PARTIAL, "部分配货"),
        (OrderAssignStatus.COMPLETED, "全部配货"),
    )
    # 发货状态
    SHIPPING_STATUS = (
        (OrderShippingStatus.INIT, "无发货"),
        (OrderShippingStatus.PARTIAL, "部分发货"),
        (OrderShippingStatus.COMPLETED, "全部发货"),
    )
    # 售后状态
    AFTERSALE_STATUS = (
        (OrderAftersaleStatus.OPEN, "有待处理售后"),
        (OrderAftersaleStatus.NONE, "无待处理售后"),
        (OrderAftersaleStatus.DONE, "有售后且完成"),
    )
    # 拼团状态
    GROUP_STATUS = (
        (OrderGroupStatus.PROGRESS, "拼团中"),
        (OrderGroupStatus.SUCCESS, "已成团"),
        (OrderGroupStatus.FAIL, "拼团失败"),
    )
    TYPE_CHOICES = (
        (OrderTypes.ONLINE, "线上订单"),
        (OrderTypes.FLASHSALE, "闪购订单"),
        (OrderTypes.VENDING, "自动售货机"),
        (OrderTypes.SCREEN, "互动触控屏"),
        (OrderTypes.GROUP, "拼团订单"),
    )
    MEMBER_CHOICES = (
        (MemberLevel.MEMBER_L0, '基础会员'),
        (MemberLevel.MEMBER_L1, '普卡会员'),
        (MemberLevel.MEMBER_L2, '银卡会员'),
    )
    # 订单号的生成不在采用自动生成的方式。事务并发的时候
    number = models.CharField(
        "Order number", max_length=128, db_index=True,
        unique=True, default=generate_order_number)
    user_id = models.CharField(
        "User Id",
        max_length=100, db_index=True)
    # 指 ShippingAddress 的地址快照ID
    shipping_address_id = models.PositiveIntegerField(
        'Shipping Address Id', blank=True, null=True,
        db_index=True)
    # 闪购和自提的联系人
    contact_id = models.PositiveIntegerField(
        'Order Contact Id', blank=True, null=True,
        db_index=True)
    flashsale_guide_id = models.CharField(
        "闪购提货导购",
        max_length=100, blank=True, null=True, db_index=True)
    # 邮寄方式
    shipping_method = models.CharField(
        "Shipping method",
        max_length=128, choices=ShippingMethod.CHOICES,
        blank=True, null=True)
    # 邮费
    postage = models.DecimalField(
        "Postage",
        decimal_places=2, max_digits=12, default=0.00)
    # 订单支付状态
    pay_status = models.CharField(
        "订单支付状态",
        max_length=100, default=OrderPayStatus.UNPAID,
        choices=PAY_STATUS)
    # 订单配货状态，冗余出来这个状态进行订单查询
    assign_status = models.CharField(
        "订单配货状态",
        max_length=100, default=OrderAssignStatus.INIT,
        choices=ASSIGN_STATUS)
    # 订单发货状态，冗余出来这个状态进行订单查询
    shipping_status = models.CharField(
        "订单发货状态",
        max_length=128,
        choices=SHIPPING_STATUS,
        blank=True, null=True, default=OrderShippingStatus.INIT)
    # 订单售后状态，冗余出来这个状态进行订单查询
    aftersale_status = models.CharField(
        "订单售后状态",
        max_length=128,
        choices=AFTERSALE_STATUS,
        blank=True, null=True, default=OrderAftersaleStatus.NONE)
    # 2019-09-14增加拼团类型订单，并且拼团订单有三种状态
    group_status = models.CharField(
        "拼团状态",
        max_length=128,
        choices=GROUP_STATUS,
        blank=True, null=True, default=None)
    # 订单总金额——所有活动优惠之前的金额——不含邮费！
    total_amount = models.DecimalField(
        "Total Amount",
        decimal_places=2, max_digits=12)
    # total_amount, actual_amount, cash_pay_amount 三个字段都不包含运费
    # 用户实付金额——包含所有支付方式，比如优惠券——不含邮费！ps:比如订单总金额打完折后的价格
    actual_amount = models.DecimalField(
        "Actual Amount",
        decimal_places=2, max_digits=12)
    # 用户现金支付的金额，微信，支付宝，银行卡等——不含邮费！
    cash_pay_amount = models.DecimalField(
        "Cash Pay Amount",
        decimal_places=2, max_digits=12)
    # # 创建日期
    # created_time = models.DateTimeField(
    #     "Date Created",
    #     auto_now_add=True)
    # # 更新日期
    # updated_time = models.DateTimeField(
    #     "Date Updated",
    #     auto_now=True)
    # 订单类型
    order_type = models.CharField(
        '订单类型', max_length=64, choices=TYPE_CHOICES, default=OrderTypes.ONLINE)

    # 顾客给订单的备注
    note = models.CharField("备注", max_length=512,
                            blank=True, null=True)
    # 客服给订单的备注
    operator_note = models.CharField(
        "客服备注", max_length=512,
        blank=True, null=True)
    # 订单同步信息
    sync_status = models.BooleanField('同步状态', default=False)
    sync_time = models.DateTimeField('订单同步时间', null=True, blank=True)
    # 订单完成时间，指发货时间，自提时间
    completed_time = models.DateTimeField('订单完成时间', null=True, blank=True)
    # 订单的平台来源
    client_app_id = models.CharField(
        '订单的平台来源(client_app_id)', max_length=40, blank=True, null=True)
    is_unpaid_warned = models.BooleanField('是否已经发了未支付提醒短信', default=False)

    # 存在有效的待配货
    has_valid_to_assign = models.BooleanField('存在有效的待配货', default=False)

    # 存在有效的待发货
    has_valid_to_shipping = models.BooleanField('存在有效的待发货', default=False)

    # 订单换货状态，冗余出来这个状态进行订单查询
    exchange_status = models.CharField(
        "订单换货状态",
        max_length=128,
        choices=OrderExchangeStatus.EXCHANGE_STATUS,
        blank=True, null=True, default=OrderExchangeStatus.NONE)

    # 支付方法（once 一次支付/twice两次支付）
    pay_method = models.CharField("支付方法", max_length=24, choices=PayMethod.PAY_METHOD_CHOICES, blank=True, null=True, default=PayMethod.ONCE)
    #  发货时间配置状态(none无需配置/to_configure待配置/configured已配置)
    delivertime_status = models.CharField("发货时间配置状态", max_length=24, choices=DeliverTimeStatus.DELIVERTIME_STATUS_CHOICES, blank=True, null=True, default=DeliverTimeStatus.NONE)

    # 退货重算-订单版本号
    order_version = models.CharField("订单版本号", max_length=12, blank=True, null=True, db_index=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']

    def __str__(self):
        return self.number


class OrderPayment(models.Model):
    """
    该表记录下来了订单所有的支付方式
    """
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    # 订单自增id
    order_id = models.PositiveIntegerField(
        _('Order ID'), blank=True, null=True)
    # 支付类型
    payment_type = models.CharField(
        "Payment type", max_length=10,
        choices=PayType.PAYMENT_TYPE_CHOICES,
        default=PayType.TO_PAY,
        db_index=True
    )
    # 支付金额
    amount = models.DecimalField(
        "Amount", decimal_places=2, max_digits=12)
    # 用来记录支付的详细信息：
    #   优惠券：优惠券ID coupon_id
    #   店内优惠券存 code
    #   C券：用户 account_id
    #   微信支付：用户 微信支付ID
    #   支付宝支付：用户 支付宝支付ID
    payment_num = models.CharField('支付号', max_length=50, blank=True, null=True)
    # 如果是券的话，券的来源
    coupon_source = models.CharField(
        '来源', max_length=64, blank=True, null=True,
        choices=CouponSourceChoices, default=CouponSource.IN_STORE)
    # 优惠券面值
    coupon_amount = models.PositiveIntegerField('优惠券面值', blank=True, null=True)
    note = models.CharField('备注', max_length=200, blank=True, null=True)
    # 如果支付方式是礼券，对应于：S001_OrderPayDetail中的Objid，其他默认为0
    # 信息部的字段
    list_id = models.IntegerField('List ID', default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)
    # 财务需要知道我们真正收到钱的时间
    cash_received_time = models.DateTimeField(
        "收到现金类支付的时间", blank=True, null=True, db_index=True)
    # 支付账号（支付现金类的数据，才有此值，退款时需要用原支付账号退回）
    pay_channel = models.CharField('支付账号', max_length=50, blank=True, null=True)

    # order_number 订单编号
    order_number = models.CharField("订单编号", max_length=64, blank=True, null=True)
    # order_number_pay 子支付订单编号(订单编号加“-1”或者“-2”)
    order_number_pay = models.CharField("子支付订单编号", max_length=64, blank=True, null=True)
    # pay_step_type 支付阶段类型(all全款/deposit定金/tailpay尾款)
    pay_step_type = models.CharField("Pay Step Type", max_length=24, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)
    # coupon_name 券名
    coupon_name = models.CharField("券名", max_length=128, blank=True, null=True)

    class Meta:
        # abstract = True
        app_label = APP_LABEL
        verbose_name = _("Order Payment")
        verbose_name_plural = _("Order Payment")
        ordering = ['-created_time']

    @property
    def coupon(self):
        coupon_id = None
        if self.coupon_source == CouponSource.ONLINE and self.payment_type == PayType.GIFT_COUPON:
            try:
                coupon_id = int(self.payment_num)
            except:
                logger.error('payment_num 字段存的应该是coupon id，现在不正确！OrderPayment id: {0}'.format(self.id))
                return None
        return get_object_or_None(Coupon, id=coupon_id)

    def __str__(self):
        return 'orderid_{0}--type_{1}--paymentnum_{2}'.format(
            self.order_id, self.payment_type, self.payment_num)

    @property
    def order(self):
        return get_object_or_None(Order, id=self.order_id)


class LineOrderPayment(models.Model):
    '''记录下来详细的 Line 支付结果 和所获取的积分'''

    # Line
    line_id = models.PositiveIntegerField(
        'Line ID', blank=True, null=True, db_index=True)
    # OrderPayment
    orderpayment_id = models.PositiveIntegerField('Order Payment ID', blank=True, null=True, db_index=True)
    # 支付类型
    payment_type = models.CharField("Payment type", max_length=10, blank=True, null=True)
    # 如果是钱类的，就存金额。如果是积分支付，就用amount存积分
    amount = models.DecimalField("Amount", decimal_places=2, max_digits=12)
    # order_id 订单ID
    order_id = models.PositiveIntegerField(editable=False, blank=True, null=True, db_index=True)
    # order_number 订单编号
    order_number = models.CharField("Order number", blank=True, null=True, max_length=64)
    # order_number_pay 子支付订单编号(订单编号加“-1”或者“-2”)
    order_number_pay = models.CharField("子支付订单编号", blank=True, null=True, max_length=64)
    # pay_step_type 支付阶段类型(all全款/deposit定金/tailpay尾款)
    pay_step_type = models.CharField("Pay Step Type", max_length=24, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)
    # coupon_name 券名
    coupon_name = models.CharField("券名", max_length=128, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL

    @property
    def order_payment(self):
        return get_object_or_None(OrderPayment, id=self.orderpayment_id)

    @property
    def line(self):
        return get_object_or_None(Line, id=self.line_id)

    def __str__(self):
        desc = 'lineid%s' % self.line_id
        if self.order_payment:
            desc = desc + str(self.order_payment)
        return desc


# 负库存系统
class ReversedStock(BaseModelNew):
    '''
    负库存系统，记录各种sku的需求变化
    '''
    SKU_STATUS_CHOICES = (
        (ReversedStockStatus.INIT, '未处理'),
        (ReversedStockStatus.SHORTAGE, '缺货'),
        (ReversedStockStatus.OFF, '断货下架'),
        (ReversedStockStatus.PREPARED, '有货可提'),
    )
    SKU_TYPE_CHOICES = (
        (ReversedStockType.PRODUCT, '商品'),
        (ReversedStockType.GIFT, '赠品'),
    )
    brand_id = models.PositiveIntegerField(
        'Brand ID', blank=True, null=True, db_index=True)
    shop_id = models.PositiveIntegerField(
        'Shop ID', blank=True, null=True, db_index=True)
    product_id = models.PositiveIntegerField(
        'Product ID', blank=True, null=True, db_index=True)
    # 2019-11-02 添加货号快照
    shop_sku = models.CharField(
        _("货号"), max_length=1024, blank=True, null=True, db_index=True)
    # 中分类
    offer = models.CharField("中分类", max_length=2, default="0", db_index=True)
    gift_id = models.PositiveIntegerField(
        'Gift ID', blank=True, null=True, db_index=True, unique=True)
    product_type = models.CharField('sku类型', max_length=31, blank=True, null=True,
                                    choices=SKU_TYPE_CHOICES, default=ReversedStockType.PRODUCT)
    # 用户拍了，我们需要去提的负库存-允许超提，所以可以是负值
    required_count = models.IntegerField(
        '需求库存', blank=True, null=True, default=0)
    # 我们已提到自己货架上的库存
    stock = models.PositiveIntegerField(
        '已有库存', blank=True, null=True, default=0)
    status = models.CharField('货品状态', max_length=31, blank=True, null=True,
                              choices=SKU_STATUS_CHOICES, default=ReversedStockStatus.INIT)
    created_time = models.DateTimeField("Datetime Created", auto_now_add=True)
    updated_time = models.DateTimeField("Datetime Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL

    def __str__(self):
        if self.product_type == ReversedStockType.PRODUCT:
            return self.product.title if self.product else ''
        else:
            return self.gift.title if self.gift else ''


class ReversedStockNote(models.Model):
    '''
    负库存各操作的日志
    记录导购和客服
    '''
    ACTION_CHOICES = (
        (ReversedStockActions.GUIDE_MARK, '导购标记'),
        (ReversedStockActions.PICK_UP, '客服提货'),
        (ReversedStockActions.RETURN, '客服还货'),
    )
    user_id = models.CharField(
        "User Id", max_length=100, blank=True, null=True, db_index=True)
    reversed_stock_id = models.IntegerField('负库存ID',
                                            blank=True, null=True, db_index=True)
    action = models.CharField(
        'Action', max_length=128, blank=True, null=True, choices=ACTION_CHOICES, db_index=True)
    # 所有库存数量都用这个字段
    pick_up_count = models.IntegerField('操作库存数量',
                                        blank=True, null=True, db_index=True)
    message = models.CharField(
        'Message', max_length=256, blank=True, null=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)

    class Meta:
        app_label = APP_LABEL

    @property
    def stock(self):
        return get_object_or_None(ReversedStock, id=self.reversed_stock_id)

    @property
    def user(self):
        return get_object_or_None(get_user_model(), id=self.user_id)


class Assignment(models.Model):
    '''
    配货表
    订单对配货表一对多，配货表对line是多对多，经过LineAssignment关系表
    每次都需要记录在OrderNote里，支持修改和删除
    '''
    SHIPPING_STATUS = (
        (AssignmentStatus.READY, "已配货"),
        (AssignmentStatus.COMPLETED, "已发或已提"),
        (AssignmentStatus.CLOSED, "已关闭取消"),
    )
    order_id = models.PositiveIntegerField(
        'Order ID', blank=True, null=True, db_index=True)
    # shipping 状态
    shipping_status = models.CharField(
        "发货单邮寄状态",
        max_length=128,
        choices=SHIPPING_STATUS,
        blank=True, null=True, default=AssignmentStatus.READY)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL

    # TODO: @property
    # @property
    # def express_order(self):
    #     from sparrow_shipping.models import ExpressOrder
    #     express_order = get_object_or_None(ExpressOrder, assignment_id=self.id)
    #     return express_order

    @property
    def order(self):
        order = get_object_or_None(
            Order, id=self.order_id)
        return order

    @property
    def shipping_address(self):
        order = self.order
        if not order:
            return None
        address = get_object_or_None(
            ShippingAddress, id=order.shipping_address_id)
        return address

    @property
    def shipping_method(self):
        shipping_method = self.order.shipping_method
        return shipping_method

    @property
    def line_assignments(self):
        return LineAssignment.objects.filter(assignment_id=self.id)

    # 不要注释！！不要删除！兼容历史订单赠品！
    @property
    def gift_assignments(self):
        return OrderPromotionGiftAssignment.objects.filter(assignment_id=self.id)

    @property
    def assignment_notes(self):
        return AssignmentNote.objects.filter(assignment_id=self.id)


class LineAssignment(models.Model):
    '''
    Assignment 和 Line 的关系表
    '''
    assignment_id = models.PositiveIntegerField(
        'Assignment ID', blank=True, null=True, db_index=True)
    line_id = models.PositiveIntegerField(
        'Line Id', blank=True, null=True, db_index=True)
    quantity = models.IntegerField('件数', default=1)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL

    @property
    def line(self):
        return get_object_or_None(Line, id=self.line_id)


# 不要注释！！不要删除！兼容历史订单赠品！
class OrderPromotionGiftAssignment(models.Model):
    '''
    Assignment 和 OrderPromotionGift 的关系表
    # 不要注释！！不要删除！兼容历史订单赠品！
    '''
    assignment_id = models.PositiveIntegerField(
        'Assignment ID', blank=True, null=True, db_index=True)
    orderpromotiongift_id = models.PositiveIntegerField(
        'Orderpromotiongift Id', blank=True, null=True, db_index=True)
    # OrderPromotionGift 里的quantity是那个活动送了几个赠品
    # 而这个 quantity 是说 这个配货包裹里有几个这个赠品，这个数量上限应该是 OrderPromotionGift 里的quantity
    quantity = models.IntegerField('件数', default=1)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL

    @property
    def orderpromotiongift(self):
        return get_object_or_None(OrderPromotionGift, id=self.orderpromotiongift_id)

    @property
    def assignment(self):
        return get_object_or_None(Assignment, id=self.assignment_id)


class AssignmentNote(models.Model):
    '''
    配货的日志
    '''
    ACTION_CHOICES = (
        (AssignmentActions.CREATE, '创建发货单'),
        (AssignmentActions.REMOVE, '关闭发货单'),
        (AssignmentActions.COMPLETE, '完成发货单'),
        (AssignmentActions.PRINTED, '打印发货单'),
    )
    user_id = models.CharField(
        "User Id", max_length=100, blank=True, null=True, db_index=True)
    order_id = models.IntegerField('订单ID',
                                   blank=True, null=True, db_index=True)
    assignment_id = models.IntegerField('Assignment ID',
                                        blank=True, null=True, db_index=True)
    line_assignment_id = models.IntegerField('Line Assignment ID',
                                             blank=True, null=True, db_index=True)
    action = models.CharField(
        'Action', max_length=128, blank=True, null=True, choices=ACTION_CHOICES, db_index=True)
    message = models.CharField(
        'Message', max_length=256, blank=True, null=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)

    class Meta:
        app_label = APP_LABEL

    @property
    def user(self):
        return get_object_or_None(get_user_model(), id=self.user_id)


class AfterSale(models.Model):
    '''
    售后单
    和 Line 是多对多的关系
    和 Order 是多对一的关系

    attr startwith "_batch" such as "_batch_line_after_sales" is a trick for batch operation
    '''
    AFTERSALE_STATUS_CHOICES = (
        (AftersaleStatus.OPEN, "客服待审"),
        # (AftersaleStatus.IN_FINANCE, "财务待审"),
        # (AftersaleStatus.IN_FINANCE_2ND, "财务一审通过"),
        # (AftersaleStatus.REJECTED, "财务驳回"),
        (AftersaleStatus.PENDING_RETURN, "待退货"),
        (AftersaleStatus.PENDING_REFUND, "待退款"),
        (AftersaleStatus.INSTORE_APPROVED, "店内系统通过"),
        (AftersaleStatus.INSTORE_REJECTED, "店内系统驳回"),
        (AftersaleStatus.ALL_APPROVED, "店内系统通过"),
        (AftersaleStatus.REFUND_FAILED, "退款失败"),
        (AftersaleStatus.COMPLETED, "已完成"),
        (AftersaleStatus.CLOSED, "已取消"),
    )
    AFTERSALE_FINANCE_STATUS_CHOICES = (
        (AftersaleFinanceStatus.INIT, "财务未审"),
        (AftersaleFinanceStatus.APPROVED_1ST, "财务一审通过，待二审"),
        (AftersaleFinanceStatus.APPROVED, "财务二审通过"),
        (AftersaleFinanceStatus.REJECTED, "财务驳回")
    )
    REFUND_STATUS_CHOICES = (
        (AftersaleRefundStatus.INIT, "未退款"),
        (AftersaleRefundStatus.SUCCEEDED, "退款成功"),
        (AftersaleRefundStatus.FAILED, "退款失败")
    )
    AFTERSALE_FINANCE_TYPE_CHOICES = (
        (AftersaleFinanceType.AUTO, "正常退单"),
        (AftersaleFinanceType.MANUAL, "需要财务手动调账退款"),
    )
    AFTERSALE_SOURCE_CHOICES = (
        (AftersaleSource.GUEST_INITIATED, "客人发起"),
        (AftersaleSource.SERVICE_INITIATED, "客服发起"),
    )
    CANCEL_SOURCE_CHOICES = (
        (AftersaleCancelSource.GUEST_CANCEL, "客人取消"),
        (AftersaleCancelSource.SERVICE_CANCEL, "客服取消"),
        (AftersaleCancelSource.TIMEOUT_CANCEL, "超时自动取消"),
    )
    AFTERSALE_TYPE_CHOICES = (
        (AfterSaleType.NORMAL, "正常退款"),
        (AfterSaleType.EXCHANGE, "换货"),
        (AfterSaleType.COMPLAINT, "投诉"),
        (AfterSaleType.REMINDER, "提醒发货"),
    )
    number = models.CharField(
        "退单号", max_length=128, db_index=True,
        unique=True, default=generate_aftersale_number)
    order_id = models.PositiveIntegerField('Order ID', blank=True,
                                           null=True, db_index=True)
    status = models.CharField(
        "Status",
        max_length=128,
        choices=AFTERSALE_STATUS_CHOICES,
        blank=True,
        null=True,
        default=AftersaleStatus.OPEN)
    reason = models.CharField("reason", max_length=512, blank=True)
    postage = models.DecimalField("退的邮费", decimal_places=2, max_digits=12, default=0)
    creator_id = models.CharField(
        'Creator User Id', max_length=100, blank=True, null=True, db_index=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)
    operator_approve_time = models.DateTimeField("客服提交财务的时间", blank=True, null=True, db_index=True)
    # 财务审核的时间，可能是通过也可能是拒绝
    finance_approve_time = models.DateTimeField("财务二审通过的时间", blank=True, null=True, db_index=True)
    finance_approver_id = models.CharField(
        '财务二审人ID', max_length=100, blank=True, null=True, db_index=True)
    finance_first_approve_time = models.DateTimeField("财务一审通过的时间", blank=True, null=True, db_index=True)
    finance_first_approver_id = models.CharField(
        '财务一审人ID', max_length=100, blank=True, null=True, db_index=True)
    finance_status = models.CharField(
        "财务审核状态",
        max_length=128,
        choices=AFTERSALE_FINANCE_STATUS_CHOICES,
        blank=True,
        null=True,
        default=AftersaleFinanceStatus.INIT)
    finance_reject_reason = models.CharField("财务拒绝理由", max_length=512,
                                             blank=True, null=True)
    # 退款状态
    refund_status = models.CharField(
        "退款状态",
        max_length=128,
        choices=REFUND_STATUS_CHOICES,
        blank=True,
        null=True,
        default=AftersaleRefundStatus.INIT)
    # 财务要的退款时间，找财务确认是要发起微信退款的时间还是微信退款到账的时间
    # 应该是调起微信退款接口的时间
    refund_time = models.DateTimeField("发起退款的时间", blank=True, null=True, db_index=True)
    # 收到推送退款成功的时间，一期就是收到微信通知成功的时间
    refund_notified_time = models.DateTimeField("退款收到推送的时间", blank=True, null=True, db_index=True)
    # 售后单同步信息
    sync_status = models.BooleanField('同步状态', default=False)
    sync_time = models.DateTimeField('售后单同步时间', null=True, blank=True)
    store_reject_reason = models.CharField("店内系统拒绝理由", max_length=512,
                                           blank=True, null=True)
    # 客服给退单的备注
    operator_note = models.CharField(
        "客服备注", max_length=512,
        blank=True, null=True)
    finance_type = models.CharField(
        "财务类型",
        max_length=128,
        choices=AFTERSALE_FINANCE_TYPE_CHOICES,
        blank=True,
        null=True,
        default=AftersaleFinanceType.AUTO)
    hg_income_cash = models.DecimalField(
        "用户补给汉光的现金额", decimal_places=2, max_digits=12, default=0)
    # 需求版本v190611 增加 tracking_no, source, user_reason
    # 退货快递单号
    tracking_no = models.CharField("退货快递单号", max_length=64, blank=True, null=True)
    # 售后来源
    source = models.CharField(
        "售后来源",
        max_length=64,
        blank=True,
        null=True,
        choices=AFTERSALE_SOURCE_CHOICES,
        default="")
    # 申请原因
    user_reason = models.CharField("用户申请原因", max_length=512, blank=True, null=True)

    # status变为 待退货 时的时间
    pending_return_time = models.DateTimeField("待退货状态时间", blank=True, null=True, db_index=True)

    # 售后人
    aftersale_user = models.CharField("售后人", max_length=64, blank=True, null=True)

    # 售后人联系方式
    aftersale_phone = models.CharField("售后人联系方式", max_length=64, blank=True, null=True)

    # 取消售后来源
    cancel_source = models.CharField("取消售后来源", max_length=64, blank=True, null=True)

    # 售后类型
    aftersale_type = models.CharField("售后类型", max_length=128, choices=AFTERSALE_TYPE_CHOICES, blank=True, null=True, default=AfterSaleType.NORMAL)

    class Meta:
        app_label = APP_LABEL
        verbose_name = "Order After Sale"
        verbose_name_plural = "Order After Sale"

    @cached_property
    def coupons_to_charge(self):
        '''系统要扣除用户的优惠券'''
        # return Coupon.objects.filter(
        #     id__in=CouponToCharge.objects.filter(
        #         line_after_sale_id=self.id
        #     ).values_list('coupon_id', flat=True)
        # )
        if not self.id:
            return None
        return CouponToCharge.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_coupons_to_charge(cls, iterable):
        batch_map = defaultdict(list)
        qs = CouponToCharge.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def coupons_to_return(self):
        '''系统要返还用户的优惠券'''
        # return Coupon.objects.filter(
        #     id__in=CouponToReturn.objects.filter(
        #         line_after_sale_id=self.id
        #     ).values_list('coupon_id', flat=True)
        # )
        if not self.id:
            return None
        return CouponToReturn.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_coupons_to_return(cls, iterable):
        batch_map = defaultdict(list)
        qs = CouponToReturn.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @property
    def finance_first_approver(self):
        if not self.finance_first_approver_id:
            return None
        return get_object_or_None(get_user_model(), id=self.finance_first_approver_id)

    @property
    def finance_approver(self):
        if not self.finance_approver_id:
            return None
        return get_object_or_None(get_user_model(), id=self.finance_approver_id)

    @cached_property
    def creator(self):
        if not self.creator_id:
            return None
        return get_object_or_None(get_user_model(), id=self.creator_id)

    @classmethod
    def _batch_creator(cls, iterable):
        qs = get_user_model().objects.filter(id__in=[_.creator_id for _ in iterable if _])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.creator_id) for _ in iterable}

    def __str__(self):
        return 'orderid_{0}--aftersaleid_{1}'.format(self.order_id, self.id)

    @cached_property
    def order(self):
        return get_object_or_None(Order, id=self.order_id)

    @classmethod
    def _batch_order(cls, iterable):
        qs = Order.objects.filter(id__in=[_.order_id for _ in iterable if _])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.order_id) for _ in iterable}

    @cached_property
    def line_after_sales(self):
        return LineAfterSale.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_line_after_sales(cls, iterable):
        batch_map = defaultdict(list)
        qs = LineAfterSale.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def aftersale_notes(self):
        return AfterSaleNote.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_aftersale_notes(cls, iterable=None):
        batch_map = defaultdict(list)
        qs = AfterSaleNote.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def sum_return_amount_map(self):
        points_map = LineAfterSale.objects.filter(aftersale_id=self.id).values(
            'points_to_charge')\
            .aggregate(
                points_to_charge=Sum('points_to_charge')
            )
        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = LineAfterSalePaymentReturn.objects.filter(
            aftersale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_return": 0,
            "cash_type_amount": 0,
            "a_coupon_to_return": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_return"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_return"] += p["amount"]
        points_map.update(payment_map)
        return points_map

    @property
    def total_refund_cash_amount(self):
        amount = self.total_cash_amount + self.postage - self.hg_income_cash
        if amount < 0:
            amount = 0
        return amount

    @property
    def total_cash_amount(self):
        # import pdb; pdb.set_trace()
        amount = self.sum_return_amount_map.get('cash_type_amount')
        if not amount:
            amount = 0
        return amount

    @property
    def total_points_to_charge(self):
        amount = self.sum_return_amount_map.get('points_to_charge')
        if not amount:
            amount = 0
        return amount

    @property
    def total_c_coupon_to_return(self):
        amount = self.sum_return_amount_map.get('c_coupon_to_return')
        if not amount:
            amount = 0
        return amount

    @property
    def total_a_coupon_to_return(self):
        amount = self.sum_return_amount_map.get('a_coupon_to_return')
        if not amount:
            amount = 0
        return amount

    @property
    def total_a_coupon_to_charge(self):
        amount = self.sum_charge_amount_map.get('a_coupon_to_charge')
        if not amount:
            amount = 0
        return amount

    @cached_property
    def sum_charge_amount_map(self):
        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = LineAfterSalePaymentCharge.objects.filter(
            aftersale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_charge": 0,
            "cash_type_amount": 0,
            "a_coupon_to_charge": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_charge"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_charge"] += p["amount"]
        return payment_map

    @property
    def payment_type(self):
        payments = OrderPayment.objects.filter(order_id=self.order_id)
        payment_types = [_.payment_type for _ in payments]
        _payment_type = ""
        if PayType.WECHAT in payment_types:
            _payment_type = PayType.WECHAT
        elif PayType.ALIPAY in payment_types:
            _payment_type = PayType.ALIPAY
        return _payment_type

    # @property
    # def total_discount_hg(self):
    #     '''原值活动汉光承担的钱 也应该算进专柜收入里'''
    #     amount = self.line_after_sales.aggregate(total_amount=Sum('discount_hg')).get('total_amount')
    #     if not amount:
    #         amount = 0
    #     return amount
    @property
    def return_remaining_time(self):
        if self.pending_return_time:
            now = datetime.datetime.now()
            future = self.pending_return_time + datetime.timedelta(days=7)
            if future >= now:
                remaining = future - now
                return "{}天{}小时".format(remaining.days, int(remaining.seconds / (60 * 60)))
            return None
        return None

    @cached_property
    def hg_income_details(self):
        return AfterSaleHgIncomeDetail.objects.filter(aftersale_id=self.id, deleted=False)


class LineAfterSale(models.Model):
    '''
    AfterSale 和 Line 的多对多关系表
    '''
    aftersale_id = models.PositiveIntegerField(
        'AfterSale ID', blank=True, null=True, db_index=True)
    line_id = models.PositiveIntegerField(
        'Line ID', blank=True, null=True, db_index=True)
    # 默认数量是0，因为退差价就可以填0.创建的时候也不填数量，更新才填。
    quantity = models.PositiveIntegerField(
        'SKU退货数量', default=0)
    # 现金类退款金额, 包括支付宝，微信，银行卡，现金
    # 所有数量一共的退款
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # cash_type_amount = models.DecimalField(
    #     "现金类金额", decimal_places=2, max_digits=12, default=0)
    # 系统要扣用户的积分（当年发给用户的，现在用户要补缴）
    points_to_charge = models.PositiveIntegerField(
        '系统需要扣除用户的积分', default=0, blank=True, null=True)
    # 系统要还用户的C券（当年被用户用掉的，现在退货了要返还）--历史备注，暂时保留
    '''
    售后单数据库结构重构 说明 By Jessica 2019-07-15:
    points_to_charge和points_to_return两个字段本来应该是成对的，前者表示“扣除客户积分”，后者表示“退还客户积分”。
    由于历史原因，points_to_return在使用中，变成了“退还客户C券”的意义。
    因此在本次数据库调整中，points_to_return需要改回为“退还客户积分”的意义。
    改回前，需要把points_to_return“退还客户C券”的数据挪至sparrow_order_LineAfterSalePaymentReturn表中。
    '''
    points_to_return = models.PositiveIntegerField(
        '系统需要返还用户的积分', default=0, blank=True, null=True)
    # 系统要扣用户的A券（当年用户用掉的，现在用户要补缴）
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # a_coupon_to_charge = models.PositiveIntegerField(
    #     '系统需要扣除用户的A券', default=0, blank=True, null=True)
    # 系统要还用户的A券（当年被用户用掉的，现在退货了要返还）
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # a_coupon_to_return = models.PositiveIntegerField(
    #     '系统需要返还用户的A券', default=0, blank=True, null=True)
    # 店内系统需要用的流水号——默认先放0，然后传店内系统的时候必须生成flow_id，第一个会从1开始
    flow_id = models.PositiveIntegerField('流水号', default=0, blank=True, null=True)
    # 为了原值活动，必须存下来退了多少当时汉光承担的优惠
    # 这个数据在一期是根据其他退的金额动态算出来的。
    # 存下来的原因是对同一个订单可能有多个退单，而新退单必须知道以前已经退了多少汉光优惠
    discount_hg = models.DecimalField(
        "汉光优惠金额", default=0, decimal_places=2, max_digits=12, blank=True, null=True)

    # 产生售后对应的订单ID，新增冗余字段 by Jessica 2019-07-15
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)
    # 中分类，新增冗余字段 by Jessica 2019-07-15
    offer = models.CharField("中分类", max_length=2, default="0")

    # @property
    # def aftersale(self):
    #     return get_object_or_None(AfterSale, id=self.aftersale_id)

    @cached_property
    def line(self):
        return get_object_or_None(Line, id=self.line_id)

    @classmethod
    def _batch_line(cls, iterable):
        qs = Line.objects.filter(id__in=[_.line_id for _ in iterable])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.line_id) for _ in iterable}

    @cached_property
    def line_coupons_to_charge(self):
        return LineAfterSalePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )

    @classmethod
    def _batch_line_coupons_to_charge(cls, iterable):
        batch_map = defaultdict(list)
        qs = LineAfterSalePaymentCharge.objects.filter(
            line_after_sale_id__in=[_.id for _ in iterable],
            payment_type=PayType.GIFT_COUPON
        )
        for q in qs:
            for i in iterable:
                if q.line_after_sale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def line_coupons_to_return(self):
        return LineAfterSalePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )

    @classmethod
    def _batch_line_coupons_to_return(cls, iterable):
        batch_map = defaultdict(list)
        qs = LineAfterSalePaymentReturn.objects.filter(
            line_after_sale_id__in=[_.id for _ in iterable],
            payment_type=PayType.GIFT_COUPON
        )
        for q in qs:
            for i in iterable:
                if q.line_after_sale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @property
    def total_line_coupons_to_charge(self):
        line_coupons_to_charge = LineAfterSalePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )
        amount = line_coupons_to_charge.aggregate(total_amount=Sum('amount')).get('total_amount')
        if not amount:
            return 0
        return amount

    @property
    def total_line_coupons_to_return(self):
        line_coupons_to_return = LineAfterSalePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )
        amount = line_coupons_to_return.aggregate(total_amount=Sum('amount')).get('total_amount')
        if not amount:
            return 0
        return amount

    @cached_property
    def sum_return_amount_map(self):

        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = LineAfterSalePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_return": 0,
            "cash_type_amount": 0,
            "a_coupon_to_return": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_return"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_return"] += p["amount"]
        return payment_map

    @property
    def cash_type_amount(self):
        return self.sum_return_amount_map.get("cash_type_amount")

    @property
    def c_coupon_to_return(self):
        return self.sum_return_amount_map.get("c_coupon_to_return")

    @property
    def a_coupon_to_return(self):
        return self.sum_return_amount_map.get("a_coupon_to_return")

    @cached_property
    def sum_charge_amount_map(self):

        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = LineAfterSalePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_charge": 0,
            "cash_type_amount": 0,
            "a_coupon_to_charge": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_charge"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_charge"] += p["amount"]
        return payment_map

    @property
    def a_coupon_to_charge(self):
        return self.sum_charge_amount_map.get("a_coupon_to_charge")

    @property
    def shop_income_refund(self):
        '''专柜收入退款共计'''
        amount = Decimal('0.00')
        if not self.discount_hg:
            self.discount_hg = 0
        amount += Decimal(self.cash_type_amount) + Decimal(self.c_coupon_to_return) + Decimal(self.a_coupon_to_return)
        amount += Decimal(self.total_line_coupons_to_return)
        amount += Decimal(self.discount_hg)
        return amount

    class Meta:
        # 同一个售后单里不应该创建两个相同的line
        unique_together = ('aftersale_id', 'line_id')
        app_label = APP_LABEL


# 退还的coupon和补缴的coupon暂时用两个表表示
# 和 LineCouponToCharge 一点关系都没有！！！CouponToCharge 是对用户的操作
# LineCouponToCharge 是用来专柜核销数据用的
class CouponToCharge(models.Model):
    '''需要用户补缴的coupon，系统要从用户那儿收回的coupon 默认数量是1'''
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    aftersale_id = models.PositiveIntegerField(
        'AfterSale ID', blank=True, null=True, db_index=True)
    # 店内系统的话，code存在coupon_id里
    coupon_id = models.CharField(
        'Coupon ID', max_length=50, blank=True, null=True, db_index=True)
    # 店内系统的话，listid存在coupon_number里
    coupon_number = models.CharField(
        'Coupon Number', max_length=64, blank=True, null=True, db_index=True)
    coupon_source = models.CharField(
        '来源', max_length=64, default=CouponSource.IN_STORE,
        choices=CouponSourceChoices
    )
    # 产生售后对应的订单ID，新增冗余字段 by Jessica 2019-07-15
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)

    @property
    def coupon(self):
        return get_object_or_None(Coupon, id=self.coupon_id)

    class Meta:
        # 同一个售后单里不应该创建两个相同的coupon
        # 如果是店内券，有可能没有coupon_id，所以不能做下面的约束
        # unique_together = ('aftersale_id', 'coupon_id')
        app_label = APP_LABEL


# 和 LineCouponToReturn 一点关系都没有！！！CouponToReturn 是对用户的操作
# LineCouponToReturn 是用来专柜核销数据用的
class CouponToReturn(models.Model):
    '''系统退给用户的coupon 数量默认都是1！'''
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    aftersale_id = models.PositiveIntegerField(
        'AfterSale ID', blank=True, null=True, db_index=True)
    # 店内系统的话，code存在coupon_id里
    coupon_id = models.CharField(
        'Coupon ID', max_length=50, blank=True, null=True, db_index=True)
    # 店内系统的话，listid存在coupon_number里
    coupon_number = models.CharField(
        'Coupon Number', max_length=64, blank=True, null=True, db_index=True)
    coupon_source = models.CharField(
        '来源', max_length=64, default=CouponSource.IN_STORE,
        choices=CouponSourceChoices
    )
    # 产生售后对应的订单ID，新增冗余字段 by Jessica 2019-07-15
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)

    @property
    def coupon(self):
        return get_object_or_None(Coupon, id=self.coupon_id)

    class Meta:
        # 同一个售后单里不应该创建两个相同的coupon
        # 如果是店内券，有可能没有coupon_id，所以不能做下面的约束
        # unique_together = ('aftersale_id', 'coupon_id')
        app_label = APP_LABEL


class AfterSaleNote(models.Model):
    '''
    售后单日志
    '''
    ACTION_CHOICES = (
        (AftersaleActions.CREATE, '创建售后单'),
        (AftersaleActions.REMOVE, '关闭售后单'),
        (AftersaleActions.COMPLETE, '完成售后单'),
        (AftersaleActions.OPERATOR_APPROVE, '客服通过审核'),
        (AftersaleActions.FINANCE_APPROVE_1ST, '财务一审通过'),
        (AftersaleActions.FINANCE_APPROVE, '财务二审通过'),
        (AftersaleActions.FINANCE_REJECT, '财务驳回'),
        (AftersaleActions.INSTORE_REJECT, '店内系统驳回'),
        (AftersaleActions.ALL_APPROVE, '店内系统通过'),
        (AftersaleActions.REFUND_FAIL, '退款失败'),
        (AftersaleActions.PENDING_RETURN, '待退货'),
        (AftersaleActions.PENDING_REFUND, '待退款'),
        # (AftersaleActions.START_REFUND, '开始退款'),
        # (AftersaleActions.REFUND_SUCCEED, '退款成功'),
    )
    user_id = models.CharField(
        "User Id", max_length=100, blank=True, null=True, db_index=True)
    order_id = models.IntegerField('订单ID',
                                   blank=True, null=True, db_index=True)
    aftersale_id = models.IntegerField('AfterSale ID',
                                       blank=True, null=True, db_index=True)
    line_aftersale_id = models.IntegerField('LineAfterSale ID',
                                            blank=True, null=True, db_index=True)
    action = models.CharField(
        'Action', max_length=128, blank=True, null=True, choices=ACTION_CHOICES, db_index=True)
    message = models.CharField(
        'Message', max_length=256, blank=True, null=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)

    @cached_property
    def user(self):
        if not self.user_id:
            return None
        return get_object_or_None(get_user_model(), id=self.user_id)

    @classmethod
    def _batch_user(cls, iterable):
        qs = get_user_model().objects.filter(id__in=[_.user_id for _ in iterable])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.user_id) for _ in iterable if qs_map.get(_.user_id)}

    class Meta:
        app_label = APP_LABEL


class AfterSaleHgIncomeDetail(BaseModelTimeAndDeleted):
    '''
    售后单汉光其他收入明细，与售后单Aftersale表关系为多对一，即一个售后单可以存在多个AfterSaleHgIncome
    hgincome_type_id目前只有三种'积分、券、快递费',由AfterSaleHgIncomeType维护
    每个售后单的每种hgincome_type_id只能唯一

    '''
    order_id = models.IntegerField('订单ID',
                                   blank=True, null=True, db_index=True)
    aftersale_id = models.IntegerField('AfterSale ID',
                                       blank=True, null=True, db_index=True)
    hgincome_type_id = models.IntegerField('hgincome Type ID',
                                       blank=True, null=True, db_index=True)
    amount = models.DecimalField(
        "Amount", decimal_places=2, max_digits=12, blank=True, null=True, default=0)

    class Meta:
        app_label = APP_LABEL


class AfterSaleHgIncomeType(BaseModelTimeAndDeleted):
    # Topic type code, such as 'PRESALE' or'FLASHSALE', which should be unique.
    code = models.CharField("HgIncome Code", max_length=100, unique=True)
    # Topic type name, such as '预售' or '闪购'， which should be uniqure.
    display_name = models.CharField("HgIncome Display Name", max_length=100, unique=True)

    class Meta:
        app_label = APP_LABEL


class Line(models.Model):
    """
    An order line
    """
    # 订单ID
    order_id = models.PositiveIntegerField(
        'Order Id', blank=True, null=True, db_index=True)
    # 品牌信息
    brand_id = models.PositiveIntegerField(
        'Brand Id', blank=True, null=True, db_index=True)
    # 专柜信息
    shop_id = models.PositiveIntegerField(
        'Shop Id', blank=True, null=True, db_index=True)
    # 柜号
    shop_num = models.CharField("Shop number", max_length=128, blank=True)
    # 厂商编码，货号
    shop_sku = models.CharField("Shop SKU", max_length=128, blank=True, null=True)
    # 汉光码 冗余进来
    hg_code = models.CharField("汉光码", max_length=255, blank=True, null=True)
    # 备注
    shop_line_notes = models.TextField("Shop Notes", blank=True)
    # 商品信息SKU
    product_id = models.PositiveIntegerField(
        'Product Id', blank=True, null=True, db_index=True)
    # 商品名字
    title = models.CharField("Product title", max_length=255)
    # 订单里图片不单独上传，用商品数据库字段里的值
    main_image = models.ImageField("Main Image", null=True, blank=True, max_length=255)
    # sku属性——文字组合
    sku_attr = models.CharField(
        "SKU Attr", max_length=255, blank=True, null=True)
    # 未启用
    upc = models.CharField("UPC", max_length=128, blank=True, null=True)
    # 数量
    quantity = models.PositiveIntegerField("Quantity", default=1)
    # line里的总金额，不考虑活动，就是line本身的售价*数量
    line_price = models.DecimalField("Price", decimal_places=2, max_digits=12)
    # 活动优惠了的金额 —— 这个line全部数量单品里，满减和折扣这种能直接让钱变少的优惠金额
    discount_amount = models.DecimalField(
        "Discount", decimal_places=2, max_digits=12, blank=True, null=True, default=0)
    # 汉光承担的优惠金额（比如原值活动的优惠）
    discount_hg = models.DecimalField(
        "汉光优惠金额", decimal_places=2, max_digits=12, blank=True, null=True, default=0)
    # 专柜承担的优惠金额（比如专柜满减，折扣）
    discount_shop = models.DecimalField(
        "专柜优惠金额", decimal_places=2, max_digits=12, blank=True, null=True, default=0)
    # 这个商品的原价（比如吊牌价）（1件的价格）
    original_price = models.DecimalField(
        "Original Price", decimal_places=2,
        max_digits=12, blank=True, null=True)
    # 这个商品的售价（1件的价格）
    # 客户实际支付的金额为 line_price-discount_amount, 也即retail_price*quantity-discount_amount
    retail_price = models.DecimalField(
        "Retail Price", decimal_places=2, max_digits=12,
        blank=True, null=True)
    # 专柜收入 —— 这个line（此line总共）专柜的收入
    shop_income_price = models.DecimalField(
        "专柜收入", decimal_places=2, max_digits=12,
        blank=True, null=True, default=0)
    # 参与积分的金额 —— 可积分的金额（此line总共）
    amount_for_point = models.DecimalField(
        '用户实际支付金额——参与积分的金额',
        default=Decimal('0'),
        decimal_places=2,
        max_digits=12,
        validators=[validators.MinValueValidator(Decimal('0.00'))])
    # 积分基数-金额 积分基数，比如1元20积分，这个字段就是1元。支持两位小数
    point_amount = models.DecimalField(
        '积分基数对应的金额，以元为单位',
        default=Decimal('1'),
        decimal_places=2,
        max_digits=12,
        validators=[validators.MinValueValidator(Decimal('0.01'))])
    # 积分倍数 积分倍数，比如1元20积分，这个字段就是20。支持两位小数
    point_multiple = models.DecimalField(
        '积分倍数',
        default=Decimal('1'),
        decimal_places=2,
        max_digits=12,
        validators=[validators.MinValueValidator(Decimal('0.01'))])
    # 用户获取积分 此line总共用户应该获得的积分
    points = models.PositiveIntegerField('Points', default=0)
    # 中分类
    offer = models.CharField("中分类", max_length=2, default="0")
    # 店内系统需要用的流水号——默认先放0，然后传店内系统的时候必须生成flow_id，第一个会从1开始
    flow_id = models.PositiveIntegerField('流水号', default=0, blank=True, null=True)
    # 商品条码
    barcode = models.CharField("Product Barcode", max_length=256, blank=True, null=True)
    # 商品信息SPU
    productmain_id = models.PositiveIntegerField('Product Main Id', blank=True, null=True, db_index=True)

    # giftproduct_id(赠品id)
    giftproduct_id = models.PositiveIntegerField('赠品 ID', blank=True, null=True, db_index=True)
    is_gift = models.BooleanField("是否是赠品", default=False, db_index=True)
    # 订单类型
    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True, default=None)
    # 商品类目
    categories = models.CharField('商品类目', max_length=128, blank=True, null=True, default=None)
    # coupon_shop_num 用来到线下查询可用活动的快照值，有可能是专柜号本身，也有可能是专柜号前五位（药店），也有可能是专柜号+offer值, 这个offer值是算出来的，可能是活动的，如果没有活动就是商品自己的。
    # 在分阶段支付里，因为尾款时查coupon要用到，否则就不是当时的情况了，重新计算有风险。所以要保存一下这个计算结果。
    # 普通订单里也会维护这个字段，便于我们以后追查订单时确定当时的offer到底取了啥
    coupon_shop_num = models.CharField("Coupon Shop Num", max_length=16, blank=True)

    class Meta:
        app_label = APP_LABEL
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"

    def __str__(self):
        return '{0}-{1}'.format(self.id, self.title)

    # TODO: @property
    # @property
    # def shop(self):
    #     '''前端需要'''
    #     return get_object_or_None(Shop, id=self.shop_id)

    # @cached_property
    # def brand(self):
    #     '''前端需要'''
    #     return get_object_or_None(Brand, id=self.brand_id)

    # @classmethod
    # def _batch_brand(cls, iterable):
    #     # import pdb ; pdb.set_trace()
    #     qs = Brand.objects.filter(id__in=set([_.brand_id for _ in iterable if _.brand_id]))
    #     qs_map = {_.id: _ for _ in qs}
    #     return {_: qs_map.get(_.brand_id) for _ in iterable}

    @property
    def actual_amount(self):
        # 用户实付金额——包含所有支付方式，比如优惠券——不含邮费！
        line_payments = LineOrderPayment.objects.filter(line_id=self.id)
        amount = line_payments.aggregate(amount=Sum('amount')).get('amount')
        if not amount:
            amount = 0
        return amount

    @property
    def line_order_payments(self):
        return LineOrderPayment.objects.filter(line_id=self.id)

    @property
    def line_after_sales(self):
        return LineAfterSale.objects.filter(line_id=self.id)

    @property
    def valid_line_after_sales(self):
        # 过滤掉被关闭的售后单
        line_after_sales = LineAfterSale.objects.filter(line_id=self.id)
        aftersale_ids = line_after_sales.values('aftersale_id')
        aftersales = AfterSale.objects.filter(id__in=aftersale_ids).exclude(status=AftersaleStatus.CLOSED)
        line_after_sales = line_after_sales.filter(aftersale_id__in=aftersales.values('id'))
        return line_after_sales

    @property
    def completed_line_after_sales(self):
        # 2018-04-17 应该用完成的售后单。因为open的包含当前的，不应该和当前的重复
        # 而我们只允许有一个open的售后单，所以用完成的售后单可以完美解决
        line_after_sales = LineAfterSale.objects.filter(line_id=self.id)
        aftersale_ids = line_after_sales.values('aftersale_id')
        aftersales = AfterSale.objects.filter(id__in=aftersale_ids, status=AftersaleStatus.COMPLETED)
        line_after_sales = line_after_sales.filter(aftersale_id__in=aftersales.values('id'))
        return line_after_sales

    @property
    def line_assignments(self):
        return LineAssignment.objects.filter(line_id=self.id)

    @property
    def valid_line_assignments(self):
        # 过滤掉被关闭的发货单
        line_assignments = LineAssignment.objects.filter(line_id=self.id)
        assignment_ids = line_assignments.values('assignment_id')
        assignments = Assignment.objects.filter(id__in=assignment_ids).exclude(status=AssignmentStatus.CLOSED)
        line_assignments = line_assignments.filter(assignment_id__in=assignments.values('id'))
        return line_assignments

    @property
    def line_order_promotions(self):
        return LineOrderPromotion.objects.filter(
            line_id=self.id
        )

    # TODO: @property
    # @property
    # def product(self):
    #     return get_object_or_None(Product, id=self.product_id)

    # @property
    # def productmain_id(self):
    #     # GIO 埋点用
    #     product = self.product
    #     return product.productmain_id if product else None

    @cached_property
    def fixed_price_product(self):
        # 有时候需要知道这个line是不是加价购
        return get_object_or_None(OrderPromotionFixedPriceProduct, line_id=self.id)

    @classmethod
    def _batch_fixed_price_product(cls, iterable):
        qs = OrderPromotionFixedPriceProduct.objects.filter(line_id__in=[_.id for _ in iterable])
        qs_map = {_.line_id: _ for _ in qs}
        return {_: qs_map.get(_.id) for _ in iterable}

    @cached_property
    def is_fixed_price_product(self):
        # 需要知道这个line是不是加价购
        promotion_fixed_price_line = OrderPromotionFixedPriceProduct.objects.filter(line_id=self.id)
        if promotion_fixed_price_line.exists():
            return True
        return False

    @classmethod
    def _batch_is_fixed_price_product(cls, iterable):
        batch_map = defaultdict(list)
        qs = OrderPromotionFixedPriceProduct.objects.filter(line_id__in=[_.id for _ in iterable])
        for i in iterable:
            for q in qs:
                if q.line_id == i.id:
                    batch_map[i].append(q)
        batch_map = {i: bool(j) for i, j in batch_map.items()}
        return batch_map

    @cached_property
    def is_gift(self):
        # 需要知道这个line是不是赠品
        promotion_gift_line = OrderPromotionGiftProduct.objects.filter(line_id=self.id)
        if promotion_gift_line.exists():
            return True
        return False

    @classmethod
    def _batch_is_gift(cls, iterable):
        batch_map = defaultdict(list)
        qs = OrderPromotionGiftProduct.objects.filter(line_id__in=[_.id for _ in iterable])
        for i in iterable:
            for q in qs:
                if q.line_id == i.id:
                    batch_map[i].append(q)
        batch_map = {i: bool(j) for i, j in batch_map.items()}
        return batch_map

    # 配货时候需要知道gift_id (GiftProduct 表)
    # 或者line是赠品的时候或者活动信息
    @cached_property
    def order_promotion_gift_product(self):
        return get_object_or_None(OrderPromotionGiftProduct, line_id=self.id)

    @classmethod
    def _batch_order_promotion_gift_product(cls, iterable):
        qs = OrderPromotionGiftProduct.objects.filter(line_id__in=[_.id for _ in iterable])
        qs_map = {_.line_id: _ for _ in qs}
        return {_: qs_map.get(_.id) for _ in iterable}

    # 配货时候需要知道gift_id (GiftProduct 表)
    @cached_property
    def gift(self):
        from sparrow_products.models import GiftProduct
        promotion_gift_line = get_object_or_None(OrderPromotionGiftProduct, line_id=self.id)
        return get_object_or_None(GiftProduct, id=promotion_gift_line.giftproduct_id) if promotion_gift_line else None

    @cached_property
    def gift_id(self):
        gift = self.gift
        return gift.id if gift else None

    @property
    def valid_refund_quantity(self):
        # import pdb; pdb.set_trace()
        completed_aftersales = AfterSale.objects.filter(
            order_id=self.order_id,
            status=AftersaleStatus.COMPLETED
        )
        completed_line_after_sales = LineAfterSale.objects.filter(
            line_id=self.id,
            aftersale_id__in=completed_aftersales.values('id')
        )
        # 计算出这个line已经完成售后的数量
        aftersaled_quantity = completed_line_after_sales.aggregate(
            aftersaled_quantity=Sum('quantity')).get('aftersaled_quantity')
        if not aftersaled_quantity:
            aftersaled_quantity = 0
        # 这个 line 已经完成售后的数量
        # self.aftersale_count = aftersaled_quantity
        # 这个 line 还能发起售后的数量
        available_quantity = self.quantity - aftersaled_quantity
        if available_quantity < 0:
            available_quantity = 0
        return available_quantity


class OrderPromotion(models.Model):
    '''订单里的活动快照'''
    order_id = models.PositiveIntegerField(
        'Order Id', blank=True, null=True, db_index=True)
    # 活动ID
    promotion_id = models.PositiveIntegerField(
        'Promotion Id', blank=True, null=True, db_index=True)

    # 主活动ID
    promotionmain_id = models.PositiveIntegerField(
        'Promotion Main Id', blank=True, null=True, db_index=True)

    name = models.CharField("活动名称", max_length=20, blank=True, null=True)
    promotion_type = models.CharField(
        "活动类型", max_length=30, blank=True, null=True)
    # 活动摘要，把对应档的活动描述复制到这里 —— 有可能在订单详情展示
    summary = models.CharField("Promotion Summary",
                               max_length=256, blank=True)
    discount_amount = models.DecimalField(
        "满减金额", decimal_places=2,
        max_digits=12, blank=True, null=True, default=0.00)

    # 退货重算 活动序号
    vseq = models.CharField("活动序号", max_length=2, null=True)

    # 只有赠品活动才有此值（全部 common| 会员绑卡礼 auth_gift）
    # 当gift_type==auth_gift时，就算是订单享受了绑卡礼
    gift_type = models.CharField("赠品类型", max_length=20, blank=True, null=True)

    @property
    def promotion(self):
        from sparrow_promotions.models import Promotion
        return get_object_or_None(Promotion, id=self.promotion_id)

    @property
    def promotionmain(self):
        '''这里放的promotionmain需要带出所有的子promotions'''
        from sparrow_promotions.models import PromotionMain
        if self.promotionmain_id:
            return get_object_or_None(PromotionMain, id=self.promotionmain_id)
        else:
            return get_object_or_None(PromotionMain, id=self.promotion.promotionmain_id)

    def __str__(self):
        return 'orderid_{0}--promotion_id_{1}--{2}'.format(
            self.order_id, self.promotion_id, self.summary)

    class Meta:
        app_label = APP_LABEL


class OrderPromotionCoupon(models.Model):
    '''
    订单活动里的券快照
    如果一个活动返了两个券，这里就创建两条，默认每条都是一张券，所以不记录quantity
    '''
    # 活动快照ID
    orderpromotion_id = models.PositiveIntegerField(
        'OrderPromotion Id', blank=True, null=True, db_index=True)
    coupon_id = models.PositiveIntegerField(
        'Coupon Id', blank=True, null=True, db_index=True)
    title = models.CharField(
        "优惠券名字", max_length=100, blank=True, null=True)
    summary = models.CharField(
        "优惠券描述", max_length=500, blank=True, null=True)
    # 费用承担方
    payer = models.CharField(
        "费用承担方", max_length=10, blank=True, null=True)

    @property
    def coupon(self):
        from sparrow_promotions.models import Coupon
        return get_object_or_None(Coupon, id=self.coupon_id)

    def __str__(self):
        return self.title if self.title else ''

    class Meta:
        app_label = APP_LABEL


class OrderPromotionGiftProduct(models.Model):
    '''
    活动赠品快照
    2019-01-25
    从此以后，用这个表来存line快照的赠品，和真实赠品，和订单活动快照的关系
    '''
    # 活动快照ID
    orderpromotion_id = models.PositiveIntegerField(
        'OrderPromotion Id', blank=True, null=True, db_index=True)
    # 赠品ID
    giftproduct_id = models.PositiveIntegerField(
        'GiftProduct Id', blank=True, null=True, db_index=True)
    # Line ID
    # 一个line（已经是订单快照的一部分了）只能是一个活动的一个赠品，不应该出现同一个line有多条记录
    line_id = models.PositiveIntegerField(
        'Line Id', unique=True, blank=True, null=True, db_index=True)

    @property
    def giftproduct(self):
        from sparrow_products.models import GiftProduct
        return get_object_or_None(GiftProduct, id=self.giftproduct_id)

    @property
    def orderpromotion(self):
        return get_object_or_None(OrderPromotion, id=self.orderpromotion_id)

    class Meta:
        app_label = APP_LABEL


# 此表不要注释！！不要删除！兼容历史订单赠品！
class OrderPromotionGift(models.Model):
    '''活动赠品快照'''
    # 活动快照ID
    orderpromotion_id = models.PositiveIntegerField(
        'OrderPromotion Id', blank=True, null=True, db_index=True)
    # 赠品ID
    giftproduct_id = models.PositiveIntegerField(
        'GiftProduct Id', blank=True, null=True, db_index=True)
    title = models.CharField('Title', max_length=255, blank=True)
    price = models.DecimalField(
        "价值", decimal_places=2, max_digits=12, blank=True, null=True)
    quantity = models.PositiveIntegerField('Quantity', default=1)
    # 订单里图片不单独上传，用赠品数据库字段里的值
    # main_image = models.ImageField("Main Image", null=True, blank=True, max_length=255)
    main_image_id = models.PositiveIntegerField("赠品图片ID", blank=True, null=True)
    # 品牌信息
    brand_id = models.PositiveIntegerField(
        'Brand Id', blank=True, null=True, db_index=True)
    # 专柜信息
    shop_id = models.PositiveIntegerField(
        'Shop Id', blank=True, null=True, db_index=True)
    # 柜号
    shop_num = models.CharField("Shop number", max_length=128, blank=True)

    # TODO: @property
    # @property
    # def giftproduct(self):
    #     from sparrow_products.models import GiftProduct
    #     return get_object_or_None(GiftProduct, id=self.giftproduct_id)

    # @property
    # def orderpromotion(self):
    #     return get_object_or_None(OrderPromotion, id=self.orderpromotion_id)

    # @property
    # def main_image(self):
    #     image_obj = get_object_or_None(ImageServer, id=self.main_image_id)
    #     if image_obj:
    #         return image_obj.image
    #     return None

    # @property
    # def shop(self):
    #     '''前端需要'''
    #     return get_object_or_None(Shop, id=self.shop_id)

    # @property
    # def brand(self):
    #     '''前端需要'''
    #     return get_object_or_None(Brand, id=self.brand_id)

    def __str__(self):
        return self.title if self.title else ''

    class Meta:
        app_label = APP_LABEL


class OrderPromotionFixedPriceProduct(models.Model):
    '''活动加价购快照'''
    # 活动快照ID
    orderpromotion_id = models.PositiveIntegerField(
        'OrderPromotion Id', blank=True, null=True, db_index=True)
    # 加价购商品的 line_id
    line_id = models.PositiveIntegerField(
        'Line Id', unique=True, blank=True, null=True, db_index=True)

    def __str__(self):
        return "line_id=%s-%s" % (self.line_id, self.orderpromotion_id)

    @cached_property
    def orderpromotion(self):
        return get_object_or_None(OrderPromotion, id=self.orderpromotion_id)

    @classmethod
    def _batch_orderpromotion(cls, iterable):
        qs = OrderPromotion.objects.filter(id__in=[_.orderpromotion_id for _ in iterable])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.orderpromotion_id) for _ in iterable if qs_map.get(_.orderpromotion_id)}

    class Meta:
        app_label = APP_LABEL


class LineOrderPromotion(models.Model):
    '''
    line 参与的促销活动
    Line 和 OrderPromotion 多对多的关系
    '''
    line_id = models.PositiveIntegerField(
        'Line ID', blank=True, null=True, db_index=True)
    orderpromotion_id = models.PositiveIntegerField(
        'OrderPromotion Id', blank=True, null=True, db_index=True)
    # 活动ID
    promotion_id = models.PositiveIntegerField(
        'Promotion Id', blank=True, null=True, db_index=True)

    # 主活动ID
    promotionmain_id = models.PositiveIntegerField(
        'Promotion Main Id', blank=True, null=True, db_index=True)

    # 活动类型
    promotion_type = models.CharField(
        "活动类型", max_length=30, blank=True, null=True)

    # 活动标签
    promotion_label = models.CharField(
        "活动标签", max_length=20, blank=True, null=True)

    # 退货重算 活动序号
    vseq = models.CharField("活动序号", max_length=2, null=True)

    # 只有赠品活动才有此值（全部 common| 会员绑卡礼 auth_gift）
    # 当gift_type==auth_gift时，就算是订单享受了绑卡礼
    gift_type = models.CharField("赠品类型", max_length=20, blank=True, null=True)

    # @property
    # def line(self):
    #     return get_object_or_None(Line, id=self.line_id)

    @cached_property
    def orderpromotion(self):
        return get_object_or_None(OrderPromotion, id=self.orderpromotion_id)

    @classmethod
    def _batch_orderpromotion(cls, iterable=None):
        qs_map = {_.id: _ for _ in OrderPromotion.objects.filter(id__in=[_.orderpromotion_id for _ in iterable])}
        return {_: qs_map.get(_.orderpromotion_id) for _ in iterable if qs_map.get(_.orderpromotion_id)}

    @property
    def order_id(self):
        orderpromotion = self.orderpromotion
        if orderpromotion:
            return orderpromotion.order_id
        return None

    def __str__(self):
        return 'lineid_{0}--orderpromotionid_{1}'.format(
            self.line_id, self.orderpromotion_id)

    class Meta:
        app_label = APP_LABEL


class OrderNote(models.Model):
    """
    A note against an order.
    This is often used for audit purposes too.  i.e., whenever an admin
    makes a change to an order, we create a note to record what happened.
    需要记录的信息有：
    下单，支付，所有修改，配货，
    提货记录在 AfterSaleNote 里面
    """
    ACTION_CHOICES = (
        (OrderActions.CREATE, '创建订单'),
        (OrderActions.MODIFY_ADDRESS, '修改收货地址'),
        (OrderActions.MODIFY_OPERATOR_NOTE, '修改客服备注'),
        (OrderActions.CLOSE, '关闭订单'),
        (OrderActions.PAY, '发起支付'),
        (OrderActions.COMPLETE_PAYMENT, '完成支付'),
        (OrderActions.SEND, '邮寄'),
        (OrderActions.TAKE, '用户来提'),
        (OrderActions.OTHERS, '其他'),
    )
    TYPE_CHOICES = (
        (LogLevel.WARNING, '警告'),
        (LogLevel.INFO, '信息'),
        (LogLevel.ERROR, '错误'),
        (LogLevel.SYSTEM, '系统'),
    )
    order_id = models.PositiveIntegerField('Order Id',
                                           blank=True, null=True, db_index=True)
    # These are sometimes programatically generated so don't need a
    # user everytime
    user_id = models.CharField(
        "User Id", max_length=100, blank=True, null=True, db_index=True)
    note_type = models.CharField("Note Type", max_length=128, blank=True,
                                 db_index=True, choices=TYPE_CHOICES, default=LogLevel.INFO)
    action = models.CharField('Action', max_length=128, blank=True,
                              null=True, choices=ACTION_CHOICES, default=OrderActions.OTHERS)
    message = models.TextField("Message")
    created_time = models.DateTimeField("Created Time",
                                        auto_now_add=True)

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Order Note")
        verbose_name_plural = _("Order Notes")

    def __str__(self):
        return u"'%s' userid_(%s)" % (self.message[0:50], self.user_id)

    @property
    def order(self):
        return get_object_or_None(Order, id=self.order_id)

    @property
    def user(self):
        if not self.user_id:
            return None
        return get_object_or_None(get_user_model(), id=self.user_id)


# 每天晚上 快照 未从专柜提的库存
class Inventory(BaseModelNew):
    '''
    盘点，快照已付未提
    '''
    created_date = models.DateField("报表日期", auto_now_add=True, blank=True, null=True)
    hg_code = models.CharField("汉光码", max_length=1024, blank=True, null=True)
    barcode = models.CharField("国际条码", max_length=1024, blank=True, null=True)
    shop_sku = models.CharField("厂商编码/货号", max_length=1024, blank=True, null=True)
    sku_attr = models.CharField("规格", max_length=1024, blank=True, null=True)
    title = models.CharField("产品名称", max_length=255, blank=True, null=True)
    required_count = models.IntegerField('需求库存/未提数量', blank=True, null=True)
    retail_price = models.DecimalField("售价", decimal_places=2, max_digits=12, blank=True, null=True)
    brand_id = models.PositiveIntegerField(
        'Brand ID', blank=True, null=True, db_index=True)
    shop_id = models.PositiveIntegerField(
        'Shop ID', blank=True, null=True, db_index=True)
    shop_num = models.CharField("柜号", max_length=64, blank=True, null=True)
    shop_name = models.CharField("柜名", max_length=50, blank=True, null=True)
    product_id = models.PositiveIntegerField(
        'Product ID', blank=True, null=True, db_index=True)
    # 我们已提到自己货架上的库存
    stock = models.PositiveIntegerField(
        '已有库存', blank=True, null=True, default=0)
    created_time = models.DateTimeField("Datetime Created", auto_now_add=True)
    updated_time = models.DateTimeField("Datetime Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL

    # TODO: @property
    # @property
    # def product(self):
    #     return get_object_or_None(Product, id=self.product_id)

    # @property
    # def brand(self):
    #     return get_object_or_None(Brand, id=self.brand_id)

    # @property
    # def shop(self):
    #     return get_object_or_None(Shop, id=self.shop_id)


class Settings(models.Model):
    '''
    订单和售后操作的配置表
    '''
    LABEL_CHOICES = (
        (SettingsLabel.SUPERVISOR_INTERCEPTION, '客服主管拦截'),
    )
    name = models.CharField("配置名称", max_length=63, blank=True, null=True)
    label = models.CharField("唯一标签", max_length=63, blank=True, null=True, choices=LABEL_CHOICES)
    is_active = models.BooleanField('是否启用', default=False)
    created_time = models.DateTimeField("Datetime Created", auto_now_add=True)
    updated_time = models.DateTimeField("Datetime Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL


class AfterSalePayment(BaseModelNew):
    '''
    Added by Jessica 2019-07-15
    订单对应的售后支付处理
    '''
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    # 售后单ID
    aftersale_id = models.PositiveIntegerField('Aftersale Id', blank=True, null=True, db_index=True)
    # 支付类型
    payment_type = models.CharField(
        "Payment type", max_length=10,
        choices=PayType.PAYMENT_TYPE_CHOICES,
        default=PayType.TO_PAY
    )
    # 数额
    amount = models.DecimalField("Amount", decimal_places=2, max_digits=12)
    # 店内系统的话，code存在coupon_id里
    coupon_id = models.CharField(
        'Coupon ID', max_length=50, blank=True, null=True, db_index=True)
    # 店内系统的话，listid存在coupon_number里
    coupon_number = models.CharField(
        'Coupon Number', max_length=64, blank=True, null=True, db_index=True)
    coupon_source = models.CharField(
        '来源', max_length=64, blank=True, null=True,
        choices=CouponSourceChoices
    )
    # 产生售后对应的订单ID
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)

    created_time = models.DateTimeField("Date Created", blank=True, null=True, auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", blank=True, null=True, auto_now=True)

    class Meta:
        abstract = True
        app_label = APP_LABEL


class AfterSalePaymentCharge(AfterSalePayment):
    '''
    Added by Jessica 2019-07-15
    订单对应的售后支付处理: 从客户扣除，它是对LineAfterSalePaymentCharge的汇总
    '''
    class Meta:
        app_label = APP_LABEL


class AfterSalePaymentReturn(AfterSalePayment):
    '''
    Added by Jessica 2019-07-15
    订单对应的售后支付处理：退还给客户，它是对LineAfterSalePaymentReturn的汇总
    '''

    class Meta:
        app_label = APP_LABEL


class LineAfterSalePayment(AfterSalePayment):
    '''
    Added by Jessica 2019-07-15
    订单Line对应的售后支付处理
    '''
    # 售后Line ID
    line_after_sale_id = models.PositiveIntegerField('LineAfterSale Id', blank=True, null=True, db_index=True)
    # 产生售后对应的订单Line ID
    line_id = models.PositiveIntegerField('Line Id', blank=True, null=True, db_index=True)

    class Meta:
        abstract = True
        app_label = APP_LABEL


class LineAfterSalePaymentCharge(LineAfterSalePayment):
    '''
    Added by Jessica 2019-07-15
    订单Line对应的售后支付处理: 从客户扣除
    '''
    class Meta:
        app_label = APP_LABEL


class LineAfterSalePaymentReturn(LineAfterSalePayment):
    '''
    Added by Jessica 2019-07-15
    订单Line对应的售后支付处理：退还给客户
    '''

    class Meta:
        app_label = APP_LABEL


class AfterSaleAlipayRefund(models.Model):
    """
    发起过支付宝退款并且返回值为10000的会有记录，作用是查询一些争议退款情况
    """
    aftersale_id = models.PositiveIntegerField('AfterSale Id', unique=True)
    order_number = models.CharField('Order ID', max_length=128, blank=True, null=True)
    amount = models.DecimalField("退款金额", decimal_places=2, max_digits=12, default=0.00)
    user_id = models.CharField("User Id", max_length=100, db_index=True)
    trade_no = models.CharField('支付宝交易号', max_length=64, blank=True, null=True)
    buyer_logon_id = models.CharField('用户的登录id', max_length=100, blank=True, null=True)
    buyer_user_id = models.CharField('买家在支付宝的用户id', max_length=28, blank=True, null=True)
    fund_change = models.CharField('本次退款是否发生了资金变化', max_length=2, blank=True, null=True)
    refund_fee = models.CharField('金额', max_length=11, blank=True, null=True)
    out_trade_no = models.CharField('商户订单号', max_length=64, blank=True, null=True)
    out_request_no = models.CharField('支付宝退款请求号', max_length=64, blank=True, null=True)
    gmt_refund_pay = models.CharField('退款支付时间', max_length=32, blank=True, null=True)
    is_success = models.BooleanField('退款是否成功', default=False)
    created_time = models.DateTimeField("Date Created", blank=True, null=True, auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", blank=True, null=True, auto_now=True)

    class Meta:
        app_label = APP_LABEL


class BatchAssignTask(BaseModelTimeAndDeleted):
    BATCH_ASSIGN_TASK_STATUS_CHOICES = (
        (BatchAssignTaskStatus.IN_PROGRESS, '正在进行中'),
        (BatchAssignTaskStatus.COMPLETED, '已完成'),
        (BatchAssignTaskStatus.ERROR, '执行失败'),
    )
    BATCH_ASSIGN_TASK_TYPE_CHOICES = (
        (BatchAssignType.WHOLE, '全部配货'),
        (BatchAssignType.PARTIAL, '部分配货'),
        (BatchAssignType.PRODUCT, '单商品部分配货'),
    )
    id = models.CharField(
        max_length=100,
        primary_key=True,
        default=get_uuid4_hex,
        editable=False)
    sparrow_task_id = models.CharField('Sparrow_Task ID', max_length=40, blank=False)
    task_executor = models.CharField("任务发起者", max_length=100, blank=True, null=True, db_index=True)
    task_type = models.CharField('批量配货类型', max_length=128, blank=True, null=True, choices=BATCH_ASSIGN_TASK_TYPE_CHOICES, db_index=True)
    task_status = models.CharField('任务执行状态', max_length=128, blank=True, null=True, choices=BATCH_ASSIGN_TASK_STATUS_CHOICES, db_index=True)
    task_kwargs = models.CharField('输入参数', max_length=500, blank=True, null=True)
    task_result = models.CharField('任务执行结果', max_length=1500, blank=True, null=True)
    message = models.CharField('信息', max_length=16384, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL


class GroupPickUpRecord(models.Model):
    HAS_PICKUP = "has_pickup"
    REFUND = "refund"
    TAKEN_STATUS = (
        (HAS_PICKUP, "已领取"),
        (REFUND, "已退"),
    )
    user_id = models.CharField("User Id", max_length=100)
    order_number = models.CharField('Order ID', max_length=128)
    taken_status = models.CharField('领取状态', max_length=128, default=HAS_PICKUP, choices=TAKEN_STATUS)
    create_time = models.DateTimeField("Date Created", auto_now_add=True)
    update_time = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL


# 每天晚上 快照 未从专柜提的库存
class InventoryV3(BaseModelNew):
    '''
    盘点，快照已付未提
    '''
    created_date = models.DateField("报表日期", auto_now_add=True, blank=True, null=True)
    hg_code = models.CharField("汉光码", max_length=1024, blank=True, null=True)
    barcode = models.CharField("国际条码", max_length=1024, blank=True, null=True)
    shop_sku = models.CharField("厂商编码/货号", max_length=1024, blank=True, null=True)
    sku_attr = models.CharField("规格", max_length=1024, blank=True, null=True)
    title = models.CharField("产品名称", max_length=255, blank=True, null=True)
    required_count = models.IntegerField('需求库存/未提数量', blank=True, null=True)
    retail_price = models.DecimalField("售价", decimal_places=2, max_digits=12, blank=True, null=True)
    brand_id = models.PositiveIntegerField('Brand ID', blank=True, null=True, db_index=True)
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True, db_index=True)
    shop_num = models.CharField("柜号", max_length=64, blank=True, null=True)
    shop_name = models.CharField("柜名", max_length=50, blank=True, null=True)
    product_id = models.PositiveIntegerField('Product ID', blank=True, null=True, db_index=True)
    giftproduct_id = models.PositiveIntegerField('Gift Product ID', blank=True, null=True, db_index=True)
    # 我们已提到自己货架上的库存
    stock = models.PositiveIntegerField('已有库存', blank=True, null=True, default=0)
    created_time = models.DateTimeField("Datetime Created", auto_now_add=True)
    updated_time = models.DateTimeField("Datetime Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL_AFS


class VendingHROrder(BaseModelNew):

    order_id = models.PositiveIntegerField('Sparrow Order ID', db_index=True, unique=True)
    order_number = models.CharField('Sparrow Order Number', max_length=128, blank=True, null=True, db_index=True)
    vmhr_order_id = models.CharField("Vending Machine HR order number", max_length=64, db_index=True, unique=True)
    delivery_status = models.BooleanField('是否已经吐货', default=False)
    delivery_time = models.DateTimeField('吐货时间', null=True, blank=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        app_label = APP_LABEL_AFS


class HGVending(BaseModelTimeAndDeleted):
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True)
    machine_code = models.CharField("贩售机机器码", max_length=32, db_index=True)
    pickup_code = models.CharField("取货码", max_length=32, db_index=True)
    expire_time = models.DateTimeField("过期时间", blank=True, null=True)
    status = models.CharField("订单发货状态", max_length=32, choices=HGVendingStatus.HGVENDING_STATUS_CHOICES, blank=True, null=True, default=HGVendingStatus.INIT)

    class Meta:
        app_label = APP_LABEL_AFS
        unique_together = ('machine_code', 'pickup_code',)


class OrderScene(BaseModelTimeAndDeleted):
    order_id = models.PositiveIntegerField('Sparrow Order ID', db_index=True, unique=True)
    order_number = models.CharField('Sparrow Order Number', max_length=128, blank=True, null=True, db_index=True)
    scene = models.PositiveIntegerField("场景值", blank=True, null=False, db_index=True)
    # newexpressorder_id_2wx = models.CharField("提交给微信的运单号", max_length=64, null=True)
    # shipping_number_2wx = models.CharField("提交给微信的运单号", max_length=32, null=True)

    class Meta:
        app_label = APP_LABEL_AFS


class OrderStepPay(BaseModelTimeAndDeleted):
    # order_id 订单ID(主键)
    order_id = models.PositiveIntegerField(primary_key=True, editable=False)
    # order_number 订单编号
    order_number = models.CharField("Order number", max_length=64, db_index=True)
    # presale_id = models.PositiveIntegerField('预售ID', db_index=True)
    # presale_name = models.CharField("预售名称", max_length=128)
    deposit_start_time = models.DateTimeField("定金开始时间", blank=True, null=True)
    deposit_end_time = models.DateTimeField("定金结束时间", blank=True, null=True)
    tail_start_time = models.DateTimeField("尾款开始时间", blank=True, null=True)
    tail_end_time = models.DateTimeField("尾款开始时间", blank=True, null=True)
    # deposit_paytime 定金支付时间
    deposit_paytime = models.DateTimeField("定金支付时间", blank=True, null=True)
    # tail_paytime 尾款支付时间
    tail_paytime = models.DateTimeField("尾款支付时间", blank=True, null=True)
    # point_txt 积分描述
    point_txt = models.CharField("积分描述", max_length=32, blank=True, null=True)
    # tail_overtime_time 尾款超时时间
    tail_overtime_time = models.DateTimeField("尾款超时时间", blank=True, null=True)

    class Meta:
        ordering = ['-created_time']
        app_label = APP_LABEL_AFS


class LineStepPay(BaseModelTimeAndDeleted):
    # line_id 行ID（主键）
    line_id = models.PositiveIntegerField(primary_key=True, editable=False)
    # order_id 订单ID(主键)
    order_id = models.PositiveIntegerField(db_index=True)
    # order_number 订单编号
    order_number = models.CharField("Order number", max_length=36, db_index=True)
    # product_id
    product_id = models.PositiveIntegerField(db_index=True)
    # productmain_id
    productmain_id = models.PositiveIntegerField(db_index=True)
    presale_id = models.PositiveIntegerField('预售ID', db_index=True)
    presale_name = models.CharField("预售名称", max_length=50)
    deposit_start_time = models.DateTimeField("定金开始时间", blank=True, null=True)
    deposit_end_time = models.DateTimeField("定金结束时间", blank=True, null=True)
    tail_start_time = models.DateTimeField("尾款开始时间", blank=True, null=True)
    tail_end_time = models.DateTimeField("尾款开始时间", blank=True, null=True)

    class Meta:
        app_label = APP_LABEL_AFS
        ordering = ['-created_time']


class LineDeliverTime(BaseModelTimeAndDeleted):
    # line_id 行ID（主键）
    line_id = models.PositiveIntegerField(primary_key=True, editable=False)
    # order_id 订单ID
    order_id = models.PositiveIntegerField(editable=False, db_index=True)
    # order_number 订单编号
    order_number = models.CharField("Order number", max_length=36, db_index=True)
    # product_id
    product_id = models.PositiveIntegerField(db_index=True)
    # productmain_id
    productmain_id = models.PositiveIntegerField(db_index=True)
    # deliver_time 发货时间
    deliver_time = models.DateTimeField("发货时间", blank=True, null=True)
    # deliver_time_type 发货时间类型(fixed_time 固定时间/pay_relative_time支付相对时间)
    deliver_time_type = models.CharField("发货时间类型", max_length=32, choices=DeliverTimeType.DELIVERTIME_TYPE_CHOICES, blank=True, null=True)
    # relative_time 相对时间(单位：天)
    relative_time = models.DecimalField("相对时间", decimal_places=2, max_digits=12, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL_AFS


class OrderPaymentInst(BaseModelTimeAndDeleted):
    """
    该表记录下来了订单所有的支付方式
    """
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    # id(主键uuid)
    id = models.CharField(max_length=36, primary_key=True, default=get_uuid4_hex, editable=False)
    # 订单自增id
    order_id = models.PositiveIntegerField(
        _('Order ID'), blank=True, null=True)
    # 支付类型
    payment_type = models.CharField("Payment type", max_length=10, blank=True, null=True)
    # 支付金额
    amount = models.DecimalField(
        "Amount", decimal_places=2, max_digits=12)
    # 用来记录支付的详细信息：
    #   优惠券：优惠券ID coupon_id
    #   店内优惠券存 code
    #   C券：用户 account_id
    #   微信支付：用户 微信支付ID
    #   支付宝支付：用户 支付宝支付ID
    payment_num = models.CharField('支付号', max_length=50, blank=True, null=True)
    # 如果是券的话，券的来源
    coupon_source = models.CharField('来源', max_length=64, blank=True, null=True, choices=CouponSourceChoices, default=CouponSource.IN_STORE)
    # 优惠券面值
    coupon_amount = models.PositiveIntegerField('优惠券面值', blank=True, null=True)
    note = models.CharField('备注', max_length=200, blank=True, null=True)
    # 如果支付方式是礼券，对应于：S001_OrderPayDetail中的Objid，其他默认为0
    # 信息部的字段
    list_id = models.IntegerField('List ID', default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)
    # 财务需要知道我们真正收到钱的时间
    cash_received_time = models.DateTimeField("收到现金类支付的时间", blank=True, null=True, db_index=True)
    # 支付账号（支付现金类的数据，才有此值，退款时需要用原支付账号退回）
    pay_channel = models.CharField('支付账号', max_length=50, blank=True, null=True)
    # order_number 订单编号
    order_number = models.CharField("订单编号", max_length=36, blank=True, null=True)
    # order_number_pay 子支付订单编号(订单编号加“-1”或者“-2”)
    order_number_pay = models.CharField("子支付订单编号", max_length=36, blank=True, null=True, db_index=True)
    # pay_step_type 支付阶段类型(all全款/deposit定金/tailpay尾款)
    pay_step_type = models.CharField("Pay Step Type", max_length=12, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)
    # coupon_name 券名
    coupon_name = models.CharField("券名", max_length=50, blank=True, null=True)
    # order_number_pay_status 子支付单状态(init初始/doing进行中/done已完成)
    order_number_pay_status = models.CharField("子支付单状态", max_length=12, blank=True, null=True, choices=Order_Number_Pay_Status.ORDER_NUMBER_PAY_STATUS_CHOICES, default=Order_Number_Pay_Status.INIT, db_index=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class LineOrderPaymentInst(BaseModelTimeAndDeleted):
    '''记录下来详细的 Line 支付结果 和所获取的积分'''
    # id(主键uuid)
    id = models.CharField(max_length=40, primary_key=True, default=get_uuid4_hex, editable=False)
    # Line
    line_id = models.PositiveIntegerField('Line ID', blank=True, null=True, db_index=True)
    # OrderPayment
    orderpayment_id = models.CharField('Order Payment ID', max_length=36, blank=True, null=True, db_index=True)
    # 支付类型
    payment_type = models.CharField("Payment type", max_length=10, blank=True, null=True)
    # 如果是钱类的，就存金额。如果是积分支付，就用amount存积分
    amount = models.DecimalField("Amount", decimal_places=2, max_digits=12)
    # order_id 订单ID
    order_id = models.PositiveIntegerField(editable=False, blank=True, null=True, db_index=True)
    # order_number 订单编号
    order_number = models.CharField("Order number", blank=True, null=True, max_length=36)
    # order_number_pay 子支付订单编号(订单编号加“-1”或者“-2”)
    order_number_pay = models.CharField("子支付订单编号", blank=True, null=True, max_length=36)
    # pay_step_type 支付阶段类型(all全款/deposit定金/tailpay尾款)
    pay_step_type = models.CharField("Pay Step Type", max_length=24, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)
    # 参与积分的金额 —— 可积分的金额（此line总共）
    amount_for_point = models.DecimalField('用户实际支付金额——参与积分的金额', default=Decimal('0'), decimal_places=2, max_digits=12)
    # 积分基数-金额 积分基数，比如1元20积分，这个字段就是1元。支持两位小数
    point_amount = models.DecimalField('积分基数对应的金额，以元为单位', default=Decimal('1'), decimal_places=2, max_digits=12)
    # 用户获取积分 此line总共用户应该获得的积分
    points = models.PositiveIntegerField('Points', default=0)
    # coupon_name 券名
    coupon_name = models.CharField("券名", max_length=50, blank=True, null=True)
    # 当支付类型是微信17时，这记录的是流水号，当支付类型是礼券16时，这里记录的是券号
    payment_num = models.CharField('支付号', max_length=50, blank=True, null=True)
    # 积分倍数 积分倍数，比如1元20积分，这个字段就是20。支持两位小数
    point_multiple = models.DecimalField('积分倍数', default=Decimal('1'), decimal_places=2, max_digits=12)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']
