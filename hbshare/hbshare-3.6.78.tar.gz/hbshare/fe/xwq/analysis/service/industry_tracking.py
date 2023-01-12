# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd


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

def get_stock_industry():
    # stock_industry = HBDB().read_stock_industry()
    # stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna('20990101')
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].str.len() == 6]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    return stock_industry

def get_industry_info():
    industry_info = HBDB().read_industry_info()
    industry_info = industry_info.rename(columns={'flmc': 'INDUSTRY_NAME', 'zsdm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    industry_info = industry_info.dropna(subset=['BEGIN_DATE'])
    industry_info['END_DATE'] = industry_info['END_DATE'].replace('', np.nan).fillna('20990101')
    industry_info['BEGIN_DATE'] = industry_info['BEGIN_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
    industry_info['END_DATE'] = industry_info['END_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
    industry_info['BEGIN_DATE'] = industry_info['BEGIN_DATE'].astype(int).astype(str)
    industry_info['END_DATE'] = industry_info['END_DATE'].astype(int).astype(str)
    industry_info['INDUSTRY_VERSION'] = industry_info['INDUSTRY_VERSION'].astype(int)
    industry_info['INDUSTRY_TYPE'] = industry_info['INDUSTRY_TYPE'].astype(int)
    industry_info['IS_NEW'] = industry_info['IS_NEW'].astype(int)
    industry_info = industry_info[industry_info['INDUSTRY_VERSION'] == 3]
    return industry_info

def get_stock_info():
    stock_info = HBDB().read_stock_info()
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqjc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].dropna()
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info['SAMPLE_DATE'] = stock_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(365)).strftime('%Y%m%d'))
    return stock_info

class IndustryHead:
    def __init__(self, date, start_date, end_date, sw_type, head):
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.sw_type = sw_type
        self.head = head
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        stock_market_value = HBDB().read_stock_market_value_given_date(self.date)
        star_stock_market_value = HBDB().read_star_stock_market_value_given_date(self.date)
        self. stock_market_value = pd.concat([stock_market_value, star_stock_market_value])

        stock_finance_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/stock_finance.hdf'
        # if os.path.isfile(stock_finance_path):
        #     existed_stock_finance = pd.read_hdf(stock_finance_path, key='table')
        #     max_date = max(existed_stock_finance['END_DATE'])
        #     start_date = max(str(max_date), '20150101')
        # else:
        #     existed_stock_finance = pd.DataFrame()
        #     start_date = '20150101'
        # report_df = self.report_df[(self.report_df['REPORT_DATE'] > start_date) & (self.report_df['REPORT_DATE'] < datetime.today().strftime('%Y%m%d'))]
        # stock_finance_list = []
        # for date in report_df['REPORT_DATE'].unique().tolist():
        #     stock_finance_date = HBDB().read_stock_finance_given_date(date)
        #     stock_finance_date = stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
        #     star_stock_finance_date = HBDB().read_star_stock_finance_given_date(date)
        #     star_stock_finance_date = star_stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(star_stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
        #     stock_finance_date = pd.concat([stock_finance_date, star_stock_finance_date])
        #     stock_finance_list.append(stock_finance_date)
        #     print(date)
        # self.stock_finance = pd.concat([existed_stock_finance] + stock_finance_list, ignore_index=True)
        # self.stock_finance = self.stock_finance.sort_values(['END_DATE', 'TICKER_SYMBOL', 'PUBLISH_DATE'])
        # self.stock_finance = self.stock_finance.reset_index().drop('index', axis=1)
        # self.stock_finance.to_hdf(stock_finance_path, key='table', mode='w')
        self.stock_finance = pd.read_hdf(stock_finance_path, key='table')

        stock_consensus_list = []
        for type in ['FY0', 'FY1', 'FY2', 'FY3', 'YOY']:
            stock_consensus_type = HBDB().read_consensus_given_date(self.date, type)
            stock_consensus_list.append(stock_consensus_type)
        self.stock_consensus = pd.concat(stock_consensus_list)
        self.stock_consensus['TICKER_SYMBOL'] = self.stock_consensus['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])

    def industry_head_stocks(self):
        stock_market_value = self.stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_market_value = stock_market_value.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE'])
        industry_head_stocks = stock_market_value.sort_values(['INDUSTRY_NAME', 'MARKET_VALUE'], ascending=[True, False]).groupby(['INDUSTRY_NAME']).head(self.head)
        industry_head_stocks = industry_head_stocks[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']]
        industry_head_stocks = industry_head_stocks.sort_values(['INDUSTRY_NAME', 'MARKET_VALUE'], ascending=[True, False])
        industry_head_stocks['MARKET_VALUE'] = industry_head_stocks['MARKET_VALUE'].apply(lambda x: round(x / 10000000000.0, 2))
        return industry_head_stocks

    def get_all(self):
        industry_head_stocks = self.industry_head_stocks()
        stock_consensus = self.stock_consensus[self.stock_consensus['TICKER_SYMBOL'].isin(industry_head_stocks['TICKER_SYMBOL'].unique().tolist())]
        est_net_profit = stock_consensus[stock_consensus['ROLLING_TYPE'] != 'YOY']
        est_net_profit['EST_NET_PROFIT'] = est_net_profit['EST_NET_PROFIT'].apply(lambda x: '{0}'.format(round(x / 10000000000.0, 2)))
        est_net_profit = est_net_profit.pivot(index='TICKER_SYMBOL', columns='ROLLING_TYPE', values='EST_NET_PROFIT').reset_index()
        industry_head_stocks = industry_head_stocks.merge(est_net_profit, on=['TICKER_SYMBOL'], how='left')
        stock_finance = self.stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance[stock_finance['TICKER_SYMBOL'].isin(industry_head_stocks['TICKER_SYMBOL'].unique().tolist())]
        stock_finance = stock_finance[stock_finance['END_DATE'].str.slice(4, 8) == '1231']
        stock_finance['YEAR'] = stock_finance['END_DATE'].apply(lambda x: x[:4])
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'YEAR'], ascending=[True, True]).groupby(['TICKER_SYMBOL']).tail(2)
        stock_finance['ROE_TTM'] = stock_finance['ROE_TTM'].apply(lambda x: '{0}%'.format(round(x, 2)))
        stock_finance['GROSS_INCOME_RATIO_TTM'] = stock_finance['GROSS_INCOME_RATIO_TTM'].apply(lambda x: '{0}%'.format(round(x, 2)))
        stock_finance['NET_PROFIT_RATIO_TTM'] = stock_finance['NET_PROFIT_RATIO_TTM'].apply(lambda x: '{0}%'.format(round(x, 2)))
        roe = stock_finance.pivot(index='TICKER_SYMBOL', columns='YEAR', values='ROE_TTM').reset_index()
        gir = stock_finance.pivot(index='TICKER_SYMBOL', columns='YEAR', values='GROSS_INCOME_RATIO_TTM').reset_index()
        npr = stock_finance.pivot(index='TICKER_SYMBOL', columns='YEAR', values='NET_PROFIT_RATIO_TTM').reset_index()
        roe.columns = ['TICKER_SYMBOL'] + ['ROE_' + str(col) for col in list(roe.columns)[1:] if col != 'TICKER_SYMBOL']
        gir.columns = ['TICKER_SYMBOL'] + ['毛利率_' + str(col) for col in list(gir.columns)[1:] if col != 'TICKER_SYMBOL']
        npr.columns = ['TICKER_SYMBOL'] + ['净利率_' + str(col) for col in list(npr.columns)[1:] if col != 'TICKER_SYMBOL']
        industry_head_stocks = industry_head_stocks.merge(roe, on=['TICKER_SYMBOL'], how='left').merge(gir, on=['TICKER_SYMBOL'], how='left').merge(npr, on=['TICKER_SYMBOL'], how='left')
        return industry_head_stocks

if __name__ == '__main__':
    date = '20220715'  # 每周最后一个交易日
    start_date = (datetime.strptime(date, '%Y%m%d') - timedelta(730)).strftime('%Y%m%d')
    end_date = date
    sw_type = 1  # 申万行业层级
    head = 5  # 龙头个股数量
    IndustryHead(date, start_date, end_date, sw_type, head).get_all()