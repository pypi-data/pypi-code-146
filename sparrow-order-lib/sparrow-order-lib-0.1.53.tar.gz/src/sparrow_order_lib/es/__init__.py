'''
基于 elasticsearch 定制开发特有功能

通过配置 doc_type、index、mapping、query_mapping 实现定制化查询

示例:
    在 es.constants、es.mapping_constants、es.query_mapping_constants 配置文档类型

    from es import ESDoor

    doc_type = order

    door = ESDoor(doc_type, phone='18575546060', id=1, number='2222222')
    res = door.main()

'''
from sparrow_order_lib.es.constants import DocType, IndexMapping
from sparrow_order_lib.es.mapping_constants import MAPPINGS
from sparrow_order_lib.es.query_mapping_constants import QUERY_MAPPING
from sparrow_order_lib.es.query_mapping_constants import QUERY_MAPPING_SPECIAL_FUNC

from sparrow_order_lib.es.es_util.base import register_doc_type

doc_types = {p: v for p, v in DocType.__dict__.items() if not p.startswith('_')}

for doc_type in doc_types.values():
    assert doc_type in IndexMapping, f"文档类型{doc_type}未配置索引"
    assert doc_type in MAPPINGS, f"文档类型{doc_type}未配置 mapping"
    assert doc_type in QUERY_MAPPING, f"文档类型{doc_type}未配置 query_mapping"

    register_doc_type(
        doc_type=doc_type,
        mapping=MAPPINGS.get(doc_type),
        query_mapping=QUERY_MAPPING.get(doc_type),
        special_query_func=QUERY_MAPPING_SPECIAL_FUNC.get(doc_type)
    )


from sparrow_order_lib.es.es_util.es_door import ESDoor
