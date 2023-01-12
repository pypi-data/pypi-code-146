"""
小市值组合模块
"""
import os
import pandas as pd
import hbshare as hbs
import numpy as np
import datetime
from hbshare.fe.common.util.data_loader import get_trading_day_list

path = r'D:\kevin\risk_model_jy\RiskModel\data'


class Portfolio:
    def __init__(self, trade_date, window=60):
        self.trade_date = trade_date
        self.window = window

    def run(self):
        # universe
        univ = pd.read_csv(os.path.join(path, r'common_data/univ/zzqz/{0}.csv'.format(self.trade_date)),
                           index_col=0)
        univ['ticker'] = univ.index
        univ['ticker'] = univ['ticker'].apply(lambda x: str(x).zfill(6))
        universe = univ['ticker'].tolist()
        # 市净率 & 股息率
        sql_script = "SELECT a.SecuCode, b.TradingDay, b.PB, b.DividendRatio FROM hsjy_gg.LC_DIndicesForValuation b " \
                     "join hsjy_gg.SecuMain a on a.InnerCode = b.InnerCode where a.SecuMarket in (83, 90) and " \
                     "a.SecuCategory = 1 and to_char(b.TradingDay,'yyyymmdd') = '{}'".format(self.trade_date)
        fin_data_main = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])

        sql_script = "SELECT a.SecuCode, b.TradingDay, b.PB, b.DividendRatioTTM FROM hsjy_gg.LC_STIBDIndiForValue b " \
                     "join hsjy_gg.SecuMain a on a.InnerCode = b.InnerCode where a.SecuMarket in (83, 90) and " \
                     "a.SecuCategory = 1 and to_char(b.TradingDay,'yyyymmdd') = '{}'".format(self.trade_date)
        fin_data_stib = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])

        fin_data_stib.rename(columns={"DIVIDENDRATIOTTM": "DIVIDENDRATIO"}, inplace=True)
        fin_data = pd.concat([fin_data_main, fin_data_stib])
        fin_data.rename(columns={"SECUCODE": "ticker", "PB": "pb",
                                 "DIVIDENDRATIO": "dividend", "TRADINGDAY": "trade_date"}, inplace=True)
        fin_data = fin_data.set_index('ticker')[['pb', 'dividend']]
        # 市值
        date_market_value = pd.read_json(os.path.join(path, r'common_data/market_value/%s.json' % self.trade_date),
                                         dtype={'ticker': np.str})
        # 波动率
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=200)).strftime('%Y%m%d')
        trading_day_list = get_trading_day_list(pre_date, self.trade_date)
        pre_date = trading_day_list[-self.window:][0]
        listdir = os.listdir(os.path.join(path, r'common_data/chg_pct'))
        listdir = [x for x in listdir if pre_date <= x.split('.')[0] <= self.trade_date]
        chg_pct = []
        for filename in listdir:
            date_chg_pct = pd.read_csv(os.path.join(path, r'common_data/chg_pct/{}'.format(filename)),
                                       dtype={'ticker': str, "tradeDate": str})
            chg_pct.append(date_chg_pct)
        chg_pct = pd.concat(chg_pct, axis=0)
        chg_pct.rename(columns={'dailyReturnReinv': 'chg_pct', 'tradeDate': 'trade_date'}, inplace=True)

        chg_pct.loc[chg_pct['chg_pct'] < -0.2, 'chg_pct'] = -0.2
        chg_pct.loc[chg_pct['chg_pct'] > 0.2, 'chg_pct'] = 0.2

        stock_return = pd.pivot_table(chg_pct, index='trade_date', columns='ticker', values='chg_pct').sort_index()
        count_df = stock_return.isnull().sum()
        included_list = count_df[count_df <= 20].index.tolist()
        stock_return = stock_return[included_list]
        stock_vol = stock_return.std().to_frame('vol')
        # 申万一级行业
        data = pd.read_json(os.path.join(path, r'common_data/sw_new.json'), dtype={'ticker': str})
        data['outDate'] = data['outDate'].fillna(20991231)
        data['intoDate'] = data['intoDate'].map(int).map(str)
        data['outDate'] = data['outDate'].map(int).map(str)
        industry = data[(data['intoDate'] <= self.trade_date) & (data['outDate'] >= self.trade_date)].drop_duplicates(
            subset='ticker')

        summary_df = fin_data[['pb', 'dividend']].merge(
            date_market_value.set_index('ticker')[['marketValue']], left_index=True, right_index=True).merge(
            stock_vol, left_index=True, right_index=True).merge(
            industry.set_index('ticker')[['industryName1']], left_index=True, right_index=True).reindex(
            universe).reset_index()

        "======================================================筛选====================================================="
        pb_quantile = summary_df.groupby(
            'industryName1').apply(lambda x: x['pb'].quantile(0.3)).to_frame('pb_quantile').reset_index()
        summary_df = summary_df.merge(pb_quantile, on='industryName1')

        # include_1 = summary_df[summary_df['pb'] <= summary_df['pb_quantile']]['ticker'].tolist()
        # include_2 = summary_df[~summary_df['dividend'].isnull()]['ticker'].tolist()
        # include_3 = summary_df[summary_df['vol'] <= summary_df['vol'].quantile(0.5)]['ticker'].tolist()
        # include_4 = summary_df[summary_df['marketValue'] <= summary_df['marketValue'].quantile(0.5)]['ticker'].tolist()

        selected_df = summary_df[summary_df['pb'] <= summary_df['pb_quantile']]
        selected_df = selected_df.dropna(subset=['dividend'])
        selected_df = selected_df[selected_df['vol'] <= selected_df['vol'].quantile(0.5)]
        selected_df = selected_df[selected_df['marketValue'] <= selected_df['marketValue'].quantile(0.3)]

        for col in ['pb', 'dividend', 'marketValue', 'vol']:
            selected_df[col] = (selected_df[col] - selected_df[col].mean()) / selected_df[col].std()

        selected_df['dividend'] = -1 * selected_df['dividend']

        selected_df['score'] = selected_df[['pb', 'dividend', 'marketValue', 'vol']].mean(axis=1)

        selected_df.sort_values(by='score', inplace=True)

        return selected_df


if __name__ == '__main__':
    Portfolio('20220826').run()