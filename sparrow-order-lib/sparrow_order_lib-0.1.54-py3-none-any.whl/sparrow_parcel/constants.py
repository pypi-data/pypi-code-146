from ..sparrow_shipping.constants import ShippingPartnerCodes
from ..core.constants import UserRole


BASE_INPARCEL_API_CODE = 20216000


class InParcelStatus(object):
    '''
    ### 换货单总单状态 ###
    '''
    INIT = "init"
    RECEIVED = "received"
    REFUSED = "refused"
    EXCEPTION = "exception"
    COMPLETE = "complete"

    INPARCEL_STATUS_CHOICES = (
        (INIT, "初始态"),
        (RECEIVED, "确收"),
        (REFUSED, "拒收"),
        (EXCEPTION, "异常"),
        (COMPLETE, "已拆"),
    )
    INPARCEL_STATUS_DICT = dict(INPARCEL_STATUS_CHOICES)


class InParcelSource(object):
    '''
    收包裹来源
    '''
    COMMON = "common"
    """ 普通收包裹（客人寄回、售后拦截、客人拒收等） """

    EXPRESS_RETURN = 'express_return'
    """ 快递公司退回包裹（比如因疫情原因，无法发往） """

    CHOICES = (
        (COMMON, "普通收包裹"),
        (EXPRESS_RETURN, "快递公司退回包裹"),
    )


class InParcelConnectCustomer(object):
    '''
    ### 联系顾客 ###
    '''
    YET_CONNECT = "yet_connect"
    NOT_CONNECT = "not_connect"
    CHOICES = (
        (YET_CONNECT, "已联系顾客"),
        (NOT_CONNECT, "未联系顾客"),
    )


class EventMapKey(object):

    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class InParcelTaskType(object):
    '''
    ### 任务类型 ###
    '''
    # 确收
    RECEIVE = "receive"
    # 拒收
    REFUSE = "refuse"

    CHOICES = (
        (RECEIVE, "确收"),
        (REFUSE, "拒收"),
    )


