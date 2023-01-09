import logging

from ..core.constants import MemberLevel
from enum import Enum, unique

logger = logging.getLogger(__name__)


DISTRIBUTE_ERROR_CODE_PREFIX = 246000
BASE_DISTRIBUTE_API_CODE = 20103000


class DistributeStatusOwner(object):
    GUIDE = 'guide'
    CUSSERVICE = 'cusservice'
    CUSTOMER = 'customer'
    OUTSTORAGE = 'outstorage'
    # 汉光贩售机
    HGVENDING = 'hgvending'
    # 海淘
    HAITAO = 'haitao'


class DistributeDirection(object):
    GUIDE = 'guide'
    CUSSERVICE = 'cusservice'
    OUTSTORAGE = 'outstorage'
    # 汉光贩售机
    HGVENDING = 'hgvending'
    # 海淘
    HAITAO = 'haitao'


class DistributeStatus(object):
    # 初始态
    INIT = "init"
    # 已打印
    PRINTED = "printed"
    # 客服已提
    CUSSERVICE_PICKED_UP = "cusservice_picked_up"
    # 导购已提
    GUIDE_PICKED_UP = "guide_picked_up"
    # 十层前台
    SERVICE_DESK = "service_desk"
    # 十层仓库
    SERVICE_STORE = "service_store"
    # 已打包发货
    PACKAGED = "packaged"
    # 客服已退
    CUSSERVICE_HOLD = "cusservice_hold"
    # #客户已确收
    CUS_CONFIRM = "cus_confirm"

    # 导购端-客户已确收
    CUS_CONFIRM_AT_GUIDE = "cus_confirm_at_guide"

    # 客服端-客户已确收
    CUS_CONFIRM_AT_CUSSERVICE = "cus_confirm_at_cusservice"

    # 拆单
    SPLIT = "split"
    # 未提已退
    NO_PICKUP_RETURN = "no_pickup_return"
    # 外仓待发货
    OUTSTORAGE_WAIT_PACKAGE = "outstorage_wait_package"
    # 外仓已发货
    OUTSTORAGE_PACKAGED = "outstorage_packaged"
    # 外仓已退
    OUTSTORAGE_RETURN = "outstorage_return"

    # 贩售机初始态
    HGVENDING_INIT = "hgvending_init"
    # 贩售机待提
    HGVENDING_WAIT_PICKUP = "hgvending_wait_pickup"
    # 贩售机客户已自提
    CUS_CONFIRM_AT_HGVENDING = "cus_confirm_at_hgvending"
    # 贩卖机已退
    HGVENDING_NO_PICKUP_RETURN = "hgvending_no_pickup_return"

    # 定金已支付, 由分阶段支付的订单产生
    DEPOSITPAY = "depositpay"
    # 尾款超时
    TAILPAY_OVERTIME = "tailpay_overtime"
    # 定金已退
    DEPOSITPAY_RETURN = "depositpay_return"
    # 海淘初始态
    HAITAO_INIT = "haitao_init"
    # 海淘已推百世快递
    HAITAO_BAISHI = "haitao_baishi"
    # 海淘已退
    HAITAO_RETURN = "haitao_return"
    # 海淘已发货
    HAITAO_PACKAGED = "haitao_packaged"

    # 滞留仓
    SERVICE_STOP = "service_stop"

    # 2022.08 虚拟商品
    # 虚拟商品INIT
    VIRTUAL_INIT = "virtual_init"
    # 虚拟已确收
    CUS_CONFIRM_AT_VIRTUAL = "cus_confirm_at_virtual"

    # 2022.09 特需售后单自提转快递支付运费订单的发货单
    MAKEUP_POSTAGE_PAID = "paid"

    NO_SPLIT_STATUS_LIST = [
        INIT,
        HGVENDING_INIT,
        VIRTUAL_INIT,
        PRINTED,
        CUSSERVICE_PICKED_UP,
        GUIDE_PICKED_UP,
        HGVENDING_WAIT_PICKUP,
        CUS_CONFIRM,
        CUS_CONFIRM_AT_GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE,
        CUS_CONFIRM_AT_VIRTUAL,
        CUS_CONFIRM_AT_HGVENDING,
        PACKAGED,
        SERVICE_DESK,
        SERVICE_STORE,
        CUSSERVICE_HOLD,
        NO_PICKUP_RETURN,
        HGVENDING_NO_PICKUP_RETURN,
        OUTSTORAGE_WAIT_PACKAGE,
        OUTSTORAGE_PACKAGED,
        OUTSTORAGE_RETURN,
        DEPOSITPAY,
        TAILPAY_OVERTIME,
        DEPOSITPAY_RETURN,
        HAITAO_INIT,
        HAITAO_BAISHI,
        HAITAO_PACKAGED,
        HAITAO_RETURN,
        SERVICE_STOP,
        MAKEUP_POSTAGE_PAID,
    ]
    

    # 可以被售后集合
    CAN_AFTERSALE_STATUS_LIST = [
        INIT,
        PRINTED,
        CUSSERVICE_PICKED_UP,
        GUIDE_PICKED_UP,
        CUS_CONFIRM,
        CUS_CONFIRM_AT_GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE,
        CUS_CONFIRM_AT_VIRTUAL,
        PACKAGED,
        SERVICE_DESK,
        SERVICE_STORE,
        OUTSTORAGE_WAIT_PACKAGE,
        OUTSTORAGE_PACKAGED,
        SERVICE_STOP,
        MAKEUP_POSTAGE_PAID,
    ]

    ## 初始态集合
    INIT_STATUS_LIST = [
        INIT,
        HGVENDING_INIT,
        VIRTUAL_INIT,
        PRINTED,
        OUTSTORAGE_WAIT_PACKAGE,
    ]
    ## 可以整单退的发货单状态集合
    ENTIRE_AFTERSALE_STATUS_LIST = [
        INIT,
        HGVENDING_INIT,
        PRINTED,
        GUIDE_PICKED_UP,
        SPLIT,
        HGVENDING_WAIT_PICKUP,
        # 补缴运费的商品可以整单退
        MAKEUP_POSTAGE_PAID,
    ]

    BEFORE_cuservice_pick_up = [
        INIT,
        PRINTED,
        NO_PICKUP_RETURN,
        SPLIT,
        CUSSERVICE_HOLD,
        TAILPAY_OVERTIME,
        DEPOSITPAY_RETURN,
    ]

    CAN_SPLIT_STATUS_LIST = [
        INIT,
        PRINTED,
        CUSSERVICE_PICKED_UP,
        GUIDE_PICKED_UP,
        SERVICE_DESK,
        SERVICE_STORE,
        SERVICE_STOP,
    ]
    # For C端显示
    DISTRIBUTE_SHOW_FOR_C = {
        INIT: '备货中',
        HGVENDING_INIT: '备货中',
        PRINTED: "备货中",
        CUSSERVICE_PICKED_UP: "已出库",
        GUIDE_PICKED_UP: "可专柜自提",
        SERVICE_DESK: "可自提",
        SERVICE_STORE: "待发货",
        PACKAGED: "已邮寄",
        OUTSTORAGE_WAIT_PACKAGE: "待发货",
        OUTSTORAGE_PACKAGED: "已邮寄",
        OUTSTORAGE_RETURN: "售后",
        CUSSERVICE_HOLD: "售后",
        CUS_CONFIRM: "已提货",
        CUS_CONFIRM_AT_GUIDE: "已提货",
        CUS_CONFIRM_AT_CUSSERVICE: "已提货",
        CUS_CONFIRM_AT_VIRTUAL: "已完成",  # 2022.8.23 琪琪说改成已完成，目前前端根据这个字段，展示下面的文字描述
        SPLIT: "已拆单",
        NO_PICKUP_RETURN: "售后",
        HGVENDING_WAIT_PICKUP: "待提",
        CUS_CONFIRM_AT_HGVENDING: "已提货",
        HGVENDING_NO_PICKUP_RETURN: "已退",
        DEPOSITPAY: "待支付尾款",
        DEPOSITPAY_RETURN: "定金已退",
        TAILPAY_OVERTIME: "尾款超时",
        HAITAO_INIT: "备货中",
        HAITAO_BAISHI: "备货中",
        HAITAO_PACKAGED: "已发货",
        HAITAO_RETURN: "售后",
        SERVICE_STOP: "待发货",
        MAKEUP_POSTAGE_PAID: "运费已支付",
    }
    # For B端 查询
    DISTRIBUTE_STATUS_CHOICES_FOR_B_QUERY = {
        INIT: '未打印',
        HGVENDING_INIT: '贩售机初始态',
        PRINTED: "已打印",
        CUSSERVICE_PICKED_UP: "客服已提",
        GUIDE_PICKED_UP: "可专柜自提",
        SERVICE_DESK: "自提点已收",
        SERVICE_STORE: "仓库已收",
        PACKAGED: "已邮寄",
        OUTSTORAGE_WAIT_PACKAGE: "外仓待发货",
        OUTSTORAGE_PACKAGED: "外仓已邮寄",
        CUSSERVICE_HOLD: "客服已退",
        CUS_CONFIRM: "已自提",
        CUS_CONFIRM_AT_GUIDE: "导购端已自提",
        CUS_CONFIRM_AT_CUSSERVICE: "客服端已自提",
        CUS_CONFIRM_AT_VIRTUAL: "虚拟商品已提货",
        # SPLIT: "拆单",
        NO_PICKUP_RETURN: "未提已退",
        OUTSTORAGE_RETURN: "外仓已退",
        HGVENDING_WAIT_PICKUP: "贩售机待提",
        CUS_CONFIRM_AT_HGVENDING: "贩售机端已提货",
        HGVENDING_NO_PICKUP_RETURN: "贩售机已退",
        DEPOSITPAY: "定金已付",
        DEPOSITPAY_RETURN: "定金已退",
        TAILPAY_OVERTIME: "尾款超时",
        HAITAO_INIT: "海淘备货中",
        HAITAO_BAISHI: "海淘已推百世",
        HAITAO_PACKAGED: "海淘已发货",
        HAITAO_RETURN: "海淘已退",
        SERVICE_STOP: "滞留仓已收",
        MAKEUP_POSTAGE_PAID: "运费已支付",
    }

    DISTRIBUTE_MESSAGE_DICT_FOR_C = {
        INIT: "专柜已收到您的订单，正在为您备货。",
        SERVICE_STORE: "商品已从专柜提货，正在为您准备邮寄。",
        SERVICE_DESK: "商品已备好，您可至【汉光百货顾客服务中心（一层北客梯旁）】领取。",
        CUSSERVICE_PICKED_UP: "商品已经出库。",
        GUIDE_PICKED_UP: "商品已备好，请至【汉光百货shop_location_desc shop_name专柜】领取。",
        PACKAGED: "已交付express_name快递，运单号为shipping_number。",
        OUTSTORAGE_WAIT_PACKAGE: "待外仓发货。",
        OUTSTORAGE_PACKAGED: "已交付express_name快递，运单号为shipping_number。",
        CUS_CONFIRM: "商品已提走，期待您下次光临。",
        CUS_CONFIRM_AT_GUIDE: "商品已提走，期待您下次光临。",
        CUS_CONFIRM_AT_CUSSERVICE: "商品已提走，期待您下次光临。",
        CUS_CONFIRM_AT_VIRTUAL: "虚拟商品已提货，期待您下次光临。",
        CUSSERVICE_HOLD: "商品已售后。",
        NO_PICKUP_RETURN: "商品已售后。",
        OUTSTORAGE_RETURN: "外仓已售后。",
        HGVENDING_NO_PICKUP_RETURN: "订单超时30分钟自动退单，如有需要请再扫码下单。",
        DEPOSITPAY: "定金已支付。",
        DEPOSITPAY_RETURN: "您的商品已退还定金",
        TAILPAY_OVERTIME: "未按时支付尾款，您的订单已关闭",
        HAITAO_INIT: "海淘备货中。",
        HAITAO_BAISHI: "海淘备货中。",
        HAITAO_PACKAGED: "海淘已发货。",
        HAITAO_RETURN: "海淘已售后。",
        SERVICE_STOP: "暂时无法发货，商品滞留。",
        MAKEUP_POSTAGE_PAID: "订单自提转快递运费已支付。",
    }

    DISTRIBUTE_STATUS_CHOICES = (
        (INIT, '未打印'),
        (HGVENDING_INIT, '贩售机初始态'),
        (PRINTED, "已打印"),
        (CUSSERVICE_PICKED_UP, "客服已提"),
        (GUIDE_PICKED_UP, "可专柜自提"),
        (SERVICE_DESK, "前台已收"),
        (SERVICE_STORE, "仓库已收"),
        (PACKAGED, "已邮寄"),
        (OUTSTORAGE_WAIT_PACKAGE, "外仓待发货"),
        (OUTSTORAGE_PACKAGED, "外仓已邮寄"),
        (CUSSERVICE_HOLD, "客服已退"),
        (CUS_CONFIRM, "已自提"),
        (CUS_CONFIRM_AT_GUIDE, "导购端已自提"),
        (CUS_CONFIRM_AT_CUSSERVICE, "客服端已自提"),
        (SPLIT, "已拆单"),
        (NO_PICKUP_RETURN, "未提已退"),
        (OUTSTORAGE_RETURN, "外仓已退"),
        (HGVENDING_WAIT_PICKUP, "贩售机待提"),
        (CUS_CONFIRM_AT_HGVENDING, "贩售机端已提货"),
        (HGVENDING_NO_PICKUP_RETURN, "贩售机端已退"),
        (DEPOSITPAY, "定金已付"),
        (DEPOSITPAY_RETURN, "定金已退"),
        (TAILPAY_OVERTIME, "尾款超时"),
        (HAITAO_INIT, "海淘备货中"),
        (HAITAO_BAISHI, "海淘已推百世"),
        (HAITAO_PACKAGED, "海淘已发货"),
        (HAITAO_RETURN, "海淘已退"),
        (SERVICE_STOP, "滞留仓已收"),
        (VIRTUAL_INIT, "虚拟商品初始态"),
        (CUS_CONFIRM_AT_VIRTUAL, "虚拟商品已提货"),
        (MAKEUP_POSTAGE_PAID, "运费已支付"),
    )

    DISTRIBUTE_STATUS_OWNER_DICT = {
        INIT: DistributeStatusOwner.GUIDE,
        VIRTUAL_INIT: DistributeStatusOwner.CUSTOMER,
        HGVENDING_INIT: DistributeStatusOwner.HGVENDING,
        PRINTED: DistributeStatusOwner.GUIDE,
        GUIDE_PICKED_UP: DistributeStatusOwner.GUIDE,
        NO_PICKUP_RETURN: DistributeStatusOwner.GUIDE,
        CUSSERVICE_PICKED_UP: DistributeStatusOwner.CUSSERVICE,
        HGVENDING_WAIT_PICKUP: DistributeStatusOwner.HGVENDING,
        SERVICE_DESK: DistributeStatusOwner.CUSSERVICE,
        SERVICE_STORE: DistributeStatusOwner.CUSSERVICE,
        CUSSERVICE_HOLD: DistributeStatusOwner.CUSSERVICE,
        CUS_CONFIRM: DistributeStatusOwner.CUSTOMER,
        CUS_CONFIRM_AT_GUIDE: DistributeStatusOwner.CUSTOMER,
        CUS_CONFIRM_AT_CUSSERVICE: DistributeStatusOwner.CUSTOMER,
        CUS_CONFIRM_AT_VIRTUAL: DistributeStatusOwner.CUSTOMER,
        CUS_CONFIRM_AT_HGVENDING: DistributeStatusOwner.CUSTOMER,
        PACKAGED: DistributeStatusOwner.CUSTOMER,
        OUTSTORAGE_WAIT_PACKAGE: DistributeStatusOwner.OUTSTORAGE,  # 外仓
        OUTSTORAGE_PACKAGED: DistributeStatusOwner.CUSTOMER,
        OUTSTORAGE_RETURN: DistributeStatusOwner.OUTSTORAGE,  # 外仓
        HGVENDING_NO_PICKUP_RETURN: DistributeStatusOwner.HGVENDING,
        DEPOSITPAY: DistributeStatusOwner.GUIDE,
        DEPOSITPAY_RETURN: DistributeStatusOwner.GUIDE,
        TAILPAY_OVERTIME: DistributeStatusOwner.GUIDE,
        HAITAO_INIT: DistributeStatusOwner.HAITAO,
        HAITAO_BAISHI: DistributeStatusOwner.HAITAO,
        HAITAO_PACKAGED: DistributeStatusOwner.HAITAO,
        HAITAO_RETURN: DistributeStatusOwner.HAITAO,
        SERVICE_STOP: DistributeStatusOwner.CUSSERVICE,
        MAKEUP_POSTAGE_PAID: DistributeStatusOwner.CUSTOMER,
    }

    DISTRIBUTE_STATUS_DIRECTION_DICT = {
        INIT: DistributeDirection.GUIDE,
        HGVENDING_INIT: DistributeDirection.HGVENDING,
        PRINTED: DistributeDirection.GUIDE,
        GUIDE_PICKED_UP: DistributeDirection.GUIDE,
        NO_PICKUP_RETURN: DistributeDirection.GUIDE,
        CUSSERVICE_PICKED_UP: DistributeDirection.CUSSERVICE,
        SERVICE_DESK: DistributeDirection.CUSSERVICE,
        SERVICE_STORE: DistributeDirection.CUSSERVICE,
        CUSSERVICE_HOLD: DistributeDirection.CUSSERVICE,
        CUS_CONFIRM: DistributeDirection.CUSSERVICE,
        CUS_CONFIRM_AT_GUIDE: DistributeDirection.GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE: DistributeDirection.CUSSERVICE,
        CUS_CONFIRM_AT_HGVENDING: DistributeDirection.HGVENDING,
        PACKAGED: DistributeDirection.CUSSERVICE,
        OUTSTORAGE_WAIT_PACKAGE: DistributeDirection.OUTSTORAGE,  # 外仓
        OUTSTORAGE_PACKAGED: DistributeDirection.OUTSTORAGE,
        OUTSTORAGE_RETURN: DistributeDirection.OUTSTORAGE,  # 外仓
        HGVENDING_WAIT_PICKUP: DistributeDirection.HGVENDING,  # 汉光贩售机
        HGVENDING_NO_PICKUP_RETURN: DistributeDirection.HGVENDING,
        DEPOSITPAY: DistributeDirection.GUIDE,
        DEPOSITPAY_RETURN: DistributeDirection.GUIDE,
        TAILPAY_OVERTIME: DistributeDirection.GUIDE,

        HAITAO_INIT: DistributeDirection.HAITAO,
        HAITAO_BAISHI: DistributeDirection.HAITAO,
        HAITAO_PACKAGED: DistributeDirection.HAITAO,
        HAITAO_RETURN: DistributeDirection.HAITAO,
        SERVICE_STOP: DistributeDirection.CUSSERVICE,

        MAKEUP_POSTAGE_PAID: DistributeDirection.CUSSERVICE,
    }

    # 终结状态列表
    TERMINATE_STATUS_LIST = [
        PACKAGED,
        CUSSERVICE_HOLD,
        CUS_CONFIRM,
        CUS_CONFIRM_AT_GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE,
        CUS_CONFIRM_AT_VIRTUAL,
        CUS_CONFIRM_AT_HGVENDING,
        SPLIT,
        NO_PICKUP_RETURN,
        HGVENDING_NO_PICKUP_RETURN,
        # 外仓
        OUTSTORAGE_PACKAGED,
        OUTSTORAGE_RETURN,
        # 分阶段支付
        DEPOSITPAY_RETURN,
        TAILPAY_OVERTIME,
        # 海淘
        HAITAO_PACKAGED,
        HAITAO_RETURN,
        MAKEUP_POSTAGE_PAID,
    ]

    # 非最终状态
    UN_TERMINATE_STATUS_LIST = [
        SERVICE_DESK,
        SERVICE_STORE,
        PRINTED,
        INIT,
        GUIDE_PICKED_UP,
        CUSSERVICE_PICKED_UP,
        SERVICE_STOP,
    ]

    # 由售后产生的终结发货单状态列表(含SPLIT)
    AFTERSALE_TERMINATE_STATUS_LIST = [
        CUSSERVICE_HOLD,
        SPLIT,
        NO_PICKUP_RETURN,
        HGVENDING_NO_PICKUP_RETURN,
        OUTSTORAGE_RETURN,
        DEPOSITPAY_RETURN,
        HAITAO_RETURN,
    ]

    # 可换货发货单状态
    EXCHANGE_TERMINATE_STATUS_LIST = [
        PACKAGED,
        CUS_CONFIRM,
        CUS_CONFIRM_AT_GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE,
        OUTSTORAGE_PACKAGED,
    ]

    # 未售后的不支持修改配送方式的发货单状态
    CAN_NOT_MODY_SHIPPING_METHOD_DISTRIBUTE_STATUS_LIST = [
        CUS_CONFIRM_AT_GUIDE,
        CUS_CONFIRM_AT_CUSSERVICE,
        PACKAGED,
        OUTSTORAGE_PACKAGED,
        OUTSTORAGE_WAIT_PACKAGE,
        SPLIT,
    ]


