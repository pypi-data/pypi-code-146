# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.efficient_frontier_solver import EF
from hbshare.fe.asset_allocation.data_loader import Loader
from hbshare.fe.common.util.exception import InputParameterError
from hbshare.fe.common.util.logger import logger
from hbshare.fe.common.util.verifier import verify_type
from numpy import linalg as la
from scipy import linalg
import numpy as np
import pandas as pd


def isPD(A):
    try:
        _ = la.cholesky(A)
        return True
    except la.LinAlgError:
        return False

def nearestPD(A):
    B = (A + A.T) / 2.0
    _, s, V = la.svd(B)
    H = np.dot(V.T, np.dot(np.diag(s), V))
    A2 = (B + H) / 2.0
    A3 = (A2 + A2.T) / 2.0
    if isPD(A3):
        return A3

def correct_cov(cov):
    if not isPD(cov):
        cov = nearestPD(cov)
    min_eig = np.min(np.real(np.linalg.eigvals(cov)))
    if min_eig < 0:
        cov -= 10 * min_eig * np.eye(*cov.shape)
    return cov

class EfficientFrontier:
    def __init__(self, asset_type, asset_list, method, start_date, end_date, is_reblance, reblance_type, n, frequency, compute_return_days, compute_risk_days,
                 w_eq=None, risk_aversion=0.01, tau=0.01, P=np.array([]), Q=np.array([]), omega=np.array([]), risk_free_rate=0.03):
        self.asset_type = asset_type
        self.asset_list = asset_list
        self.method = method
        self.start_date = start_date
        self.end_date = end_date
        self.is_reblance = is_reblance
        self.reblance_type = reblance_type
        self.n = n
        self.frequency = frequency
        self.compute_return_days = compute_return_days
        self.compute_risk_days = compute_risk_days
        self.w_eq = w_eq if w_eq is not None else [1.0 / len(self.asset_list)] * len(self.asset_list)
        self.w_eq = [w / sum(self.w_eq) for w in self.w_eq]
        self.risk_aversion = risk_aversion
        self.tau = tau
        self.P = np.matrix(P)
        self.Q = np.matrix(Q).T
        self.omega = np.matrix(omega)
        self.risk_free_rate = risk_free_rate
        self._verify_input_param()
        self._load()
        self._init_data()

    def _verify_input_param(self):
        verify_type(self.asset_type, 'asset_type', str)
        verify_type(self.asset_list, 'asset_list', list)
        verify_type(self.method, 'method', str)
        verify_type(self.start_date, 'start_date', str)
        verify_type(self.end_date, 'end_date', str)
        verify_type(self.is_reblance, 'is_reblance', bool)
        verify_type(self.reblance_type, 'reblance_type', str)
        verify_type(self.n, 'n', int)
        verify_type(self.frequency, 'frequency', str)
        verify_type(self.compute_return_days, 'compute_return_days', int)
        verify_type(self.compute_risk_days, 'compute_risk_days', int)
        if self.method == 'black_litterman':
            verify_type(self.w_eq, 'w_eq', list)
            verify_type(self.risk_aversion, 'risk_aversion', float)
            verify_type(self.tau, 'tau', float)
            verify_type(self.P, 'P', np.matrix)
            verify_type(self.Q, 'Q', np.matrix)
            verify_type(self.omega, 'omega', np.matrix)
        verify_type(self.risk_free_rate, 'risk_free_rate', float)
        if self.asset_type not in ['index', 'fund']:
            msg = "asset_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.asset_list) == 0:
            msg = "asset_list is empty, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.method not in ['simple', 'risk_parity', 'risk_budget', 'max_return', 'min_risk', 'max_utility', 'max_sr', 'max_ir', 'black_litterman']:
            msg = "method not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.reblance_type not in ['init_weight', 'init_target']:
            msg = "reblance_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.n <= 0:
            msg = "n must be larger than 0, check your input"
            logger.error(msg)
        if self.frequency not in ['day', 'week', 'month', 'quarter', 'year']:
            msg = "frequency not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.compute_return_days <= 0:
            msg = "compute_return_days must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.compute_risk_days <= 0:
            msg = "compute_risk_days must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.method == 'black_litterman':
            if len([i for i in self.w_eq if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
                msg = "w_eq must be between 0 and 1, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)
            if self.risk_aversion <= 0:
                msg = "risk_aversion must be larger than 0, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)
            if self.tau <= 0:
                msg = "tau must be larger than 0, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)
            if (self.P.shape[0] != self.Q.shape[0]) or (self.P.shape[1] != len(self.asset_list)) or (self.Q.shape[1] != 1):
                msg = "the dimension of view matrix error, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)
            if (self.omega.shape[0] != self.P.shape[0]) or (self.omega.shape[1] != self.P.shape[0]) or not (np.all(self.omega == np.diag(np.diagonal(self.omega)))) or np.any(np.diagonal(self.omega) == 0.0):
                msg = "the confidence matrix error, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)
        if self.risk_free_rate <= 0:
            msg = "risk_free_rate must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)

    def _load(self):
        self.calendar_df = Loader().read_cal('19900101', self.end_date)
        self.calendar_df = self.calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
        self.calendar_df['CALENDAR_DATE'] = self.calendar_df['CALENDAR_DATE'].astype(str)
        self.calendar_df = self.calendar_df.sort_values('CALENDAR_DATE')
        self.calendar_df['IS_OPEN'] = self.calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
        self.calendar_df['IS_WEEK_END'] = self.calendar_df['IS_WEEK_END'].fillna(0).astype(int)
        self.calendar_df['IS_MONTH_END'] = self.calendar_df['IS_MONTH_END'].fillna(0).astype(int)
        self.calendar_df['YEAR_MONTH'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
        self.calendar_df['MONTH'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
        self.calendar_df['MONTH_DAY'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
        self.calendar_df['IS_QUARTER_END'] = np.where((self.calendar_df['IS_MONTH_END'] == 1) & (self.calendar_df['MONTH'].isin(['03', '06', '09', '12'])), 1, 0)
        self.calendar_df['IS_QUARTER_END'] = self.calendar_df['IS_QUARTER_END'].astype(int)
        self.calendar_df['IS_SEASON_END'] = np.where(self.calendar_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231']), 1, 0)
        self.calendar_df['IS_SEASON_END'] = self.calendar_df['IS_SEASON_END'].astype(int)
        self.trade_cal = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]
        self.trade_cal['TRADE_DATE'] = self.trade_cal['CALENDAR_DATE']
        self.calendar_df = self.calendar_df.merge(self.trade_cal[['CALENDAR_DATE', 'TRADE_DATE']], on=['CALENDAR_DATE'], how='left')
        self.calendar_df['TRADE_DATE'] = self.calendar_df['TRADE_DATE'].fillna(method='ffill')
        self.calendar_df = self.calendar_df[['CALENDAR_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END', 'IS_QUARTER_END', 'IS_SEASON_END', 'TRADE_DATE', 'YEAR_MONTH', 'MONTH', 'MONTH_DAY']]

        self.window = max(self.compute_return_days, self.compute_risk_days)
        self.start_date_backup = self.trade_cal[self.trade_cal['TRADE_DATE'] <= self.start_date]['TRADE_DATE'].unique().tolist()[-self.window - 20]

        if self.asset_type == 'index':
            self.mutual_index_nav_df = Loader().read_mutual_index_daily_k_given_indexs(self.asset_list, self.start_date_backup, self.end_date)
            self.mutual_index_nav_df = self.mutual_index_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.mutual_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.mutual_index_nav_df = self.mutual_index_nav_df.drop_duplicates()
            self.mutual_index_nav_df['TRADE_DATE'] = self.mutual_index_nav_df['TRADE_DATE'].astype(str)
            self.mutual_index_nav_df = self.mutual_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.mutual_index_nav_df = self.mutual_index_nav_df.sort_index()

            self.private_index_nav_df = Loader().read_private_index_daily_k_given_indexs(self.asset_list, self.start_date_backup[:6], self.end_date[:6])
            self.private_index_nav_df = self.private_index_nav_df[['INDEX_CODE', 'TRADE_MONTH', 'CLOSE_INDEX']] if len(self.private_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_MONTH', 'CLOSE_INDEX'])
            self.private_index_nav_df = self.private_index_nav_df.drop_duplicates()
            self.private_index_nav_df['TRADE_MONTH'] = self.private_index_nav_df['TRADE_MONTH'].astype(str)
            self.private_index_nav_df = self.private_index_nav_df.merge(self.calendar_df[self.calendar_df['IS_MONTH_END'] == 1][['YEAR_MONTH', 'TRADE_DATE']].rename(columns={'YEAR_MONTH': 'TRADE_MONTH'}), on=['TRADE_MONTH'], how='left')
            self.private_index_nav_df = self.private_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.private_index_nav_df = self.private_index_nav_df.sort_index()

            self.market_index_nav_df = Loader().read_market_index_daily_k_given_indexs(self.asset_list, self.start_date_backup, self.end_date)
            self.market_index_nav_df = self.market_index_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.market_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.market_index_nav_df = self.market_index_nav_df.drop_duplicates()
            self.market_index_nav_df['TRADE_DATE'] = self.market_index_nav_df['TRADE_DATE'].astype(str)
            self.market_index_nav_df = self.market_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.market_index_nav_df = self.market_index_nav_df.sort_index()

            self.nav_df = pd.concat([self.mutual_index_nav_df, self.private_index_nav_df, self.market_index_nav_df], axis=1)
            for asset in [asset for asset in self.asset_list if asset not in self.nav_df.columns]:
                self.nav_df[asset] = np.nan
            self.nav_df = self.nav_df[self.asset_list].sort_index()

        if self.asset_type == 'fund':
            self.mutual_fund_nav_df = Loader().read_mutual_fund_cumret_given_codes(self.asset_list, self.start_date_backup, self.end_date)
            self.mutual_fund_nav_df = self.mutual_fund_nav_df[['FUND_CODE', 'TRADE_DATE', 'CUM_RET']] if len(self.mutual_fund_nav_df) != 0 else pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'CUM_RET'])
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.drop_duplicates()
            self.mutual_fund_nav_df['TRADE_DATE'] = self.mutual_fund_nav_df['TRADE_DATE'].astype(str)
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.pivot(index='TRADE_DATE', columns='FUND_CODE', values='CUM_RET')
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.sort_index()
            self.mutual_fund_nav_df = 0.01 * self.mutual_fund_nav_df + 1

            self.private_fund_nav_df = Loader().read_private_fund_adj_nav_given_codes(self.asset_list, self.start_date_backup, self.end_date)
            self.private_fund_nav_df = self.private_fund_nav_df[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']] if len(self.private_fund_nav_df) != 0 else pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV'])
            self.private_fund_nav_df = self.private_fund_nav_df.drop_duplicates()
            self.private_fund_nav_df['TRADE_DATE'] = self.private_fund_nav_df['TRADE_DATE'].astype(str)
            self.private_fund_nav_df = self.private_fund_nav_df.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV')
            self.private_fund_nav_df = self.private_fund_nav_df.sort_index()

            self.nav_df = pd.concat([self.mutual_fund_nav_df, self.private_fund_nav_df], axis=1)
            for asset in [asset for asset in self.asset_list if asset not in self.nav_df.columns]:
                self.nav_df[asset] = np.nan
            self.nav_df = self.nav_df[self.asset_list].sort_index()
        return

    def _init_data(self):
        # 确定再平衡时点
        self.start_trade_date = self.calendar_df[self.calendar_df['CALENDAR_DATE'] == self.start_date]['TRADE_DATE'].values[0]
        if not self.is_reblance:
            reblance_list = [self.start_trade_date]
        else:
            if self.frequency == 'day':
                reblance_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                reblance_list = reblance_list[::self.n]
            elif self.frequency == 'week':
                reblance_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                reblance_list = reblance_list[::self.n * 5]
            elif self.frequency == 'month':
                reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                reblance_list = reblance_list[::self.n]
                reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
            elif self.frequency == 'quarter':
                reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                reblance_list = reblance_list[::self.n * 3]
                reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
            elif self.frequency == 'year':
                reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                reblance_list = reblance_list[::self.n * 12]
                reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
            else:
                reblance_list = [self.start_trade_date]

        # 确定每个再平衡时点所需数据
        trading_day_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
        if self.asset_type == 'index' and len(self.private_index_nav_df) > 0:
            date_list = self.calendar_df[self.calendar_df['IS_MONTH_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 12
        elif self.asset_type == 'fund' and len(self.private_fund_nav_df) > 0:
            date_list = self.calendar_df[self.calendar_df['IS_WEEK_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 52
        else:
            date_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 250
        preprocessed_data = dict()
        if not (self.nav_df.empty or self.nav_df.reindex(date_list).interpolate().dropna().empty or self.nav_df.dropna(axis=1, how='all').shape[1] != len(self.asset_list)):
            nav_df = self.nav_df.reindex(date_list).interpolate().dropna().sort_index()
            nav_df = nav_df / nav_df.iloc[0]
            ret_df = nav_df.pct_change().dropna()
            for date in reblance_list:
                if self.method != 'black_litterman':
                    interval_data = dict()
                    ret_start = [td for td in trading_day_list if td <= date][-self.compute_return_days]
                    cov_start = [td for td in trading_day_list if td <= date][-self.compute_risk_days]
                    end = date
                    interval_data['ret_df'] = pd.DataFrame(ret_df[(ret_df.index >= ret_start) & (ret_df.index <= end)].mean() * self.q)
                    interval_data['cov_df'] = ret_df[(ret_df.index >= cov_start) & (ret_df.index <= end)].cov() * self.q
                    interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                    preprocessed_data[date] = interval_data
                else:
                    interval_data = dict()
                    start = [td for td in trading_day_list if td <= date][-self.compute_risk_days]
                    end = date
                    cov_df_prior = ret_df[(ret_df.index >= start) & (ret_df.index <= end)].cov() * self.q
                    cov_df_prior = correct_cov(cov_df_prior)
                    cov_df_prior = np.matrix(cov_df_prior)
                    interval_data['cov_df'] = linalg.inv(self.tau * cov_df_prior) + self.P.T * linalg.inv(self.omega) * self.P
                    interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                    interval_data['cov_df'] = linalg.inv(interval_data['cov_df'])
                    w_eq = np.matrix(self.w_eq).T  # if self.w_eq is not None else get_w_eq(self.asset_type, self.asset_list, date)
                    ret_df_prior = self.risk_aversion * cov_df_prior * w_eq
                    interval_data['ret_df'] = interval_data['cov_df'] * (linalg.inv(self.tau * cov_df_prior) * ret_df_prior + self.P.T * linalg.inv(self.omega) * self.Q)
                    interval_data['ret_df'] = pd.DataFrame(interval_data['ret_df'])
                    interval_data['cov_df'] = pd.DataFrame(interval_data['cov_df'])
                    preprocessed_data[date] = interval_data
        else:
            for date in reblance_list:
                interval_data = dict()
                interval_data['ret_df'] = pd.DataFrame()
                interval_data['cov_df'] = pd.DataFrame()
                preprocessed_data[date] = interval_data
        self.preprocessed_data = preprocessed_data
        return

    def get_all(self):
        ef_weight_list = []
        for date, period_data in self.preprocessed_data.items():
            if period_data['ret_df'].empty or period_data['cov_df'].empty:
                logger.warning("{0}: ret_df or cov_df is empty !".format(date))
                ef_weight = pd.DataFrame(columns=['date', 'group'] + self.asset_list + ['cash', 'sigma', 'r'])
            else:
                self.ret = period_data['ret_df']
                self.cov = period_data['cov_df']
                ef_weight = EF(date, self.asset_list, self.ret, self.cov, self.risk_free_rate, pd.DataFrame(index=[date], columns=self.asset_list + ['cash'])).solve()
                ef_weight = ef_weight.reset_index().rename(columns={'index': 'group'})
                ef_weight['date'] = date
                ef_weight = ef_weight[['date', 'group'] + self.asset_list + ['cash', 'sigma', 'r']]
            ef_weight_list.append(ef_weight)
            print('[{0}]/efficient frontier done'.format(date))
        ef_weight_df = pd.concat(ef_weight_list)
        # 权重归一化（本版本不支持有现金配置）
        ef_weight_df['TOTAL'] = ef_weight_df[self.asset_list].sum(axis=1)
        ef_weight_df[self.asset_list] = ef_weight_df[self.asset_list + ['TOTAL']].apply(lambda x: x.iloc[:len(self.asset_list)] / x[-1], axis=1)
        ef_weight_df = ef_weight_df[['date', 'group'] + self.asset_list + ['sigma', 'r']]
        return ef_weight_df


if __name__ == '__main__':
    # mutual_index: ['HM0001', 'HM0024', 'HM0095']
    # private_index: ['HB0000', 'HB0016', 'HB1001']
    # market_index: ['000300', '000906', 'CBA00301']
    # mutual_fund: ['002943', '688888', '000729']
    # private_fund: ['SGK768', 'SX8958', 'SR4480']

    ef_weight_df = EfficientFrontier(asset_type='index',  # index, fund
                                     asset_list=['000300', '000906', 'CBA00301'],
                                     method='max_return',  # [simple, risk_parity, risk_budget, max_return, min_risk, max_utility, max_sr, max_ir, black_litterman
                                     start_date='20181231',
                                     end_date='20220704',
                                     is_reblance=True,   # True, False
                                     reblance_type='init_target',  # init_weight，init_target
                                     n=3,
                                     frequency='month',  # day, week, month, quarter, year
                                     compute_return_days=120,  # 交易日
                                     compute_risk_days=120,  # 交易日
                                     risk_free_rate=0.03
                                     ).get_all()
    print(ef_weight_df)