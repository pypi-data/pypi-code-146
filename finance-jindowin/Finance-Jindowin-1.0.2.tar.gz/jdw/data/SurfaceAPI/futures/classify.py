# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class FutClassify(object):

    def __init__(self, table_name=None):
        self._engine = FetchKDEngine()
        self._table_name = table_name if table_name is not None else 'fut_classify'
        self._table_model = self._engine.table_model(self._table_name)

    def _map_industry_category(self, category):
        if category == 'kh':
            return 'KH行业分类'
        else:
            raise ValueError(
                "No other industry is supported at the current time")

    def codes_fetch(self, codes, start_date, end_date, category, level):
        industry_category_name = self._map_industry_category(category)
        code_name = 'industryID' + str(level)
        industry_model = self._engine.table_model('fut_classify')
        query = select([
            industry_model.trade_date, industry_model.code,
            getattr(industry_model, code_name).label('industry_code')
        ]).where(
            and_(industry_model.code.in_(codes),
                 industry_model.industry == industry_category_name)).order_by(
                     industry_model.code)

        return pd.read_sql(query, self._engine.client()).dropna()

    def universe_fetch(self, universe, start_date, end_date, category, level):
        industry_category_name = self._map_industry_category(category)
        code_name = 'industryID' + str(level)
        industry_model = self._engine.table_model('fut_classify')

        codes = universe.query(start_date, end_date)['code'].unique().tolist()

        query = select([
            industry_model.trade_date, industry_model.code,
            getattr(industry_model, code_name).label('industry_code')
        ]).where(
            and_(industry_model.code.in_(codes),
                 industry_model.industry == industry_category_name)).order_by(
                     industry_model.code)

        return pd.read_sql(query, self._engine.client()).dropna()