'''
ES 查询组件使用的基础，本模块提供了 register_doc_type 函数，项目启动时，会将文档配置读入。
'''
import logging

from sparrow_order_lib.es.es_util.constants import ESParamOp
from sparrow_order_lib.es.es_util.exceptions import ESUtilConfException, ESUtilInvalidDocType
from sparrow_order_lib.core.datastructures import ImmutableDict

logger = logging.getLogger("elastic")

_doc_types_conf = ImmutableDict()

_doc_types_conf_mapping_key = 'mapping'
_doc_types_conf_query_mapping_key = 'query_mapping'


def register_doc_type(doc_type, mapping, query_mapping, special_query_func=None):
    ''' 注册一个ES文档类型

    :param doc_type: 文档类型
    :param mapping: 建立 ES 文档时的 mapping
    :param query_mapping: 对该文档查询时的一些配置, 是查询条件对查询字段的映射
    :param special_query_func: 对于一些特殊查询, 支持定义特定的查询函数

    示例:
        doc_type = 'test_doc_type'
        mapping =  {
                'mapping': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'number': {'type': 'keyword'},
                        'inner': {
                            'type': 'nested',
                            'properties': {
                                'id': {'type': 'integer'},
                                'number': {'type': 'keyword'}
                            }
                        }
                    }
                }
            }
        query_mapping = {
                'main_id': {
                    'path': 'id',
                    'type': 'integer'  # 如果缺省 type 会去 mapping 里面 按照 path 进行匹配类型, 匹配不到时会抛出异常
                },
                'all_number': [
                    {
                        'path': 'number'
                    },
                    {
                        'path': 'inner.number',
                        'type': 'keyword'  # 如果缺省 type, 会使用 . 作为分隔符将 path 分割后, 逐级去查询到最后一层获取 type
                    }
                ]
            }
        }

        register_doc_type(doc_type, mapping, query_mapping)

    '''
    global _doc_types_conf

    if doc_type in _doc_types_conf:
        logger.error(f"文档类型重复, {doc_type}")
        raise ESUtilInvalidDocType(doc_type, "文档类型重复")

    __mapping_inspection(doc_type, mapping)
    __query_mapping_inspection(doc_type, mapping, query_mapping)

    d = dict()

    d[doc_type] = {
        _doc_types_conf_mapping_key: mapping,
        _doc_types_conf_query_mapping_key: query_mapping
    }

    for doc_type, doc_type_conf in _doc_types_conf.items():
        d[doc_type] = doc_type_conf

    _doc_types_conf = ImmutableDict(d)

    logger.debug(f"文档注册成功, doc_type={doc_type}, mapping={mapping}, query_mapping={query_mapping}, special_query_func={special_query_func}")


def __mapping_inspection(doc_type, mapping):
    ''' 查看 mapping 配置是否正确 '''

    def __check_properties(properties):
        for field, conf in properties.items():
            if 'type' not in conf:
                raise ESUtilConfException(f"doc_type={doc_type}的 mapping 配置项 {field} 缺失 type.")
            if conf['type'] in ('nested', 'object'):
                if 'properties' not in conf:
                    raise ESUtilConfException(f"doc_type={doc_type}的 mapping 配置项 {field} 类型type={conf['type']}缺失 properties.")
                _properties = conf['properties']
                __check_properties(_properties)

    properties = mapping['mapping']['properties']
    __check_properties(properties)


def __query_mapping_inspection(doc_type, mapping, query_mapping):
    ''' 检查查询项是否正确 '''

    properties = mapping['mapping']['properties']

    def __inspection_one_conf(query_key, query_conf):
        if isinstance(query_conf, dict):
            if 'path' not in query_conf:

                if query_conf.get('is_special_query'):
                    # TODO: 特殊的处理
                    return
                else:
                    raise ESUtilConfException(f"doc_type={doc_type} 的 query_mapping 配置 {query_key} 无法找到 path.")
            field_path = query_conf['path']
            paths = field_path.split('.')
            dic = properties
            type = None
            for p in paths:  # 逐层查找 path
                try:
                    if type in ('nested', 'object'):
                        dic = dic['properties']
                    dic = dic[p]
                    type = dic['type']
                except KeyError:
                    raise ESUtilConfException(f"doc_type={doc_type} 的 query_mapping 配置项{query_key} path={field_path} 无效.")
            # type = dic['type']
            query_conf['type'] = type  # 补充 type 信息
            if 'op' not in query_conf:
                query_conf['op'] = ESParamOp.eq

        elif isinstance(query_conf, list):
            for conf in query_conf:
                __inspection_one_conf(query_key, conf)

    for query_key, query_conf in query_mapping.items():
        __inspection_one_conf(query_key, query_conf)

    # 将 mapping 内所有的字段不在 query_mapping 出现的字段 配置进入 query_mapping
    def __complemented_query_mapping(properties, path_profix=""):
        for field, conf in properties.items():
            type = conf['type']
            path = '.'.join(list(filter(bool, [path_profix, field])))
            query_key = '_'.join(list(filter(bool, [path_profix, field])))

            if type not in ('nested', 'object'):
                if query_key in query_mapping:
                    continue
                query_mapping[query_key] = {
                    'path': path,
                    'type': type,
                    'op': ESParamOp.eq
                }
            else:
                _properties = conf['properties']
                __complemented_query_mapping(_properties, path)

    __complemented_query_mapping(properties)


# 测试 register_doc_type, 也是举例说明 register_doc_type 的使用方式
__EXAMPLE_DOC_TYPE = 'test_doc_type'
__EXAMPLE_MAPPING = {
    'mapping': {
        'properties': {
            'id': {'type': 'integer'},
            'number': {'type': 'keyword'},
            'inner': {
                'type': 'nested',
                'properties': {
                    'id': {'type': 'integer'},
                    'number': {'type': 'keyword'}
                }
            },
            'created_time': {'type': 'date'}
        }
    }
}
__EXAMPLE_QUERY_MAPPING = {
    'main_id': {
        'path': 'id',
        'type': 'integer',  # 如果缺省 type 会去 mapping 里面 按照 path 进行匹配类型, 匹配不到时会抛出异常
    },
    'all_number': [
        {
            'path': 'number'
        },
        {
            'path': 'inner.number',
            'type': 'keyword'  # 如果缺省 type, 会使用 . 作为分隔符将 path 分割后, 逐级去查询到最后一层获取 type
        }
    ],
    'created_time__before': {
        'path': 'created_time',
        'op': ESParamOp.lte  # 决定查询时以什么关系使用参数
    },
    'created_time__after': {
        'path': 'created_time',
        'op': ESParamOp.gte
    },
    'query_type': {
        'is_special_query': True,
        'func_key': 'get_special_dsl'
    }
}

__EXAMPLE_SPECIAL_QUERY_FUNC = {
        'get_special_dsl': lambda x: x  # TODO: 定义特殊查询函数  用于一些特殊字段的查询
}

register_doc_type(
    doc_type=__EXAMPLE_DOC_TYPE,
    mapping=__EXAMPLE_MAPPING,
    query_mapping=__EXAMPLE_QUERY_MAPPING,
    special_query_func=__EXAMPLE_SPECIAL_QUERY_FUNC
)
