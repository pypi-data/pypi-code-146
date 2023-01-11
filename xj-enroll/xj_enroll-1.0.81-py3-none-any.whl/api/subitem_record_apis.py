from django.db import transaction
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_user.utils.user_wrapper import user_authentication_wrapper, user_authentication_force_wrapper
from ..service.enroll_subitem_record_service import EnrollSubitemRecordService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class SubitemRecordApis(APIView):

    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    def add(self, *args, user_info=None, **kwargs, ):
        params = parse_data(self)
        params["user_id"] = user_info.get("user_id")
        data, err = EnrollSubitemRecordService.add(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    def batch_add(self, *args, user_info=None, **kwargs, ):
        sid = transaction.savepoint()
        params = parse_data(self)
        try:
            for param in params:
                data, err = EnrollSubitemRecordService.add(param)
                if err:
                    transaction.savepoint_rollback(sid)
                    return util_response(err=1000, msg=err)

            transaction.clean_savepoints()
            return util_response()
        except Exception as e:
            return util_response(msg=str(e))

    @require_http_methods(['GET'])
    @user_authentication_wrapper
    def list(self, *args, **kwargs, ):
        request_params = parse_data(self)
        need_pagination = request_params.get("need_pagination", 0)
        need_pagination = int(need_pagination)
        data, err = EnrollSubitemRecordService.list(params=request_params, need_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=data)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
        data, err = EnrollSubitemRecordService.edit(params, subitem_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def delete(self, *args, **kwargs, ):
        params = parse_data(self)
        pk = params.pop("id", None) or kwargs.pop("pk", None)
        data, err = EnrollSubitemRecordService.delete(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
