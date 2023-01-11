"""
Created on 2022-05-19
@author:刘飞
@description:报名模块序列化器
"""
from rest_framework import serializers

from .models import *


class EnrollListSerializer(serializers.ModelSerializer):
    """
    报名表序列化器
    """

    class Meta:
        model = Enroll
        fields = '__all__'


class EnrollRecordListSerializer(serializers.ModelSerializer):
    """
    报名记录列表序列化器
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    deposit = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()
    main_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupon_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    again_reduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    subitems_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    unpaid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = EnrollRecord
        fields = '__all__'


class EnrollSubitemRecordSerializer(serializers.ModelSerializer):
    """
    报名记录列表序列化器
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    subitem_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()

    class Meta:
        model = EnrollSubitemRecord
        fields = '__all__'


class EnrollSubitemSerializer(serializers.ModelSerializer):
    """
    报名记录列表序列化器
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()

    class Meta:
        model = EnrollSubitem
        fields = '__all__'
