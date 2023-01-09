from sparrow_order_lib.es.constants import DocType
from sparrow_order_lib.es.es_util.constants import ESParamOp


# 存放各文档的查询 mapping
QUERY_MAPPING = {
    # 订单数据
    DocType.ORDER_V2: {
        'phone': [
            {
                'path': 'user.user_name',
            },
            {
                'path': 'shipping_address.phone'
            }
        ],
        'name': [
            {
                'path': 'user.name',
            },
            {
                'path': 'shipping_address.name'
            }
        ],
        'shipping_phone': {
            'path': 'shipping_address.phone'
        },
        'order_num': {
            'path': 'order_number'
        },
        'distribute_id': {
            'path': 'distributes.id'
        },
        'distribute_number': {
            'path': 'distributes.number'
        },
        'distribute_status': {
            'path': 'distributes.status'
        },
        'brand_id': {
            'path': 'lines.brand_id'
        },
        'shop_num': {
            'path': 'lines.shop_num',
        },
        'shop_id': {
            'path': 'lines.shop_id'
        },
        'product_id': {
            'path': 'lines.product_id'
        },
        'product_title': {
            'path': 'lines.title'
        },
        'hg_code': {
            'path': 'lines.hg_code'
        },
        'created_time_after': {
            'path': 'created_time',
            'op': ESParamOp.gte,
        },
        'created_time_before': {
            'path': 'created_time',
            'op': ESParamOp.lte,
        }
    },
    DocType.ORDER_V3: {
        'phone': [
            {
                'path': 'user.user_name',
            },
            {
                'path': 'shipping_address.phone'
            }
        ],
        'name': [
            {
                'path': 'user.name',
            },
            {
                'path': 'shipping_address.name'
            }
        ],
        'shipping_phone': {
            'path': 'shipping_address.phone'
        },
        'order_num': {
            'path': 'number'
        },
        'distribute_id': {
            'path': 'distributes.id'
        },
        'distribute_number': {
            'path': 'distributes.number'
        },
        'distribute_status': {
            'path': 'distributes.status'
        },
        'brand_id': {
            'path': 'lines.brand_id'
        },
        'shop_num': {
            'path': 'lines.shop_num',
        },
        'shop_id': {
            'path': 'lines.shop_id'
        },
        'product_id': {
            'path': 'lines.product_id'
        },
        'product_title': {
            'path': 'lines.title'
        },
        'hg_code': {
            'path': 'lines.hg_code'
        },
        'created_time_after': {
            'path': 'created_time',
            'op': ESParamOp.gte,
        },
        'created_time_before': {
            'path': 'created_time',
            'op': ESParamOp.lte,
        }
    }
}


QUERY_MAPPING_SPECIAL_FUNC = {
    # 查询的特殊函数
}
