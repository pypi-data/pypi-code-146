# -*- coding: utf-8 -*-
import abc
from typing import List
from sqlalchemy import select, and_, join
from sqlalchemy.ext.automap import automap_base
import pandas as pd
from jdw.data.SurfaceAPI.engine import FetchKDEngine
from jdw.data.DataAPI.db.kd.kd_engine import risk_styles, industry_styles

macro_styles = ['COUNTRY']

total_risk_factors = risk_styles + industry_styles + macro_styles


class BaseRiskModel(metaclass=abc.ABCMeta):

    def get_risk_profile(self):
        pass


class FactorRiskModel(BaseRiskModel):

    def __init__(self, factor_cov: pd.DataFrame, risk_exp: pd.DataFrame,
                 idsync: pd.Series):
        self.factor_cov = factor_cov
        self.idsync = idsync
        self.codes = self.idsync.index.tolist()
        self.factor_names = sorted(self.factor_cov.index)
        self.risk_exp = risk_exp.loc[self.codes, self.factor_names]
        self.factor_cov = self.factor_cov.loc[self.factor_names,
                                              self.factor_names]
        self.idsync = self.idsync[self.codes]

    def get_risk_exp(self, codes: List[int] = None):
        if codes:
            return self.risk_exp.loc[codes, :].values
        else:
            return self.risk_exp.values

    def get_factor_cov(self):
        return self.factor_cov.values

    def get_idsync(self, codes: List[int] = None):
        if codes:
            return self.idsync[codes].values
        else:
            return self.idsync.values

    def get_risk_profile(self, codes: List[int] = None):
        return dict(cov=None,
                    factor_cov=self.get_factor_cov(),
                    factor_loading=self.get_risk_exp(codes),
                    idsync=self.get_idsync(codes))


