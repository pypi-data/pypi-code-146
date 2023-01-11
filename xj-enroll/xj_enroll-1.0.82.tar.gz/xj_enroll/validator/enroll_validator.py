# encoding: utf-8
"""
@project: djangoModel->enroll_validator
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名验证器
@created_time: 2022/9/17 15:50
"""

from django import forms
from django.core.exceptions import ValidationError

from xj_thread.services.thread_item_service import ThreadItemService
from ..utils.validator import Validator


class EnrollValidator(Validator):
    # 信息ID验证
    def clean_thread_id(self):
        cleaned_data = super().clean()
        thread_id = cleaned_data.get('thread_id')
        data, err = ThreadItemService.detail(thread_id)
        if err:
            raise ValidationError('不存在该信息，请重新选择')

    # 报名截至时间验证
    def clean_close_time(self):
        cleaned_data = super().clean()
        open_time = cleaned_data.get('open_time')
        close_time = cleaned_data.get('close_time')
        if not open_time < close_time:
            raise forms.ValidationError('报名截至时间必须大于报名开始时间')

    # 报名截至时间验证
    def clean_finish_time(self):
        cleaned_data = super().clean()
        launch_time = cleaned_data.get('launch_time')
        finish_time = cleaned_data.get('finish_time')
        if not launch_time < finish_time:
            raise forms.ValidationError('报名截至时间必须大于报名开始时间')

    # ====================== 验证 =============================

    thread_id = forms.CharField(
        required=True,
        error_messages={
            "required": "信息ID必填 必填",
        },
    )

    # 报名开始与截至时间
    open_time = forms.DateTimeField(
        required=True,
        error_messages={
            "required": "open_time 必填 必填",
        },
    )
    close_time = forms.DateTimeField(
        required=True,
        error_messages={
            "required": "open_time 必填 必填",
        },
    )

    # 活动开始与截至时间
    launch_time = forms.CharField(
        required=True,
        error_messages={
            "required": "launch_time 必填 必填",
        },
    )
    finish_time = forms.CharField(
        required=True,
        error_messages={
            "required": "finish_time 必填 必填",
        },
    )

    # 报名人数西安至
    min_number = forms.IntegerField(
        required=True,
        error_messages={
            "required": "min_number 必填 必填",
        },
    )
    max_number = forms.IntegerField(
        required=True,
        error_messages={
            "required": "max_number 必填 必填",
        },
    )
