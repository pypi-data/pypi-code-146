from django.db.models import CharField, DateTimeField, BooleanField, PositiveIntegerField, Count

from ..core.common_utils import get_uuid4_hex
from ..core.base_models import BaseModelTimeAndDeleted
from .constants import InventoryDetailResult
from .constants import InventoryHelpStatus
from .constants import InventoryMainStatus
from . import APP_LABEL


__all__ = [
    'InventoryMain',
    'InventoryDetail',
    'InventoryHelp',
    'InventoryNote',
    'Shelf',
    'Seat',
    'StorageRecord',
]


class InventoryMain(BaseModelTimeAndDeleted):
    """
        库存盘点主表
    """
    id = CharField("id", primary_key=True, default=get_uuid4_hex, blank=True, max_length=128)
    number = CharField("盘点序列号", max_length=128, db_index=True, unique=True)
    distribute_status = CharField("盘点位置", max_length=128, blank=True)
    distribute_status_name = CharField("盘点位置名称", max_length=128, blank=True)
    inventory_user_id = CharField("盘点人 id", max_length=128, blank=True)
    inventory_username = CharField("盘点人姓名", max_length=128, blank=True)
    inventory_user_displayname = CharField("盘点人昵称", max_length=128, blank=True)
    initial_num = PositiveIntegerField("期初数", blank=True)  # 盘点开始时, 由系统判断在库房内的发货单数量
    actual_num = PositiveIntegerField("实核数", default=0, blank=True)  # 盘平的发货单数量
    profit_num = PositiveIntegerField("盘盈发货单数量", default=0, blank=True, null=True)
    loss_num = PositiveIntegerField("盘亏发货单数量", default=0, blank=True, null=True)
    profit_dealed_num = PositiveIntegerField("已核销的盘盈发货单数量", default=0, blank=True, null=True)
    loss_dealed_num = PositiveIntegerField("已核销的盘亏发货单数量", default=0, blank=True, null=True)
    if_balance = BooleanField("是否持平", default=False, blank=True, null=True)
    inventory_start_time = DateTimeField("盘点开始时间", blank=True, auto_now_add=True)
    inventory_end_time = DateTimeField("盘点结束时间", blank=True, null=True)
    if_help = BooleanField("是否是多人盘点", null=True, default=0, db_index=True)
    status = CharField("盘点状态", max_length=16, default=InventoryMainStatus.INIT, db_index=True)

    @property
    def helps(self):
        return InventoryHelp.objects.filter(main_id=self.id).order_by('-help_start_time', 'shelf_number')

    @property
    def details(self):
        ''' 所有盘点列表 '''
        return InventoryDetail.objects.filter(main_id=self.id).order_by('updated_time')

    class Meta:
        verbose_name = '库存盘点主表'
        app_label = APP_LABEL


class InventoryDetail(BaseModelTimeAndDeleted):
    """
        盘点明细表
    """
    id = CharField("id", primary_key=True, default=get_uuid4_hex, blank=True, max_length=128)
    main_id = CharField("盘点主表 id", db_index=True, blank=True, max_length=128)
    main_number = CharField("盘点序列号", max_length=128, blank=True)
    distribute_id = CharField("发货单 id", max_length=100, blank=True, db_index=True)
    distribute_number = CharField("发货单号", max_length=100, blank=True)
    distribute_name = CharField("发货单名称", max_length=100, blank=True)
    order_id = PositiveIntegerField("订单 id", blank=True, db_index=True)
    order_number = CharField("订单号", max_length=128, blank=True)
    shop_id = PositiveIntegerField("专柜 id", blank=True)
    shop_num = CharField("专柜号", max_length=128, blank=True)
    shop_name = CharField("专柜名称", max_length=128, blank=True)
    aftersale_status = BooleanField("是否售后", blank=True)
    store_in_time = DateTimeField("入库时间", blank=True, null=True)
    if_checked = BooleanField("是否已盘点", default=False, blank=True)
    checked_time = DateTimeField("盘点时间", default=None, blank=True, null=True)
    checked_result = CharField("盘点结果", max_length=100, default='unchecked', blank=True, db_index=True)
    if_dealed = BooleanField("是否核销", default=False, blank=True, db_index=True)

    dealed_user_id = CharField("核销人 id", max_length=128, blank=True, null=True)
    dealed_username = CharField("核销人姓名", max_length=128, blank=True, null=True)
    dealed_user_displayname = CharField("核销人昵称", max_length=128, blank=True, null=True)
    dealed_time = DateTimeField("核销时间", null=True, blank=True)

    help_id = CharField("领取任务助力人", max_length=32, null=True, db_index=True)
    dealed_type = CharField("核销类型", max_length=16, null=True)
    shelf_id = CharField("shelf_id", max_length=32, null=True)
    shelf_number = CharField("shelf_number", max_length=32, null=True)
    seat_id = CharField("seat_id", max_length=32, null=True)
    seat_number = CharField("seat_number", max_length=32, null=True)
    checked_user_id = CharField("实际盘点人", max_length=64, null=True)
    checked_shelf_number = CharField("实际盘点位置", max_length=64, null=True)

    @property
    def notes(self):
        return InventoryNote.objects.filter(detail_id=self.id).order_by('-created_time')

    @property
    def checked_result_show(self):
        return InventoryDetailResult.CHECKED_RESULT_MAP.get(self.checked_result)

    class Meta:
        verbose_name = '盘点明细表'
        app_label = APP_LABEL


