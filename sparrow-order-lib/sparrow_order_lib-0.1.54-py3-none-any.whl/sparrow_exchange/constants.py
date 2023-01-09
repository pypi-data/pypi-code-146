from ..core.constants import UserRole

BASE_EXCHANGE_API_CODE = 20106000


class ExchangeOrderStatus(object):
    '''
    ### 换货单总单状态 ###
    '''
    IN_PROCESS = "in_process"
    CLOSED = "closed"
    DONE = "done"
    EXCHANGE_ORDER_STATUS_CHOICES = (
        (IN_PROCESS, "进行中"),
        (DONE, "已完成"),
        (CLOSED, "已关闭"),
    )


class ExchangeOrderStatusForDistribute:
    '''
    发货单上要展示的换货状态, 由 if_need_exchange 和 exchange_status 计算而来
    '''

    EXO_STATUS_MAP = {
        0: "无换货",
        1: "换货中",
        2: "换货完成",
    }


class ExchangeLineStatus(object):
    '''
    ### 换货单分单状态 ###
    '''
    # 待审核
    OPEN = "open"
    # 已关闭
    CLOSED = "closed"
    # 待客户退回商品
    PENDING_RETURN = "pending_return"
    # 待确收商品
    PENDING_CONFIRM = "pending_confirm"
    # 待换货
    PENDING_EXCHANGE = "pending_exchange"
    # 客服收到寄回商品
    CUSSERVICE_RECEIVED = "cusservice_received"
    # 退换货仓
    AFTERSALE_WH = "AftersaleWH"
    # 换货完成
    DONE = "done"

    EXCHANGE_LINE_STATUS_CHOICES = (
        (OPEN, "待审核"),
        (PENDING_RETURN, "待客人寄回"),
        (PENDING_CONFIRM, "待专柜确收"),
        (PENDING_EXCHANGE, "待寄出换货"),
        (CUSSERVICE_RECEIVED, "客服收到寄回商品"),
        (AFTERSALE_WH, "退货仓上架"),
        (DONE, "换货完成"),
        (CLOSED, "已关闭"),
    )
    EXCHANGE_LINE_STATUS_DICT = dict(EXCHANGE_LINE_STATUS_CHOICES)

    EXCHANGE_LINE_STATUS_CHOICES_FOR_A = EXCHANGE_LINE_STATUS_CHOICES

    EXCHANGE_LINE_STATUS_CHOICES_FOR_B = (
        (OPEN, "待审核"),
        (PENDING_RETURN, "待客人寄回"),
        (PENDING_CONFIRM, "待专柜确收"),
        (PENDING_EXCHANGE, "待寄出换货"),
        (CUSSERVICE_RECEIVED, "客服收到寄回商品"),
        (AFTERSALE_WH, "客服已收退货"),
        (DONE, "换货完成"),
        (CLOSED, "已关闭"),
    )

    EXCHANGE_LINE_STATUS_CHOICES_FOR_P = EXCHANGE_LINE_STATUS_CHOICES


