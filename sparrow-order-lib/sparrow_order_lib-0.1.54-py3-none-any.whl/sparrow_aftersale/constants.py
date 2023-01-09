from ..core.datastructures import ImmutableList


class AfsLineStatus:
    ''' 退款单表体状态 '''
    # 导购收货
    # GUIDE_RECEIVED = "GuideReceived"
    GUIDE_RECEIVED = "guide_received"

    CHOICES = (
        (GUIDE_RECEIVED, "导购收货"),
    )


class Aftersale_Number_Refund_Status(object):
    # 退单子退款状态(init初始/doing进行中/done已完成)
    INIT = "init"
    DOING = "doing"
    DONE = "done"
    FAILED = "failed"
    AFTERSALE_NUMBER_REFUND_STATUS_CHOICES = (
        (INIT, '初始'),
        (DOING, '进行中'),
        (DONE, "已完成"),
        (FAILED, "失败"),

    )
    AFTERSALE_NUMBER_REFUND_STATUS_DICT = dict(AFTERSALE_NUMBER_REFUND_STATUS_CHOICES)


class WechatDeliveryReturnStatus:
    """ 用户寄回时的方式 """
    INIT = 0  # 用户未填写退货信息
    APPLY = 1  # 在线预约
    SELF = 2  # 自主填写


class WechatDeliveryReturnOrderStatus:
    """ 退单状态 """
    INIT = 0  # 已下单, 待揽收
    PACKAGED = 1  # 已揽件
    TRANSIT = 2  # 运输中
    DELIVERING = 3  # 派件中
    SELF_SIGNED = 4  # 已签收
    ABNORMAL = 5  # 异常
    PRE_SIGNED = 6  # 代签收
    FAIL_PACKAGED = 7  # 揽件失败
    FAIL_SIGNED = 8  # 签收失败(拒签、超区)
    CANCEL = 11  # 已取消
    RETURNING = 13  # 退件中
    RETURNED = 14  # 已退件
    UNHEARD = 99  # 未知

    # 非终态退单状态
    UNTERMINATE_ORDER_TYPE_LIST = ImmutableList(
        [INIT, PACKAGED, TRANSIT, DELIVERING, RETURNING, UNHEARD]
    )


######### 以下内容来自 constant_event.py ##########
class EventMapKey(object):

    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class AfsNumberRefundEventConst(object):
    ### 子退单事件 ###
    # 子退单开始申请退
    START = "start"
    # 子退单完成
    SUCCESS = "success"
    # 子退单失败
    FAIL = "fail"

    EVENT_2_BUTTONNAME_MAP = {
        START: "子退单开始申请退",
        SUCCESS: "子退单完成",
        FAIL: "子退单失败"
    }

    FROM_TO_MAP = {
        START: {  # 子退单开始申请退
            Aftersale_Number_Refund_Status.INIT: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DOING,
                EventMapKey.USER_ROLES_KEY: None
            }
        },
        SUCCESS: {  # 子退单完成
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
        },
        FAIL: {  # 子退单失败
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            }
        }
    }


class AfsLineGenerateFrom:
    SELECT = 'select'  # 创建售后时选中的
    VIRTUAL = 'virtual'  # 虚拟订单数据
    ORIGIN = 'origin'  # 创建售后前的订单(或虚拟订单)数据

    CHOICES = (
        (SELECT, "创建售后时选择的商品"),
        (VIRTUAL, "虚拟订单数据"),
        (ORIGIN, "创建售后前的订单(或虚拟订单)数据"),
    )


class AfsVersionConst:
    V2 = "V2"
    V3 = "V3"


