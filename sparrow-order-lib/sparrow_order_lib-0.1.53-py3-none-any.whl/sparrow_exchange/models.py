import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..core.constants import UserRole
from ..core.base_models import BaseModelTimeAndDeleted
from ..core.formats import EXCHANGE_NUMBER_FMT
from ..core.numbers import getRandomNumSet
from ..core.common_utils import get_uuid4_hex
from ..sparrow_distribute.constants import DistributeStatus
from .constants import ExchangeOrderStatus
from .constants import ExchangeLineStatus
from .constants import ExchangeReturnShippingMethod
from . import APP_LABEL


def get_sparrow_exchange_number():
    '''
    发货单number生成规则， 年月日时分秒+"-"+6位随机数，比如20200513123086-564734
    '''
    now = datetime.datetime.now()
    random_set = getRandomNumSet(6)
    number = now.strftime(EXCHANGE_NUMBER_FMT).format(rand=random_set)
    return number


# exchangeorder 换货总单
class ExchangeOrder(BaseModelTimeAndDeleted):
    # id 主键
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # exo_number 换货总单编号
    exo_number = models.CharField("Exchange Number", max_length=64, db_index=True, unique=True, default=get_sparrow_exchange_number)
    # order_id 订单ID
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number 订单编号
    order_number = models.CharField('Order Number', max_length=64, blank=True, null=True, db_index=True)
    # order_created_time 订单下单时间
    order_created_time = models.DateTimeField("Order Created Time", blank=True, null=True, default=None)
    # order_type 订单类型
    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True)
    # exo_status 总单状态
    exo_status = models.CharField('总单状态', max_length=32, blank=True, null=True, choices=ExchangeOrderStatus.EXCHANGE_ORDER_STATUS_CHOICES, db_index=True, default=ExchangeOrderStatus.IN_PROCESS)
    # ----- 申请人
    # apply_user_role 申请人角色
    apply_user_role = models.CharField('申请人角色', max_length=32, blank=True, null=True, choices=UserRole.USERROLE_CHOICES)
    # apply_user_id 申请人ID
    apply_user_id = models.CharField('申请人id', max_length=255, blank=True, null=True, db_index=True)
    # apply_user_username 申请人账号
    apply_user_username = models.CharField('申请人账号', max_length=15, help_text=u'申请人账号', blank=True, null=True, db_index=True)
    # apply_user_name 申请人姓名
    apply_user_name = models.CharField('申请人姓名', max_length=15, help_text=u'申请人姓名', blank=True, null=True)
    # ----- 客户
    # customer_user_id 客户ID
    customer_user_id = models.CharField('申请人id', max_length=255, blank=True, null=True, db_index=True)
    # customer_user_username 客户账号
    customer_user_username = models.CharField('申请人账号', max_length=15, help_text=u'申请人账号', blank=True, null=True, db_index=True)
    # customer_user_name 客户姓名
    customer_user_name = models.CharField('申请人姓名', max_length=15, help_text=u'申请人姓名', blank=True, null=True)
    # customer_member_xx_level (客户会员级别)
    customer_member_xx_level = models.CharField('Customer Member Level', max_length=128, blank=True, null=True)
    # customer_member_xx_level (客户会员号)
    customer_member_number = models.CharField('Customer Member Number', max_length=128, blank=True, null=True)
    # exaddress_id (将换货回寄给客户的地址)
    exaddress_id = models.PositiveIntegerField('换货地址ID', blank=True, null=True)

    class Meta:
        ordering = ['-created_time']
        app_label = APP_LABEL

    @property
    def exchange_lines(self):
        return ExchangeLine.objects.filter(exo_id=self.id)


