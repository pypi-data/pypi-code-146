import unittest

from sparrow_order_lib.es.es_util.base import _doc_types_conf
from sparrow_order_lib.es.es_util.base import __EXAMPLE_DOC_TYPE as EXAMPLE_DOC_TYPE
from sparrow_order_lib.es.es_util.base import __EXAMPLE_MAPPING as EXAMPLE_MAPPING
from sparrow_order_lib.es.es_util.base import _doc_types_conf_mapping_key
from sparrow_order_lib.es.es_util.base import _doc_types_conf_query_mapping_key
from sparrow_order_lib.es.es_util.constants import ESFieldType


class TestConfig(unittest.TestCase):

    def test_assert_doc_type_in_conf(self):
        ''' 判断示例文档类型注册成功 '''

        expr = EXAMPLE_DOC_TYPE in _doc_types_conf
        self.assertTrue(expr=expr, msg="测试文档类型未加载到配置中")

    def test_assert_all_fields_in_conf(self):
        ''' 示例文档类型注册后配置正确 '''
        query_conf = _doc_types_conf[EXAMPLE_DOC_TYPE][_doc_types_conf_query_mapping_key]
        mapping_conf = _doc_types_conf[EXAMPLE_DOC_TYPE][_doc_types_conf_mapping_key]['mapping']['properties']
        for field in EXAMPLE_MAPPING['mapping']['properties']:
            if EXAMPLE_MAPPING['mapping']['properties'][field]['type'] not in ESFieldType.SUB_OBJECT_FIELD:
                # 所有 field 都在配置中
                expr = field in _doc_types_conf[EXAMPLE_DOC_TYPE][_doc_types_conf_query_mapping_key]
                self.assertTrue(expr=expr, msg=f"示例文档类型配置错误, {field}不在配置中")
                # 所有 field 的配置类型都相同
                expr2 = query_conf[field]['type'] == mapping_conf[field]['type']
                self.assertTrue(expr=expr2, msg=f"示例文档类型 {field} 在 mapping 和 query_mapping 中的类型不一致.")


if __name__ == '__main__':
    unittest.main()