class RiskModel(object):

    def __init__(self, risk_model=None):
        self._engine = FetchKDEngine()
        self._risk_model = risk_model if risk_model is not None else 'day'

    def map_risk_model_table(self):
        risk_cov_table = self._engine.table_model('risk_cov_{0}'.format(
            self._risk_model))
        special_risk_table = self._engine.table_model(
            'specific_risk_{0}'.format(self._risk_model))
        return risk_cov_table, special_risk_table

    def universe_risk(self, universe, start_date, end_date):
        risk_cov_table, special_risk_table = self.map_risk_model_table()
        RiskExposure = self._engine.table_model('risk_exposure')

        risk_exposure_cols = [
            RiskExposure.__table__.columns[f] for f in total_risk_factors
        ]

        cond = universe._query_statements(start_date, end_date)

        big_table = join(
            RiskExposure, universe._table_model,
            and_(RiskExposure.trade_date == universe._table_model.trade_date,
                 RiskExposure.code == universe._table_model.code, cond))

        big_table = join(
            special_risk_table, big_table,
            and_(RiskExposure.code == special_risk_table.code,
                 RiskExposure.trade_date == special_risk_table.trade_date,
                 RiskExposure.flag == 1, special_risk_table.flag == 1))

        query = select(
            [RiskExposure.trade_date,
             RiskExposure.code,
             special_risk_table.SRISK.label('srisk')] + risk_exposure_cols).select_from(big_table) \
            .distinct()

        risk_exp = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'code']).dropna()
        return risk_exp

    def codes_risk(self, codes, start_date, end_date):
        _, special_risk_table = self.map_risk_model_table()

        RiskExposure = self._engine.table_model('risk_exposure')

        risk_exposure_cols = [
            RiskExposure.__table__.columns[f] for f in total_risk_factors
        ]

        big_table = join(
            RiskExposure, special_risk_table,
            and_(RiskExposure.code == special_risk_table.code,
                 RiskExposure.trade_date == special_risk_table.trade_date))

        query = select([RiskExposure.trade_date, RiskExposure.code, special_risk_table.SRISK.label('srisk')] + risk_exposure_cols) \
            .select_from(big_table).where(
            and_(RiskExposure.trade_date.between(start_date,end_date),
                 RiskExposure.code.in_(codes)
                 ))

        risk_exp = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'code']).dropna()
        return risk_exp

    def universe_fetch(self, universe, start_date, end_date, model_type=None):
        risk_cov_table, special_risk_table = self.map_risk_model_table()
        cov_risk_cols = [
            risk_cov_table.__table__.columns[f] for f in total_risk_factors
        ]
        query = select([
            risk_cov_table.trade_date, risk_cov_table.FactorID,
            risk_cov_table.Factor
        ] + cov_risk_cols).where(
            risk_cov_table.trade_date.between(start_date, end_date))

        risk_cov = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'FactorID'])

        RiskExposure = self._engine.table_model('risk_exposure')

        risk_exposure_cols = [
            RiskExposure.__table__.columns[f] for f in total_risk_factors
        ]

        cond = universe._query_statements(start_date, end_date)

        big_table = join(
            RiskExposure, universe._table_model,
            and_(RiskExposure.trade_date == universe._table_model.trade_date,
                 RiskExposure.code == universe._table_model.code, cond))

        big_table = join(
            special_risk_table, big_table,
            and_(RiskExposure.code == special_risk_table.code,
                 RiskExposure.trade_date == special_risk_table.trade_date,
                 RiskExposure.flag == 1, special_risk_table.flag == 1))

        query = select(
            [RiskExposure.trade_date,
             RiskExposure.code,
             special_risk_table.SRISK.label('srisk')] + risk_exposure_cols).select_from(big_table) \
            .distinct()

        risk_exp = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'code']).dropna()

        if not model_type:
            return risk_cov, risk_exp
        elif model_type == 'factor':
            new_risk_cov = risk_cov.set_index('Factor')
            new_risk_exp = risk_exp.set_index('code')

            risk_cov_groups = new_risk_cov.groupby('trade_date')
            risk_exp_groups = new_risk_exp.groupby('trade_date')

            models = {}
            for ref_date, cov_g in risk_cov_groups:
                exp_g = risk_exp_groups.get_group(ref_date)
                factor_names = cov_g.index.tolist()
                factor_cov = cov_g.loc[factor_names, factor_names] / 10000.
                factor_loading = exp_g.loc[:, factor_names]
                idsync = exp_g['srisk'] * exp_g['srisk'] / 10000
                models[ref_date] = FactorRiskModel(factor_cov, factor_loading,
                                                   idsync)
            return pd.Series(models), risk_cov, risk_exp

    def codes_fetch(self, codes, start_date, end_date, model_type=None):
        risk_cov_table, special_risk_table = self.map_risk_model_table()
        cov_risk_cols = [
            risk_cov_table.__table__.columns[f] for f in total_risk_factors
        ]
        query = select([
            risk_cov_table.trade_date, risk_cov_table.FactorID,
            risk_cov_table.Factor
        ] + cov_risk_cols).where(
            risk_cov_table.trade_date.between(start_date, end_date))
        risk_cov = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'FactorID'])

        RiskExposure = self._engine.table_model('risk_exposure')

        risk_exposure_cols = [
            RiskExposure.__table__.columns[f] for f in total_risk_factors
        ]

        big_table = join(
            RiskExposure, special_risk_table,
            and_(RiskExposure.code == special_risk_table.code,
                 RiskExposure.trade_date == special_risk_table.trade_date))

        query = select([RiskExposure.trade_date, RiskExposure.code, special_risk_table.SRISK.label('srisk')] + risk_exposure_cols) \
            .select_from(big_table).where(
            and_(RiskExposure.trade_date.between(start_date,end_date),
                 RiskExposure.code.in_(codes)
                 ))

        risk_exp = pd.read_sql(query, self._engine.client()).sort_values(
            ['trade_date', 'code']).dropna()

        if not model_type:
            return risk_cov, risk_exp
        elif model_type == 'factor':
            new_risk_cov = risk_cov.set_index('Factor')
            new_risk_exp = risk_exp.set_index('code')

            risk_cov_groups = new_risk_cov.groupby('trade_date')
            risk_exp_groups = new_risk_exp.groupby('trade_date')

            models = {}
            for ref_date, cov_g in risk_cov_groups:
                exp_g = risk_exp_groups.get_group(ref_date)
                factor_names = cov_g.index.tolist()
                factor_cov = cov_g.loc[factor_names, factor_names] / 10000.
                factor_loading = exp_g.loc[:, factor_names]
                idsync = exp_g['srisk'] * exp_g['srisk'] / 10000
                models[ref_date] = FactorRiskModel(factor_cov, factor_loading,
                                                   idsync)
            return pd.Series(models), risk_cov, risk_exp
