# -*- encoding:utf-8 -*-
import six
import pandas as pd
from jdw import DBAPI
from jdw.kdutils.singleton import Singleton
from jdw.mfc.lombard.indicator.symbol_pd import _benchmark
from jdw.mfc.lombard.base import Base


@six.add_metaclass(Singleton)
class Stock(Base):

    def __init__(self, market_trade_year=252):
        super(Stock, self).__init__(market_trade_year=market_trade_year)

    def transform_code(self, market_data, benchmark_kl_pd):
        pick_kl_pd_dict = {}
        choice_symbols = [code for code in market_data.code.unique().tolist()]
        for code in choice_symbols:
            kl_pd = market_data.set_index(
                'code').loc[code].reset_index().set_index('trade_date')
            kl_pd.index = pd.to_datetime(kl_pd.index)
            if benchmark_kl_pd is not None:
                kl_pd = _benchmark(kl_pd, benchmark_kl_pd)
            self.calc_atr(kl_pd)
            name = 'sh' + code if code[0] == '6' else 'sz' + code
            kl_pd.name = name
            kl_pd['key'] = list(range(0, len(kl_pd)))
            pick_kl_pd_dict[name] = kl_pd
        return pick_kl_pd_dict

    def fetch_data(self, codes, benchmark, begin_date, end_date, columns):
        market_data = DBAPI.MarketStockFactory(self._kd_engine).result(
            codes=codes,
            key='code',
            begin_date=begin_date,
            end_date=end_date,
            columns=columns)

        if 'turnoverValue' in market_data.columns and 'turnoverVol' in market_data.columns:
            market_data['vwap'] = market_data['turnoverValue'] / market_data[
                'turnoverVol']

        market_data = market_data.sort_values(
            by=['trade_date', 'code'], ascending=True).rename(
                columns={
                    'preClosePrice': 'pre_close',
                    'openPrice': 'open',
                    'highestPrice': 'high',
                    'lowestPrice': 'low',
                    'closePrice': 'close',
                    'settlePrice': 'settle',
                    'turnoverVol': 'volume',
                    'turnoverValue': 'value',
                    'vwap': 'vwap',
                    'chgPct': 'p_change'
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
