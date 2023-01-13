# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sqlalchemy import create_engine
import os
import numpy as np
import pandas as pd

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format( 'admin', 'mysql', '192.168.223.152', '3306', 'fe_temp_data'))


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

def get_industry_symbol():
    industry_symbol = HBDB().read_industry_symbol()
    industry_symbol = industry_symbol.rename(columns={'hyhfbz': 'INDUSTRY_VERSION', 'fldm': 'INDUSTRY_ID', 'flmc': 'INDUSTRY_NAME', 'zsdm': 'INDEX_SYMBOL', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    industry_symbol = industry_symbol.dropna(subset=['BEGIN_DATE'])
    industry_symbol['END_DATE'] = industry_symbol['END_DATE'].replace('', np.nan).fillna('20990101')
    industry_symbol['BEGIN_DATE'] = industry_symbol['BEGIN_DATE'].astype(int).astype(str)
    industry_symbol['END_DATE'] = industry_symbol['END_DATE'].astype(int).astype(str)
    industry_symbol['INDUSTRY_VERSION'] = industry_symbol['INDUSTRY_VERSION'].astype(int)
    industry_symbol['INDUSTRY_TYPE'] = industry_symbol['INDUSTRY_TYPE'].astype(int)
    industry_symbol['IS_NEW'] = industry_symbol['IS_NEW'].astype(int)
    industry_symbol = industry_symbol[industry_symbol['INDUSTRY_VERSION'] == 3]
    return industry_symbol

def get_stock_industry():
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('{0}stock_industry.hdf'.format(data_path), key='table', mode='w')
    stock_industry = pd.read_hdf('{0}stock_industry.hdf'.format(data_path), key='table')
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

def get_stock_info(days=365):
    stock_info = HBDB().read_stock_info()
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqjc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].dropna()
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info['SAMPLE_DATE'] = stock_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(days)).strftime('%Y%m%d'))
    return stock_info

def filter_extreme_mad(ser, n=3):
    median = ser.quantile(0.5)
    new_median = ((ser - median).abs()).quantile(0.5)
    max_range = median + n * new_median
    min_range = median - n * new_median
    ser = np.clip(ser, min_range, max_range)
    return ser