class ExchangeLine(BaseModelTimeAndDeleted):
    # id 主键
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # exo_number 换货总单编号
    exo_number = models.CharField("换货总单编号", max_length=64, db_index=True)
    # exo_id 换货总单ID
    exo_id = models.CharField('换货总单 ID', max_length=100, blank=True, null=True, db_index=True)
    # number 换货分单编号
    exline_number = models.CharField("换货分单编号", max_length=64, db_index=True, unique=True)
    # order_id 订单ID
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number 订单编号
    order_number = models.CharField('Order Number', max_length=64, blank=True, null=True, db_index=True)
    # order_type 订单类型
    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True)
    # exline_status 分单状态
    exline_status = models.CharField('分单状态', max_length=32, blank=True, null=True, choices=ExchangeLineStatus.EXCHANGE_LINE_STATUS_CHOICES, db_index=True, default=ExchangeLineStatus.OPEN)
    # distribute_id 发货单ID
    distribute_id = models.CharField('新发货单 ID', max_length=100, blank=True, null=True)
    # distribute_number 发货单编号
    distribute_number = models.CharField("Distribute Number", max_length=128, blank=True, null=True)
    # distribute_status 申请换货时发货单状态
    distribute_status = models.CharField('配货单状态', max_length=128, blank=True, null=True, choices=DistributeStatus.DISTRIBUTE_STATUS_CHOICES, db_index=True)
    # distribute_line_id 发货单行ID
    distribute_line_id = models.CharField('新发货单行 ID', max_length=100, blank=True, null=True, db_index=True)
    # product_id 单品ID
    product_id = models.PositiveIntegerField('Product ID', blank=True, null=True, db_index=True)
    # productmain_id 主商品ID
    productmain_id = models.PositiveIntegerField('ProductMain ID', blank=True, null=True, db_index=True)
    # giftproduct_id 赠品ID
    giftproduct_id = models.PositiveIntegerField('赠品 ID', blank=True, null=True, db_index=True)
    # is_gift 是否是赠品
    is_gift = models.BooleanField("是否是赠品", default=False)
    # title 商品名称
    title = models.CharField("Product title", max_length=255, blank=True, null=True)
    # quantity 商品数量
    quantity = models.PositiveIntegerField('SKU换货数量', default=1)
    # offer 中分类
    offer = models.CharField("中分类", max_length=2, default="0")
    # barcode 条形码
    barcode = models.CharField("Product Barcode", max_length=1024, default='0')
    # sku_attr 型号
    sku_attr = models.CharField("Product SKU Attr", max_length=255, blank=True, null=True)
    # hg_code 汉光码
    hg_code = models.CharField("Product HG Code", max_length=255, blank=True, null=True)
    # shop_sku 货号
    shop_sku = models.CharField("Shop SKU", max_length=128, blank=True, null=True)
    # main_image 图片地址
    main_image = models.ImageField("Main Image", null=True, blank=True, max_length=255)
    # original_price 原价
    original_price = models.DecimalField("Original Price", decimal_places=2, max_digits=12, blank=True, null=True)
    # retail_price 售价
    retail_price = models.DecimalField("Retail Price", decimal_places=2, max_digits=12, blank=True, null=True)
    # brand_id 品牌ID
    brand_id = models.PositiveIntegerField('Brand ID', blank=True, null=True)
    # brand_name 品牌名称
    brand_name = models.CharField("Brand Name", max_length=128, blank=True, null=True)
    # shop_id 专柜ID
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True)
    # shop_num 专柜编号
    shop_num = models.CharField("Shop number", max_length=128, blank=True)
    # shop_name 专柜名称
    shop_name = models.CharField("Shop Name", max_length=128, blank=True, null=True)
    # print_time 打印次数
    print_times = models.IntegerField(_("打印次数"), default=0)
    # apply_reason 申请换货原因
    apply_reason = models.CharField("申请换货原因", max_length=64, blank=True)
    # apply_reason_detail 申请换货原因描述
    apply_reason_detail = models.CharField("申请换货原因描述", max_length=512, blank=True)
    # apply_img1 换货图片1
    apply_img1 = models.PositiveIntegerField("换货图片1", blank=True, null=True)
    # apply_img2 换货图片2
    apply_img2 = models.PositiveIntegerField("换货图片2", blank=True, null=True)
    # apply_img3 换货图片3
    apply_img3 = models.PositiveIntegerField("换货图片3", blank=True, null=True)
    # apply_img4 换货图片4
    apply_img4 = models.PositiveIntegerField("换货图片4", blank=True, null=True)
    # apply_img5 换货图片5
    apply_img5 = models.PositiveIntegerField("换货图片5", blank=True, null=True)
    # apply_img6 换货图片6
    apply_img6 = models.PositiveIntegerField("换货图片6", blank=True, null=True)

    # ----- 申请人

    # apply_user_role 申请人角色
    apply_user_role = models.CharField('申请人角色', max_length=32, blank=True, null=True, choices=UserRole.USERROLE_CHOICES)
    # apply_user_id 申请人ID
    apply_user_id = models.CharField('申请人id', max_length=255, blank=True, null=True, db_index=True)
    # apply_user_username 申请人账号
    apply_user_username = models.CharField('申请人账号', max_length=15, help_text=u'申请人账号', blank=True, null=True, db_index=True)
    # apply_user_name 申请人姓名
    apply_user_name = models.CharField('申请人姓名', max_length=15, help_text=u'申请人姓名', blank=True, null=True)

    # ----- 客户
    # customer_user_id 客户ID
    customer_user_id = models.CharField('申请人id', max_length=255, blank=True, null=True, db_index=True)
    # customer_user_username 客户账号
    customer_user_username = models.CharField('申请人账号', max_length=15, help_text=u'申请人账号', blank=True, null=True, db_index=True)
    # customer_user_name 客户姓名
    customer_user_name = models.CharField('申请人姓名', max_length=15, help_text=u'申请人姓名', blank=True, null=True)
    # customer_member_xx_level (客户会员级别)
    customer_member_xx_level = models.CharField('Customer Member Level', max_length=128, blank=True, null=True)
    # customer_member_xx_level (客户会员号)
    customer_member_number = models.CharField('Customer Member Number', max_length=128, blank=True, null=True)

    # cus_expresscode 客户退货回填快递公司
    cus_expresscode = models.CharField('客户退货回填快递公司', max_length=16, blank=True, null=True)
    # cus_shippingnumber 客户退货回填快递单号
    cus_shippingnumber = models.CharField('客户退货回填快递单号', max_length=32, blank=True, null=True)
    # guide_expresscode 导购新发货快递公司
    guide_expresscode = models.CharField('导购新发货快递公司', max_length=16, blank=True, null=True)
    # guide_shippingnumber 导购新发货运单号
    guide_shippingnumber = models.CharField('导购新发货运单号', max_length=32, blank=True, null=True)

    # exaddress_id (将换货回寄给客户的地址)
    exaddress_id = models.PositiveIntegerField('换货地址ID', blank=True, null=True)
    # terminate_time 终结时间
    terminate_time = models.DateTimeField("Date Terminated", blank=True, null=True, default=None)
    # terminate_user_id 终结人
    terminate_user_id = models.CharField("Terminate User ID", max_length=32, blank=True, null=True)
    terminate_user_name = models.CharField("Terminate User Name", max_length=15, blank=True, null=True)
    terminate_user_displayname = models.CharField("Terminate User Displayname", max_length=15, blank=True, null=True)
    terminate_user_role = models.CharField("Terminate User Role", max_length=15, blank=True, null=True)
    # order_created_time 订单下单时间
    order_created_time = models.DateTimeField("Order Created Time", blank=True, null=True, default=None)
    # pending_return_time 导购审批之后状态变为待客人寄回商品的时间
    pending_return_time = models.DateTimeField("Pending Return Time", blank=True, null=True, default=None)

    class Meta:
        ordering = ['-created_time']
        app_label = APP_LABEL

    @property
    def exchange_notes(self):
        return ExchangeNote.objects.filter(exline_id=self.id)

    @property
    def exchange_address(self):
        return ExchangeAddress.objects.filter(id=self.exaddress_id).first()

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

    @property
    def exreturn_method(self):
        if not self.exline_status == ExchangeLineStatus.DONE:
            return None
        elif self.guide_shippingnumber:
            return ExchangeReturnShippingMethod.EXPRESS
        else:  # 换货完成, 且没有寄出换货的单号 则为自提
            return ExchangeReturnShippingMethod.SELF_SERVICE