class InventoryHelp(BaseModelTimeAndDeleted):
    id = CharField("id", primary_key=True, default=get_uuid4_hex, blank=True, max_length=32)
    main_id = CharField("盘点记录ID", max_length=32)
    main_number = CharField("盘点记录 number", max_length=64)
    shelf_id = CharField("货架ID", max_length=32)
    shelf_number = CharField("货架号", max_length=32)
    help_user_id = CharField("助力人 id", max_length=64, null=True, db_index=True)
    help_username = CharField("助力人姓名", max_length=64, null=True)
    help_user_displayname = CharField("助力人昵称", max_length=64, null=True)
    initial_num = PositiveIntegerField("期初数")
    actual_num = PositiveIntegerField("实核数", null=True)
    status = CharField("助力盘点状态", max_length=16, default=InventoryHelpStatus.PENDING)
    help_start_time = DateTimeField("助力开始时间", null=True)
    help_end_time = DateTimeField("助力结束时间", null=True)

    class Meta:
        index_together = ["main_id", "shelf_id"]
        app_label = APP_LABEL

    @property
    def status_show(self):
        return InventoryHelpStatus.InventoryHelpStatusShowDict[self.status]


class InventoryNote(BaseModelTimeAndDeleted):
    """
        盘点结果备注表, 存储对盘盈/盘亏发货单的核销意见
    """
    id = CharField("id", primary_key=True, default=get_uuid4_hex, blank=True, max_length=128)
    detail_id = CharField("盘点明细表 id", db_index=True, max_length=128)

    main_id = CharField("盘点主表 id", db_index=True, blank=True, max_length=128)
    main_number = CharField("盘点序列号", max_length=128, blank=True)
    distribute_id = CharField("发货单 id", max_length=100, blank=True, db_index=True)
    distribute_number = CharField("发货单号", max_length=100, blank=True)
    distribute_name = CharField("发货单名称", max_length=100, blank=True)

    note_user_id = CharField("备注人 id", max_length=128, blank=True)
    note_username = CharField("备注人姓名", max_length=128, blank=True)
    note_user_displayname = CharField("备注人昵称", max_length=128, blank=True)
    note_time = DateTimeField("处理时间")
    message = CharField("处理意见", max_length=512, blank=True)

    class Meta:
        verbose_name = '盘点备注表'
        app_label = APP_LABEL


