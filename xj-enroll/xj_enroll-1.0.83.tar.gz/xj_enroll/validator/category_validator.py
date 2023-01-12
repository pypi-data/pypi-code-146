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


class CategoryValidator(Validator):
    value = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "value 必填 必填",
        },
    )

    description = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "value 必填 必填",
        },
    )
