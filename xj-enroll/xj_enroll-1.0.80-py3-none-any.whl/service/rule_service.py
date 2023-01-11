# encoding: utf-8
"""
@project: djangoModel->rule_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名规则表
@created_time: 2022/9/19 15:54
"""
from django.core.paginator import Paginator

from ..models import EnrollRuleValuate, EnrollRuleGroup
from ..utils.custom_tool import format_params_handle


class RuleValueService():
    @staticmethod
    def list(params, need_pagination=1):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "enroll_rule_group_id", "name", "type", "field", "expression_string", ],
        )
        try:
            fetch_obj = EnrollRuleValuate.objects.filter(**params).values()
            if not need_pagination:
                return list(fetch_obj), None
            paginator = Paginator(fetch_obj, size)
            page_obj = paginator.page(page)
            data = {'total': paginator.count, "size": size, 'page': page, 'list': list(page_obj.object_list)}
            return data, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(params, rule_value_id):
        rule_value_id = params.pop("rule_value_id", None) or rule_value_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["rule_value_id", "enroll_rule_group_id", "name", "type", "field", "expression_string", ],
        )
        enroll_obj = EnrollRuleValuate.objects.filter(id=rule_value_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def delete(rule_value_id):
        enroll_obj = EnrollRuleValuate.objects.filter(id=rule_value_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["rule_value_id", "enroll_rule_group_id", "name", "type", "field", "expression_string", ],
        )
        try:
            EnrollRuleValuate.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return None, None

    @staticmethod
    def group_list(request_params):
        print(request_params)
        params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["id", "classifyt_id", "category_id", "rule_group"],
            alias_dict={"rule_group": "rule_group__contains"}
        )
        res_obj = EnrollRuleGroup.objects.filter(**params)
        if res_obj:
            return res_obj.to_json(), None
        else:
            return None, None
