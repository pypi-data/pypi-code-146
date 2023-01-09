# -*- coding: utf-8 -*-
import pdb
import pandas as pd
import numpy as np
from sqlalchemy import select, and_
from jdw.data.SurfaceAPI.engine import FetchKDEngine
from jdw.data.SurfaceAPI.utilities import create_stats


class IndexMarket(object):

    def __init__(self):
        self._engine = FetchKDEngine()
        self._table_model = self._engine.table_model('index_market')

    def yields(self, start_date, end_date, index_code, horizon=0, offset=0):
        query = select([
            self._table_model.trade_date,
            self._table_model.indexCode.label('code'), self._table_model.chgPct
        ]).where(
            and_(self._table_model.trade_date.between(start_date, end_date),
                 self._table_model.indexCode == index_code,
                 self._table_model.flag == 1)).order_by(
                     self._table_model.trade_date, self._table_model.indexCode)

        market = pd.read_sql(query, self._engine.client())
        market = create_stats(market, horizon, offset)
        return market