# -*- encoding:utf-8 -*-
import datetime
import pandas as pd
from jdw import DBAPI
from jdw.mfc.lombard.indicator.atr import atr14, atr21
from jdw.mfc.lombard.indicator.symbol_pd import _benchmark


class Base(object):

    def __init__(self, market_trade_year=252):
        self._kd_engine = DBAPI.FetchEngine.create_engine('kd')
        self._market_trade_year = market_trade_year

    def calc_atr(self, kline_df):
        kline_df['atr21'] = 0
        if kline_df.shape[0] > 21:
            # 大于21d计算atr21
            kline_df['atr21'] = atr21(kline_df['high'].values,
                                      kline_df['low'].values,
                                      kline_df['pre_close'].values)
            # 将前面的bfill
            kline_df['atr21'].fillna(method='bfill', inplace=True)
        kline_df['atr14'] = 0
        if kline_df.shape[0] > 14:
            # 大于14d计算atr14
            kline_df['atr14'] = atr14(kline_df['high'].values,
                                      kline_df['low'].values,
                                      kline_df['pre_close'].values)
            # 将前面的bfill
            kline_df['atr14'].fillna(method='bfill', inplace=True)

    def transform(self, market_data):
        market_data['date'] = pd.to_datetime(
            market_data['trade_date']).dt.strftime('%Y%m%d').astype(int)
        market_data['date_week'] = market_data['date'].apply(
            lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').weekday())
        market_data['trade_date'] = pd.to_datetime(market_data['trade_date'])
        market_data['p_change'] = market_data['p_change'] * 100
        market_data = market_data.dropna(subset=['pre_close'])
        return market_data

    def transform_benchmark(self, index_data, n_fold):
        benchmark_kl_pd = index_data.set_index('trade_date')
        benchmark_kl_pd['key'] = list(range(0, len(benchmark_kl_pd)))
        self.calc_atr(benchmark_kl_pd)
        ind = benchmark_kl_pd.key.values[
            -1] - self._market_trade_year * n_fold + 1
        start_date = benchmark_kl_pd.index[ind]
        benchmark_kl_pd = benchmark_kl_pd.loc[start_date:]
        benchmark_kl_pd.name = str('benchmark')
        return benchmark_kl_pd