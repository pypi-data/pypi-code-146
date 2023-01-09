# -*- coding: utf-8 -*-
import datetime, pdb
import pandas as pd
from ultron.tradingday import *
from ultron.factor.data.transformer import Transformer
from ultron.strategy.strategy import StrategyEngine, create_params
from jdw.kdutils.logger import kd_logger
from jdw.data.SurfaceAPI import StkFactors as Factors
from jdw.data.SurfaceAPI import StkIndustry as Industry
from jdw.data.SurfaceAPI import StkUniverse as Universe
from jdw.data.SurfaceAPI import StkYields as Yields
from jdw.data.SurfaceAPI import MarketStock as Market
from jdw.data.SurfaceAPI import IndexComponent
from jdw.data.SurfaceAPI import IndexMarket
from jdw.data.SurfaceAPI import RiskModel


class Daily(object):

    def __init__(self,
                 offset,
                 horizon=0,
                 factors_data=None,
                 industry_name='sw',
                 risk_model=None,
                 industry_level=1,
                 universe=None,
                 benchmark=None,
                 yield_name='returns',
                 alpha_model=None,
                 factor_columns=None):
        self._offset = offset
        self._horizon = horizon
        self._industry_name = industry_name
        self._universe = universe
        self._industry_level = industry_level
        self._risk_model = risk_model
        self._factors_data = factors_data
        self._benchmark = benchmark
        self._yield_name = yield_name
        self._alpha_model = alpha_model
        self._transformer = Transformer(
            factor_columns) if alpha_model is None else alpha_model[list(
                alpha_model.keys())[0]].formulas
        self._params = None

    def fetch_industry(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch industry data")
        industry = Industry()
        if self._universe is not None:
            universe = Universe(u_name=self._universe)
            industry_data = industry.universe_fetch(
                universe,
                start_date=begin_date,
                end_date=end_date,
                category=self._industry_name,
                level=self._industry_level)
        else:
            industry_data = industry.codes_fetch(codes=codes,
                                                 start_date=begin_date,
                                                 end_date=end_date,
                                                 category=self._industry_name,
                                                 level=self._industry_level)
        return industry_data

    def industry_median(self, factors_data):

        def _industry_median(standard_data, factor_name):
            median_values = standard_data[[
                'trade_date', 'industry_code', 'code', factor_name
            ]].groupby(['trade_date', 'industry_code']).median()[factor_name]

            median_values.name = factor_name + '_median'
            factor_data = standard_data[[
                'trade_date', 'industry_code', 'code', factor_name
            ]].merge(median_values.reset_index(),
                     on=['trade_date', 'industry_code'],
                     how='left')
            factor_data['standard_' +
                        factor_name] = factor_data[factor_name].mask(
                            pd.isnull(factor_data[factor_name]),
                            factor_data[factor_name + '_median'])
            return factor_data.drop(
                [factor_name + '_median'],
                axis=1).set_index(['trade_date', 'code', 'industry_code'])

        res = []
        standarad_cols = [
            'standard_' + col for col in self._transformer.dependency
        ]
        kd_logger.info("start industry median data ...")

        for col in self._transformer.dependency:
            rts = _industry_median(factors_data, col)
            res.append(rts)

        factors_data = pd.concat(res, axis=1)

        factors_data = factors_data.fillna(0)
        factors_data = factors_data.reset_index().set_index(
            ['trade_date', 'code'])
        factors_data = factors_data.drop(
            self._transformer.dependency, axis=1).rename(columns=dict(
                zip(standarad_cols, self._transformer.dependency)))
        return factors_data.reset_index()

    def fetch_factors(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch factor data")
        factors = Factors()
        if self._universe is not None:
            universe = Universe(u_name=self._universe)
            factors_data = factors.universe_fetch(
                universe=universe,
                start_date=begin_date,
                end_date=end_date,
                columns=self._transformer.dependency)
        else:
            factors_data = factors.codes_fetch(
                codes=codes,
                start_date=begin_date,
                end_date=end_date,
                columns=self._transformer.dependency)
        return factors_data

    def create_riskmodel(self, begin_date, end_date, codes=None):
        kd_logger.info("start create risk model data")
        risk_model = RiskModel(risk_model=self._risk_model)
        if self._universe is not None:
            universe = Universe(u_name=self._universe)
            factor_model, risk_cov, risk_exp = risk_model.universe_fetch(
                universe=universe,
                start_date=begin_date,
                end_date=end_date,
                model_type='factor')
        else:
            factor_model, risk_cov, risk_exp = risk_model.codes_fetch(
                codes=codes,
                start_date=begin_date,
                end_date=end_date,
                model_type='factor')
        return factor_model, risk_cov, risk_exp

    def fetch_yields(self, begin_date, end_date, codes=None):
        kd_logger.info("start create yields data")
        yields = Yields()
        if self._universe is not None:
            universe = Universe(u_name=self._universe)
            if self._yield_name == 'returns':
                closing_date = advanceDateByCalendar(
                    'china.sse', end_date,
                    "{}b".format(self._offset + self._horizon + 1),
                    BizDayConventions.Following)
                yields_data = yields.fetch_returns(universe=universe,
                                                   start_date=begin_date,
                                                   end_date=closing_date,
                                                   horizon=self._horizon,
                                                   offset=self._offset,
                                                   benchmark=None)
            else:
                yields_data = yields.universe_fetch(universe=universe,
                                                    start_date=begin_date,
                                                    end_date=end_date,
                                                    name=self._yield_name)
        else:
            yields_data = yields.codes_fetch(codes=codes,
                                             start_date=begin_date,
                                             end_date=end_date,
                                             name=self._yield_name)
        return yields_data

    def create_benchmark(self, begin_date, end_date, codes):

        def _weighted(data):
            weighted = data[['market_values']] / data[['market_values']].sum()
            weighted['code'] = data['code'].values
            weighted['code'] = data['code'].values
            weighted = weighted.reset_index().drop(['trade_date'], axis=1)
            return weighted.rename(columns={'market_values': 'weight'})

        kd_logger.info("start create benchmark")
        if self._benchmark is not None:
            benchmark_data = IndexComponent().query(start_date=begin_date,
                                                    end_date=end_date,
                                                    benchmark=self._benchmark)
        else:
            market_data = Market().codes_fetch(
                codes=codes,
                start_date=begin_date,
                end_date=end_date,
                columns=['negMarketValue', 'marketValue'])
            market_data = market_data.rename(
                columns={'marketValue': 'market_values'})
            benchmark_data = market_data.set_index('trade_date').groupby(
                level=['trade_date']).apply(lambda x: _weighted(x))
            benchmark_data = benchmark_data.reset_index()
        return benchmark_data

    def create_params(self, **kwargs):
        self._params = create_params(**kwargs)

    def params(self):
        return self._params

    def run(self, begin_date, end_date, codes=None):
        kd_logger.info("start service")
        index_return = None
        if self._benchmark is not None:
            closing_date = advanceDateByCalendar(
                'china.sse', end_date,
                "{}b".format(self._offset + self._horizon + 1),
                BizDayConventions.Following)
            index_return = IndexMarket().yields(start_date=begin_date,
                                                end_date=closing_date,
                                                offset=self._offset,
                                                horizon=self._horizon,
                                                index_code=self._benchmark)
            index_return.rename(columns={'nxt1_ret': 'returns'}, inplace=True)

        yields_data = self.fetch_yields(begin_date=begin_date,
                                        end_date=end_date,
                                        codes=codes)

        benchmark_data = self.create_benchmark(begin_date=begin_date,
                                               end_date=end_date,
                                               codes=codes)
        if self._factors_data is None:
            factors_data = self.fetch_factors(begin_date=begin_date,
                                              end_date=end_date,
                                              codes=codes)
        else:
            factors_data = self._factors_data.copy()

        industry_data = self.fetch_industry(begin_date=begin_date,
                                            end_date=end_date,
                                            codes=codes)
        factors_data = factors_data.merge(industry_data,
                                          on=['trade_date', 'code'])
        factors_data = self.industry_median(factors_data)
        factors_data = factors_data.sort_values(by=['trade_date', 'code'])
        factors_data = self._transformer.transform(
            'code', factors_data.set_index('trade_date'))

        factor_model, _, risk_exp = self.create_riskmodel(
            begin_date=begin_date, end_date=end_date, codes=codes)

        industry_dummy = pd.get_dummies(
            industry_data.set_index(['trade_date',
                                     'code'])['industry_code']).reset_index()

        total_data = factors_data.merge(
            industry_data[['trade_date', 'code', 'industry_code']],
            on=['trade_date',
                'code']).merge(yields_data, on=['trade_date', 'code']).merge(
                    benchmark_data,
                    on=['trade_date',
                        'code']).merge(industry_dummy,
                                       on=['trade_date', 'code'
                                           ]).merge(risk_exp,
                                                    on=['trade_date', 'code'])
        strategy = StrategyEngine.create_class('stk')(
            alpha_model=self._alpha_model,
            index_return=index_return,
            risk_model=factor_model,
            total_data=total_data,
            features=self._transformer.names,
            start_date=datetime.datetime(2018, 1, 4))

        metrics, returns, positions = strategy.run(self._params)
        return pd.DataFrame(metrics), returns, positions
