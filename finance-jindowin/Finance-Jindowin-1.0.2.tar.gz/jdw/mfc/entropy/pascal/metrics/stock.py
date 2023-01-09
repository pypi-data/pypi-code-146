# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.stock.industry import Industry
from jdw.mfc.entropy.pascal.metrics.base import Base


class StockMetrics(Base):

    def __init__(self,
                 universe,
                 factor_columns,
                 industry_name,
                 industry_level,
                 offset=0,
                 horizon=0,
                 factors_data=None,
                 yield_name='returns'):
        super(StockMetrics, self).__init__(yields_class=StkYields,
                                           factors_class=StkFactors,
                                           universe_class=StkUniverse,
                                           industry_class=Industry,
                                           universe=universe,
                                           offset=offset,
                                           horizon=horizon,
                                           industry_name=industry_name,
                                           industry_level=industry_level,
                                           factor_columns=factor_columns,
                                           factors_data=factors_data,
                                           yield_name=yield_name)

    def industry_fillna(self, industry_data, factors_data):
        factors_data = factors_data.merge(industry_data,
                                          on=['trade_date', 'code'])
        factors_data = self.industry_median(factors_data)
        return factors_data