class AftersaleActions(object):
    # 创建售后单
    CREATE = "create"
    # 修改售后单
    UPDATE = "update"
    # 关闭售后单
    REMOVE = "remove"
    # 完成售后单
    COMPLETE = "complete"
    # 客服审核通过
    OPERATOR_APPROVE = "operator_approve"
    # 客服审核拒绝- 消费抖店拒绝售后消息
    OPERATOR_REFUSED = "operator_refused"
    # 财务审核通过
    FINANCE_APPROVE_1ST = "finance_approve_1st"
    # 财务审核通过
    FINANCE_APPROVE = "finance_approve"
    # 财务驳回
    FINANCE_REJECT = "finance_reject"
    # 店内系统驳回
    INSTORE_REJECT = "instore_reject"
    # 店内通过
    ALL_APPROVE = "all_approve"
    # 退款失败
    REFUND_FAIL = "refund_fail"
    # 开始退款
    START_REFUND = "start_refund"
    # 退款成功
    REFUND_SUCCEED = "refund_succeed"
    # 待退货
    PENDING_RETURN = "pending_return"
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 直接退款
    REFUND_DIRECTLY = "pending_directly"
    # 自动
    AUTO = "auto"
    # 确认已经退货
    CONFIRM_RETURNED = "confirm_returned"
    # 客户回填运单信息
    CUSTOMER_WRITEBACK_EXPRESS = "customer_writeback_express"
    # 拦截失败
    BLOCK_FAILED = "block_failed"
    # 客服修改运单信息
    CUSSERVICE_MODIFY_EXPRESS = "cusservice_modify_express"
    # 强制确收退货
    FORCE_CONFIRM_RETURNED = "force_confirm_returned"
    # 同步线下-总退单
    SYNC_OFFLINE = "sync_offline"
    # 同步线下-退款
    SYNC_OFFLINE_AFS = "sync_offline_afs"
    # 同步线下-营业外收入
    SYNC_OFFLINE_HGINCOME = "sync_offline_hgincome"
    # 打印退款单
    PRINT_AFTERSALE_SUB = "print"
    # 自动
    AUTO_REFUND = "auto_refund"



class AfterSaleType(object):
    # 正常售后单
    NORMAL = "normal"
    # 换货
    EXCHANGE= "exchange"
    # 投诉
    COMPLAINT = "complaint"
    # 催货
    REMINDER = "reminder"
    # 仅退运费
    ONLY_REFUND_POSTAGE = "only_refund_postage"
    # 其他
    OTHER = "other"
    # 退定金
    REFUND_DEPOIST = "refund_deposit"
    # 退海淘
    REFUND_HAITAO = "refund_haitao"
    # 仅退差价
    ONLY_REFUND = "onlyrefund"

    # 特殊售后单快递转自提退运费
    AFSPLUS_REFUND_POSTAGE = "afsplus_refund_postage"

    CHOICES = (
        (NORMAL, "退货退款"),
        (EXCHANGE, "换货"),
        (COMPLAINT, "投诉"),
        (REMINDER, "提醒发货"),
        (ONLY_REFUND_POSTAGE, "仅退运费"),
        (REFUND_DEPOIST, "退定金"),
        (REFUND_HAITAO, "退海淘"),
        (OTHER, "其他"),
        (ONLY_REFUND, "仅退差价"),
        (AFSPLUS_REFUND_POSTAGE, "退运费"),
    )

