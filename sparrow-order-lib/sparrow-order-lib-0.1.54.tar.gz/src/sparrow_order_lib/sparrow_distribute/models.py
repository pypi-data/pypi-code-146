import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..core.base_models import BaseModelTimeAndDeleted
from ..core.common_utils import get_uuid4_hex
from ..core.constants import ShippingMethod
from ..core.numbers import getRandomNumSet
from ..sparrow_orders.constants import PayMethod
from ..sparrow_orders.constants import DeliverTimeType
from .constants import DistributeStatus
from . import APP_LABEL

__all__ = ['Distribute', 'Distributeline', 'FootPrint', 'ExpressRela',
           'QueryResult', 'QueryResultDetail', 'OlayToken', 'EventPool',
           'EventPoolDetail', 'DeviceConfig', 'AddressGroup', 'AddressGroupRela']


def get_sparrow_distribute_number():
    '''
    发货单number生成规则， 年月日时分秒+"-"+6位随机数，比如20200513123086-564734
    '''
    now = datetime.datetime.now()
    random_set = getRandomNumSet(6)
    number = now.strftime('%y%m%d%H%M%S') + '-' + random_set
    return number


class Distribute(BaseModelTimeAndDeleted):
    '''
    配货单总表
    '''
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # 发货单名称（包裹1、包裹2等，这个名称并不是固定的，由于客户提货或者售后造成的拆单，可能造成这个字段值发生变化）
    name = models.CharField("Distribute Name", max_length=128, blank=True, null=True, default="")
    # number(发货单号）
    number = models.CharField("Distribute number", max_length=128, db_index=True, unique=True, default=get_sparrow_distribute_number)
    # origin_id（原始发货单id）
    origin_id = models.CharField('原始发货单id', max_length=100, blank=True, null=True, db_index=True)
    # parent_id（上一级发货单id）
    parent_id = models.CharField('上一级发货单id', max_length=100, blank=True, null=True, db_index=True)
    # order_id (订单主键)
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True, db_index=True)
    # 订单下单时间
    order_created_time = models.DateTimeField("Order Created Time", blank=True, null=True, default=None)
    # distribute_status(配货单状态：初始态、已打印、导购已取货、客服已取货、已发货等等)
    distribute_status = models.CharField('配货单状态', max_length=128, blank=True, null=True, choices=DistributeStatus.DISTRIBUTE_STATUS_CHOICES, db_index=True)
    # aftersale_status(有售后，无售后)
    aftersale_status = models.BooleanField("是否有售后", default=False, db_index=True)
    # shipping_method(发货方式：自提、快递、闪送)
    shipping_method = models.CharField('发货方式', max_length=128, blank=True, null=True, choices=ShippingMethod.CHOICES, db_index=True)
    # print_times打印次数
    print_times = models.IntegerField(_("打印次数"), default=0)
    # shop_id(专柜id)
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True, db_index=True)
    # shop_num(专柜号)
    shop_num = models.CharField("Shop number", max_length=128, blank=True, db_index=True)
    # shop_name(专柜号)
    shop_name = models.CharField("Shop Name", max_length=128, blank=True)
    # customer_user_id  (客户id)
    customer_user_id = models.CharField('客户id', max_length=255, blank=True, null=True, db_index=True)
    # customer_member_xx_level (客户会员级别)
    customer_member_xx_level = models.CharField('Customer Member Level', max_length=128, blank=True, null=True)
    # customer_member_xx_level (客户会员号)
    customer_member_number = models.CharField('Customer Member Number', max_length=128, blank=True, null=True)
    # customer_displayname (客户昵称)
    customer_displayname = models.CharField('客户昵称', max_length=15, help_text=u'客户昵称', blank=True, null=True)
    # customer_username (客户手机号)
    customer_username = models.CharField('客户手机号', max_length=15, help_text=u'客户手机号', blank=True, null=True)
    # # 指 ShippingAddress 的地址快照ID
    shipping_address_id = models.PositiveIntegerField('Shipping Address Id', blank=True, null=True, db_index=True)
    # 发货单终结时间
    terminate_time = models.DateTimeField("Time Terminate", blank=True, null=True, default=None)
    # 发货单终结操作人ID
    terminate_user_id = models.CharField("Terminate User ID", max_length=255, blank=True, null=True, db_index=True)
    # 发货单终结操作人名称
    terminate_user_name = models.CharField("Terminate User Name", max_length=255, blank=True, null=True)
    # 发货单终结操作人角色
    terminate_user_role = models.CharField("Terminate User Role", max_length=16, blank=True, null=True)
    # 导购留言
    guide_note = models.CharField('导购留言', max_length=16384, blank=True, null=True)
    # 出货时间
    out_time = models.DateTimeField("Out Time", blank=True, null=True, default=None)
    # 出货操作人
    out_user_id = models.CharField("Out User ID", max_length=255, blank=True, null=True, db_index=True)
    # 出货操作人姓名
    out_user_name = models.CharField("Out User Name", max_length=255, blank=True, null=True)
    # 出货操作人角色
    out_user_role = models.CharField("Out User Role", max_length=16, blank=True, null=True)
    # 发货单所有者
    out_user_owner = models.CharField("Owner", max_length=16, blank=True, null=True)
    # 外仓id
    outstorage_id = models.CharField("Outstorage ID", max_length=255, blank=True, null=True, db_index=True)
    # 出货方向（Guide、CusService、OutStorage）
    out_direction = models.CharField("Out Direction", max_length=64, blank=True, null=True, db_index=True)
    # if_need_exchange -- 是否需换货
    if_need_exchange = models.BooleanField("是否需换货", default=False)
    # exchange_status -- 是否已换货
    exchange_status = models.BooleanField("是否已换货", default=False)

    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True)

    # 支付方法（once 一次支付/twice两次支付）
    pay_method = models.CharField("支付方法", max_length=24, choices=PayMethod.PAY_METHOD_CHOICES, blank=True, null=True, default=PayMethod.ONCE)

    # tail_paytime 尾款支付时间(分阶段支付订单，且尾款支付成功后，才会这个值)
    tail_paytime = models.DateTimeField("尾款支付时间", blank=True, null=True)

    # 发货单上的商品数量
    total_quantity = models.IntegerField('商品数量', null=True, blank=True, default=0)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class Distributeline(BaseModelTimeAndDeleted):
    '''
    配货单明细
    '''
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # distribute_id(发货单id)
    distribute_id = models.CharField('Distribute ID', max_length=100, blank=True, null=True, db_index=True)
    # distribute_number(发货单号）
    distribute_number = models.CharField("Distribute Number", max_length=128)
    # order_id (订单主键)
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True)
    # line_id(订单行id)
    line_id = models.PositiveIntegerField('Line ID', blank=True, null=True, db_index=True)
    # brand_id(品牌id)
    brand_id = models.PositiveIntegerField('Brand ID', blank=True, null=True)
    # shop_id(专柜id)
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True, db_index=True)
    # shop_num(专柜号)
    shop_num = models.CharField("Shop number", max_length=128, blank=True)
    # product_id(商品id)
    product_id = models.PositiveIntegerField('Product ID', blank=True, null=True, db_index=True)
    # giftproduct_id(赠品id)
    giftproduct_id = models.PositiveIntegerField('赠品 ID', blank=True, null=True, db_index=True)
    # title(商品名称)
    title = models.CharField("Product title", max_length=255)
    # quantity (发货数量)
    quantity = models.PositiveIntegerField("Quantity", default=1)
    # offer(中分类)
    offer = models.CharField("中分类", max_length=2, default="0", db_index=True)
    # 发货每件商品实际付款金额
    actual_pay_per_product = models.DecimalField("发货每件商品实际付款金额", decimal_places=2, max_digits=12, blank=True, null=True, default=0)
    # 商品条码
    barcode = models.CharField("Product Barcode", max_length=1024, blank=True, null=True, default='')
    # 商品sku Attr
    sku_attr = models.CharField("Product SKU Attr", max_length=255, blank=True, null=True)
    # 商品汉光码
    hg_code = models.CharField("Product HG Code", max_length=255, blank=True, null=True)
    # 这个商品的原价（比如吊牌价）（1件的价格）
    original_price = models.DecimalField("Original Price", decimal_places=2, max_digits=12, blank=True, null=True)
    # 这个商品的售价（1件的价格）
    retail_price = models.DecimalField("Retail Price", decimal_places=2, max_digits=12, blank=True, null=True)
    # 专柜收入 —— 这个line（此line总共）专柜的收入
    shop_income_price = models.DecimalField("专柜收入", decimal_places=2, max_digits=12, blank=True, null=True, default=0)
    # 订单里图片不单独上传，用商品数据库字段里的值
    main_image = models.ImageField("Main Image", null=True, blank=True, max_length=255)
    shop_sku = models.CharField("Shop SKU", max_length=128, blank=True, null=True, db_index=True)
    shop_name = models.CharField("Shop Name", max_length=128, blank=True, null=True)
    brand_name = models.CharField("Brand Name", max_length=128, blank=True, null=True)
    is_gift = models.BooleanField("是否是赠品", default=False, db_index=True)
    is_fixed_price_product = models.BooleanField("是否为换购", default=False)
    # aftersale_id (当本发货单是退单时，需要记录对应的售后单id)
    aftersale_id = models.PositiveIntegerField('售后单 ID', blank=True, null=True, db_index=True, default=None)
    # aftersale_line_id (当本发货单是退单时，需要记录对应的售后单行id)
    aftersale_line_id = models.PositiveIntegerField('售后单行 ID', blank=True, null=True, db_index=True, default=None)
    # aftersale_number (当本发货单是退单时，需要记录对应的售后单号)
    aftersale_number = models.CharField("售后单号", max_length=128, blank=True, null=True, default=None)
    # ----------- 2021-06-17 ---换货单新增如下字段 ---开始-----------
    # productmain_id 主商品ID
    productmain_id = models.PositiveIntegerField('ProductMain ID', blank=True, null=True, db_index=True)
    # if_need_exchange -- 是否需换货
    if_need_exchange = models.BooleanField("是否需换货", default=False)
    # exchange_status -- 是否已换货
    exchange_status = models.BooleanField("是否已换货", default=False)
    # number 换货分单编号
    exline_number = models.CharField("换货分单编号", max_length=64, blank=True, null=True, db_index=True)
    # exline_id 换货分单ID
    exline_id = models.CharField('换货分单ID', max_length=64, blank=True, null=True, db_index=True)
    # ----------- 2021-06-17 ------结束-----------

    # 订单类型
    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True)

    # deliver_time 预定发货时间
    deliver_time = models.DateTimeField("发货时间", blank=True, null=True)
    # 商品类目
    categories = models.CharField('商品类目', max_length=128, blank=True, null=True, default=None)

    # deliver_time_type 发货时间类型(fixed_time 固定时间/pay_relative_time支付相对时间)
    deliver_time_type = models.CharField("发货时间类型", max_length=32, choices=DeliverTimeType.DELIVERTIME_TYPE_CHOICES, blank=True, null=True)
    # deliver_relative_time 相对时间(单位：天)
    deliver_relative_time = models.DecimalField("相对时间", decimal_places=2, max_digits=12, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class FootPrint(BaseModelTimeAndDeleted):
    '''
    配货单足迹
    '''
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # distribute_id(新发货单id)
    distribute_id = models.CharField('Distribute ID', max_length=100, blank=True, null=True, db_index=True)
    # distribute_number(新发货单号)
    distribute_number = models.CharField("Distribute Number", max_length=128)
    # order_id (订单主键)
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True)
    # event(事件)
    event = models.CharField('事件', max_length=128, blank=True, null=True, db_index=True)
    # event_remarks(事件备注)
    event_remarks = models.CharField('事件备注', max_length=36, blank=True, null=True)
    # event_sponsor（事件发起人）
    event_sponsor = models.CharField('事件发起人', max_length=255, blank=True, null=True)
    # event_sponsor_name（事件发起人昵称）
    event_sponsor_name = models.CharField('事件发起人昵称', max_length=255, blank=True, null=True)
    # event_sponsor_role (事件发起人角色)
    event_sponsor_role = models.CharField('事件发起人角色', max_length=16, blank=True, null=True)
    # event_time(事件发生时间)
    event_time = models.DateTimeField("Event Happened Time", blank=True, null=True, auto_now=True)
    # from_status(起始状态)
    from_status = models.CharField('起始状态', max_length=128, blank=True, null=True, db_index=True)
    # to_status(结果状态)
    to_status = models.CharField('结果状态', max_length=128, blank=True, null=True, db_index=True)
    # message(展示信息，比如导购已接单，导购已配单完成，客服已取货，已发货等等)
    message = models.CharField('信息', max_length=16384, blank=True, null=True)
    # message_detail(数据详细信息)
    message_detail = models.CharField('开发看的信息', max_length=2048, blank=True, null=True)
    # level (=1给客户看，=2给客服看，>0展示所有数据)
    message_level = models.PositiveIntegerField("Log Level", default=1, db_index=True)
    # device_no 机台号
    device_no = models.CharField('机台号', max_length=32, blank=True, null=True)
    # if_device 是否用自助工作台操作
    if_device = models.BooleanField("是否用自助工作台操作", default=False)

    def __str__(self):
        return "日志【id={id}】: 发起人【{event_sponsor}】在时间【{event_time}】执行了事件【{event}】, 发货单【id={distribute_id}; " \
               "number={distribute_number}】从状态【{from_status}】变成了【{to_status}】，相关订单为【id={order_id}; number={order_number}】, " \
               "具体信息为【level:{message_level}; msg={message}】; message_detail={message_detail}".\
            format(
                id=self.id,
                event_sponsor=self.event_sponsor,
                event_time=self.event_time,
                event=self.event,
                distribute_id=self.distribute_id,
                distribute_number=self.distribute_number,
                from_status=self.from_status,
                to_status=self.to_status,
                order_id=self.order_id,
                order_number=self.order_number,
                message=self.message,
                message_level=self.message_level,
                message_detail=self.message_detail
            )

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class ExpressRela(BaseModelTimeAndDeleted):
    '''
    发货单与运单关系表
    加这一张表，可以实现多对多关系
    '''
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # distribute_id(新发货单id)
    distribute_id = models.CharField('Distribute ID', max_length=100, default=get_uuid4_hex, db_index=True)
    # distribute_number(新发货单id)
    distribute_number = models.CharField('Distribute Number', max_length=128)
    # order_id (订单主键)
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True)
    # newexpressorder_id(运单信息id)
    newexpressorder_id = models.CharField(max_length=100, default=get_uuid4_hex, editable=False)
    # if_main 是否主单（当发生合单时，将给主单与运单关联数据打上此标记，表示运单先由此发货单生成）
    if_main = models.BooleanField("是否主单", default=True)
    # 是否参与了合单
    if_merge = models.BooleanField("是否合单", default=False)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class QueryResult(BaseModelTimeAndDeleted):
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class QueryResultDetail(BaseModelTimeAndDeleted):
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    query_result_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    busi_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class OlayToken(BaseModelTimeAndDeleted):
    # id(主键uuid)
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    access_token = models.CharField('Access Token', max_length=512, blank=True, null=True)
    token_type = models.CharField('Token Type', max_length=64, blank=True, null=True)
    refresh_token = models.CharField('Refresh Token', max_length=512, blank=True, null=True)
    expires_time = models.DateTimeField('过期时间', null=True, blank=True)
    scope = models.CharField('使用范围', max_length=32, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL


class EventPool(BaseModelTimeAndDeleted):
    '''
    发货单批量操作池
    '''
    # id 主键
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # device_no 机台号
    device_no = models.CharField('机台号', max_length=32)
    # number 序列号 -- 发货单操作池number生成规则， 设备号+"-"+事件类型+"-"+年月日时分秒
    number = models.CharField("Event Pool number", max_length=128, blank=True, null=True, db_index=True, unique=True)
    # login_user_id 登录人ID
    login_user_id = models.CharField('登录人ID', max_length=255, blank=True, null=True)
    # login_user_role 登录人角色
    login_user_role = models.CharField('登录人角色', max_length=16, blank=True, null=True)
    # creator_id 创建人ID
    creator_id = models.CharField('创建人ID', max_length=40, blank=True, null=True, db_index=True)
    # creator_role 创建人角色
    creator_role = models.CharField('创建人角色', max_length=16, blank=True, null=True, db_index=True)
    # creator_username 创建人手机号
    creator_username = models.CharField('创建人手机号', max_length=15, help_text=u'创建人手机号', blank=True, null=True)
    # creator_displayname 创建人昵称
    creator_displayname = models.CharField('创建人昵称', max_length=15, help_text=u'创建人昵称', blank=True, null=True)
    # creator_shop_id 创建人所属专柜ID
    creator_shop_id = models.PositiveIntegerField('创建人所属专柜ID', blank=True, null=True, db_index=True)
    # creator_shop_num 创建人所属专柜号
    creator_shop_num = models.CharField('创建人所属专柜号', max_length=20, blank=True, null=True)
    # event 事件
    event = models.CharField('事件', max_length=128, blank=True, null=True, db_index=True)
    # event_name 事件名称
    event_name = models.CharField('事件名称', max_length=128, blank=True, null=True)
    # start_time 事件开始执行时间
    start_time = models.DateTimeField("Event Start Time", blank=True, null=True)
    # end_time 事件结束执行时间
    end_time = models.DateTimeField("Event End Time", blank=True, null=True)

    class Meta:
        app_label = APP_LABEL


class EventPoolDetail(BaseModelTimeAndDeleted):
    '''发货单批量操作池 详单'''
    # id 主键
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # pool_id 操作池ID
    pool_id = models.CharField('操作池ID', max_length=255, blank=True, null=True, db_index=True)
    # pool_number 操作池序列号
    pool_number = models.CharField("Event Pool number", max_length=128, blank=True, null=True, db_index=True)
    # distribute_id(发货单id)
    distribute_id = models.CharField('Distribute ID', max_length=100, blank=True, null=True, db_index=True)
    # distribute_number(发货单号）
    distribute_number = models.CharField("Distribute Number", max_length=128)
    # distribute_status_before 操作前发货单状态
    distribute_status_before = models.CharField('操作前发货单状态', max_length=128, blank=True, null=True, choices=DistributeStatus.DISTRIBUTE_STATUS_CHOICES)
    # distribute_status_after 操作后发货单状态
    distribute_status_after = models.CharField('操作后发货单状态', max_length=128, blank=True, null=True, choices=DistributeStatus.DISTRIBUTE_STATUS_CHOICES)
    # scan_time 扫入发货单时间
    scan_time = models.DateTimeField("Event Scan Time", blank=True, null=True, auto_now_add=True)
    # event 事件
    event = models.CharField('事件', max_length=128, blank=True, null=True, db_index=True)
    # event_name 事件名称
    event_name = models.CharField('事件名称', max_length=128, blank=True, null=True)
    # event_time(事件发生时间)
    event_time = models.DateTimeField("Event Happened Time", blank=True, null=True)
    # if_event_succ 是否执行成功
    if_event_succ = models.BooleanField("是否执行成功", blank=True, null=True, default=None)
    #  执行失败原因
    event_failed_reason = models.CharField('执行失败原因', max_length=2048, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        unique_together = ('pool_number', 'distribute_number',)


class DeviceConfig(BaseModelTimeAndDeleted):
    device_no = models.CharField("设备号", max_length=128, blank=True, null=True)
    unique_code = models.CharField("设备唯一标识码", max_length=128, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL


class AddressGroup(BaseModelTimeAndDeleted):

    # id(主键uuid)
    id = models.CharField(max_length=64, primary_key=True, default=get_uuid4_hex, editable=False)
    user_id = models.CharField('User ID', max_length=64, db_index=True)
    address = models.CharField("地址", max_length=256)
    address_key = models.CharField("地址key", max_length=64, db_index=True)

    class Meta:
        app_label = APP_LABEL


class AddressGroupRela(BaseModelTimeAndDeleted):

    # id(主键uuid)
    distribute_id = models.CharField(max_length=64, primary_key=True)
    group_id = models.CharField('Group ID', max_length=64, db_index=True)

    class Meta:
        app_label = APP_LABEL


class UserShipReminderSum(BaseModelTimeAndDeleted):
    '''
    客户发货提醒总计
    '''
    # id 主键
    id = models.CharField(max_length=40, primary_key=True, default=get_uuid4_hex, editable=False)
    # order_id 订单ID
    order_id = models.PositiveIntegerField(editable=False, blank=True, null=True, db_index=True)
    # distribute_id 发货单ID
    distribute_id = models.CharField('Distribute ID', max_length=100, blank=True, null=True, db_index=True)
    # user_id 客户ID
    user_id = models.CharField("User ID", max_length=40, blank=True, null=True, db_index=True)
    # total_cnt 客户操作提醒总次数
    total_cnt = models.IntegerField('客户操作提醒总次数', default=1)
    # reminder_date 客户操作提醒日期（单位：日）
    reminder_date = models.DateField("客户操作提醒日期", blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class UserShipReminderDetail(BaseModelTimeAndDeleted):
    '''
    客户发货提醒明细
    '''
    # id 主键
    id = models.CharField(max_length=40, primary_key=True, default=get_uuid4_hex, editable=False)
    # order_id 订单ID
    order_id = models.PositiveIntegerField(editable=False, blank=True, null=True, db_index=True)
    # distribute_id 发货单ID
    distribute_id = models.CharField('Distribute ID', max_length=100, blank=True, null=True, db_index=True)
    # user_id 客户ID
    user_id = models.CharField("User ID", max_length=40, blank=True, null=True, db_index=True)
    # reminder_time 客户操作提醒时间
    reminder_time = models.DateTimeField("客户操作提醒时间", blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']


class UserOptCount(BaseModelTimeAndDeleted):

    opt_user_id = models.CharField('User ID', max_length=40, db_index=True)
    # opt_username 操作员手机号
    opt_username = models.CharField('操作员手机号', max_length=15, help_text=u'操作员手机号', blank=True, null=True)
    # opt_displayname 操作员姓名
    opt_displayname = models.CharField("操作员姓名", max_length=10, blank=True, null=True)
    # opt_user_role 操作员角色
    opt_user_role = models.CharField("操作员橘色", max_length=15, blank=True, null=True)
    # event_code 事件编码
    event_code = models.CharField("事件编码", max_length=36, db_index=True)
    # event_name 事件名称
    event_name = models.CharField("事件名称", max_length=36)
    # event_day 发生日
    event_day = models.DateField(blank=True, null=True, auto_now=True)
    # opt_times 操作次数
    opt_times = models.PositiveIntegerField("操作次数", default=0)
    # shop_id 专柜id
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True, db_index=True)
    # shop_name 专柜号
    shop_name = models.CharField("Shop Name", max_length=36, blank=True)
    # shop_num(专柜号)
    shop_num = models.CharField("Shop number", max_length=12, blank=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']
        # 联合约束
        unique_together = ["opt_user_id", "event_day", "event_code", "shop_id"]

    def __str__(self):
        return f'{self.opt_username}-{self.opt_displayname}-{self.event_code}-{self.event_day}-{self.shop_name}'


class UserOptDetail(BaseModelTimeAndDeleted):
    opt_user_id = models.CharField('User ID', max_length=40, db_index=True)
    # opt_username 操作员手机号
    opt_username = models.CharField('操作员手机号', max_length=15, help_text=u'操作员手机号', blank=True, null=True)
    # opt_displayname 操作员姓名
    opt_displayname = models.CharField("操作员姓名", max_length=10, blank=True, null=True)
    # opt_user_role 操作员角色
    opt_user_role = models.CharField("操作员橘色", max_length=15, blank=True, null=True)
    # event_code 事件编码
    event_code = models.CharField("事件编码", max_length=36, db_index=True)
    # event_name 事件名称
    event_name = models.CharField("事件名称", max_length=36)
    # event_day 发生日
    event_day = models.DateField(blank=True, null=True, auto_now=True)
    # opt_times 操作次数
    opt_times = models.PositiveIntegerField("操作次数", default=0)
    # shop_id 专柜id
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True, db_index=True)
    # shop_name 专柜号
    shop_name = models.CharField("Shop Name", max_length=36, blank=True)
    # shop_num 专柜号
    shop_num = models.CharField("Shop number", max_length=12, blank=True)
    # distribute_id 发货单id
    distribute_id = models.CharField('Distribute ID', max_length=40, blank=True, null=True, db_index=True)
    # distribute_number 发货单号
    distribute_number = models.CharField("Distribute Number", max_length=40)
    # from_status(起始状态)
    from_status = models.CharField('起始状态', max_length=24, blank=True, null=True, db_index=True)
    # to_status(结果状态)
    to_status = models.CharField('结果状态', max_length=24, blank=True, null=True, db_index=True)
    # 运单号
    shipping_number = models.CharField("快递单号/母单号", max_length=64, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.opt_username}-{self.opt_displayname}-{self.event_code}-{self.event_day}-{self.shop_name}'
