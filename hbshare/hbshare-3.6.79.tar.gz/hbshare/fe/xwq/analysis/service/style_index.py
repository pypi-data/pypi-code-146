# -*- coding: utf-8 -*-

from datetime import datetime
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df

def get_cx_index(type, style, start_date, end_date):
    # 日历数据
    calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df = get_date(start_date, end_date)
    # 个股市值数据
    stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/stock_market_value.hdf', key='table')
    # 个股行情数据
    stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/stock_daily_k.hdf', key='table')
    stock_daily_k = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
    stock_daily_k = stock_daily_k.replace(0.0, np.nan).fillna(method='ffill')
    stock_daily_ret = stock_daily_k.pct_change()
    stock_daily_ret = stock_daily_ret[(stock_daily_ret.index >= start_date) & (stock_daily_ret.index <= end_date)]
    stock_daily_ret = stock_daily_ret.unstack().reset_index()
    stock_daily_ret.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'RET']

    # 晨星股票风格
    stock_style = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/stock_style.hdf', key='table')
    stock_style = stock_style[stock_style['type'] == type]
    stock_style = stock_style[stock_style['category'] == style + '型']
    stock_style = stock_style[(stock_style['trade_date'] >= start_date) & (stock_style['trade_date'] <= end_date)]
    stock_style = stock_style.merge(calendar_trade_df.rename(columns={'CALENDAR_DATE': 'trade_date'}), on=['trade_date'], how='left')
    stock_style = stock_style.rename(columns={'ticker': 'TICKER_SYMBOL'}).merge(stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    total_mv = stock_style[['TRADE_DATE', 'MARKET_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
    stock_style = stock_style.merge(total_mv, on=['TRADE_DATE'], how='left')
    stock_style['WEIGHT'] = stock_style['MARKET_VALUE'] / stock_style['TOTAL_MARKET_VALUE']
    stock_style = stock_style.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='WEIGHT').sort_index().fillna(0.0)
    stock_style = trade_df[['TRADE_DATE']].set_index('TRADE_DATE').merge(stock_style, left_index=True, right_index=True, how='left')
    stock_style = stock_style.fillna(method='ffill')
    stock_style = stock_style.unstack().reset_index()
    stock_style.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'WEIGHT']
    stock_style = stock_style[stock_style['WEIGHT'] != 0.0]

    index = stock_style.merge(stock_daily_ret, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left')
    index['WEIGHT_RET'] = index['RET'] * index['WEIGHT']
    index = index[['TRADE_DATE', 'WEIGHT_RET']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'WEIGHT_RET': style})
    index[style].iloc[0] = 0.0
    index[style] = (index[style] + 1.0).cumprod()
    index = index.set_index('TRADE_DATE')
    return index

if __name__ == '__main__':
    start_date = '20151231'
    end_date = '20220721'
    type = 'main'
    style_list = ['大盘成长', '大盘价值', '中盘成长', '中盘价值', '小盘成长', '小盘价值']
    for style in style_list:
        print(style)
        # 巨潮指数数据
        jc_df = HBDB().read_index_daily_k_given_date_and_indexs(start_date, ['399372', '399373', '399374', '399375', '399376', '399377'])
        jc_df = jc_df.pivot(index='jyrq', columns='zqmc', values='spjg')
        jc_df = jc_df[[style]]
        jc_df = jc_df / jc_df.iloc[0]
        jc_df = jc_df.rename(columns={style: style + '_巨潮'})
        jc_df.index = map(lambda x: datetime.strptime(str(x), '%Y%m%d'), jc_df.index)
        # 晨星指数数据
        cx_df = get_cx_index(type, style, start_date, end_date)
        cx_df = cx_df.rename(columns={style: style + '_晨星'})
        cx_df.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), cx_df.index )

        plt.figure(figsize=(6, 6))
        plt.plot(jc_df.index, jc_df[style + '_巨潮'].values, label=style + '_巨潮', color='#F04950')
        plt.plot(cx_df.index, cx_df[style + '_晨星'].values, label=style + '_晨星', color='#6268A2')
        plt.legend(loc=2)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/{0}_{1}.png'.format(style, start_date))

    # # 巨潮相关
    # jc_daily_k = HBDB().read_index_daily_k_given_date_and_indexs('20220630', ['399311'])
    # jc_daily_k = jc_daily_k[jc_daily_k['jyrq'] == 20220630]
    # jc_cons = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/jc_cons.hdf', key='table')
    # jc_cons = jc_cons[jc_cons['ENDDATE'] == '2022-06-30 00:00:00']
    # jc_cons = jc_cons[['SECUCODE']].rename(columns={'SECUCODE': 'TICKER_SYMBOL'})
    # stock_mv = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/stock_market_value.hdf', key='table')
    # stock_mv = stock_mv[stock_mv['TRADE_DATE'] == '20220630']
    # stock_mv = jc_cons.merge(stock_mv[['TICKER_SYMBOL', 'MARKET_VALUE']], on=['TICKER_SYMBOL'], how='left')
    # stock_mv = stock_mv.sort_values('MARKET_VALUE', ascending=False).reset_index().drop('index', axis=1)
    # stock_mv['SIZE'] = np.nan
    # stock_mv['SIZE'].iloc[:200] = '大盘'
    # stock_mv['SIZE'].iloc[200:500] = '中盘'
    # stock_mv['SIZE'].iloc[500:] = '小盘'
    # stock_turnover = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/A股成交额.xlsx')
    # stock_turnover['TICKER_SYMBOL'] = stock_turnover['TICKER_SYMBOL'].apply(lambda x: str(x).split('.')[0])
    # stock_mv = stock_mv.merge(stock_turnover, on=['TICKER_SYMBOL'], how='left')
    # stock_mv = stock_mv.dropna(subset=['TURNOVER_VALUE'])
    #
    # # 晨星相关
    # stock_mv = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/stock_market_value.hdf', key='table')
    # stock_mv = stock_mv[stock_mv['TRADE_DATE'] == '20220630']
    # stock_mv_total = stock_mv['MARKET_VALUE'].sum()
    # stock_mv_70 = stock_mv_total * 0.7
    # stock_mv_90 = stock_mv_total * 0.9
    # stock_mv = stock_mv.sort_values('MARKET_VALUE', ascending=False)
    # stock_mv['ACCUM_MARKET_VALUE'] = stock_mv['MARKET_VALUE'].cumsum()
    # stock_mv['SIZE'] = stock_mv['ACCUM_MARKET_VALUE'].apply(lambda x: '大盘' if x <= stock_mv_70 else '中盘' if x > stock_mv_70 and x <= stock_mv_90 else '小盘')
    # stock_turnover = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/style_index/A股成交额.xlsx')
    # stock_turnover['TICKER_SYMBOL'] = stock_turnover['TICKER_SYMBOL'].apply(lambda x: str(x).split('.')[0])
    # stock_mv = stock_mv.merge(stock_turnover, on=['TICKER_SYMBOL'], how='left')
    # stock_mv = stock_mv.dropna(subset=['TURNOVER_VALUE'])