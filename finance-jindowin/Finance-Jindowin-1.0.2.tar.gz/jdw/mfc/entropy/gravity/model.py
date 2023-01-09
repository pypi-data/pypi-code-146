# -*- coding: utf-8 -*-
import datetime, pdb, copy
import numpy as np
import pandas as pd
from ultron.tradingday import *
from ultron.factor.data.transformer import Transformer
from ultron.factor.data.processing import factor_processing
from jdw.kdutils.logger import kd_logger


class Model(object):

    def __init__(self,
                 factor_class,
                 universe_class,
                 yields_class,
                 industry_class,
                 risk_class,
                 alpha_model,
                 factors_data=None,
                 batch=1,
                 freq=1,
                 neutralized_risk=None,
                 risk_model='short',
                 pre_process=None,
                 post_process=None,
                 industry_name='sw',
                 industry_level=1,
                 yield_name='returns',
                 universe=None):
        self._factors_data = factors_data
        self._factor_class = factor_class
        self._yields_class = yields_class
        self._industry_class = industry_class
        self._universe_class = universe_class
        self._risk_class = risk_class
        self._industry_name = industry_name
        self._industry_level = industry_level
        self._batch = batch
        self._freq = freq
        self._universe = universe
        self._features = alpha_model.formulas.dependency
        self._yield_name = yield_name
        self._alpha_model = alpha_model
        self._neutralized_risk = neutralized_risk
        self._risk_model = risk_model
        self._pre_process = pre_process
        self._post_process = post_process

    def industry_fillna(self, industry_data, factors_data):
        return factors_data.fillna(0)

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
        standarad_cols = ['standard_' + col for col in self._features]
        kd_logger.info("start industry median data ...")

        for col in self._features:
            rts = _industry_median(factors_data, col)
            res.append(rts)

        factors_data = pd.concat(res, axis=1)

        factors_data = factors_data.fillna(0)
        factors_data = factors_data.reset_index().set_index(
            ['trade_date', 'code'])
        factors_data = factors_data.drop(
            self._features,
            axis=1).rename(columns=dict(zip(standarad_cols, self._features)))
        return factors_data.reset_index()

    def fetch_factors(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch factor data")
        factors = self._factor_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
            factors_data = factors.universe_fetch(universe=universe,
                                                  start_date=begin_date,
                                                  end_date=end_date,
                                                  columns=self._features)
        else:
            factors_data = factors.codes_fetch(codes=codes,
                                               start_date=begin_date,
                                               end_date=end_date,
                                               columns=self._features)
        return factors_data

    def fetch_yields(self, begin_date, end_date, codes=None):
        kd_logger.info("start create yields data")
        yields = self._yields_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
            if self._yield_name == 'returns':
                ### 将batch天后的因子偏移上来进行进行对齐
                closing_date = advanceDateByCalendar(
                    'china.sse', end_date,
                    "{}b".format(self._batch + self._freq + 1),
                    BizDayConventions.Following)
                yields_data = yields.fetch_returns(universe=universe,
                                                   start_date=begin_date,
                                                   end_date=closing_date,
                                                   horizon=self._freq,
                                                   offset=self._batch,
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

    def fetch_risk(self, begin_date, end_date, codes=None):
        kd_logger.info("start fetch risk data")
        risk_model = self._risk_class()
        if self._universe is not None:
            universe = self._universe_class(u_name=self._universe)
            risk_data = risk_model.universe_risk(universe=universe,
                                                 start_date=begin_date,
                                                 end_date=end_date)
        else:
            risk_data = risk_model.codes_risk(codes=codes,
                                              start_date=begin_date,
                                              end_date=end_date)
        return risk_data

    def create_models(self, total_data, begin_date, end_date):
        models = {}
        date_label = pd.DatetimeIndex(total_data.trade_date).to_pydatetime()
        #dates = np.unique(date_label)
        dates = makeSchedule(begin_date,
                             end_date,
                             '1b',
                             calendar='china.sse',
                             dateRule=BizDayConventions.Following,
                             dateGenerationRule=DateGeneration.Backward)
        for d in dates:
            start_date = advanceDateByCalendar(
                'china.sse', d, "-{}b".format(self._batch + self._freq),
                BizDayConventions.Following)
            ref_dates = makeSchedule(
                start_date,
                d,
                '1b',
                calendar='china.sse',
                dateRule=BizDayConventions.Following,
                dateGenerationRule=DateGeneration.Backward)

            if ref_dates[-1] == d:
                end = ref_dates[-2]
                start = ref_dates[
                    -self._batch -
                    1] if self._batch <= len(ref_dates) - 1 else ref_dates[0]
            else:
                end = ref_dates[-1]
                start = ref_dates[-self._batch] if self._batch <= len(
                    ref_dates) else ref_dates[0]
            index = (date_label >= start) & (date_label <= end)
            base_model = copy.deepcopy(self._alpha_model)
            train_data = total_data.set_index(
                'trade_date').loc[index].reset_index()
            train_data = train_data.sort_values(by=['trade_date', 'code'])
            ne_x = factor_processing(
                train_data[self._alpha_model.formulas.names].values,
                pre_process=self._pre_process,
                risk_factors=train_data[self._neutralized_risk].values.astype(
                    float) if self._neutralized_risk is not None else None,
                post_process=self._post_process)

            ne_y = factor_processing(
                train_data[['nxt1_ret']].values,
                pre_process=self._pre_process,
                risk_factors=train_data[self._neutralized_risk].values.astype(
                    float) if self._neutralized_risk is not None else None,
                post_process=self._post_process)
            X = pd.DataFrame(ne_x, columns=self._alpha_model.formulas.names)
            Y = ne_y

            kd_logger.info("start train {} model".format(d))
            base_model.fit(X, Y)
            models[d] = base_model
        return models

    def run(self, begin_date, end_date, codes=None):
        kd_logger.info("start service")
        start_date = advanceDateByCalendar(
            'china.sse', begin_date,
            "-{}b".format(self._batch + self._freq + 1),
            BizDayConventions.Following)
        if self._factors_data is None:
            factors_data = self.fetch_factors(begin_date=start_date,
                                              end_date=end_date,
                                              codes=codes)
        else:
            factors_data = self._factors_data.copy()

        industry_data = self.fetch_industry(begin_date=start_date,
                                            end_date=end_date,
                                            codes=codes)

        ## 中位数填充
        factors_data = self.industry_fillna(industry_data=industry_data,
                                            factors_data=factors_data)
        factors_data = factors_data.sort_values(by=['trade_date', 'code'])
        ### 因子换算
        factors_data = self._alpha_model.formulas.transform(
            'code', factors_data.set_index('trade_date'))

        yields_data = self.fetch_yields(begin_date=start_date,
                                        end_date=end_date,
                                        codes=codes)

        if self._neutralized_risk is not None:
            risk_data = self.fetch_risk(begin_date=start_date,
                                        end_date=end_date,
                                        codes=codes)
            total_data = factors_data.merge(yields_data,
                                            on=['trade_date', 'code']).merge(
                                                risk_data,
                                                on=['trade_date', 'code'])
        else:
            total_data = factors_data.merge(yields_data,
                                            on=['trade_date', 'code'])

        return self.create_models(total_data=total_data,
                                  begin_date=begin_date,
                                  end_date=end_date)
