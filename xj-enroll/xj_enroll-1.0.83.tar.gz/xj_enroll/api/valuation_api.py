# encoding: utf-8
"""
@project: djangoModel->valuation_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/10/13 11:22
"""
from rest_framework.views import APIView

from ..service.valuation_service import ValuationService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class ValuationAPIView(APIView):
    # 获取计价 测试接口
    @request_params_wrapper
    def valuate_test(self, *args, request_params, **kwargs):
        expression_string = request_params.get("expression", "5+if(((IF(1=5,5,0)+((3)))>=(1+3+4)),'号外号外',IF(2 >= 60, '及格', '不及格')) + SUM(1,2,5,7,8)", )
        variables_dict = request_params.get("variables", {"a": 1, "b": 2, "c": 5}, )
        data, err = ValuationService.valuate_test(
            expression_string,
            variables_dict
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 计价预处理
    @request_params_wrapper
    def valuate(self, *args, request_params, **kwargs):
        category_id = request_params.pop("category_id", None)
        classify_id = request_params.pop("classify_id", None)
        variables_dict = request_params
        if not category_id or not classify_id or not variables_dict:
            return util_response(err=1000, msg="参数错误:category_id|classify_id必传")
        data, err = ValuationService.valuate(category_id, classify_id, variables_dict)

        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    def valuation_detailed_list(self, *args, **kwargs):
        enroll_id = kwargs.get("enroll_id", None)
        if not enroll_id:
            return util_response(err=1000, msg="enroll_id 不能为空，请检查路由")
        data, err = ValuationService.valuation_detailed_list(enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
