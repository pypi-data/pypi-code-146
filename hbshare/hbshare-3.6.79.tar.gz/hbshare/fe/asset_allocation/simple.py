# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.data_loader import Loader
from hbshare.fe.common.util.exception import InputParameterError
from hbshare.fe.common.util.logger import logger
from hbshare.fe.common.util.verifier import verify_type
import numpy as np
import pandas as pd


class Simple:
    def __init__(self, asset_type, asset_list, method, start_date, end_date, is_reblance, reblance_type, n, frequency, set_w=None):
        self.asset_type = asset_type
        self.asset_list = asset_list
        self.method = method
        self.start_date = start_date
        self.end_date = end_date
        self.is_reblance = is_reblance
        self.reblance_type = reblance_type
        self.n = n
        self.frequency = frequency
        self.set_w = set_w if set_w is not None else [1.0 / len(self.asset_list)] * len(self.asset_list)
        self.set_w = [w / sum(self.set_w) for w in self.set_w]
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
        verify_type(self.set_w, 'set_w', list)
        if self.asset_type not in ['index', 'fund']:
            msg = "asset_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.asset_list) == 0:
            msg = "asset_list is empty, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.method not in ['simple']:
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
        if len(self.set_w) != len(self.asset_list):
            msg = "set_w is not the same length with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.set_w if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "set_w must be between 0 and 1, check your input"
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
            self.reblance_list = reblance_list
        return

    def get_all(self):
        weight_list, status_list = [], []
        for date in self.reblance_list:
            weight = pd.DataFrame(index=[date], columns=self.asset_list)
            weight.loc[date] = self.set_w
            status = pd.DataFrame(index=[date], columns=['优化状态'], data=['optimal'])
            weight_list.append(weight)
            status_list.append(status)
            print('[{0}]/[{1}] done'.format(date, self.method))
        weight_df = pd.concat(weight_list)
        status_df = pd.concat(status_list)
        if self.reblance_type == 'init_weight':
            start_index = weight_df.dropna().index[0]
            weight_df.loc[weight_df.index > start_index, :] = np.nan
            weight_df = weight_df.fillna(method='ffill')
            status_df.loc[status_df.index > start_index, :] = np.nan
            status_df = status_df.fillna(method='ffill')
        return weight_df, status_df


if __name__ == '__main__':
    # mutual_index: ['HM0001', 'HM0024', 'HM0095']
    # private_index: ['HB0000', 'HB0016', 'HB1001']
    # market_index: ['000300', '000906', 'CBA00301']
    # mutual_fund: ['002943', '688888', '000729']
    # private_fund: ['SGK768', 'SX8958', 'SR4480']

    weight_df, status_df = Simple(asset_type='index',  # index, fund
                                  asset_list=['000300', '000906', 'CBA00301'],
                                  method='simple',  # simple
                                  start_date='20181231',
                                  end_date='20220704',
                                  is_reblance=True,   # True, False
                                  reblance_type='init_target',  # init_weight，init_target
                                  n=3,
                                  frequency='month',  # day, week, month, quarter, year
                                  set_w=[0.3, 0.3, 0.4]
                                  ).get_all()
    print(weight_df, status_df)