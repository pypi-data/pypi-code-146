"""
    常量
"""
from ..core.datastructures import ImmutableList
from ..core.datastructures import ImmutableDict
from ..sparrow_distribute.constants import DistributeStatus


class StorageRecordBusiType:
    ''' 入库时, 单据类型 '''
    REFUND = 'refund'  # 退款单小票
    EXCHANGE = 'exchange'  # 换货单小票
    DISTRIBUTE = 'distribute'  # 发货单小票


class StoreNumberInfo(object):
    """ 仓库信息及对应发货单状态 """
    SERVICE_STORE_NUMBER = "B3"
    SERVICE_STORE_NAME = "B3仓库"
    SERVICE_DESK_NUMBER = "ZT"
    SERVICE_DESK_NAME = "自提点"
    SERVICE_STOP_NUMBER = "STOP"
    SERVICE_STOP_NAME = "滞留仓"
    AFTERSALE_WH_NUMBER = "AFS"
    AFTERSALE_WH_CODE = "AFS"
    AFTERSALE_WH_NAME = "退换货仓"

    DISTRIBUTE_STATUS_STORE_INFO_MAP = {
        DistributeStatus.SERVICE_DESK: {
            'name': SERVICE_DESK_NAME,
            'number': SERVICE_DESK_NUMBER,
            'code': DistributeStatus.SERVICE_DESK
        },
        DistributeStatus.SERVICE_STORE: {
            'name': SERVICE_STORE_NAME,
            'number': SERVICE_STORE_NUMBER,
            'code': DistributeStatus.SERVICE_STORE
        },
        DistributeStatus.SERVICE_STOP: {
            'name': SERVICE_STOP_NAME,
            'number': SERVICE_STOP_NUMBER,
            'code': DistributeStatus.SERVICE_STOP
        }
    }

    STORE_INFO_MAP = {
        SERVICE_STORE_NUMBER: {
            'name': SERVICE_STORE_NAME,
            'number': SERVICE_STORE_NUMBER,
            'code': DistributeStatus.SERVICE_STORE
        },
        SERVICE_DESK_NUMBER: {
            'name': SERVICE_DESK_NAME,
            'number': SERVICE_DESK_NUMBER,
            'code': DistributeStatus.SERVICE_DESK
        },
        SERVICE_STOP_NUMBER: {
            'name': SERVICE_STOP_NAME,
            'number': SERVICE_STOP_NUMBER,
            'code': DistributeStatus.SERVICE_STOP
        },
        AFTERSALE_WH_NUMBER: {
            'name': AFTERSALE_WH_NAME,
            'number': AFTERSALE_WH_NUMBER,
            'code': AFTERSALE_WH_CODE,
        }
    }

    STORE_NUMBER_TO_NAME_MAP = {d['number']: d['name'] for d in STORE_INFO_MAP.values()}
    STORE_NUMBER_TO_CODE_MAP = {d['number']: d['code'] for d in STORE_INFO_MAP.values()}
    STORE_CODE_TO_NAME_MAP = {d['code']: d['name'] for d in STORE_INFO_MAP.values()}
    STORE_CODE_TO_NUMBER_MAP = {d['code']: d['number'] for d in STORE_INFO_MAP.values()}


class InventoryDetailResult(object):
    """
        发货单盘点结果
    """
    # 盘盈
    PROFIT = 'profit'
    # 盘亏
    LOSS = 'loss'
    # 持平
    BALANCE = 'balance'
    # 库内盘盈
    DISLOCATION = 'dislocation'

    # INVENTORY_DETAIL_RESULT_CHOICES = (
    #     (PROFIT, '盘盈'),
    #     (LOSS, '盘亏'),
    #     (BALANCE, '持平'),
    #     (DISLOCATION, '库内差异')
    # )

    CHECKED_RESULT_MAP = ImmutableDict({
        PROFIT: "盘盈",
        LOSS: "盘亏",
        BALANCE: "盘平",
        DISLOCATION: "库内差异"
    })

    UNBALANCE = [PROFIT, LOSS]
    UNBALANCE_MID = [PROFIT, LOSS, DISLOCATION]
    ACTUAL_CHECKED_RESULT = [BALANCE, PROFIT, DISLOCATION]

    DEALED_MESSAGE_MAP = ImmutableDict({
        PROFIT: "核销盘盈差异",
        LOSS: "核销盘亏差异",
        DISLOCATION: "核销库内位置错误差异",
    })


class InventoryDealedType:
    INTERIOR = 'interior'  # 库内核销
    EXTERIOR = 'exterior'  # 库外核销

    DealedTypeMap = ImmutableDict({
        INTERIOR: "库内核销",
        EXTERIOR: "库外核销"
    })


