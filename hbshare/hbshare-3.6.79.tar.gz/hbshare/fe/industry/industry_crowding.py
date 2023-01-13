# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import numpy as np
import pandas as pd
import os

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

from matplotlib.ticker import FuncFormatter
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C', '#44488E', '#BA67E9', '#3FAEEE',
                   '#DC494F', '#9EA2C9', '#CBCBCB', '#5A5A63', '#F8B399', '#B074D1', '#C8A060', '#1C26CE', '#CB96E9', '#AFDEFA']


def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'


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

class Crowding:
    def __init__(self, index, index_name_dic, start_date, end_date, data_path):
        self.index = index
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.end_date_hyphen = datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.data_path = data_path
        self.index_name_dic = index_name_dic
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date((datetime.strptime(self.start_date, '%Y%m%d') - timedelta(20)).strftime('%Y%m%d'), self.end_date)

        # 指数收盘点位、成交额、换手率、主动资金净流入
        self.index_data = w.wsd(self.index, "close,amt,turn,mfd_inflow_m", self.start_date_hyphen, self.end_date_hyphen, "unit=1", usedf=True)[1].reset_index()
        self.index_data.to_hdf('{0}{1}.hdf'.format(self.data_path, self.index), key='table', mode='w')
        self.index_data = pd.read_hdf('{0}{1}.hdf'.format(self.data_path, self.index), key='table')
        self.index_data.columns = ['TRADE_DATE', 'CLOSE_INDEX', 'TURNOVER_VALUE', 'TURNOVER_RATE', 'MF_NET_INFLOW']
        self.index_data['INDEX_SYMBOL'] = self.index
        self.index_data['TRADE_DATE'] = self.index_data['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_data = self.index_data[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX', 'TURNOVER_VALUE', 'TURNOVER_RATE', 'MF_NET_INFLOW']]
        self.index_data = self.index_data.sort_values('TRADE_DATE')

        # 市场收盘点位、成交额、换手率、主动资金净流入
        self.index_market_data = w.wsd("881001.WI", "close,amt,turn,mfd_inflow_m", self.start_date_hyphen, self.end_date_hyphen, "unit=1", usedf=True)[1].reset_index()
        self.index_market_data.to_hdf('{0}{1}.hdf'.format(self.data_path, '881001.WI'), key='table', mode='w')
        self.index_market_data = pd.read_hdf('{0}{1}.hdf'.format(self.data_path, '881001.WI'), key='table')
        self.index_market_data.columns = ['TRADE_DATE', 'CLOSE_INDEX', 'TURNOVER_VALUE', 'TURNOVER_RATE', 'MF_NET_INFLOW']
        self.index_market_data['INDEX_SYMBOL'] = '881001.WI'
        self.index_market_data['TRADE_DATE'] = self.index_market_data['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        self.index_market_data = self.index_market_data[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX', 'TURNOVER_VALUE', 'TURNOVER_RATE', 'MF_NET_INFLOW']]
        self.index_market_data = self.index_market_data.sort_values('TRADE_DATE')

        # 指数成分股（每季度更新）
        index_cons_list = []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            date_hyphen = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
            index_cons_date = w.wset("sectorconstituent", "date={0};windcode={1}".format(date_hyphen, self.index), usedf=True)[1]
            index_cons_list.append(index_cons_date)
        self.index_cons = pd.concat(index_cons_list)
        self.index_cons.to_hdf('{0}{1}_cons.hdf'.format(self.data_path, self.index), key='table', mode='w')
        self.index_cons = pd.read_hdf('{0}{1}_cons.hdf'.format(self.data_path, self.index), key='table')
        self.index_cons.columns = ['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME']
        self.index_cons['INDEX_SYMBOL'] = self.index
        self.index_cons['TRADE_DATE'] = self.index_cons['TRADE_DATE'].apply(lambda x: str(x.date()).replace('-', ''))
        self.index_cons['TICKER_SYMBOL'] = self.index_cons['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.index_cons = self.index_cons[['INDEX_SYMBOL', 'TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME']]
        self.index_cons = self.index_cons.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.index_cons['IS_CON'] = 1
        self.index_cons = self.index_cons.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='IS_CON').sort_index().fillna(0.0)
        self.index_cons = self.trade_df[['TRADE_DATE']].set_index('TRADE_DATE').merge(self.index_cons, left_index=True, right_index=True, how='left')
        self.index_cons = self.index_cons.fillna(method='ffill').dropna()

        # 股票行情
        stock_daily_k_path = '{0}stock_daily_k.hdf'.format(self.data_path)
        if os.path.isfile(stock_daily_k_path):
            existed_stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
            max_date = max(existed_stock_daily_k['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_daily_k = pd.DataFrame()
            start_date = '20150101'
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_daily_k_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_daily_k_date = HBDB().read_stock_daily_k_given_date(date)
            stock_daily_k_date = stock_daily_k_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE']] if len(stock_daily_k_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE'])
            star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(date)
            star_stock_daily_k_date = star_stock_daily_k_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE']] if len(star_stock_daily_k_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE'])
            stock_daily_k_date = pd.concat([stock_daily_k_date, star_stock_daily_k_date])
            stock_daily_k_list.append(stock_daily_k_date)
            print(date)
        self.stock_daily_k = pd.concat([existed_stock_daily_k] + stock_daily_k_list, ignore_index=True)
        self.stock_daily_k = self.stock_daily_k.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_daily_k = self.stock_daily_k.reset_index().drop('index', axis=1)
        self.stock_daily_k.to_hdf(stock_daily_k_path, key='table', mode='w')
        self.stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
        self.stock_daily_k = self.stock_daily_k.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_daily_k = self.stock_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE').sort_index()
        self.stock_daily_k_max = self.stock_daily_k.rolling(60).max()
        self.stock_new_high = (self.stock_daily_k >= self.stock_daily_k_max).astype(int)
        self.stock_daily_k_mean = self.stock_daily_k.rolling(20).mean()
        self.stock_mean_above = (self.stock_daily_k > self.stock_daily_k_mean).astype(int)

    def quantile_definition(self, col, idxs, daily_df):
        part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
        q = (1.0 - np.count_nonzero(part_df[col].iloc[-1] <= part_df[col]) / len(part_df))
        return q

    def get_crowding(self):
        index_data = self.index_data.merge(self.index_market_data[['TRADE_DATE', 'TURNOVER_VALUE']].rename(columns={'TURNOVER_VALUE': 'TURNOVER_VALUE_MARKET'}), on=['TRADE_DATE'], how='left')
        index_data['TURNOVER_VALUE_RATE'] = index_data['TURNOVER_VALUE'] / index_data['TURNOVER_VALUE_MARKET']
        index_data['MF_NET_INFLOW_RATE'] = index_data['MF_NET_INFLOW'] / index_data['TURNOVER_VALUE']
        stock_new_high = (self.stock_new_high * self.index_cons).sum(axis=1) / self.index_cons.sum(axis=1)
        stock_new_high = pd.DataFrame(stock_new_high, columns=['NEW_HIGH']).reset_index()
        stock_mean_above = (self.stock_mean_above * self.index_cons).sum(axis=1) / self.index_cons.sum(axis=1)
        stock_mean_above = pd.DataFrame(stock_mean_above, columns=['MEAN_ABOVE']).reset_index()
        index_data = index_data.merge(stock_new_high, on=['TRADE_DATE'], how='left').merge(stock_mean_above, on=['TRADE_DATE'], how='left')
        index_data = index_data[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX', 'TURNOVER_VALUE_RATE', 'TURNOVER_RATE', 'MF_NET_INFLOW_RATE', 'NEW_HIGH', 'MEAN_ABOVE']]
        index_data = index_data.sort_values('TRADE_DATE')
        index_data['IDX'] = range(len(index_data))
        for col in list(index_data.columns)[3:]:
            index_data[col] = index_data['IDX'].rolling(window=250, min_periods=250, center=False).apply(lambda x: self.quantile_definition(col, x, index_data))
        index_data['CROWDING'] = index_data[list(index_data.columns)[3:]].mean(axis=1)
        index_data = index_data.dropna(subset=['CROWDING'])
        index_data['CROWDING_MEAN'] = index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).mean()
        index_data['CROWDING_UP1'] = index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).mean() + 1.0 * index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).std(ddof=1)
        index_data['CROWDING_DOWN1'] = index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).mean() - 1.0 * index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).std(ddof=1)
        index_data['CROWDING_UP15'] = index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).mean() + 1.5 * index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).std(ddof=1)
        index_data['CROWDING_DOWN15'] = index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).mean() - 1.5 * index_data['CROWDING'].rolling(window=250, min_periods=1, center=False).std(ddof=1)

        index_data_disp = index_data.merge(self.trade_df[['TRADE_DATE', 'IS_WEEK_END']], on=['TRADE_DATE'], how='left')
        index_data_disp = index_data_disp[index_data_disp['IS_WEEK_END'] == '1']
        index_data_disp = index_data_disp[index_data_disp['TRADE_DATE'] >= '20200101']
        index_data_disp['TRADE_DATE'] = index_data_disp['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        ax1 = ax
        ax2 = ax.twinx()
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING'].values, '-', linewidth=3.0, label='拥挤度指标', color=line_color_list[1])
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING_MEAN'].values, '--', label='均值', color=line_color_list[2])
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING_UP1'].values, '--', label='均值±1.0*标准差', color=line_color_list[7])
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING_UP15'].values, '--', label='均值±1.5*标准差', color=line_color_list[3])
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING_DOWN1'].values, '--', color=line_color_list[7])
        ax1.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CROWDING_DOWN15'].values, '--', color=line_color_list[3])
        ax2.plot(index_data_disp['TRADE_DATE'].values, index_data_disp['CLOSE_INDEX'].values, '-', linewidth=3.0, label=self.index_name_dic[self.index] + '（右轴）', color=line_color_list[0])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.15), ncol=5)
        ax1.set_ylim([0, 1.3])
        ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        plt.title('{0}拥挤度'.format(self.index_name_dic[self.index]))
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, self.index_name_dic[self.index]))
        return index_data