class AfterSaleReasons(object):
    """
    用户售后原因
    """
    # 催单
    REMINDER = "reminder"
    # 退运费
    RETURN_POST = "return_post"
    # 不喜欢/不想要了
    NOT_LIKE_OR_NOT_WANT = "not_like_or_not_want"
    # 快递太慢了不想等了
    SHIPPING_TOO_SLOW_AND_NO_WAIT= "shipping_too_slow_and_no_wait"
    # 快递太慢，帮我催一下
    SHIPPING_TOO_SLOW_AND_REMINDER= "shipping_too_slow_reminder"
    # 换货：质量问题
    EXCHANGE_PRODUCT_QUALITY_ISSUE = "exchange_product_quality_issue"
    # 退货：质量问题
    RETURN_PRODUCT_QUALITY_ISSUE = "return_product_quality_issue"
    # 退货：不喜欢，不想要了
    RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT = "return_product_not_like_or_not_want"
    # 退货：穿着不合适需退货
    RETURN_PRODUCT_INAPPROPRIATE = "return_product_inappropriate"
    # 换货：大小/款式不合适
    EXCHANGE_PRODUCT_INAPPROPRIATE = "exchange_inappropriate"
    # 退货：商品与描述不符
    RETURN_PRODUCT_DESCRIPTION_MISMATCH = "return_product_description_mismatch"
    # 其他
    OTHER = "other"
    ##其他前缀，用来做过滤查询
    OTHER_PREFIX = "其他-"
    ###############
    # 客人不想要了
    CUSTOMER_NOT_WANT = "customer_not_want"
    # 商品缺货，不想等了
    PRODUCT_LACK_NO_WAIT = "product_lack_no_wait"
    # 订单不能按预计时间送达
    ORDER_CANNOT_SHIPPING_ONTIME = "order_cannot_shipping_ontime"
    # 操作有误（商品、地址等选错）
    OPERATE_ERROR = "operate_error"
    # 重复下单/误下单
    ORDER_DUPLICATE = "order_duplicate"
    # 其他渠道价格更低
    CHIPPER_ON_OTHER_CHANNEL = "chipper_on_other_channel"
    # 该商品降价了
    CHIPPER_NOW = "chipper_now"
    # 重新下单买（商品/数量拍错了）
    ORDER_DUPLICATE2 = "order_duplicate2"
    # 不想买了
    NOT_WANT_ANYMORE = "not_want_anymore"
    # 用户整单退
    USER_ENTIRE_RETURN = "user_entire_return"
    # 整单退
    ENTIRE_RETURN = "entire_return"
    # 买多了/买错了
    BOUGHT_TOO_MUCH = "bought_too_much"
    # 计划有变，暂时不需要了
    PLAN_CHANGED = "plan_changed"
    #信息填错
    INFORMATION_ERROR = "information_error"
    #无法绑卡
    CAN_NOT_BIND_CARD = "can_not_bind_card"
    #发票问题
    INVOICE_ISSUE = "invoice_issue"

AFTERSALE_ALL_REASON_DICT = {
    AfterSaleReasons.REMINDER: "提醒发货",
    AfterSaleReasons.RETURN_POST: "退运费",
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT: "不喜欢/不想要了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT: "快递太慢了不想等了",
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
    AfterSaleReasons.EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
    AfterSaleReasons.EXCHANGE_PRODUCT_QUALITY_ISSUE:'换货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '退货：不喜欢，不想要了',
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH: '退货：商品与描述不符',
    AfterSaleReasons.CUSTOMER_NOT_WANT:"客人不想要了",
    AfterSaleReasons.PRODUCT_LACK_NO_WAIT: "商品缺货，不想等了",
    AfterSaleReasons.ORDER_CANNOT_SHIPPING_ONTIME: "订单不能按预计时间送达",
    AfterSaleReasons.OPERATE_ERROR: "操作有误（商品、地址等选错）",
    AfterSaleReasons.ORDER_DUPLICATE: "重复下单/误下单",
    AfterSaleReasons.CHIPPER_ON_OTHER_CHANNEL:"其他渠道价格更低",
    AfterSaleReasons.CHIPPER_NOW:"该商品降价了",
    AfterSaleReasons.ORDER_DUPLICATE2: "重新下单买（商品/数量拍错了）",
    AfterSaleReasons.NOT_WANT_ANYMORE: "不想买了",
    AfterSaleReasons.USER_ENTIRE_RETURN: "用户整单退",
    AfterSaleReasons.ENTIRE_RETURN: "整单退",
    AfterSaleReasons.OTHER: "其他",
    # 买多了/买错了
    AfterSaleReasons.BOUGHT_TOO_MUCH: "买多了/买错了",
    # 计划有变，暂时不需要了
    AfterSaleReasons.PLAN_CHANGED: "计划有变，暂时不需要了",
    # 信息填错
    AfterSaleReasons.INFORMATION_ERROR: "信息填错",
    # 无法绑卡
    AfterSaleReasons.CAN_NOT_BIND_CARD: "无法绑卡",
    # 发票问题
    AfterSaleReasons.INVOICE_ISSUE: "发票问题",
}