class InventoryMainStatus:
    """ 盘点记录状态 """
    INIT = "init"  # 初始
    COMPLETED = "completed"  # 已完成
    CLOSED = "closed"  # 已关闭


class InventoryHelpStatus:
    """ 助力盘点的状态 """
    PENDING = "pending"  # 待领取
    ACCESSED = "accessed"  # 已领取
    CHECKING = "checking"  # 盘点中
    COMPLETED = "completed"  # 已完成
    CLOSED = "closed"  # 已关闭, 由关闭盘点记录触发

    InventoryHelpStatusShowDict = ImmutableDict({
        PENDING: "待盘点",
        ACCESSED: "待盘点",
        CHECKING: "盘点中",
        COMPLETED: "盘点完成",
        CLOSED: "已关闭",
    })

    # 盘点中的状态
    CHECKING_STATUS = ImmutableList([ACCESSED, CHECKING])


class ShelfType(object):
    NORMAL = 'NORMAL'  # 常规货架
    INSTANT = 'INSTANT'  # 临时货架
    INIT = 'INIT'  # 货架管理上架时数据升级使用
    MERGED = 'MERGED'  # 系统默认合单后用于放发货单的位置, 这些合单后的发货单会直接打包发货, 所以没必要分配其他货位, 提高客服操作效率
    PICKUP = 'PICKUP'

    NORMAL_NAME = "固定货架"
    INSTANT_NAME = "临时货架"

    VALID_SHELF_TYPES_TO_CREATE = frozenset([NORMAL, INSTANT])
    VALID_SHELF_TYPES_TO_VIEW = frozenset([NORMAL, INSTANT, MERGED, PICKUP, INIT])

    SHELF_TYPE_DICT = {
        NORMAL: NORMAL_NAME,
        INSTANT: INSTANT_NAME
    }


class StringFmt(object):
    # 盘点序列号
    INVENTORY_NUMBER = '{}%y%m%d%H%M%S'
    # 固定货架编号格式
    SHELF_NORMAL_NUMBER = '{store_number}-{serial_number:0>3d}'
    # 临时货架编号格式
    SHELF_INSTANT_NUMBER = '{store_number}-LS{serial_number:0>3d}'
    # 固定货架货位编号格式
    SEAT_NORMAL_NUMBER = '{shelf_serial_number:0>3d}-{row_number}{column_number:0>3d}-{store_number}'
    # 临时货架货位编码格式
    SEAT_INSTANT_NUMBER = 'LS{shelf_serial_number:0>3d}-A000-{store_number}'

    SEAT_NUMBER_FMT_MAP = {
        ShelfType.NORMAL: SEAT_NORMAL_NUMBER,
        ShelfType.INSTANT: SEAT_INSTANT_NUMBER
    }

    SHELF_NUMBER_FMT_MAP = {
        ShelfType.NORMAL: SHELF_NORMAL_NUMBER,
        ShelfType.INSTANT: SHELF_INSTANT_NUMBER
    }

    # 货架管理上架前, 对所有在库发货单初始化库存信息, 使用该货架
    SHELF_INIT_NUMBER = '{store_number}-INIT'
    SEAT_INIT_NUMBER = 'INIT-A000-{store_number}'
    SHELF_MERGED_NUMBER = '{store_number}-888'
    SEAT_MERGED_NUMBER = '888-A000-{store_number}'
    SHELF_PICKUP_NUMBER = '{store_number}-666'
    SEAT_PICKUP_NUMBER = '666-A000-{store_number}'


ROW_NUMBERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class ShelfSeatStatus(object):
    ON = 'ON'  # 正常
    OFF = 'OFF'  # 废弃
    INIT = 'INIT'  # 货架管理上架时数据升级使用


# 助力时分布式锁
ACCESS_HELPS_LOCK_KEY_FMT = "SparrowOrderDisstorageHelpsAccessLock_{main_id}_{shelf_id}"
ACCESS_HELPS_LOCK_EXPIRE = 10


class FlashInventoryConst(object):

    SERVICE_STOP_INVENTORY = "service_stop_inventory"

    FlashInventory_code2name_DICT = {
        SERVICE_STOP_INVENTORY: "滞留仓盘点"
    }

    FlashInventory_code2sql_DICT = {
        SERVICE_STOP_INVENTORY: """ select distinct np.shipping_number
from sparrow_distribute_distribute dis
join sparrow_distribute_expressrela rela on dis.id=rela.distribute_id
join sparrow_shipping_newexpressorder np on np.id=rela.newexpressorder_id
where dis.distribute_status='service_stop' """
    }
