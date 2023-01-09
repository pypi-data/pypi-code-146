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


class CommentAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentAPIView(APIView):
    permission_classes = (AllowAny,)
    params = None

    def get(self, request, format=None):
        self.params = request.query_params  # 返回QueryDict类型

        page = int(self.params['page']) - 1 if 'page' in self.params else 0
        size = int(self.params['size']) if 'size' in self.params else 10

        print(">>>page", page)
        print(">>>size", size)

        comments = Comment.objects.all()\
            # .filter(Q(account=self.params['uid']) | Q(their_account=self.params['id'])).order_by('id')
        total = comments.count()
        now_pages = comments[page * size:page * size + size] if page >= 0 else comments
        data = now_pages.annotate(
            username = F('user__username'),
        ).values(
            'id',
            'thread',
            'user',
            'create_time',
            'message',
            'by_comment_id',
            'weight',
            'likes',
            'comments',
            'favorite',
            'shares',
        )

        return Response({
            'err': 0,
            'msg': 'OK',
            'data': {'total': total, 'list': data, },
            'request': self.params,
            # 'serializer': serializer.data,
        })

    def post(self, request):
        self.params = request.query_params

        return Response({
            'err': 0,
            'msg': 'OK',
            'data': {},
            'request': self.params,
        })