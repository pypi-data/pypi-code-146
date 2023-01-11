# encoding: utf-8
"""
@project: djangoModel->export_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 导出AOIView
@created_time: 2022/11/23 18:03
"""
import datetime

from rest_framework.views import APIView

from main.settings import MEDIA_ROOT
from xj_user.services.user_detail_info_service import DetailInfoService
from ..services.doc_export_service import DocExportService, TEMPLET_PATH_MAP
from ..services.excel_export_service import ExcelExport
from ..utils.custom_response import doc_response, excel_response, util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_wrapper


class exportAPIView(APIView):

    @user_authentication_wrapper
    @request_params_wrapper
    def doc_export(self, *args, request_params=None, user_info=None, **kwargs):
        if request_params is None:
            request_params = {}
        if user_info is None:
            user_info = {}

        templet_path_name = request_params.pop("templet_path_name", None)
        if templet_path_name is None or TEMPLET_PATH_MAP.get(templet_path_name, None) is None:
            return util_response(err=1000, msg="找不到导出模板")

        # print("request_params", request_params, "user_info:", user_info)
        user_id = user_info.get("user_id", None) or request_params.get("user_id", None)
        if user_id is None:
            return util_response(err=1001, msg="找不到用户信息")
        user_detail_info, detail_err = DetailInfoService.get_detail(user_id)
        if not detail_err is None:
            return util_response(err=1002, msg=detail_err)
        request_params.update(user_detail_info)
        today = datetime.date.today()
        request_params.update({"current_date": today.strftime('%Y-%m-%d')})
        # print("request_params:", request_params)
        data, export_err = DocExportService.export(request_params, templet_path=TEMPLET_PATH_MAP.get(templet_path_name))
        if not export_err is None:
            return util_response(err=1003, msg=export_err)
        return doc_response(data)

    @request_params_wrapper
    def  excel_export(self, request_params, *args, **kwargs):
        templet_path = MEDIA_ROOT + "/templet/test.xls"
        print(templet_path)
        print("request_params", request_params)
        export_instance = ExcelExport(excel_templet_path=templet_path)
        # 写入
        data, err = export_instance.additional_write(input_dict=[request_params])
        # 保存
        excel_data, err = export_instance.save(workbook=export_instance.additional_write_wb)
        return excel_response(excel_data)
