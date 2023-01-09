# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import select, and_
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class IndexComponent(object):

    def __init__(self):
        self._engine = FetchKDEngine()
        self._table_model = self._engine.table_model('index_components')

    def query(self, start_date, end_date, benchmark):
        query = select([
            self._table_model.trade_date, self._table_model.code,
            (self._table_model.weight).label('weight')
        ]).where(
            and_(self._table_model.trade_date.between(start_date, end_date),
                 self._table_model.indexCode == benchmark))
        return pd.read_sql(query, self._engine.client())