# 用户售后原因list
AFTERSALE_USER_REASON_LIST = [
    AfterSaleReasons.NOT_LIKE_OR_NOT_WANT,
    AfterSaleReasons.SHIPPING_TOO_SLOW_AND_NO_WAIT,
    AfterSaleReasons.RETURN_PRODUCT_QUALITY_ISSUE,
    AfterSaleReasons.RETURN_PRODUCT_INAPPROPRIATE,
    AfterSaleReasons.RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT,
    AfterSaleReasons.RETURN_PRODUCT_DESCRIPTION_MISMATCH,
    AfterSaleReasons.RETURN_POST,
    AfterSaleReasons.OTHER,
]
# 用户售后原因dict
AFTERSALE_USER_REASON_DICT = { item: AFTERSALE_ALL_REASON_DICT[item] for item in AFTERSALE_USER_REASON_LIST }

# E卡售后原因list
AFTERSALE_USER_REASON_HG_ECARD_LIST = [
    # 买多了/买错了
    AfterSaleReasons.BOUGHT_TOO_MUCH,
    # 计划有变，暂时不需要了
    AfterSaleReasons.PLAN_CHANGED,
    # 信息填错
    AfterSaleReasons.INFORMATION_ERROR,
    # 无法绑卡
    AfterSaleReasons.CAN_NOT_BIND_CARD,
    # 发票问题
    AfterSaleReasons.INVOICE_ISSUE,
]
# E卡售后原因dict
AFTERSALE_USER_REASON_HG_ECARD_DICT = { item: AFTERSALE_ALL_REASON_DICT[item] for item in AFTERSALE_USER_REASON_HG_ECARD_LIST }




