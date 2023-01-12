# encoding: utf-8
"""
@project: djangoModel->enroll_validator
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名验证器
@created_time: 2022/9/17 15:50
"""

from django import forms

from ..utils.validator import Validator


class RecordValidator(Validator):
    enroll_id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "enroll_id 必填 必填",
        },
    )

    # 报名开始与截至时间
    user_id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "user_id 必填 必填",
        },
    )
