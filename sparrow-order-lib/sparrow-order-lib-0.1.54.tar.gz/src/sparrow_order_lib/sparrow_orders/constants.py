# 这些常量会在其他地方被用到，用作某些判断
import logging
import warnings

logger = logging.getLogger(__name__)

class ReversedStockStatus(object):
    # 默认状态
    INIT = "init"
    # 缺货
    SHORTAGE = "shortage"
    # 无货需要下架
    OFF = "off"
    # 备好货
    PREPARED = "prepared"


class ReversedStockType(object):
    PRODUCT = "product"
    GIFT = "gift"


class ReversedStockActions(object):
    # 导购标记货品
    GUIDE_MARK = "guide_mark"
    # 客服取货
    PICK_UP = "pick_up"
    # 客服还货
    RETURN = "return"


class ReversedStockNoteMessage(object):
    GUIDE_MARK = '标记货品状态为{0}'
    PICK_UP = '客服提货'
    RETURN = '客服还货'


class RequiredCountStock(object):
    IS_STOCK = "is_stock"
    IS_REQUIRED_COUNT = "is_required_count"
    IS_ANY = "is_any"

class AssignmentActions(object):
    # 创建配货
    CREATE = "create"
    # 关闭配货
    REMOVE = "remove"
    # 完成配货
    COMPLETE = "complete"
    # 已打印
    PRINTED = "printed"


class OrderActions(object):
    # 售后单独有一个Note表
    # 负库存相关单独有一个Note表
    # 修改
    MODIFY_ADDRESS = "modify_address"
    # 修改客服备注
    MODIFY_OPERATOR_NOTE = "modify_operator_note"
    # 关闭订单
    CLOSE = "close"
    # 发起支付
    PAY = "pay"
    # 完成支付订单
    COMPLETE_PAYMENT = "complete_payment"
    # 发货
    SEND = "send"
    # 用户提货
    TAKE = "take"
    # 其他
    OTHERS = "others"
    # 创建订单
    CREATE = "create"
    # 生成发货单
    GENERATE_DISTRIBUTE = "generate_distribute"
    # 给客户发短信
    SEND_SMS_MESSAGE = "send_sms_message"


class OrderTypes(object):
    # 线上订单
    ONLINE = "online"
    # 闪购
    FLASHSALE = "flashsale"
    # 贩卖机类型，现场直接出货
    VENDING = "vending"
    # 贩卖机类型，现场直接出货： 样机种草
    VENDING_MACHINE_HR = "vending_machine_hr"
    # 互动触摸屏类型，提货需要到专柜
    SCREEN = "screen"
    # rfid 订单类型
    RFID = "rfid"
    # 拼团订单
    GROUP = "group"
    # 积分商城
    POINTS_MALL = "points_mall"
    # 汉光贩售机
    HGVENDING = "hgvending"
    # 海淘
    HAITAO = "haitao"

    ORDER_TYPES_CHOICES = (
        (ONLINE, "线上订单"),
        (FLASHSALE, "闪购订单"),
        (VENDING, "售货机自提"),
        (VENDING_MACHINE_HR, "样机种草"),
        (SCREEN, "互动触摸屏"),
        (RFID, "RFID"),
        (GROUP, "拼团订单"),
        (HGVENDING, "汉光贩售机"),
        (HAITAO, "海淘"),
    )


class __OrderShippingMethods(object):
    warnings.warn("已废弃", DeprecationWarning)

    SELF_SERVICE = "self_service"
    EXPRESS = "express"

    def __getattribute__(self, name: str):
        value = super().__getattribute__(name)
        logger.warn("sparrow_order_lib.sparrow_order.constants.OrderShippingMethod 已废弃, 请使用 sparrow_order_lib.core.constants.ShippingMethod 替换")
        return value


OrderShippingMethods = __OrderShippingMethods()


