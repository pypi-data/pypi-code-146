# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.risk_parity_budget_solver import RiskParity, RiskBudget
from hbshare.fe.asset_allocation.data_loader import Loader
from hbshare.fe.common.util.exception import InputParameterError
from hbshare.fe.common.util.logger import logger
from hbshare.fe.common.util.verifier import verify_type
from multiprocessing import Pool
from numpy import linalg as la
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
    spacing = np.spacing(la.norm(A))
    I = np.eye(A.shape[0])
    k = 1
    while not isPD(A3):
        mineig = np.min(np.real(la.eigvals(A3)))
        A3 += I * (-mineig * k**2 + spacing)
        k += 1
    return A3

def correct_cov(cov):
    if not isPD(cov):
        cov = nearestPD(cov)
    min_eig = np.min(np.real(np.linalg.eigvals(cov)))
    if min_eig < 0:
        cov -= 10 * min_eig * np.eye(*cov.shape)
    return cov

class RiskParityBudget:
    def __init__(self, asset_type, asset_list, method, start_date, end_date, is_reblance, reblance_type, n, frequency, compute_risk_days,
                 lb_list=None, ub_list=None, total_weight=None, risk_budget_list=None, processes=16):
        self.asset_type = asset_type
        self.asset_list = asset_list
        self.method = method
        self.start_date = start_date
        self.end_date = end_date
        self.is_reblance = is_reblance
        self.reblance_type = reblance_type
        self.n = n
        self.frequency = frequency
        self.compute_risk_days = compute_risk_days
        self.lb_list = [0.0] * len(self.asset_list) if lb_list is None or lb_list == [] else lb_list
        self.ub_list = [1.0] * len(self.asset_list) if ub_list is None or ub_list == [] else ub_list
        self.total_weight = 1.0 if total_weight is None else total_weight
        self.risk_budget_list = [1.0 / len(self.asset_list)] * len(self.asset_list) if risk_budget_list is None or risk_budget_list == [] else risk_budget_list
        self.risk_budget_list = [budget / sum(self.risk_budget_list) for budget in self.risk_budget_list]
        self.processes = processes
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
        verify_type(self.compute_risk_days, 'compute_risk_days', int)
        verify_type(self.lb_list, 'lb_list', list)
        verify_type(self.ub_list, 'ub_list', list)
        verify_type(self.total_weight, 'total_weight', float)
        verify_type(self.risk_budget_list, 'risk_budget_list', list)
        verify_type(self.processes, 'processes', int)
        if self.asset_type not in ['index', 'fund']:
            msg = "asset_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.asset_list) == 0:
            msg = "asset_list is empty, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.method not in ['risk_parity', 'risk_budget']:
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
            raise InputParameterError(message=msg)
        if self.frequency not in ['day', 'week', 'month', 'quarter', 'year']:
            msg = "frequency not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.compute_risk_days <= 0:
            msg = "compute_risk_days must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.lb_list) != len(self.asset_list) or len(self.ub_list) != len(self.asset_list):
            msg = "lb_list or ub_list must be the same length with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.lb_list if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "lb must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.ub_list if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "ub must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if not (self.total_weight >= 0.0 and self.total_weight <= 1.0):
            msg = "total_weight must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.risk_budget_list) != len(self.asset_list):
            msg = "risk_budget_list must be the same length with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.risk_budget_list if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "risk_budget must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.processes <= 0:
            msg = "processes must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)

    def _load(self):
        self.calendar_df = Loader().read_cal('19900101', self.end_date)
        self.calendar_df = self.calendar_df.rename(columns={'jyrq': 'CALENDAR_DATE', 'sfjj': 'IS_OPEN', 'sfzm': 'IS_WEEK_END', 'sfym': 'IS_MONTH_END'})
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

        self.window = self.compute_risk_days
        self.start_date_backup = self.trade_cal[self.trade_cal['TRADE_DATE'] <= self.start_date]['TRADE_DATE'].unique().tolist()[-self.window - 40]

        if self.asset_type == 'index':
            self.mutual_index_nav_df = Loader().read_mutual_index_daily_k_given_indexs(self.asset_list, self.start_date_backup, self.end_date)
            self.mutual_index_nav_df = self.mutual_index_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.mutual_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.mutual_index_nav_df = self.mutual_index_nav_df.drop_duplicates()
            self.mutual_index_nav_df['TRADE_DATE'] = self.mutual_index_nav_df['TRADE_DATE'].astype(str)
            self.mutual_index_nav_df = self.mutual_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.mutual_index_nav_df = self.mutual_index_nav_df.sort_index()

            self.private_index_nav_df = Loader().read_private_index_daily_k_given_indexs(self.asset_list, self.start_date_backup, self.end_date)
            self.private_index_nav_df = self.private_index_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.private_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.private_index_nav_df = self.private_index_nav_df.drop_duplicates()
            self.private_index_nav_df['TRADE_DATE'] = self.private_index_nav_df['TRADE_DATE'].astype(str)
            self.private_index_nav_df = self.private_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.private_index_nav_df = self.private_index_nav_df.sort_index()

            self.market_index_nav_df = Loader().read_market_index_daily_k_given_indexs(self.asset_list, self.start_date_backup, self.end_date)
            self.market_index_nav_df = self.market_index_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.market_index_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.market_index_nav_df = self.market_index_nav_df.drop_duplicates()
            self.market_index_nav_df['TRADE_DATE'] = self.market_index_nav_df['TRADE_DATE'].astype(str)
            self.market_index_nav_df = self.market_index_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.market_index_nav_df = self.market_index_nav_df.sort_index()

            self.nav_df = pd.concat([self.mutual_index_nav_df, self.private_index_nav_df, self.market_index_nav_df], axis=1)

        if self.asset_type == 'fund':
            self.mutual_fund_nav_df = Loader().read_mutual_fund_cumret_given_codes(self.asset_list, self.start_date_backup, self.end_date)
            self.mutual_fund_nav_df = self.mutual_fund_nav_df[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']] if len(self.mutual_fund_nav_df) != 0 else pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV'])
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.drop_duplicates()
            self.mutual_fund_nav_df['TRADE_DATE'] = self.mutual_fund_nav_df['TRADE_DATE'].astype(str)
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV')
            self.mutual_fund_nav_df = self.mutual_fund_nav_df.sort_index()

            self.private_fund_nav_df = Loader().read_private_fund_adj_nav_given_codes(self.asset_list, self.start_date_backup, self.end_date)
            self.private_fund_nav_df = self.private_fund_nav_df[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']] if len(self.private_fund_nav_df) != 0 else pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV'])
            self.private_fund_nav_df = self.private_fund_nav_df.drop_duplicates()
            self.private_fund_nav_df['TRADE_DATE'] = self.private_fund_nav_df['TRADE_DATE'].astype(str)
            self.private_fund_nav_df = self.private_fund_nav_df.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV')
            self.private_fund_nav_df = self.private_fund_nav_df.sort_index()

            self.nav_df = pd.concat([self.mutual_fund_nav_df, self.private_fund_nav_df], axis=1)

        nan_nav_list = [asset for asset in self.asset_list if asset not in self.nav_df.columns]
        if len(nan_nav_list) == 0:
            self.nav_df = self.nav_df[self.asset_list].sort_index()
        else:
            msg = "{0} no nav data".format(','.join(nan_nav_list))
            logger.error(msg)
            raise InputParameterError(message=msg)
        return

    def _init_data(self):
        # 确定再平衡时点
        if len(self.trade_cal[(self.trade_cal['TRADE_DATE'] >= self.start_date) & (self.trade_cal['TRADE_DATE'] <= self.end_date)]) == 0:
            msg = "no reblance dates between start_date and end_date, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        else:
            self.start_trade_date = self.trade_cal[self.trade_cal['TRADE_DATE'] >= self.start_date]['TRADE_DATE'].values[0]
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
            date_list = self.calendar_df[self.calendar_df['IS_WEEK_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 52
        elif self.asset_type == 'fund' and len(self.private_fund_nav_df) > 0:
            date_list = self.calendar_df[self.calendar_df['IS_WEEK_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 52
        else:
            date_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 250
        preprocessed_data = dict()
        self.reason_df = pd.DataFrame(index=reblance_list, columns=['原因'])
        if not (self.nav_df.empty or self.nav_df.reindex(date_list).interpolate().dropna(how='all').empty or self.nav_df.dropna(axis=1, how='all').shape[1] != len(self.asset_list)):
            nav_df = self.nav_df.reindex(date_list).interpolate().dropna(how='all').sort_index()
            ret_df = nav_df.pct_change().dropna(how='all')
            for date in reblance_list:
                interval_data = dict()
                start = [td for td in trading_day_list if td <= date][-self.compute_risk_days]
                end = date
                need_length = len(ret_df[(ret_df.index >= start) & (ret_df.index < end)])
                density = [len(self.nav_df[(self.nav_df.index >= start) & (self.nav_df.index < end)][[asset]].dropna()) / float(need_length) if need_length != 0 else 0.0 for asset in self.asset_list]
                if min(density) < 0.3:
                    density_ser = pd.Series(density)
                    density_ser = density_ser[density_ser < 0.3]
                    self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期风险！'.format(date, ','.join([self.asset_list[i] for i in density_ser.index.tolist()]))
                    interval_data['cov_df'] = pd.DataFrame()
                    preprocessed_data[date] = interval_data
                else:
                    interval_data['cov_df'] = ret_df[(ret_df.index >= start) & (ret_df.index < end)].cov() * self.q
                    interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                    preprocessed_data[date] = interval_data
        else:
            for date in reblance_list:
                self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期风险！'.format(date, ','.join(self.asset_list))
                interval_data = dict()
                interval_data['cov_df'] = pd.DataFrame()
                preprocessed_data[date] = interval_data
        self.preprocessed_data = preprocessed_data
        # cov_df_list = []
        # for date in sorted(list(self.preprocessed_data.keys())):
        #     cov_df_list.append(self.preprocessed_data[date]['cov_df'])
        # all_cov_df = pd.concat(cov_df_list)
        # if len(all_cov_df) == 0:
        #     print('no enough nav data for computing risk model!')
        return

    def get_optimal_one_process(self, date, period_data):
        if period_data['cov_df'].empty:
            weight = pd.DataFrame(index=[date], columns=self.asset_list + ['cash'])
            status = pd.DataFrame(index=[date], columns=['优化状态'], data=['infeasible'])
            status = status.merge(self.reason_df, left_index=True, right_index=True, how='left')
        else:
            try:
                if self.method == 'risk_parity':
                    self.cov = period_data['cov_df']
                    weight, status = RiskParity(self.asset_list, self.cov, self.lb_list, self.ub_list, self.total_weight).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
                else:
                    self.cov = period_data['cov_df']
                    weight, status = RiskBudget(self.asset_list, self.cov, self.lb_list, self.ub_list, self.total_weight, self.risk_budget_list).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
            except:
                weight = pd.DataFrame(index=[date], columns=self.asset_list + ['cash'])
                status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[['infeasible', '{0}：模型当期无优化解！'.format(date)]])
        print('[{0}]/[{1}] done'.format(date, self.method))
        return weight, status

    def get_all(self):
        result_list = []
        p = Pool(processes=self.processes)
        for date, period_data in self.preprocessed_data.items():
            result = p.apply_async(self.get_optimal_one_process, args=(date, period_data))
            result_list.append(result)
        p.close()
        p.join()
        print('processes done.')
        weight_list, status_list = [], []
        for result in result_list:
            weight, status = result.get()
            weight_list.append(weight)
            status_list.append(status)
        weight_df = pd.concat(weight_list).sort_index()
        status_df = pd.concat(status_list).sort_index()
        # 权重归一化（本版本不支持有现金配置）
        weight_df = weight_df[self.asset_list]
        weight_df['TOTAL'] = weight_df.sum(axis=1)
        weight_df['TOTAL'] = weight_df['TOTAL'].replace(0.0, np.nan)
        weight_df = weight_df.apply(lambda x: x.iloc[:len(self.asset_list)] / x[-1], axis=1)
        if self.reblance_type == 'init_weight' and len(weight_df.dropna()) != 0:
            start_index = weight_df.dropna().index[0]
            weight_df.loc[weight_df.index > start_index, :] = np.nan
            weight_df = weight_df.fillna(method='ffill')
            status_df.loc[status_df.index > start_index, :] = np.nan
            status_df = status_df.fillna(method='ffill')
        # if len(weight_df.dropna()) == 0:
        #     print('no optimal results!')
        return weight_df, status_df


if __name__ == '__main__':
    # mutual_index: ['HM0001', 'HM0024', 'HM0095']
    # private_index: ['HB0011', 'HB0016', 'HB1001']
    # market_index: ['000300', '000906', 'CBA00301']
    # mutual_fund: ['002943', '688888', '000729']
    # private_fund: ['SGK768', 'SX8958', 'SR4480']

    weight_df, status_df = RiskParityBudget(asset_type='index',  # index, fund
                                            asset_list=['000300', '000906', 'CBA00301'],
                                            method='risk_parity',  # risk_parity, risk_budget
                                            start_date='20181231',
                                            end_date='20220704',
                                            is_reblance=True,   # True, False
                                            reblance_type='init_target',  # init_weight, init_target
                                            n=3,
                                            frequency='month',  # day, week, month, quarter, year
                                            compute_risk_days=120,  # 交易日
                                            processes=4
                                            ).get_all()
    print(weight_df, status_df)