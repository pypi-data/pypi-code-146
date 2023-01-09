# -*- coding: utf-8 -*-
import json, pdb
import pandas as pd
import numpy as np
from jdw.kdutils.logger import kd_logger
from jdw.mfc.entropy.catalyst.paramizer import Paramizer
from ultron.tradingday import *
from ultron.optimize.geneticist.genetic import Gentic
from ultron.factor.dimension.corrcoef import FCorrType
from ultron.factor.dimension import DimensionCorrcoef
from ultron.ump.similar.corrcoef import ECoreCorrType

default_models = [
    'RandomForestRegressor', 'LGBMRegressor', 'XGBRegressor',
    'HuberRegression', 'SGDRegression', 'RidgeRegression',
    'ExtraTreesRegressor', 'AdaBoostRegressor', 'GradientBoostingRegressor'
]


class Base(object):

    def __init__(self,
                 yields_class,
                 factors_class,
                 universe_class,
                 industry_class,
                 thresh,
                 universe,
                 factor_columns,
                 industry_name,
                 industry_level,
                 offset=0,
                 horizon=0,
                 callback=None,
                 model_sets=None,
                 factors_data=None,
                 yield_name='returns'):
        self._yields_class = yields_class
        self._factors_class = factors_class
        self._universe_class = universe_class
        self._industry_class = industry_class
        self._factor_columns = factor_columns
        self._offset = offset
        self._horizon = horizon
        self._universe = universe
        self._thresh = thresh
        self._factors_data = factors_data
        self._yield_name = yield_name
        self._industry_name = industry_name
        self._industry_level = industry_level
        self._callback = callback
        self._results = None
        self._total_data = None
        self._params = None
        self._best_programs = None
        self._model_sets = default_models if model_sets is None else model_sets

    def industry_fillna(self, industry_data, factors_data):
        raise NotImplemented

    def fetch_yields(self, begin_date, end_date, codes=None):
        kd_logger.info("start create yields data")
        yields = self._yields_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
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
        factors = self._factors_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
            factors_data = factors.universe_fetch(universe=universe,
                                                  start_date=begin_date,
                                                  end_date=end_date,
                                                  columns=self._factor_columns)
        else:
            factors_data = factors.codes_fetch(codes=codes,
                                               start_date=begin_date,
                                               end_date=end_date,
                                               columns=self._factor_columns)
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
        standarad_cols = ['standard_' + col for col in self._factor_columns]
        kd_logger.info("start industry median data ...")

        for col in self._factor_columns:
            rts = _industry_median(factors_data, col)
            res.append(rts)

        factors_data = pd.concat(res, axis=1)

        factors_data = factors_data.fillna(0)
        factors_data = factors_data.reset_index().set_index(
            ['trade_date', 'code'])
        factors_data = factors_data.drop(self._factor_columns, axis=1).rename(
            columns=dict(zip(standarad_cols, self._factor_columns)))
        return factors_data.reset_index()

    def create_params(self, **kwargs):
        parmas = {}

        n_jobs = 4 if 'n_jobs' not in kwargs else kwargs['n_jobs']

        generations = 10 if 'generations' not in kwargs else kwargs[
            'generations']

        convergence = 0.002 if 'convergence' not in kwargs else kwargs[
            'convergence']

        stopping_criteria = 0.1 if 'stopping_criteria' not in kwargs else kwargs[
            'stopping_criteria']
        population_size = 50 if 'population_size' not in kwargs else kwargs[
            'population_size']
        tournament_size = 10 if 'tournament_size' not in kwargs else kwargs[
            'tournament_size']
        point_mutation = 0.45 if 'point_mutation' not in kwargs else kwargs[
            'point_mutation']

        subtree_mutation = 0.15 if 'subtree_mutation' not in kwargs else kwargs[
            'subtree_mutation']

        hoist_mutation = 0.2 if 'hoist_mutation' not in kwargs else kwargs[
            'hoist_mutation']

        point_replace = 0.05 if 'point_replace' not in kwargs else kwargs[
            'point_replace']

        crossover = 0.05 if 'crossover' not in kwargs else kwargs['crossover']

        mode = 'score' if 'mode' not in kwargs else kwargs['mode']

        n_splits = 5 if 'n_splits' not in kwargs else kwargs['n_splits']

        standard_score = 5 if 'standard_score' not in kwargs else kwargs[
            'standard_score']

        parmas['n_jobs'] = n_jobs
        parmas['convergence'] = convergence
        parmas['stopping_criteria'] = stopping_criteria
        parmas['population_size'] = population_size
        parmas['tournament_size'] = tournament_size
        parmas['point_mutation'] = point_mutation
        parmas['subtree_mutation'] = subtree_mutation
        parmas['hoist_mutation'] = hoist_mutation
        parmas['point_replace'] = point_replace
        parmas['crossover'] = crossover
        parmas['standard_score'] = standard_score
        parmas['mode'] = mode
        parmas['n_splits'] = n_splits
        parmas['generations'] = generations
        self._params = parmas

    def corrcoef(self, factors_data, yields_data):
        kd_logger.info("start corrcoef")
        total_data = factors_data.merge(yields_data, on=['trade_date', 'code'])
        total_data = total_data.sort_values(by=['trade_date', 'code'])
        engine = DimensionCorrcoef(features=self._factor_columns,
                                   thresh=self._thresh,
                                   method=FCorrType.F_CS_CORR)
        dimension_data = engine.run(
            factors_data=factors_data.reset_index(),
            similar_type=ECoreCorrType.E_CORE_TYPE_PEARS)
        dimension_data = dimension_data.replace([np.inf, -np.inf], np.nan)
        return dimension_data.merge(yields_data, on=['trade_date', 'code'])

    def fetch_industry(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch industry data")
        industry = self._industry_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
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

    def save_model(self, gen, rootid, best_programs):  ## 每一代优秀模型回调

        def _create_program(best_programs):
            result = [p.output() for p in best_programs]
            result = pd.DataFrame(result)
            result['desc'] = result['desc'].apply(lambda x: json.dumps(x))
            result.sort_values(by='fitness', ascending=False, inplace=True)
            return result.drop(['update_time'], axis=1)

        result = _create_program(best_programs=best_programs)
        if self._best_programs is None:
            self._best_programs = result
        else:
            self._best_programs = pd.concat([self._best_programs, result],
                                            axis=0)
            self._best_programs = self._best_programs.drop_duplicates(
                subset=['name'])

        if self._callback is not None:
            self._callback(self._best_programs, result, gen)

    def best_programs(self):
        return self._best_programs

    def run(self, begin_date, end_date, codes):
        kd_logger.info("start service")
        yields_data = self.fetch_yields(begin_date=begin_date,
                                        end_date=end_date,
                                        codes=codes)

        factors_data = self.fetch_factors(begin_date=begin_date,
                                          end_date=end_date,
                                          codes=codes)

        industry_data = self.fetch_industry(begin_date=begin_date,
                                            end_date=end_date,
                                            codes=codes)
        ## 中位数填充
        factors_data = self.industry_fillna(industry_data=industry_data,
                                            factors_data=factors_data)

        dimension_data = self.corrcoef(factors_data=factors_data,
                                       yields_data=yields_data)

        params_sets = dict(
            zip(self._model_sets,
                [Paramizer().__getattribute__(m)() for m in self._model_sets]))

        X = dimension_data[['trade_date', 'code'] +
                           self._factor_columns].set_index(
                               ['trade_date', 'code']).fillna(0)
        Y = dimension_data[['trade_date', 'code',
                            'nxt1_ret']].set_index(['trade_date',
                                                    'code']).fillna(0)

        gentic = Gentic(model_sets=self._model_sets,
                        params_sets=params_sets,
                        rootid='10001',
                        generations=self._params['generations'],
                        n_jobs=self._params['n_jobs'],
                        stopping_criteria=self._params['stopping_criteria'],
                        convergence=self._params['convergence'],
                        population_size=self._params['population_size'],
                        tournament_size=self._params['tournament_size'],
                        p_point_mutation=self._params['point_mutation'],
                        p_crossover=self._params['crossover'],
                        standard_score=self._params['standard_score'],
                        save_model=self.save_model)

        gentic.train(self._factor_columns,
                     X=X,
                     Y=Y,
                     mode=self._params['mode'],
                     n_splits=self._params['n_splits'])