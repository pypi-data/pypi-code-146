"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""
from rest_framework.response import Response
from rest_framework.views import APIView

# from xj_user.utils.custom_authorization import CustomAuthentication
from ..services.thread_classify_tree_service import ThreadClassifyTreeServices
from ..utils.custom_tool import parse_data


# from ..utils.custom_authentication_wrapper import authentication_wrapper


class ThreadClassifyTreeAPIView(APIView):
    """
    get: 信息表列表
    post: 信息表新增
    """

    def get(self, request, classify_value=None, *args, **kwargs):
        params = parse_data(request)
        # print("> ThreadclassifyTreeAPIView params classify_value:", params, classify_value)
        classify_value = classify_value if classify_value else params.get('classify_value', None)
        classify_id = params.get('classify_id', None)
        # print("> ThreadclassifyTreeAPIView classify_value, classify_id:", classify_value, classify_id)
        if classify_value or classify_id:
            classify_serv, error_text = ThreadClassifyTreeServices.get_classify_tree(classify_id=classify_id, classify_value=classify_value)
        else:
            classify_serv, error_text = ThreadClassifyTreeServices.get_classify_all_tree()

        if error_text:
            return Response({'err': 1000, 'msg': error_text})

        return Response({'err': 0, 'msg': 'OK', 'data': classify_serv})
