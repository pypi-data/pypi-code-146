from sparrow_order_lib.es.constants import DocType


# 存放各文档的 mapping
MAPPINGS = {
    # 订单数据
    DocType.ORDER_V2: {
        "mapping": {
            "properties": {
                "id": {"type": "integer"},
                "order_number": {"type": "keyword"},
                "pay_status": {"type": "keyword"},
                "aftersale_status": {"type": "keyword"},
                "exchange_status": {"type": "keyword"},
                "assign_status": {"type": "keyword"},
                "shipping_status": {"type": "keyword"},
                "delivertime_status": {"type": "keyword"},
                "pay_method": {"type": "keyword"},
                "group_status": {"type": "keyword"},
                "user_id": {"type": "keyword"},
                "order_type": {"type": "keyword"},
                "sync_status": {"type": "boolean"},
                "sync_time": {"type": "date"},
                "updated_time": {"type": "date"},
                "created_time": {"type": "date"},
                "completed_time": {"type": "date"},
                "has_valid_to_assign": {"type": "boolean"},
                "has_valid_to_shipping": {"type": "boolean"},
                "lines": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "integer"},
                        "order_id": {"type": "integer"},
                        "brand_id": {"type": "integer"},
                        "shop_id": {"type": "integer"},
                        "shop_num": {"type": "keyword"},
                        "product_id": {"type": "integer"},
                        "productmain_id": {"type": "integer"},
                        "giftproduct_id": {"type": "integer"},
                        "shop_sku": {"type": "keyword"},
                        "hg_code": {"type": "keyword"},
                        "barcode": {"type": "keyword"},
                        "offer": {"type": "keyword"},
                        "if_gift": {"type": "boolean"},
                        "title": {
                            "type": "text",
                            "store": False,
                            "index_analyzer": "ik",
                            "search_analyzer": "ik"
                        }
                    }
                },
                "distributes": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "order_id": {"type": "integer"},
                        "order_number": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "number": {"type": "keyword"},
                        "created_time": {"type": "date"},
                        "completed_time": {"type": "date"}
                    }
                },
                "user": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "user_name": {"type": "keyword"},
                        "name": {"type": "keyword"}
                    }
                },
                "shipping_address": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "keyword"},
                        "phone": {"type": "keyword"}
                    }
                }
            }
        }
    },
    DocType.ORDER_V3: {
        "mapping": {
            "properties": {
                "id": {"type": "integer"},
                "number": {"type": "keyword"},
                "pay_status": {"type": "keyword"},
                "aftersale_status": {"type": "keyword"},
                "exchange_status": {"type": "keyword"},
                "assign_status": {"type": "keyword"},
                "shipping_status": {"type": "keyword"},
                "delivertime_status": {"type": "keyword"},
                "pay_method": {"type": "keyword"},
                "group_status": {"type": "keyword"},
                "user_id": {"type": "keyword"},
                "order_type": {"type": "keyword"},
                "sync_status": {"type": "boolean"},
                "sync_time": {"type": "date"},
                "updated_time": {"type": "date"},
                "created_time": {"type": "date"},
                "completed_time": {"type": "date"},
                "has_valid_to_assign": {"type": "boolean"},
                "has_valid_to_shipping": {"type": "boolean"},
                "is_note": {"type": "boolean"},
                "is_operator_note": {"type": "boolean"},
                "is_single_product": {"type": "boolean"},
                "note": {"type": "text"},
                "number": {"type": "keyword"},
                "operator_note": {"type": "text"},
                "actual_amount": {"type": "double"},
                "total_amount": {"type": "float"},
                "shipping_method": {"type": "keyword"},
                "lines": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "integer"},
                        "order_id": {"type": "integer"},
                        "brand_id": {"type": "integer"},
                        "shop_id": {"type": "integer"},
                        "shop_num": {"type": "keyword"},
                        "product_id": {"type": "integer"},
                        "productmain_id": {"type": "integer"},
                        "giftproduct_id": {"type": "integer"},
                        "shop_sku": {"type": "keyword"},
                        "hg_code": {"type": "keyword"},
                        "barcode": {"type": "keyword"},
                        "offer": {"type": "keyword"},
                        "if_gift": {"type": "boolean"},
                        "quantity": {"type": "integer"},
                        "title": {
                            "type": "text",
                            "store": False,
                            "index_analyzer": "ik",
                            "search_analyzer": "ik"
                        },
                        "sku_attr": {"type": "text"},
                        "main_image": {"type": "text"},
                    }
                },
                "distributes": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "order_id": {"type": "integer"},
                        "order_number": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "number": {"type": "keyword"},
                        "created_time": {"type": "date"},
                        "completed_time": {"type": "date"}
                    }
                },
                "user": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "user_name": {"type": "keyword"},
                        "name": {"type": "keyword"}
                    }
                },
                "shipping_address": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "keyword"},
                        "phone": {"type": "keyword"}
                    }
                }
            }
        }
    }
}
