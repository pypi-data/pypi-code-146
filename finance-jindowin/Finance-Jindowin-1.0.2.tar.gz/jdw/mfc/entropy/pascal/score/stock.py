# -*- coding: utf-8 -*-
from jdw.mfc.entropy.pascal.score.base import Base
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.stock.market_stock import MarketStock
from jdw.data.SurfaceAPI.stock.industry import Industry


class StockScore(Base):

    def __init__(self,
                 universe,
                 factor_columns,
                 industry_name,
                 industry_level,
                 offset=0,
                 horizon=0,
                 score_class=None,
                 factors_data=None,
                 weights=None,
                 yield_name='returns'):
        super(StockScore, self).__init__(yields_class=StkYields,
                                         factors_class=StkFactors,
                                         industry_class=Industry,
                                         universe_class=StkUniverse,
                                         universe=universe,
                                         offset=offset,
                                         horizon=horizon,
                                         factor_columns=factor_columns,
                                         industry_name=industry_name,
                                         industry_level=industry_level,
                                         score_class=score_class,
                                         factors_data=factors_data,
                                         weights=weights,
                                         yield_name=yield_name)

    def industry_fillna(self, industry_data, factors_data):
        factors_data = factors_data.merge(industry_data,
                                          on=['trade_date', 'code'])
        factors_data = self.industry_median(factors_data)
        return factors_data