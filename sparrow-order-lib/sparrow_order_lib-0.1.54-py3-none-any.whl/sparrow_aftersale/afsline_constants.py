from ..core.constants import UserRole


class EventMapKey(object):

    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class AfsLineStatus:
    ''' 退款单表体状态 '''
    # 待审核
    OPEN = "open"
    # 已拒绝
    REFUSED = "refused"
    # 已关闭
    CLOSED = 'closed'
    # 待客人寄回
    PENDING_CUSTOMER_RETURN = "pending_customer_return"
    # 客人已寄回
    CUSTOMER_RETURNED = "customer_returned"
    # 客服已收货
    CUSSERVICE_RECEIVED = "cusservice_received"
    # 进入退换货仓
    AFTERSALE_WH = "AftersaleWH"
    # 导购收货
    GUIDE_RECEIVED = "guide_received"
    # 待客服退货
    PENDING_CUSSERVICE_RETURN = "pending_cusservice_return"
    # 待外仓退货
    PENDING_OUTSTORAGE_RETURN = "pending_outstorage_return"
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 已完成
    COMPLETED = 'completed'

    CHOICES_FOR_A = (
        # OPEN 待审核
        (OPEN, "待审核"),
        # 已拒绝
        (REFUSED, "已拒绝"),
        # 已关闭
        (CLOSED, '已关闭'),
        # 待客人寄回
        (PENDING_CUSTOMER_RETURN, "待客人寄回"),
        # 客人已寄回
        (CUSTOMER_RETURNED, "客人已寄回"),
        # 客服已收货
        (CUSSERVICE_RECEIVED, "客服已收货"),
        # 进入退换货仓
        (AFTERSALE_WH, "退货仓上架"),
        # 导购收货
        (GUIDE_RECEIVED, "导购收货"),
        # 待客服退货
        (PENDING_CUSSERVICE_RETURN, "待客服退货"),
        # 待外仓退货
        (PENDING_OUTSTORAGE_RETURN, "待外仓退货"),
        # 待退款
        (PENDING_REFUND, "待退款"),
        # 完成
        (COMPLETED, '已完成'),
    )

    CHOICES_FOR_B = CHOICES_FOR_A

    CHOICES_FOR_P = CHOICES_FOR_A

    NAME_MAP_A = dict(CHOICES_FOR_A)


class AfsLineEventConst:
    '''
    ### 事件 ###
    '''

    # 拒绝退货申请
    REFUSE = 'refuse'
    # 取消退货
    CANCEL = "cancel"
    # 客户回填运单信息
    CUS_WRITE_BACK = "cus_write_back"
    # 客服收货
    CUSSERVICE_RECEIVE = 'cusservice_receive'
    # 取消客服收货
    CANCEL_CUSSERVICE_RECEIVE = 'cancel_cusservice_receive'
    # 售后仓入库
    ENTER_AFTERSALE_WH = 'enter_aftersale_wh'
    # 导购收货
    GUIDE_RECEIVE = "guide_receive"
    # 导购确退
    GUIDE_CONFIRM = 'guide_confirm'
    # 未出专柜审核，直接到待退款
    APPROVE_NO_ASSIGN = "approve_no_assign"
    # 售后完成
    COMPLETE = 'complete'

    EVENT_2_BUTTONNAME_MAP = {
        APPROVE_NO_ASSIGN: "未出专柜审核通过",
        CANCEL: "关闭",
        CUS_WRITE_BACK: "客户回填运单信息",
        GUIDE_RECEIVE: "导购收货",
        GUIDE_CONFIRM: "导购确退",
        ENTER_AFTERSALE_WH: "售后仓入库"
    }

    EVENT_2_CNAME_MAP = {
        APPROVE_NO_ASSIGN: "未出专柜审核通过",
        CANCEL: "关闭换货",
    }

    # 注意：
    # 1、当不存在EventMapKey.USER_ROLES_KEY的key时，说明所有角色都可以操作；
    # 2、当EventMapKey.TO_STATUS_KEY对应的value设置为None时，则说明动作不会造成状态变更；
    FROM_TO_MAP = {
        APPROVE_NO_ASSIGN: {  # 导购同意客户换货
            AfsLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.AUTO, UserRole.CUSSERVICE]
            }
        },
        REFUSE: {
            AfsLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.REFUSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.AUTO, UserRole.CUSSERVICE]
            }
        },
        CANCEL: {  # 取消换货
            AfsLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
            AfsLineStatus.PENDING_CUSTOMER_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
        },
        CUS_WRITE_BACK: {  # 客户回填运单信息
            AfsLineStatus.PENDING_CUSTOMER_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CUSTOMER_RETURNED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSTOMER, UserRole.CUSSERVICE]
            },
        },
        CUSSERVICE_RECEIVE: {
            AfsLineStatus.PENDING_CUSTOMER_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CUSSERVICE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            AfsLineStatus.CUSTOMER_RETURNED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CUSSERVICE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
        },
        CANCEL_CUSSERVICE_RECEIVE: {
            AfsLineStatus.CUSSERVICE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.CUSTOMER_RETURNED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
        },
        ENTER_AFTERSALE_WH: {
            AfsLineStatus.CUSSERVICE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.AFTERSALE_WH,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
        },
        GUIDE_RECEIVE: {  # 打印
            AfsLineStatus.AFTERSALE_WH: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.GUIDE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            AfsLineStatus.PENDING_CUSSERVICE_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.GUIDE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
        },
        GUIDE_CONFIRM: {
            AfsLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.PENDING_CUSSERVICE_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.PENDING_CUSTOMER_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.CUSTOMER_RETURNED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.CUSSERVICE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.GUIDE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.AFTERSALE_WH: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
            AfsLineStatus.PENDING_OUTSTORAGE_RETURN: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            }
        },
        COMPLETE: {
            AfsLineStatus.PENDING_REFUND: {
                EventMapKey.TO_STATUS_KEY: AfsLineStatus.COMPLETED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.AUTO, UserRole.CUSTOMER]
            }
        }
    }

    # # 按钮排序
    # EVENT_CONST_SORT_MAP = {
    #     CANCEL: 0,
    #     COMMENT: 1,
    #     APPROVE: 2,
    #     CONFIRM: 2,
    #     GUIDE_EXPRESS: 2,
    #     PRINT: 3,
    #     CUS_SELF_SERVICE: 4,
    # }


class AfsLineGenerateFrom:
    SELECT = 'select'  # 创建售后时选中的
    VIRTUAL = 'virtual'  # 虚拟订单数据
    ORIGIN = 'origin'  # 创建售后前的订单(或虚拟订单)数据

    CHOICES = (
        (SELECT, "创建售后时选择的商品"),
        (VIRTUAL, "虚拟订单数据"),
        (ORIGIN, "创建售后前的订单(或虚拟订单)数据"),
    )

    NON_AFSLINE = [VIRTUAL, ORIGIN]