class OrderStatus(object):
    """订单对外展示状态"""
    # 2018-02-08 确定新的四个统一订单对外状态
    # 待付款
    UNPAID = "unpaid"
    # 准备中
    PREPARING = "preparing"
    # 可提货，待发货
    TO_DELIVER = "to_deliver"
    # 已发货，已完成
    COMPLETED = "completed"
    # 已关闭/取消
    CLOSED = "closed"
    # 订单不再筛选售后状态！

    # 售后
    AFTERSALE = "after_sale"
    # 待发货
    TO_SHIP = "to_ship"
    # 可自提
    TO_PICKUP = "to_pickup"

    # 待付款
    # UNPAID = "unpaid"
    # # 备货中
    # IN_PREPARING = "in_preparing"
    # # 待发货
    # TO_SEND = "to_send"
    # # 待提货
    # TO_TAKE = "to_take"
    # # 部分发货
    # PARTIALLY_SENT = "partially_sent"
    # # 已发货
    # SENT = "sent"
    # # 部分提货
    # PARTIALLY_TAKEN = "partially_taken"
    # # 已提货
    # TAKEN = "taken"
    # # 退换/售后
    # IN_AFTERSALE = "in_aftersale"
    # # 已关闭/取消
    # CLOSED = "closed"


class OrderPayStatus(object):
    # 订单支付状态
    UNPAID = "unpaid"
    PAY_FINISHED = "pay_finished"
    CLOSED = "closed"
    # ------------- 分阶段支付 --------------
    # 定金待支付
    TO_DEPOSITPAY = "to_depositpay"
    # 尾款待支付
    TO_TAILPAY = "to_tailpay"
    # 尾款超时
    TAILPAY_OVERTIME = "tailpay_overtime"

    ORDER_PAY_STATUS_CHOICE = (
        (UNPAID, "未支付"),
        (PAY_FINISHED, "支付完成"),
        (CLOSED, "已关闭"),
        (TO_DEPOSITPAY, "待支付定金"),
        (TO_TAILPAY, "待支付尾款"),
        (TAILPAY_OVERTIME, "尾款超时"),
    )
    ORDER_PAY_STATUS_DICT = dict(ORDER_PAY_STATUS_CHOICE)


class OrderGroupStatus(object):
    # 拼团中
    PROGRESS = "progress"
    # 已成团
    SUCCESS = "success"
    # 拼团失败
    FAIL = "fail"


class OrderAssignStatus(object):
    '''订单配货状态'''
    # 无配货 - 没有ready或completed的发货单，或者说没有发货单或发货单只有closed的
    INIT = "init"
    # 部分配货 - 有ready的发货单，但是ready的发货单里的line的总数总量不全
    PARTIAL = "partial"
    # 全部配货 - 有不是closed的发货单，全部发货单里全部line数量总量和订单一致
    COMPLETED = "completed"


class OrderShippingStatus(object):
    '''订单发货状态'''
    # 未发货 - 没有completed的发货单
    INIT = "init"
    # 部分发货 - 有completed的发货单，里面的line总量不全
    PARTIAL = "partial"
    # 全部发货 - completed的发货单里面的line总量和订单一致
    COMPLETED = "completed"


class OrderAftersaleStatus(object):
    # 订单售后状态
    # 有待处理售后
    OPEN = "open"
    # 无售后
    NONE = "none"
    # 售后都完成（因为同时open的售后单只会有一单）
    DONE = "done"


class OrderExchangeStatus(object):
    '''### 订单换货状态###'''
    # 有待处理售后
    OPEN = "open"
    # 无售后
    NONE = "none"
    # 换货都完成（因为同时open的换货单只会有一单）
    DONE = "done"
    # 配货状态
    EXCHANGE_STATUS = (
        (OPEN, "有在进行的换货"),
        (NONE, "无换货"),
        (DONE, "换货已完成"),
    )

class CouponSource(object):
    # 线上发的券
    ONLINE = "online"
    # 店内发的券
    IN_STORE = "store"


class ProductSaleType(object):
    # 实物类型
    REAL = "REAL"

    # 虚拟商品
    VIRTUAL = "VIRTUAL"


class SettingsLabel(object):
    """
    系统配置
    """
    # 客服主管拦截
    SUPERVISOR_INTERCEPTION = "supervisor_interception"