class __ShippingMethod(object):
    # 普通快递
    EXPRESS = 'express'
    # 自提
    SELF_SERVICE = 'self_service'
    # 闪送
    FLASH_DELIVERY = 'flash_delivery'

    CHOICES = (
        (EXPRESS, "快递发货"),
        (SELF_SERVICE, "到店自提"),
        (FLASH_DELIVERY, "闪送"),
    )

    def __getattribute__(self, name: str):
        value = super().__getattribute__(name)
        logger.warning("sparrow_distribute.constants.ShippingMethod 已废弃, 请使用 sparrow_order_lib.core.constants.ShippingMethod 替换")
        return value


ShippingMethod = __ShippingMethod()


class DistributeEventConstKey(object):
    FROM_STATUS_LIST_KEY = "from_status_list"
    TO_STATUS_KEY = "to_status"
    TO_STATE_MAP_KEY = "to_state_map"


class MessageLevel(object):
    FOR_CUSTOMER = 1
    FOR_CUSSERVICE = 2
    FOR_DEV = 3


class DistributeSyncType(object):
    MEMBER = "MEMBER"
    VISITOR = "VISITOR"


# 发货单操作事件名称常量
class DistributeEventConst(object):
    NEW_ADD = "new_add"
    PRINT = "print"
    GUIDE_PRINT = "guide_print"
    PRINT_AND_OVERWRITE_EXPRESS = "print_and_overwrite_express"
    CANCEL_PRINT = "cancel_print"
    CUSSERVICE_PICK_UP = "cusservice_pick_up"

    CUSSERVICE_PICK_UP_BY_DEVICEC_ONLY_FOR_LOG = "cusservice_pick_up_by_device_only_for_log"

    GUIDE_PICK_UP = "guide_pick_up"
    SERVICESTORE_PICK_UP = "servicestore_pick_up"
    SERVICEDESK_PICK_UP = "servicedesk_pick_up"

    PACKAGE = "package"
    PACKAGE_BY_DEVICEC_ONLY_FOR_LOG = "package_by_device_only_for_log"
    CANCEL_PACKAGE = "cancel_package"
    SERVICESTOP_CANCEL_PACKAGE = "service_stop_cancel_package"

    CUS_CONFIRM = "cus_confirm"
    CUS_CONFIRM_AT_GUIDE = "cus_confirm_at_guide"
    CUS_CONFIRM_AT_CUSSERVICE = "cus_confirm_at_cusservice"

    TO_WAIT_OUTSTORAGE_PACKAGE = "to_wait_outstorage_package"
    CANCEL_WAIT_OUTSTORAGE_PACKAGE = "cancel_wait_outstorage_package"
    OUTSTORAGE_PACKAGE = "outstorage_package"
    CANCEL_OUTSTORAGE_PACKAGE = "cancel_outstorage_package"

    OPEN_AFTERSALE = "open_aftersale"
    CLOSE_AFTERSALE = "close_aftersale"
    COMPLETE_AFTERSALE = "complete_aftersale"
    CREATE_EXPRESS = "create_express"
    CANCEL_EXPRESS = "cancel_express"
    MODIFY_SHIPPING_NUMBER = "modfiy_shipping_number"
    MERGE_EXPRESS = "merge_express"
    MERGE_EXPRESS_MAIN = "merge_express_main"
    # 客服退还货物给专柜事件
    CUSSERVICE_RETURN = "cusservice_return"
    OUTSTORAGE_RETURN = "outstorage_return"
    ADD_SHIPPING_ADDRESS = "add_shipping_address"
    UPDATE_SHIPPING_METHOD = "update_shipping_method"
    UPDATE_SHIPPING_METHOD_FOR_MERGE = "update_shipping_method_for_merge"
    ADD_GUIDE_NOTE = "add_guide_note"
    BLOCK_SUCC = "block_succ"
    BLOCK_FAILED = "block_failed"
    MODIFY_SHIPPING_NUMBER_FAILED = "modify_shipping_number_failed"

    # 货架管理 出库/入库/更改货位/合并货位
    STORAGE_IN = "storage_in"
    STORAGE_OUT = "storage_out"
    STORAGE_SEAT_CHANGE = "storage_seat_change"
    STORAGE_SEAT_MERGE = "storage_seat_merge"

    # 换货
    EXCHANGE_OPEN = "exchange_open"
    EXCHANGE_CANCEL = "exchange_cancel"
    EXCHANGE_DONE = "exchange_done"
    # 汉光贩卖机提货
    HGVENDING_PICKED_UP = "hgvending_pick_up"
    # 汉光贩卖机-客户自提
    CUS_CONFIRM_AT_HGVENDING = "cus_confirm_at_hgvending"

    # 海淘打包
    HAITAO_PACKAGE = "haitao_package"

    # 海淘推数据给百世
    HAITAO_PUSHDATA_2_BAISHI = "haitao_pushdata_2_baishi"
    # 海淘取消推百世数据
    HAITAO_CANCEL_FROM_BAISHI = "haitao_cancel_from_baishi"
    # 报错日志
    ERROR_MESSAGE = "error_message"
    # 普通日志
    NORMAL_MESSAGE = "normal_message"

    # 付尾款
    PAY_TAIL = "pay_tail"
    # 退定金
    RETURN_DEPOSIT = "return_deposit"
    # 尾款超时
    OVERTIME_TAILPAY = "overtime_tailpay"
    # 更新发货时间
    UPDATE_DELIVER_TIME = "update_deliver_time"
    # 合单催配送提醒
    PUSH_GUIDE_ASSIGN = "push_guide_assign"

    # 2022.08 特殊售后单需求
    AFSPLUS_OPEN = "afsplus_open"
    AFSPLUS_CLOSE = "afsplus_close"
    AFSPLUS_COMPLETE = "afsplus_complete"
    AFSPLUS_S2E = "afsplus_s2e"  # 自提转快递
    AFSPLUS_E2S = "afsplus_e2s"  # 快递转自提
    AFSPLUS_TO_EXPRESS = "afsplus_2e"  # 转快递
    AFSPLUS_TO_SELF_SERVICE = "afsplus_2s"

    # 2022.08 虚拟商品确收
    CUS_CONFIRM_AT_VIRTUAL = "cus_confirm_at_virtual"
    
    CLOUDPRINT_SHIPPING_NUMBER = "cloudprint_shipping_number"

    FROM_TO_MAP = {
        PRINT: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.INIT, DistributeStatus.PRINTED,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.SERVICE_STORE, DistributeStatus.SERVICE_DESK,
                DistributeStatus.PACKAGED, DistributeStatus.CUSSERVICE_HOLD,
                DistributeStatus.CUS_CONFIRM,
                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                DistributeStatus.OUTSTORAGE_PACKAGED, DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
                DistributeStatus.SERVICE_STOP,
                ],
            DistributeEventConstKey.TO_STATE_MAP_KEY: {
                    DistributeStatus.INIT: DistributeStatus.PRINTED,
                    },
        },
        GUIDE_PRINT: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.INIT, DistributeStatus.PRINTED,
                DistributeStatus.GUIDE_PICKED_UP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.SPLIT
        },
        PRINT_AND_OVERWRITE_EXPRESS: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.INIT, DistributeStatus.PRINTED,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.SERVICE_STORE, DistributeStatus.SERVICE_DESK,
                DistributeStatus.CUSSERVICE_HOLD,
                DistributeStatus.CUS_CONFIRM,
                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                DistributeStatus.SERVICE_STOP,
                DistributeStatus.PACKAGED,
                ],
            DistributeEventConstKey.TO_STATE_MAP_KEY: {
                    DistributeStatus.INIT: DistributeStatus.PRINTED,
                    },
        },
        CANCEL_PRINT: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.PRINTED],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.INIT,
        },
        CUSSERVICE_PICK_UP: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.SERVICE_DESK, DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUSSERVICE_PICKED_UP,
        },
        GUIDE_PICK_UP: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.INIT, DistributeStatus.PRINTED],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.GUIDE_PICKED_UP,
        },
        HGVENDING_PICKED_UP: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.HGVENDING_INIT],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.HGVENDING_WAIT_PICKUP,
        },
        SERVICESTORE_PICK_UP: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, 
                DistributeStatus.PRINTED,
                DistributeStatus.CUSSERVICE_PICKED_UP, 
                DistributeStatus.SERVICE_DESK,
                DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.SERVICE_STORE,
        },
        SERVICEDESK_PICK_UP: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                DistributeStatus.CUSSERVICE_PICKED_UP, DistributeStatus.SERVICE_STORE, DistributeStatus.GUIDE_PICKED_UP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.SERVICE_DESK,
        },
        PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                    DistributeStatus.INIT, DistributeStatus.PRINTED,
                    DistributeStatus.CUSSERVICE_PICKED_UP,
                    DistributeStatus.SERVICE_DESK,
                    DistributeStatus.SERVICE_STORE,
                    DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.PACKAGED,
        },
        CANCEL_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.PACKAGED
                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        SERVICESTOP_CANCEL_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.PACKAGED,
                DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.SERVICE_STORE],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.SERVICE_STOP,
        },
        CUS_CONFIRM_AT_GUIDE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.SERVICE_DESK],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUS_CONFIRM_AT_GUIDE,
        },
        CUS_CONFIRM_AT_CUSSERVICE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.SERVICE_DESK],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
        },
        CUS_CONFIRM_AT_HGVENDING: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.HGVENDING_WAIT_PICKUP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUS_CONFIRM_AT_HGVENDING,
        },

        TO_WAIT_OUTSTORAGE_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
        },
        CANCEL_WAIT_OUTSTORAGE_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [DistributeStatus.OUTSTORAGE_WAIT_PACKAGE],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        OUTSTORAGE_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                # DistributeStatus.INIT,
                # DistributeStatus.PRINTED,
                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.OUTSTORAGE_PACKAGED,
        },
        CANCEL_OUTSTORAGE_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                # DistributeStatus.OUTSTORAGE_PACKAGED
                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },

        OPEN_AFTERSALE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.SERVICE_STORE, DistributeStatus.SERVICE_DESK,
                DistributeStatus.PACKAGED,
                DistributeStatus.CUS_CONFIRM,
                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                DistributeStatus.CUS_CONFIRM_AT_VIRTUAL,
                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
                DistributeStatus.PACKAGED, DistributeStatus.SERVICE_STOP,
                DistributeStatus.OUTSTORAGE_PACKAGED,
                DistributeStatus.HGVENDING_INIT, DistributeStatus.HGVENDING_WAIT_PICKUP, DistributeStatus.CUS_CONFIRM_AT_HGVENDING,
                DistributeStatus.HAITAO_INIT,
                DistributeStatus.DEPOSITPAY,
                DistributeStatus.TAILPAY_OVERTIME,
                DistributeStatus.MAKEUP_POSTAGE_PAID,
            ],

            DistributeEventConstKey.TO_STATE_MAP_KEY: {
                DistributeStatus.INIT: DistributeStatus.SPLIT,
                DistributeStatus.PRINTED: DistributeStatus.SPLIT,
                DistributeStatus.CUSSERVICE_PICKED_UP: DistributeStatus.SPLIT,
                DistributeStatus.GUIDE_PICKED_UP: DistributeStatus.SPLIT,
                DistributeStatus.SERVICE_STORE: DistributeStatus.SPLIT,
                DistributeStatus.SERVICE_DESK: DistributeStatus.SPLIT,
                DistributeStatus.PACKAGED: None,
                DistributeStatus.CUS_CONFIRM: None,
                DistributeStatus.CUS_CONFIRM_AT_GUIDE: None,
                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE: None,
                DistributeStatus.CUS_CONFIRM_AT_VIRTUAL: None,
                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE: DistributeStatus.SPLIT,
                DistributeStatus.PACKAGED: None,
                DistributeStatus.OUTSTORAGE_PACKAGED: None,
                DistributeStatus.HGVENDING_INIT: None,
                DistributeStatus.HGVENDING_WAIT_PICKUP: None,
                DistributeStatus.CUS_CONFIRM_AT_HGVENDING: None,
                DistributeStatus.HAITAO_INIT: None,
                DistributeStatus.DEPOSITPAY: None,
                DistributeStatus.SERVICE_STOP: DistributeStatus.SPLIT,
                # DistributeStatus.HAITAO_INIT: None,
                DistributeStatus.TAILPAY_OVERTIME: None,
                DistributeStatus.MAKEUP_POSTAGE_PAID: None,
            },
        },
        CLOSE_AFTERSALE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.CUSSERVICE_HOLD, DistributeStatus.PACKAGED,
                DistributeStatus.CUS_CONFIRM,
                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                DistributeStatus.CUS_CONFIRM_AT_VIRTUAL,
                DistributeStatus.CUSSERVICE_HOLD, DistributeStatus.PACKAGED, DistributeStatus.OUTSTORAGE_PACKAGED,
                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE, DistributeStatus.OUTSTORAGE_RETURN,
                DistributeStatus.INIT, DistributeStatus.PRINTED, DistributeStatus.CUSSERVICE_PICKED_UP,
                DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.SERVICE_DESK, DistributeStatus.SERVICE_STORE,
                DistributeStatus.HGVENDING_INIT, DistributeStatus.HGVENDING_WAIT_PICKUP,
                DistributeStatus.SERVICE_STOP,
                DistributeStatus.DEPOSITPAY,
                DistributeStatus.TAILPAY_OVERTIME,
                DistributeStatus.MAKEUP_POSTAGE_PAID,
                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        COMPLETE_AFTERSALE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT,
                DistributeStatus.PRINTED,
                DistributeStatus.GUIDE_PICKED_UP,
                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
                DistributeStatus.HGVENDING_INIT,
                DistributeStatus.HGVENDING_WAIT_PICKUP,
                DistributeStatus.CUS_CONFIRM_AT_VIRTUAL,
                DistributeStatus.HAITAO_INIT,
                DistributeStatus.DEPOSITPAY,
                DistributeStatus.TAILPAY_OVERTIME,
                DistributeStatus.MAKEUP_POSTAGE_PAID,
                ],
            DistributeEventConstKey.TO_STATE_MAP_KEY: {
                DistributeStatus.INIT: DistributeStatus.NO_PICKUP_RETURN,
                DistributeStatus.PRINTED: DistributeStatus.NO_PICKUP_RETURN,
                DistributeStatus.GUIDE_PICKED_UP: DistributeStatus.NO_PICKUP_RETURN,
                DistributeStatus.HGVENDING_INIT: DistributeStatus.HGVENDING_NO_PICKUP_RETURN,
                DistributeStatus.HGVENDING_WAIT_PICKUP: DistributeStatus.HGVENDING_NO_PICKUP_RETURN,
                DistributeStatus.HAITAO_INIT: DistributeStatus.HAITAO_RETURN,
                # DistributeStatus.OUTSTORAGE_WAIT_PACKAGE: DistributeStatus.OUTSTORAGE_RETURN
                # DistributeStatus.CUSSERVICE_PICKED_UP:DistributeStatus.CUSSERVICE_HOLD,
                # DistributeStatus.SERVICE_DESK:DistributeStatus.CUSSERVICE_HOLD,
                # DistributeStatus.SERVICE_STORE:DistributeStatus.CUSSERVICE_HOLD,
                DistributeStatus.DEPOSITPAY: DistributeStatus.DEPOSITPAY_RETURN,
                DistributeStatus.TAILPAY_OVERTIME: DistributeStatus.DEPOSITPAY_RETURN,
                DistributeStatus.CUS_CONFIRM_AT_VIRTUAL: None,
                DistributeStatus.MAKEUP_POSTAGE_PAID: None,
            }
        },
        CREATE_EXPRESS: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.INIT,
                                DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.PACKAGED,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        CANCEL_EXPRESS: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.INIT,
                                DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.PACKAGED,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        MODIFY_SHIPPING_NUMBER: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
                                DistributeStatus.OUTSTORAGE_PACKAGED,
                                DistributeStatus.PACKAGED,
                                DistributeStatus.SERVICE_STOP,
                                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        CUSSERVICE_RETURN: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUSSERVICE_HOLD,  # 客服已退
        },
        OUTSTORAGE_RETURN: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.OUTSTORAGE_RETURN,  # 外仓已退
        },
        ADD_GUIDE_NOTE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.PACKAGED,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.OUTSTORAGE_WAIT_PACKAGE,
                                DistributeStatus.OUTSTORAGE_PACKAGED,
                                DistributeStatus.CUS_CONFIRM,
                                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,
        },
        EXCHANGE_OPEN: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [  # 仅支持发货单邮寄或者自提后进行换货申请，外仓不支持换货
                                DistributeStatus.PACKAGED,
                                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                DistributeStatus.OUTSTORAGE_PACKAGED,
                                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,  # 发货单状态不变更
        },
        EXCHANGE_CANCEL: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [  # 仅支持发货单邮寄或者自提后进行换货申请，外仓不支持换货
                                DistributeStatus.PACKAGED,
                                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                DistributeStatus.OUTSTORAGE_PACKAGED,
                                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,  # 发货单状态不变更
        },
        EXCHANGE_DONE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [  # 仅支持发货单邮寄或者自提后进行换货申请，外仓不支持换货
                                DistributeStatus.PACKAGED,
                                DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                DistributeStatus.OUTSTORAGE_PACKAGED,
                                ],
            DistributeEventConstKey.TO_STATUS_KEY: None,  # 发货单状态不变更
        },
        RETURN_DEPOSIT: {  # 分阶段支付--退定金
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.DEPOSITPAY,
                DistributeStatus.TAILPAY_OVERTIME,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.DEPOSITPAY_RETURN
        },
        OVERTIME_TAILPAY: {  # 分阶段支付--尾款超时
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.DEPOSITPAY
            ],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.TAILPAY_OVERTIME
        },
        PAY_TAIL: {  # 分阶段支付--支付尾款
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.DEPOSITPAY
            ],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.INIT
        },
        HAITAO_PACKAGE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.HAITAO_BAISHI],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.HAITAO_PACKAGED
        },
        HAITAO_PUSHDATA_2_BAISHI: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.HAITAO_INIT],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.HAITAO_BAISHI
        },
        HAITAO_CANCEL_FROM_BAISHI: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.HAITAO_BAISHI],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.HAITAO_INIT
        },

        PUSH_GUIDE_ASSIGN: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                                DistributeStatus.PRINTED,
                                DistributeStatus.INIT],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },

        # 2022.08 特殊售后单需求
        AFSPLUS_OPEN: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_CLOSE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_COMPLETE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_S2E: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_E2S: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_TO_EXPRESS: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },
        AFSPLUS_TO_SELF_SERVICE: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.INIT, DistributeStatus.PRINTED,
                                DistributeStatus.CUSSERVICE_PICKED_UP,
                                DistributeStatus.GUIDE_PICKED_UP,
                                DistributeStatus.SERVICE_DESK,
                                DistributeStatus.SERVICE_STORE,
                                DistributeStatus.SERVICE_STOP,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        },

        # 2022.08 虚拟商品确收事件
        CUS_CONFIRM_AT_VIRTUAL: {
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.VIRTUAL_INIT],
            DistributeEventConstKey.TO_STATUS_KEY: DistributeStatus.CUS_CONFIRM_AT_VIRTUAL,
        },
        # 2022.12.16 云打印面单
        CLOUDPRINT_SHIPPING_NUMBER:{
            DistributeEventConstKey.FROM_STATUS_LIST_KEY: [
                DistributeStatus.PACKAGED,
            ],
            DistributeEventConstKey.TO_STATUS_KEY: None
        }

    }

    EVENT_TO_BUTTONNAME_MAP = {
        NEW_ADD: "新增发货单",
        PRINT: '打印',
        GUIDE_PRINT: '导购打单',
        PRINT_AND_OVERWRITE_EXPRESS: '更新运单并打印',
        CANCEL_PRINT: "清除打印",
        CUSSERVICE_PICK_UP: "客服提货",
        CUSSERVICE_PICK_UP_BY_DEVICEC_ONLY_FOR_LOG: "设备提货",
        GUIDE_PICK_UP: "导购提货",
        SERVICESTORE_PICK_UP: "B3仓库收货",
        SERVICEDESK_PICK_UP: "自提点入库",

        PACKAGE: "快递发货",
        CANCEL_PACKAGE: "取消发货",
        PACKAGE_BY_DEVICEC_ONLY_FOR_LOG: "设备发货",
        SERVICESTOP_CANCEL_PACKAGE: "滞留仓入库",

        TO_WAIT_OUTSTORAGE_PACKAGE: "外仓待发货",
        CANCEL_WAIT_OUTSTORAGE_PACKAGE: "取消外仓待发货",
        OUTSTORAGE_PACKAGE: "外仓发货",
        CANCEL_OUTSTORAGE_PACKAGE: "取消外仓发货",

        CUS_CONFIRM: "客人自提",
        CUS_CONFIRM_AT_GUIDE: "导购端客人自提",
        CUS_CONFIRM_AT_CUSSERVICE: "客服端客人自提",

        OPEN_AFTERSALE: "新建退款单",
        CLOSE_AFTERSALE: "关闭售后",
        COMPLETE_AFTERSALE: "完成售后",
        CREATE_EXPRESS: "快递下单",
        CANCEL_EXPRESS: "取消快递下单",
        MODIFY_SHIPPING_NUMBER: "修改运单号",
        UPDATE_SHIPPING_METHOD_FOR_MERGE: "合单-修改发货方式",
        MERGE_EXPRESS: "合单-修改运单号-辅单",
        MERGE_EXPRESS_MAIN: "合单-修改运单号-主单",
        CUSSERVICE_RETURN: "客服还货",
        OUTSTORAGE_RETURN: "外仓还货",
        ADD_SHIPPING_ADDRESS: "新增发货地址",
        UPDATE_SHIPPING_METHOD: "修改发货方式",
        ADD_GUIDE_NOTE: "导购备注",
        BLOCK_SUCC: "拦截成功",
        BLOCK_FAILED: "拦截失败",
        MODIFY_SHIPPING_NUMBER_FAILED: "修改运单号失败",
        # 货架管理
        STORAGE_IN: "入库",
        STORAGE_OUT: "出库",
        STORAGE_SEAT_CHANGE: "更改货位",
        STORAGE_SEAT_MERGE: "更改货位",

        # 换货
        EXCHANGE_OPEN: "申请换货",
        EXCHANGE_CANCEL: "取消换货",
        EXCHANGE_DONE: "换货完成",
        # 汉光贩卖机提货
        HGVENDING_PICKED_UP: "贩售机提货",
        # 汉光贩卖机-客人自提
        CUS_CONFIRM_AT_HGVENDING: "贩售机端客人自提",
        # 报错日志
        ERROR_MESSAGE: "错误日志",
        # 分阶段支付相关
        PAY_TAIL: "支付尾款",
        RETURN_DEPOSIT: "退定金",
        OVERTIME_TAILPAY: "尾款支付超时",
        # 普通日志
        NORMAL_MESSAGE: "普通日志",
        HAITAO_PACKAGE: "海淘已发货",
        # 海淘推数据给百世
        HAITAO_PUSHDATA_2_BAISHI: "海淘推数据给百世",
        HAITAO_CANCEL_FROM_BAISHI: "海淘取消推百世",
        UPDATE_DELIVER_TIME: "更新发货时间",
        # 合单催配货消息功能
        PUSH_GUIDE_ASSIGN: "合单催配送提醒",

        # 特殊售后单
        AFSPLUS_OPEN: "申请特殊售后",
        AFSPLUS_CLOSE: "取消特殊售后",
        AFSPLUS_COMPLETE: "完成特殊售后",
        AFSPLUS_S2E: "自提转快递",  # 自提转快递
        AFSPLUS_E2S: "快递转自提",  # 快递转自提
        AFSPLUS_TO_EXPRESS: "转快递",
        AFSPLUS_TO_SELF_SERVICE: "转自提",

        # 虚拟商品
        CUS_CONFIRM_AT_VIRTUAL: "虚拟商品确收",
        CLOUDPRINT_SHIPPING_NUMBER: "打印面单"
    }


