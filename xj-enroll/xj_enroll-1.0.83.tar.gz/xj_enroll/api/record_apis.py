from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..service.enroll_record_serivce import EnrollRecordServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data
from ..utils.join_list import JoinList


class RecordAPI(APIView):
    # 添加记录,用户报名
    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    def add(self, *args, user_info=None, **kwargs, ):
        # 表单数据验证
        # is_valid, error = RecordValidator(params).validate()
        # if not is_valid:
        #     return util_response(err=1000, msg=error)

        # 提取参数
        params = parse_data(self) or {}
        params['user_id'] = user_info.get("user_id")

        # 判断是否科技继续报名
        enroll_id = params.get("enroll_id")
        user_id = params.get("user_id")
        if not enroll_id:
            return util_response(err=1000, msg="enroll_id不能为空")

        # 查看是否符合报名条件
        if not EnrollRecordServices.check_can_add(enroll_id, user_id):
            return util_response(err=1001, msg="当前报名已经报满，或者您已经报名了")

        # 添加数据
        data, err = EnrollRecordServices.record_add(params)
        if err:
            return util_response(err=1002, msg=err)

        # 报名触发倒计时,取消自动成单
        # clocker = ClockService()
        # data, err = clocker.add_clock(enroll_id, user_id)
        return util_response(data={"id": data.get("id")})

    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        need_pagination = params.get("need_pagination", 0)
        need_pagination = int(need_pagination)
        data, err = EnrollRecordServices.record_list(params=params, need_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=err)
        user_ids = []
        if need_pagination:
            for i in data["list"]:
                i["fee"] = round(i["fee"], 2)
                i["price"] = round(i["price"], 2)
                i["amount"] = round(i["amount"], 2)
                i["deposit_amount"] = round(i["deposit_amount"], 2)
                i["coupon_amount"] = round(i["coupon_amount"], 2)
                i["again_reduction"] = round(i["again_reduction"], 2)
                i["subitems_amount"] = round(i["subitems_amount"], 2)
                i["paid_amount"] = round(i["paid_amount"], 2)
                i["unpaid_amount"] = round(i["unpaid_amount"], 2)
                i["main_amount"] = round(i["main_amount"], 2)
                i["deposit"] = round(i["deposit"], 2)
                i["count"] = round(i["count"], 0)
                user_ids.append(i["user_id"])
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data["list"] = JoinList(data["list"], user_infos, "user_id", "user_id").join()
        else:
            for i in data:
                i["fee"] = round(i["fee"], 2)
                i["price"] = round(i["price"], 2)
                i["amount"] = round(i["amount"], 2)
                i["deposit_amount"] = round(i["deposit_amount"], 2)
                i["coupon_amount"] = round(i["coupon_amount"], 2)
                i["again_reduction"] = round(i["again_reduction"], 2)
                i["subitems_amount"] = round(i["subitems_amount"], 2)
                i["paid_amount"] = round(i["paid_amount"], 2)
                i["unpaid_amount"] = round(i["unpaid_amount"], 2)
                i["main_amount"] = round(i["main_amount"], 2)
                i["deposit"] = round(i["deposit"], 2)
                i["count"] = round(i["count"], 0)
                user_ids.append(i["user_id"])
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data = JoinList(data, user_infos, "user_id", "user_id").join()

        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def record_del(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_del(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def record_edit(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_edit(params, pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def record_detail(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk", None) or params.pop("id", None) or params.pop("record_id", None) or None
        if not pk:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollRecordServices.record_detail(pk, search_params=params)

        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    @user_authentication_force_wrapper
    def appoint(self, *args, user_info=None, **kwargs, ):
        """
        需求描述：报名可多人报名，不在自动成单，可以手动指派报名
        1.由用户或者客服进行指派工作人员完成任务。
        2.没有被选中的用户，报名状态修改成草稿状态。
        3.主报名项目，则进入代补差价状态。
        :return: response
        """
        params = parse_data(self)
        enroll_id = params.get("enroll_id", None)
        record_id = params.get("record_id", None)
        subitem_id = params.get("subitem_id", None)
        if enroll_id is None or record_id is None or subitem_id is None:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollRecordServices.appoint(enroll_id, record_id, subitem_id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data, msg="指派成功")
