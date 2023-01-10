# _*_coding:utf-8_*_

import logging

from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import BaseInfo, ContactBook
# from apps.finance.models import *
from ..services.contact_book import ContactBookService
from ..services.user_service import UserService

logger = logging.getLogger(__name__)


class UserContactBookSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = BaseInfo
    #     fields = [
    #         'id',
    #         'full_name',
    #     ]
    class Meta:
        model = ContactBook
        fields = [
            'friend_id',
        ]


# 获取通讯录列表
class UserContactBook(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserContactBookSerializer

    def get(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        self.params = request.data
        if not token:
            return Response({'err': 4001, 'msg': '缺少Token', })

        user_serv, error_text = UserService.check_token(token)
        if error_text:
            return Response({'err': 4001, 'msg': error_text, })
        user_id = user_serv.get('user_id', '')
        if not user_id:
            return Response({'err': 4002, 'msg': 'token验证失败', })

        # user_base_info_list = BaseInfo.objects.all()
        # serializer = UserContactBookSerializer(user_base_info_list, many=True)
        find_user_id = self.params.get('user_id', '')
        if not find_user_id:
            find_user_id = user_id
        list = ContactBookService.get_list(self, find_user_id)
        return list

    def post(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        self.params = request.data
        if not token:
            return Response({'err': 4001, 'msg': '缺少Token', })

        user_id = UserService.check_token(token)
        if not user_id:
            return Response({'err': 4002, 'msg': 'token验证失败', })

        user_id = self.params.get('user_id', '')
        friend_id = self.params.get('friend_id', '')
        remarks = self.params.get('remarks', '')
        data = {
            'user_id': user_id,
            'friend_id': friend_id,
            'remarks': remarks
        }

        add = ContactBookService.add_friends(self, data)
        return add
        # list = ContactBookService.get_list(self, user_id)
        # return list
