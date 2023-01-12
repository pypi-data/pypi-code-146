# encoding: utf-8
"""
@project: djangoModel->valuation_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 计价生成服务
@created_time: 2022/10/13 9:40
"""
from django.db.models import F

from ..models import Enroll, EnrollRuleValuate
# 接口服务类
from ..service.subitem_service import SubitemService
from ..utils.j_valuation import JExpression


class ValuationService:
    expression = None  # 表达式

    @staticmethod
    def valuate_test(expression_string=None, input_dict=None):
        # 测试代码
        if input_dict is None:
            input_dict = {}

        expression_string, parsed_variable_map = JExpression.parse_variables(
            expression_string,
            input_dict
        )
        calculator = JExpression()
        data, err = calculator.process(expression_string)
        return data, err

    @staticmethod
    def valuate(category_id, classify_id, variables_dict=None):
        # 测试代码
        expression_list = EnrollRuleValuate.objects \
            .annotate(category_id=F("enroll_rule_group__category_id")) \
            .annotate(classify_id=F("enroll_rule_group__classify_id")) \
            .filter(category_id=category_id, classify_id=classify_id) \
            .order_by("-sort") \
            .values("field", "expression_string")

        expression_map = {i["field"]: i["expression_string"] for i in expression_list}
        # print("category_id:", category_id, " expression_list:", expression_list)
        result = {}
        for k, v in expression_map.items():
            expression_string, parsed_variable_map = JExpression.parse_variables(
                v,
                variables_dict
            )
            calculator = JExpression()
            data, err = calculator.process(expression_string)
            data = round(data,2) if isinstance(data,float) else data
            result.update({k: data})
            variables_dict[k] = data
        return result, None

    @staticmethod
    def valuation_detailed_list(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, "不存在该报名信息"
        # 变量字典
        variables_dict = enroll_obj.first().to_json()

        # 获取计价ID
        enroll_rule_group_id = variables_dict.get("enroll_rule_group_id")
        if not enroll_rule_group_id:
            return None, "该报名没有绑定计价ID"

        # 获取计价规则
        valuate_obj = EnrollRuleValuate.objects.filter(enroll_rule_group_id=enroll_rule_group_id)
        if not valuate_obj:
            return None, "没有配置计价公式"

        # 子项变量
        subitem_list, err = SubitemService.list({"enroll_id": enroll_id}, False)
        subitem_dict = {}
        for i in subitem_list:
            for k, v in i.items():
                key = "enroll_subitem__" + k
                value = str(v) if v else "0"
                subitem_dict[key] = value if (subitem_dict.get(key, None) is None) else (subitem_dict[key] + "," + value)

        variables_dict.update(subitem_dict)

        # 计算公式解析
        result = {}
        valuate_list = valuate_obj.values("name", "type", "field", "expression_string")
        for item in valuate_list:
            expression_string, parsed_variable_map = JExpression.parse_variables(
                item["expression_string"],
                variables_dict
            )
            calculator = JExpression()
            data, err = calculator.process(expression_string)
            result[item["field"]] = data
        return result, None
