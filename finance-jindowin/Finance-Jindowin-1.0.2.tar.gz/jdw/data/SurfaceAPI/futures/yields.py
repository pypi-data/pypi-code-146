# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import select, and_, join
from jdw.data.SurfaceAPI.yields import Yields


class FutYields(Yields):

    def __init__(self):
        super().__init__(table_name='fut_derived_yields')

    def fetch_returns(self,
                      universe,
                      start_date,
                      end_date,
                      offset,
                      horizon=0,
                      name='ret',
                      benchmark=None):
        table_model = self._engine.table_model('fut_derived_yields')
        return self._fetch_returns(universe=universe,
                                   name=name,
                                   table_model=table_model,
                                   start_date=start_date,
                                   end_date=end_date,
                                   horizon=horizon,
                                   offset=offset,
                                   benchmark=benchmark)
