# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.yields import Yields
from jdw.data.SurfaceAPI.utilities import create_stats


class StkYields(Yields):

    def __init__(self):
        super().__init__(table_name='stk_derived_yields')

    def fetch_returns(self,
                      universe,
                      start_date,
                      end_date,
                      offset,
                      horizon=0,
                      name='chgPct',
                      benchmark=None):
        table_model = self._engine.table_model('market_stock')
        return self._fetch_returns(universe=universe,
                                   name=name,
                                   table_model=table_model,
                                   start_date=start_date,
                                   end_date=end_date,
                                   horizon=horizon,
                                   offset=offset,
                                   benchmark=benchmark)
