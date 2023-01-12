"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/9/15 14:14
"""
from pathlib import Path

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F

from main.settings import BASE_DIR
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from ..models import Enroll, EnrollRecord, EnrollSubitem, EnrollSubitemRecord
from ..serializers import EnrollRecordListSerializer
from ..service.clock_service import ClockService
from ..service.enroll_record_serivce import EnrollRecordServices
from ..service.enroll_subitem_record_service import EnrollSubitemRecordService
from ..service.subitem_extend_service import output_convert
from ..utils.custom_tool import format_params_handle
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

sand_box_meet = main_config_dict.sand_box_meet or module_config_dict.sand_box_meet or ""
sand_box_receivable = main_config_dict.sand_box_receivable or module_config_dict.sand_box_receivable or ""


class EnrollServices:
    def __init__(self):
        pass

    @staticmethod
    def enroll_add(params, is_valuate=False, subitem=None):
        """
        报名表新增
        :param params:
        :param is_valuate: 是否使用计价，False直接使用传过来的值
        :return: data,err
        """
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "user_id", "category_id", "trading_relate", "region_code", "occupy_room",
                "enroll_status_code", "enroll_status_code_id",
                "min_number", "max_number", "min_count_apiece", "max_count_apiece", "enroll_rule_group_id",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount",
                "paid_amount", "unpaid_amount", "commision", "deposit",
                "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit",
                "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time",
                "create_time", "update_time", "snapshot", "remark",
            ],
        )
        if is_valuate:
            pass

        try:
            instance = Enroll.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return instance.to_json(), None

    @staticmethod
    def enroll_detail(enroll_id, simple_return=False):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, "不存的报名信息"
        enroll_detail = enroll_obj.first().to_json()

        # 是否输出联表数据
        if not simple_return:
            # 报名倒计时
            clocker = ClockService()
            data, err = clocker.check_clock(enroll_id)
            enroll_detail.update(data)

            # 获取需要拼接的数据，报名分项，报名记录，报名分项记录
            enroll_subitems_record_list = list(
                EnrollSubitemRecord.objects.filter(enroll_subitem__enroll_id=enroll_id).values())
            # enroll_subitems_record_list = EnrollSubitemRecordSerializer(EnrollSubitemRecord.objects.filter(enroll_subitem__enroll_id=enroll_id), many=True).data
            main_record_list = EnrollRecordListSerializer(EnrollRecord.objects.filter(enroll_id=enroll_id),
                                                          many=True).data

            enroll_subitems_list = list(EnrollSubitem.objects.annotate(category_id=F("enroll__category_id")).filter(
                enroll_id=enroll_id).values())
            enroll_subitems_list = output_convert(enroll_subitems_list)  # 进行扩展字段转换

            # 建立映射
            record_id_to_subitems_record_map = {}
            for enroll_subitems_record in enroll_subitems_record_list:
                this_subitems_record = record_id_to_subitems_record_map.get(enroll_subitems_record["enroll_record_id"],
                                                                            None)
                if not this_subitems_record:
                    record_id_to_subitems_record_map[enroll_subitems_record["enroll_record_id"]] = [
                        enroll_subitems_record]
                    continue
                this_subitems_record.append(enroll_subitems_record)

            subitems_id_to_subitem_record_map = {}
            for enroll_subitems_record in enroll_subitems_record_list:
                this_subitems_record = subitems_id_to_subitem_record_map.get(
                    enroll_subitems_record["enroll_subitem_id"], None)
                if not this_subitems_record:
                    subitems_id_to_subitem_record_map[enroll_subitems_record["enroll_subitem_id"]] = [
                        enroll_subitems_record]
                    continue
                this_subitems_record.append(enroll_subitems_record)

            # print("record_id_to_subitems_record_id_map", record_id_to_subitems_record_id_map)
            # print("subitems_id_to_subitems_record_map", subitems_id_to_subitems_record_map)

            # 数据拼接
            for main_record in main_record_list:
                main_record["subitem_record_list"] = record_id_to_subitems_record_map.get(main_record["id"], {})

            for enroll_subitem in enroll_subitems_list:
                enroll_subitem["subitem_record_list"] = subitems_id_to_subitem_record_map.get(enroll_subitem["id"], {})

            enroll_detail["subitem_list"] = enroll_subitems_list
            enroll_detail["main_record_list"] = main_record_list

        return enroll_detail, None

    @staticmethod
    def enroll_list(params, filter_fields=None, need_pagination=True):
        # 字段处理
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        filter_fields_list = filter_fields.split(";") if filter_fields else []
        params['enroll_status_code'] = params['enroll_status_code'].split(";") if params.get(
            "enroll_status_code") else None
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "thread_id", "category_id", "thread_id_list", "trading_relate", "region_code", "spend_time_start",
                "enroll_status_code",
                "spend_time_end", "create_time_start", "create_time_end", "finish_time_start", "finish_time_end",
                "open_time_start", "open_time_end", "enroll_status_code", "has_subitem"
            ],
            alias_dict={
                "spend_time_start": "spend_time__gte", "spend_time_end": "spend_time__lte",
                "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "finish_time_start": "finish_time__gte", "open_time_start": "open_time__gte",
                "open_time_end": "open_time__lte", "enroll_classify_value": "classify__value",
                "enroll_category_value": "category__value", "enroll_status_code": "enroll_status_code__in",
                "thread_id_list": "thread_id__in"
            }
        )
        enroll_obj = Enroll.objects.filter(**params).order_by("-id").values(*filter_fields_list)
        if not need_pagination:
            return list(enroll_obj), None

        # 分页展示
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_own_list(params, need_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params['enroll_status_code'] = params['enroll_status_code'].split(";") if params.get(
            "enroll_status_code") else None
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id", "thread_id", "user_id", "enroll_pay_status", "enroll_status_code", "price", "count",
                "amount",
            ],
            alias_dict={"enroll_id": "id", "enroll_status_code": "enroll_status_code__in", }
        )
        enroll_obj = Enroll.objects.filter(**params).order_by("-id").values()
        if not need_pagination:
            # serializer = EnrollRecordListSerializer(data=enroll_obj)
            # serializer.is_valid()
            return list(enroll_obj.object_list), None

        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_undertake_list(params, need_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params['enroll_status_code'] = params['enroll_status_code'].split(";") if params.get(
            "enroll_status_code") else None
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id", "user_id", "enroll_pay_status", "enroll_status_code", "price", "count", "amount",
            ],
            alias_dict={"enroll_status_code": "enroll_status_code__in", }
        )
        enroll_obj = EnrollRecord.objects.annotate(commision=F("enroll__commision")).annotate(thread_id=F("enroll__thread_id")).filter(**params).order_by(
            "-id").values()
        if not need_pagination:
            # serializer = EnrollRecordListSerializer(data=enroll_obj)
            # serializer.is_valid()
            return list(enroll_obj.object_list), None

        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        # serializer = EnrollRecordListSerializer(enroll_obj, many=True)
        # print(serializer.data)
        # print(list(enroll_obj.object_list))
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_edit(params=None, enroll_id=None, search_param=None):
        if not enroll_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"
        enroll_id = params.pop("enroll_id", None) or enroll_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "category_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code",
                "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount",
                "paid_amount", "unpaid_amount", "commision", "deposit",
                "bid_mode", "ticket", "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch",
                "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time",
                "create_time", "update_time", "snapshot", "remark",
            ],
        )
        enroll_obj = Enroll.objects
        if enroll_id:
            enroll_obj = enroll_obj.filter(id=enroll_id)
        if search_param:
            enroll_obj = enroll_obj.filter(**search_param)
        if not enroll_obj:
            return None, None

        try:
            enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return enroll_obj.first().to_json(), None

    @staticmethod
    def enroll_delete(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def enroll(request_params=None):
        """报名记录联合添加报名记录和分项记录"""
        sid = transaction.savepoint()
        # 信息主表
        main_record_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=[
                "id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code",
                "create_time", "price", "deposit", "count",
                "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
                "paid_amount", "unpaid_amount", "fee", "photos",
                "files", "score", "reply", "remark",
            ]
        )
        main_data, err = EnrollRecordServices.record_add(main_record_params)
        if err:
            transaction.savepoint_rollback(sid)
            return None, err

        # 分项表
        subitem_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["enroll_record_id", "enroll_subitem_id", "user_id", "subitem_price", "subitem_count",
                               "subitem_amount", ],
            alias_dict={"subitem_price": "price", "subitem_count": "count"}
        )

        enroll_record_id = main_data.get("id", None)
        if not enroll_record_id:
            transaction.savepoint_rollback(sid)
            return None, err
        subitem_params["enroll_record_id"] = enroll_record_id

        subitem_data, err = EnrollSubitemRecordService.add(subitem_params)
        if err:
            transaction.savepoint_rollback(sid)
            return None, err

        # 添加定时器
        clocker = ClockService()
        clocker.add_clock(enroll_id=request_params.get("enroll_id"), user_id=request_params.get("user_id"))
        transaction.clean_savepoints()
        return None, err

    @staticmethod
    def pay_call_back(order_no):
        """
        回调逻辑：
        1.用户支付分为两种：（1）用户支付预付款 （2）用户补差价
        情况1：支付预付款，但是还没有成单。修改状态进入代报名状态。
        情况2：（报名并指派后）用户支付差价，订单开始。进入上传状态。
        扩展逻辑：分销逻辑，资金逻辑。
        :param order_no: 订单号
        :return: response
        """
        finance_transact_data, err = FinanceTransactsService.detail(order_no=order_no)
        if err:
            return None, err
        try:
            user_id = finance_transact_data.get("account_id", None)
            enroll_id = finance_transact_data.get("enroll_id", None)
            outgo = finance_transact_data.get("outgo", 0)
            # print("支付回调报名", "user_id:", user_id, "enroll_id:", enroll_id, "order_no", order_no)
            enroll_obj = Enroll.objects.filter(id=enroll_id, user_id=user_id)
            enroll_set = enroll_obj.first()
            if not enroll_set:
                return None, None
            paid_amount = (enroll_set.paid_amount or 0) + (outgo or 0)
            # print(paid_amount, enroll_set.enroll_status_code)
            if int(enroll_set.enroll_status_code) == 243:
                enroll_obj.update(paid_amount=paid_amount, unpaid_amount=0, enroll_status_code=356)
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=356)
            else:
                enroll_obj.update(paid_amount=paid_amount, unpaid_amount=0, enroll_status_code=43)
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=43)
            # EnrollRecord.objects.filter(enroll_id=enroll_id).update(enroll_status_code=43)

            # 写入资金沙盒
            pass
            return None, None
        except Exception as e:
            return None, e
