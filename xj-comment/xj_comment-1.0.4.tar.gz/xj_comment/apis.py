"""
Created on 2022-05-01
@author:刘飞
@description:评论模块逻辑分发
"""
from rest_framework.views import APIView
from .services import CommentServices
from utils.custom_authorization import Authentication
from xj_user.utils.custom_authorization import CustomAuthentication
from utils.custom_authentication_wrapper import authentication_wrapper
from utils.custom_response import util_response

c = CommentServices()


class CommentListView(APIView):
    """
    get:评论列表
    post:评论新增
    """

    # authentication_classes = (CustomAuthentication,)

    def get(self, request):
        data, error_text = c.comment_list_read(request)
        return util_response(data=data)

    @authentication_wrapper
    def post(self, request):
        data, error_text = c.comment_list_create(request)
        return util_response(data=data)


class CommentDetailView(APIView):
    """
    delete:评论删除
    """
    authentication_classes = (CustomAuthentication,)

    def delete(self, request, pk):
        data, error_text = c.comment_detail(request, pk)
        return util_response(data=data)
