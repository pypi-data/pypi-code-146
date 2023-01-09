'''
创建者模式
'''

import copy
import logging

from sparrow_order_lib.es.es_util.client import init_es
from sparrow_order_lib.es.es_util.es_param import ESParamPageGroup, ESParamSortGroup

logger = logging.getLogger('sparrow_order_lib')


class ESBuilder(object):
    ''' 接收查询条件构建 DSL, 查询ES集群 '''

    def __init__(self, index):
        self.index = index
        self.__query_group = {}
        self.__other_query_group = {}
        self.__es = None
        self.__main_dsl = None
        self.__other_dsl = None
        self.__paged_dsl = None

    def addQueryGroup(self, es_param_group):
        ''' 添加查询条件

        :param es_param_group: 某一组查询条件, 可以是 ESParamMustGroup 等 或者 ESParamPageGroup
        '''

        if isinstance(es_param_group, (ESParamPageGroup, ESParamSortGroup)):
            self.__other_dsl = None
            self.__other_query_group[es_param_group.query_name] = es_param_group
        else:
            self.__main_dsl = None
            _es_param_group = self.__query_group.get(es_param_group.query_name)
            if _es_param_group is None:
                self.__query_group[es_param_group.query_name] = es_param_group
            else:
                _es_param_group.add_one_espm(es_param_group.espm)

        return self

    @property
    def main_dsl(self):
        if self.__main_dsl is None:
            self.__get_dsl()
        return self.__main_dsl

    @property
    def page_dsl(self):
        if self.__paged_dsl is None:
            self.__get_dsl()
        return self.__paged_dsl

    def __get_dsl(self):
        if self.__main_dsl is None:
            bool_dsl = {}
            for query_group in self.__query_group.values():
                bool_dsl.update(query_group.get_dsl())

            # TODO: 在规划初期 没有设置好 A and B and (C or D) 的表现形式, 临时在这处理
            if len(bool_dsl) >= 2:
                # 当有两个以上的条件时, 它们其实都应该是与的关系, 目前却作成了或的关系
                must = []
                if 'must' in bool_dsl:
                    must = bool_dsl.pop('must')
                for query in bool_dsl:
                    must.append(
                        {
                            'bool': {
                                query: bool_dsl[query]
                            }
                        }
                    )
                bool_dsl = {'must': must}

            self.__main_dsl = {
                'query': {
                    'bool': bool_dsl
                }
            }
        if self.__other_dsl is None:
            self.__other_dsl = {}
            for other_group in self.__other_query_group.values():
                self.__other_dsl.update(copy.deepcopy(other_group.get_dsl()))
        self.__paged_dsl = {}
        self.__paged_dsl.update(copy.deepcopy(self.__main_dsl))
        self.__paged_dsl.update(self.__other_dsl)

    @property
    def es(self):
        ''' 返回与 ES 集群的连接 '''
        if self.__es is None:
            self.__es = init_es()
        return self.__es

    def executeQuery(self):
        ''' 执行查询 并返回查询结果 '''
        self.__get_dsl()
        logger.info(f'index={self.index}, dsl={self.__paged_dsl}')
        res = self.es.search(body=self.__paged_dsl, index=self.index)
        return res

    def executeCountQuery(self):
        ''' 数据总条数 '''
        self.__get_dsl()
        logger.info(f'index={self.index}, count_dsl={self.__main_dsl}')
        res = self.es.count(body=self.__main_dsl, index=self.index)
        return res['count']