class AftersaleStatus(object):

    # 财务待审
    IN_FINANCE = "in_finance"
    # 财务一审通过，待二审
    IN_FINANCE_2ND = "in_finance_2nd"
    # 财务驳回, 目前这个状态仅在抖店售后在抖店平台拒绝时使用
    REJECTED = "rejected"
    # 店内通过的售后单状态们
    # AFTER_APPROVES = [ALL_APPROVED, REFUND_FAILED, COMPLETED]
    # IN_OPENS = [OPEN, IN_FINANCE, IN_FINANCE_2ND, REJECTED, INSTORE_REJECTED]
    ######以上为需求v190611之前的状态，现在不用了,但必须保留做兼容#########

    # 待审核/审核中
    OPEN = "open"
    # 待退货
    PENDING_RETURN = "pending_return" 
    PENDING_RETURN_0 = "pending_return_0" # For C端， 待客服退货，此状态，在数据库中并不存在
    PENDING_RETURN_1 = "pending_return_1" # For C端， 待客人退货，此状态，在数据库中并不存在
    PENDING_RETURN_2 = "pending_return_2" # For C端， 待外仓退货，此状态，在数据库中并不存在
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 店内系统通过
    INSTORE_APPROVED = "instore_approved"
    # 店内系统驳回
    INSTORE_REJECTED = "instore_rejected"
    # 已完成主流程，不涉及退款 —— 这是一个中间状态，退款的时候用来校验
    # 这里店内系统也已经记录了，绝对不能改了。如果退款失败了只能单独和用户沟通或者店内系统也得改
    # 只有是这个状态才能发起退款
    ALL_APPROVED = "all_approved"

    # 退款失败
    REFUND_FAILED = "refund_failed"
    # 已完成
    COMPLETED = "completed"
    # 已取消，已关闭
    CLOSED = "closed"

    # 2022.07 售后单和发货单解耦新增中间状态
    OPENING = 'opening'  # 申请中
    CLOSING = 'closing'  # 关闭中
    COMPLETING = 'completing'  # 完成中
    OPEN_FAILED = 'open_failed'  # 申请售后失败
    CLOSE_FAILED = 'close_failed'  # 关闭售后失败
    COMPLETE_FAILED = 'complete_failed'  # 完成售后失败

    AFTERSALE_STATUS_CHOICES = (
        (OPEN, "待审核"),
        # (IN_FINANCE, "财务待审"),
        # (IN_FINANCE_2ND, "财务一审通过"),
        (REJECTED, "客服驳回"),
        (PENDING_RETURN, "待退货"),
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "店内系统通过"),
        (INSTORE_REJECTED, "店内系统驳回"),
        (ALL_APPROVED, "店内系统通过"),
        (REFUND_FAILED, "退款失败"),
        (COMPLETED, "已完成"),
        (CLOSED, "已取消"),
    )
    AFTERSALE_STATUS_CHOICES_FOR_C = (
        (OPEN, "待审核"),
        (PENDING_RETURN_0, "待审核"), # 待客服退货
        (PENDING_RETURN_1, "待退货"), # 待客人退货
        (PENDING_RETURN_2, "待退货"), # 发货拦截中
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "待退款"),
        (INSTORE_REJECTED, "待退款"),
        (ALL_APPROVED, "待退款"),
        (REFUND_FAILED, "待退款"),
        (COMPLETED, "已完成"),
        (CLOSED, "已关闭"),
    )
    AFTERSALE_MESSAGE_DICT_FOR_C = {
        # OPEN: ["您的退换货申请已提交，等待客服审核，请保持电话畅通。"],
        OPEN: ["您的售后已申请成功，待售后审核中"],
        # PENDING_RETURN_0: ["您的售后正在审核中，请耐心等待。"],
        PENDING_RETURN_0: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_1: ["您的售后已审核通过，请将售后商品邮寄到指定地址并填写物流单号，查看退货地址"],
        PENDING_RETURN_1: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_2: ["正在为您尝试拦截中，请耐心等待。"],
        PENDING_RETURN_2: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_REFUND: ["客服正在为您处理退款。"],
        PENDING_REFUND: ["您的售后待客服处理退款"],
        # INSTORE_APPROVED: ["客服正在为您处理退款。"],
        INSTORE_APPROVED: ["您的售后待客服处理退款"],
        # INSTORE_REJECTED: ["客服正在为您处理退款。"],
        INSTORE_REJECTED: ["您的售后待客服处理退款"],
        # ALL_APPROVED: ["客服正在为您处理退款。"],
        ALL_APPROVED: ["您的售后待客服处理退款"],
        # REFUND_FAILED: ["客服正在为您处理退款。"],
        REFUND_FAILED: ["您的售后待客服处理退款"],
        # COMPLETED: ["售后已完成，退款金额将原路返回到您的帐户，预计最晚到账1-7个工作日，请您注意查收。"],
        COMPLETED: ["售后服务已完成，感谢您对汉光的支持"],
        CLOSED: ["售后已关闭。"],
    }


class AftersaleFinanceStatus(object):
    # 未审核
    INIT = "init"
    # 一审通过
    APPROVED_1ST = "approved_1st"
    # 二审通过
    APPROVED = "approved"
    # 财务驳回
    REJECTED = "rejected"


class AftersaleFinanceType(object):
    '''一期有一些需要财务手动调账的'''
    # 普普通通的售后单
    AUTO = "auto"
    # 需要财务手动调账的售后单，微信不能自动退款
    MANUAL = "manual"

class AftersaleSource(object):
    """
    售后来源
    """
    # 客人发起
    GUEST_INITIATED = "guest_initiated"
    # 客服发起
    SERVICE_INITIATED = "service_initiated"

class AftersaleCancelSource(object):
    """
    售后取消来源
    """
    # 客人取消
    GUEST_CANCEL = "guest_cancel"
    # 客服取消
    SERVICE_CANCEL = "service_cancel"
    # 高级客服取消
    SUPER_SERVICE_CANCEL = "super_service_cancel"
    # 超时自动取消
    TIMEOUT_CANCEL = "timeout_cancel"

class AftersaleRefundStatus(object):
    # 未退款，初始状态
    INIT = "init"
    # 退款成功
    SUCCEEDED = "succeeded"
    # 退款失败
    FAILED = "failed"
