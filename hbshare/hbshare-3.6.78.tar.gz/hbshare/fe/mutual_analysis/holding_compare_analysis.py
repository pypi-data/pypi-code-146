# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})
cell_dic = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M',
            14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def holding_operation(stock, fund_code, fund_start_date=None):
    all_fund = HBDB().read_fund_info()
    all_fund = all_fund.rename(columns={'jjdm': 'FUND_CODE', 'jjjc': 'FUND_NAME'})
    all_fund = all_fund[all_fund['FUND_CODE'] == fund_code]
    all_fund = all_fund[['FUND_CODE', 'FUND_NAME']].drop_duplicates('FUND_CODE', keep='last')
    fund_name = all_fund['FUND_NAME'].values[0]

    calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df = get_date('19900101', datetime.today().strftime('%Y%m%d'))

    if stock[:2] != '68':
        stock_daily_k = HBDB().read_stock_daily_k_given_code(stock)
    else:
        stock_daily_k = HBDB().read_star_stock_daily_k_given_code(stock)
    stock_daily_k['TRADE_DATE'] = stock_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
    stock_daily_k = stock_daily_k.sort_values('TRADE_DATE')
    stock_name = stock_daily_k['SEC_SHORT_NAME'].values[0]

    fund_holding = HBDB().read_fund_holding_given_codes([fund_code])
    fund_holding = fund_holding.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ccsz': 'HOLDING_MARKET_VALUE', 'ccsl': 'HOLDING_AMOUNT', 'zjbl': 'MV_IN_NA'})
    fund_holding['REPORT_DATE'] = fund_holding['REPORT_DATE'].astype(str)
    fund_start_date = fund_holding['REPORT_DATE'].min() if fund_start_date is None else fund_start_date
    fund_holding_season = fund_holding.copy(deep=True)
    fund_holding_season['MONTH'] = fund_holding_season['REPORT_DATE'].apply(lambda x: x[4:6])
    fund_holding_season = fund_holding_season[fund_holding_season['MONTH'].isin(['03', '09'])]
    fund_holding_min = fund_holding_season[['REPORT_DATE', 'MV_IN_NA']].groupby(['REPORT_DATE']).min().reset_index().rename(columns={'MV_IN_NA': 'MV_IN_NA_MIN'})
    fund_holding_min['MV_IN_NA_MIN'] = fund_holding_min['MV_IN_NA_MIN'].apply(lambda x: '<{0}'.format(round(x, 2)))
    fund_holding = fund_holding[fund_holding['TICKER_SYMBOL'] == stock]
    disp_dates = report_df[report_df['REPORT_DATE'] >= fund_start_date]['REPORT_DATE'].unique().tolist()
    fund_holding = fund_holding.set_index('REPORT_DATE')
    fund_holding = fund_holding.reindex(disp_dates)
    fund_holding.loc[(fund_holding.index.str.slice(4, 6).isin(['06', '12'])) & (fund_holding['MV_IN_NA'].isnull()), 'MV_IN_NA'] = 0.0
    fund_holding = pd.concat([fund_holding, fund_holding_min[['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
    fund_holding.loc[(fund_holding.index.str.slice(4, 6).isin(['03', '09'])) & (fund_holding['MV_IN_NA'].isnull()), 'MV_IN_NA'] = fund_holding.loc[(fund_holding.index.str.slice(4, 6).isin(['03', '09'])) & (fund_holding['MV_IN_NA'].isnull()), 'MV_IN_NA_MIN']
    fund_holding = fund_holding.drop('MV_IN_NA_MIN', axis=1)
    fund_holding['MV_IN_NA_STR'] = fund_holding['MV_IN_NA'].astype(str)
    fund_holding = fund_holding.reset_index()
    fund_holding = fund_holding.merge(calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
    fund_holding['TRADE_DATE'] = fund_holding['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
    fund_holding = fund_holding.sort_values('TRADE_DATE')
    fund_holding = fund_holding.merge(stock_daily_k[['TRADE_DATE', 'CLOSE_PRICE']], on=['TRADE_DATE'], how='left')
    fund_holding_quancang = fund_holding.loc[fund_holding['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
    fund_holding_quancang['MV_IN_NA'] = fund_holding_quancang['MV_IN_NA'].astype(float)

    stock_daily_k = stock_daily_k[stock_daily_k['TRADE_DATE'] >= datetime.strptime(fund_start_date, '%Y%m%d') - timedelta(30)]
    data = stock_daily_k[['TRADE_DATE', 'CLOSE_PRICE']].merge(fund_holding[['TRADE_DATE', 'MV_IN_NA_STR']], on=['TRADE_DATE'], how='left').merge(fund_holding_quancang[['TRADE_DATE', 'MV_IN_NA']], on=['TRADE_DATE'], how='left')
    data['INDEX'] = range(len(data))
    dates = data[['TRADE_DATE']].sort_values('TRADE_DATE')
    dates['YEAR_MONTH'] = dates['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
    dates = dates.drop_duplicates('YEAR_MONTH', keep='last')
    dates = dates.loc[dates['YEAR_MONTH'].str.slice(4, 6).isin(['03', '06', '09', '12'])]
    data = data.merge(dates[['TRADE_DATE', 'YEAR_MONTH']], on=['TRADE_DATE'], how='left')

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(data['INDEX'], data['CLOSE_PRICE'], color='#F04950', label='{0}'.format(stock_name))
    ax2.bar(data['INDEX'], data['MV_IN_NA'], width=len(stock_daily_k) / len(fund_holding_quancang) / 10, color='#C94649', label='占净值比（%）')
    ax2.set_ylim([0, 50])
    ax1.scatter(data.dropna(subset=['MV_IN_NA_STR'])['INDEX'], data.dropna(subset=['MV_IN_NA_STR'])['CLOSE_PRICE'], color='#6268A2', label='{0}中该个股持仓占净值比（%）'.format(fund_name))
    for x, y, value in zip(list(data.dropna(subset=['MV_IN_NA_STR'])['INDEX']), list(data.dropna(subset=['MV_IN_NA_STR'])['CLOSE_PRICE']), list(data.dropna(subset=['MV_IN_NA_STR'])['MV_IN_NA_STR'])):
        ax1.text(x, y * 1.05, value, ha='center', va='bottom')
    plt.xticks(ticks=data.dropna(subset=['YEAR_MONTH'])['INDEX'], labels=data.dropna(subset=['YEAR_MONTH'])['YEAR_MONTH'], rotation=90)
    ax1.set_xlabel('')
    ax1.set_ylabel('股价（元）')
    ax2.set_ylabel('占净值比（%）')
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
    plt.tight_layout()
    plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/{1}.png'.format(fund_code, stock_name))
    # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/{0}_{1}.png'.format(fund_name, stock_name))
    return

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
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df

class HoldingCompare:
    def __init__(self, target_fund_code, compare_fund_code_list, sw_type=1, begin_date=None):
        self.target_fund_code = target_fund_code
        self.compare_fund_code_list = compare_fund_code_list
        self.sw_type = sw_type
        self.begin_date = begin_date
        self.load()

    def load(self):
        # 基金信息数据
        self.all_fund = HBDB().read_fund_info()
        self.all_fund = self.all_fund.rename(columns={'jjdm': 'FUND_CODE', 'jjjc': 'FUND_NAME'})
        self.all_fund = self.all_fund[self.all_fund['FUND_CODE'].isin([self.target_fund_code] + self.compare_fund_code_list)]
        self.all_fund = self.all_fund[['FUND_CODE', 'FUND_NAME']].drop_duplicates('FUND_CODE', keep='last')
        # 行业信息数据
        self.industry_info = HBDB().read_industry_info()
        self.industry_info = self.industry_info.rename(columns={'flmc': 'INDUSTRY_NAME', 'zsdm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
        self.industry_info = self.industry_info.dropna(subset=['BEGIN_DATE'])
        self.industry_info['END_DATE'] = self.industry_info['END_DATE'].replace('', np.nan).fillna('20990101')
        self.industry_info['BEGIN_DATE'] = self.industry_info['BEGIN_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
        self.industry_info['END_DATE'] = self.industry_info['END_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
        self.industry_info['BEGIN_DATE'] = self.industry_info['BEGIN_DATE'].astype(int).astype(str)
        self.industry_info['END_DATE'] = self.industry_info['END_DATE'].astype(int).astype(str)
        self.industry_info['INDUSTRY_VERSION'] = self.industry_info['INDUSTRY_VERSION'].astype(int)
        self.industry_info['INDUSTRY_TYPE'] = self.industry_info['INDUSTRY_TYPE'].astype(int)
        self.industry_info['IS_NEW'] = self.industry_info['IS_NEW'].astype(int)
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_VERSION'] == 3]
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        # 个股行业对应数据
        self.stock_industry = HBDB().read_stock_industry()
        self.stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_industry.hdf', key='table', mode='w')
        # self.stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_industry.hdf', key='table')
        self.stock_industry = self.stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW', 'credt_etl': 'CREDT_ETL'})
        self.stock_industry['INDUSTRY_VERSION'] = self.stock_industry['INDUSTRY_VERSION'].astype(int)
        self.stock_industry['INDUSTRY_TYPE'] = self.stock_industry['INDUSTRY_TYPE'].astype(int)
        self.stock_industry['IS_NEW'] = self.stock_industry['IS_NEW'].astype(int)
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.sort_values(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL', 'CREDT_ETL']).drop_duplicates(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL'], keep='last')
        self.stock_industry_sw = self.stock_industry[self.stock_industry['INDUSTRY_VERSION'] == 2]
        # 个股持仓数据
        self.all_fund_holding = HBDB().read_fund_holding_given_codes([self.target_fund_code] + self.compare_fund_code_list)
        self.all_fund_holding = self.all_fund_holding.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ccsz': 'HOLDING_MARKET_VALUE', 'ccsl': 'HOLDING_AMOUNT', 'zjbl': 'MV_IN_NA'})
        self.all_fund_holding = self.all_fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False])
        self.all_fund_holding['REPORT_DATE'] = self.all_fund_holding['REPORT_DATE'].astype(str)
        self.all_fund_holding = self.all_fund_holding[self.all_fund_holding['MV_IN_NA'] != 0.0]
        # 基金季报前十大最小权重
        self.all_fund_holding_season = self.all_fund_holding.copy(deep=True)
        self.all_fund_holding_season['MONTH'] = self.all_fund_holding_season['REPORT_DATE'].apply(lambda x: x[4:6])
        self.all_fund_holding_season = self.all_fund_holding_season[self.all_fund_holding_season['MONTH'].isin(['03', '09'])]
        self.all_fund_holding_min = self.all_fund_holding_season[['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA']].groupby(['FUND_CODE', 'REPORT_DATE']).min().reset_index().rename(columns={'MV_IN_NA': 'MV_IN_NA_MIN'})
        self.all_fund_holding_min['MV_IN_NA_MIN'] = self.all_fund_holding_min['MV_IN_NA_MIN'].apply(lambda x: '<{0}'.format(round(x, 2)))
        # 行业持仓数据
        self.all_fund_industry_holding = self.all_fund_holding.merge(self.stock_industry_sw[self.stock_industry_sw['INDUSTRY_TYPE'] == self.sw_type][['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
        self.all_fund_industry_holding = self.all_fund_industry_holding.dropna(subset=['FUND_CODE', 'REPORT_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MV_IN_NA'])
        self.all_fund_industry_holding = self.all_fund_industry_holding[['FUND_CODE', 'REPORT_DATE', 'INDUSTRY_NAME', 'MV_IN_NA']].groupby(['FUND_CODE', 'REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        # 日历数据
        self.all_calendar_df, self.all_report_df, self.all_trade_df, self.all_report_trade_df, self.all_calendar_trade_df = get_date('19900101',datetime.today().strftime('%Y%m%d'))
        # 个股行情数据
        stock_daily_k_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_daily_k.hdf'
        if os.path.isfile(stock_daily_k_path):
            existed_stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
            max_date = max(existed_stock_daily_k['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_daily_k = pd.DataFrame()
            start_date = '20150101'
        trade_df = self.all_trade_df[(self.all_trade_df['TRADE_DATE'] > start_date) & (self.all_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        data = []
        for idx, td in enumerate(trade_df['TRADE_DATE'].unique().tolist()):
            stock_daily_k_date = HBDB().read_stock_daily_k_given_date(td)
            star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(td)
            stock_daily_k_date = pd.concat([stock_daily_k_date, star_stock_daily_k_date])
            data.append(stock_daily_k_date)
            print('[PreloadStockDailyK][{0}/{1}]'.format(idx, len(trade_df['TRADE_DATE'])))
        self.all_stock_daily_k = pd.concat([existed_stock_daily_k] + data, ignore_index=True)
        self.all_stock_daily_k = self.all_stock_daily_k.sort_values(['TRADE_DATE', 'TICKER_SYMBOL']).drop_duplicates(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.all_stock_daily_k.to_hdf(stock_daily_k_path, key='table', mode='w')
        # self.all_stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_daily_k.hdf', key='table')
        # 个股名称对应数据
        self.all_stock_name = self.all_stock_daily_k.sort_values(['TICKER_SYMBOL', 'TRADE_DATE'])[['TICKER_SYMBOL', 'SEC_SHORT_NAME']].drop_duplicates('TICKER_SYMBOL', keep='last')
        # 个股估值数据
        stock_valuation_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_valuation.hdf'
        if os.path.isfile(stock_valuation_path):
            existed_stock_valuation = pd.read_hdf(stock_valuation_path, key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = '20150101'
        trade_df = self.all_trade_df[(self.all_trade_df['TRADE_DATE'] > start_date) & (self.all_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        data = []
        for idx, td in enumerate(trade_df['TRADE_DATE'].unique().tolist()):
            stock_valuation_date = HBDB().read_stock_valuation_given_date(td)
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(td)
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            data.append(stock_valuation_date)
            print('[PreloadStockValuation][{0}/{1}]'.format(idx, len(trade_df['TRADE_DATE'])))
        self.all_stock_valuation = pd.concat([existed_stock_valuation] + data, ignore_index=True)
        self.all_stock_valuation = self.all_stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL']).drop_duplicates(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.all_stock_valuation.to_hdf(stock_valuation_path, key='table', mode='w')
        # self.all_stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_valuation.hdf', key='table')
        # 个股财务数据
        stock_finance_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_finance.hdf'
        if os.path.isfile(stock_finance_path):
            existed_stock_finance = pd.read_hdf(stock_finance_path, key='table')
            max_date = max(existed_stock_finance['END_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_finance = pd.DataFrame()
            start_date = '20150101'
        report_df = self.all_report_df[(self.all_report_df['REPORT_DATE'] > start_date) & (self.all_report_df['REPORT_DATE'] < datetime.today().strftime('%Y%m%d'))]
        data = []
        for idx, td in enumerate(report_df['REPORT_DATE'].unique().tolist()):
            stock_finance_date = HBDB().read_stock_finance_given_date(td)
            star_stock_finance_date = HBDB().read_star_stock_finance_given_date(td)
            stock_finance_date = pd.concat([stock_finance_date, star_stock_finance_date])
            data.append(stock_finance_date)
            print('[PreloadFinance][{0}/{1}]'.format(idx, len(report_df['REPORT_DATE'])))
        self.all_stock_finance = pd.concat([existed_stock_finance] + data, ignore_index=True)
        self.all_stock_finance = self.all_stock_finance.loc[self.all_stock_finance['TICKER_SYMBOL'].str.len() == 6]
        self.all_stock_finance = self.all_stock_finance.loc[self.all_stock_finance['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.all_stock_finance.to_hdf(stock_finance_path, key='table', mode='w')
        # self.all_stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/stock_finance.hdf', key='table')
        # 行业行情数据
        self.all_industry_daily_k = HBDB().read_index_daily_k_given_date_and_indexs('20150101', self.industry_info['INDUSTRY_ID'].unique().tolist())
        self.all_industry_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/all_industry_daily_k.hdf', key='table', mode='w')
        # self.all_industry_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/all_industry_daily_k.hdf', key='table')
        self.all_industry_daily_k = self.all_industry_daily_k.rename(columns={'zqdm': 'INDUSTRY_ID', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        self.all_industry_daily_k['TRADE_DATE'] = self.all_industry_daily_k['TRADE_DATE'].astype(str)
        self.all_industry_daily_k = self.all_industry_daily_k.sort_values(['TRADE_DATE', 'INDUSTRY_ID'])
        self.all_industry_daily_k['INDUSTRY_NAME'] = self.all_industry_daily_k['INDUSTRY_ID'].apply(lambda x: self.industry_id_name_dic[x])
        # 行业估值数据
        self.all_industry_valuation = FEDB().read_industry_valuation(self.sw_type)
        # 行业财务数据
        self.all_industry_finance = FEDB().read_industry_fundamental(self.sw_type)

    def get_stock_holding_compare(self, worksheet_h, worksheet_hc):
        target_start_date = self.all_fund_holding[self.all_fund_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
        all_fund_holding_cut = self.all_fund_holding[self.all_fund_holding['REPORT_DATE'] >= target_start_date]
        fund_holding_list = []
        for fund_code in [self.target_fund_code] + self.compare_fund_code_list:
            # 个股仓位情况
            fund_holding = all_fund_holding_cut[all_fund_holding_cut['FUND_CODE'] == fund_code]
            fund_holding = fund_holding.pivot(index='TICKER_SYMBOL', columns='REPORT_DATE', values='MV_IN_NA')
            fund_holding_date_columns = sorted(list(fund_holding.columns))
            rank_list = list(fund_holding[fund_holding_date_columns[-1]].sort_values(ascending=False).index)
            fund_holding = fund_holding.reset_index()
            fund_holding['TICKER_SYMBOL'] = fund_holding['TICKER_SYMBOL'].astype('category')
            fund_holding['TICKER_SYMBOL'].cat.reorder_categories(rank_list, inplace=True)
            fund_holding = fund_holding.sort_values('TICKER_SYMBOL')
            fund_holding = fund_holding.merge(self.all_stock_name[['TICKER_SYMBOL', 'SEC_SHORT_NAME']], on=['TICKER_SYMBOL'], how='left')
            fund_holding = fund_holding.merge(self.stock_industry_sw[self.stock_industry_sw['INDUSTRY_TYPE'] == 1][['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW1'}), on=['TICKER_SYMBOL'], how='left')
            fund_holding = fund_holding.merge(self.stock_industry_sw[self.stock_industry_sw['INDUSTRY_TYPE'] == 2][['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW2'}), on=['TICKER_SYMBOL'], how='left')
            fund_holding = fund_holding.merge(self.stock_industry_sw[self.stock_industry_sw['INDUSTRY_TYPE'] == 3][['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW3'}), on=['TICKER_SYMBOL'], how='left')
            fund_name = self.all_fund[self.all_fund['FUND_CODE'] == fund_code]['FUND_NAME'].values[0]
            fund_holding['FUND_NAME'] = fund_name
            fund_holding = fund_holding[['FUND_NAME', 'INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW2', 'INDUSTRY_NAME_SW3', 'TICKER_SYMBOL', 'SEC_SHORT_NAME'] + fund_holding_date_columns]
            fund_holding.columns = ['基金名称', '申万一级行业', '申万二级行业', '申万三级行业', '股票代码', '股票名称'] + fund_holding_date_columns
            fund_holding.loc[fund_holding.shape[0]] = [np.nan] * fund_holding.shape[1]
            fund_holding_list.append(fund_holding)

            if fund_code == self.target_fund_code:
                target_start_date = self.all_fund_holding[self.all_fund_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
                target_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == self.target_fund_code]['FUND_NAME'].values[0]
                for idx, stock in enumerate(fund_holding[['股票代码', fund_holding_date_columns[-1]]].dropna()['股票代码'].unique().tolist()[:10]):
                    # 个股仓位变动图
                    stock_daily_k = self.all_stock_daily_k[self.all_stock_daily_k['TICKER_SYMBOL'] == stock]
                    stock_daily_k['TRADE_DATE'] = stock_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    stock_daily_k = stock_daily_k.sort_values('TRADE_DATE')
                    stock_name = stock_daily_k['SEC_SHORT_NAME'].values[0]
                    stock_valuation = self.all_stock_valuation[self.all_stock_valuation['TICKER_SYMBOL'] == stock]
                    stock_valuation['TRADE_DATE'] = stock_valuation['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    stock_valuation = stock_valuation.sort_values('TRADE_DATE')
                    stock_finance = self.all_stock_finance[self.all_stock_finance['TICKER_SYMBOL'] == stock]
                    stock_finance = stock_finance.sort_values(['END_DATE', 'PUBLISH_DATE']).drop_duplicates(['END_DATE'], keep='last')
                    stock_finance = stock_finance.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='left')
                    stock_finance['TRADE_DATE'] = stock_finance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    stock_finance = stock_finance.sort_values('TRADE_DATE')
                    stock_holding_disp = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_holding['TICKER_SYMBOL'] == stock)]
                    stock_holding_disp = stock_holding_disp[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE')
                    stock_holding_disp['MV_IN_NA'] = stock_holding_disp['MV_IN_NA'].apply(lambda x: round(x, 2))
                    stock_holding_disp.columns = [target_fund_name]
                    disp_start_date = target_start_date if self.begin_date is None else self.begin_date
                    disp_dates = self.all_report_df[self.all_report_df['REPORT_DATE'] >= disp_start_date]['REPORT_DATE'].unique().tolist()
                    stock_holding_disp = stock_holding_disp.reindex(disp_dates)
                    stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding_disp[target_fund_name].isnull()), target_fund_name] = 0.00
                    stock_holding_disp = pd.concat([stock_holding_disp, self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == self.target_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
                    stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[target_fund_name].isnull()), target_fund_name] = stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[target_fund_name].isnull()), 'MV_IN_NA_MIN']
                    stock_holding_disp = stock_holding_disp.drop('MV_IN_NA_MIN', axis=1)
                    stock_holding_disp.loc[stock_holding_disp.index < target_start_date, target_fund_name] = '--'
                    stock_holding_disp[target_fund_name] = stock_holding_disp[target_fund_name].astype(str)
                    stock_holding_disp = stock_holding_disp.reset_index()
                    stock_holding_disp = stock_holding_disp.merge(self.all_calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                    stock_holding_disp['TRADE_DATE'] = stock_holding_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    stock_holding_disp = stock_holding_disp.sort_values('TRADE_DATE')
                    stock_holding_disp_quancang = stock_holding_disp.loc[stock_holding_disp['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
                    stock_holding_disp_quancang[target_fund_name] = stock_holding_disp_quancang[target_fund_name].replace('--', np.nan)
                    stock_holding_disp_quancang[target_fund_name] = stock_holding_disp_quancang[target_fund_name].astype(float)
                    stock_holding_disp_quancang = stock_holding_disp_quancang.rename(columns={target_fund_name: target_fund_name + '（全仓）'})
                    all_report_trade_df = self.all_report_trade_df[['TRADE_DATE']]
                    all_report_trade_df['TRADE_DATE'] = all_report_trade_df['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    all_report_trade_df['IS_QUARTER_END'] = 1
                    data = stock_daily_k[stock_daily_k['TRADE_DATE'] >= datetime.strptime(disp_start_date, '%Y%m%d') - timedelta(30)][['TRADE_DATE', 'CLOSE_PRICE']]
                    data = data.merge(stock_valuation[['TRADE_DATE', 'PE_TTM']], on=['TRADE_DATE'], how='left')
                    data = data.merge(stock_finance[['TRADE_DATE', 'ROE_TTM']], on=['TRADE_DATE'], how='left')
                    data = data.merge(stock_holding_disp[['TRADE_DATE', target_fund_name]], on=['TRADE_DATE'], how='left')
                    data = data.merge(stock_holding_disp_quancang[['TRADE_DATE', target_fund_name + '（全仓）']], on=['TRADE_DATE'], how='left')
                    data = data.merge(all_report_trade_df[['TRADE_DATE', 'IS_QUARTER_END']], on=['TRADE_DATE'], how='left')
                    data['INDEX'] = range(len(data))
                    data['TRADE_DATE_DISP'] = data['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
                    fig, ax = plt.subplots(2, 1, figsize=(25, 10))
                    bar_width = len(data) / len(data.dropna(subset=[target_fund_name])) / 10.0
                    ax0_right = ax[0].twinx()
                    ax[0].plot(data['INDEX'], data['CLOSE_PRICE'], color='#AFDEFA', label='{0}（元）'.format(stock_name))
                    ax0_right.bar(data['INDEX'], data[target_fund_name + '（全仓）'], width=bar_width, color='#C94649', label='占净值比（%）')
                    ax0_right.set_ylim([0, 50])
                    ax[0].scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_PRICE'], marker='.', color='#F04950', label='{0}中该个股持仓占净值比（%）'.format(target_fund_name))
                    for x, y, value in zip(list(data.dropna(subset=[target_fund_name])['INDEX']), list(data.dropna(subset=[target_fund_name])['CLOSE_PRICE']), list(data.dropna(subset=[target_fund_name])[target_fund_name])):
                        ax[0].text(x, y * 1.1, value, ha='center', va='bottom', color='#F04950')
                    ax[0].scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_PRICE'], marker='.', color='#959595')
                    plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                    ax[0].set_xlabel('')
                    ax[0].set_ylabel('')
                    ax0_right.set_ylabel('')
                    ax[0].legend(loc=2)
                    ax0_right.legend(loc=1)
                    ax0_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                    ax1_right = ax[1].twinx()
                    ax[1].bar([i - bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['PE_TTM']), width=bar_width, color='#C94649', label='PE_TTM')
                    ax1_right.bar([i + bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['ROE_TTM']), width=bar_width, color='#8588B7', label='ROE_TTM')
                    plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                    ax[1].set_xlabel('')
                    ax[1].set_ylabel('')
                    ax1_right.set_ylabel('')
                    ax[1].legend(loc=2)
                    ax1_right.legend(loc=1)
                    ax1_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                    plt.tight_layout()
                    plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding/{1}_{2}.png'.format(self.target_fund_code, stock_name, target_fund_name))
                    worksheet_h.insert_image('A{0}'.format(idx + 1), 'D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding/{1}_{2}.png'.format(self.target_fund_code, stock_name, target_fund_name), {'x_scale': 0.05, 'y_scale': 0.05})
                    ########################################
                    hypre_link = r'=HYPERLINK("#' + '个股仓位变动图' + '!' + 'A{0}'.format(idx + 1) + '\",\"' + fund_holding.iloc[idx, 5] + '")'
                    fund_holding.iloc[idx, 5] = hypre_link

        fund_holding = pd.concat(fund_holding_list)
        fund_holding.loc[:, fund_holding.shape[1]] = [np.nan] * fund_holding.shape[0]
        fund_holding = fund_holding.rename(columns={list(fund_holding.columns)[-1]: ''})
        fund_holding = fund_holding.reset_index().drop('index', axis=1)

        target_start_date = self.all_fund_holding[self.all_fund_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
        target_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == self.target_fund_code]['FUND_NAME'].values[0]
        target_fund_stocks = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_holding['REPORT_DATE'].isin(sorted(self.all_fund_holding['REPORT_DATE'].unique().tolist())[-12:])) & (self.all_fund_holding['MV_IN_NA'] >= 4.0)]['TICKER_SYMBOL'].unique().tolist()
        same_stocks_list = []
        stock_holding_list = []
        for j, compare_fund_code in enumerate(self.compare_fund_code_list):
            compare_fund_stocks = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == compare_fund_code) & (self.all_fund_holding['REPORT_DATE'].isin(sorted(self.all_fund_holding['REPORT_DATE'].unique().tolist())[-12:])) & (self.all_fund_holding['MV_IN_NA'] >= 4.0)][['TICKER_SYMBOL']].drop_duplicates()
            compare_fund_stocks = compare_fund_stocks[compare_fund_stocks['TICKER_SYMBOL'].isin(target_fund_stocks)]
            compare_fund_stocks = compare_fund_stocks.merge(self.all_stock_name[['TICKER_SYMBOL', 'SEC_SHORT_NAME']], on=['TICKER_SYMBOL'], how='left')
            compare_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == compare_fund_code]['FUND_NAME'].values[0]
            compare_fund_stocks['FUND_NAME'] = compare_fund_name
            compare_fund_stocks = compare_fund_stocks[['FUND_NAME', 'TICKER_SYMBOL', 'SEC_SHORT_NAME']]
            compare_fund_stocks.columns = ['基金名称', '与{0}同持仓股票代码'.format(target_fund_name), '与{0}同持仓股票名称'.format(target_fund_name)]
            compare_fund_stocks = compare_fund_stocks.reset_index().drop('index', axis=1)
            same_stocks_list.append(compare_fund_stocks)

            compare_start_date = self.all_fund_holding[self.all_fund_holding['FUND_CODE'] == compare_fund_code]['REPORT_DATE'].min()
            compare_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == compare_fund_code]['FUND_NAME'].values[0]
            disp_start_date = min(target_start_date, compare_start_date) if self.begin_date is None else self.begin_date
            disp_dates = self.all_report_df[self.all_report_df['REPORT_DATE'] >= disp_start_date]['REPORT_DATE'].unique().tolist()
            for i, stock in enumerate(compare_fund_stocks['与{0}同持仓股票代码'.format(target_fund_name)].unique().tolist()):
                target_holding = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_holding['TICKER_SYMBOL'] == stock)]
                target_holding = target_holding[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE').rename(columns={'MV_IN_NA': target_fund_name})
                target_holding[target_fund_name] = target_holding[target_fund_name].apply(lambda x: round(x, 2))
                compare_holding = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == compare_fund_code) & (self.all_fund_holding['TICKER_SYMBOL'] == stock)]
                compare_holding = compare_holding[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE').rename(columns={'MV_IN_NA': compare_fund_name})
                compare_holding[compare_fund_name] = compare_holding[compare_fund_name].apply(lambda x: round(x, 2))
                stock_holding = target_holding.merge(compare_holding, left_index=True, right_index=True, how='outer')
                stock_holding = stock_holding.reindex(disp_dates)

                ########################################
                # 个股仓位变动比较图
                stock_daily_k = self.all_stock_daily_k[self.all_stock_daily_k['TICKER_SYMBOL'] == stock]
                stock_daily_k['TRADE_DATE'] = stock_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                stock_daily_k = stock_daily_k.sort_values('TRADE_DATE')
                stock_name = stock_daily_k['SEC_SHORT_NAME'].values[0]
                stock_valuation = self.all_stock_valuation[self.all_stock_valuation['TICKER_SYMBOL'] == stock]
                stock_valuation['TRADE_DATE'] = stock_valuation['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                stock_valuation = stock_valuation.sort_values('TRADE_DATE')
                stock_finance = self.all_stock_finance[self.all_stock_finance['TICKER_SYMBOL'] == stock]
                stock_finance = stock_finance.sort_values(['END_DATE', 'PUBLISH_DATE']).drop_duplicates(['END_DATE'], keep='last')
                stock_finance = stock_finance.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='left')
                stock_finance['TRADE_DATE'] = stock_finance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                stock_finance = stock_finance.sort_values('TRADE_DATE')
                stock_holding_disp = stock_holding.copy(deep=True)
                stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding_disp[target_fund_name].isnull()), target_fund_name] = 0.00
                stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding_disp[compare_fund_name].isnull()), compare_fund_name] = 0.00
                stock_holding_disp = pd.concat([stock_holding_disp, self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == self.target_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
                stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[target_fund_name].isnull()), target_fund_name] = stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[target_fund_name].isnull()), 'MV_IN_NA_MIN']
                stock_holding_disp = stock_holding_disp.drop('MV_IN_NA_MIN', axis=1)
                stock_holding_disp = pd.concat([stock_holding_disp, self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == compare_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
                stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[compare_fund_name].isnull()), compare_fund_name] = stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[compare_fund_name].isnull()), 'MV_IN_NA_MIN']
                stock_holding_disp = stock_holding_disp.drop('MV_IN_NA_MIN', axis=1)
                stock_holding_disp.loc[stock_holding_disp.index < target_start_date, target_fund_name] = '--'
                stock_holding_disp.loc[stock_holding_disp.index < compare_start_date, compare_fund_name] = '--'
                stock_holding_disp[target_fund_name] = stock_holding_disp[target_fund_name].astype(str)
                stock_holding_disp[compare_fund_name] = stock_holding_disp[compare_fund_name].astype(str)
                stock_holding_disp = stock_holding_disp.reset_index()
                stock_holding_disp = stock_holding_disp.merge(self.all_calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                stock_holding_disp['TRADE_DATE'] = stock_holding_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                stock_holding_disp = stock_holding_disp.sort_values('TRADE_DATE')
                stock_holding_disp_quancang = stock_holding_disp.loc[stock_holding_disp['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
                stock_holding_disp_quancang[target_fund_name] = stock_holding_disp_quancang[target_fund_name].replace('--', np.nan)
                stock_holding_disp_quancang[compare_fund_name] = stock_holding_disp_quancang[compare_fund_name].replace('--', np.nan)
                stock_holding_disp_quancang[target_fund_name] = stock_holding_disp_quancang[target_fund_name].astype(float)
                stock_holding_disp_quancang[compare_fund_name] = stock_holding_disp_quancang[compare_fund_name].astype(float)
                stock_holding_disp_quancang = stock_holding_disp_quancang.rename(columns={target_fund_name: target_fund_name + '（全仓）', compare_fund_name: compare_fund_name + '（全仓）'})
                all_report_trade_df = self.all_report_trade_df[['TRADE_DATE']]
                all_report_trade_df['TRADE_DATE'] = all_report_trade_df['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                all_report_trade_df['IS_QUARTER_END'] = 1
                data = stock_daily_k[stock_daily_k['TRADE_DATE'] >= datetime.strptime(disp_start_date, '%Y%m%d') - timedelta(30)][['TRADE_DATE', 'CLOSE_PRICE']]
                data = data.merge(stock_valuation[['TRADE_DATE', 'PE_TTM']], on=['TRADE_DATE'], how='left')
                data = data.merge(stock_finance[['TRADE_DATE', 'ROE_TTM']], on=['TRADE_DATE'], how='left')
                data = data.merge(stock_holding_disp[['TRADE_DATE', target_fund_name, compare_fund_name]], on=['TRADE_DATE'], how='left')
                data = data.merge(stock_holding_disp_quancang[['TRADE_DATE', target_fund_name + '（全仓）', compare_fund_name + '（全仓）']], on=['TRADE_DATE'], how='left')
                data = data.merge(all_report_trade_df[['TRADE_DATE', 'IS_QUARTER_END']], on=['TRADE_DATE'], how='left')
                data['INDEX'] = range(len(data))
                data['TRADE_DATE_DISP'] = data['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
                fig, ax = plt.subplots(2, 1, figsize=(25, 10))
                bar_width = len(data) / len(data.dropna(subset=[target_fund_name])) / 10.0
                ax0_right = ax[0].twinx()
                ax[0].plot(data['INDEX'], data['CLOSE_PRICE'], color='#AFDEFA', label='{0}（元）'.format(stock_name))
                ax0_right.bar([i - bar_width / 2.0 for i in data['INDEX']], data[target_fund_name + '（全仓）'], width=bar_width, color='#C94649')
                ax0_right.bar([i + bar_width / 2.0 for i in data['INDEX']], data[compare_fund_name + '（全仓）'], width=bar_width, color='#8588B7')
                ax0_right.set_ylim([0, 50])
                ax[0].scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_PRICE'], marker='.', color='#F04950', label='{0}中该个股持仓占净值比（%）'.format(target_fund_name))
                ax[0].scatter(data.dropna(subset=[compare_fund_name])['INDEX'], data.dropna(subset=[compare_fund_name])['CLOSE_PRICE'], marker='.', color='#6268A2', label='{0}中该个股持仓占净值比（%）'.format(compare_fund_name))
                for x, y, value in zip(list(data.dropna(subset=[target_fund_name])['INDEX']), list(data.dropna(subset=[target_fund_name])['CLOSE_PRICE']), list(data.dropna(subset=[target_fund_name])[target_fund_name])):
                    ax[0].text(x, y * 1.1, value, ha='center', va='bottom', color='#F04950')
                for x, y, value in zip(list(data.dropna(subset=[compare_fund_name])['INDEX']), list(data.dropna(subset=[compare_fund_name])['CLOSE_PRICE']), list(data.dropna(subset=[compare_fund_name])[compare_fund_name])):
                    ax[0].text(x, y * 0.9, value, ha='center', va='bottom', color='#6268A2')
                ax[0].scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_PRICE'], marker='.', color='#959595')
                ax[0].scatter(data.dropna(subset=[compare_fund_name])['INDEX'], data.dropna(subset=[compare_fund_name])['CLOSE_PRICE'], marker='.', color='#959595')
                plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'],  labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                ax[0].set_xlabel('')
                ax[0].set_ylabel('')
                ax0_right.set_ylabel('占净值比（%）')
                ax[0].legend(loc=2)
                ax0_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                ax1_right = ax[1].twinx()
                ax[1].bar([i - bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['PE_TTM']), width=bar_width, color='#C94649', label='PE_TTM')
                ax1_right.bar([i + bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['ROE_TTM']), width=bar_width, color='#8588B7', label='ROE_TTM')
                plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'],  labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                ax[1].set_xlabel('')
                ax[1].set_ylabel('')
                ax1_right.set_ylabel('')
                ax[1].legend(loc=2)
                ax1_right.legend(loc=1)
                ax1_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                plt.tight_layout()
                plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding_compare/{1}_{2}_{3}.png'.format(self.target_fund_code, stock_name, target_fund_name, compare_fund_name))
                worksheet_hc.insert_image('{0}{1}'.format(cell_dic[j + 1], i + 1), 'D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding_compare/{1}_{2}_{3}.png'.format(self.target_fund_code, stock_name, target_fund_name, compare_fund_name), {'x_scale': 0.05, 'y_scale': 0.05})
                ########################################

                stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding[target_fund_name].isnull()), target_fund_name] = 0.00
                stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding[compare_fund_name].isnull()), compare_fund_name] = 0.00
                stock_holding = pd.concat([stock_holding, self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == self.target_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
                stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding[target_fund_name].isnull()), target_fund_name] = stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding[target_fund_name].isnull()), 'MV_IN_NA_MIN']
                stock_holding = stock_holding.drop('MV_IN_NA_MIN', axis=1)
                stock_holding = pd.concat([stock_holding, self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == compare_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE')], axis=1)
                stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding[compare_fund_name].isnull()), compare_fund_name] = stock_holding.loc[(stock_holding.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding[compare_fund_name].isnull()), 'MV_IN_NA_MIN']
                stock_holding = stock_holding.drop('MV_IN_NA_MIN', axis=1)
                stock_holding.loc[stock_holding.index < target_start_date, target_fund_name] = '--'
                stock_holding.loc[stock_holding.index < compare_start_date, compare_fund_name] = '--'
                stock_holding = stock_holding.sort_index().T.reset_index().rename(columns={'index': '基金名称'})
                stock_holding_columns = list(stock_holding.columns)
                stock_holding['TICKER_SYMBOL'] = stock
                stock_holding = stock_holding.merge(self.all_stock_name[['TICKER_SYMBOL', 'SEC_SHORT_NAME']], on=['TICKER_SYMBOL'], how='left')
                stock_holding = stock_holding[['SEC_SHORT_NAME'] + stock_holding_columns]
                stock_holding.columns = ['股票名称'] + stock_holding_columns
                stock_holding['个股仓位变动比较图'] = ''
                stock_holding.loc[stock_holding.shape[0]] = [np.nan] * stock_holding.shape[1]
                stock_holding = stock_holding.T.reset_index().T
                hypre_link = r'=HYPERLINK("#' + '个股仓位变动比较图' + '!' + '{0}{1}'.format(cell_dic[j + 1], i + 1) + '\",\"' + '个股仓位变动比较图' + '")'
                stock_holding.iloc[0, -1] = hypre_link
                stock_holding_list.append(stock_holding)

        if len(self.compare_fund_code_list) > 0:
            same_stocks = pd.concat(same_stocks_list, axis=1)
            same_stocks.loc[:, same_stocks.shape[1]] = [np.nan] * same_stocks.shape[0]
            same_stocks = same_stocks.rename(columns={list(same_stocks.columns)[-1]: ''})
            same_stocks = same_stocks.reset_index().drop('index', axis=1)
            stock_holding = pd.concat(stock_holding_list)
            stock_holding.columns = [''] * stock_holding.shape[1]
            stock_holding = stock_holding.reset_index().drop('index', axis=1)
            stock_holding_compare = pd.concat([fund_holding, same_stocks, stock_holding], axis=1)
        else:
            stock_holding_compare = pd.concat([fund_holding], axis=1)
        return stock_holding_compare

    def get_industry_holding_compare(self, worksheet_h, worksheet_hc):
        target_start_date = self.all_fund_industry_holding[self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
        all_fund_industry_holding_cut = self.all_fund_industry_holding[self.all_fund_industry_holding['REPORT_DATE'] >= target_start_date]
        fund_industry_holding_list = []
        for fund_code in [self.target_fund_code] + self.compare_fund_code_list:
            # 行业仓位情况
            fund_industry_holding = all_fund_industry_holding_cut[all_fund_industry_holding_cut['FUND_CODE'] == fund_code]
            fund_industry_holding = fund_industry_holding.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values='MV_IN_NA')
            fund_industry_holding_date_columns = sorted(list(fund_industry_holding.columns))
            industry_rank_list = list(fund_industry_holding[fund_industry_holding_date_columns[-1]].sort_values(ascending=False).index)
            fund_industry_holding = fund_industry_holding.reset_index()
            fund_industry_holding['INDUSTRY_NAME'] = fund_industry_holding['INDUSTRY_NAME'].astype('category')
            fund_industry_holding['INDUSTRY_NAME'].cat.reorder_categories(industry_rank_list, inplace=True)
            fund_industry_holding = fund_industry_holding.sort_values('INDUSTRY_NAME')
            fund_name = self.all_fund[self.all_fund['FUND_CODE'] == fund_code]['FUND_NAME'].values[0]
            fund_industry_holding['FUND_NAME'] = fund_name
            fund_industry_holding = fund_industry_holding[['FUND_NAME', 'INDUSTRY_NAME'] + fund_industry_holding_date_columns]
            fund_industry_holding.columns = ['基金名称', '申万一级行业'] + fund_industry_holding_date_columns
            fund_industry_holding.loc[fund_industry_holding.shape[0]] = [np.nan] * fund_industry_holding.shape[1]
            fund_industry_holding_list.append(fund_industry_holding)

            if fund_code == self.target_fund_code:
                target_start_date = self.all_fund_industry_holding[self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
                target_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == self.target_fund_code]['FUND_NAME'].values[0]
                for idx, industry in enumerate(fund_industry_holding[['申万一级行业', fund_industry_holding_date_columns[-1]]].dropna()['申万一级行业'].unique().tolist()):
                    # 行业仓位变动图
                    industry_daily_k = self.all_industry_daily_k[self.all_industry_daily_k['INDUSTRY_NAME'] == industry]
                    industry_daily_k['TRADE_DATE'] = industry_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    industry_daily_k = industry_daily_k.sort_values('TRADE_DATE')
                    industry_valuation = self.all_industry_valuation[self.all_industry_valuation['INDUSTRY_NAME'] == industry]
                    industry_valuation = industry_valuation.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                    industry_valuation['TRADE_DATE'] = industry_valuation['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    industry_valuation = industry_valuation.sort_values('TRADE_DATE')
                    industry_finance = self.all_industry_finance[self.all_industry_finance['INDUSTRY_NAME'] == industry]
                    industry_finance = industry_finance.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                    industry_finance['TRADE_DATE'] = industry_finance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    industry_finance = industry_finance.sort_values('TRADE_DATE')
                    industry_holding_disp = self.all_fund_industry_holding[(self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_industry_holding['INDUSTRY_NAME'] == industry)]
                    industry_holding_disp = industry_holding_disp[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE')
                    industry_holding_disp['MV_IN_NA'] = industry_holding_disp['MV_IN_NA'].apply(lambda x: round(x, 2))
                    industry_holding_disp.columns = [target_fund_name]
                    disp_start_date = target_start_date if self.begin_date is None else self.begin_date
                    disp_dates = self.all_report_df[self.all_report_df['REPORT_DATE'] >= disp_start_date]['REPORT_DATE'].unique().tolist()
                    industry_holding_disp = industry_holding_disp.reindex(disp_dates)
                    industry_holding_disp[target_fund_name] = industry_holding_disp[target_fund_name].fillna(0.00)
                    industry_holding_disp.loc[ industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), target_fund_name] = industry_holding_disp.loc[industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), target_fund_name].apply(lambda x: '>={0}'.format(x))
                    industry_holding_disp.loc[industry_holding_disp.index < target_start_date, target_fund_name] = '--'
                    industry_holding_disp[target_fund_name] = industry_holding_disp[target_fund_name].astype(str)
                    industry_holding_disp = industry_holding_disp.reset_index()
                    industry_holding_disp = industry_holding_disp.merge(self.all_calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                    industry_holding_disp['TRADE_DATE'] = industry_holding_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    industry_holding_disp = industry_holding_disp.sort_values('TRADE_DATE')
                    industry_holding_disp_quancang = industry_holding_disp.loc[industry_holding_disp['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
                    industry_holding_disp_quancang[target_fund_name] = industry_holding_disp_quancang[target_fund_name].replace('--', np.nan)
                    industry_holding_disp_quancang[target_fund_name] = industry_holding_disp_quancang[target_fund_name].astype(float)
                    industry_holding_disp_quancang = industry_holding_disp_quancang.rename(columns={target_fund_name: target_fund_name + '（全仓）'})
                    all_report_trade_df = self.all_report_trade_df[['TRADE_DATE']]
                    all_report_trade_df['TRADE_DATE'] = all_report_trade_df['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                    all_report_trade_df['IS_QUARTER_END'] = 1
                    data = industry_daily_k[industry_daily_k['TRADE_DATE'] >= datetime.strptime(disp_start_date, '%Y%m%d') - timedelta(30)][['TRADE_DATE', 'CLOSE_INDEX']]
                    data = data.merge(industry_valuation[['TRADE_DATE', 'PE_TTM']], on=['TRADE_DATE'], how='left')
                    data = data.merge(industry_finance[['TRADE_DATE', 'ROE_TTM']], on=['TRADE_DATE'], how='left')
                    data = data.merge(industry_holding_disp[['TRADE_DATE', target_fund_name]], on=['TRADE_DATE'], how='left')
                    data = data.merge(industry_holding_disp_quancang[['TRADE_DATE', target_fund_name + '（全仓）']], on=['TRADE_DATE'], how='left')
                    data = data.merge(all_report_trade_df[['TRADE_DATE', 'IS_QUARTER_END']], on=['TRADE_DATE'], how='left')
                    data['INDEX'] = range(len(data))
                    data['TRADE_DATE_DISP'] = data['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
                    fig, ax = plt.subplots(figsize=(25, 10))
                    bar_width = len(data) / len(data.dropna(subset=[target_fund_name])) / 10.0
                    ax_right = ax.twinx()
                    ax.plot(data['INDEX'], data['CLOSE_INDEX'], color='#AFDEFA', label='{0}（元）'.format(industry))
                    ax_right.bar(data['INDEX'], data[target_fund_name + '（全仓）'], width=bar_width, color='#C94649', label='占净值比（%）')
                    ax_right.set_ylim([0, 50])
                    ax.scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_INDEX'], marker='.', color='#F04950', label='{0}中该行业持仓占净值比（%）'.format(target_fund_name))
                    for x, y, value in zip(list(data.dropna(subset=[target_fund_name])['INDEX']), list(data.dropna(subset=[target_fund_name])['CLOSE_INDEX']), list(data.dropna(subset=[target_fund_name])[target_fund_name])):
                        ax.text(x, y * 1.1, value, ha='center', va='bottom', color='#F04950')
                    ax.scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_INDEX'], marker='.', color='#959595')
                    plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                    ax.set_xlabel('')
                    ax.set_ylabel('')
                    ax_right.set_ylabel('')
                    ax_right.set_ylim([0, 100])
                    ax.legend(loc=2)
                    ax_right.legend(loc=1)
                    ax_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                    # ax1_right = ax[1].twinx()
                    # ax[1].bar([i - bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['PE_TTM']), width=bar_width, color='#C94649', label='PE_TTM')
                    # ax1_right.bar([i + bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['ROE_TTM']), width=bar_width, color='#8588B7', label='ROE_TTM')
                    # plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                    # ax[1].set_xlabel('')
                    # ax[1].set_ylabel('')
                    # ax1_right.set_ylabel('')
                    # ax[1].legend(loc=2)
                    # ax1_right.legend(loc=1)
                    # ax1_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                    plt.tight_layout()
                    plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding/{1}_{2}.png'.format(self.target_fund_code, industry, target_fund_name))
                    worksheet_h.insert_image('A{0}'.format(idx + 1), 'D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding/{1}_{2}.png'.format(self.target_fund_code, industry, target_fund_name), {'x_scale': 0.05, 'y_scale': 0.05})
                    ########################################
                    hypre_link = r'=HYPERLINK("#' + '行业仓位变动图' + '!' + 'A{0}'.format(idx + 1) + '\",\"' + fund_industry_holding.iloc[idx, 1] + '")'
                    fund_industry_holding.iloc[idx, 1] = hypre_link

        fund_industry_holding = pd.concat(fund_industry_holding_list)
        fund_industry_holding.loc[:, fund_industry_holding.shape[1]] = [np.nan] * fund_industry_holding.shape[0]
        fund_industry_holding = fund_industry_holding.rename(columns={list(fund_industry_holding.columns)[-1]: ''})
        fund_industry_holding = fund_industry_holding.reset_index().drop('index', axis=1)

        target_start_date = self.all_fund_industry_holding[self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code]['REPORT_DATE'].min()
        target_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == self.target_fund_code]['FUND_NAME'].values[0]
        target_fund_industry = self.all_fund_industry_holding[(self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_industry_holding['REPORT_DATE'].isin(sorted(self.all_fund_industry_holding['REPORT_DATE'].unique().tolist())[-12:])) & (self.all_fund_industry_holding['MV_IN_NA'] >= 10)]['INDUSTRY_NAME'].unique().tolist()
        same_industry_list = []
        industry_holding_list = []
        for j, compare_fund_code in enumerate(self.compare_fund_code_list):
            compare_fund_industry = self.all_fund_industry_holding[(self.all_fund_industry_holding['FUND_CODE'] == compare_fund_code) & (self.all_fund_industry_holding['REPORT_DATE'].isin(sorted(self.all_fund_industry_holding['REPORT_DATE'].unique().tolist())[-12:])) & (self.all_fund_industry_holding['MV_IN_NA'] >= 10)][['INDUSTRY_NAME']].drop_duplicates()
            compare_fund_industry = compare_fund_industry[compare_fund_industry['INDUSTRY_NAME'].isin(target_fund_industry)]
            compare_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == compare_fund_code]['FUND_NAME'].values[0]
            compare_fund_industry['FUND_NAME'] = compare_fund_name
            compare_fund_industry = compare_fund_industry[['FUND_NAME', 'INDUSTRY_NAME']]
            compare_fund_industry.columns = ['基金名称', '与{0}同持仓行业名称'.format(target_fund_name)]
            compare_fund_industry = compare_fund_industry.reset_index().drop('index', axis=1)
            same_industry_list.append(compare_fund_industry)

            compare_start_date = self.all_fund_industry_holding[self.all_fund_industry_holding['FUND_CODE'] == compare_fund_code]['REPORT_DATE'].min()
            compare_fund_name = self.all_fund[self.all_fund['FUND_CODE'] == compare_fund_code]['FUND_NAME'].values[0]
            disp_start_date = min(target_start_date, compare_start_date) if self.begin_date is None else self.begin_date
            disp_dates = self.all_report_df[self.all_report_df['REPORT_DATE'] >= disp_start_date]['REPORT_DATE'].unique().tolist()
            for i, industry in enumerate(compare_fund_industry['与{0}同持仓行业名称'.format(target_fund_name)].unique().tolist()):
                target_holding_industry = self.all_fund_industry_holding[(self.all_fund_industry_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_industry_holding['INDUSTRY_NAME'] == industry)]
                target_holding_industry = target_holding_industry[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE').rename(columns={'MV_IN_NA': target_fund_name})
                target_holding_industry[target_fund_name] = target_holding_industry[target_fund_name].apply(lambda x: round(x, 2))
                compare_holding_industry = self.all_fund_industry_holding[(self.all_fund_industry_holding['FUND_CODE'] == compare_fund_code) & (self.all_fund_industry_holding['INDUSTRY_NAME'] == industry)]
                compare_holding_industry = compare_holding_industry[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE').rename(columns={'MV_IN_NA': compare_fund_name})
                compare_holding_industry[compare_fund_name] = compare_holding_industry[compare_fund_name].apply(lambda x: round(x, 2))
                industry_holding = target_holding_industry.merge(compare_holding_industry, left_index=True, right_index=True, how='outer')
                industry_holding = industry_holding.reindex(disp_dates)

                ########################################
                # 行业仓位变动比较图
                industry_daily_k = self.all_industry_daily_k[self.all_industry_daily_k['INDUSTRY_NAME'] == industry]
                industry_daily_k['TRADE_DATE'] = industry_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                industry_daily_k = industry_daily_k.sort_values('TRADE_DATE')
                industry_valuation = self.all_industry_valuation[self.all_industry_valuation['INDUSTRY_NAME'] == industry]
                industry_valuation = industry_valuation.merge( self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                industry_valuation['TRADE_DATE'] = industry_valuation['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                industry_valuation = industry_valuation.sort_values('TRADE_DATE')
                industry_finance = self.all_industry_finance[self.all_industry_finance['INDUSTRY_NAME'] == industry]
                industry_finance = industry_finance.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                industry_finance['TRADE_DATE'] = industry_finance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                industry_finance = industry_finance.sort_values('TRADE_DATE')
                industry_holding_disp = industry_holding.copy(deep=True)
                industry_holding_disp[target_fund_name] = industry_holding_disp[target_fund_name].fillna(0.00)
                industry_holding_disp[compare_fund_name] = industry_holding_disp[compare_fund_name].fillna(0.00)
                industry_holding_disp.loc[industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), target_fund_name] = industry_holding_disp.loc[industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), target_fund_name].apply(lambda x: '>={0}'.format(x))
                industry_holding_disp.loc[industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), compare_fund_name] = industry_holding_disp.loc[industry_holding_disp.index.str.slice(4, 6).isin(['03', '09']), compare_fund_name].apply(lambda x: '>={0}'.format(x))
                industry_holding_disp.loc[industry_holding_disp.index < target_start_date, target_fund_name] = '--'
                industry_holding_disp.loc[industry_holding_disp.index < compare_start_date, compare_fund_name] = '--'
                industry_holding_disp[target_fund_name] = industry_holding_disp[target_fund_name].astype(str)
                industry_holding_disp[compare_fund_name] = industry_holding_disp[compare_fund_name].astype(str)
                industry_holding_disp = industry_holding_disp.reset_index()
                industry_holding_disp = industry_holding_disp.merge(self.all_calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                industry_holding_disp['TRADE_DATE'] = industry_holding_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                industry_holding_disp = industry_holding_disp.sort_values('TRADE_DATE')
                industry_holding_disp_quancang = industry_holding_disp.loc[industry_holding_disp['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
                industry_holding_disp_quancang[target_fund_name] = industry_holding_disp_quancang[target_fund_name].replace('--', np.nan)
                industry_holding_disp_quancang[compare_fund_name] = industry_holding_disp_quancang[compare_fund_name].replace('--', np.nan)
                industry_holding_disp_quancang[target_fund_name] = industry_holding_disp_quancang[target_fund_name].astype(float)
                industry_holding_disp_quancang[compare_fund_name] = industry_holding_disp_quancang[compare_fund_name].astype(float)
                industry_holding_disp_quancang = industry_holding_disp_quancang.rename(columns={target_fund_name: target_fund_name + '（全仓）', compare_fund_name: compare_fund_name + '（全仓）'})
                all_report_trade_df = self.all_report_trade_df[['TRADE_DATE']]
                all_report_trade_df['TRADE_DATE'] = all_report_trade_df['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
                all_report_trade_df['IS_QUARTER_END'] = 1
                data = industry_daily_k[industry_daily_k['TRADE_DATE'] >= datetime.strptime(disp_start_date, '%Y%m%d') - timedelta(30)][['TRADE_DATE', 'CLOSE_INDEX']]
                data = data.merge(industry_valuation[['TRADE_DATE', 'PE_TTM']], on=['TRADE_DATE'], how='left')
                data = data.merge(industry_finance[['TRADE_DATE', 'ROE_TTM']], on=['TRADE_DATE'], how='left')
                data = data.merge(industry_holding_disp[['TRADE_DATE', target_fund_name, compare_fund_name]], on=['TRADE_DATE'], how='left')
                data = data.merge(industry_holding_disp_quancang[['TRADE_DATE', target_fund_name + '（全仓）', compare_fund_name + '（全仓）']], on=['TRADE_DATE'], how='left')
                data = data.merge(all_report_trade_df[['TRADE_DATE', 'IS_QUARTER_END']], on=['TRADE_DATE'], how='left')
                data['INDEX'] = range(len(data))
                data['TRADE_DATE_DISP'] = data['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
                fig, ax = plt.subplots(1, 1, figsize=(25, 10))
                bar_width = len(data) / len(data.dropna(subset=[target_fund_name])) / 10.0
                ax_right = ax.twinx()
                ax.plot(data['INDEX'], data['CLOSE_INDEX'], color='#AFDEFA', label='{0}（元）'.format(industry))
                ax_right.bar([i - bar_width / 2.0 for i in data['INDEX']], data[target_fund_name + '（全仓）'], width=bar_width, color='#C94649')
                ax_right.bar([i + bar_width / 2.0 for i in data['INDEX']], data[compare_fund_name + '（全仓）'], width=bar_width, color='#8588B7')
                ax_right.set_ylim([0, 50])
                ax.scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_INDEX'], marker='.', color='#F04950', label='{0}中该行业持仓占净值比（%）'.format(target_fund_name))
                ax.scatter(data.dropna(subset=[compare_fund_name])['INDEX'], data.dropna(subset=[compare_fund_name])['CLOSE_INDEX'], marker='.', color='#6268A2', label='{0}中该行业持仓占净值比（%）'.format(compare_fund_name))
                for x, y, value in zip(list(data.dropna(subset=[target_fund_name])['INDEX']), list(data.dropna(subset=[target_fund_name])['CLOSE_INDEX']), list(data.dropna(subset=[target_fund_name])[target_fund_name])):
                    ax.text(x, y * 1.1, value, ha='center', va='bottom', color='#F04950')
                for x, y, value in zip(list(data.dropna(subset=[compare_fund_name])['INDEX']), list(data.dropna(subset=[compare_fund_name])['CLOSE_INDEX']), list(data.dropna(subset=[compare_fund_name])[compare_fund_name])):
                    ax.text(x, y * 0.9, value, ha='center', va='bottom', color='#6268A2')
                ax.scatter(data.dropna(subset=[target_fund_name])['INDEX'], data.dropna(subset=[target_fund_name])['CLOSE_INDEX'], marker='.', color='#959595')
                ax.scatter(data.dropna(subset=[compare_fund_name])['INDEX'], data.dropna(subset=[compare_fund_name])['CLOSE_INDEX'], marker='.', color='#959595')
                plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                ax.set_xlabel('')
                ax.set_ylabel('')
                ax_right.set_ylabel('占净值比（%）')
                ax_right.set_ylim([0, 100])
                ax.legend(loc=2)
                ax_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                # ax1_right = ax[1].twinx()
                # ax[1].bar([i - bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['PE_TTM']), width=bar_width, color='#C94649', label='PE_TTM')
                # ax1_right.bar([i + bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['ROE_TTM']), width=bar_width, color='#8588B7', label='ROE_TTM')
                # plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
                # ax[1].set_xlabel('')
                # ax[1].set_ylabel('')
                # ax1_right.set_ylabel('')
                # ax[1].legend(loc=2)
                # ax1_right.legend(loc=1)
                # ax1_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
                plt.tight_layout()
                plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding_compare/{1}_{2}_{3}.png'.format(self.target_fund_code, industry, target_fund_name, compare_fund_name))
                worksheet_hc.insert_image('{0}{1}'.format(cell_dic[j + 1], i + 1), 'D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding_compare/{1}_{2}_{3}.png'.format(self.target_fund_code, industry, target_fund_name, compare_fund_name), {'x_scale': 0.05, 'y_scale': 0.05})
                ########################################

                industry_holding[target_fund_name] = industry_holding[target_fund_name].fillna(0.00)
                industry_holding[compare_fund_name] = industry_holding[compare_fund_name].fillna(0.00)
                industry_holding.loc[industry_holding.index.str.slice(4, 6).isin(['03', '09']), target_fund_name] = industry_holding.loc[industry_holding.index.str.slice(4, 6).isin(['03', '09']), target_fund_name].apply(lambda x: '>={0}'.format(x))
                industry_holding.loc[industry_holding.index.str.slice(4, 6).isin(['03', '09']), compare_fund_name] = industry_holding.loc[industry_holding.index.str.slice(4, 6).isin(['03', '09']), compare_fund_name].apply(lambda x: '>={0}'.format(x))
                industry_holding.loc[industry_holding.index < target_start_date, target_fund_name] = '--'
                industry_holding.loc[industry_holding.index < compare_start_date, compare_fund_name] = '-'
                industry_holding = industry_holding.sort_index().T.reset_index().rename(columns={'index': '基金名称'})
                industry_holding_columns = list(industry_holding.columns)
                industry_holding['INDUSTRY_NAME'] = industry
                industry_holding = industry_holding[['INDUSTRY_NAME'] + industry_holding_columns]
                industry_holding.columns = ['申万一级行业'] + industry_holding_columns
                industry_holding['行业仓位变动比较图'] = ''
                industry_holding.loc[industry_holding.shape[0]] = [np.nan] * industry_holding.shape[1]
                industry_holding = industry_holding.T.reset_index().T
                hypre_link = r'=HYPERLINK("#' + '行业仓位变动比较图' + '!' + '{0}{1}'.format(cell_dic[j + 1], i + 1) + '\",\"' + '行业仓位变动比较图' + '")'
                industry_holding.iloc[0, -1] = hypre_link
                industry_holding_list.append(industry_holding)

        if len(self.compare_fund_code_list) > 0:
            same_industry = pd.concat(same_industry_list, axis=1)
            same_industry.loc[:, same_industry.shape[1]] = [np.nan] * same_industry.shape[0]
            same_industry = same_industry.rename(columns={list(same_industry.columns)[-1]: ''})
            same_industry = same_industry.reset_index().drop('index', axis=1)
            industry_holding = pd.concat(industry_holding_list)
            industry_holding.columns = [''] * industry_holding.shape[1]
            industry_holding = industry_holding.reset_index().drop('index', axis=1)
            industry_holding_compare = pd.concat([fund_industry_holding, same_industry, industry_holding], axis=1)
        else:
            industry_holding_compare = pd.concat([fund_industry_holding], axis=1)
        return industry_holding_compare

    def get_stock_operation(self, stocks):
        fund_name = self.all_fund[self.all_fund['FUND_CODE'] == self.target_fund_code]['FUND_NAME'].values[0]
        for stock in stocks:
            # 个股仓位变动图
            stock_daily_k = self.all_stock_daily_k[self.all_stock_daily_k['TICKER_SYMBOL'] == stock]
            stock_daily_k['TRADE_DATE'] = stock_daily_k['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
            stock_daily_k = stock_daily_k.sort_values('TRADE_DATE')
            stock_name = stock_daily_k['SEC_SHORT_NAME'].values[-1]
            stock_valuation = self.all_stock_valuation[self.all_stock_valuation['TICKER_SYMBOL'] == stock]
            stock_valuation['TRADE_DATE'] = stock_valuation['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
            stock_valuation = stock_valuation.sort_values('TRADE_DATE')
            stock_finance = self.all_stock_finance[self.all_stock_finance['TICKER_SYMBOL'] == stock]
            stock_finance = stock_finance.sort_values(['END_DATE', 'PUBLISH_DATE']).drop_duplicates(['END_DATE'], keep='last')
            stock_finance = stock_finance.merge(self.all_calendar_trade_df[['CALENDAR_DATE', 'TRADE_DATE']].rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='left')
            stock_finance['TRADE_DATE'] = stock_finance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
            stock_finance = stock_finance.sort_values('TRADE_DATE')
            stock_holding_disp = self.all_fund_holding[(self.all_fund_holding['FUND_CODE'] == self.target_fund_code) & (self.all_fund_holding['TICKER_SYMBOL'] == stock)]
            stock_holding_disp = stock_holding_disp[['REPORT_DATE', 'MV_IN_NA']].set_index('REPORT_DATE')
            stock_holding_disp['MV_IN_NA'] = stock_holding_disp['MV_IN_NA'].apply(lambda x: round(x, 2))
            stock_holding_disp.columns = [fund_name]
            disp_start_date = min(stock_holding_disp.index)
            disp_dates = self.all_report_df[self.all_report_df['REPORT_DATE'] >= disp_start_date]['REPORT_DATE'].unique().tolist()[:-1]
            stock_holding_disp = stock_holding_disp.reindex(disp_dates)
            stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['06', '12'])) & (stock_holding_disp[fund_name].isnull()), fund_name] = 0.00
            stock_holding_disp = stock_holding_disp.merge(self.all_fund_holding_min[self.all_fund_holding_min['FUND_CODE'] == self.target_fund_code][['REPORT_DATE', 'MV_IN_NA_MIN']].set_index('REPORT_DATE'), left_index=True, right_index=True, how='left')
            stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[fund_name].isnull()), fund_name] = stock_holding_disp.loc[(stock_holding_disp.index.str.slice(4, 6).isin(['03', '09'])) & (stock_holding_disp[fund_name].isnull()), 'MV_IN_NA_MIN']
            stock_holding_disp = stock_holding_disp.drop('MV_IN_NA_MIN', axis=1)
            stock_holding_disp[fund_name] = stock_holding_disp[fund_name].astype(str)
            stock_holding_disp = stock_holding_disp.reset_index()
            stock_holding_disp = stock_holding_disp.merge(self.all_calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
            stock_holding_disp['TRADE_DATE'] = stock_holding_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
            stock_holding_disp = stock_holding_disp.sort_values('TRADE_DATE')
            stock_holding_disp_quancang = stock_holding_disp.loc[stock_holding_disp['REPORT_DATE'].str.slice(4, 6).isin(['06', '12'])]
            stock_holding_disp_quancang[fund_name] = stock_holding_disp_quancang[fund_name].replace('--', np.nan)
            stock_holding_disp_quancang[fund_name] = stock_holding_disp_quancang[fund_name].astype(float)
            stock_holding_disp_quancang = stock_holding_disp_quancang.rename(columns={fund_name: fund_name + '（全仓）'})
            all_report_trade_df = self.all_report_trade_df[['TRADE_DATE']]
            all_report_trade_df['TRADE_DATE'] = all_report_trade_df['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
            all_report_trade_df['IS_QUARTER_END'] = 1

            data = stock_daily_k[stock_daily_k['TRADE_DATE'] >= datetime.strptime(disp_start_date, '%Y%m%d') - timedelta(30)][['TRADE_DATE', 'CLOSE_PRICE']]
            data = data.merge(stock_valuation[['TRADE_DATE', 'PE_TTM']], on=['TRADE_DATE'], how='left')
            data = data.merge(stock_finance[['TRADE_DATE', 'ROE_TTM']], on=['TRADE_DATE'], how='left')
            data = data.merge(stock_holding_disp[['TRADE_DATE', fund_name]], on=['TRADE_DATE'], how='left')
            data = data.merge(stock_holding_disp_quancang[['TRADE_DATE', fund_name + '（全仓）']], on=['TRADE_DATE'], how='left')
            data = data.merge(all_report_trade_df[['TRADE_DATE', 'IS_QUARTER_END']], on=['TRADE_DATE'], how='left')
            data['INDEX'] = range(len(data))
            data['TRADE_DATE_DISP'] = data['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d')[:6])
            fig, ax = plt.subplots(2, 1, figsize=(25, 10))
            bar_width = len(data) / len(data.dropna(subset=[fund_name])) / 10.0
            ax0_right = ax[0].twinx()
            ax[0].plot(data['INDEX'], data['CLOSE_PRICE'], color='#AFDEFA', label='{0}（元）'.format(stock_name))
            ax0_right.bar(data['INDEX'], data[fund_name + '（全仓）'], width=bar_width, color='#C94649', label='占净值比（%）')
            ax0_right.set_ylim([0, 50])
            ax[0].scatter(data.dropna(subset=[fund_name])['INDEX'], data.dropna(subset=[fund_name])['CLOSE_PRICE'], marker='.', color='#F04950', label='{0}中该个股持仓占净值比（%）'.format(fund_name))
            for x, y, value in zip(list(data.dropna(subset=[fund_name])['INDEX']), list(data.dropna(subset=[fund_name])['CLOSE_PRICE']), list(data.dropna(subset=[fund_name])[fund_name])):
                ax[0].text(x, y * 1.1, value, ha='center', va='bottom', color='#F04950')
            plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
            ax[0].set_xlabel('')
            ax[0].set_ylabel('')
            ax0_right.set_ylabel('')
            ax[0].legend(loc=2)
            ax0_right.legend(loc=1)
            ax0_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax1_right = ax[1].twinx()
            ax[1].bar([i - bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['PE_TTM']), width=bar_width, color='#C94649', label='PE_TTM')
            ax1_right.bar([i + bar_width / 2.0 for i in list(data.dropna(subset=['ROE_TTM'])['INDEX'])], list(data.dropna(subset=['ROE_TTM'])['ROE_TTM']), width=bar_width, color='#8588B7', label='ROE_TTM')
            plt.xticks(ticks=data.dropna(subset=['IS_QUARTER_END'])['INDEX'], labels=data.dropna(subset=['IS_QUARTER_END'])['TRADE_DATE_DISP'], rotation=90)
            ax[1].set_xlabel('')
            ax[1].set_ylabel('')
            ax1_right.set_ylabel('')
            ax[1].legend(loc=2)
            ax1_right.legend(loc=1)
            ax1_right.yaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.tight_layout()
            plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/{0}_{1}.png'.format(stock_name, fund_name))
        return

    def get_holding_compare(self):
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/'):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/holding_compare/')
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/'.format(self.target_fund_code)):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/'.format(self.target_fund_code))
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding/'.format(self.target_fund_code)):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding/'.format(self.target_fund_code))
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding_compare/'.format(self.target_fund_code)):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/stock_holding_compare/'.format(self.target_fund_code))
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding/'.format(self.target_fund_code)):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding/'.format(self.target_fund_code))
        if not os.path.exists('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding_compare/'.format(self.target_fund_code)):
            os.makedirs('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/industry_holding_compare/'.format(self.target_fund_code))

        excel_writer = pd.ExcelWriter('D:/Git/hbshare/hbshare/fe/xwq/data/fund_report/{0}/持仓情况.xlsx'.format(self.target_fund_code), engine='xlsxwriter')
        worksheet1 = excel_writer.book.add_worksheet('个股仓位变动图')
        worksheet2 = excel_writer.book.add_worksheet('个股仓位变动比较图')
        worksheet3 = excel_writer.book.add_worksheet('行业仓位变动图')
        worksheet4 = excel_writer.book.add_worksheet('行业仓位变动比较图')
        stock_holding_compare = self.get_stock_holding_compare(worksheet1, worksheet2)
        industry_holding_compare = self.get_industry_holding_compare(worksheet3, worksheet4)
        stock_holding_compare.to_excel(excel_writer, sheet_name='个股持仓情况', index=False)
        industry_holding_compare.to_excel(excel_writer, sheet_name='行业持仓情况', index=False)
        excel_writer.save()
        # self.get_stock_operation(['600745', '002049', '002920', '300474', '601012', '600438', '002250', '600406', '600703', '600021','600116'])
        return

if __name__ == '__main__':
    target_fund_code = '007493'
    compare_fund_code_list = ['001856', '001410', '001975']
    HoldingCompare(target_fund_code, compare_fund_code_list).get_holding_compare()

    # holding_operation('601012', '007493')

    # for stock in ['002141', '300059', '601128', '603816']:
    #     holding_operation(stock, '688888', '20190331')