# encoding: utf-8
"""
@project: djangoModel->subitem_extend_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 分项扩展字段处理服务
@created_time: 2022/10/18 16:55
"""

# 分项扩展字段
import re

from ..models import Enroll, EnrollSubitemExtendField
from ..utils.custom_tool import format_params_handle


def output_convert(result_list=None):
    """结果集 扩展字段处理函数"""
    if not result_list:
        return []
    extend_field_list = list(EnrollSubitemExtendField.objects.all().values("category_id", "field_index", "field"))
    extend_field_map = {}
    for item in extend_field_list:
        extend_field_map.setdefault(item["category_id"], {})
        extend_field_map[item["category_id"]].update({item["field_index"]: item["field"]})

    result = []
    for item in result_list:
        this_category_map = extend_field_map.get(item.get("category_id") or 0, {})
        temp = {this_category_map.get(k, k): v for k, v in item.items()}
        result.append({k: v for k, v in temp.items() if not re.search("field_.*", k)})
    return result


def input_convert(params_dict=None, enroll_id=None):
    """修改或插入数据时 参数还原成数据库对应字段"""
    if not params_dict or not enroll_id:
        return {}

    enroll_obj = Enroll.objects.filter(id=enroll_id)
    category_id = enroll_obj.first().to_json().get("category_id") if enroll_obj else None
    if not category_id:
        return format_params_handle(
            param_dict=params_dict,
            filter_filed_list=["enroll_id", "name", "price", "count", "unit", "amount", "description", "remark", "enroll_subitem_status_code"]
        )

    extend_field_obj = EnrollSubitemExtendField.objects.filter(category_id=category_id)
    extend_field_list = extend_field_obj.values("field_index", "field") if extend_field_obj else []
    extend_field_map = {item["field"]: item["field_index"] for item in extend_field_list}
    return format_params_handle(
        param_dict=params_dict,
        filter_filed_list=["enroll_id", "name", "price", "count", "unit", "amount", "description", "remark", "enroll_subitem_status_code"] + list(extend_field_map.keys()),
        alias_dict=extend_field_map
    )