def get_available_event_list(distribute_status):
    '''
    根据发货单的状态，获取可进行的操作事件列表
    '''
    available_event_list = []
    if not distribute_status:
        return available_event_list
    special_event_list = [
        DistributeEventConst.OPEN_AFTERSALE,
        DistributeEventConst.CLOSE_AFTERSALE,
        DistributeEventConst.COMPLETE_AFTERSALE,
        DistributeEventConst.CREATE_EXPRESS,
        DistributeEventConst.CANCEL_EXPRESS,
        DistributeEventConst.ADD_GUIDE_NOTE,
        DistributeEventConst.CUSSERVICE_RETURN,
        DistributeEventConst.OUTSTORAGE_RETURN,
        DistributeEventConst.EXCHANGE_OPEN,
        DistributeEventConst.EXCHANGE_CANCEL,
        DistributeEventConst.EXCHANGE_DONE,
        DistributeEventConst.HGVENDING_PICKED_UP,
        DistributeEventConst.CUS_CONFIRM_AT_HGVENDING,
        DistributeEventConst.PAY_TAIL,
        DistributeEventConst.RETURN_DEPOSIT,
        DistributeEventConst.OVERTIME_TAILPAY,
        DistributeEventConst.HAITAO_PACKAGE,
        DistributeEventConst.UPDATE_DELIVER_TIME,
        DistributeEventConst.CLOUDPRINT_SHIPPING_NUMBER
    ]
    from_to_map = DistributeEventConst.FROM_TO_MAP
    for event_name, event_dict in from_to_map.items():
        if DistributeEventConstKey.FROM_STATUS_LIST_KEY not in event_dict:
            continue
        from_status_list = event_dict.get(DistributeEventConstKey.FROM_STATUS_LIST_KEY)
        if distribute_status in from_status_list and event_name not in special_event_list:
            event_str = event_name + "|" + DistributeEventConst.EVENT_TO_BUTTONNAME_MAP.get(event_name, event_name)
            available_event_list.append(event_str)
    return available_event_list


