"""
大小盘流动性
"""
import pandas as pd
from datetime import datetime
import hbshare as hbs
from hbshare.fe.common.util.data_loader import get_trading_day_list
from WindPy import w

w.start()


class StockLiquidity:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        # 指数
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        sql_script = "SELECT JYRQ as TRADEDATE, ZQDM, SPJG as TCLOSE from funddb.ZSJY WHERE " \
                     "ZQDM in ('000300', '000852', '399303') " \
                     "and JYRQ >= {} and JYRQ <= {}".format(self.start_date, self.end_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=10000)['data'])
        index_data = pd.pivot_table(
            data, index='TRADEDATE', columns='ZQDM', values='TCLOSE').reindex(week_list).dropna().sort_index()
        # DR007
        res = w.wsd("DR007.IB", "close", self.start_date, self.end_date, "")
        data = pd.DataFrame(res.Data[0], index=res.Times, columns=res.Codes)
        data.index.name = 'trade_date'
        data.reset_index(inplace=True)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        data['DR007-MA20'] = data['DR007.IB'].rolling(20).mean()
        rates = data.set_index('trade_date').reindex(week_list)
        # 10年期国债收益率
        res = w.edb('M1001654', self.start_date, self.end_date)
        data = pd.DataFrame(res.Data[0], index=res.Times, columns=res.Codes)
        data.index.name = 'trade_date'
        data.reset_index(inplace=True)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        data.rename(columns={"M1001654": "ytm_10y"}, inplace=True)
        ytm_data = data.set_index('trade_date').reindex(week_list)
        # 信用利差
        res = w.edb('M1016547,M1016548', self.start_date, self.end_date)
        data = pd.DataFrame(res.Data, index=res.Codes, columns=res.Times).T
        data.index.name = 'trade_date'
        data.reset_index(inplace=True)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        data.rename(columns={"M1016547": "credit_spread_AA+", "M1016548": "credit_spread_AA"}, inplace=True)
        spread = data.set_index('trade_date').reindex(week_list)

        df = index_data.merge(
            rates, left_index=True, right_index=True).merge(
            ytm_data, left_index=True, right_index=True).merge(spread, left_index=True, right_index=True)

        df.rename(columns={"000300": "沪深300", "000852": "中证1000", "399303": "国证2000"}, inplace=True)
        df['中证1000/沪深300'] = df['中证1000'] / df['沪深300']
        df['国证2000/沪深300'] = df['国证2000'] / df['沪深300']

        self.data = df


if __name__ == '__main__':
    StockLiquidity('20141120', '20221118')