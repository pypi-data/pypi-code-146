
from sparrow_order_lib.core.datastructures import ImmutablePropertyClassBase


class DocType(ImmutablePropertyClassBase):
    _TEST_DOC_TYPE = 'test_doc_type'  # 测试数据类型
    ORDER_V2 = 'order_v2'  # 订单数据
    ORDER_V3 = 'order_v3'  # 订单数据


IndexMapping = {
    DocType._TEST_DOC_TYPE: 'test_doc_type',  # 测试数据类型
    DocType.ORDER_V2: 'order_v2',
    DocType.ORDER_V3: 'order_v3',
}