class Timing:
    def __init__(self, start_date, end_date, data_path, sw_type=1):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.end_date_hyphen = datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.data_path = data_path
        self.sw_type = sw_type
        self.load()

    def load(self):
        # 日历
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date('19000101', self.end_date)

        # 个股相关
        self.stock_info = get_stock_info(180)

        # 行业相关
        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        self.industry_list = self.industry_info['INDUSTRY_ID'].unique().tolist()
        self.industry_symbol = get_industry_symbol()
        self.industry_symbol = self.industry_symbol[self.industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_symbol = self.industry_symbol[self.industry_symbol['IS_NEW'] == 1]
        self.industry_symbol = self.industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.drop('INDUSTRY_NAME', axis=1).merge(self.industry_symbol, on=['INDUSTRY_ID'], how='left')
        self.stock_industry = self.stock_industry.drop('INDUSTRY_ID', axis=1).merge(self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID']], on=['INDUSTRY_NAME'], how='left')
        self.stock_industry = self.stock_industry[['INDUSTRY_ID', 'INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        # 股票收盘价、涨跌幅、成交金额、换手率、流通市值、总市值
        stock_daily_k_path = '{0}stock_daily_k.hdf'.format(self.data_path)
        if os.path.isfile(stock_daily_k_path):
            existed_stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
            max_date = max(existed_stock_daily_k['TDATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_stock_daily_k = pd.DataFrame()
            start_date = '20071231'
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_daily_k_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_daily_k_date = HBDB().read_stock_daily_k_ch(int(date))
            stock_daily_k_list.append(stock_daily_k_date)
            print(date)
        self.stock_daily_k = pd.concat([existed_stock_daily_k] + stock_daily_k_list, ignore_index=True)
        self.stock_daily_k.to_hdf(stock_daily_k_path, key='table', mode='w')
        self.stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
        self.stock_daily_k = self.stock_daily_k.rename(columns={'TDATE': 'TRADE_DATE', 'SYMBOL': 'TICKER_SYMBOL', 'SNAME': 'SEC_SHORT_NAME', 'TCLOSE': 'CLOSE_PRICE', 'PCHG': 'PCT_CHANGE', 'VATURNOVER': 'TURNOVER_VALUE', 'TURNOVER': 'TURNOVER_RATE', 'MCAP': 'NEG_MARKET_VALUE', 'TCAP': 'MARKET_VALUE'})
        self.stock_daily_k['TRADE_DATE'] = self.stock_daily_k['TRADE_DATE'].astype(str)
        self.stock_daily_k = self.stock_daily_k.loc[self.stock_daily_k['TICKER_SYMBOL'].str.len() == 6]
        self.stock_daily_k = self.stock_daily_k.loc[self.stock_daily_k['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_daily_k = self.stock_daily_k.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_daily_k = self.stock_daily_k.reset_index().drop('index', axis=1)
        self.stock_daily_k = self.stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE', 'PCT_CHANGE', 'TURNOVER_VALUE', 'TURNOVER_RATE', 'NEG_MARKET_VALUE', 'MARKET_VALUE']]

        # 指数收盘点位、涨跌幅、成交金额
        index_daily_k_path = '{0}index_daily_k.hdf'.format(self.data_path)
        if os.path.isfile(index_daily_k_path):
            existed_index_daily_k = pd.read_hdf(index_daily_k_path, key='table')
            max_date = max(existed_index_daily_k['TDATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_index_daily_k = pd.DataFrame()
            start_date = '20071231'
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        index_daily_k_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            index_daily_k_date = HBDB().read_index_daily_k_ch(int(date))
            index_daily_k_list.append(index_daily_k_date)
            print(date)
        self.index_daily_k = pd.concat([existed_index_daily_k] + index_daily_k_list, ignore_index=True)
        self.index_daily_k.to_hdf(index_daily_k_path, key='table', mode='w')
        self.index_daily_k = pd.read_hdf(index_daily_k_path, key='table')
        self.index_daily_k = self.index_daily_k.rename(columns={'TDATE': 'TRADE_DATE', 'SYMBOL': 'INDEX_SYMBOL', 'SNAME': 'INDEX_NAME', 'TCLOSE': 'CLOSE_INDEX', 'PCHG': 'PCT_CHANGE', 'VATURNOVER': 'TURNOVER_VALUE'})
        self.index_daily_k['TRADE_DATE'] = self.index_daily_k['TRADE_DATE'].astype(str)
        self.index_daily_k = self.index_daily_k.sort_values(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_daily_k = self.index_daily_k.reset_index().drop('index', axis=1)
        self.index_daily_k = self.index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'INDEX_NAME', 'CLOSE_INDEX', 'PCT_CHANGE', 'TURNOVER_VALUE']]

        # 北上资金
        hk_cash_path = '{0}hk_cash.hdf'.format(self.data_path)
        if os.path.isfile(hk_cash_path):
            existed_hk_cash = pd.read_hdf(hk_cash_path, key='table')
            max_date = max(existed_hk_cash['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_hk_cash = pd.DataFrame()
            start_date = '20071231'
        if start_date < self.end_date:
            start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            sh_cash_update = w.wset("shhktransactionstatistics", "startdate={0};enddate={1};cycle=day;currency=hkd;field=date,sh_net_purchases".format(start_date_hyphen, self.end_date_hyphen), usedf=True)[1].reset_index()
            sh_cash_update = sh_cash_update.drop('index', axis=1)
            sh_cash_update.columns = ['TRADE_DATE', 'SH_NET_PURCHASE']
            sz_cash_update = w.wset("szhktransactionstatistics", "startdate={0};enddate={1};cycle=day;currency=hkd;field=date,sz_net_purchases".format(start_date_hyphen, self.end_date_hyphen), usedf=True)[1].reset_index()
            sz_cash_update = sz_cash_update.drop('index', axis=1)
            sz_cash_update.columns = ['TRADE_DATE', 'SZ_NET_PURCHASE']
            hk_cash_update = sh_cash_update.merge(sz_cash_update, on=['TRADE_DATE'], how='left')
            hk_cash_update['HK_NET_PURCHASE'] = hk_cash_update['SH_NET_PURCHASE'].fillna(0.0) + hk_cash_update['SZ_NET_PURCHASE'].fillna(0.0)
            hk_cash_update['TRADE_DATE'] = hk_cash_update['TRADE_DATE'].apply(lambda x: str(x.date()).replace('-', ''))
            self.hk_cash = pd.concat([existed_hk_cash, hk_cash_update], ignore_index=True)
            self.hk_cash = self.hk_cash.drop_duplicates()
            self.hk_cash.to_hdf(hk_cash_path, key='table', mode='w')
        self.hk_cash = pd.read_hdf(hk_cash_path, key='table')
        self.hk_cash['TRADE_DATE'] = self.hk_cash['TRADE_DATE'].astype(str)
        self.hk_cash = self.hk_cash.sort_values('TRADE_DATE')

        # 融资融券余额
        margin_balance_path = '{0}margin_balance.hdf'.format(self.data_path)
        if os.path.isfile(margin_balance_path):
            existed_margin_balance = pd.read_hdf(margin_balance_path, key='table')
            max_date = max(existed_margin_balance['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_margin_balance = pd.DataFrame()
            start_date = '20071231'
        if start_date < self.end_date:
            start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            margin_balance_update = w.edb("M0075992", start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
            margin_balance_update.columns = ['TRADE_DATE', 'MARGIN_BALANCE']
            margin_balance_update['TRADE_DATE'] = margin_balance_update['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
            self.margin_balance = pd.concat([existed_margin_balance, margin_balance_update], ignore_index=True)
            self.margin_balance = self.margin_balance.drop_duplicates()
            self.margin_balance.to_hdf(margin_balance_path, key='table', mode='w')
        self.margin_balance = pd.read_hdf(margin_balance_path, key='table')
        self.margin_balance['TRADE_DATE'] = self.margin_balance['TRADE_DATE'].astype(str)
        self.margin_balance = self.margin_balance.sort_values('TRADE_DATE')

        # 市场估值、财务数据
        market_valuation_finance_path = '{0}market_valuation_finance.hdf'.format(self.data_path)
        if os.path.isfile(market_valuation_finance_path):
            existed_market_valuation_finance = pd.read_hdf(market_valuation_finance_path, key='table')
            max_date = max(existed_market_valuation_finance['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_market_valuation_finance = pd.DataFrame()
            start_date = '20071231'
        if start_date < self.end_date:
            start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            market_valuation_finance_update_list = []
            for index in ['000300.SH', '000905.SH', '000852.SH', '000985.CSI']:
                market_valuation_finance_update = w.wsd(index, "pe_ttm,val_dividendyield2_issuer,yoynetprofit", start_date_hyphen, self.end_date_hyphen, "Days=Alldays", usedf=True)[1].reset_index()
                market_valuation_finance_update.columns = ['TRADE_DATE', 'PE_TTM', 'DIVIDEND_YIELD', 'NET_PROFIT_YOY']
                market_valuation_finance_update['TRADE_DATE'] = market_valuation_finance_update['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
                market_valuation_finance_update['INDEX_SYMBOL'] = index
                market_valuation_finance_update_list.append(market_valuation_finance_update)
            market_valuation_finance_update = pd.concat(market_valuation_finance_update_list)
            self.market_valuation_finance = pd.concat([existed_market_valuation_finance, market_valuation_finance_update], ignore_index=True)
            self.market_valuation_finance = self.market_valuation_finance.drop_duplicates()
            self.market_valuation_finance.to_hdf(market_valuation_finance_path, key='table', mode='w')
        self.market_valuation_finance = pd.read_hdf(market_valuation_finance_path, key='table')
        self.market_valuation_finance['TRADE_DATE'] = self.market_valuation_finance['TRADE_DATE'].astype(str)

        # 十年期国债收益率
        bond_yield_10y_path = '{0}bond_yield_10y.hdf'.format(self.data_path)
        if os.path.isfile(bond_yield_10y_path):
            existed_bond_yield_10y = pd.read_hdf(bond_yield_10y_path, key='table')
            max_date = max(existed_bond_yield_10y['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_bond_yield_10y = pd.DataFrame()
            start_date = '20071231'
        if start_date < self.end_date:
            start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            bond_yield_10y_update = w.edb("M0325687", start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
            bond_yield_10y_update.columns = ['TRADE_DATE', 'BOND_YIELD_10Y']
            bond_yield_10y_update['TRADE_DATE'] = bond_yield_10y_update['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
            self.bond_yield_10y = pd.concat([existed_bond_yield_10y, bond_yield_10y_update], ignore_index=True)
            self.bond_yield_10y = self.bond_yield_10y.drop_duplicates()
            self.bond_yield_10y.to_hdf(bond_yield_10y_path, key='table', mode='w')
        self.bond_yield_10y = pd.read_hdf(bond_yield_10y_path, key='table')
        self.bond_yield_10y['TRADE_DATE'] = self.bond_yield_10y['TRADE_DATE'].astype(str)

        # 股票财务数据
        stock_finance_path = '{0}stock_finance.hdf'.format(self.data_path)
        if os.path.isfile(stock_finance_path):
            existed_stock_finance = pd.read_hdf(stock_finance_path, key='table')
            max_date = max(existed_stock_finance['END_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_stock_finance = pd.DataFrame()
            start_date = '20071231'
        report_df = self.report_df[(self.report_df['REPORT_DATE'] > start_date) & (self.report_df['REPORT_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_finance_list = []
        for date in report_df['REPORT_DATE'].unique().tolist():
            stock_finance_date = HBDB().read_stock_finance_jy(date)
            stock_finance_date = stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'OPER_REVENUE_YOY', 'NET_PROFIT_YOY', 'ROE_TTM', 'EPS_TTM', 'NAPS', 'OCF_TTM', 'DIVIDEND_TTM']] if len(stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'OPER_REVENUE_YOY', 'NET_PROFIT_YOY', 'ROE_TTM', 'EPS_TTM', 'NAPS', 'OCF_TTM', 'DIVIDEND_TTM'])
            star_stock_finance_date = HBDB().read_star_stock_finance_jy(date)
            star_stock_finance_date = star_stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'OPER_REVENUE_YOY', 'NET_PROFIT_YOY', 'ROE_TTM', 'EPS_TTM', 'NAPS', 'OCF_TTM', 'DIVIDEND_TTM']] if len(star_stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'OPER_REVENUE_YOY', 'NET_PROFIT_YOY', 'ROE_TTM', 'EPS_TTM', 'NAPS', 'OCF_TTM', 'DIVIDEND_TTM'])
            stock_finance_date = pd.concat([stock_finance_date, star_stock_finance_date])
            stock_finance_list.append(stock_finance_date)
            print(date)
        self.stock_finance = pd.concat([existed_stock_finance] + stock_finance_list, ignore_index=True)
        self.stock_finance.to_hdf(stock_finance_path, key='table', mode='w')
        self.stock_finance = pd.read_hdf(stock_finance_path, key='table')
        self.stock_finance['END_DATE'] = self.stock_finance['END_DATE'].astype(str)
        self.stock_finance['PUBLISH_DATE'] = self.stock_finance['PUBLISH_DATE'].astype(str)
        self.stock_finance = self.stock_finance.loc[self.stock_finance['TICKER_SYMBOL'].str.len() == 6]
        self.stock_finance = self.stock_finance.loc[self.stock_finance['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]

        # 行业主力净流入金额
        industry_main_cash_path = '{0}industry_main_cash.hdf'.format(self.data_path)
        if os.path.isfile(industry_main_cash_path):
            existed_industry_main_cash = pd.read_hdf(industry_main_cash_path, key='table')
            max_date = max(existed_industry_main_cash['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_industry_main_cash = pd.DataFrame()
            start_date = '20071231'
        if start_date < self.end_date:
            start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            industry_main_cash_update_list = []
            for index in self.industry_list:
                industry_main_cash_update = w.wsd("{0}.SI".format(index), "mfd_inflow_m", start_date_hyphen, self.end_date_hyphen, "unit=1", usedf=True)[1].reset_index()
                industry_main_cash_update.columns = ['TRADE_DATE', 'INDUSTRY_MAIN_CASH']
                industry_main_cash_update['TRADE_DATE'] = industry_main_cash_update['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
                industry_main_cash_update['INDEX_SYMBOL'] = index
                industry_main_cash_update_list.append(industry_main_cash_update)
            industry_main_cash_update = pd.concat(industry_main_cash_update_list)
            self.industry_main_cash = pd.concat([existed_industry_main_cash, industry_main_cash_update], ignore_index=True)
            self.industry_main_cash = self.industry_main_cash.drop_duplicates()
            self.industry_main_cash.to_hdf(industry_main_cash_path, key='table', mode='w')
        self.industry_main_cash = pd.read_hdf(industry_main_cash_path, key='table')
        self.industry_main_cash['TRADE_DATE'] = self.industry_main_cash['TRADE_DATE'].astype(str)

        # 行业融资买入额占成交额
        industry_margin_proportion_path = '{0}industry_margin_proportion.hdf'.format(self.data_path)
        if os.path.isfile(industry_margin_proportion_path):
            existed_industry_margin_proportion = pd.read_hdf(industry_margin_proportion_path, key='table')
            max_date = max(existed_industry_margin_proportion['TRADE_DATE'])
            start_date = max(str(max_date), '20071231')
        else:
            existed_industry_margin_proportion = pd.DataFrame()
            start_date = '20071231'
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        industry_margin_proportion_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            date_hyphen = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
            industry_margin_proportion_date = w.wset("tradingstatisticsbyindustry","exchange=sws_2021;startdate={0};enddate={1};field=industryname,financingbuyamount".format(date_hyphen, date_hyphen), usedf=True)[1].reset_index()
            industry_margin_proportion_date = industry_margin_proportion_date.drop('index', axis=1)
            industry_margin_proportion_date.columns = ['INDUSTRY_NAME', 'MARGIN_PROPORTION']
            industry_margin_proportion_date['TRADE_DATE'] = date
            industry_margin_proportion_list.append(industry_margin_proportion_date)
            print(date)
        self.industry_margin_proportion = pd.concat([existed_industry_margin_proportion] + industry_margin_proportion_list, ignore_index=True)
        self.industry_margin_proportion = self.industry_margin_proportion.drop_duplicates()
        self.industry_margin_proportion.to_hdf(industry_margin_proportion_path, key='table', mode='w')
        self.industry_margin_proportion = pd.read_hdf(industry_margin_proportion_path, key='table')
        self.industry_margin_proportion['TRADE_DATE'] = self.industry_margin_proportion['TRADE_DATE'].astype(str)
        self.industry_margin_proportion['INDUSTRY_NAME'] = self.industry_margin_proportion['INDUSTRY_NAME'].apply(lambda x: x.split('SW')[1])
        self.industry_margin_proportion = self.industry_margin_proportion.merge(self.stock_industry[['INDUSTRY_NAME', 'INDUSTRY_ID']].drop_duplicates(), on=['INDUSTRY_NAME'], how='left')

        type = 'FY1'
        stock_consensus_path = '{0}stock_consensus_{1}.hdf'.format(self.data_path, type)
        if os.path.isfile(stock_consensus_path):
            existed_stock_consensus = pd.read_hdf(stock_consensus_path, key='table')
            max_date = max(existed_stock_consensus['EST_DT'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_consensus = pd.DataFrame()
            start_date = '20150101'
        calendar_df = self.calendar_df[(self.calendar_df['CALENDAR_DATE'] > start_date) & (self.calendar_df['CALENDAR_DATE'] <= self.end_date)]
        stock_consensus_list = []
        for date in calendar_df['CALENDAR_DATE'].unique().tolist():
            stock_consensus_date = HBDB().read_consensus_given_date(date, type)
            stock_consensus_list.append(stock_consensus_date)
            print(date)
        self.stock_consensus = pd.concat([existed_stock_consensus] + stock_consensus_list, ignore_index=True)
        self.stock_consensus = self.stock_consensus.sort_values(['EST_DT', 'TICKER_SYMBOL'])
        self.stock_consensus = self.stock_consensus.reset_index().drop('index', axis=1)
        self.stock_consensus.to_hdf(stock_consensus_path, key='table', mode='w')
        self.stock_consensus = pd.read_hdf(stock_consensus_path, key='table')
        self.stock_consensus['TICKER_SYMBOL'] = self.stock_consensus['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus = self.stock_consensus.loc[self.stock_consensus['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus = self.stock_consensus.loc[self.stock_consensus['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]

    def MarketTiming(self):
        ###########################################################################################################################
        # 市场拥挤度
        # 成交额
        n = 0
        stock_turnover = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_turnover = stock_turnover[['TRADE_DATE', 'TICKER_SYMBOL', 'TURNOVER_VALUE']]
        stock_turnover = stock_turnover[stock_turnover['TURNOVER_VALUE'] > 0.0]
        market_total_turnover = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index()

        # 成交额占比：沪深300、中证500、中证1000、中证全指成交额/市场成交额
        n = 0
        index_list = ['000300', '000905', '000852', '000985']
        stock_turnover = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_turnover = stock_turnover[['TRADE_DATE', 'TICKER_SYMBOL', 'TURNOVER_VALUE']]
        stock_turnover = stock_turnover[stock_turnover['TURNOVER_VALUE'] > 0.0]
        total_turnover = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'TURNOVER_VALUE': 'TOTAL_TURNOVER_VALUE'})
        market_turnover = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        market_turnover = market_turnover[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_VALUE']]
        market_turnover = market_turnover[market_turnover['TURNOVER_VALUE'] > 0.0]
        market_turnover = market_turnover[market_turnover['INDEX_SYMBOL'].isin(index_list)]
        market_turnover = market_turnover.merge(total_turnover, on=['TRADE_DATE'], how='left')
        market_turnover['TURNOVER_PROPORTION'] = market_turnover['TURNOVER_VALUE'] / market_turnover['TOTAL_TURNOVER_VALUE']
        market_turnover = market_turnover.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='TURNOVER_PROPORTION').sort_index().reset_index()
        market_turnover = market_turnover[['TRADE_DATE'] + index_list]
        market_turnover.columns = ['TRADE_DATE'] + ['TURNOVER_PROPORTION_' + col for col in list(market_turnover.columns)[1:]]
        market_turnover = market_turnover[(market_turnover['TRADE_DATE'] > self.start_date) & (market_turnover['TRADE_DATE'] <= self.end_date)]

        # 北向资金净流入
        n = 0
        hk_cash = self.hk_cash[(self.hk_cash['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.hk_cash['TRADE_DATE'] <= self.end_date)]
        market_hk_cash = hk_cash[['TRADE_DATE', 'SH_NET_PURCHASE', 'SZ_NET_PURCHASE', 'HK_NET_PURCHASE']]
        market_hk_cash = market_hk_cash[(market_hk_cash['TRADE_DATE'] > self.start_date) & (market_hk_cash['TRADE_DATE'] <= self.end_date)]

        # 融资融券余额
        n = 0
        margin_balance = self.margin_balance[(self.margin_balance['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.margin_balance['TRADE_DATE'] <= self.end_date)]
        market_margin_balance = margin_balance[['TRADE_DATE', 'MARGIN_BALANCE']]
        market_margin_balance = market_margin_balance[(market_margin_balance['TRADE_DATE'] > self.start_date) & (market_margin_balance['TRADE_DATE'] <= self.end_date)]

        # 创近一月/近六月新高个股数量及占比
        n1 = 20
        n2 = 120
        n = max(n1, n2)
        stock_daily_k = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_daily_k = stock_daily_k.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_daily_k = stock_daily_k[stock_daily_k['TRADE_DATE'] >= stock_daily_k['SAMPLE_DATE']]
        stock_daily_k = stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']]
        stock_daily_k_short = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        stock_daily_k_short = stock_daily_k_short.rolling(n1).max()
        stock_daily_k_short = stock_daily_k_short.unstack().reset_index()
        stock_daily_k_short.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE_SHORT']
        stock_new_high_short = stock_daily_k.merge(stock_daily_k_short, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        stock_new_high_short['NEW_HIGH_SHORT'] = (stock_new_high_short['CLOSE_PRICE'] >= stock_new_high_short['CLOSE_PRICE_SHORT']).astype(int)
        market_new_high_short_count = stock_new_high_short[['TRADE_DATE', 'NEW_HIGH_SHORT']].groupby('TRADE_DATE').count().reset_index().rename(columns={'NEW_HIGH_SHORT': 'COUNT'})
        market_new_high_short = stock_new_high_short[['TRADE_DATE', 'NEW_HIGH_SHORT']].groupby('TRADE_DATE').sum().reset_index()
        market_new_high_short = market_new_high_short.merge(market_new_high_short_count, on=['TRADE_DATE'], how='left')
        market_new_high_short['NEW_HIGH_RATIO_SHORT'] = market_new_high_short['NEW_HIGH_SHORT'] / market_new_high_short['COUNT']
        stock_daily_k_long = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        stock_daily_k_long = stock_daily_k_long.rolling(n2).max()
        stock_daily_k_long = stock_daily_k_long.unstack().reset_index()
        stock_daily_k_long.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE_LONG']
        stock_new_high_long = stock_daily_k.merge(stock_daily_k_long, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        stock_new_high_long['NEW_HIGH_LONG'] = (stock_new_high_long['CLOSE_PRICE'] >= stock_new_high_long['CLOSE_PRICE_LONG']).astype(int)
        market_new_high_long_count = stock_new_high_long[['TRADE_DATE', 'NEW_HIGH_LONG']].groupby('TRADE_DATE').count().reset_index().rename(columns={'NEW_HIGH_LONG': 'COUNT'})
        market_new_high_long = stock_new_high_long[['TRADE_DATE', 'NEW_HIGH_LONG']].groupby('TRADE_DATE').sum().reset_index()
        market_new_high_long = market_new_high_long.merge(market_new_high_long_count, on=['TRADE_DATE'], how='left')
        market_new_high_long['NEW_HIGH_RATIO_LONG'] = market_new_high_long['NEW_HIGH_LONG'] / market_new_high_long['COUNT']
        market_new_high = market_new_high_short[['TRADE_DATE', 'NEW_HIGH_SHORT', 'NEW_HIGH_RATIO_SHORT']].merge(market_new_high_long[['TRADE_DATE', 'NEW_HIGH_LONG', 'NEW_HIGH_RATIO_LONG']], on=['TRADE_DATE'], how='outer')
        market_new_high = market_new_high[(market_new_high['TRADE_DATE'] > self.start_date) & (market_new_high['TRADE_DATE'] <= self.end_date)]

        # 行业分歧度：100% - 过去10/60日申万二级行业收益率第一主成分解释比例
        n1 = 10
        n2 = 60
        n = max(n1, n2)
        industry_info = get_industry_info()
        industry_info = industry_info[industry_info['INDUSTRY_TYPE'] == 2]
        industry_info = industry_info[industry_info['IS_NEW'] == 1]
        industry_info = industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        industry_list = industry_info['INDUSTRY_ID'].unique().tolist()
        index_daily_ret = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        index_daily_ret = index_daily_ret[['TRADE_DATE', 'INDEX_SYMBOL', 'PCT_CHANGE']]
        index_daily_ret = index_daily_ret[index_daily_ret['INDEX_SYMBOL'].isin(industry_list)]
        index_daily_ret = index_daily_ret.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PCT_CHANGE').sort_index()
        model_short = PCA(n_components=1)
        model_long = PCA(n_components=1)
        market_industry_divergence = pd.DataFrame(index=list(index_daily_ret.iloc[n:].index), columns=['PCA_1ST_SHORT', 'PCA_1ST_LONG'])
        for date in list(index_daily_ret.iloc[n:].index):
            print(date)
            index_daily_ret_short = index_daily_ret[index_daily_ret.index <= date].iloc[-n1:]
            index_daily_ret_short = index_daily_ret_short.dropna(axis=1, how='all').fillna(0.0)
            index_daily_ret_short = (index_daily_ret_short - index_daily_ret_short.mean()) / index_daily_ret_short.std()
            try:
                model_short.fit(index_daily_ret_short.values)
                market_industry_divergence.loc[date, 'PCA_1ST_SHORT'] = 1.0 - model_short.explained_variance_ratio_[0]
            except:
                market_industry_divergence.loc[date, 'PCA_1ST_SHORT'] = np.nan
            index_daily_ret_long = index_daily_ret[index_daily_ret.index <= date].iloc[-n2:]
            index_daily_ret_long = index_daily_ret_long.dropna(axis=1, how='all').fillna(0.0)
            index_daily_ret_long = (index_daily_ret_long - index_daily_ret_long.mean()) / index_daily_ret_long.std()
            try:
                model_long.fit(index_daily_ret_long.values)
                market_industry_divergence.loc[date, 'PCA_1ST_LONG'] = 1.0 - model_long.explained_variance_ratio_[0]
            except:
                market_industry_divergence.loc[date, 'PCA_1ST_LONG'] = np.nan
        market_industry_divergence = market_industry_divergence.reset_index().rename(columns={'index': 'TRADE_DATE'})
        market_industry_divergence = market_industry_divergence[(market_industry_divergence['TRADE_DATE'] > self.start_date) & (market_industry_divergence['TRADE_DATE'] <= self.end_date)]

        # 偏股基金仓位（考虑公募、私募）：以申万一级行业指数日收益率作为自变量，基金的日频收益率作为因变量进行带约束的Lasso回归，高频估算基金仓位
        n1 = 30
        n2 = 12
        n = max(n1, n2)
        mutual_index = 'HM0037'
        private_index = 'HB1001'
        industry_info = get_industry_info()
        industry_info = industry_info[industry_info['INDUSTRY_TYPE'] == 1]
        industry_info = industry_info[industry_info['IS_NEW'] == 1]
        industry_info = industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        industry_list = industry_info['INDUSTRY_ID'].unique().tolist()
        index_daily_k = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 6)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        index_daily_k = index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        index_daily_k = index_daily_k[index_daily_k['INDEX_SYMBOL'].isin(industry_list)]
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        mutual_index_daily_k = HBDB().read_mutual_index_daily_k_given_indexs([mutual_index], (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d'), self.end_date)
        mutual_index_daily_k = mutual_index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        mutual_index_daily_k = mutual_index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        mutual_index_data = mutual_index_daily_k.merge(index_daily_k, left_index=True, right_index=True, how='left')
        mutual_index_data = mutual_index_data.pct_change().dropna()
        private_index_daily_k = HBDB().read_private_index_daily_k_given_indexs([private_index], (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 6)).strftime('%Y%m%d'), self.end_date)
        private_index_daily_k = private_index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        private_index_daily_k = private_index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        private_index_data = private_index_daily_k.merge(index_daily_k, left_index=True, right_index=True, how='left')
        private_index_data = private_index_data.pct_change().dropna()
        model_mutual = LassoCV()
        model_private = LassoCV()
        market_fund_position = pd.DataFrame(index=list(mutual_index_data.iloc[n:].index), columns=['POSITION_MUTUAL', 'POSITION_PRIVATE'])
        for date in list(mutual_index_data.iloc[n:].index):
            print(date)
            mutual_index_data_date = mutual_index_data[mutual_index_data.index <= date].iloc[-n1:]
            y_data = mutual_index_data_date.iloc[:, :1]
            x_data = mutual_index_data_date.iloc[:, 1:]
            try:
                model_mutual.fit(x_data, y_data)
                market_fund_position.loc[date, 'POSITION_MUTUAL'] = model_mutual.coef_.sum()
            except:
                market_fund_position.loc[date, 'POSITION_MUTUAL'] = np.nan
            private_index_data_date = private_index_data[private_index_data.index <= date].iloc[-n2:]
            y_data = private_index_data_date.iloc[:, :1]
            x_data = private_index_data_date.iloc[:, 1:]
            try:
                model_private.fit(x_data, y_data)
                market_fund_position.loc[date, 'POSITION_PRIVATE'] = model_private.coef_.sum()
            except:
                market_fund_position.loc[date, 'POSITION_PRIVATE'] = np.nan
        market_fund_position = market_fund_position.reset_index().rename(columns={'index': 'TRADE_DATE'})
        market_fund_position = market_fund_position[(market_fund_position['TRADE_DATE'] > self.start_date) & (market_fund_position['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 市场景气度
        n = 0
        index_list = ['000300', '000905', '000852', '000985']
        market_valuation_finance = self.market_valuation_finance[(self.market_valuation_finance['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & ( self.market_valuation_finance['TRADE_DATE'] <= self.end_date)]
        market_valuation_finance['INDEX_SYMBOL'] = market_valuation_finance['INDEX_SYMBOL'].apply(lambda x: x.split('.')[0])
        market_prosperity = market_valuation_finance.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='NET_PROFIT_YOY').dropna(how='all')
        market_prosperity = market_prosperity[index_list].reset_index()
        market_prosperity.columns = ['TRADE_DATE'] + ['NET_PROFIT_YOY_' + col for col in list(market_prosperity.columns)[1:]]
        market_prosperity = market_prosperity[(market_prosperity['TRADE_DATE'] > self.start_date) & (market_prosperity['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 股债性价比
        n = 0
        index_list = ['000300', '000905', '000852', '000985']
        market_valuation_finance = self.market_valuation_finance[(self.market_valuation_finance['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.market_valuation_finance['TRADE_DATE'] <= self.end_date)]
        market_valuation_finance['INDEX_SYMBOL'] = market_valuation_finance['INDEX_SYMBOL'].apply(lambda x: x.split('.')[0])
        bond_yield_10y = self.bond_yield_10y[(self.bond_yield_10y['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.bond_yield_10y['TRADE_DATE'] <= self.end_date)]
        market_valuation_finance = market_valuation_finance.merge(bond_yield_10y, on=['TRADE_DATE'], how='left')
        market_valuation_finance['EP_B'] = 1.0 / market_valuation_finance['PE_TTM'] / market_valuation_finance['BOND_YIELD_10Y']
        market_valuation_finance['B_GXL'] = market_valuation_finance['BOND_YIELD_10Y'] - market_valuation_finance['DIVIDEND_YIELD']
        market_ep_b = market_valuation_finance.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='EP_B').dropna(how='all')
        market_ep_b = market_ep_b[index_list].reset_index()
        market_ep_b.columns = ['TRADE_DATE'] + ['EP_B_' + col for col in list(market_ep_b.columns)[1:]]
        market_ep_b = market_ep_b[(market_ep_b['TRADE_DATE'] > self.start_date) & (market_ep_b['TRADE_DATE'] <= self.end_date)]
        market_b_gxl = market_valuation_finance.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='B_GXL').dropna(how='all')
        market_b_gxl = market_b_gxl[index_list].reset_index()
        market_b_gxl.columns = ['TRADE_DATE'] + ['B_GXL_' + col for col in list(market_b_gxl.columns)[1:]]
        market_b_gxl = market_b_gxl[(market_b_gxl['TRADE_DATE'] > self.start_date) & (market_b_gxl['TRADE_DATE'] <= self.end_date)]
        market_stock_bond = market_ep_b.merge(market_b_gxl, on=['TRADE_DATE'], how='outer')

        market_timing = market_total_turnover.merge(market_turnover, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_hk_cash, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_margin_balance, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_new_high, on=['TRADE_DATE'], how='outer')  \
                                             .merge(market_industry_divergence, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_fund_position, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_prosperity, on=['TRADE_DATE'], how='outer') \
                                             .merge(market_stock_bond, on=['TRADE_DATE'], how='outer')
        market_timing.to_sql('timing_market', engine, index=False, if_exists='append')
        return

    def StyleTiming(self):
        stock_finance = self.stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='left')
        stock_finance = stock_finance.merge(self.stock_daily_k[['TICKER_SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE', 'MARKET_VALUE']], on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left')
        stock_finance['CLOSE_PRICE'] = stock_finance['CLOSE_PRICE'].replace(0.0, np.nan)
        stock_finance['OPER_REVENUE_YOY_MEAN'] = stock_finance['OPER_REVENUE_YOY'].rolling(12).mean()
        stock_finance['NET_PROFIT_YOY_MEAN'] = stock_finance['NET_PROFIT_YOY'].rolling(12).mean()
        stock_finance['EP_TTM'] = stock_finance['EPS_TTM'] / stock_finance['CLOSE_PRICE']
        stock_finance['BP'] = stock_finance['NAPS'] / stock_finance['CLOSE_PRICE']
        stock_finance['CFP_TTM'] = stock_finance['OCF_TTM'] / stock_finance['CLOSE_PRICE']
        stock_finance['DP_TTM'] = stock_finance['DIVIDEND_TTM'] / stock_finance['MARKET_VALUE']
        stock_finance = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'OPER_REVENUE_YOY_MEAN', 'NET_PROFIT_YOY_MEAN', 'ROE_TTM', 'EP_TTM', 'BP', 'CFP_TTM', 'DP_TTM']]
        industry_info = get_industry_info()
        industry_info = industry_info[industry_info['INDUSTRY_TYPE'] == 1]
        industry_info = industry_info[industry_info['IS_NEW'] == 1]
        industry_info = industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        industry_symbol = get_industry_symbol()
        industry_symbol = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == 1]
        industry_symbol = industry_symbol[industry_symbol['IS_NEW'] == 1]
        industry_symbol = industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        stock_industry = get_stock_industry()
        stock_industry = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
        stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
        stock_industry = stock_industry.drop('INDUSTRY_NAME', axis=1).merge(industry_symbol, on=['INDUSTRY_ID'], how='left')
        stock_industry = stock_industry.drop('INDUSTRY_ID', axis=1).merge(industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID']], on=['INDUSTRY_NAME'], how='left')
        stock_industry = stock_industry[['INDUSTRY_ID', 'INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]
        stock_finance = stock_finance.merge(stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        stock_finance_list = []
        for date in stock_finance['END_DATE'].unique().tolist():
            stock_finance_date = stock_finance[stock_finance['END_DATE'] == date]
            for col in ['OPER_REVENUE_YOY_MEAN', 'NET_PROFIT_YOY_MEAN', 'ROE_TTM', 'EP_TTM', 'BP', 'CFP_TTM', 'DP_TTM']:
                stock_finance_date[col] = filter_extreme_mad(stock_finance_date[col])
                industry_finance = stock_finance_date[['INDUSTRY_ID', col]].groupby('INDUSTRY_ID').mean().rename(columns={col: col + '_INDU'})
                stock_finance_date = stock_finance_date.merge(industry_finance, on=['INDUSTRY_ID'], how='left')
                stock_finance_date[col] = stock_finance_date.apply(lambda x: x[col + '_INDU'] if np.isnan(x[col]) else x[col], axis=1)
                stock_finance_date[col] = (stock_finance_date[col] - stock_finance_date[col].mean()) / stock_finance_date[col].std(ddof=1)
            stock_finance_list.append(stock_finance_date)
            print(date)
        stock_finance = pd.concat(stock_finance_list)
        stock_finance = stock_finance[['TICKER_SYMBOL', 'END_DATE', 'OPER_REVENUE_YOY_MEAN', 'NET_PROFIT_YOY_MEAN', 'ROE_TTM', 'EP_TTM', 'BP', 'CFP_TTM', 'DP_TTM']]
        stock_finance['GROWTH'] = (stock_finance['OPER_REVENUE_YOY_MEAN'] + stock_finance['NET_PROFIT_YOY_MEAN'] + stock_finance['ROE_TTM']) / 3.0
        stock_finance['VALUE'] = (stock_finance['EP_TTM'] + stock_finance['BP'] + stock_finance['CFP_TTM'] + stock_finance['DP_TTM']) / 4.0
        # 成长因子
        growth = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='GROWTH').sort_index()
        growth = self.calendar_df[['CALENDAR_DATE']].set_index('CALENDAR_DATE').merge(growth, left_index=True, right_index=True, how='left')
        growth = growth.fillna(method='ffill').dropna(how='all')
        growth = growth[growth.index.isin(self.trade_df['TRADE_DATE'].unique())]
        growth = growth.unstack().reset_index()
        growth.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'GROWTH']
        # 价值因子
        value = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='VALUE').sort_index()
        value = self.calendar_df[['CALENDAR_DATE']].set_index('CALENDAR_DATE').merge(value, left_index=True, right_index=True, how='left')
        value = value.fillna(method='ffill').dropna(how='all')
        value = value[value.index.isin(self.trade_df['TRADE_DATE'].unique())]
        value = value.unstack().reset_index()
        value.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'VALUE']
        # 市值因子
        size = self.stock_daily_k[['TICKER_SYMBOL', 'TRADE_DATE', 'MARKET_VALUE']]
        size = size.groupby('TRADE_DATE').apply(lambda x: (x.set_index('TICKER_SYMBOL') - x.set_index('TICKER_SYMBOL').mean()) / x.set_index('TICKER_SYMBOL').std()).reset_index()
        size = size[['TICKER_SYMBOL', 'TRADE_DATE', 'MARKET_VALUE']]
        size.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'MARKET_VALUE']

        n = 60
        stock_daily_k = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_turnover = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='TURNOVER_RATE').sort_index()
        stock_turnover = stock_turnover.rolling(n).mean()
        stock_volatility = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='PCT_CHANGE').sort_index()
        stock_volatility = stock_volatility.rolling(n).std()
        bmk_beta = HBDB().read_index_daily_k_given_date_and_indexs((datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d'), ['881001'])
        bmk_beta['jyrq'] = bmk_beta['jyrq'].astype(str)
        bmk_beta = bmk_beta.pivot(index='jyrq', columns='zqdm', values='spjg').sort_index().pct_change()
        stock_beta = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='PCT_CHANGE').sort_index()

        ###########################################################################################################################
        # 风格拥挤度
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > self.start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        style_crowding = pd.DataFrame(index=trade_df['TRADE_DATE'].unique().tolist(), columns=['GROWTH_CROWDING', 'VALUE_CROWDING', 'SIZE_CROWDING'])
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_beta_date = stock_beta[stock_beta.index <= date].iloc[-n:]
            bmk_beta_date = bmk_beta[bmk_beta.index <= date].iloc[-n:]
            stock_beta_date = pd.DataFrame(stock_beta_date.apply(lambda x: np.cov(x, bmk_beta_date['881001'])[0, 1] / np.var(bmk_beta_date['881001'])), columns=[date]).T

            growth_date = growth[growth['TRADE_DATE'] == date]
            growth_top_tickers = growth_date[growth_date['GROWTH'] >= growth_date['GROWTH'].quantile(0.8)]['TICKER_SYMBOL'].unique().tolist()
            growth_bottom_tickers = growth_date[growth_date['GROWTH'] <= growth_date['GROWTH'].quantile(0.2)]['TICKER_SYMBOL'].unique().tolist()
            growth_top_tickers = list(set(growth_top_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            growth_bottom_tickers = list(set(growth_bottom_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            style_crowding.loc[date, 'GROWTH_CROWDING'] = (stock_turnover.loc[date, growth_top_tickers].mean() / stock_turnover.loc[date, growth_bottom_tickers].mean() +
                                                           stock_volatility.loc[date, growth_top_tickers].mean() / stock_volatility.loc[date, growth_bottom_tickers].mean() +
                                                           stock_beta_date.loc[date, growth_top_tickers].mean() / stock_beta_date.loc[date, growth_bottom_tickers].mean()) / 3.0
            value_date = value[value['TRADE_DATE'] == date]
            value_top_tickers = value_date[value_date['VALUE'] >= value_date['VALUE'].quantile(0.8)]['TICKER_SYMBOL'].unique().tolist()
            value_bottom_tickers = value_date[value_date['VALUE'] <= value_date['VALUE'].quantile(0.2)]['TICKER_SYMBOL'].unique().tolist()
            value_top_tickers = list(set(value_top_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            value_bottom_tickers = list(set(value_bottom_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            style_crowding.loc[date, 'VALUE_CROWDING'] = (stock_turnover.loc[date, value_top_tickers].mean() / stock_turnover.loc[date, value_bottom_tickers].mean() +
                                                          stock_volatility.loc[date, value_top_tickers].mean() / stock_volatility.loc[date, value_bottom_tickers].mean() +
                                                          stock_beta_date.loc[date, value_top_tickers].mean() / stock_beta_date.loc[date, value_bottom_tickers].mean()) / 3.0
            size_date = size[size['TRADE_DATE'] == date]
            size_top_tickers = size_date[size_date['MARKET_VALUE'] >= size_date['MARKET_VALUE'].quantile(0.8)]['TICKER_SYMBOL'].unique().tolist()
            size_bottom_tickers = size_date[size_date['MARKET_VALUE'] <= size_date['MARKET_VALUE'].quantile(0.2)]['TICKER_SYMBOL'].unique().tolist()
            size_top_tickers = list(set(size_top_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            size_bottom_tickers = list(set(size_bottom_tickers) & set(list(stock_turnover.columns)) & set(list(stock_volatility.columns)) & set(list(stock_beta.columns)))
            style_crowding.loc[date, 'SIZE_CROWDING'] = (stock_turnover.loc[date, size_top_tickers].mean() / stock_turnover.loc[date, size_bottom_tickers].mean() +
                                                         stock_volatility.loc[date, size_top_tickers].mean() /  stock_volatility.loc[date, size_bottom_tickers].mean() +
                                                         stock_beta_date.loc[date, size_top_tickers].mean() / stock_beta_date.loc[date, size_bottom_tickers].mean()) / 3.0
            print(date)
        style_crowding = style_crowding.reset_index().rename(columns={'index': 'TRADE_DATE'})
        style_crowding = style_crowding[(style_crowding['TRADE_DATE'] > self.start_date) & (style_crowding['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 风格离散度
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > self.start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        style_spread = pd.DataFrame(index=trade_df['TRADE_DATE'].unique().tolist(), columns=['GROWTH_SPREAD', 'VALUE_SPREAD', 'SIZE_SPREAD'])
        for date in trade_df['TRADE_DATE'].unique().tolist():
            growth_date = growth[growth['TRADE_DATE'] == date]
            style_spread.loc[date, 'GROWTH_SPREAD'] = growth_date[growth_date['GROWTH'] >= growth_date['GROWTH'].quantile(0.8)]['GROWTH'].median() - growth_date[growth_date['GROWTH'] <= growth_date['GROWTH'].quantile(0.2)]['GROWTH'].median()
            value_date = value[value['TRADE_DATE'] == date]
            style_spread.loc[date, 'VALUE_SPREAD'] = value_date[value_date['VALUE'] >= value_date['VALUE'].quantile(0.8)]['VALUE'].median() - value_date[value_date['VALUE'] <= value_date['VALUE'].quantile(0.2)]['VALUE'].median()
            size_date = size[size['TRADE_DATE'] == date]
            style_spread.loc[date, 'SIZE_SPREAD'] = size_date[size_date['MARKET_VALUE'] >= size_date['MARKET_VALUE'].quantile(0.8)]['MARKET_VALUE'].median() - size_date[size_date['MARKET_VALUE'] <= size_date['MARKET_VALUE'].quantile(0.2)]['MARKET_VALUE'].median()
            print(date)
        style_spread = style_spread.reset_index().rename(columns={'index': 'TRADE_DATE'})
        style_spread = style_spread[(style_spread['TRADE_DATE'] > self.start_date) & (style_spread['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 风格动量
        n = 250
        stock_daily_k = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        growth = growth[(growth['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (growth['TRADE_DATE'] <= self.end_date)]
        value = value[(value['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (value['TRADE_DATE'] <= self.end_date)]
        size = size[(size['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (size['TRADE_DATE'] <= self.end_date)]
        stock_daily_k = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        stock_daily_k = stock_daily_k.replace(0.0, np.nan)
        forward_return = stock_daily_k.pct_change(20)
        forward_return = forward_return.unstack().reset_index()
        forward_return.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'FORWARD_RETURN']
        growth_ic = growth.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='GROWTH').sort_index()
        growth_ic = growth_ic.shift(20)
        growth_ic = growth_ic.unstack().reset_index()
        growth_ic.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'GROWTH']
        growth_ic = growth_ic.merge(forward_return, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left')
        growth_ic = growth_ic.dropna()
        growth_ic = growth_ic.drop('TICKER_SYMBOL', axis=1).groupby('TRADE_DATE').corr().reset_index().set_index('level_1').rename(columns={'FORWARD_RETURN': 'GROWTH_IC'})
        growth_ic = growth_ic.loc[growth_ic.index == 'GROWTH'].reset_index().drop(['GROWTH', 'level_1'], axis=1)
        growth_ic['GROWTH_MOMENTUM'] = growth_ic['GROWTH_IC'].rolling(250).apply(lambda x: (x.iloc[-1] - x.mean()) / x.std())
        value_ic = value.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='VALUE').sort_index()
        value_ic = value_ic.shift(20)
        value_ic = value_ic.unstack().reset_index()
        value_ic.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'VALUE']
        value_ic = value_ic.merge(forward_return, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left')
        value_ic = value_ic.dropna()
        value_ic = value_ic.drop('TICKER_SYMBOL', axis=1).groupby('TRADE_DATE').corr().reset_index().set_index( 'level_1').rename(columns={'FORWARD_RETURN': 'VALUE_IC'})
        value_ic = value_ic.loc[value_ic.index == 'VALUE'].reset_index().drop(['VALUE', 'level_1'], axis=1)
        value_ic['VALUE_MOMENTUM'] = value_ic['VALUE_IC'].rolling(250).apply(lambda x: (x.iloc[-1] - x.mean()) / x.std())
        size_ic = size.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='MARKET_VALUE').sort_index()
        size_ic = size_ic.shift(20)
        size_ic = size_ic.unstack().reset_index()
        size_ic.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'MARKET_VALUE']
        size_ic = size_ic.merge(forward_return, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left')
        size_ic = size_ic.dropna()
        size_ic = size_ic.drop('TICKER_SYMBOL', axis=1).groupby('TRADE_DATE').corr().reset_index().set_index('level_1').rename(columns={'FORWARD_RETURN': 'SIZE_IC'})
        size_ic = size_ic.loc[size_ic.index == 'MARKET_VALUE'].reset_index().drop(['MARKET_VALUE', 'level_1'], axis=1)
        size_ic['SIZE_MOMENTUM'] = size_ic['SIZE_IC'].rolling(250).apply(lambda x: (x.iloc[-1] - x.mean()) / x.std())
        style_momentum = growth_ic[['TRADE_DATE', 'GROWTH_MOMENTUM']].merge(value_ic[['TRADE_DATE', 'VALUE_MOMENTUM']], on=['TRADE_DATE'], how='left').merge(size_ic[['TRADE_DATE', 'SIZE_MOMENTUM']], on=['TRADE_DATE'], how='left')
        style_momentum = style_momentum[(style_momentum['TRADE_DATE'] > self.start_date) & (style_momentum['TRADE_DATE'] <= self.end_date)]

        style_timing = style_crowding.merge(style_spread, on=['TRADE_DATE'], how='outer').merge(style_momentum, on=['TRADE_DATE'], how='outer')
        style_timing.to_sql('timing_style', engine, index=False, if_exists='append')
        return

    def IndustryTiming(self):
        ###########################################################################################################################
        # 行业拥挤度
        # 量能：成交额占比：行业指数成交额/市场成交额
        n = 0
        stock_turnover = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_turnover = stock_turnover[['TRADE_DATE', 'TICKER_SYMBOL', 'TURNOVER_VALUE']]
        stock_turnover = stock_turnover[stock_turnover['TURNOVER_VALUE'] > 0.0]
        total_turnover = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'TURNOVER_VALUE': 'TOTAL_TURNOVER_VALUE'})
        industry_turnover = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        industry_turnover = industry_turnover[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_VALUE']]
        industry_turnover = industry_turnover[industry_turnover['TURNOVER_VALUE'] > 0.0]
        industry_turnover = industry_turnover[industry_turnover['INDEX_SYMBOL'].isin(self.industry_list)]
        industry_turnover_proportion = industry_turnover.merge(total_turnover, on=['TRADE_DATE'], how='left')
        industry_turnover_proportion['TURNOVER_PROPORTION'] = industry_turnover_proportion['TURNOVER_VALUE'] / industry_turnover_proportion['TOTAL_TURNOVER_VALUE']
        industry_turnover_proportion = industry_turnover_proportion[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_PROPORTION']]
        industry_turnover_proportion = industry_turnover_proportion[(industry_turnover_proportion['TRADE_DATE'] > self.start_date) & (industry_turnover_proportion['TRADE_DATE'] <= self.end_date)]

        # 量能：换手率：行业指数成交额/市场市值
        n = 0
        stock_market_value = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_market_value = stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'NEG_MARKET_VALUE']]
        stock_market_value = stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        stock_market_value = stock_market_value.dropna()
        total_market_value = stock_market_value[['TRADE_DATE', 'INDUSTRY_ID', 'NEG_MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_ID']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL'})
        industry_turnover = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        industry_turnover = industry_turnover[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_VALUE']]
        industry_turnover = industry_turnover[industry_turnover['TURNOVER_VALUE'] > 0.0]
        industry_turnover = industry_turnover[industry_turnover['INDEX_SYMBOL'].isin(self.industry_list)]
        industry_turnover_rate = industry_turnover.merge(total_market_value, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        industry_turnover_rate['TURNOVER_RATE'] = industry_turnover_rate['TURNOVER_VALUE'] / industry_turnover_rate['NEG_MARKET_VALUE']
        industry_turnover_rate = industry_turnover_rate[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_RATE']]
        industry_turnover_rate = industry_turnover_rate[(industry_turnover_rate['TRADE_DATE'] > self.start_date) & (industry_turnover_rate['TRADE_DATE'] <= self.end_date)]

        # 量能：量价相关系数：近20日收盘价与换手率之间的相关系数
        n = 20
        stock_market_value = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_market_value = stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'NEG_MARKET_VALUE']]
        stock_market_value = stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        stock_market_value = stock_market_value.dropna()
        total_market_value = stock_market_value[['TRADE_DATE', 'INDUSTRY_ID', 'NEG_MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_ID']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL'})
        industry_turnover = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        industry_turnover = industry_turnover[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_VALUE']]
        industry_turnover = industry_turnover[industry_turnover['TURNOVER_VALUE'] > 0.0]
        industry_turnover = industry_turnover[industry_turnover['INDEX_SYMBOL'].isin(self.industry_list)]
        turnover_rate = industry_turnover.merge(total_market_value, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        turnover_rate['TURNOVER_RATE'] = turnover_rate['TURNOVER_VALUE'] / turnover_rate['NEG_MARKET_VALUE']
        turnover_rate = turnover_rate[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_RATE']].dropna()
        industry_cprice = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        industry_cprice = industry_cprice[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        industry_cprice = industry_cprice[industry_cprice['INDEX_SYMBOL'].isin(self.industry_list)]
        industry_corr = industry_cprice.merge(turnover_rate, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        industry_corr = industry_corr.sort_values(['INDEX_SYMBOL', 'TRADE_DATE']).set_index('TRADE_DATE')
        industry_corr = industry_corr.groupby('INDEX_SYMBOL').rolling(window=n, min_periods=n, center=False).corr().reset_index().set_index('level_2').rename(columns={'TURNOVER_RATE': 'CORR'})
        industry_corr = industry_corr.loc[industry_corr.index == 'CLOSE_INDEX'].reset_index().drop(['CLOSE_INDEX', 'level_2'], axis=1)
        industry_corr = industry_corr[['TRADE_DATE', 'INDEX_SYMBOL', 'CORR']]
        industry_corr = industry_corr[(industry_corr['TRADE_DATE'] > self.start_date) & (industry_corr['TRADE_DATE'] <= self.end_date)]

        # 价格：行业内创60日新高个股数量及占比
        n = 60
        stock_daily_k = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_daily_k = stock_daily_k.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_daily_k = stock_daily_k[stock_daily_k['TRADE_DATE'] >= stock_daily_k['SAMPLE_DATE']]
        stock_daily_k = stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']]
        stock_daily_k_max = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        stock_daily_k_max = stock_daily_k_max.rolling(n).max()
        stock_daily_k_max = stock_daily_k_max.unstack().reset_index()
        stock_daily_k_max.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE_MAX']
        stock_new_high = stock_daily_k.merge(stock_daily_k_max, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        stock_new_high['NEW_HIGH'] = (stock_new_high['CLOSE_PRICE'] >= stock_new_high['CLOSE_PRICE_MAX']).astype(int)
        stock_new_high = stock_new_high.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        industry_new_high_count = stock_new_high[['INDUSTRY_ID', 'TRADE_DATE', 'NEW_HIGH']].groupby(['INDUSTRY_ID', 'TRADE_DATE']).count().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'NEW_HIGH': 'COUNT'})
        industry_new_high = stock_new_high[['INDUSTRY_ID', 'TRADE_DATE', 'NEW_HIGH']].groupby(['INDUSTRY_ID', 'TRADE_DATE']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL'})
        industry_new_high = industry_new_high.merge(industry_new_high_count, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
        industry_new_high['NEW_HIGH_RATIO'] = industry_new_high['NEW_HIGH'] / industry_new_high['COUNT']
        industry_new_high = industry_new_high[['TRADE_DATE', 'INDEX_SYMBOL', 'NEW_HIGH', 'NEW_HIGH_RATIO']]
        industry_new_high = industry_new_high[(industry_new_high['TRADE_DATE'] > self.start_date) & (industry_new_high['TRADE_DATE'] <= self.end_date)]

        # 价格：行业内20日均线上个股数量及占比
        n = 20
        stock_daily_k = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_daily_k = stock_daily_k.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_daily_k = stock_daily_k[stock_daily_k['TRADE_DATE'] >= stock_daily_k['SAMPLE_DATE']]
        stock_daily_k = stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']]
        stock_daily_k_mean = stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        stock_daily_k_mean = stock_daily_k_mean.rolling(n).mean()
        stock_daily_k_mean = stock_daily_k_mean.unstack().reset_index()
        stock_daily_k_mean.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE_MEAN']
        stock_mean_above = stock_daily_k.merge(stock_daily_k_mean, on=['TICKER_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        stock_mean_above['MEAN_ABOVE'] = (stock_mean_above['CLOSE_PRICE'] >= stock_mean_above['CLOSE_PRICE_MEAN']).astype(int)
        stock_mean_above = stock_mean_above.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        industry_mean_above_count = stock_mean_above[['INDUSTRY_ID', 'TRADE_DATE', 'MEAN_ABOVE']].groupby(['INDUSTRY_ID', 'TRADE_DATE']).count().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'MEAN_ABOVE': 'COUNT'})
        industry_mean_above = stock_mean_above[['INDUSTRY_ID', 'TRADE_DATE', 'MEAN_ABOVE']].groupby(['INDUSTRY_ID', 'TRADE_DATE']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL'})
        industry_mean_above = industry_mean_above.merge(industry_mean_above_count, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
        industry_mean_above['MEAN_ABOVE_RATIO'] = industry_mean_above['MEAN_ABOVE'] / industry_mean_above['COUNT']
        industry_mean_above = industry_mean_above[['TRADE_DATE', 'INDEX_SYMBOL', 'MEAN_ABOVE', 'MEAN_ABOVE_RATIO']]
        industry_mean_above = industry_mean_above[(industry_mean_above['TRADE_DATE'] > self.start_date) & (industry_mean_above['TRADE_DATE'] <= self.end_date)]

        # 资金：主力资金净流入率：行业指数主力（超大单和大单）净流入金额/行业指数成交额
        n = 0
        industry_main_cash = self.industry_main_cash[(self.industry_main_cash['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.industry_main_cash['TRADE_DATE'] <= self.end_date)]
        industry_turnover = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        industry_turnover = industry_turnover[['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_VALUE']]
        industry_turnover = industry_turnover[industry_turnover['TURNOVER_VALUE'] > 0.0]
        industry_turnover = industry_turnover[industry_turnover['INDEX_SYMBOL'].isin(self.industry_list)]
        industry_main_cash_proportion = industry_main_cash.merge(industry_turnover, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        industry_main_cash_proportion['MAIN_CASH_PROPORTION'] = industry_main_cash_proportion['INDUSTRY_MAIN_CASH'] / industry_main_cash_proportion['TURNOVER_VALUE']
        industry_main_cash_proportion = industry_main_cash_proportion[['TRADE_DATE', 'INDEX_SYMBOL', 'MAIN_CASH_PROPORTION']]
        industry_main_cash_proportion = industry_main_cash_proportion[(industry_main_cash_proportion['TRADE_DATE'] > self.start_date) & (industry_main_cash_proportion['TRADE_DATE'] <= self.end_date)]

        # 资金：融资买入情绪：行业融资买入额/行业指数成交额
        n = 0
        industry_margin_proportion = self.industry_margin_proportion[(self.industry_margin_proportion['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.industry_margin_proportion['TRADE_DATE'] <= self.end_date)]
        industry_margin_proportion = industry_margin_proportion[['TRADE_DATE', 'INDUSTRY_ID', 'MARGIN_PROPORTION']].rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL'})
        industry_margin_proportion['MARGIN_PROPORTION'] = industry_margin_proportion['MARGIN_PROPORTION'] / 100.0
        industry_margin_proportion = industry_margin_proportion[(industry_margin_proportion['TRADE_DATE'] > self.start_date) & (industry_margin_proportion['TRADE_DATE'] <= self.end_date)]

        # 分析师情绪：行业内个股近三月买入、增持评级研报数量/行业内个股数量

        # 分析师情绪：一致预期：一致预期净利润、一致预期评级、一致预期目标价上调个股数量占比
        n = 90
        stock_consensus = self.stock_consensus[(self.stock_consensus['EST_DT'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_consensus['EST_DT'] <= self.end_date)]
        stock_consensus_before = stock_consensus.pivot(index='EST_DT', columns='TICKER_SYMBOL', values='EST_NET_PROFIT').sort_index()
        stock_consensus_before = stock_consensus_before.shift(n)
        stock_consensus_before = stock_consensus_before.unstack().reset_index()
        stock_consensus_before.columns = ['TICKER_SYMBOL', 'EST_DT', 'EST_NET_PROFIT_BEFORE']
        stock_consensus_up = stock_consensus.merge(stock_consensus_before, on=['TICKER_SYMBOL', 'EST_DT'], how='left').dropna()
        stock_consensus_up['CONSENSUS_UP'] = (stock_consensus_up['EST_NET_PROFIT'] > stock_consensus_up['EST_NET_PROFIT_BEFORE']).astype(int)
        stock_consensus_up = stock_consensus_up.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        industry_consensus_up_count = stock_consensus_up[['INDUSTRY_ID', 'EST_DT', 'CONSENSUS_UP']].groupby(['INDUSTRY_ID', 'EST_DT']).count().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'EST_DT': 'TRADE_DATE', 'CONSENSUS_UP': 'COUNT'})
        industry_consensus_up = stock_consensus_up[['INDUSTRY_ID', 'EST_DT', 'CONSENSUS_UP']].groupby(['INDUSTRY_ID', 'EST_DT']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'EST_DT': 'TRADE_DATE'})
        industry_consensus_up = industry_consensus_up.merge(industry_consensus_up_count, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
        industry_consensus_up['CONSENSUS_UP_RATIO'] = industry_consensus_up['CONSENSUS_UP'] / industry_consensus_up['COUNT']
        industry_consensus_up = industry_consensus_up[['TRADE_DATE', 'INDEX_SYMBOL', 'CONSENSUS_UP', 'CONSENSUS_UP_RATIO']]
        stock_consensus_down = stock_consensus.merge(stock_consensus_before, on=['TICKER_SYMBOL', 'EST_DT'], how='left').dropna()
        stock_consensus_down['CONSENSUS_DOWN'] = (stock_consensus_down['EST_NET_PROFIT'] < stock_consensus_down['EST_NET_PROFIT_BEFORE']).astype(int)
        stock_consensus_down = stock_consensus_down.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        industry_consensus_down_count = stock_consensus_down[['INDUSTRY_ID', 'EST_DT', 'CONSENSUS_DOWN']].groupby(['INDUSTRY_ID', 'EST_DT']).count().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'EST_DT': 'TRADE_DATE', 'CONSENSUS_DOWN': 'COUNT'})
        industry_consensus_down = stock_consensus_down[['INDUSTRY_ID', 'EST_DT', 'CONSENSUS_DOWN']].groupby(['INDUSTRY_ID', 'EST_DT']).sum().reset_index().rename(columns={'INDUSTRY_ID': 'INDEX_SYMBOL', 'EST_DT': 'TRADE_DATE'})
        industry_consensus_down = industry_consensus_down.merge(industry_consensus_down_count,on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
        industry_consensus_down['CONSENSUS_DOWN_RATIO'] = industry_consensus_down['CONSENSUS_DOWN'] / industry_consensus_down['COUNT']
        industry_consensus_down = industry_consensus_down[['TRADE_DATE', 'INDEX_SYMBOL', 'CONSENSUS_DOWN', 'CONSENSUS_DOWN_RATIO']]
        industry_consensus = industry_consensus_up.merge(industry_consensus_down, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer')
        industry_consensus = industry_consensus[(industry_consensus['TRADE_DATE'] > self.start_date) & (industry_consensus['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 行业动量
        n = 20
        index_daily_k = self.index_daily_k[(self.index_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.index_daily_k['TRADE_DATE'] <= self.end_date)]
        index_daily_k = index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        index_daily_k = index_daily_k[index_daily_k['INDEX_SYMBOL'].isin(self.industry_list)]
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        industry_momentum = index_daily_k.replace(0.0, np.nan).pct_change(n)
        industry_momentum = industry_momentum.unstack().reset_index()
        industry_momentum.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'INDUSTRY_MOMENTUM']
        industry_momentum = industry_momentum[['TRADE_DATE', 'INDEX_SYMBOL', 'INDUSTRY_MOMENTUM']]
        industry_momentum = industry_momentum[(industry_momentum['TRADE_DATE'] > self.start_date) & (industry_momentum['TRADE_DATE'] <= self.end_date)]

        ###########################################################################################################################
        # 行业景气度
        stock_finance = self.stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        oper_revenue_yoy = stock_finance[['END_DATE', 'TICKER_SYMBOL', 'OPER_REVENUE_YOY']]
        oper_revenue_yoy = oper_revenue_yoy.set_index('TICKER_SYMBOL').groupby('END_DATE').apply(lambda x: filter_extreme_mad(x['OPER_REVENUE_YOY'])).reset_index()
        oper_revenue_yoy = oper_revenue_yoy.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        oper_revenue_yoy = oper_revenue_yoy[['END_DATE', 'INDUSTRY_ID', 'OPER_REVENUE_YOY']].groupby(['END_DATE', 'INDUSTRY_ID']).mean().reset_index()
        oper_revenue_yoy = oper_revenue_yoy.pivot(index='END_DATE', columns='INDUSTRY_ID', values='OPER_REVENUE_YOY').sort_index()
        oper_revenue_yoy_diff = oper_revenue_yoy.diff()
        oper_revenue_yoy_diff = oper_revenue_yoy_diff.unstack().reset_index()
        oper_revenue_yoy_diff.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'OPER_REVENUE_YOY_DIFF']
        oper_revenue_yoy_diff = oper_revenue_yoy_diff[['TRADE_DATE', 'INDEX_SYMBOL', 'OPER_REVENUE_YOY_DIFF']]
        net_profit_yoy = stock_finance[['END_DATE', 'TICKER_SYMBOL', 'NET_PROFIT_YOY']]
        net_profit_yoy = net_profit_yoy.set_index('TICKER_SYMBOL').groupby('END_DATE').apply(lambda x: filter_extreme_mad(x['NET_PROFIT_YOY'])).reset_index()
        net_profit_yoy = net_profit_yoy.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        net_profit_yoy = net_profit_yoy[['END_DATE', 'INDUSTRY_ID', 'NET_PROFIT_YOY']].groupby(['END_DATE', 'INDUSTRY_ID']).mean().reset_index()
        net_profit_yoy = net_profit_yoy.pivot(index='END_DATE', columns='INDUSTRY_ID', values='NET_PROFIT_YOY').sort_index()
        net_profit_yoy_diff = net_profit_yoy.diff()
        net_profit_yoy_diff = net_profit_yoy_diff.unstack().reset_index()
        net_profit_yoy_diff.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'NET_PROFIT_YOY_DIFF']
        net_profit_yoy_diff = net_profit_yoy_diff[['TRADE_DATE', 'INDEX_SYMBOL', 'NET_PROFIT_YOY_DIFF']]
        roe_ttm = stock_finance[['END_DATE', 'TICKER_SYMBOL', 'ROE_TTM']]
        roe_ttm = roe_ttm.set_index('TICKER_SYMBOL').groupby('END_DATE').apply(lambda x: filter_extreme_mad(x['ROE_TTM'])).reset_index()
        roe_ttm = roe_ttm.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
        roe_ttm = roe_ttm[['END_DATE', 'INDUSTRY_ID', 'ROE_TTM']].groupby(['END_DATE', 'INDUSTRY_ID']).mean().reset_index()
        roe_ttm = roe_ttm.pivot(index='END_DATE', columns='INDUSTRY_ID', values='ROE_TTM').sort_index()
        roe_ttm_diff = roe_ttm.diff()
        roe_ttm_diff = roe_ttm_diff.unstack().reset_index()
        roe_ttm_diff.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'ROE_TTM_DIFF']
        roe_ttm_diff = roe_ttm_diff[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE_TTM_DIFF']]
        industry_prosperity = oper_revenue_yoy_diff.merge(net_profit_yoy_diff, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer').merge(roe_ttm_diff, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer')
        industry_prosperity = industry_prosperity[(industry_prosperity['TRADE_DATE'] > self.start_date) & (industry_prosperity['TRADE_DATE'] <= self.end_date)]

        industry_timing = industry_turnover_proportion.merge(industry_turnover_rate, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_corr, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_new_high, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_mean_above, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_main_cash_proportion, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_margin_proportion, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_consensus, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_momentum, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer') \
                                                      .merge(industry_prosperity, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='outer')
        industry_timing.to_sql('timing_industry', engine, index=False, if_exists='append')
        return

    def StockTiming(self):
        # 个股拥挤度
        # 前5%、10%个股成交额/市场成交额
        n = 0
        stock_turnover = self.stock_daily_k[(self.stock_daily_k['TRADE_DATE'] > (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(n * 2)).strftime('%Y%m%d')) & (self.stock_daily_k['TRADE_DATE'] <= self.end_date)]
        stock_turnover = stock_turnover[['TRADE_DATE', 'TICKER_SYMBOL', 'TURNOVER_VALUE']]
        stock_turnover = stock_turnover[stock_turnover['TURNOVER_VALUE'] > 0.0]
        top5_turnover_thresh = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').quantile(0.95).reset_index().rename(columns={'TURNOVER_VALUE': 'TURNOVER_VALUE_Q'})
        top10_turnover_thresh = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').quantile(0.90).reset_index().rename(columns={'TURNOVER_VALUE': 'TURNOVER_VALUE_Q'})
        top5_turnover = stock_turnover.merge(top5_turnover_thresh, on=['TRADE_DATE'], how='left')
        top10_turnover = stock_turnover.merge(top10_turnover_thresh, on=['TRADE_DATE'], how='left')
        top5_turnover = top5_turnover[top5_turnover['TURNOVER_VALUE'] > top5_turnover['TURNOVER_VALUE_Q']]
        top10_turnover = top10_turnover[top10_turnover['TURNOVER_VALUE'] > top10_turnover['TURNOVER_VALUE_Q']]
        top5_turnover = top5_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'TURNOVER_VALUE': 'TOP5_TURNOVER_VALUE'})
        top10_turnover = top10_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'TURNOVER_VALUE': 'TOP10_TURNOVER_VALUE'})
        market_stock_turnover = stock_turnover[['TRADE_DATE', 'TURNOVER_VALUE']].groupby('TRADE_DATE').sum().reset_index().rename(columns={'TURNOVER_VALUE': 'MARKET_TURNOVER_VALUE'})
        stock_turnover_proportion = top5_turnover.merge(top10_turnover, on=['TRADE_DATE'], how='left').merge(market_stock_turnover, on=['TRADE_DATE'], how='left')
        stock_turnover_proportion['TURNOVER_PROPORTION_TOP5'] = stock_turnover_proportion['TOP5_TURNOVER_VALUE'] / stock_turnover_proportion['MARKET_TURNOVER_VALUE']
        stock_turnover_proportion['TURNOVER_PROPORTION_TOP10'] = stock_turnover_proportion['TOP10_TURNOVER_VALUE'] / stock_turnover_proportion['MARKET_TURNOVER_VALUE']
        stock_turnover_proportion = stock_turnover_proportion[['TRADE_DATE', 'TURNOVER_PROPORTION_TOP5', 'TURNOVER_PROPORTION_TOP10']]
        stock_turnover_proportion = stock_turnover_proportion[(stock_turnover_proportion['TRADE_DATE'] > self.start_date) & (stock_turnover_proportion['TRADE_DATE'] <= self.end_date)]

        stock_turnover_proportion.to_sql('timing_stock', engine, index=False, if_exists='append')
        return


if __name__ == '__main__':
    start_date = '20221209'
    end_date = '20221230'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/timing/'
    sw_type = 1
    timing = Timing(start_date, end_date, data_path, sw_type)
    timing.MarketTiming()
    timing.StyleTiming()
    timing.IndustryTiming()
    timing.StockTiming()


