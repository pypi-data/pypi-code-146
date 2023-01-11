from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.db.models import F
import json

from django.http import JsonResponse
# Create your views here.


class FinanceAPISerializer(serializers.ModelSerializer):   # 继承自ModelSerializer类
    """ 序列化数据的类，根据model表来获取字段 """
    class Meta:
        model = Transact
        fields = '__all__'


class FinanceListAPIView(APIView):
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户
    params = None

    def get(self, request, format=None):
        self.params = request.query_params  # 返回QueryDict类型

        if 'uid' not in self.params or self.params['uid'].isspace():
            return Response({'err': 0, 'msg': '缺少uid', 'data': [], 'request': self.params, })

        page = int(self.params['page']) - 1 if 'page' in self.params else 0
        size = int(self.params['size']) if 'size' in self.params else 10

        """ Return a list of all users. """
        transacts = Transact.objects.all().filter(Q(account=self.params['uid']) | Q(their_account=self.params['uid'])).order_by('transact_time')
        total = transacts.count()
        now_pages = transacts[page*size:page*size+size] if page >= 0 else transacts
        data = now_pages.annotate(
            self_name=F('account__full_name'),
            their_name=F('their_account__full_name'),
            time=F('transact_time'),
            platform_name=F('platform__platform_name'),
            currency_name=F('currency__currency'),
            payment=F('pay_mode__pay_mode'),
            order_id=F('platform_order_id'),
        ).values(
            'id',
            'transact_id',
            'self_name',
            'their_name',
            'time',
            'platform_name',
            'order_id',
            'opposite_account',
            'summary',
            'currency_name',
            'income',
            'outgo',
            'balance',
            'payment',
        )

        serializer = FinanceAPISerializer(transacts, many=True)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': {'total': total, 'list': data, },
            'request': self.params,
            # 'serializer': serializer.data,
        })

        # m_transacts = Transact.objects.values()
        # m_result_transacts = {}
        # m_result_transacts['list'] = list(m_transacts)
        #
        # m_BaseInfo = BaseInfo.objects.values()
        # m_result = {}
        # m_result['list'] = list(m_BaseInfo)

        # return Response({'err': 0, 'msg': 'OK', 'data': serializer.data, 'm_result': m_result, 'm_result_transacts': m_result_transacts})

        # transacts = Transact.objects.all().values()
        # data = {}
        # data['list'] = list(transacts)
        #
        # # return JsonResponse(data)

    def post(self, request):
        self.params = request.query_params

        return Response({
            'err': 0,
            'msg': 'OK',
            'data': {},
            'request': self.params,
        })
