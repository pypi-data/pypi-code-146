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


class RuleValidator(Validator):
    name = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "name 必填",
        },
    )

    type = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "type 必填",
        },
    )

    field = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "field 必填",
        },
    )

    expression_string = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            "required": "expression_string 必填",
        },
    )
