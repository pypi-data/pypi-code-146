# -*- encoding:utf-8 -*-
import six
import pandas as pd
import numpy as np
from jdw import DBAPI
from jdw.kdutils.singleton import Singleton
from jdw.mfc.lombard.indicator.symbol_pd import _benchmark
from jdw.mfc.lombard.base import Base


@six.add_metaclass(Singleton)
class Futures(Base):

    def __init__(self, market_trade_year=252):
        super(Futures, self).__init__(market_trade_year=market_trade_year)

    def _prev_returs_impl(self, price_data, key, name):
        price_tb = price_data[key].unstack()
        price_tb.fillna(method='pad', inplace=True)
        return_tb = np.log(price_tb / price_tb.shift(-1))
        return_tb = return_tb.replace([np.inf, -np.inf], np.nan)
        return_tb = return_tb.stack().reindex(price_data.index)
        return_tb.name = name
        return return_tb

    def _pre_impl(self, price_data, key, name):
        price_tb = price_data[key].unstack()
        price_tb.fillna(method='pad', inplace=True)
        return_tb = price_tb.shift(-1)
        return_tb = return_tb.stack().reindex(price_data.index)
        return_tb.name = name
        return return_tb

    def transform_code(self, market_data, benchmark_kl_pd):
        pick_kl_pd_dict = {}
        choice_symbols = [code for code in market_data.code.unique().tolist()]
        for code in choice_symbols:
            kl_pd = market_data.reset_index().set_index(
                'code').loc[code].reset_index().set_index('trade_date')
            kl_pd.index = pd.to_datetime(kl_pd.index)
            if benchmark_kl_pd is not None:
                kl_pd = _benchmark(kl_pd, benchmark_kl_pd)
            self.calc_atr(kl_pd)
            kl_pd.name = str(code) + '0'
            kl_pd['key'] = list(range(0, len(kl_pd)))
            pick_kl_pd_dict[str(code) + '0'] = kl_pd
        return pick_kl_pd_dict

    def fetch_data(self, codes, benchmark, begin_date, end_date, columns):
        market_data = DBAPI.FutruesIndexMarketFactory(self._kd_engine).result(
            codes=codes + [benchmark],
            key='code',
            begin_date=begin_date,
            end_date=end_date,
            columns=columns)

        market_data = market_data.sort_values(
            by=['trade_date', 'code'], ascending=True).rename(columns={
                'CHGPct': 'chgPct',
                'CHG': 'chg'
            })
        if 'turnoverValue' in market_data.columns and 'turnoverVol' in market_data.columns:
            market_data['vwap'] = market_data['turnoverValue'] / market_data[
                'turnoverVol']

        pre_close = self._pre_impl(
            market_data.set_index(['trade_date', 'code']), 'closePrice',
            'pre_close').reset_index()
        pre_close['trade_date'] = pd.to_datetime(pre_close['trade_date'])

        prev_rets = self._prev_returs_impl(
            market_data.set_index(['trade_date', 'code']), 'closePrice',
            'pre1_ret').reset_index()
        prev_rets['trade_date'] = pd.to_datetime(prev_rets['trade_date'])

        market_data = market_data.merge(prev_rets,
                                        on=['trade_date', 'code'
                                            ]).merge(pre_close,
                                                     on=['trade_date', 'code'])

        market_data = market_data.rename(
            columns={
                'preSettlePrice': 'pre_settle',
                'openPrice': 'open',
                'highestPrice': 'high',
                'lowestPrice': 'low',
                'closePrice': 'close',
                'settlePrice': 'settle',
                'turnoverVol': 'volume',
                'turnoverValue': 'value',
                'vwap': 'vwap',
                'pre1_ret': 'p_change'
            })
        market_data = self.transform(market_data=market_data)

        index_data = DBAPI.IndexMarketFactory(self._kd_engine).result(
            codes=[benchmark],
            key='indexCode',
            begin_date=begin_date,
            end_date=end_date,
            columns=[
                'preCloseIndex', 'openIndex', 'highestIndex', 'lowestIndex',
                'closeIndex', 'turnoverVol', 'turnoverValue', 'chgPct'
            ])

        if 'turnoverValue' in index_data.columns and 'turnoverVol' in index_data.columns:
            index_data['vwap'] = index_data['turnoverValue'] / index_data[
                'turnoverVol']

        index_data = index_data.sort_values(
            by=['trade_date', 'indexCode'], ascending=True).rename(
                columns={
                    'indexCode': 'code',
                    'preCloseIndex': 'pre_close',
                    'openIndex': 'open',
                    'highestIndex': 'high',
                    'lowestIndex': 'low',
                    'closeIndex': 'close',
                    'turnoverVol': 'volume',
                    'turnoverValue': 'value',
                    'vwap': 'vwap',
                    'chgPct': 'p_change'
                })

        index_data = index_data.sort_values(by=['trade_date', 'code'],
                                            ascending=True)

        index_data = self.transform(market_data=index_data)
        return market_data, index_data

    def run(self, codes, benchmark, begin_date, end_date, columns, n_fold):
        market_data, index_data = self.fetch_data(codes=codes,
                                                  benchmark=benchmark,
                                                  begin_date=begin_date,
                                                  end_date=end_date,
                                                  columns=columns)
        benchmark_kl_pd = self.transform_benchmark(index_data=index_data,
                                                   n_fold=n_fold)
        pick_kl_pd_dict = self.transform_code(market_data=market_data,
                                              benchmark_kl_pd=benchmark_kl_pd)
        pick_kl_pd_dict['benchmark'] = benchmark_kl_pd
        return pick_kl_pd_dict