if __name__ == '__main__':
    start_date = '20180101'
    end_date = '20220930'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/crowding/'
    index_list = ['8841448.WI', '884963.WI', '884045.WI', '8841269.WI', '886032.WI', '884878.WI', '8841278.WI', '801740.SI']
    index_name_dic = {'8841448.WI': '先进制造', '884963.WI': '动力电池', '884045.WI': '光伏', '8841269.WI': '新能源整车',
                      '886032.WI': '汽车零部件', '884878.WI': '半导体', '8841278.WI': '消费电子', '801740.SI': '军工'}
    index_crowding_list = []
    for index in index_list:
        index_data = Crowding(index, index_name_dic, start_date, end_date, data_path).get_crowding()
        index_crowding_list.append(index_data)
    index_crowding = pd.concat(index_crowding_list)
    index_crowding.to_hdf('{0}index_crowding.hdf'.format(data_path), key='table', mode='w')
    index_crowding = pd.read_hdf('{0}index_crowding.hdf'.format(data_path), key='table')
    index_crowding = index_crowding.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CROWDING')
    index_crowding_up = index_crowding.rolling(window=250, min_periods=1, center=False).mean() + 1.0 * index_crowding.rolling(window=250, min_periods=1, center=False).std(ddof=1)
    index_crowding_down = index_crowding.rolling(window=250, min_periods=1, center=False).mean() - 1.0 * index_crowding.rolling(window=250, min_periods=1, center=False).std(ddof=1)
    index_relative_crowding = (index_crowding - index_crowding_down) / (index_crowding_up - index_crowding_down)
    index_relative_crowding_change = index_relative_crowding.pct_change(20)

    plt.figure(figsize=(6, 6))
    plt.scatter(index_relative_crowding.iloc[-1], index_relative_crowding_change.iloc[-1], color=line_color_list[1])
    for i in range(len(index_relative_crowding.iloc[-1])):
        plt.annotate([index_name_dic[index] for index in list(index_relative_crowding.iloc[-1].index)][i], xy=(index_relative_crowding.iloc[-1][i], index_relative_crowding_change.iloc[-1][i]), xytext=(index_relative_crowding.iloc[-1][i], index_relative_crowding_change.iloc[-1][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.xlabel('拥挤度相对水平')
    plt.ylabel('拥挤度相对水平近一月变化')
    plt.xlim([-1.5, 1.5])
    plt.ylim([-1.5, 1.5])
    plt.hlines(y=0, xmin=-1.5, xmax=1.5, linestyles='-', color='#959595')
    plt.vlines(x=0, ymin=-1.5, ymax=1.5, linestyles='-', color='#959595')
    plt.gca().xaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('先进制造各板块拥挤度情况')
    plt.tight_layout()
    plt.savefig('{0}拥挤度.png'.format(data_path))