class InnerApiUri(object):
    ALIPAY = "/api/sparrow_alipay/i/alipay_aftersale_returned/"
    REFUND_QUERY = "/api/sparrow_alipay/i/alipay_aftersale_returned_query/"
    PRODUCT = "/api/sparrow_products_i/pure_products/{}/"


class ErrorCode(object):
    SUCCESS = 0  # 成功
    FLASH_HAS_PICKUP = 201001  # 闪购订单已提货，不能发起退单。
    HAS_VALID_AFTERSALE = 201002  # 此订单已发起售后
    HAS_VALID_ASSIGNMENT = 201003  # 此订单已配货，请点击申请售后
    REFUND_ERROR = 201004  # 退款失败


class BatchAssignType(object):
    '''订单配货类型'''
    # 全部配货
    WHOLE = "whole"
    # 部分配货
    PARTIAL = "partial"
    # 按商品部分配货
    PRODUCT = "product"
    # 按专柜部分配货
    SHOP = "shop"


class BatchAssignTaskStatus(object):
    '''订单配货任务执行状态'''
    # 正在进行中
    IN_PROGRESS = "in_progress"
    # 已经完成
    COMPLETED = "completed"
    # 执行出错
    ERROR = "error"

class HGVendingStatus(object):
    # 初始态
    INIT = "init"
    # 已取货
    PICKED_UP = "picked_up"
    # 已售后
    REFUND = "refund"
    # 超时未支付关闭
    CLOSED = "closed"

    HGVENDING_STATUS_CHOICES = (
        (INIT, "初始态"),
        (PICKED_UP, "已取货"),
        (REFUND, "已售后"),
        (CLOSED, "已关闭")
    )


# 贩售机取货码过期检测定时任务运行间隔
HGVENDING_BULK_TASK_INTERVAL = 15 * 60


class DeliverTimeType(object):
    '''
    发货时间类型(fixed_time 固定时间/pay_relative_time 支付相对时间)
    '''
    FIXED_TIME = "fixed_time"
    PAY_RELATIVE_TIME = "pay_relative_time"
    DELIVERTIME_TYPE_CHOICES = (
        (FIXED_TIME, "固定时间"),
        (PAY_RELATIVE_TIME, "支付相对时间")
    )


class PayMethod(object):
    '''支付方法（once 一次支付/twice两次支付）'''
    ONCE = "once"
    TWICE = "twice"
    PAY_METHOD_CHOICES = (
        (ONCE, "一次支付"),
        (TWICE, "两次支付")
    )


class DeliverTimeStatus(object):
    '''发货时间配置状态(none无需配置/to_configure待配置/configured已配置)'''
    NONE = "none"
    TO_CONFIGURE = "to_configure"
    CONFIGURED = "configured"
    DELIVERTIME_STATUS_CHOICES = (
        (NONE, "无需配置"),
        (TO_CONFIGURE, "待配置"),
        (CONFIGURED, "已配置")
    )


class PayStepType(object):
    '''支付阶段类型(all全款/deposit定金/tailpay尾款)'''
    ONCE = "once"
    DEPOSIT = "deposit"
    TAIL = "tail"
    PAY_STEP_TYPE_CHOICES = (
        (ONCE, "全款"),
        (DEPOSIT, "定金"),
        (TAIL, "尾款")
    )


STEP_CHAR = "&"


class AssignmentStatus(object):
    '''发货单邮寄状态'''
    # 只要创建了发货单就认为是配货了
    # 已配货，待发货（无快递单号）或待提货
    READY = "ready"
    # 已完成-有快递单号了，或者用户来自提了
    COMPLETED = "completed"
    # 已取消
    # 发货单不能删除，只能关闭取消
    CLOSED = "closed"

class Order_Number_Pay_Status(object):
    # 子支付单状态(init初始/doing进行中/done已完成)
    INIT = "init"
    DOING = "doing"
    DONE = "done"
    FAILED = "failed"
    ORDER_NUMBER_PAY_STATUS_CHOICES = (
        (INIT, '初始'),
        (DOING, '进行中'),
        (DONE, "已完成"),
        (FAILED, "失败"),

    )
    ORDER_NUMBER_PAY_STATUS_DICT = dict(ORDER_NUMBER_PAY_STATUS_CHOICES)
