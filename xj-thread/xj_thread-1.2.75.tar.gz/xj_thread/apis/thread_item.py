"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块单挑数据删除/修改/详情
"""
from rest_framework.views import APIView

from xj_enroll.service.enroll_services import EnrollServices
from ..services.thread_item_service import ThreadItemService
from ..utils.custom_authentication_wrapper import authentication_wrapper
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data

item_service = ThreadItemService()


class ThreadItemAPI(APIView):
    """单挑信息处理，查，改，删"""

    def get(self, request, pk, *args, **kwargs):
        """信息表详情"""
        if not pk:
            return util_response(msg="非法请求", err=2554)
        data, error_text = item_service.detail(pk)

        if not error_text:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)

    @authentication_wrapper
    def put(self, request, pk, *args, **kwargs):
        """信息表编辑"""
        if not pk:
            return util_response(msg="非法请求", err=1000)
        form_data = parse_data(request=request)
        data, error_text = item_service.edit(form_data, pk)

        # 报名表同步修改category_id
        category_id = form_data.get("category_id", None)
        if category_id:
            data, err = EnrollServices.enroll_edit({"category_id": category_id}, enroll_id=None, search_param={"thread_id": pk})
            if err:
                print("err:", err)
            #     return util_response(err=1001, msg=err)

        if not error_text:
            return util_response()
        return util_response(err=1002, msg=error_text)

    @authentication_wrapper
    def delete(self, request, pk, *args, **kwargs):
        data, error_text = item_service.delete(pk)
        print(error_text)
        if not error_text:
            return util_response()
        return util_response(err=47767, msg=error_text)