class Shelf(BaseModelTimeAndDeleted):
    """
    货架表
    """
    id = CharField("id", primary_key=True, default=get_uuid4_hex, blank=True, max_length=128)
    store_code = CharField("货架位置编码", db_index=True, max_length=128)
    store_number = CharField("货架位置编号", db_index=True, max_length=128)
    store_name = CharField("货架位置名称", max_length=128)
    number = CharField("货架编号", max_length=128)
    rows_count = PositiveIntegerField("货架行数", default=1, blank=True)
    column_count = PositiveIntegerField("货架列数", default=1, blank=True)
    created_user_id = CharField("创建人 id ", max_length=128)
    created_user_name = CharField("创建人姓名", max_length=128)
    created_user_displayname = CharField("创建人昵称", max_length=128)
    shelf_type = CharField("货架类型", default="NORMAL", blank=True, max_length=32)
    status = CharField("货架状态", default="ON", blank=True, max_length=32)

    class Meta:
        app_label = APP_LABEL

    @property
    def seats(self):
        '''
        货架所有货位详情

        "seats": [
            {
                "line": "E",
                "data": [
                    {
                        "seat_number": "002-E001-ZT",
                        "count": 0
                    },
                    ... ...
                ],
            },
            {
                "line": "D",
                "data": [
                    {
                        "seat_number": "002-D001-ZT",
                        "count": 0
                    },
                    ... ...
                ],
            },
            ... ...
        ]
        '''
        storage_record_count_distribute_number_by_seat = StorageRecord.objects.filter(shelf_id=self.id, if_out=False).\
            values('seat_number').annotate(count=Count('distribute_number', distinct=True)).values('count', 'seat_number').all()
        count_dict = {row['seat_number']: row['count'] or 0 for row in storage_record_count_distribute_number_by_seat}

        seat_objs = Seat.objects.filter(shelf_id=self.id).all()

        seats = {}

        for seat in seat_objs:
            row_number = seat.row_number
            seat_number = seat.seat_number
            count = count_dict.get(seat_number, 0)
            seats.setdefault(row_number, [])
            seats[seat.row_number].append({'seat_number': seat_number, 'count': count})

        result = []
        for row, data in seats.items():
            data.sort(key=lambda d: d['seat_number'])
            result.append({'line': row, 'data': data})
        result.sort(key=lambda d: d['line'])

        return result

    @property
    def distributes_count(self):
        ''' 货架上所有存在的发货单数量 '''
        return StorageRecord.objects.filter(shelf_id=self.id, if_out=False).count()


class Seat(BaseModelTimeAndDeleted):
    """
    货位表
    """
    id = CharField("货位 id ", primary_key=True, default=get_uuid4_hex, max_length=128, blank=True)
    shelf_id = CharField("货架 id ", max_length=128, db_index=True)
    shelf_number = CharField("货架编号", max_length=128)
    store_code = CharField("货架位置编码", max_length=128)
    store_number = CharField("货架位置", max_length=128)
    store_name = CharField("货架位置名称", max_length=128)
    row_number = CharField("行号", max_length=128)
    column_number = CharField("列号", max_length=128)
    seat_number = CharField("货位编号", max_length=128)
    status = CharField("货位状态", default="ON", blank=True, max_length=32)

    class Meta:
        app_label = APP_LABEL


class StorageRecord(BaseModelTimeAndDeleted):
    """
    库存表
    """
    id = CharField("库存 id", primary_key=True, default=get_uuid4_hex, max_length=128, blank=True)

    distribute_id = CharField("发货单id", max_length=128, db_index=True)
    distribute_number = CharField("发货单号", max_length=128, db_index=True)

    order_id = CharField("订单 id ", max_length=128, db_index=True)
    order_number = CharField("订单号", max_length=128, db_index=True)
    shop_id = CharField("专柜id", max_length=128)
    shop_num = CharField("专柜号", max_length=128)
    shop_name = CharField("专柜名称", max_length=128, db_index=True)

    store_code = CharField("货架位置编码", db_index=True, max_length=128)
    store_number = CharField("仓库编号", db_index=True, max_length=128)
    store_name = CharField("仓库名称", max_length=128)
    shelf_id = CharField("货架", max_length=128, db_index=True)
    shelf_number = CharField("货架编号", max_length=128)
    seat_id = CharField("货位", max_length=128, db_index=True)
    seat_number = CharField("货位编号", max_length=128)

    store_in_time = DateTimeField("入库时间", db_index=True)
    store_in_event = CharField("入库原因", max_length=128, default="storage_init")
    store_in_user_id = CharField("入库人 id ", max_length=128)
    store_in_user_name = CharField("入库人姓名", max_length=128)
    store_in_user_displayname = CharField("入库人昵称", max_length=128)
    store_out_time = DateTimeField("出库时间", db_index=True, null=True)
    store_out_event = CharField("出库原因", max_length=128, null=True)
    store_out_user_id = CharField("出库人 id ", max_length=128, null=True)
    store_out_user_name = CharField("出库人姓名", max_length=128, null=True)
    store_out_user_displayname = CharField("出库人昵称", max_length=128, null=True)
    if_out = BooleanField("是否已提走", default=False, db_index=False, blank=False)

    busi_id = CharField("业务单ID", max_length=40, db_index=True, null=True)
    busi_number = CharField("业务单number", max_length=64, db_index=True, null=True)
    busi_type = CharField("业务单类型", max_length=16, db_index=True, null=True)

    class Meta:
        app_label = APP_LABEL
