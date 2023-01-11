from django.db import transaction
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_user.utils.user_wrapper import user_authentication_wrapper
from ..service.subitem_service import SubitemService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class SubitemApis(APIView):

    @require_http_methods(['GET'])
    @user_authentication_wrapper
    def list(self, *args, user_info=None, **kwargs):
        request_params = parse_data(self)
        request_params["user_id"] = user_info.get("user_id", None)
        need_pagination = request_params.get("need_pagination", 1)
        need_pagination = int(need_pagination)
        data, err = SubitemService.list(params=request_params, is_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def detail(self, *args, **kwargs, ):
        request_params = parse_data(self)
        pk = kwargs.get("pk") or request_params.get("id") or request_params.get("subitem_id")
        if not pk:
            return util_response(err=1000, msg="参数错误")
        data, err = SubitemService.detail(pk=pk)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = SubitemService.add(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def batch_add(self, *args, **kwargs, ):
        """批量添加报名分项"""
        params_list = parse_data(self)
        if not isinstance(params_list, list) or not params_list:
            return util_response(err=1000, msg="应该传[{},{},....]")

        sid = transaction.savepoint()
        try:
            for params in params_list:
                enroll_id = params.get("enroll_id", None)
                if not enroll_id:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1001, msg="enroll_id 必传")
                is_can_add = SubitemService.check_num(enroll_id)
                if not is_can_add:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1002, msg="超出需求份数，或者enroll_id 不存在。")
                data, err = SubitemService.add(params)
                if err:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1000, msg=err)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return util_response(err=1000, msg=str(e))

        # 清除mysql事务点
        transaction.clean_savepoints()
        return util_response()

    @require_http_methods(['PUT'])
    def batch_edit(self, *args, **kwargs, ):
        """批量添加报名分项"""
        params_list = parse_data(self)
        if not isinstance(params_list, list) or not params_list:
            return util_response(err=1000, msg="应该传[{},{},....]")

        sid = transaction.savepoint()
        try:
            for params in params_list:
                enroll_id = params.get("enroll_id", None)
                if not enroll_id:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1001, msg="enroll_id 必传")
                data, err = SubitemService.edit(params)
                if err:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1000, msg=err)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return util_response(err=1000, msg=str(e))

        # 清除mysql事务点
        transaction.clean_savepoints()
        return util_response()

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
        data, err = SubitemService.edit(params, subitem_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit_by_enroll_id(self, *args, **kwargs, ):
        params = parse_data(self)
        enroll_id = params.pop("id", None) or kwargs.pop("enroll_id", None)
        data, err = SubitemService.batch_edit(params, enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # @require_http_methods(['DELETE'])
    # def delete(self, *args, **kwargs, ):
    #     params = parse_data(self)
    #     subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
    #     data, err = SubitemService.delete(params, subitem_id)
    #     if err:
    #         return util_response(err=1000, msg=err)
    #     return util_response(data=data)

    @require_http_methods(['GET'])
    def extend_field(self, *args, **kwargs, ):
        request_params = parse_data(self)
        need_pagination = request_params.get("need_pagination", 0)
        need_pagination = int(need_pagination)
        data, err = SubitemService.extend_field(params=request_params, is_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
