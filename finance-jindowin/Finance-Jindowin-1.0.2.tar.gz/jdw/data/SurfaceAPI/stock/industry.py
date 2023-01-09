# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class Industry(object):

    def __init__(self, table_name=None):
        self._engine = FetchKDEngine()
        self._table_name = table_name if table_name is not None else 'industry'
        self._table_model = self._engine.table_model(self._table_name)

    def _map_industry_category(self, category):
        if category == 'sw':
            return '申万行业分类'
        elif category == 'zz':
            return '中证行业分类'
        elif category == 'zjh':
            return '证监会行业V2012'
        else:
            raise ValueError(
                "No other industry is supported at the current time")

    def codes_fetch(self, codes, start_date, end_date, category, level):
        industry_category_name = self._map_industry_category(category)
        code_name = 'industryID' + str(level)
        category_name = 'industryName' + str(level)
        industry_model = self._engine.table_model('industry')

        query = select([
            industry_model.trade_date, industry_model.code,
            getattr(industry_model, code_name).label('industry_code'),
            getattr(industry_model, category_name).label('industry')
        ]).where(
            and_(industry_model.trade_date.between(start_date, end_date),
                 industry_model.code.in_(codes),
                 industry_model.industry == industry_category_name)).order_by(
                     industry_model.trade_date, industry_model.code)

        return pd.read_sql(query, self._engine.client()).dropna()

    def universe_fetch(self, universe, start_date, end_date, category, level):
        industry_category_name = self._map_industry_category(category)
        cond = universe._query_statements(start_date, end_date)
        code_name = 'industryID' + str(level)
        category_name = 'industryName' + str(level)
        industry_model = self._engine.table_model('industry')
        universe_model = universe._table_model

        cond = universe._query_statements(start_date, end_date)

        big_table = join(
            industry_model, universe_model,
            and_(industry_model.trade_date == universe_model.trade_date,
                 industry_model.code == universe_model.code,
                 industry_model.flag == 1,
                 industry_model.industry == industry_category_name, cond))

        query = select([industry_model.trade_date,
                        industry_model.code,
                        getattr(industry_model, code_name).label('industry_code'),
                        getattr(industry_model, category_name).label('industry')]).select_from(big_table)\
            .order_by(industry_model.trade_date, industry_model.code)

        return pd.read_sql(query, self._engine.client()).dropna()

    def codes_matrix(self, codes, start_date, end_date, category, level):
        df = self.codes_fetch(codes=codes,
                              start_date=start_date,
                              end_date=end_date,
                              category=category,
                              level=level)

        df['industry_name'] = df['industry']
        df = pd.get_dummies(df,
                            columns=['industry_code'],
                            prefix="",
                            prefix_sep="")
        return df.drop('industry',
                       axis=1).drop_duplicates(['trade_date', 'code'])

    def universe_matrix(self, universe, start_date, end_date, category, level):
        df = self.universe_fetch(universe=universe,
                                 start_date=start_date,
                                 end_date=end_date,
                                 category=category,
                                 level=level)

        df['industry_name'] = df['industry']
        df = pd.get_dummies(df,
                            columns=['industry_code'],
                            prefix="",
                            prefix_sep="")
        return df.drop('industry',
                       axis=1).drop_duplicates(['trade_date', 'code'])
