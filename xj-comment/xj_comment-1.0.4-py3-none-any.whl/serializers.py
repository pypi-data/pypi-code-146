"""
Created on 2022-05-01
@author:刘飞
@description:评论模块序列化器
"""
from rest_framework import serializers
from apps.comment.models import *


class CommentListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = CommentAbstract
        fields = '__all__'
