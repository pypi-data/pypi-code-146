# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.xwq.analysis.utils.const_var import TimeDateFormat
from hbshare.fe.xwq.analysis.utils.timedelta_utils import TimeDateUtil
from datetime import datetime
import os
import numpy as np
import pandas as pd

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

from matplotlib.ticker import FuncFormatter
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
myfont = matplotlib.font_manager.FontProperties(fname=r"D:/Git/hbshare/hbshare/fe/xwq/data/FZCKJW.TTF")
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                   '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
new_color_list = ['#F04950', '#959595', '#6268A2', '#333335', '#D57C56', '#628497']


def from_rgb_to_color16(rgb):
    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


def to_100percent(temp, position):
    return '%0.01f'%(temp * 100) + '%'


def to_percent(temp, position):
    return '%0.01f'%(temp) + '%'


def filter_extreme_mad(ser, n=3):
    median = ser.quantile(0.5)
    new_median = ((ser - median).abs()).quantile(0.5)
    max_range = median + n * new_median
    min_range = median - n * new_median
    ser = np.clip(ser, min_range, max_range)
    return ser


def quantile_definition(col, idxs, daily_df):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    q = (1.0 - np.count_nonzero(part_df[col].iloc[-1] <= daily_df[col]) / len(daily_df)) * 100.0
    return q


def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:4])
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


