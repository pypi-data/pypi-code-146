# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.engine import FetchKDEngine
from jdw.data.SurfaceAPI.utilities import create_stats


class MarketStock(object):

    def __init__(self, table_name=None):
        self._engine = FetchKDEngine()
        self._table_name = table_name if table_name is not None else 'market_stock'
        self._table_model = self._engine.table_model(self._table_name)

    def codes_fetch(self, codes, start_date, end_date, columns):
        cols = [self._table_model.trade_date, self._table_model.code]
        for col in columns:
            cols.append(self._table_model.__dict__[col])

        clause_list = and_(
            self._table_model.flag == 1, self._table_model.code.in_(codes),
            self._table_model.trade_date.between(start_date, end_date))

        query = select(cols).where(clause_list)
        return pd.read_sql(query, self._engine.client())

    def universe_fetch(self, universe, start_date, end_date, columns):
        universe_model = universe._table_model
        cols = [self._table_model.trade_date, self._table_model.code]
        for col in columns:
            cols.append(self._table_model.__dict__[col])

        cond = universe._query_statements(start_date, end_date)
        big_table = join(
            self._table_model, universe_model,
            and_(self._table_model.trade_date == universe_model.trade_date,
                 self._table_model.flag == 1,
                 self._table_model.code == universe_model.code, cond))

        #clause_list = and_(
        #    self._table_model.flag == 1,
        #    self._table_model.trade_date == universe_model.trade_date,
        #    self._table_model.code == universe_model.code,
        #    self._table_model.trade_date.between(start_date, end_date))
        # query = select(cols).where(clause_list)
        query = select(cols).select_from(big_table)
        return pd.read_sql(query, self._engine.client())
