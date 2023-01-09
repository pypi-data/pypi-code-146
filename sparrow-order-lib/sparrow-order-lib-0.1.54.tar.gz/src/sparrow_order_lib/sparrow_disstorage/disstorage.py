
import re
from typing import List

from .models import Seat
from .models import StorageRecord
from .constants import ShelfSeatStatus
from .constants import StoreNumberInfo
from .constants import StorageRecordBusiType


class ShelfManager:

    def _seat_number_check(self, seat_number, store_number):
        seat_obj = Seat.objects.filter(
            store_number=store_number,
            seat_number=seat_number,
            status=ShelfSeatStatus.ON
        ).first()
        if not seat_obj:
            raise ValueError(f"货位号{seat_number}无效")
        return seat_obj

    def afswh_seat_number_check(self, seat_number):
        ''' 退换货仓货位检测 '''
        return self._seat_number_check(seat_number, store_number=StoreNumberInfo.AFTERSALE_WH_NUMBER)


class StorageRecordManager:
    ''' 库存管理 '''

    AFS_NUMBER_RE = re.compile(r'T-[^-]+-\d{6}@\d*')
    EXCHANGE_NUMBER_RE = re.compile(r'E-[^-]+-\d{6}-\d+')

    def busi_number_check(self, busi_number):
        if self.AFS_NUMBER_RE.findall(busi_number):
            return StorageRecordBusiType.REFUND
        elif self.EXCHANGE_NUMBER_RE.findall(busi_number):
            return StorageRecordBusiType.EXCHANGE

        raise ValueError(f"票据号{busi_number}格式无效")

    def afs_busi_number_check(self, busi_number):
        ''' 售后单小票检测包含退款单和换货单 '''
        if self.AFS_NUMBER_RE.findall(busi_number):
            return StorageRecordBusiType.REFUND
        elif self.EXCHANGE_NUMBER_RE.findall(busi_number):
            return StorageRecordBusiType.EXCHANGE

        raise ValueError(f"票据号{busi_number}格式无效")

    def get_storage_records(self, busi_number_list) -> List[StorageRecord]:
        obj_list = StorageRecord.objects.filter(
            if_out=0,
            busi_number__in=busi_number_list
        ).all()
        return obj_list
