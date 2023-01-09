# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.futures.yields import FutYields
from jdw.data.SurfaceAPI.futures.factors import FutFactors
from jdw.data.SurfaceAPI.universe import FutUniverse
from jdw.data.SurfaceAPI.futures.classify import FutClassify
from jdw.mfc.entropy.catalyst.base import Base


class FuturesCatalyst(Base):

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
                 yield_name='ret'):
        super(FuturesCatalyst, self).__init__(yields_class=FutYields,
                                              factors_class=FutFactors,
                                              universe_class=FutUniverse,
                                              industry_class=FutClassify,
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
        factors_data = factors_data.merge(industry_data.drop(['trade_date'],
                                                             axis=1),
                                          on=['code'])
        factors_data = self.industry_median(factors_data)
        return factors_data