class ExchangeNote(BaseModelTimeAndDeleted):
    # id 主键
    id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
    # exo_number 换货总单编号
    exo_number = models.CharField("换货总单编号", max_length=64, db_index=True)
    # exo_id 换货总单ID
    exo_id = models.CharField('换货总单 ID',max_length=100,  blank=True, null=True, db_index=True)
    # number 换货分单编号
    exline_number = models.CharField("换货分单编号", max_length=64, db_index=True)
    # exline_id 换货分单ID
    exline_id = models.CharField('换货分单ID',max_length=64, blank=True, null=True, db_index=True)
    # order_id 订单ID
    order_id = models.PositiveIntegerField('Order ID', blank=True, null=True, db_index=True)
    # order_number 订单编号
    order_number = models.CharField('Order Number', max_length=64, blank=True, null=True, db_index=True)
    # event 事件
    event = models.CharField('事件', max_length=32, blank=True, null=True, db_index=True)
    # event_name 事件名称
    event_name = models.CharField('事件名称', max_length=32, blank=True, null=True)
    # event_time 事件发生时间
    event_time = models.CharField('事件发生时间', max_length=128, blank=True, null=True, db_index=True)
    # opt_user_role 操作人角色（客服、客户、导购）
    opt_user_role = models.CharField('操作人角色', max_length=32, blank=True, null=True, choices=UserRole.USERROLE_CHOICES)
    # opt_user_id 操作人ID
    opt_user_id = models.CharField('操作人ID', max_length=255, blank=True, null=True, db_index=True)
    # opt_user_username 操作人账号
    opt_user_username = models.CharField('操作人账号', max_length=15, help_text=u'申请人账号', blank=True, null=True, db_index=True)
    # opt_user_name 操作人姓名
    opt_user_name = models.CharField('操作人姓名', max_length=15, help_text=u'申请人姓名', blank=True, null=True)
    # from_status 开始状态
    from_status = models.CharField('起始状态', max_length=128, blank=True, null=True, db_index=True)
    # to_status 结束状态
    to_status = models.CharField('结果状态', max_length=128, blank=True, null=True, db_index=True)
    # message 消息
    message = models.CharField('信息', max_length=2048, blank=True, null=True)
    # message_level 消息级别
    message_level = models.PositiveIntegerField("Log Level", default=1, db_index=True)
    # message_detail 消息明细
    message_detail = models.CharField('开发看的信息', max_length=2048, blank=True, null=True)

    class Meta:
        ordering = ['-created_time']
        app_label = APP_LABEL

    def __str__(self):
        return "日志【id={id}】: 发起人【{opt_user_role} {opt_user_name} {opt_user_username}】在时间【{event_time}】执行了事件【{event}】, \
            换货单【id={exline_id}; number={exline_number}】从状态【{from_status}】变成了【{to_status}】，相关订单为【id={order_id}; \
                number={order_number}】, 具体信息为【level:{message_level}; msg={message}】; message_detail={message_detail}".\
            format(
                id=self.id,
                opt_user_role=self.opt_user_role,
                opt_user_name=self.opt_user_name,
                opt_user_username=self.opt_user_username,
                event_time=self.event_time,
                event=self.event,
                exline_id=self.exline_id,
                exline_number=self.exline_number,
                from_status=self.from_status,
                to_status=self.to_status,
                order_id=self.order_id,
                order_number=self.order_number,
                message=self.message,
                message_level=self.message_level,
                message_detail=self.message_detail
            )


class ExchangeAddress(BaseModelTimeAndDeleted):
    '''
    ### 将换货回寄给客户的地址 ###
    '''
    addr_name = models.CharField('姓名', max_length=64,blank=True)
    addr_phone = models.CharField('收件人手机号', max_length=11,unique=False)
    addr_detail = models.CharField('地址详情', max_length=255, blank=True)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.addr_name, self.addr_phone, self.detail)

    class Meta:
        ordering = ['-created_time']
        app_label = APP_LABEL