class PeTracking:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = TimeDateUtil.convert_format(self.start_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.end_date_hyphen = TimeDateUtil.convert_format(self.end_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.data_path = data_path
        self.stocks = pd.read_excel('{0}stocks.xlsx'.format(self.data_path))
        self.stocks['TICKER_SYMBOL'] = self.stocks['代码'].apply(lambda x: str(x).split('.')[0])
        self.indexs = pd.read_excel('{0}indexs.xlsx'.format(self.data_path))
        if not os.path.exists(self.data_path + self.end_date):
            os.makedirs(self.data_path + self.end_date)
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        if os.path.isfile('{0}stock_valuation.hdf'.format(self.data_path)):
            existed_stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), self.start_date)
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = self.start_date
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_valuation_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            stock_valuation_date = stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            star_stock_valuation_date = star_stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(star_stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            stock_valuation_list.append(stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat([existed_stock_valuation] + stock_valuation_list, ignore_index=True)
        self.stock_valuation = self.stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_valuation = self.stock_valuation.reset_index().drop('index', axis=1)
        self.stock_valuation['TRADE_DATE'] = self.stock_valuation['TRADE_DATE'].astype(str)
        self.stock_valuation.to_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')

        index_valuation_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_valuation_index = w.wsd(index, "pe_ttm", self.start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_valuation_index.columns = ['TRADE_DATE', 'PE_TTM']
            index_valuation_index['INDEX_SYMBOL'] = index
            index_valuation_index = index_valuation_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
            index_valuation_list.append(index_valuation_index)
            print(index)
        self.index_valuation = pd.concat(index_valuation_list, ignore_index=True)
        self.index_valuation = self.index_valuation[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
        self.index_valuation = self.index_valuation.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_valuation = self.index_valuation.reset_index().drop('index', axis=1)
        self.index_valuation['TRADE_DATE'] = self.index_valuation['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_valuation.to_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')
        return

    def get_stocks_forwardpehr(self):
        latest_stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'] == self.end_date]
        stocks_forwardpehr = self.stocks.merge(latest_stock_valuation[['TICKER_SYMBOL', 'FORWARD_PEHR']], on=['TICKER_SYMBOL'], how='left')
        stocks_forwardpehr = stocks_forwardpehr.drop('TICKER_SYMBOL', axis=1)
        stocks_forwardpehr.to_excel('{0}{1}/stocks_forwardpehr.xlsx'.format(self.data_path, self.end_date))
        return

    def get_stocks_pe_quantile(self):
        stock_valuation = self.stock_valuation[self.stock_valuation['TICKER_SYMBOL'].isin(self.stocks['TICKER_SYMBOL'].unique().tolist())]
        stock_valuation = stock_valuation.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='PE_TTM')
        stock_valuation = stock_valuation.sort_index()
        stocks_pe_quantile = pd.DataFrame(stock_valuation.apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0))
        stocks_pe_quantile = stocks_pe_quantile.reset_index()
        stocks_pe_quantile.columns = ['TICKER_SYMBOL', 'PE_QUANTILE']
        stocks_pe_quantile = self.stocks.merge(stocks_pe_quantile, on=['TICKER_SYMBOL'], how='left')
        stocks_pe_quantile = stocks_pe_quantile.drop('TICKER_SYMBOL', axis=1)
        stocks_pe_quantile.to_excel('{0}{1}/stocks_pe_quantile.xlsx'.format(self.data_path, self.end_date))
        return

    def get_indexs_pe_quantile(self):
        index_valuation = self.index_valuation[self.index_valuation['INDEX_SYMBOL'].isin(self.indexs['代码'].unique().tolist())]
        index_valuation = index_valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE_TTM')
        index_valuation = index_valuation.sort_index()
        indexs_pe_quantile = pd.DataFrame(index_valuation.apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0))
        indexs_pe_quantile = indexs_pe_quantile.reset_index()
        indexs_pe_quantile.columns = ['代码', 'PE_QUANTILE']
        indexs_pe_quantile = self.indexs.merge(indexs_pe_quantile, on=['代码'], how='left')
        indexs_pe_quantile.to_excel('{0}{1}/indexs_pe_quantile.xlsx'.format(self.data_path, self.end_date))

        for sector in self.indexs['板块'].unique().tolist():
            sector_indexs = self.indexs[self.indexs['板块'] == sector]['代码'].unique().tolist()
            index_name_list = self.indexs[self.indexs['板块'] == sector]['名称'].unique().tolist()
            index_pe_list = [filter_extreme_mad(index_valuation[index].dropna()) for index in sector_indexs]
            ind_pe_latest = index_valuation[sector_indexs].iloc[-1]
            plt.figure(figsize=(12, 6))
            plt.boxplot(index_pe_list, labels=index_name_list, vert=True, widths=0.25, flierprops={'marker': 'o', 'markersize': 1}, meanline=True, showmeans=True, showfliers=False)
            plt.scatter(range(1, len(ind_pe_latest) + 1), ind_pe_latest.values, marker='o')
            plt.xticks(rotation=45)
            plt.ylabel('PE_TTM')
            plt.title(sector)
            plt.tight_layout()
            plt.savefig('{0}{1}/indexs_pe_quantile_{2}.png'.format(self.data_path, self.end_date, sector))
        return

    def get_amt_results(self):
        self.get_stocks_forwardpehr()
        self.get_stocks_pe_quantile()
        self.get_indexs_pe_quantile()


class IndustryTracking:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = TimeDateUtil.convert_format(self.start_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.end_date_hyphen = TimeDateUtil.convert_format(self.end_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.data_path = data_path
        self.stocks = pd.read_excel('{0}stocks.xlsx'.format(self.data_path))
        self.stocks['TICKER_SYMBOL'] = self.stocks['代码'].apply(lambda x: str(x).split('.')[0])
        self.indexs = pd.read_excel('{0}indexs_disp.xlsx'.format(self.data_path))
        self.indexs = self.indexs[self.indexs['是否展示'] == 1]
        self.indexs_names_dic = self.indexs.set_index('代码')['展示名称'].to_dict()
        self.factor_list = ['MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']
        self.factor_name_list = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS']
        self.factor_name_dict = {self.factor_list[i]: self.factor_name_list[i] for i in range(len(self.factor_list))}
        self.con_factor_list = ['CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
        self.con_factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
        self.con_factor_name_dict = {self.con_factor_list[i]: self.con_factor_name_list[i] for i in range(len(self.con_factor_list))}
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        if os.path.isfile('{0}stock_valuation.hdf'.format(self.data_path)):
            existed_stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), self.start_date)
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = self.start_date
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_valuation_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            stock_valuation_date = stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            star_stock_valuation_date = star_stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(star_stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            stock_valuation_list.append(stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat([existed_stock_valuation] + stock_valuation_list, ignore_index=True)
        self.stock_valuation = self.stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_valuation = self.stock_valuation.reset_index().drop('index', axis=1)
        self.stock_valuation['TRADE_DATE'] = self.stock_valuation['TRADE_DATE'].astype(str)
        self.stock_valuation.to_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')
        self.stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.stock_valuation = self.stock_valuation[(self.stock_valuation['TRADE_DATE'] >= self.start_date) & (self.stock_valuation['TRADE_DATE'] <= self.end_date)]

        index_valuation_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_valuation_index = w.wsd(index, "pe_ttm", self.start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_valuation_index.columns = ['TRADE_DATE', 'PE_TTM']
            index_valuation_index['INDEX_SYMBOL'] = index
            index_valuation_index = index_valuation_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
            index_valuation_list.append(index_valuation_index)
            print(index)
        self.index_valuation = pd.concat(index_valuation_list, ignore_index=True)
        self.index_valuation = self.index_valuation[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
        self.index_valuation = self.index_valuation.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_valuation = self.index_valuation.reset_index().drop('index', axis=1)
        self.index_valuation['TRADE_DATE'] = self.index_valuation['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_valuation.to_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')
        self.index_valuation = self.index_valuation[self.index_valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.index_valuation = self.index_valuation[(self.index_valuation['TRADE_DATE'] >= self.start_date) & (self.index_valuation['TRADE_DATE'] <= self.end_date)]

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_daily_k_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_daily_k_index = w.wsd(index, "close", start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_daily_k_index.columns = ['TRADE_DATE', 'CLOSE_INDEX']
            index_daily_k_index['INDEX_SYMBOL'] = index
            index_daily_k_index = index_daily_k_index[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
            index_daily_k_list.append(index_daily_k_index)
            print(index)
        self.index_daily_k = pd.concat(index_daily_k_list, ignore_index=True)
        self.index_daily_k = self.index_daily_k[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        self.index_daily_k = self.index_daily_k.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_daily_k = self.index_daily_k.reset_index().drop('index', axis=1)
        self.index_daily_k['TRADE_DATE'] = self.index_daily_k['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_daily_k.to_hdf('{0}index_daily_k.hdf'.format(self.data_path), key='table', mode='w')
        self.index_daily_k = pd.read_hdf('{0}index_daily_k.hdf'.format(self.data_path), key='table')
        self.index_daily_k = self.index_daily_k[self.index_daily_k['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.index_daily_k = self.index_daily_k[self.index_daily_k['TRADE_DATE'] <= self.end_date]

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_finance_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_finance_index = w.wsd(index, "oper_rev,or_ttm2,yoy_or,qfa_yoysales,qfa_cgrsales,np_belongto_parcomsh,profit_ttm2,yoynetprofit,qfa_yoynetprofit,qfa_cgrnetprofit,roe_avg,qfa_roe,yoyroe,roa,qfa_roa,grossprofitmargin,qfa_grossprofitmargin,netprofitmargin,qfa_netprofitmargin,eps_basic,bps", start_date_hyphen, self.end_date_hyphen, "unit=1;rptType=1;Period=Q;Days=Alldays", usedf=True)[1].reset_index()
            index_finance_index.columns = ['REPORT_DATE', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']
            index_finance_index['INDEX_SYMBOL'] = index
            index_finance_index = index_finance_index[['REPORT_DATE', 'INDEX_SYMBOL', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']]
            index_finance_list.append(index_finance_index)
            print(index)
        self.index_finance = pd.concat(index_finance_list, ignore_index=True)
        self.index_finance = self.index_finance[['REPORT_DATE', 'INDEX_SYMBOL', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']]
        self.index_finance = self.index_finance.sort_values(['REPORT_DATE', 'INDEX_SYMBOL']).drop_duplicates(['REPORT_DATE', 'INDEX_SYMBOL'])
        self.index_finance = self.index_finance.reset_index().drop('index', axis=1)
        self.index_finance['REPORT_DATE'] = self.index_finance['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_finance.to_hdf('{0}index_finance.hdf'.format(self.data_path), key='table', mode='w')
        self.index_finance = pd.read_hdf('{0}index_finance.hdf'.format(self.data_path), key='table')
        self.index_finance = self.index_finance[(self.index_finance['REPORT_DATE'] >= self.start_date) & (self.index_finance['REPORT_DATE'] <= self.end_date)]
        self.index_finance = self.index_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_consensus_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_consensus_index = w.wsd(index, "west_sales_FY1,west_sales_YOY,west_sales_CAGR,west_netprofit_FY1,west_netprofit_YOY,west_netprofit_CAGR,west_nproc_1w,west_nproc_4w,west_nproc_13w,west_nproc_26w,west_avgroe_FY1,west_avgroe_YOY,west_eps_FY1,west_avgbps_FY1", start_date_hyphen, self.end_date_hyphen, "unit=1;year=2022;Period=Q;Days=Alldays", usedf=True)[1].reset_index()
            index_consensus_index.columns = ['REPORT_DATE', 'CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
            index_consensus_index['INDEX_SYMBOL'] = index
            index_consensus_index = index_consensus_index[['REPORT_DATE', 'INDEX_SYMBOL', 'CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']]
            index_consensus_list.append(index_consensus_index)
            print(index)
        self.index_consensus = pd.concat(index_consensus_list, ignore_index=True)
        self.index_consensus = self.index_consensus[['REPORT_DATE', 'INDEX_SYMBOL', 'CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']]
        self.index_consensus = self.index_consensus.sort_values(['REPORT_DATE', 'INDEX_SYMBOL']).drop_duplicates(['REPORT_DATE', 'INDEX_SYMBOL'])
        self.index_consensus = self.index_consensus.reset_index().drop('index', axis=1)
        self.index_consensus['REPORT_DATE'] = self.index_consensus['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_consensus.to_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table', mode='w')
        self.index_consensus = pd.read_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table')
        self.index_consensus = self.index_consensus[(self.index_consensus['REPORT_DATE'] >= self.start_date) & (self.index_consensus['REPORT_DATE'] <= self.end_date)]
        self.index_consensus = self.index_consensus.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_data_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_data_index = w.wsd("8841448.WI", "west_avgroe_FY1,west_avgroe_YOY,pb_lf", start_date_hyphen, self.end_date_hyphen, "Days=Alldays", usedf=True)[1].reset_index()
            index_data_index.columns = ['TRADE_DATE', 'CON_ROE_FY1', 'CON_ROE_YOY', 'PB_LF']
            index_data_index['INDEX_SYMBOL'] = index
            index_data_index = index_data_index[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1', 'CON_ROE_YOY', 'PB_LF']]
            index_data_list.append(index_data_index)
            print(index)
        self.index_data = pd.concat(index_data_list, ignore_index=True)
        self.index_data.to_hdf('{0}index_data.hdf'.format(self.data_path), key='table', mode='w')
        self.index_data = pd.read_hdf('{0}index_data.hdf'.format(self.data_path), key='table')

        self.index_con_roe = self.index_data[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1']]
        self.index_con_roe = self.index_con_roe.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_con_roe = self.index_con_roe.reset_index().drop('index', axis=1)
        self.index_con_roe['TRADE_DATE'] = self.index_con_roe['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_con_roe = self.index_con_roe[self.index_con_roe['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.index_con_roe = self.index_con_roe[(self.index_con_roe['TRADE_DATE'] >= self.start_date) & (self.index_con_roe['TRADE_DATE'] <= self.end_date)]

        self.index_con_roe_yoy = self.index_data[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_YOY']]
        self.index_con_roe_yoy = self.index_con_roe_yoy.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_con_roe_yoy = self.index_con_roe_yoy.reset_index().drop('index', axis=1)
        self.index_con_roe_yoy['TRADE_DATE'] = self.index_con_roe_yoy['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_con_roe_yoy = self.index_con_roe_yoy[self.index_con_roe_yoy['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.index_con_roe_yoy = self.index_con_roe_yoy[(self.index_con_roe_yoy['TRADE_DATE'] >= self.start_date) & (self.index_con_roe_yoy['TRADE_DATE'] <= self.end_date)]

        self.index_pb_lf = self.index_data[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
        self.index_pb_lf = self.index_pb_lf.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_pb_lf = self.index_pb_lf.reset_index().drop('index', axis=1)
        self.index_pb_lf['TRADE_DATE'] = self.index_pb_lf['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_pb_lf = self.index_pb_lf[self.index_pb_lf['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        self.index_pb_lf = self.index_pb_lf[(self.index_pb_lf['TRADE_DATE'] >= self.start_date) & (self.index_pb_lf['TRADE_DATE'] <= self.end_date)]
        return

    def get_amt_ret(self):
        index_daily_k = self.index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()

        # 周收益情况
        last_date = self.trade_df[(self.trade_df['IS_WEEK_END'] == '1') & (self.trade_df['TRADE_DATE'] <= self.end_date)]['TRADE_DATE'].iloc[-2]
        index_daily_k_w = index_daily_k[(index_daily_k.index >= last_date) & (index_daily_k.index <= self.end_date)]
        index_daily_k_wret = index_daily_k_w.iloc[-1] / index_daily_k_w.iloc[0] - 1
        index_daily_k_wret = index_daily_k_wret.reset_index()
        index_daily_k_wret.columns = ['代码', '周收益']
        indexs_wret = self.indexs.merge(index_daily_k_wret, on=['代码'], how='left')
        sector_list = self.indexs['板块'].unique().tolist()
        sector_color_list = ([bar_color_list[0], bar_color_list[7]] * len(sector_list))[:len(sector_list)]
        sector_color_dict = {sector: sector_color_list[i] for i, sector in enumerate(sector_list)}
        indexs_wret['颜色'] = indexs_wret['板块'].apply(lambda x: sector_color_dict[x])
        indexs_wret['索引'] = range(len(indexs_wret))
        # 周收益柱状图
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='索引', y='周收益', data=indexs_wret, palette=indexs_wret['颜色'].tolist())
        ax.set_xticklabels(labels=indexs_wret['展示名称'].tolist(), rotation=90)
        ax.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.xlabel('')
        plt.ylabel('周收益')
        plt.tight_layout()
        plt.savefig('{0}wret_{1}.png'.format(self.data_path, self.end_date))

        # 先进制造情况
        amt_indexs = self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()
        amt_index_daily_k = index_daily_k[amt_indexs]
        amt_index_daily_k = amt_index_daily_k / amt_index_daily_k.iloc[0]
        amt_index_daily_k.columns = [self.indexs_names_dic[col] for col in list(amt_index_daily_k.columns)]
        amt_index_daily_k = amt_index_daily_k.reset_index()
        amt_index_daily_k['TRADE_DATE'] = amt_index_daily_k['TRADE_DATE'].apply(lambda x: TimeDateUtil.convert_str_to_date(x, '%Y%m%d'))
        # 指数走势线型图
        plt.figure(figsize=(12, 6))
        for i, index_name in enumerate(list(amt_index_daily_k.columns)[1:]):
            sns.lineplot(x='TRADE_DATE', y=index_name, data=amt_index_daily_k, label=index_name, color=line_color_list[i])
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.25), ncol=5)
        plt.xlabel('')
        plt.ylabel('')
        plt.title('各板块指数走势', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}close_{1}.png'.format(self.data_path, self.end_date))
        return

    def get_amt_valuation(self):
        index_valuation = self.index_valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE_TTM').sort_index()

        # 估值分布情况
        indexs_info = self.indexs.copy(deep=True)
        index_id_list = indexs_info['代码'].tolist()[::-1]
        index_name_list = indexs_info['展示名称'].tolist()[::-1]
        index_valuation_list = [filter_extreme_mad(index_valuation[index].dropna()) for index in index_id_list]
        index_valuation_latest = index_valuation[index_id_list].iloc[-1]
        sector_list = indexs_info['板块'].unique().tolist()
        sector_color_list = ([bar_color_list[0], bar_color_list[7]] * len(sector_list))[:len(sector_list)]
        sector_color_dict = {sector: sector_color_list[i] for i, sector in enumerate(sector_list)}
        indexs_info['颜色'] = indexs_info['板块'].apply(lambda x: sector_color_dict[x])
        # 估值分布箱型图
        plt.figure(figsize=(12, 18))
        f = plt.boxplot(index_valuation_list, labels=index_name_list, vert=False, meanline=True, showmeans=True, showfliers=False, patch_artist=True, zorder=1)
        for box, c in zip(f['boxes'], indexs_info['颜色'].tolist()[::-1]):
            box.set(color=c)
        plt.scatter(index_valuation_latest.values, range(1, len(index_valuation_latest) + 1), marker='o', zorder=2)
        plt.xlabel('PE_TTM')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('{0}valuation_{1}.png'.format(self.data_path, self.end_date))

        # 估值分布情况（不细分）
        indexs_info = self.indexs[self.indexs['板块'] == '先进制造']
        index_id_list = indexs_info['代码'].tolist()
        index_name_list = indexs_info['展示名称'].tolist()
        index_valuation_list = [filter_extreme_mad(index_valuation[index].dropna()) for index in index_id_list]
        index_valuation_latest = index_valuation[index_id_list].iloc[-1]
        sector_list = indexs_info['板块'].unique().tolist()
        sector_color_list = ([bar_color_list[0], bar_color_list[7]] * len(sector_list))[:len(sector_list)]
        sector_color_dict = {sector: sector_color_list[i] for i, sector in enumerate(sector_list)}
        indexs_info['颜色'] = indexs_info['板块'].apply(lambda x: sector_color_dict[x])

        plt.figure(figsize=(12, 6))
        f = plt.boxplot(index_valuation_list, labels=index_name_list, vert=True, meanline=True, showmeans=True, showfliers=False, patch_artist=True, zorder=1)
        for box, c in zip(f['boxes'], indexs_info['颜色'].tolist()[::-1]):
            box.set(color=c)
        plt.scatter(range(1, len(index_valuation_latest) + 1), index_valuation_latest.values, marker='o', zorder=2)
        plt.xlabel('')
        plt.xticks(rotation=45)
        plt.title('各板块估值分布', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}valuation_{1}.png'.format(self.data_path, self.end_date))
        return

    def get_amt_prosperity(self):
        index_finance = self.index_finance.copy(deep=True)
        # index_finance = index_finance[index_finance['INDEX_SYMBOL'] != '881001.WI']
        index_consensus = self.index_consensus.copy(deep=True)
        # index_consensus = index_consensus[index_consensus['INDEX_SYMBOL'] != '881001.WI']
        index_factor = index_finance.drop('TRADE_DATE', axis=1).merge(index_consensus, on=['REPORT_DATE', 'INDEX_SYMBOL'], how='left')
        index_daily_k = self.index_daily_k.copy(deep=True)
        # index_daily_k_bmk = index_daily_k[index_daily_k['INDEX_SYMBOL'] == '881001.WI']

        # 测试指标有效性
        factor_list = ['MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']
        factor_name_list = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS']
        con_factor_list = ['CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
        con_factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
        factor_list = factor_list + con_factor_list
        factor_name_list = factor_name_list + con_factor_name_list
        factor_name_dict = {factor_list[i]: factor_name_list[i] for i in range(len(factor_list))}
        corr_df = pd.DataFrame(index=self.indexs['代码'].unique().tolist(), columns=factor_list)
        for factor in factor_list:
            for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
                # if index == '881001.WI':
                #     continue
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
                index_factor_index = index_factor[index_factor['INDEX_SYMBOL'] == index]
                max_report_date = index_factor_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
                index_factor_index = index_factor_index[index_factor_index['REPORT_DATE'] <= max_report_date]
                index_factor_index = index_factor_index[['REPORT_DATE', 'TRADE_DATE', 'INDEX_SYMBOL', factor]]
                index_factor_index = index_factor_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
                n = 1
                # ret or forward_ret
                index_factor_index['CLOSE_INDEX'] = index_factor_index['CLOSE_INDEX'].pct_change(n).shift(-n)
                # # forward_excess_ret
                # index_factor_index = index_factor_index.merge(index_daily_k_bmk.rename(columns={'CLOSE_INDEX': 'CLOSE_INDEX_BMK'}), on=['TRADE_DATE'], how='left')
                # index_factor_index['CLOSE_INDEX'] = (index_factor_index['CLOSE_INDEX'].pct_change(n) - index_factor_index['CLOSE_INDEX_BMK'].pct_change(n)).shift(-n)
                index_factor_index = index_factor_index.dropna().drop('TRADE_DATE', axis=1).sort_values('REPORT_DATE')
                # daily_ret_mean or daily_ret_median
                # index_daily_k_index['CLOSE_INDEX'] = index_daily_k_index['CLOSE_INDEX'].pct_change()
                # index_daily_k_index = index_daily_k_index[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX']]
                # index_daily_k_index['REPORT_DATE'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
                # index_daily_k_index = index_daily_k_index[['REPORT_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']].groupby(['REPORT_DATE', 'INDEX_SYMBOL']).mean().reset_index().rename(columns={'DAILY_RET': 'CLOSE_INDEX'})
                # index_factor_index = index_factor_index.merge(index_daily_k_index,  on=['INDEX_SYMBOL', 'REPORT_DATE'], how='left')
                # index_factor_index['CLOSE_INDEX'] = index_factor_index['CLOSE_INDEX'].shift(-1)
                # index_factor_index = index_factor_index.dropna().sort_values('REPORT_DATE')
                if len(index_factor_index) <= 2:
                    continue
                corr = round(np.corrcoef(index_factor_index[factor], index_factor_index['CLOSE_INDEX'])[0, 1], 2)
                corr_df.loc[index, factor] = corr

                # fig, ax1 = plt.subplots(figsize=(6, 3))
                # ax2 = ax1.twinx()
                # sns.lineplot(ax=ax1, x='REPORT_DATE', y=factor, data=index_factor_index, color=line_color_list[0])
                # sns.lineplot(ax=ax2, x='REPORT_DATE', y='CLOSE_INDEX', data=index_factor_index, color=line_color_list[1])
                # ax1.set_xlabel('')
                # ax2.set_xlabel('')
                # ax1.set_ylabel(factor_name_dict[factor])
                # ax2.set_ylabel(self.indexs_names_dic[index])
                # ax1.set_xticklabels(labels=index_factor_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # ax2.set_xticklabels(labels=index_factor_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # plt.title('两者相关系数为{2}%'.format(factor_name_dict[factor], self.indexs_names_dic[index], corr))
                # plt.tight_layout()
                # plt.savefig('{0}corr/{1}_{2}_{3}.png'.format(self.data_path, factor_name_dict[factor], self.indexs_names_dic[index], self.end_date))

        corr_df = corr_df.reset_index()
        corr_df.columns = ['代码'] + [factor_name_dict[col] for col in list(corr_df.columns)[1:]]
        indexs_corr = self.indexs[self.indexs['板块'] == '先进制造'].merge(corr_df, on=['代码'], how='left')
        # indexs_corr.to_excel('{0}factor_corr/factor_close_corr.xlsx'.format(self.data_path))
        # indexs_corr.to_excel('{0}factor_corr/factor_ret_corr.xlsx'.format(self.data_path))
        indexs_corr.to_excel('{0}factor_corr/factor_forward_ret_corr_{1}q.xlsx'.format(self.data_path, n))
        # indexs_corr.to_excel('{0}factor_corr/factor_forward_excess_ret_corr_{1}q.xlsx'.format(self.data_path, n))
        # indexs_corr.to_excel('{0}factor_corr/factor_forward_ret_median_corr.xlsx'.format(self.data_path))
        # indexs_corr.to_excel('{0}factor_corr/factor_forward_ret_mean_corr.xlsx'.format(self.data_path))
        return

    def get_amt_con_prosperity(self):
        index_consensus = self.index_consensus.copy(deep=True)
        # index_consensus = index_consensus[index_consensus['INDEX_SYMBOL'] != '881001.WI']
        index_finance = self.index_finance.copy(deep=True)
        index_daily_k = self.index_daily_k.copy(deep=True)
        # index_daily_k_bmk = index_daily_k[index_daily_k['INDEX_SYMBOL'] == '881001.WI']

        # 测试指标有效性
        factor_list = ['CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
        factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
        factor_name_dict = {factor_list[i]: factor_name_list[i] for i in range(len(factor_list))}
        corr_df = pd.DataFrame(index=self.indexs['代码'].unique().tolist(), columns=factor_list)
        for factor in factor_list:
            for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
                # if index == '881001.WI':
                #     continue
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
                index_consensus_index = index_consensus[index_consensus['INDEX_SYMBOL'] == index]
                index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
                max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
                index_consensus_index = index_consensus_index[index_consensus_index['REPORT_DATE'] <= max_report_date]
                index_consensus_index = index_consensus_index[['REPORT_DATE', 'TRADE_DATE', 'INDEX_SYMBOL', factor]]
                index_consensus_index = index_consensus_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
                n = 1
                # ret or forward_ret
                index_consensus_index['CLOSE_INDEX'] = index_consensus_index['CLOSE_INDEX'].pct_change(n).shift(-n)
                # # forward_excess_ret
                # index_consensus_index = index_consensus_index.merge(index_daily_k_bmk.rename(columns={'CLOSE_INDEX': 'CLOSE_INDEX_BMK'}), on=['TRADE_DATE'], how='left')
                # index_consensus_index['CLOSE_INDEX'] = (index_consensus_index['CLOSE_INDEX'].pct_change(n) - index_consensus_index['CLOSE_INDEX_BMK'].pct_change(n)).shift(-n)
                index_consensus_index = index_consensus_index.dropna().drop('TRADE_DATE', axis=1).sort_values('REPORT_DATE')
                # daily_ret_mean or daily_ret_median
                # index_daily_k_index['CLOSE_INDEX'] = index_daily_k_index['CLOSE_INDEX'].pct_change()
                # index_daily_k_index = index_daily_k_index[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX']]
                # index_daily_k_index['REPORT_DATE'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
                # index_daily_k_index = index_daily_k_index[['REPORT_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']].groupby(['REPORT_DATE', 'INDEX_SYMBOL']).mean().reset_index().rename(columns={'DAILY_RET': 'CLOSE_INDEX'})
                # index_consensus_index = index_consensus_index.merge(index_daily_k_index,  on=['INDEX_SYMBOL', 'REPORT_DATE'], how='left')
                # index_consensus_index['CLOSE_INDEX'] = index_consensus_index['CLOSE_INDEX'].shift(-1)
                # index_consensus_index = index_consensus_index.dropna().sort_values('REPORT_DATE')
                if len(index_consensus_index) <= 2:
                    continue
                corr = round(np.corrcoef(index_consensus_index[factor], index_consensus_index['CLOSE_INDEX'])[0, 1], 2)
                corr_df.loc[index, factor] = corr

                # fig, ax1 = plt.subplots(figsize=(6, 3))
                # ax2 = ax1.twinx()
                # sns.lineplot(ax=ax1, x='REPORT_DATE', y=factor, data=index_consensus_index, color=line_color_list[0])
                # sns.lineplot(ax=ax2, x='REPORT_DATE', y='CLOSE_INDEX', data=index_consensus_index, color=line_color_list[1])
                # ax1.set_xlabel('')
                # ax2.set_xlabel('')
                # ax1.set_ylabel(factor_name_dict[factor])
                # ax2.set_ylabel(self.indexs_names_dic[index])
                # ax1.set_xticklabels(labels=index_consensus_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # ax2.set_xticklabels(labels=index_consensus_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # plt.title('两者相关系数为{2}%'.format(factor_name_dict[factor], self.indexs_names_dic[index], corr))
                # plt.tight_layout()
                # plt.savefig('{0}con_corr/{1}_{2}_{3}.png'.format(self.data_path, factor_name_dict[factor], self.indexs_names_dic[index], self.end_date))

        corr_df = corr_df.reset_index()
        corr_df.columns = ['代码'] + [factor_name_dict[col] for col in list(corr_df.columns)[1:]]
        indexs_corr = self.indexs[self.indexs['板块'] == '先进制造'].merge(corr_df, on=['代码'], how='left')
        # indexs_corr.to_excel('{0}factor_corr/con_factor_close_corr.xlsx'.format(self.data_path))
        # indexs_corr.to_excel('{0}factor_corr/con_factor_ret_corr.xlsx'.format(self.data_path))
        indexs_corr.to_excel('{0}factor_corr/con_factor_forward_ret_corr_{1}q.xlsx'.format(self.data_path, n))
        # indexs_corr.to_excel('{0}factor_corr/con_factor_forward_excess_ret_corr_{1}q.xlsx'.format(self.data_path, n))
        # indexs_corr.to_excel('{0}factor_corr/con_factor_forward_ret_median_corr.xlsx'.format(self.data_path))
        # indexs_corr.to_excel('{0}factor_corr/con_factor_forward_ret_mean_corr.xlsx'.format(self.data_path))
        return

    def get_amt_prosperity_factor(self):
        index_finance = self.index_finance.copy(deep=True)
        # index_finance = index_finance[index_finance['INDEX_SYMBOL'] != '881001.WI']
        index_consensus = self.index_consensus.copy(deep=True)
        # index_consensus = index_consensus[index_consensus['INDEX_SYMBOL'] != '881001.WI']
        index_factor = index_finance.drop('TRADE_DATE', axis=1).merge(index_consensus, on=['REPORT_DATE', 'INDEX_SYMBOL'], how='left')
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k = index_daily_k[(index_daily_k['TRADE_DATE'] >= self.start_date) & (index_daily_k['TRADE_DATE'] <= self.end_date)]

        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        index_daily_k = index_daily_k[index_daily_k.index.isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        n = 1
        index_daily_k = index_daily_k.pct_change(n).shift(-n) * 100.0
        # index_daily_k = index_daily_k[[col for col in (index_daily_k.columns) if col != '881001.WI'] + ['881001.WI']]
        # index_daily_k = index_daily_k.apply(lambda x: x[:-1] - x[-1], axis=1)
        index_daily_k = index_daily_k.unstack().reset_index()
        index_daily_k.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'FORWARD_RET']
        index_corr = pd.read_excel('{0}factor_corr/factor_forward_ret_corr_{1}q.xlsx'.format(self.data_path, n), index_col=0)
        # index_corr = pd.read_excel('{0}factor_corr/factor_forward_excess_ret_corr_{1}q.xlsx'.format(self.data_path, n), index_col=0)
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        index_prosperity_list = []
        index_prosperity_corr = pd.DataFrame(index=self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist(), columns=['PROSPERITY_IC'])
        new_line_color_list = []
        for idx, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            # if index == '881001.WI':
            #     continue
            index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
            index_factor_index = index_factor[index_factor['INDEX_SYMBOL'] == index]
            index_corr_index = index_corr[index_corr['代码'] == index]
            index_factor_list = index_corr_index.T.iloc[6:].astype(float)
            index_factor_list.columns = ['CORR']
            index_factor_list = index_factor_list[index_factor_list['CORR'] > 0.3].index.tolist()
            if len(index_factor_list) == 0:
                continue
            index_factor_index = index_factor_index.drop('INDEX_SYMBOL', axis=1).set_index(['REPORT_DATE', 'TRADE_DATE']).sort_index().dropna(subset=['MAIN_INCOME'])
            index_factor_index.columns = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS'] + ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
            index_factor_index = index_factor_index[index_factor_list]
            index_factor_index = (index_factor_index - index_factor_index.mean()) / index_factor_index.std()
            index_factor_index = index_factor_index.mean(axis=1)
            index_factor_index = pd.DataFrame(index_factor_index).sort_index().reset_index()
            index_factor_index.columns = ['REPORT_DATE', 'TRADE_DATE', 'PROSPERITY']
            index_factor_index['INDEX_SYMBOL'] = index
            index_factor_index = index_factor_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='inner')
            index_prosperity_list.append(index_factor_index)
            corr = round(np.corrcoef(index_factor_index.dropna()['PROSPERITY'], index_factor_index.dropna()['FORWARD_RET'])[0, 1], 2)
            index_prosperity_corr.loc[index, 'PROSPERITY_IC'] = corr
            new_line_color_list.append(line_color_list[idx])
            sns.lineplot(ax=ax1, x='REPORT_DATE', y='PROSPERITY', data=index_factor_index, color=line_color_list[idx])
            ax1.set_xlabel('')
            ax1.set_ylabel('景气度指标', fontsize=16)
            ax1.set_ylim([-7.0, 5.0])
        index_prosperity = pd.concat(index_prosperity_list)
        index_prosperity['板块'] = index_prosperity['INDEX_SYMBOL'].apply(lambda x: self.indexs_names_dic[x])
        index_order = [self.indexs_names_dic[x] for x in index_prosperity['INDEX_SYMBOL'].unique().tolist()]
        sns.barplot(ax=ax2, x='REPORT_DATE', y='FORWARD_RET', data=index_prosperity, hue='板块', hue_order=index_order, palette=new_line_color_list)
        ax2.set_xlabel('')
        ax2.set_ylabel('未来{0}个季度收益'.format('一' if n == 1 else '两' if n == 2 else '三' if n == 3 else '四'), fontsize=16)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax2.set_ylim([-30.0, 120.0])
        ax2.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=9)
        plt.title('景气度指标与未来{0}个季度收益'.format('一' if n == 1 else '两' if n == 2 else '三' if n == 3 else '四'), fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}prosperity/prosperity_{1}q.png'.format(self.data_path, n))
        # plt.savefig('{0}prosperity/excess_prosperity_{1}q.png'.format(self.data_path, n))
        index_prosperity.to_excel('{0}prosperity/prosperity_{1}q.xlsx'.format(self.data_path, n))
        # index_prosperity.to_excel('{0}prosperity/excess_prosperity_{1}q.xlsx'.format(self.data_path, n))
        index_prosperity_corr = index_prosperity_corr.reset_index()
        index_prosperity_corr.columns = ['代码', '合成景气度指标IC']
        index_prosperity_corr = self.indexs[self.indexs['板块'] == '先进制造'].merge(index_prosperity_corr, on=['代码'], how='left')
        index_prosperity_corr.to_excel('{0}prosperity/prosperity_corr_{1}q.xlsx'.format(self.data_path, n))
        # index_prosperity_corr.to_excel('{0}prosperity/excess_prosperity_corr_{1}q.xlsx'.format(self.data_path, n))
        return

    def get_amt_pb_roe(self):
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_finance = self.index_finance.copy(deep=True)
        index_consensus = self.index_consensus.copy(deep=True)
        index_con_roe = self.index_con_roe.copy(deep=True)
        index_con_roe_yoy = self.index_con_roe_yoy.copy(deep=True)
        index_pb_lf = self.index_pb_lf.copy(deep=True)

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pb_lf_index = index_pb_lf[index_pb_lf['INDEX_SYMBOL'] == index]
            index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
            max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
            index_finance_index = index_finance_index[index_finance_index['REPORT_DATE'] <= max_report_date]
            index_pb_lf_index = index_pb_lf_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
            index_finance_index = index_finance_index[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE']]
            index_pb_roe = index_finance_index.merge(index_pb_lf_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            sns.lmplot(x='ROE', y='PB_LF', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['ROE'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['ROE'].iloc[i], index_pb_roe['PB_LF'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（历史ROE）', fontsize=10)
            plt.ylabel('ln(PB)', fontsize=10)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/roe_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

        max_report_date = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='MAIN_INCOME').dropna().index.max()
        index_finance_latest = index_finance[index_finance['REPORT_DATE'] == max_report_date]
        index_finance_latest = index_finance_latest[index_finance_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_finance_latest = index_finance_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE']]
        index_pb_lf_latest = index_pb_lf[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
        index_pb_roe = index_finance_latest.merge(index_pb_lf_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
        plt.figure(figsize=(6, 6))
        sns.lmplot(x='ROE', y='PB_LF', data=index_pb_roe, scatter=True, scatter_kws={'color': 'm'}, line_kws={'color': 'm'})
        for i in range(len(index_pb_roe)):
            plt.annotate(self.indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['ROE'][i], index_pb_roe['PB_LF'][i]), xytext=(index_pb_roe['ROE'][i], index_pb_roe['PB_LF'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（历史ROE）')
        plt.ylabel('ln(PB)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/roe_{1}.png'.format(self.data_path, self.end_date))

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pb_lf_index = index_pb_lf[index_pb_lf['INDEX_SYMBOL'] == index]
            index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
            max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
            index_finance_index = index_finance_index[index_finance_index['REPORT_DATE'] <= max_report_date]
            index_pb_lf_index = index_pb_lf_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
            index_finance_index = index_finance_index[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE_Q']]
            index_pb_roe = index_finance_index.merge(index_pb_lf_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            sns.lmplot(x='ROE_Q', y='PB_LF', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['ROE_Q'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['ROE_Q'].iloc[i], index_pb_roe['PB_LF'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（单季度ROE）', fontsize=10)
            plt.ylabel('ln(PB)', fontsize=10)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/roe_q_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

        max_report_date = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='MAIN_INCOME').dropna().index.max()
        index_finance_latest = index_finance[index_finance['REPORT_DATE'] == max_report_date]
        index_finance_latest = index_finance_latest[index_finance_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_finance_latest = index_finance_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE_Q']]
        index_pb_lf_latest = index_pb_lf[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
        index_pb_roe = index_finance_latest.merge(index_pb_lf_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
        plt.figure(figsize=(6, 6))
        sns.lmplot(x='ROE_Q', y='PB_LF', data=index_pb_roe, scatter=True, scatter_kws={'color': 'm'}, line_kws={'color': 'm'})
        for i in range(len(index_pb_roe)):
            plt.annotate(self.indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['ROE_Q'][i], index_pb_roe['PB_LF'][i]), xytext=(index_pb_roe['ROE_Q'][i], index_pb_roe['PB_LF'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（单季度ROE）')
        plt.ylabel('ln(PB)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/roe_q_{1}.png'.format(self.data_path, self.end_date))

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index]
            index_con_roe_index = index_con_roe[index_con_roe['INDEX_SYMBOL'] == index]
            index_pe_ttm_index = index_pe_ttm_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
            index_con_roe_index = index_con_roe_index[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1']]
            index_pb_roe = index_pe_ttm_index.merge(index_con_roe_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe = index_pb_roe.merge(self.trade_df, on=['TRADE_DATE'], how='left')
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=True).reset_index().drop('index', axis=1)
            index_pb_roe_weekly = index_pb_roe[index_pb_roe['IS_WEEK_END'] == '1']
            index_pb_roe_weekly = index_pb_roe_weekly.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            # sns.lmplot(x='CON_ROE_FY1', y='PE_TTM', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            # plt.plot(index_pb_roe['CON_ROE_FY1'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe_weekly))
            for i in range(len(index_pb_roe_weekly)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe_weekly['CON_ROE_FY1'].iloc[i], index_pb_roe_weekly['PE_TTM'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（一致预测ROE）', fontsize=10)
            plt.ylabel('PE_TTM', fontsize=10)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/con_roe_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

            index_pb_roe_line = index_pb_roe.copy(deep=True)
            index_pb_roe_line['TRADE_DATE'] = index_pb_roe_line['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            sns.lineplot(ax=ax1, x='TRADE_DATE', y='CON_ROE_FY1', data=index_pb_roe_line, label='预期ROE（一致预测ROE）', color=line_color_list[0])
            sns.lineplot(ax=ax2, x='TRADE_DATE', y='PE_TTM', data=index_pb_roe_line, label='PE_TTM', color=line_color_list[1])
            ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax1.set_xlabel('')
            ax2.set_xlabel('')
            ax1.set_ylabel('预期ROE（一致预测ROE）', fontsize=10)
            ax2.set_ylabel('PE_TTM', fontsize=10)
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/con_roe_line_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

        index_con_roe_latest = index_con_roe[index_con_roe['TRADE_DATE'] == self.end_date]
        index_con_roe_latest = index_con_roe_latest[index_con_roe_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_con_roe_latest = index_con_roe_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1']]
        index_pe_ttm_latest = index_pe_ttm[index_pe_ttm['TRADE_DATE'] == self.end_date]
        index_pe_ttm_latest = index_pe_ttm_latest[index_pe_ttm_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_pe_ttm_latest = index_pe_ttm_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
        index_pb_roe = index_con_roe_latest.merge(index_pe_ttm_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        plt.figure(figsize=(6, 6))
        plt.scatter(index_pb_roe['CON_ROE_FY1'].values, index_pb_roe['PE_TTM'].values, color='m')
        for i in range(len(index_pb_roe)):
            plt.annotate(self.indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['CON_ROE_FY1'][i], index_pb_roe['PE_TTM'][i]), xytext=(index_pb_roe['CON_ROE_FY1'][i], index_pb_roe['PE_TTM'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（一致预测ROE）')
        plt.ylabel('PE_TTM')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/con_roe_{1}.png'.format(self.data_path, self.end_date))

        index_prosperity = pd.read_excel('{0}prosperity/excess_prosperity_1q.xlsx'.format(self.data_path), index_col=0)
        index_prosperity['TRADE_DATE'] = index_prosperity['TRADE_DATE'].astype(str)
        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index]
            index_prosperity_index = index_prosperity[index_prosperity['INDEX_SYMBOL'] == index]
            if len(index_prosperity_index) == 0:
                continue
            index_pe_ttm_index = index_pe_ttm_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
            index_prosperity_index = index_prosperity_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PROSPERITY']]
            index_pb_roe = index_prosperity_index.merge(index_pe_ttm_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1).iloc[:5]
            plt.figure(figsize=(6, 6))
            # sns.lmplot(x='CON_ROE_FY1', y='PE_TTM', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['PROSPERITY'].values, index_pb_roe['PE_TTM'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['PROSPERITY'].iloc[i], index_pb_roe['PE_TTM'].iloc[i], '*', color=c)
            plt.xlabel('预期景气度', fontsize=16)
            plt.ylabel('PE_TTM', fontsize=16)
            plt.title(self.indexs_names_dic[index], fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
            plt.tight_layout()
            sns.despine(top=True, right=True, left=False, bottom=False)
            plt.savefig('{0}pe_q_prosperity/con_roe_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

            index_pb_roe_line = index_pb_roe.copy(deep=True)
            index_pb_roe_line['TRADE_DATE'] = index_pb_roe_line['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            sns.lineplot(ax=ax1, x='TRADE_DATE', y='PROSPERITY', data=index_pb_roe_line, label='预期景气度', color=line_color_list[0])
            sns.lineplot(ax=ax2, x='TRADE_DATE', y='PE_TTM', data=index_pb_roe_line, label='PE_TTM', color=line_color_list[1])
            ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax1.set_xlabel('')
            ax2.set_xlabel('')
            ax1.set_ylabel('预期景气度', fontsize=10)
            ax2.set_ylabel('PE_TTM', fontsize=10)
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_q_prosperity/con_roe_line_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

        index_prosperity = pd.read_excel('{0}prosperity_{1}.xlsx'.format(self.data_path, self.end_date))
        index_prosperity['REPORT_DATE'] = index_prosperity['REPORT_DATE'].astype(str)
        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index]
            index_pe_ttm_index = index_pe_ttm_index.sort_values('TRADE_DATE')
            index_pe_ttm_index['IDX'] = range(len(index_pe_ttm_index))
            index_pe_ttm_index['PE_TTM_QUANTILE'] = index_pe_ttm_index['IDX'].rolling(window=len(index_pe_ttm_index), min_periods=1, center=False).apply(lambda x: quantile_definition('PE_TTM', x, index_pe_ttm_index))
            index_prosperity_index = index_prosperity[index_prosperity['INDEX_SYMBOL'] == index]
            if len(index_prosperity_index) == 0:
                continue
            index_pe_ttm_index = index_pe_ttm_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM_QUANTILE']]
            index_prosperity_index = index_prosperity_index[['REPORT_DATE', 'INDEX_SYMBOL', 'PROSPERITY']]
            index_prosperity_index = index_prosperity_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PROSPERITY']]
            index_pb_roe = index_prosperity_index.merge(index_pe_ttm_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.merge(self.trade_df, on=['TRADE_DATE'], how='left')
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1).iloc[:5]
            plt.figure(figsize=(6, 6))
            # sns.lmplot(x='CON_ROE_FY1', y='PE_TTM_QUANTILE', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['PROSPERITY'].values, index_pb_roe['PE_TTM_QUANTILE'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['PROSPERITY'].iloc[i], index_pb_roe['PE_TTM_QUANTILE'].iloc[i], '*', color=c)
            plt.xlim([-2, 2])
            plt.ylim([0, 100])
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期景气度', fontsize=10)
            plt.ylabel('PE_TTM历史分位水平', fontsize=10)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_q_prosperity/con_roe_pe_q{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))

            index_pb_roe_line = index_pb_roe.copy(deep=True)
            index_pb_roe_line['TRADE_DATE'] = index_pb_roe_line['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            sns.lineplot(ax=ax1, x='TRADE_DATE', y='PROSPERITY', data=index_pb_roe_line, label='预期景气度', color=line_color_list[0])
            sns.lineplot(ax=ax2, x='TRADE_DATE', y='PE_TTM_QUANTILE', data=index_pb_roe_line, label='PE_TTM历史分位水平', color=line_color_list[1])
            ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax1.set_xlabel('')
            ax2.set_xlabel('')
            ax1.set_ylabel('预期景气度', fontsize=10)
            ax2.set_ylabel('PE_TTM历史分位水平', fontsize=10)
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_q_prosperity/con_roe_pe_q_line_{1}_{2}.png'.format(self.data_path, self.indexs_names_dic[index], self.end_date))
        return

    def get_amt_prosperity_tianfeng(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_finance = self.index_finance.copy(deep=True)
        index_pe_ttm = self.index_valuation.copy(deep=True)

        start = '20220501'
        end = '20220630'
        indexs = self.indexs.copy(deep=True)
        # indexs = self.indexs[self.indexs['板块'] == '先进制造']
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX')
        index_daily_k = index_daily_k.sort_index()
        index_pe_ttm = index_pe_ttm.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE_TTM')
        index_pe_ttm = index_pe_ttm.sort_index()
        # 各板块start与end之间涨幅
        index_daily_k_ytd = index_daily_k[(index_daily_k.index >= start) & (index_daily_k.index <= end)]
        index_ret = pd.DataFrame((index_daily_k_ytd.iloc[-1] / index_daily_k_ytd.iloc[0] - 1) * 100.0).reset_index()
        index_ret.columns = ['代码', '收益（%）']
        # 各板块2022Q1财务指标
        index_finance_2022Q1 = index_finance[index_finance['REPORT_DATE'] == '20220331']
        index_finance_2022Q1 = index_finance_2022Q1[['INDEX_SYMBOL', 'ROE', 'ROE_YOY', 'MAIN_INCOME_YOY', 'NET_PROFIT_YOY']]
        index_finance_2022Q1.columns = ['代码', 'ROE（%）', 'ROE同比增长率（%）', '营业收入同比增长率（%）', '归母净利润同比增长率（%）']
        # 各板块start与end估值
        index_pe_ttm_start = pd.DataFrame(index_pe_ttm[index_pe_ttm.index >= start].iloc[0]).reset_index()
        index_pe_ttm_start.columns = ['代码', '年初PE_TTM']
        index_pe_ttm_end = pd.DataFrame(index_pe_ttm[index_pe_ttm.index <= end].iloc[-1]).reset_index()
        index_pe_ttm_end.columns = ['代码', '期末PE_TTM（{0}）'.format(end)]
        index_pe_ttm_quantile_start = pd.DataFrame(index_pe_ttm[index_pe_ttm.index <= index_pe_ttm[index_pe_ttm.index >= start].index[0]].apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0)).reset_index()
        index_pe_ttm_quantile_start.columns = ['代码', '年初PE_TTM分位水平（%）']
        index_pe_ttm_quantile_end = pd.DataFrame(index_pe_ttm[index_pe_ttm.index <= end].apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0)).reset_index()
        index_pe_ttm_quantile_end.columns = ['代码', '期末PE_TTM分位水平（%）（{0}）'.format(end)]
        # 涨幅与财务估值
        index_performance = indexs[['展示名称', '代码']].merge(index_ret, on=['代码'], how='left').merge(index_finance_2022Q1, on=['代码'], how='left') \
                                       .merge(index_pe_ttm_start, on=['代码'], how='left').merge(index_pe_ttm_end, on=['代码'], how='left') \
                                       .merge(index_pe_ttm_quantile_start, on=['代码'], how='left').merge(index_pe_ttm_quantile_end, on=['代码'], how='left')
        index_performance = index_performance.sort_values('收益（%）', ascending=False).drop_duplicates()
        index_performance.to_excel('{0}performance/index_performance_{1}.xlsx'.format(self.data_path, end))
        # index_performance.to_excel('{0}performance/index_performance_先进制造_{1}.xlsx'.format(self.data_path, end))
        return

    def get_amt_prosperity_change_tianfeng(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_finance = self.index_finance.copy(deep=True)

        index_finance = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='NET_PROFIT_YOY')
        index_finance = index_finance.sort_index()
        index_finance = index_finance.unstack().reset_index()
        index_finance.columns = ['INDEX_SYMBOL', 'REPORT_DATE', 'NET_PROFIT_YOY_YEAR']
        index_finance['NET_PROFIT_YOY_LAST_YEAR'] = index_finance.groupby('INDEX_SYMBOL').apply(lambda x: x.sort_values('REPORT_DATE').shift(4))['NET_PROFIT_YOY_YEAR']
        index_finance['NET_PROFIT_YOY_DELTA'] = (index_finance['NET_PROFIT_YOY_YEAR'] - index_finance['NET_PROFIT_YOY_LAST_YEAR']) / abs(index_finance['NET_PROFIT_YOY_LAST_YEAR']) * 100.0
        index_finance['NET_PROFIT_YOY_DELTA_ABS'] = index_finance['NET_PROFIT_YOY_DELTA'].abs()
        # index_finance = index_finance[index_finance['INDEX_SYMBOL'] != '881001.WI']
        index_daily_k = index_daily_k[index_daily_k['TRADE_DATE'].isin([index_daily_k['TRADE_DATE'].min()] + index_finance['TRADE_DATE'].unique().tolist())]
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX')
        index_daily_k = index_daily_k.sort_index()
        index_daily_k = index_daily_k.pct_change().dropna() * 100.0
        # index_daily_k = index_daily_k[[col for col in (index_daily_k.columns) if col != '881001.WI'] + ['881001.WI']]
        # index_daily_k = index_daily_k.apply(lambda x: x[:-1] - x[-1], axis=1)
        index_daily_k = index_daily_k.unstack().reset_index()
        index_daily_k.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'RET']
        index_stat = index_finance.merge(index_daily_k, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        index_stat = index_stat[['INDEX_SYMBOL', 'REPORT_DATE', 'NET_PROFIT_YOY_LAST_YEAR', 'NET_PROFIT_YOY_YEAR', 'NET_PROFIT_YOY_DELTA', 'NET_PROFIT_YOY_DELTA_ABS', 'RET']]
        index_stat.columns = ['代码', '报告日期', '上一年增速（%）', '本年增速（%）', '增速变化幅度（%）', '增速变化幅度绝对值（%）', '收益率（%）']
        # 持续高增长
        index_prosperity_change = pd.DataFrame(index=range(16), columns=['增长类型', '上一年增速（%）', '本年增速（%）', '增速变化幅度（%）'] + sorted(index_stat['报告日期'].unique().tolist()))
        index_prosperity_change['增长类型'] = pd.Series(['持续高增长'] * 3 + ['加速增长'] * 3 + ['减速增长'] * 4 + ['低速稳定'] * 3 + ['困境反转'] * 3)
        index_prosperity_change['上一年增速（%）'] = pd.Series(['>100', '50-100', '30-50', '>100', '50-100', '30-50', '>60', '>60', '>60', '>60', '20-30', '10-20', '0-10', '<-100', '<-100', '<-100'])
        index_prosperity_change['本年增速（%）'] = pd.Series(['>100', '50-100', '30-50', '>100', '>50', '>30', '>40', '>30', '>20', '>0', '20-30', '10-20', '0-10', '>200', '>100', '>50'])
        index_prosperity_change['增速变化幅度（%）'] = pd.Series(['无要求', '无要求', '无要求', '加速', '加速', '加速', '减速（0-1/3）', '减速（1/3-1/2）', '减速（1/2-2/3）', '减速（2/3-1）', '无要求', '无要求', '无要求', '加速', '加速', '加速'])
        for year in index_stat['报告日期'].unique().tolist():
            index_stat_year = index_stat[index_stat['报告日期'] == year]
            index_prosperity_change.loc[0, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 100) & (index_stat_year['本年增速（%）'] > 100)]['收益率（%）'].mean()
            index_prosperity_change.loc[1, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 50) & (index_stat_year['上一年增速（%）'] <= 100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['本年增速（%）'] <= 100)]['收益率（%）'].mean()
            index_prosperity_change.loc[2, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 30) & (index_stat_year['上一年增速（%）'] <= 50) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['本年增速（%）'] <= 50)]['收益率（%）'].mean()
            index_prosperity_change.loc[3, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 100) & (index_stat_year['本年增速（%）'] > 100) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change.loc[4, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 50) & (index_stat_year['上一年增速（%）'] <= 100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change.loc[5, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 30) & (index_stat_year['上一年增速（%）'] <= 50) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change.loc[6, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 40) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 0) & (index_stat_year['增速变化幅度绝对值（%）'] <= 33.33)]['收益率（%）'].mean()
            index_prosperity_change.loc[7, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 33.33) & (index_stat_year['增速变化幅度绝对值（%）'] <= 50)]['收益率（%）'].mean()
            index_prosperity_change.loc[8, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 20) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 50) & (index_stat_year['增速变化幅度绝对值（%）'] <= 66.66)]['收益率（%）'].mean()
            index_prosperity_change.loc[9, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 0) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 66.66) & (index_stat_year['增速变化幅度绝对值（%）'] <= 100)]['收益率（%）'].mean()
            index_prosperity_change.loc[10, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 20) & (index_stat_year['上一年增速（%）'] <= 30) & (index_stat_year['本年增速（%）'] > 20) & (index_stat_year['本年增速（%）'] <= 30)]['收益率（%）'].mean()
            index_prosperity_change.loc[11, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 10) & (index_stat_year['上一年增速（%）'] <= 20) & (index_stat_year['本年增速（%）'] > 10) & (index_stat_year['本年增速（%）'] <= 20)]['收益率（%）'].mean()
            index_prosperity_change.loc[12, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 0) & (index_stat_year['上一年增速（%）'] <= 10) & (index_stat_year['本年增速（%）'] > 0) & (index_stat_year['本年增速（%）'] <= 10)]['收益率（%）'].mean()
            index_prosperity_change.loc[13, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 200) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change.loc[14, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 100) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change.loc[15, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
        index_prosperity_change['收益均值（%）'] = index_prosperity_change[sorted(index_stat['报告日期'].unique().tolist())].mean(axis=1)
        for col in sorted(index_stat['报告日期'].unique().tolist()) + ['收益均值（%）']:
            index_prosperity_change[col] = index_prosperity_change[col].apply(lambda x: round(x, 2))
        index_prosperity_change.columns = [col.replace('0331', 'Q1').replace('0630', 'Q2').replace('0930', 'Q3').replace('1231', 'Q4') for col in index_prosperity_change.columns]
        index_prosperity_change.to_excel('{0}growth/index_prosperity_change.xlsx'.format(self.data_path))
        # index_prosperity_change.to_excel('{0}growth/index_prosperity_change_excess.xlsx'.format(self.data_path))
        return

    def get_amt_prosperity_change_single_tianfeng(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_finance = self.index_finance.copy(deep=True)

        index_finance = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='NET_PROFIT_YOY')
        index_finance = index_finance.sort_index()
        index_finance = index_finance.unstack().reset_index()
        index_finance.columns = ['INDEX_SYMBOL', 'REPORT_DATE', 'NET_PROFIT_YOY_YEAR']
        index_finance['NET_PROFIT_YOY_LAST_YEAR'] = index_finance.groupby('INDEX_SYMBOL').apply(lambda x: x.sort_values('REPORT_DATE').shift(4))['NET_PROFIT_YOY_YEAR']
        index_finance['NET_PROFIT_YOY_DELTA'] = (index_finance['NET_PROFIT_YOY_YEAR'] - index_finance['NET_PROFIT_YOY_LAST_YEAR']) / abs(index_finance['NET_PROFIT_YOY_LAST_YEAR']) * 100.0
        index_finance['NET_PROFIT_YOY_DELTA_ABS'] = index_finance['NET_PROFIT_YOY_DELTA'].abs()
        # index_finance = index_finance[index_finance['INDEX_SYMBOL'] != '881001.WI']
        index_daily_k = index_daily_k[index_daily_k['TRADE_DATE'].isin([index_daily_k['TRADE_DATE'].min()] + index_finance['TRADE_DATE'].unique().tolist())]
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX')
        index_daily_k = index_daily_k.sort_index()
        index_daily_k = index_daily_k.pct_change().dropna() * 100.0
        # index_daily_k = index_daily_k[[col for col in (index_daily_k.columns) if col != '881001.WI'] + ['881001.WI']]
        # index_daily_k = index_daily_k.apply(lambda x: x[:-1] - x[-1], axis=1)
        index_daily_k = index_daily_k.unstack().reset_index()
        index_daily_k.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'RET']
        index_stat = index_finance.merge(index_daily_k, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').dropna()
        index_stat = index_stat[['INDEX_SYMBOL', 'REPORT_DATE', 'NET_PROFIT_YOY_LAST_YEAR', 'NET_PROFIT_YOY_YEAR', 'NET_PROFIT_YOY_DELTA', 'NET_PROFIT_YOY_DELTA_ABS', 'RET']]
        index_stat.columns = ['代码', '报告日期', '上一年增速（%）', '本年增速（%）', '增速变化幅度（%）', '增速变化幅度绝对值（%）', '收益率（%）']
        # 持续高增长
        index_prosperity_change_list = []
        for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
            # if index == '881001.WI':
            #     continue
            index_prosperity_change = pd.DataFrame(index=range(16), columns=['代码', '增长类型', '上一年增速（%）', '本年增速（%）', '增速变化幅度（%）'] + sorted(index_stat['报告日期'].unique().tolist()))
            index_prosperity_change['代码'] = index
            index_prosperity_change['增长类型'] = pd.Series(['持续高增长'] * 3 + ['加速增长'] * 3 + ['减速增长'] * 4 + ['低速稳定'] * 3 + ['困境反转'] * 3)
            index_prosperity_change['上一年增速（%）'] = pd.Series(['>100', '50-100', '30-50', '>100', '50-100', '30-50', '>60', '>60', '>60', '>60', '20-30', '10-20', '0-10', '<-100', '<-100', '<-100'])
            index_prosperity_change['本年增速（%）'] = pd.Series(['>100', '50-100', '30-50', '>100', '>50', '>30', '>40', '>30', '>20', '>0', '20-30', '10-20', '0-10', '>200', '>100', '>50'])
            index_prosperity_change['增速变化幅度（%）'] = pd.Series(['无要求', '无要求', '无要求', '加速', '加速', '加速', '减速（0-1/3）', '减速（1/3-1/2）', '减速（1/2-2/3）', '减速（2/3-1）', '无要求', '无要求', '无要求', '加速', '加速', '加速'])
            index_stat_index = index_stat[index_stat['代码'] == index]
            for year in index_stat['报告日期'].unique().tolist():
                index_stat_year = index_stat_index[index_stat_index['报告日期'] == year]
                index_prosperity_change.loc[0, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 100) & (index_stat_year['本年增速（%）'] > 100)]['收益率（%）'].mean()
                index_prosperity_change.loc[1, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 50) & (index_stat_year['上一年增速（%）'] <= 100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['本年增速（%）'] <= 100)]['收益率（%）'].mean()
                index_prosperity_change.loc[2, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 30) & (index_stat_year['上一年增速（%）'] <= 50) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['本年增速（%）'] <= 50)]['收益率（%）'].mean()
                index_prosperity_change.loc[3, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 100) & (index_stat_year['本年增速（%）'] > 100) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
                index_prosperity_change.loc[4, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 50) & (index_stat_year['上一年增速（%）'] <= 100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
                index_prosperity_change.loc[5, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 30) & (index_stat_year['上一年增速（%）'] <= 50) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
                index_prosperity_change.loc[6, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 40) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 0) & (index_stat_year['增速变化幅度绝对值（%）'] <= 33.33)]['收益率（%）'].mean()
                index_prosperity_change.loc[7, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 30) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 33.33) & (index_stat_year['增速变化幅度绝对值（%）'] <= 50)]['收益率（%）'].mean()
                index_prosperity_change.loc[8, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 20) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 50) & (index_stat_year['增速变化幅度绝对值（%）'] <= 66.66)]['收益率（%）'].mean()
                index_prosperity_change.loc[9, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 60) & (index_stat_year['本年增速（%）'] > 0) & (index_stat_year['增速变化幅度（%）'] < 0) & (index_stat_year['增速变化幅度绝对值（%）'] > 66.66) & (index_stat_year['增速变化幅度绝对值（%）'] <= 100)]['收益率（%）'].mean()
                index_prosperity_change.loc[10, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 20) & (index_stat_year['上一年增速（%）'] <= 30) & (index_stat_year['本年增速（%）'] > 20) & (index_stat_year['本年增速（%）'] <= 30)]['收益率（%）'].mean()
                index_prosperity_change.loc[11, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 10) & (index_stat_year['上一年增速（%）'] <= 20) & (index_stat_year['本年增速（%）'] > 10) & (index_stat_year['本年增速（%）'] <= 20)]['收益率（%）'].mean()
                index_prosperity_change.loc[12, year] = index_stat_year[(index_stat_year['上一年增速（%）'] > 0) & (index_stat_year['上一年增速（%）'] <= 10) & (index_stat_year['本年增速（%）'] > 0) & (index_stat_year['本年增速（%）'] <= 10)]['收益率（%）'].mean()
                index_prosperity_change.loc[13, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 200) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
                index_prosperity_change.loc[14, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 100) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
                index_prosperity_change.loc[15, year] = index_stat_year[(index_stat_year['上一年增速（%）'] < -100) & (index_stat_year['本年增速（%）'] > 50) & (index_stat_year['增速变化幅度（%）'] > 0)]['收益率（%）'].mean()
            index_prosperity_change['收益均值（%）'] = index_prosperity_change[sorted(index_stat['报告日期'].unique().tolist())].mean(axis=1)
            for col in sorted(index_stat['报告日期'].unique().tolist()) + ['收益均值（%）']:
                index_prosperity_change[col] = index_prosperity_change[col].apply(lambda x: round(x, 2))
            index_prosperity_change.columns = [col.replace('0331', 'Q1').replace('0630', 'Q2').replace('0930', 'Q3').replace('1231', 'Q4') for col in index_prosperity_change.columns]
            index_prosperity_change_list.append(index_prosperity_change)
        index_prosperity_chang_single = pd.concat(index_prosperity_change_list)
        index_prosperity_chang_single['展示名称'] = index_prosperity_chang_single['代码'].apply(lambda x: self.indexs_names_dic[x])
        index_prosperity_chang_single = index_prosperity_chang_single.set_index('展示名称').reset_index()
        index_prosperity_chang_single.to_excel('{0}growth/index_prosperity_chang_single.xlsx'.format(self.data_path))
        # index_prosperity_chang_single.to_excel('{0}growth/index_prosperity_chang_single_excess.xlsx'.format(self.data_path))
        return

    def get_amt_pb_roe_group(self):
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k_bmk = index_daily_k[index_daily_k['INDEX_SYMBOL'] == '881001.WI']

        factor_list = self.factor_list
        index_prosperity = self.index_finance.copy(deep=True)
        index_prosperity = index_prosperity[index_prosperity['INDEX_SYMBOL'] != '881001.WI']
        factor_name_dict = self.factor_name_dict
        window = 1

        index_data_list = []
        for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
            if index == '881001.WI':
                continue
            index_factor_data_list = []
            for factor in factor_list:
                index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
                index_pe_ttm_index = index_pe_ttm_index[['INDEX_SYMBOL', 'TRADE_DATE', 'PE_TTM']]
                # index_pe_ttm_index['PE_TTM_Q1'] = index_pe_ttm_index['PE_TTM'].quantile(0.33)
                # index_pe_ttm_index['PE_TTM_Q2'] = index_pe_ttm_index['PE_TTM'].quantile(0.67)
                # index_pe_ttm_index['PE_TTM_Q'] = index_pe_ttm_index.apply(lambda x: '低' if x['PE_TTM'] <= x['PE_TTM_Q1'] else '高' if x['PE_TTM'] >= x['PE_TTM_Q2'] else '中', axis=1)
                index_pe_ttm_index['PE_TTM_Q50'] = index_pe_ttm_index['PE_TTM'].quantile(0.5)
                index_pe_ttm_index['PE_TTM_Q'] = index_pe_ttm_index.apply(lambda x: '低' if x['PE_TTM'] <= x['PE_TTM_Q50'] else '高', axis=1)
                index_pe_ttm_index['YEAR_MONTH'] = index_pe_ttm_index['TRADE_DATE'].apply(lambda x: x[:6])
                index_pe_ttm_index['MONTH'] = index_pe_ttm_index['TRADE_DATE'].apply(lambda x: x[4:6])
                index_pe_ttm_index = index_pe_ttm_index.drop_duplicates('YEAR_MONTH', keep='last')
                index_pe_ttm_index = index_pe_ttm_index.loc[index_pe_ttm_index['MONTH'].isin(['03', '06', '09', '12'])]
                index_prosperity_index = index_prosperity[index_prosperity['INDEX_SYMBOL'] == index].sort_values('REPORT_DATE')
                index_prosperity_index = index_prosperity_index[index_prosperity_index['TRADE_DATE'] <= '20220331']
                index_prosperity_index = index_prosperity_index[['INDEX_SYMBOL', 'TRADE_DATE', factor]].rename(columns={factor: 'PROSPERITY'})
                # index_prosperity_index['PROSPERITY'] = index_prosperity_index['PROSPERITY'].pct_change()
                index_prosperity_index = index_prosperity_index.dropna()
                if len(index_prosperity_index) == 0:
                    continue
                # index_prosperity_index['PROSPERITY_Q1'] = index_prosperity_index['PROSPERITY'].quantile(0.33)
                # index_prosperity_index['PROSPERITY_Q2'] = index_prosperity_index['PROSPERITY'].quantile(0.67)
                # index_prosperity_index['PROSPERITY_Q'] = index_prosperity_index.apply(lambda x: '低' if x['PROSPERITY'] <= x['PROSPERITY_Q1'] else '高' if x['PROSPERITY'] >= x['PROSPERITY_Q2'] else '中', axis=1)
                index_prosperity_index['PROSPERITY_Q50'] = index_prosperity_index['PROSPERITY'].quantile(0.5)
                index_prosperity_index['PROSPERITY_Q'] = index_prosperity_index.apply(lambda x: '低' if x['PROSPERITY'] <= x['PROSPERITY_Q50'] else '高', axis=1)
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
                index_daily_k_index = index_daily_k_index[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX']]
                index_daily_k_index['YEAR_MONTH'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[:6])
                index_daily_k_index['MONTH'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[4:6])
                index_daily_k_index = index_daily_k_index.drop_duplicates('YEAR_MONTH', keep='last')
                index_daily_k_index = index_daily_k_index.loc[index_daily_k_index['MONTH'].isin(['03', '06', '09', '12'])]
                index_daily_k_index = index_daily_k_index.merge(index_daily_k_bmk[['TRADE_DATE', 'CLOSE_INDEX']].rename(columns={'CLOSE_INDEX': 'CLOSE_INDEX_BMK'}), on=['TRADE_DATE'], how='left')
                # index_daily_k_index['RET'] = index_daily_k_index['CLOSE_INDEX'].pct_change(window).shift(-window)
                index_daily_k_index['RET'] = index_daily_k_index['CLOSE_INDEX'].pct_change(window).shift(-window) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(window).shift(-window)
                index_factor_data = index_pe_ttm_index.merge(index_prosperity_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
                index_factor_data = index_factor_data[['PE_TTM_Q', 'PROSPERITY_Q', 'RET']].groupby(['PE_TTM_Q', 'PROSPERITY_Q']).mean().reset_index()
                index_factor_data = index_factor_data.pivot(index='PE_TTM_Q', columns='PROSPERITY_Q', values='RET')
                # index_factor_data = index_factor_data.T.reindex(['低', '中', '高']).reset_index()
                # index_factor_data['指标'] = factor_name_dict[factor]
                # index_factor_data = index_factor_data.set_index(['指标', 'PROSPERITY_Q']).T.reindex(['低', '中', '高'])
                index_factor_data = index_factor_data.T.reindex(['低', '高']).reset_index()
                index_factor_data['指标'] = factor_name_dict[factor]
                index_factor_data = index_factor_data.set_index(['指标', 'PROSPERITY_Q']).T.reindex(['低', '高'])
                index_factor_data_list.append(index_factor_data)
            index_data = pd.concat(index_factor_data_list, axis=1) if len(index_factor_data_list) > 0 else pd.DataFrame()
            index_data_list.append(index_data)
        index_group = pd.concat(index_data_list)
        # index_group.to_excel('{0}group/factor.xlsx'.format(self.data_path))
        # index_group.to_excel('{0}group/factor.xlsx'.format(self.data_path))
        index_group.to_excel('{0}group/factor_excess_class2_q{1}.xlsx'.format(self.data_path, window))
        # index_group.to_excel('{0}group/con_factor_excess_class2_q{1}.xlsx'.format(self.data_path, window))
        return

    def get_amt_pb_roe_factor(self):
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k_bmk = index_daily_k[index_daily_k['INDEX_SYMBOL'] == '881001.WI']

        factor_list = self.factor_list
        index_prosperity = self.index_finance.copy(deep=True)
        index_prosperity = index_prosperity[index_prosperity['INDEX_SYMBOL'] != '881001.WI']
        factor_name_dict = self.factor_name_dict
        window = 1

        corr_df = pd.DataFrame(index=self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist(), columns=factor_list)
        factor_data_list = []
        for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
            if index == '881001.WI':
                continue
            index_factor_data_list = []
            for factor in factor_list:
                index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
                index_pe_ttm_index = index_pe_ttm_index[['INDEX_SYMBOL', 'TRADE_DATE', 'PE_TTM']]
                index_pe_ttm_index['IDX'] = range(len(index_pe_ttm_index))
                index_pe_ttm_index['PE_TTM_QUANTILE'] = index_pe_ttm_index['IDX'].rolling(window=len(index_pe_ttm_index), min_periods=1, center=False).apply(lambda x: quantile_definition('PE_TTM', x, index_pe_ttm_index))
                index_prosperity_index = index_prosperity[index_prosperity['INDEX_SYMBOL'] == index].sort_values('REPORT_DATE')
                index_prosperity_index = index_prosperity_index[['INDEX_SYMBOL', 'TRADE_DATE', factor]].dropna().rename(columns={factor: 'PROSPERITY'})
                index_prosperity_index['IDX'] = range(len(index_prosperity_index))
                index_prosperity_index['PROSPERITY_QUANTILE'] = index_prosperity_index['IDX'].rolling(window=len(index_pe_ttm_index), min_periods=1, center=False).apply(lambda x: quantile_definition('PROSPERITY', x, index_prosperity_index))
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
                index_daily_k_index = index_daily_k_index[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX']]
                index_daily_k_index['YEAR_MONTH'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[:6])
                index_daily_k_index['MONTH'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: x[4:6])
                index_daily_k_index = index_daily_k_index.drop_duplicates('YEAR_MONTH', keep='last')
                index_daily_k_index = index_daily_k_index.loc[index_daily_k_index['MONTH'].isin(['03', '06', '09', '12'])]
                index_daily_k_index = index_daily_k_index.merge(index_daily_k_bmk[['TRADE_DATE', 'CLOSE_INDEX']].rename(columns={'CLOSE_INDEX': 'CLOSE_INDEX_BMK'}), on=['TRADE_DATE'], how='left')
                index_daily_k_index['RET'] = index_daily_k_index['CLOSE_INDEX'].pct_change(window).shift(-window) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(window).shift(-window)
                index_factor_data = index_prosperity_index[['INDEX_SYMBOL', 'TRADE_DATE', 'PROSPERITY_QUANTILE']].merge(index_pe_ttm_index[['INDEX_SYMBOL', 'TRADE_DATE', 'PE_TTM_QUANTILE']], on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').merge(index_daily_k_index[['INDEX_SYMBOL', 'TRADE_DATE', 'RET']], how='left')
                index_factor_data['FACTOR'] = index_factor_data['PROSPERITY_QUANTILE'] - index_factor_data['PE_TTM_QUANTILE']
                index_factor_data = index_factor_data.dropna()
                index_factor_data_list.append(index_factor_data[['INDEX_SYMBOL', 'TRADE_DATE', 'FACTOR']].rename(columns={'FACTOR': factor}).set_index(['INDEX_SYMBOL', 'TRADE_DATE']))
                if len(index_factor_data) <= 2:
                    continue
                corr = round(np.corrcoef(index_factor_data['FACTOR'], index_factor_data['RET'])[0, 1], 2)
                corr_df.loc[index, factor] = corr
            factor_data_list.append(pd.concat(index_factor_data_list, axis=1).reset_index())

        corr_df = corr_df.reset_index()
        corr_df.columns = ['代码'] + [factor_name_dict[col] for col in list(corr_df.columns)[1:]]
        indexs_corr = self.indexs.merge(corr_df, on=['代码'], how='left')
        indexs_corr.to_excel('{0}pb_roe_corr/factor_corr_q{1}.xlsx'.format(self.data_path, window))
        # indexs_corr.to_excel('{0}pb_roe_corr/con_factor_corr_q{1}.xlsx'.format(self.data_path, window))

        factor_data = pd.concat(factor_data_list)
        factor_data.to_excel('{0}pb_roe_corr/factor_data.xlsx'.format(self.data_path))
        # factor_data.to_excel('{0}pb_roe_corr/con_factor_data.xlsx'.format(self.data_path))
        return

    def get_amt_pb_roe_prosperity_factor(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index().reset_index()
        index_daily_k['YEAR_MONTH'] = index_daily_k['TRADE_DATE'].apply(lambda x: x[:6])
        index_daily_k['MONTH'] = index_daily_k['TRADE_DATE'].apply(lambda x: x[4:6])
        index_daily_k = index_daily_k.drop_duplicates('YEAR_MONTH', keep='last')
        index_daily_k = index_daily_k.loc[index_daily_k['MONTH'].isin(['03', '06', '09', '12'])]
        index_daily_k = index_daily_k.drop(['YEAR_MONTH', 'MONTH'], axis=1).set_index('TRADE_DATE')
        index_daily_k = index_daily_k[[col for col in (index_daily_k.columns) if col != '881001.WI'] + ['881001.WI']]
        index_daily_k = index_daily_k.pct_change(1).shift(-1).dropna() * 100.0
        index_daily_k = index_daily_k.apply(lambda x: x[:-1] - x[-1], axis=1)
        index_daily_k = index_daily_k.unstack().reset_index()
        index_daily_k.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'FORWARD_RET']
        index_factor = pd.read_excel('{0}pb_roe_prosperity/factor_data.xlsx'.format(self.data_path), index_col=0)
        index_factor['TRADE_DATE'] = index_factor['TRADE_DATE'].astype(str)
        index_factor = index_factor.rename(columns=self.factor_name_dict)
        index_con_factor = pd.read_excel('{0}pb_roe_prosperity/con_factor_data.xlsx'.format(self.data_path), index_col=0)
        index_con_factor['TRADE_DATE'] = index_con_factor['TRADE_DATE'].astype(str)
        index_con_factor = index_con_factor.rename(columns=self.con_factor_name_dict)
        index_factor = index_factor.merge(index_con_factor, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
        index_factor['REPORT_DATE'] = index_factor['TRADE_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')
        index_corr = pd.read_excel('{0}pb_roe_prosperity/excess_corr.xlsx'.format(self.data_path))
        # index_corr = pd.read_excel('{0}pb_roe_prosperity/decay_excess_corr.xlsx'.format(self.data_path))
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        index_prosperity_list = []
        index_prosperity_corr = pd.DataFrame(index=self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist(), columns=['PROSPERITY_IC'])
        new_line_color_list = []
        for idx, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            if index == '881001.WI':
                continue
            index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
            index_factor_index = index_factor[index_factor['INDEX_SYMBOL'] == index]
            index_corr_index = index_corr[index_corr['代码'] == index]
            index_factor_list = index_corr_index.T.iloc[4:].astype(float)
            index_factor_list.columns = ['CORR']
            index_factor_list = index_factor_list[index_factor_list['CORR'] > 0.3].index.tolist()
            if len(index_factor_list) == 0:
                continue
            index_factor_index['PROSPERITY'] = index_factor_index[index_factor_list].mean(axis=1)
            index_factor_index = index_factor_index[['INDEX_SYMBOL', 'TRADE_DATE', 'REPORT_DATE', 'PROSPERITY']]
            index_factor_index = index_factor_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='inner').sort_values('TRADE_DATE')
            index_prosperity_list.append(index_factor_index)
            corr = round(np.corrcoef(index_factor_index.dropna()['PROSPERITY'], index_factor_index.dropna()['FORWARD_RET'])[0, 1], 2)
            index_prosperity_corr.loc[index, 'PROSPERITY_IC'] = corr
            new_line_color_list.append(line_color_list[idx])
            sns.lineplot(ax=ax1, x='REPORT_DATE', y='PROSPERITY', data=index_factor_index, color=line_color_list[idx])
            ax1.set_xlabel('')
            ax1.set_ylabel('估值景气指标', fontsize=10)
            ax1.set_ylim([-200.0, 100.0])
        index_prosperity = pd.concat(index_prosperity_list)
        index_prosperity['板块'] = index_prosperity['INDEX_SYMBOL'].apply(lambda x: self.indexs_names_dic[x])
        index_order = [self.indexs_names_dic[x] for x in index_prosperity['INDEX_SYMBOL'].unique().tolist()]
        sns.barplot(ax=ax2, x='REPORT_DATE', y='FORWARD_RET', data=index_prosperity, hue='板块', hue_order=index_order, palette=new_line_color_list)
        ax2.set_xlabel('')
        ax2.set_ylabel('下一季度收益', fontsize=10)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax2.set_ylim([-30.0, 120.0])
        ax2.legend(loc=2)
        plt.tight_layout()
        plt.savefig('{0}pb_roe_prosperity/excess_prosperity.png'.format(self.data_path))
        # plt.savefig('{0}pb_roe_prosperity/decay_excess_prosperity.png'.format(self.data_path))
        index_prosperity.to_excel('{0}pb_roe_prosperity/excess_prosperity.xlsx'.format(self.data_path))
        # index_prosperity.to_excel('{0}pb_roe_prosperity/decay_excess_prosperity.xlsx'.format(self.data_path))
        index_prosperity_corr = index_prosperity_corr.reset_index()
        index_prosperity_corr.columns = ['代码', '合成景气度指标IC']
        index_prosperity_corr = self.indexs[self.indexs['板块'] == '先进制造'].merge(index_prosperity_corr, on=['代码'], how='left')
        index_prosperity_corr.to_excel('{0}pb_roe_prosperity/excess_prosperity_corr.xlsx'.format(self.data_path))
        # index_prosperity_corr.to_excel('{0}pb_roe_prosperity/decay_excess_prosperity_corr.xlsx'.format(self.data_path))
        return

    def get_amt_pe_group(self):
        # 不同估值水平下未来收益情况
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k_bmk = index_daily_k[index_daily_k['INDEX_SYMBOL'] == '881001.WI']
        for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE').dropna(subset=['PE_TTM'])
            index_pe_ttm_index['PE_TTM_Q'] = index_pe_ttm_index.apply(lambda x: (1.0 - np.count_nonzero(x['PE_TTM'] <= index_pe_ttm_index['PE_TTM']) / len(index_pe_ttm_index)) * 100.0, axis=1)
            index_pe_ttm_index['PE_TTM_Q'] = (index_pe_ttm_index['PE_TTM_Q'] / 10).astype(int) + 1
            index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
            index_daily_k_index = index_daily_k_index.merge(index_daily_k_bmk[['TRADE_DATE', 'CLOSE_INDEX']].rename(columns={'CLOSE_INDEX': 'CLOSE_INDEX_BMK'}), on=['TRADE_DATE'], how='left')
            index_daily_k_index['RET_FQ1'] = index_daily_k_index['CLOSE_INDEX'].pct_change(60).shift(-60)
            index_daily_k_index['RET_FQ2'] = index_daily_k_index['CLOSE_INDEX'].pct_change(120).shift(-120)
            index_daily_k_index['RET_FQ3'] = index_daily_k_index['CLOSE_INDEX'].pct_change(180).shift(-180)
            index_daily_k_index['RET_FQ4'] = index_daily_k_index['CLOSE_INDEX'].pct_change(250).shift(-250)
            index_daily_k_index['EXCESS_RET_FQ1'] = index_daily_k_index['CLOSE_INDEX'].pct_change(60).shift(-60) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(60).shift(-60)
            index_daily_k_index['EXCESS_RET_FQ2'] = index_daily_k_index['CLOSE_INDEX'].pct_change(120).shift(-120) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(120).shift(-120)
            index_daily_k_index['EXCESS_RET_FQ3'] = index_daily_k_index['CLOSE_INDEX'].pct_change(180).shift(-180) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(180).shift(-180)
            index_daily_k_index['EXCESS_RET_FQ4'] = index_daily_k_index['CLOSE_INDEX'].pct_change(250).shift(-250) - index_daily_k_index['CLOSE_INDEX_BMK'].pct_change(250).shift(-250)
            index_data = index_pe_ttm_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')

            index_data_fq_list = []
            for i in [1, 2, 3, 4]:
                index_data_fq = index_data[['INDEX_SYMBOL', 'PE_TTM', 'PE_TTM_Q', 'RET_FQ{0}'.format(i)]].rename(columns={'RET_FQ{0}'.format(i): 'RET_FQ'})
                index_data_fq['FQ'] = '未来一个季度收益' if i == 1 else '未来两个季度收益' if i == 2 else '未来三个季度收益' if i == 3 else '未来四个季度收益'
                index_data_fq_list.append(index_data_fq)
            index_data_fq = pd.concat(index_data_fq_list)
            index_data_fq['PE_TTM'] = filter_extreme_mad(index_data_fq['PE_TTM'])
            index_data_fq_mean = index_data_fq[['INDEX_SYMBOL', 'PE_TTM_Q', 'FQ', 'RET_FQ']].groupby(['INDEX_SYMBOL', 'FQ', 'PE_TTM_Q']).mean().reset_index().rename(columns={'RET_FQ': 'RET_FQ_MEAN'})
            index_data_fq_median = index_data_fq[['INDEX_SYMBOL', 'PE_TTM_Q', 'FQ', 'RET_FQ']].groupby(['INDEX_SYMBOL', 'FQ', 'PE_TTM_Q']).median().reset_index().rename(columns={'RET_FQ': 'RET_FQ_MEDIAN'})
            # 未来收益
            plt.subplots(figsize=(6, 6))
            sns.lmplot(x='PE_TTM', y='RET_FQ', data=index_data_fq, hue='FQ', ci=0, legend=False, scatter=True, scatter_kws={'s': 1}, palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM')
            plt.ylabel('未来收益')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_group/pe_ret_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))
            # 未来收益均值
            plt.subplots(figsize=(6, 6))
            sns.barplot(x='PE_TTM_Q', y='RET_FQ_MEAN', data=index_data_fq_mean, hue='FQ', hue_order=['未来一个季度收益', '未来两个季度收益', '未来三个季度收益', '未来四个季度收益'], palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM分组')
            plt.ylabel('未来收益均值')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_group/pe_ret_mean_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))
            # 未来收益中位数
            plt.subplots(figsize=(6, 6))
            sns.barplot(x='PE_TTM_Q', y='RET_FQ_MEDIAN', data=index_data_fq_median, hue='FQ', hue_order=['未来一个季度收益', '未来两个季度收益', '未来三个季度收益', '未来四个季度收益'], palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM分组')
            plt.ylabel('未来收益中位数')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pe_group/pe_ret_median_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))

            index_data_fq_list = []
            for i in [1, 2, 3, 4]:
                index_data_fq = index_data[['INDEX_SYMBOL', 'PE_TTM', 'PE_TTM_Q', 'EXCESS_RET_FQ{0}'.format(i)]].rename(columns={'EXCESS_RET_FQ{0}'.format(i): 'EXCESS_RET_FQ'})
                index_data_fq['FQ'] = '未来一个季度超额收益' if i == 1 else '未来两个季度超额收益' if i == 2 else '未来三个季度超额收益' if i == 3 else '未来四个季度超额收益'
                index_data_fq_list.append(index_data_fq)
            index_data_fq = pd.concat(index_data_fq_list)
            index_data_fq['PE_TTM'] = filter_extreme_mad(index_data_fq['PE_TTM'])
            index_data_fq_mean = index_data_fq[['INDEX_SYMBOL', 'PE_TTM_Q', 'FQ', 'EXCESS_RET_FQ']].groupby(['INDEX_SYMBOL', 'FQ', 'PE_TTM_Q']).mean().reset_index().rename(columns={'EXCESS_RET_FQ': 'EXCESS_RET_FQ_MEAN'})
            index_data_fq_median = index_data_fq[['INDEX_SYMBOL', 'PE_TTM_Q', 'FQ', 'EXCESS_RET_FQ']].groupby(['INDEX_SYMBOL', 'FQ', 'PE_TTM_Q']).median().reset_index().rename(columns={'EXCESS_RET_FQ': 'EXCESS_RET_FQ_MEDIAN'})
            # 未来收益
            plt.subplots(figsize=(6, 6))
            sns.lmplot(x='PE_TTM', y='EXCESS_RET_FQ', data=index_data_fq, hue='FQ', ci=0, legend=False, scatter=True, scatter_kws={'s': 1}, palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM')
            plt.ylabel('未来超额收益')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}scenario/pe/pe_excess_ret_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))
            # 未来收益均值
            plt.subplots(figsize=(6, 6))
            sns.barplot(x='PE_TTM_Q', y='EXCESS_RET_FQ_MEAN', data=index_data_fq_mean, hue='FQ', hue_order=['未来一个季度超额收益', '未来两个季度超额收益', '未来三个季度超额收益', '未来四个季度超额收益'], palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM分组')
            plt.ylabel('未来超额收益均值')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}scenario/pe/pe_excess_ret_mean_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))
            # 未来收益中位数
            plt.subplots(figsize=(6, 6))
            sns.barplot(x='PE_TTM_Q', y='EXCESS_RET_FQ_MEDIAN', data=index_data_fq_median, hue='FQ', hue_order=['未来一个季度超额收益', '未来两个季度超额收益', '未来三个季度超额收益', '未来四个季度超额收益'], palette=line_color_list)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.xlabel('PE_TTM分组')
            plt.ylabel('未来超额收益中位数')
            plt.legend(loc=2)
            plt.title(self.indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}scenario/pe/pe_excess_ret_median_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))

    def get_line(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_finance = self.index_finance.copy(deep=True)
        index_consensus = self.index_consensus.copy(deep=True)
        index_finance = index_finance.merge(index_consensus, on=['INDEX_SYMBOL', 'REPORT_DATE', 'TRADE_DATE'])
        for index in self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist():
            index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
            index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index].sort_values('TRADE_DATE')
            index_daily_k_index = index_daily_k_index[index_daily_k_index['TRADE_DATE'] <= '20220630']
            index_pe_ttm_index = index_pe_ttm_index[index_pe_ttm_index['TRADE_DATE'] <= '20220630']
            index_finance_index = index_finance_index[index_finance_index['TRADE_DATE'] <= '20220630']
            index_daily_k_index['TRADE_DATE'] = index_daily_k_index['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
            index_pe_ttm_index['TRADE_DATE'] = index_pe_ttm_index['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())
            index_finance_index['TRADE_DATE'] = index_finance_index['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())

            temp_list = []
            for i, factor in enumerate(['NET_PROFIT_YOY', 'ROE_Q', 'ROE_YOY', 'CON_NET_PROFIT_YOY', 'CON_ROE_FY1', 'CON_ROE_YOY']):
                temp = index_finance_index[['INDEX_SYMBOL', 'REPORT_DATE', 'TRADE_DATE', factor]].rename(columns={factor: 'FACTOR'})
                temp['TYPE'] = self.factor_name_dict[factor] if i < 3 else self.con_factor_name_dict[factor]
                temp_list.append(temp)
            index_finance_index = pd.concat(temp_list)

            fig, ax = plt.subplots(2, 1, figsize=(12, 12))
            ax0, ax1 = ax[0], ax[1]
            ax0_r = ax[0].twinx()
            sns.lineplot(ax=ax0, x='TRADE_DATE', y='CLOSE_INDEX', data=index_daily_k_index, label='指数点位', color=line_color_list[0])
            sns.lineplot(ax=ax0_r, x='TRADE_DATE', y='PE_TTM', data=index_pe_ttm_index, label='PE_TTM', color=line_color_list[1])
            ax0.set_xlabel('')
            ax0.set_ylabel('指数点位')
            ax0_r.set_ylabel('PE_TTM')
            ax0.legend(loc=2)
            ax0_r.legend(loc=1)
            ax0.set_title(self.indexs_names_dic[index])
            sns.barplot(ax=ax1, x='TRADE_DATE', y='FACTOR', data=index_finance_index, hue='TYPE', palette=line_color_list)
            ax1.set_xticklabels(labels=index_finance_index['REPORT_DATE'].unique().tolist(), rotation=90)
            ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax1.set_xlabel('')
            ax1.set_ylabel('财务指标')
            ax1.legend(loc=2)
            plt.savefig('{0}line/line_{1}.png'.format(self.data_path, self.indexs_names_dic[index]))

    def combine_factor(self):
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        index_daily_k = index_daily_k[index_daily_k.index.isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        n = 1
        index_daily_k = index_daily_k.pct_change(n).shift(-n).dropna() * 100.0
        index_daily_k = index_daily_k[[col for col in (index_daily_k.columns) if col != '881001.WI'] + ['881001.WI']]
        index_daily_k = index_daily_k.apply(lambda x: x[:-1] - x[-1], axis=1)
        index_daily_k = index_daily_k.unstack().reset_index()
        index_daily_k.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'FORWARD_RET']
        index_prosperity = pd.read_excel('{0}prosperity/excess_prosperity_{1}q.xlsx'.format(self.data_path, n), index_col=0)
        index_prosperity['REPORT_DATE'] = index_prosperity['REPORT_DATE'].astype(str)
        index_prosperity['TRADE_DATE'] = index_prosperity['TRADE_DATE'].astype(str)
        index_pe_ttm = self.index_valuation.copy(deep=True)

        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        index_factor_list = []
        index_factor_corr = pd.DataFrame(index=self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist(), columns=['IC'])
        new_line_color_list = []
        for idx, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            if index == '881001.WI' or index not in index_prosperity['INDEX_SYMBOL'].unique().tolist():
                continue
            index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index][['INDEX_SYMBOL', 'TRADE_DATE', 'FORWARD_RET']].sort_values('TRADE_DATE').dropna()
            index_prosperity_index = index_prosperity[index_prosperity['INDEX_SYMBOL'] == index][['INDEX_SYMBOL', 'REPORT_DATE', 'TRADE_DATE', 'PROSPERITY']].sort_values('TRADE_DATE').dropna()
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index][['INDEX_SYMBOL', 'TRADE_DATE', 'PE_TTM']].sort_values('TRADE_DATE').dropna()

            # 合成方式一：
            # index_prosperity_index['PROSPERITY_Q'] = index_prosperity_index.apply(lambda x: (1.0 - np.count_nonzero(x['PROSPERITY'] <= index_prosperity_index['PROSPERITY']) / len(index_prosperity_index)) * 100.0, axis=1)
            # index_pe_ttm_index['PE_TTM_Q'] = index_pe_ttm_index.apply(lambda x: (1.0 - np.count_nonzero(x['PE_TTM'] <= index_pe_ttm_index['PE_TTM']) / len(index_pe_ttm_index)) * 100.0, axis=1)
            # index_factor_index = index_prosperity_index.merge(index_pe_ttm_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
            # index_factor_index['FACTOR'] = index_factor_index['PROSPERITY_Q'] - index_factor_index['PE_TTM_Q']
            # 合成方式二：
            # index_factor_index = index_prosperity_index.merge(index_pe_ttm_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
            # index_factor_index['PROSPERITY'] = (index_factor_index['PROSPERITY'] - index_factor_index['PROSPERITY'].mean()) / index_factor_index['PROSPERITY'].std()
            # index_factor_index['PE_TTM'] = (index_factor_index['PE_TTM'] - index_factor_index['PE_TTM'].mean()) / index_factor_index['PE_TTM'].std()
            # index_factor_index['FACTOR'] = 0.5 * index_factor_index['PROSPERITY'] - 0.5 *index_factor_index['PE_TTM']
            # 合成方式三：
            index_factor_index = index_prosperity_index.merge(index_pe_ttm_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left').merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
            index_factor_index['PROSPERITY'] = (index_factor_index['PROSPERITY'] - index_factor_index['PROSPERITY'].mean()) / index_factor_index['PROSPERITY'].std()
            index_factor_index['PE_TTM'] = (index_factor_index['PE_TTM'] - index_factor_index['PE_TTM'].mean()) / index_factor_index['PE_TTM'].std()
            index_factor_index['FACTOR'] = 0.75 * index_factor_index['PROSPERITY'] - 0.25 *index_factor_index['PE_TTM']

            index_factor_list.append(index_factor_index)
            corr = round(np.corrcoef(index_factor_index.dropna()['FACTOR'], index_factor_index.dropna()['FORWARD_RET'])[0, 1], 2)
            index_factor_corr.loc[index, 'IC'] = corr
            new_line_color_list.append(line_color_list[idx])
            sns.lineplot(ax=ax1, x='REPORT_DATE', y='FACTOR', data=index_factor_index, color=line_color_list[idx])
            ax1.set_xlabel('')
            ax1.set_ylabel('估值-景气度指标', fontsize=16)
            ax1.set_ylim([-7.0, 5.0])  # [-200.0, 100.0], [-7.0, 5.0]
        index_factor = pd.concat(index_factor_list)
        index_factor['板块'] = index_factor['INDEX_SYMBOL'].apply(lambda x: self.indexs_names_dic[x])
        index_order = [self.indexs_names_dic[x] for x in index_factor['INDEX_SYMBOL'].unique().tolist()]
        sns.barplot(ax=ax2, x='REPORT_DATE', y='FORWARD_RET', data=index_prosperity, hue='板块', hue_order=index_order, palette=new_line_color_list)
        ax2.set_xlabel('')
        ax2.set_ylabel('未来{0}个季度超额收益'.format('一' if n == 1 else '两'if n == 2 else '三' if n == 3 else '四'), fontsize=16)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax2.set_ylim([-30.0, 120.0])
        ax2.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=9)
        plt.title('估值-景气度指标与未来{0}个季度超额收益'.format('一' if n == 1 else '两' if n == 2 else '三' if n == 3 else '四'), fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}factor/factor_3_{1}q.png'.format(self.data_path, n))
        index_factor.to_excel('{0}factor/factor_3_{1}q.xlsx'.format(self.data_path, n))
        index_factor_corr = index_factor_corr.reset_index()
        index_factor_corr.columns = ['代码', '合成景气度指标IC']
        index_factor_corr = self.indexs[self.indexs['板块'] == '先进制造'].merge(index_factor_corr, on=['代码'], how='left')
        index_factor_corr.to_excel('{0}factor/factor_3_corr_{1}q.xlsx'.format(self.data_path, n))
        return


    def get_amt_results(self):
        self.get_amt_ret()
        self.get_amt_valuation()
        self.get_amt_prosperity()
        self.get_amt_con_prosperity()
        self.get_amt_prosperity_factor()
        self.get_amt_pb_roe()
        self.get_amt_prosperity_tianfeng()
        self.get_amt_prosperity_change_tianfeng()
        self.get_amt_prosperity_change_single_tianfeng()
        self.get_amt_pb_roe_group()
        self.get_amt_pb_roe_factor()
        self.get_amt_pb_roe_prosperity_factor()
        self.get_amt_pe_group()
        self.get_line()
        self.combine_factor()


class IndustryPrediction:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = TimeDateUtil.convert_format(self.start_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.end_date_hyphen = TimeDateUtil.convert_format(self.end_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.data_path = data_path
        self.pv_factor = ['M6422131', 'S0270092', 'U5508992', 'S0270496', 'S5804302', 'S5119573', 'C5553658']
        self.pv_factor_dict = {'M6422131': '产量:太阳能电池', 'S0270092': '出口数量:太阳能电池', 'U5508992': '出口数量:单晶硅切片', 'S0270496': '进口数量:多晶硅', 'S5804302': '进口数量:银粉', 'S5119573': '发电新增设备容量:太阳能', 'C5553658': '出口数量:逆变器'}
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        # self.pv_factor_data = w.edb(",".join(self.pv_factor), self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        # self.pv_factor_data.to_hdf('{0}pv_factor_data.hdf'.format(self.data_path), key='table', mode='w')
        self.pv_factor_data = pd.read_hdf('{0}pv_factor_data.hdf'.format(self.data_path), key='table')
        self.pv_factor_data.columns = ['时间'] + [self.pv_factor_dict[col] for col in list(self.pv_factor_data.columns)[1:]]
        self.pv_factor_data['时间'] = self.pv_factor_data['时间'].apply(lambda x: str(x).replace('-', ''))
        self.pv_factor_data = self.pv_factor_data.sort_values('时间')
        self.pv_factor_data['发电新增设备容量:太阳能'] = self.pv_factor_data['发电新增设备容量:太阳能'].diff()
        self.pv_factor_data = self.pv_factor_data.set_index('时间')
        return

    def get_data_process(self):
        pv_factor_data = self.pv_factor_data.fillna(method='ffill')
        pv_factor_data = pv_factor_data.rolling(12).mean()
        pv_factor_data = (pv_factor_data - pv_factor_data.mean()) / pv_factor_data.std(ddof=1)
        pv_factor_data = pv_factor_data.dropna(how='all').sort_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        for i, factor in enumerate(list(pv_factor_data.columns)):
            ax.plot(pv_factor_data.index, pv_factor_data[factor].values, color=line_color_list[i], label=factor)
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.3), ncol=4)
        plt.xticks(rotation=45)
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=False, left=False)
        plt.savefig('{0}factor.png'.format(self.data_path))
        return

    def get_pca_model(self):
        from sklearn.decomposition import PCA
        model = PCA()

        factor = pd.DataFrame(index=list(self.pv_factor_data[self.pv_factor_data.index >= '20190131'].index), columns=['FACTOR'])
        for date in list(self.pv_factor_data[self.pv_factor_data.index >= '20190131'].index):
            if date < '20210131':
                pv_factor_data = self.pv_factor_data.drop('进口数量:多晶硅', axis=1)
            else:
                pv_factor_data = self.pv_factor_data.copy(deep=True)
            pv_factor_data_date = pv_factor_data[pv_factor_data.index <= date]
            pv_factor_data_date = pv_factor_data_date.fillna(method='ffill')
            pv_factor_data_date = pv_factor_data_date.rolling(12).mean()
            pv_factor_data_date = pv_factor_data_date.dropna().iloc[-6:]
            pv_factor_data_date = (pv_factor_data_date - pv_factor_data_date.mean()) / pv_factor_data_date.std(ddof=1)
            model.fit(pv_factor_data_date.values)
            score = PCA(1).fit_transform(pv_factor_data_date)[-1][0]
            factor.loc[date, 'FACTOR'] = score
        factor['FACTOR_DIFF'] = factor['FACTOR'].diff()
        factor = factor.dropna()
        factor['884045_isin'] = factor['FACTOR_DIFF'] >= 0
        factor['881001_isin'] = factor['FACTOR_DIFF'] <= 0
        factor['884045_isin'] = factor['884045_isin'].astype(int)
        factor['881001_isin'] = factor['881001_isin'].astype(int)
        factor = factor.merge(self.calendar_trade_df.set_index('CALENDAR_DATE'), left_index=True, right_index=True, how='left')

        main_income_yoy = w.wsd('884045.WI', "yoy_or", self.start_date_hyphen, self.end_date_hyphen, "unit=1;rptType=1;Period=Q;Days=Alldays", usedf=True)[1].reset_index()
        main_income_yoy.columns = ['REPORT_DATE', 'MAIN_INCOME_YOY']
        main_income_yoy['REPORT_DATE'] = main_income_yoy['REPORT_DATE'].apply(lambda x: x.strftime('%Y%m%d'))
        main_income_yoy = main_income_yoy.sort_values('REPORT_DATE')
        main_income_yoy = main_income_yoy.set_index('REPORT_DATE')

        factor_miy = factor.merge(main_income_yoy, left_index=True, right_index=True, how='left').dropna()
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.plot(factor_miy.index, factor_miy['MAIN_INCOME_YOY'].values, color=line_color_list[0], label='光伏板块营业收入增速')
        ax2.plot(factor_miy.index, factor_miy['FACTOR'].values, color=line_color_list[1], label='光伏产业综合景气指标（右轴）')
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.xticks(rotation=45)
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=False, left=False)
        plt.savefig('{0}factor_miy.png'.format(self.data_path))

        daily_k = w.wsd('884045.WI,881001.WI', "close", self.start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
        daily_k.columns = ['TRADE_DATE', '884045', '881001']
        daily_k['TRADE_DATE'] = daily_k['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d'))
        daily_k = daily_k.sort_values('TRADE_DATE')
        daily_k = daily_k.set_index('TRADE_DATE')
        daily_ret = daily_k.pct_change().dropna()
        daily_ret = daily_ret.merge(factor[['TRADE_DATE', '884045_isin', '881001_isin']].set_index('TRADE_DATE'), left_index=True, right_index=True, how='left')
        daily_ret = daily_ret.fillna(method='ffill')
        daily_ret['884045_isin'] = daily_ret['884045_isin'].shift()
        daily_ret['881001_isin'] = daily_ret['881001_isin'].shift()
        daily_ret = daily_ret.dropna()

        daily_ret_1 = daily_ret.copy(deep=True)
        daily_ret_1['RET'] = daily_ret_1['884045'] * daily_ret_1['884045_isin'] + daily_ret_1['881001'] * daily_ret_1['881001_isin']
        daily_ret_1 = daily_ret_1[['RET', '884045', '881001']]
        daily_ret_1.iloc[0] = 0.0
        daily_ret_1 = (daily_ret_1 + 1.0).cumprod()
        daily_ret_1.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), daily_ret_1.index)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_ret_1.index, daily_ret_1['RET'].values, color=line_color_list[0], label='策略')
        ax.plot(daily_ret_1.index, daily_ret_1['884045'].values, color=line_color_list[1], label='光伏指数')
        ax.plot(daily_ret_1.index, daily_ret_1['881001'].values, color=line_color_list[2], label='万得全A')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=True, left=False)
        plt.savefig('{0}result_1.png'.format(self.data_path))

        daily_ret_2 = daily_ret.copy(deep=True)
        daily_ret_2['RET'] = daily_ret_2['884045'] * daily_ret_2['884045_isin']
        daily_ret_2 = daily_ret_2[['RET', '884045', '881001']]
        daily_ret_2.iloc[0] = 0.0
        daily_ret_2 = (daily_ret_2 + 1.0).cumprod()
        daily_ret_2.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), daily_ret_2.index)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_ret_2.index, daily_ret_2['RET'].values, color=line_color_list[0], label='策略')
        ax.plot(daily_ret_2.index, daily_ret_2['884045'].values, color=line_color_list[1], label='光伏指数')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=True, left=False)
        plt.savefig('{0}result_2.png'.format(self.data_path))
        return

    def get_amt_results(self):
        self.get_data_process()
        self.get_pca_model()
        return


if __name__ == '__main__':
    start_date = '20190101'
    end_date = '20230106'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/'
    PeTracking(start_date, end_date, data_path).get_amt_results()
    IndustryTracking(start_date, end_date, data_path).get_amt_results()
    IndustryPrediction(start_date, end_date, data_path).get_amt_results()