class EventMapKey(object):

    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class ExchangeEventConst(object):
    '''
    ### 事件 ###
    '''
    # 创建换货单
    NEW_ADD = "new_add"
    # 导购同意客户换货
    APPROVE = "approve"
    # 取消换货
    CANCEL = "cancel"
    # 客人自提
    CUS_SELF_SERVICE = "cus_self_service"
    # 客户回填运单信息
    CUS_WRITE_BACK = "cus_write_back"
    # 确收
    CONFIRM = "confirm"
    # 导购发货
    GUIDE_EXPRESS = "guide_express"
    # 留言
    COMMENT = "comment"
    # 打印
    PRINT = "print"
    # 修改换货地址
    MODIFY_ADDRESS = "modify_address"
    # 修改客户回填运单号
    MODIFY_CUS_SHIPPING_NUMBER = "modify_cus_shipping_number"
    # 催导购确收
    PUSH_GUIDE_CONFIRM = "push_guide_confirm"
    # 催导购审核
    PUSH_GUIDE_APPROVE = "push_guide_approve"
    # 催导购寄出
    PUSH_GUIDE_EXPRESS = "push_guide_express"
    # 客服收货
    CUSSERVICE_RECEIVE = "cusservice_receive"
    # 取消客服收货
    CANCEL_CUSSERVICE_RECEIVE = "cancel_cusservice_receive"
    # 售后仓入库、上架
    ENTER_AFTERSALE_WH = "enter_aftersale_wh"

    EVENT_2_BUTTONNAME_MAP = {
        NEW_ADD: "创建换货单",
        APPROVE: "通过",
        CANCEL: "关闭",
        CUS_SELF_SERVICE: "现换",
        CUS_WRITE_BACK: "客户回填运单信息",
        CONFIRM: "收换货",
        GUIDE_EXPRESS: "寄换货",
        COMMENT: "备注",
        PRINT: "打印",
        MODIFY_ADDRESS: "修改换货地址",
        MODIFY_CUS_SHIPPING_NUMBER: "修改客户回填运单号",
        PUSH_GUIDE_CONFIRM: "催确收",
        PUSH_GUIDE_APPROVE: "催审核",
        PUSH_GUIDE_EXPRESS: "催寄出",
        CUSSERVICE_RECEIVE: "客服收货",
        CANCEL_CUSSERVICE_RECEIVE: "取消客服收货",
        ENTER_AFTERSALE_WH: "售后仓入库",
    }

    EVENT_2_CNAME_MAP = {
        CUS_SELF_SERVICE: "客人现场换货",
        APPROVE: "通过审核",
        CANCEL: "关闭换货",
    }

    # 注意：
    # 1、当不存在EventMapKey.USER_ROLES_KEY的key时，说明所有角色都可以操作；
    # 2、当EventMapKey.TO_STATUS_KEY对应的value设置为None时，则说明动作不会造成状态变更；
    FROM_TO_MAP = {
        NEW_ADD: {  # 创建换货单
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSTOMER, UserRole.CUSSERVICE]
            }
        },
        APPROVE: {  # 导购同意客户换货
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.PENDING_RETURN,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            }
        },
        CANCEL: {  # 取消换货
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
        },
        CUS_SELF_SERVICE: {  # 客人自提
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.DONE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.DONE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.DONE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.DONE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
        },
        CUS_WRITE_BACK: {  # 客户回填运单信息
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.PENDING_CONFIRM,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSTOMER]
            },
        },
        CONFIRM: {  # 确收
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.PENDING_EXCHANGE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.PENDING_EXCHANGE,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
        },
        GUIDE_EXPRESS: {  # 导购发货
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.DONE,
                EventMapKey.USER_ROLES_KEY: [UserRole.GUIDE]
            },
        },
        PRINT: {  # 打印
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.DONE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
        },
        COMMENT: {
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.DONE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.GUIDE, UserRole.CUSSERVICE]
            },
        },
        MODIFY_ADDRESS: {
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        MODIFY_CUS_SHIPPING_NUMBER: {
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.CUSTOMER]
            },
        },
        PUSH_GUIDE_CONFIRM: {
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        PUSH_GUIDE_APPROVE: {
            ExchangeLineStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            },
        },
        PUSH_GUIDE_EXPRESS: {
            ExchangeLineStatus.PENDING_EXCHANGE: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            }
        },
        CUSSERVICE_RECEIVE: {
            ExchangeLineStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CUSSERVICE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            },
            ExchangeLineStatus.PENDING_CONFIRM: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.CUSSERVICE_RECEIVED,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            },
        },
        CANCEL_CUSSERVICE_RECEIVE: {
            ExchangeLineStatus.CUSSERVICE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.PENDING_CONFIRM,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            },
        },
        ENTER_AFTERSALE_WH: {
            ExchangeLineStatus.CUSSERVICE_RECEIVED: {
                EventMapKey.TO_STATUS_KEY: ExchangeLineStatus.AFTERSALE_WH,
                EventMapKey.USER_ROLES_KEY: [
                    UserRole.CUSSERVICE, UserRole.AUTO]
            },
        },
    }

    # 按钮排序
    EVENT_CONST_SORT_MAP = {
        CANCEL: 0,
        COMMENT: 1,
        APPROVE: 2,
        CONFIRM: 2,
        GUIDE_EXPRESS: 2,
        PRINT: 3,
        CUS_SELF_SERVICE: 4,
    }


def get_available_event_list(exline_status, user_role):
    '''
    根据换货分单的状态和用户角色，获取可进行的操作事件列表
    '''
    available_event_list = []
    if not exline_status or not user_role:
        return available_event_list
    # special_event_list 记录了不需要展示按钮的事件
    special_event_list = []
    from_to_map = ExchangeEventConst.FROM_TO_MAP
    for event_code, event_dict in from_to_map.items():
        if event_code in special_event_list:
            continue

        if exline_status not in event_dict:
            continue
        to_status_dict = event_dict.get(exline_status)
        to_status_user_role_list = to_status_dict.get(
            EventMapKey.USER_ROLES_KEY, None)

        event_str = event_code + "|" + \
            ExchangeEventConst.EVENT_2_BUTTONNAME_MAP.get(event_code)

        # 当不存在EventMapKey.USER_ROLES_KEY的key时，说明所有角色都可以操作；
        if not to_status_user_role_list:
            available_event_list.append(event_str)
        else:
            if user_role in to_status_user_role_list:
                available_event_list.append(event_str)
    available_event_list.sort(
        key=lambda event_str: ExchangeEventConst.EVENT_CONST_SORT_MAP.get(event_str.split("|")[0], 0))
    return available_event_list


EXCHANGE_USER_REASON = [
    "无理由换货",
    "尺码/颜色不合适",
    "质量问题",
    "其他"
]


class ExchangeReturnShippingMethod:
    ''' 换货后客户取货方式 '''
    SELF_SERVICE = "self_service"
    EXPRESS = "express"