class DistributeCommonConst(object):
    NAME_PRIFIX = "包裹"

    MEMBER_CHOICES = (
        (MemberLevel.MEMBER_L0, '普卡'),
        (MemberLevel.MEMBER_L1, '银卡'),
        (MemberLevel.MEMBER_L2, '金卡'),
    )


class OutStorageConfigOrderAddressType(object):
    """ 发货地址配置 """
    # 仅专柜发货
    ONLY_SHOP = "only_shop"
    # 仅外仓发货
    ONLY_OUTSTORAGE = "only_outstorage"
    # 混合发货（既可专柜发货、又可外仓发货）
    MIX_STORAGE = "mix_storage"

    ORDER_ADDRESS_TYPE_CHOICES = (
        (ONLY_SHOP, '专柜'),
        (ONLY_OUTSTORAGE, '外仓'),
        (MIX_STORAGE, '混合仓库'),
    )


class OutStorageConfigAfsAddressType(object):
    """ 退货地址配置 """
    # 全退回专柜
    ALL_TO_SHOP = "all_to_shop"
    # 全退回外仓
    ALL_TO_OUTSTORAGE = "all_to_outstorage"
    # 哪里发货退哪里
    WHERE_TO_COME_AND_WHERE_TO_GO = "where_to_come_and_where_to_go"

    AFS_ADDRESS_TYPE_CHOICES = (
        (ALL_TO_SHOP, '退回专柜'),
        (ALL_TO_OUTSTORAGE, '退回外仓'),
        (WHERE_TO_COME_AND_WHERE_TO_GO, '退回原处'),
    )


