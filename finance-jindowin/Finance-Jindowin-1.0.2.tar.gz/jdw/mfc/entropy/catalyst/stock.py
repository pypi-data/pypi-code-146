# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.stock.industry import Industry
from jdw.mfc.entropy.catalyst.base import Base


class StockCatalyst(Base):

    def __init__(self,
                 thresh,
                 universe,
                 factor_columns,
                 industry_name,
                 industry_level,
                 offset=0,
                 horizon=0,
                 model_sets=None,
                 factors_data=None,
                 yield_name='returns'):
        super(StockCatalyst, self).__init__(yields_class=StkYields,
                                            factors_class=StkFactors,
                                            universe_class=StkUniverse,
                                            industry_class=Industry,
                                            thresh=thresh,
                                            offset=offset,
                                            horizon=horizon,
                                            universe=universe,
                                            factor_columns=factor_columns,
                                            industry_name=industry_name,
                                            industry_level=industry_level,
                                            model_sets=model_sets,
                                            factors_data=factors_data,
                                            yield_name=yield_name)

    def industry_fillna(self, industry_data, factors_data):
        factors_data = factors_data.merge(industry_data,
                                          on=['trade_date', 'code'])
        factors_data = self.industry_median(factors_data)
        return factors_data