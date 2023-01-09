'''
根据配置, 将查询入参转化为 ES 查询所需参数
'''
from sparrow_order_lib.es.es_util import logger
from sparrow_order_lib.es.es_util.field import ESField
from sparrow_order_lib.es.es_util.es_param import ESParam, ESParamGroup, ESParamsForOneGroup, ESParamPageGroup, ESParamSortGroup
from sparrow_order_lib.es.es_util.in_query_param import InQueryParam
from sparrow_order_lib.es.es_util.exceptions import ESUtilInvalidDocType, ESUtilConfException
from sparrow_order_lib.es.es_util.constants import ESParamOp, ESQueryGroupName
from sparrow_order_lib.es.es_util.base import _doc_types_conf, _doc_types_conf_mapping_key, _doc_types_conf_query_mapping_key


class ESQueryUtil(object):
    ''' 对某文档类型进行查询时的工具类, 用于构建查询参数 '''

    def __init__(self, query_type_string: str):
        '''
        :param doc_type: 文档类型
        '''

        self.__doc_type_is_valid(query_type_string)

        self.__doc_type = query_type_string
        self.__mapping = _doc_types_conf[self.__doc_type][_doc_types_conf_mapping_key]
        self.__query_mapping = _doc_types_conf[self.__doc_type][_doc_types_conf_query_mapping_key]

    def get_es_query_param(self, in_param_obj: InQueryParam) -> ESParamGroup:
        ''' 由入参构造查询 ES 时的参数

        :param in_param_obj: 查询初始参数
        '''
        in_param_key = in_param_obj.in_param_key
        in_param_value = in_param_obj.in_param_value

        if in_param_key not in self.query_mapping:
            logger.error(f"文档类型doc_type={self.doc_type}配置中无法找到 in_param_key={in_param_key}, query_mapping={self.query_mapping}")
            raise ESUtilConfException(f"文档类型doc_type={self.doc_type}配置中无法找到 in_param_key={in_param_key}")
        query_mapping_conf = self.query_mapping[in_param_key]

        if isinstance(query_mapping_conf, dict):

            path = query_mapping_conf['path']
            type = query_mapping_conf['type']
            opstring = query_mapping_conf['op']

            if opstring == ESParamOp.ne:
                query_name = ESQueryGroupName.MUST_NOT
            else:
                query_name = ESQueryGroupName.MUST

            es_field = ESField(path=path, type=type)

            es_param = ESParam(field=es_field, op=opstring, other=in_param_value)

            return ESParamGroup(es_param, query_name=query_name)

        elif isinstance(query_mapping_conf, list):

            es_params = []

            for single in query_mapping_conf:
                path = single['path']
                type = single['type']
                opstring = single['op']

                es_field = ESField(path=path, type=type)

                es_params.append(ESParam(field=es_field, op=opstring, other=in_param_value))

            espm = ESParamsForOneGroup(es_params)

            return ESParamGroup(espm, query_name=ESQueryGroupName.SHOULD)

    @property
    def doc_type(self):
        return self.__doc_type

    @property
    def mapping(self):
        return self.__mapping

    @property
    def query_mapping(self):
        return self.__query_mapping

    def __doc_type_is_valid(self, doc_type):
        if doc_type not in _doc_types_conf:
            logger.error(f"无效文档类型, doc_type={doc_type}, 无法找到配置.")
            raise ESUtilInvalidDocType(doc_type)

    @classmethod
    def get_page_param_group(cls, page, page_size):
        return ESParamPageGroup(page, page_size)

    @classmethod
    def get_sort_param_group(cls, sort_string):
        return ESParamSortGroup(sort_string)