class StepPayDeliverTimeType:
    ''' 预售商品发货时间配置 '''

    RELATIVE_TIME = "pay_relative_time"  # 相对发货时间  尾款支付成功后多久可以发货
    FIXED_TIME = "fixed_time"  # 绝对时间


# 欧莱雅集团可同步专柜列表
OLAY_SHOP_DICT_CONST = {
    "108030": "01",
    "108048": "45",
    "108063": "15"
}

class AddressGroupStatus(object):
    """
    可合-已齐、可合-未齐、无可合、已合单、在库已合、单单、无在库、其他
    """
    # 可合-已齐（多单在库、未合、无其他状态）
    MERGABLE_READY = "mergable_ready"
    # 可合-未齐（多单在库、未合、有其他状态）
    MERGABLE_WAITING = "mergable_waiting"
    # 已合单（多单在库、已合、无其他状态）
    MERGED = "merged"
    # 在库-已合（多单在库、已合、有其他状态）
    MERGED_IN_STORE = "merged_in_store"
    # 无可合（一单在库、有其他状态）
    UNMERGABLE = "unmergable"
    # 单单（一单在库、无其他状态）
    SINGLE = 'single'
    # 无在库（0单在库、有其他状态）
    NO_IN_STORE = 'no_in_store'
    # 其他
    OTHER = 'other'

    CHOICES = (
        (MERGABLE_READY, '可合-已齐'),
        (MERGABLE_WAITING, '可合-未齐'),
        (MERGED, "已合单"),
        (MERGED_IN_STORE, "在库-已合"),
        (UNMERGABLE, "无可合"),
        (SINGLE, "单单"),
        (NO_IN_STORE, "无在库"),
        (OTHER, "其他"),
    )
    # 存在未终结发货单的分组
    UNTERMINATE_STATUS_LIST = [MERGABLE_READY, MERGABLE_WAITING, MERGED, MERGED_IN_STORE, UNMERGABLE, NO_IN_STORE, SINGLE]

