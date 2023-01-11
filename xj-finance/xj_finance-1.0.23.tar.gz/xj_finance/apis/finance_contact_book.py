# _*_coding:utf-8_*_

import os, logging, time, json, copy
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import response
from rest_framework import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from django.db.models import F

from xj_finance.models import *
from xj_user.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserContactBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInfo
        fields = [
            'id',
            'full_name',
        ]


# 获取平台列表
class UserContactBook(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserContactBookSerializer

    def get(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return Response({'err': 4001, 'msg': '缺少Token', })

        user_service, error_text = UserService.check_token(token)
        if error_text:
            return Response({'err': 4002, 'msg': error_text, })

        user_id = user_service.get('user_id', None)
        if not user_id:
            return Response({'err': 4003, 'msg': '用户不存在', })

        print(">>> user_id ", user_id)
        their_account_id_set = Transact.objects.filter(account_id=user_id).values('their_account_id').distinct()
        their_account_id_list = list(their_account_id_set)
        # print(">>> their_account_id_list ", their_account_id_list)
        full_name_list = []
        for i in range(len(their_account_id_list)):
            # print(">>> ", i, their_account_id_list[i]['their_account_id'])
            full_name_set = BaseInfo.objects.filter(id=their_account_id_list[i]['their_account_id']).values('id', 'full_name')
            # print(">>> full_name_set ", full_name_set)
            print(">>> list(full_name_set) ", list(full_name_set))
            full_name_list.append({
                'id': list(full_name_set)[0]['id'],
                'full_name': list(full_name_set)[0]['full_name'],
            })
            # full_name_list = list(full_name_set)
        print(">>> full_name_list ", full_name_list)

        user_base_info_list = BaseInfo.objects.all()
        # print(">>> user_base_info_list", user_base_info_list)
        serializer = UserContactBookSerializer(user_base_info_list, many=True)
        return Response({
            'err': 0,
            'msg': 'OK',
            # 'data': serializer.data,
            'data': full_name_list,
        })