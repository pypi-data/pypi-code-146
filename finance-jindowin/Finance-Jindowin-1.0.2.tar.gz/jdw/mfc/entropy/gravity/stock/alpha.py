# -*- coding: utf-8 -*-
from jdw.mfc.entropy.gravity.model import Model
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.stock.industry import Industry
from jdw.data.SurfaceAPI.stock.risk_model import RiskModel


class AlphaModel(Model):

    def __init__(self,
                 alpha_model,
                 factors_data=None,
                 batch=1,
                 freq=1,
                 neutralized_risk=None,
                 risk_model='day',
                 pre_process=None,
                 post_process=None,
                 industry_name='sw',
                 industry_level=1,
                 yield_name='ret',
                 universe=None):
        super(AlphaModel, self).__init__(factor_class=StkFactors,
                                         universe_class=StkUniverse,
                                         yields_class=StkYields,
                                         industry_class=Industry,
                                         risk_class=RiskModel,
                                         alpha_model=alpha_model,
                                         factors_data=factors_data,
                                         batch=batch,
                                         freq=freq,
                                         neutralized_risk=neutralized_risk,
                                         risk_model=risk_model,
                                         pre_process=pre_process,
                                         post_process=post_process,
                                         industry_name=industry_name,
                                         industry_level=industry_level,
                                         yield_name=yield_name,
                                         universe=universe)