"""
发货单运送变更事件 枚举
合单、更新运单
TODO 修改地址、修改运输方式
"""
@unique
class DistributeShippingChangeEventEnum(Enum):

    merge_express_order = "merge_express_order"
    create_express_order = "create_express_order"
    update_shipping_number = "update_shipping_number"


    @classmethod
    def choices(cls):
        return (
            (cls.merge_express_order, "合单"),
            (cls.update_shipping_number, "更新运单"),
            (cls.create_express_order, "创建运单"),
        )

"""
拣货任务创建途径
"""
class MergePickPickTaskSource(object):
    # 揽月领任务
    LANYUE_ASSIGN_PICKTASK = 'lanyue_assign_picktask'
    # PDA扫发货单创建拣货任务
    PDA_SCAN_CREATE = 'pda_scan_create'

    CHOICES = (
        (LANYUE_ASSIGN_PICKTASK, '揽月领任务'),
        (PDA_SCAN_CREATE, 'PDA扫码创建任务'),
    )

# 合单拣货任务状态
class MergePickTaskStatus(object):
    # 已领取
    CLAIMED = "claimed"
    # 已完成
    COMPLETED = 'completed'
    # 已关闭
    CLOSED = 'closed'

    CHOICES = (
        (CLAIMED, '已领取'),
        (COMPLETED, '已完成'),
        (CLOSED, "已关闭"),
    )

    NAME_MAP = dict(CHOICES)

# 合单拣货任务覆盖 address group
class MergePickTaskCoverAddressGroup(object):
    # 部分
    PART = "part"
    # 全部
    ALL = 'all'

    CHOICES = (
        (PART, '部分'),
        (ALL, '全部'),
    )

    NAME_MAP = dict(CHOICES)
