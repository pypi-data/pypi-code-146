# -*- coding: utf-8 -*-
import pdb
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class Basic(object):

    def __init__(self, table_name=None):
        self._engine = FetchKDEngine()
        self._table_name = table_name if table_name is not None else 'fut_basic'
        self._table_model = self._engine.table_model(self._table_name)

    def cond1(self, cols, codes, start_date, end_date):

        clause_list = and_(self._table_model.flag == 1,
                           self._table_model.code.in_(codes),
                           self._table_model.lastTradeDate >= start_date,
                           self._table_model.listDate <= end_date)

        query = select(cols).where(clause_list)
        return pd.read_sql(query, self._engine.client())
