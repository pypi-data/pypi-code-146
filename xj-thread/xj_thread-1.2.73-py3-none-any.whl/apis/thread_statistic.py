# encoding: utf-8
"""
@project: djangoModel->thread_static
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 统计接口
@created_time: 2022/8/8 10:05
"""

# 计数统计
from rest_framework.views import APIView

from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class ThreadStaticAPIView(APIView):

    # 统计列表
    def get(self, request):
        params = parse_data(request)
        data, err_txt = StatisticsService.statistic_list(params)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    # 单条自增
    def post(self, request):
        thread_id = request.data.get('thread_id', None)
        tag = request.data.get('tag', None)
        step = request.data.get('step', None)
        tag_list = ['step', 'views', 'plays', 'comments', 'likes', 'favorite', 'shares']
        if not thread_id or not tag in tag_list:
            return util_response(err=45767, msg='参数错误')
        data, err_txt = StatisticsService.increment(thread_id, tag, step)
        if err_txt == 0:
            return util_response()
        return util_response(err=47767, msg=err_txt)

    # 多字段自增
    def put(self, request):
        form_data = parse_data(request)
        thread_id = form_data.pop('thread_id', None)
        if thread_id is None:
            return util_response(msg="参数错误", err=57766)
        data, err_txt = StatisticsService.increments(thread_id, form_data)
        if err_txt == 0:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
