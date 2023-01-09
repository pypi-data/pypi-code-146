# -*- coding: utf-8 -*-
from jdw.mfc.entropy.pascal.score.base import Base
from jdw.data.SurfaceAPI.futures.yields import FutYields
from jdw.data.SurfaceAPI.futures.factors import FutFactors
from jdw.data.SurfaceAPI.universe import FutUniverse
from jdw.data.SurfaceAPI.futures.classify import FutClassify


class FuturesScore(Base):

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
        super(FuturesScore, self).__init__(yields_class=FutYields,
                                           factors_class=FutFactors,
                                           universe_class=FutUniverse,
                                           industry_class=FutClassify,
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
        factors_data = factors_data.merge(industry_data.drop(['trade_date'],
                                                             axis=1),
                                          on=['code'])
        factors_data = self.industry_median(factors_data)
        return factors_data