# -*- coding: utf-8 -*-
import datetime, pdb
import pandas as pd
import numpy as np
from ultron.tradingday import *
from ultron.factor.data.transformer import Transformer
from jdw.kdutils.logger import kd_logger
from jdw.data.SurfaceAPI import IndexMarket
from jdw.data.SurfaceAPI import FutClassify as Classify
from jdw.data.SurfaceAPI import FutIndexMarket
from jdw.data.SurfaceAPI import FutYields as Yields
from jdw.data.SurfaceAPI import FutUniverse as Universe
from jdw.data.SurfaceAPI import FutBasic as Basic
from jdw.data.SurfaceAPI import FutFactors as Factors
from ultron.strategy.strategy import StrategyEngine, create_params


class Daily(object):

    def __init__(self,
                 offset,
                 horizon,
                 factors_data=None,
                 industry_name='kh',
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

    def fetch_classify(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch classify data")
        classify = Classify()
        if self._universe is not None:
            universe = Universe(u_name=self._universe)
            classify_data = classify.universe_fetch(
                universe=universe,
                start_date=begin_date,
                end_date=end_date,
                category=self._industry_name,
                level=self._industry_level)
        else:
            classify_data = classify.codes_fetch(codes=codes,
                                                 start_date=begin_date,
                                                 end_date=end_date,
                                                 category=self._industry_name,
                                                 level=self._industry_level)
        return classify_data.drop(['trade_date'], axis=1)

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

    '''
    def create_benchmark(self, begin_date, end_date, codes):

        def mv_weighted(data):
            weighted = data[['market_values']] / data[['market_values']].sum()
            weighted['code'] = data['code'].values
            weighted = weighted.reset_index().drop(['trade_date'], axis=1)
            return weighted.rename(columns={'market_values': 'weight'})

        def equal_weighted(data):
            weighted = 1 / len(data)
            weighted = pd.DataFrame([weighted for i in range(0, len(data))],
                                    columns=['market_values'],
                                    index=data.index)
            weighted['code'] = data['code'].values
            weighted = weighted.reset_index().drop(['trade_date'], axis=1)
            return weighted.rename(columns={'market_values': 'weight'})

        if True:
            universe = Universe(u_name=self._universe)
            market_data = FutIndexMarket().market(universe=universe,
                                                  codes=codes,
                                                  start_date=begin_date,
                                                  end_date=end_date,
                                                  columns=['closePrice'])
            benchmark_weighed = market_data.set_index('trade_date').groupby(
                level=['trade_date']).apply(lambda x: equal_weighted(x))
            benchmark_weighed = benchmark_weighed.reset_index().drop(
                ['level_1'], axis=1)

        return benchmark_weighed
    '''

    def create_params(self, **kwargs):
        self._params = create_params(**kwargs)

    def params(self):
        return self._params

    def create_benchmark(self, total_data):
        kd_logger.info("create benchmark")
        strategy = StrategyEngine.create_class('fut')(
            alpha_model=None,
            total_data=total_data,
            features=self._transformer.names,
            start_date=datetime.datetime(2018, 1, 4))
        total_data['weight'] = 0.0
        total_data['prev1_ret'] = 0.0
        params = create_params(method='long_short')
        positions = strategy.rebalance_positions(params=params)
        return positions[['trade_date', 'code', 'weight']]

    def prev_yields(self, begin_date, end_date, codes=None):
        start_date = advanceDateByCalendar('china.sse', begin_date, '-1b')
        universe = Universe(u_name=self._universe)
        market_data = FutIndexMarket().market(
            universe=universe,
            codes=codes,
            start_date=start_date,
            end_date=end_date,
            columns=['trade_date', 'code', 'closePrice'])
        price_data = market_data.set_index(['trade_date', 'code'])
        price_tb = price_data['closePrice'].unstack()
        price_tb.fillna(method='pad', inplace=True)
        return_tb = np.log(price_tb / price_tb.shift(1)).replace(
            [np.inf, -np.inf], np.nan)
        return_tb = return_tb.stack().reindex(price_data.index)
        return_tb.name = 'prev1_ret'
        return return_tb.dropna().reset_index()

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

        if self._factors_data is None:
            factors_data = self.fetch_factors(begin_date=begin_date,
                                              end_date=end_date,
                                              codes=codes)
        else:
            factors_data = self._factors_data.copy()

        industry_data = self.fetch_classify(begin_date=begin_date,
                                            end_date=end_date,
                                            codes=codes)

        factors_data = factors_data.merge(industry_data, on=['code'])

        factors_data = self.industry_median(factors_data)

        factors_data = factors_data.sort_values(by=['trade_date', 'code'])
        factors_data = self._transformer.transform(
            'code', factors_data.set_index('trade_date'))

        industry_dummy = pd.get_dummies(
            industry_data.set_index(['code'])['industry_code']).reset_index()

        total_data = factors_data.reset_index().merge(
            industry_data,
            on=['code']).merge(yields_data, on=['trade_date',
                                                'code']).merge(industry_dummy,
                                                               on=['code'])
        prev_data = self.prev_yields(begin_date=begin_date,
                                     end_date=end_date,
                                     codes=codes)
        benchmark_data = self.create_benchmark(total_data.copy())
        total_data = total_data.merge(benchmark_data,
                                      on=['trade_date', 'code'
                                          ]).merge(prev_data,
                                                   on=['trade_date', 'code'])

        strategy = StrategyEngine.create_class('fut')(
            alpha_model=self._alpha_model,
            index_return=index_return,
            risk_model=None,
            total_data=total_data,
            features=self._transformer.names,
            start_date=datetime.datetime(2018, 1, 4))

        metrics, returns, positions = strategy.run(self._params)
        return pd.DataFrame(metrics), returns, positions