class InParcelEventConst(object):
    '''
    ### 事件 ###
    '''
    # 确收
    RECEIVE = "receive"
    # 拒收
    REFUSE = "refuse"
    # 修改邮费支付方式
    UPDATE_POSTAGE_PAY_METHOD = 'update_postage_pay_method'
    # 删除
    DELETE_FROM_TASK = 'delete_from_task'
    # 自动关联商品
    AUTO_RELA_ENTITY = 'auto_rela_entity'
    # 手动增加关联商品
    MANUAL_ADD_RELA_ENTITY = 'manual_add_rela_entity'
    # 手动删除关联商品
    MANUAL_REMOVE_RELA_ENTITY = 'manual_remove_rela_entity'
    # 标记异常
    MARK_EXCEPTION = 'mark_exception'
    # 标记完成、拆包裹
    MARK_COMPLETE = 'mark_complete'

    CHOICES = (
        (RECEIVE, "确收"),
        (REFUSE, "拒收"),
        (UPDATE_POSTAGE_PAY_METHOD, "修改邮费支付方式"),
        (DELETE_FROM_TASK, "删除"),
        (AUTO_RELA_ENTITY, '自动关联商品'),
        (MANUAL_ADD_RELA_ENTITY, '手动增加关联商品'),
        (MANUAL_REMOVE_RELA_ENTITY, '手动删除关联商品'),
        (MARK_EXCEPTION, '标记异常'),
        (MARK_COMPLETE, '拆包裹(标记完成)'),
    )

    EVENT_2_NAME_MAP = {
        RECEIVE: "确收",
        REFUSE: "拒收",
        UPDATE_POSTAGE_PAY_METHOD: "修改邮费支付方式",
        DELETE_FROM_TASK: "删除",
        AUTO_RELA_ENTITY: '自动关联商品',
        MANUAL_ADD_RELA_ENTITY: '手动增加关联商品',
        MANUAL_REMOVE_RELA_ENTITY: '手动删除关联商品',
        MARK_EXCEPTION: '标记异常',
        MARK_COMPLETE: '拆包裹(标记完成)',
    }

    # 注意：
    # 1、当不存在EventMapKey.USER_ROLES_KEY的key时，说明所有角色都可以操作；
    # 2、当EventMapKey.TO_STATUS_KEY对应的value设置为None时，则说明动作不会造成状态变更；
    FROM_TO_MAP = {
        RECEIVE: {  # 收包裹
            InParcelStatus.INIT: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.RECEIVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            InParcelStatus.EXCEPTION: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.RECEIVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
        },
        REFUSE: {  # 拒收包裹
            InParcelStatus.INIT: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.REFUSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            },
            InParcelStatus.COMPLETE: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.REFUSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        UPDATE_POSTAGE_PAY_METHOD: {  # 修改邮费支付方式
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        DELETE_FROM_TASK: {
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        MANUAL_ADD_RELA_ENTITY: {
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        MANUAL_REMOVE_RELA_ENTITY: {
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        MARK_EXCEPTION: {
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.EXCEPTION,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
        MARK_COMPLETE: {
            InParcelStatus.RECEIVED: {
                EventMapKey.TO_STATUS_KEY: InParcelStatus.COMPLETE,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE]
            }
        },
    }


"""
收包裹的快递公司
京东
顺丰
中通
申通
韵达
邮政
圆通
德邦
其他
"""
in_parcel_express_partner_list = [
    ShippingPartnerCodes.JD,
    ShippingPartnerCodes.SF,
    ShippingPartnerCodes.ZTO,
    ShippingPartnerCodes.STO,
    ShippingPartnerCodes.YD,
    ShippingPartnerCodes.YZPY,
    ShippingPartnerCodes.YTO,
    ShippingPartnerCodes.DBL,
    ShippingPartnerCodes.OTHERS,
]


"""
收包裹关联类型

# 关联发货单、换货单、退货单
发货单Distribute ID models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
发货单Distribute number models.CharField("Distribute number", max_length=40, db_index=True, unique=True, default=get_sparrow_distribute_number)

换货单行ExchangeLine id = models.CharField(max_length=100, primary_key=True, default=get_uuid4_hex, editable=False)
换货单行ExchangeLine exline_number = models.CharField("换货分单编号", max_length=64, db_index=True, unique=True)

售后单lineID 售后单line = 
"""


class InParcelEntityRelaType():
    # 发货单的运单号
    DISTRIBUTE = 'distribute'
    # 退货单line
    AFTERSALE_LINE = 'aftersale_line'
    # 换货单line 客人寄回
    EXCHANGE_LINE_CUSTOMER = 'exchange_line_customer'
    # 换货单line 导购寄出
    EXCHANGE_LINE_GUIDE = 'exchange_line_guide'

    CHOICES = (
        (DISTRIBUTE, "发货单"),
        (AFTERSALE_LINE, "退货单line"),
        (EXCHANGE_LINE_CUSTOMER, "换货单line 客人寄回"),
        (EXCHANGE_LINE_GUIDE, "换货单line 导购寄出"),
    )
    # 给手动关联接口用的选项
    MANUAL_UPDATE_CHOICES = (
        ('refund', "退货单line"),
        ('exchange', "换货单line 客人寄回"),
    )
    MANUAL_UPDATE_CHOICES_MAP = {
        'refund': AFTERSALE_LINE,
        'exchange': EXCHANGE_LINE_CUSTOMER,
    }


"""
收包裹关联创建来源

收包裹时，客人回填时，客服修改售后运单号时


"""


class InParcelEntityRelaDataSource():
    # 收包裹
    RECEIVE_INPARCEL = 'receive_inparcel'
    # 客人回填运单号
    CUSTOMER_SUBMIT = 'customer_submit'
    # 客服修改运单号
    CUSSERVICE_UPDATE = 'cusservice_update'
    # 客服手动编辑关联商品
    CUSSERVICE_MANUAL_UPDATE = 'cusservice_manual_update'

    CHOICES = (
        (RECEIVE_INPARCEL, "收包裹时"),
        (CUSTOMER_SUBMIT, "客人回填运单号"),
        (CUSSERVICE_UPDATE, "客服修改售后运单号"),
        (CUSSERVICE_MANUAL_UPDATE, "客服手动编辑关联商品"),
    )

    USER_ROLE_TO_DATA_SOURCE_MAP = {
        UserRole.CUSTOMER: CUSTOMER_SUBMIT,
        UserRole.CUSSERVICE: CUSSERVICE_UPDATE,
    }
