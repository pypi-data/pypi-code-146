# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators


class BaseModelTimeAndDeleted(models.Model):
    '''基础 model'''
    created_time = models.DateTimeField("Date Created", blank=True, null=True, auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", blank=True, null=True, auto_now=True)
    deleted = models.BooleanField("已删除", default=False)

    class Meta:
        abstract = True


class BaseModelNew(models.Model):
    '''基础 model'''
    deleted = models.BooleanField("已删除", default=False)

    class Meta:
        abstract = True


class AbstractAddress(models.Model):

    PHONE_NUMBER_REGEX = r"1[0-9]{10}"

    title = models.CharField(
        '地址名称',
        max_length=64,
        # choices=TITLE_CHOICES,
        blank=True
    )
    name = models.CharField(
        '姓名',
        max_length=64,
        blank=True
    )
    phone = models.CharField(
        '收件人手机号',
        max_length=11,
        unique=False,
        help_text='请输入手机号',
        validators=[
            validators.RegexValidator(
                PHONE_NUMBER_REGEX,
                '手机号输入有误，请重新输入',
            ),
        ],
    )
    province = models.CharField(
        '省',
        max_length=64,
        blank=True
    )
    city = models.CharField(
        '城市',
        max_length=255,
        # choices=TITLE_CHOICES,
        blank=True
    )
    district = models.CharField(
        '区县',
        max_length=255,
        # choices=TITLE_CHOICES,
        blank=True
    )
    detail = models.CharField(
        '地址详情',
        max_length=255,
        # choices=TITLE_CHOICES,
        blank=True
    )

    def __str__(self):
        return '{0}-{1}-{2}{3}{4}{5}'.format(self.name, self.phone, self.province, self.city, self.district, self.detail)

    class Meta:
        abstract = True
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
