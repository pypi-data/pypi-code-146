import datetime

from django.db import models

from ..core.base_models import BaseModelTimeAndDeleted
from ..core.formats import PARCEL_NUMBER_FMT
from ..core.numbers import getRandomNumSet
from ..core.common_utils import get_uuid4_hex
from .constants import TransferStatus
from .constants import ParcelStatus
from . import APP_LABEL

__all__ = ['Parcel', 'Footprint', 'Transfer', 'TransferDetail']


class Parcel(BaseModelTimeAndDeleted):
    """ 包裹档案 """
    id = models.CharField(max_length=32, primary_key=True, default=get_uuid4_hex, editable=False)
    shipping_number = models.CharField("包裹运单号", max_length=32, db_index=True)
    express_code = models.CharField("快递公司代码", max_length=32, db_index=True, null=True)
    express_name = models.CharField("快递公司名称", max_length=32, null=True)
    parcel_status = models.CharField("包裹状态", max_length=32, db_index=True, default=ParcelStatus.INIT)
    in_time = models.DateTimeField("包裹入系统时间", null=True)
    in_user_id = models.CharField("包裹入系统操作人", max_length=32, null=True)
    in_user_name = models.CharField("包裹入系统操作人", max_length=32, null=True)
    in_user_role = models.CharField("包裹入系统操作人角色", max_length=16, null=True)
    out_time = models.DateTimeField("包裹出系统时间", null=True)
    out_user_id = models.CharField("包裹出系统操作人", max_length=32, null=True)
    out_user_name = models.CharField("包裹出系统操作人", max_length=32, null=True)
    out_user_role = models.CharField("包裹出系统操作人角色", null=True, max_length=16)
    # 包裹有可能来源于 发货单打包发货、提货机打包、退货
    source = models.CharField("包裹入系统来源", max_length=16, db_index=True)

    class Meta:
        app_label = APP_LABEL


class Footprint(BaseModelTimeAndDeleted):
    """ 包裹操作日志 """
    id = models.CharField(max_length=32, primary_key=True, default=get_uuid4_hex, editable=False)
    parcel_id = models.CharField(max_length=32, editable=False, db_index=True)
    shipping_number = models.CharField("包裹运单号", max_length=32, db_index=True)
    express_code = models.CharField("快递公司代码", max_length=32, null=True)
    express_name = models.CharField("快递公司名称", max_length=32, null=True)
    event = models.CharField('事件', max_length=128, blank=True, null=True, db_index=True)
    event_sponsor = models.CharField('事件发起人', max_length=255, blank=True, null=True)
    event_sponsor_name = models.CharField('事件发起人昵称', max_length=255, blank=True, null=True)
    event_time = models.DateTimeField("Event Happened Time", blank=True, null=True, auto_now=True)
    from_status = models.CharField('起始状态', max_length=128, blank=True, null=True, db_index=True)
    to_status = models.CharField('结果状态', max_length=128, blank=True, null=True, db_index=True)
    message = models.CharField('信息', max_length=16384, blank=True, null=True)
    message_detail = models.CharField('开发看的信息', max_length=2048, blank=True, null=True)
    message_level = models.PositiveIntegerField("Log Level", default=1, db_index=True)

    class Meta:
        app_label = APP_LABEL


def get_sparrow_parcel_number():
    '''
    发货单number生成规则， 年月日时分秒+"-"+6位随机数，比如20200513123086-564734
    '''
    now = datetime.datetime.now()
    random_set = getRandomNumSet(6)
    number = now.strftime(PARCEL_NUMBER_FMT).format(rand=random_set)
    return number


class Transfer(BaseModelTimeAndDeleted):
    """ 交接档案表 """
    id = models.CharField(max_length=32, primary_key=True, default=get_uuid4_hex, editable=False)
    transfer_number = models.CharField("交接单号", max_length=32, unique=True, default=get_sparrow_parcel_number)
    express_code = models.CharField("快递公司代码", max_length=32)
    express_name = models.CharField("快递公司名称", max_length=32)
    onshelf_user_id = models.CharField("上架人信息", max_length=32, db_index=True)
    onshelf_user_name = models.CharField("上架人信息", max_length=32)
    onshelf_time = models.DateTimeField("上架时间")
    transfer_status = models.CharField("交接状态", max_length=16, db_index=True, default=TransferStatus.ACTIVE)
    recall_user_id = models.CharField("召回人信息", max_length=32, db_index=True, null=True)
    recall_user_name = models.CharField("召回人信息", max_length=32, null=True)
    recall_time = models.DateTimeField("召回时间", null=True)
    shelf_id = models.CharField("货架ID", max_length=32)
    shelf_number = models.CharField("货架编号", max_length=32)
    parcel_cnt_initial = models.PositiveIntegerField("包裹初始数量")

    class Meta:
        app_label = APP_LABEL

    @property
    def transfer_details(self):
        return TransferDetail.objects.filter(transfer_id=self.id)


class TransferDetail(BaseModelTimeAndDeleted):
    """ 交接明细表 """
    id = models.CharField(max_length=32, primary_key=True, default=get_uuid4_hex, editable=False)
    transfer_id = models.CharField("交接记录ID", max_length=32, db_index=True)
    transfer_number = models.CharField("交接单号", max_length=32, db_index=True)
    parcel_id = models.CharField(max_length=32, db_index=True)
    shipping_number = models.CharField("包裹运单号", max_length=32, db_index=True)
    express_code = models.CharField("快递公司代码", max_length=32, db_index=True, null=True)
    express_name = models.CharField("快递公司名称", max_length=32, null=True)
    # material_code varchar(12) 物料编码
    material_code = models.CharField("物料编码", max_length=12, null=True)
    # material_name varchar(12) 物料名称
    material_name = models.CharField("物料名称", max_length=12, null=True)

    class Meta:
        app_label = APP_LABEL


class Material(BaseModelTimeAndDeleted):
    """ 物料档案 """
    # name varchar(12) 名称
    name = models.CharField("物料名称", max_length=12, null=True)
    # code varchar(10) 编码，编码格式：B-001
    code = models.CharField("物料编码", max_length=12, null=True)
    # type varchar(10) 类型
    type = models.CharField("类型", max_length=10, null=True)
    # description varchar(50) 描述
    description = models.CharField("描述", max_length=50, null=True)
    # spec varchar(20) 规格
    spec = models.CharField("规格", max_length=20, null=True)
    # model varchar(20) 型号
    model = models.CharField("型号", max_length=20, null=True)
    # 排序规则
    seq = models.IntegerField("排序", default=0)

    class Meta:
        app_label = APP_LABEL
        


class MaterialOptRecord(BaseModelTimeAndDeleted):
    """ 物料档案 """
    # material_name varchar(12) 物料名称
    material_name = models.CharField("物料名称", max_length=12, null=True)
    # material_code varchar(12) 物料编码
    material_code = models.CharField("物料编码", max_length=12, null=True)
    # opt varchar(12)  （出库/入库）
    opt = models.CharField("操作类型", max_length=12, null=True)
    # opt_user_id varchar(12) 操作人ID
    opt_user_id = models.CharField("操作人ID", max_length=40, null=True)
    # opt_user_name  varchar(12) 操作人名称
    opt_user_name = models.CharField("操作人名称", max_length=32, null=True)
    # quantity 数量 int（出库/入库都是正整数）
    quantity = models.IntegerField("数量", default=0)
    

    class Meta:
        app_label = APP_LABEL

