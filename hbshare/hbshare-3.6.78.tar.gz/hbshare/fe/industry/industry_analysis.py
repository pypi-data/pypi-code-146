# -*- coding: utf-8 -*-

from hbshare.fe.industry.industry_crowding import Crowding
from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
from scipy import stats
import os
import pandas as pd
import numpy as np

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C', '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
new_color_list = ['#F04950', '#959595', '#6268A2', '#333335', '#D57C56', '#628497']
industry_theme_dic = {'银行': '大金融', '非银金融': '大金融', '房地产': '大金融',
                      '食品饮料': '消费', '家用电器': '消费', '医药生物': '消费', '社会服务': '消费', '农林牧渔': '消费', '商贸零售': '消费', '美容护理': '消费',
                      '通信': 'TMT', '计算机': 'TMT', '电子': 'TMT', '传媒': 'TMT', '国防军工': 'TMT',
                      '交通运输': '制造', '机械设备': '制造', '汽车': '制造', '纺织服饰': '制造', '轻工制造': '制造', '电力设备': '制造',
                      '钢铁': '周期', '有色金属': '周期', '建筑装饰': '周期', '建筑材料': '周期', '基础化工': '周期', '石油石化': '周期', '煤炭': '周期', '公用事业': '周期', '环保': '周期',
                      '综合': '其他'}

def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def to_percent_r1(temp, position):
    return '%0.01f'%(temp) + '%'

def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'

def to_100percent_r1(temp, position):
    return '%0.01f'%(temp * 100) + '%'

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
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_industry.hdf', key='table')
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

def get_stock_info():
    stock_info = HBDB().read_stock_info()
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqjc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].dropna()
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info['SAMPLE_DATE'] = stock_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(365)).strftime('%Y%m%d'))
    return stock_info

class IndustryAnalysis:
    def __init__(self, start_date, end_date, last_report_date, report_date, con_date, sw_type, file_path, select_industry=[]):
        self.start_date = start_date
        self.end_date = end_date
        self.last_report_date = last_report_date
        self.report_date = report_date
        self.con_date = con_date
        self.sw_type = sw_type
        self.file_path = file_path + end_date
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        if len(select_industry) == 0:
            self.industry_info = get_industry_info()
            self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
            self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
            self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
            self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
            self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()
            self.select_industry = self.industry_info['INDUSTRY_NAME'].unique().tolist()
        else:
            self.select_industry = select_industry

    def IndustryMarketValue(self):
        ind_mv = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'MARKET_VALUE'], 'industry_technology', self.sw_type)
        ind_mv = ind_mv[ind_mv['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_mv['MARKET_VALUE'] = ind_mv['MARKET_VALUE'].apply(lambda x: round(x / 10000000000.0, 2))
        ind_mv = ind_mv.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values='MARKET_VALUE')
        date_list = sorted(list(ind_mv.columns))[-12:]
        rank_list = list(ind_mv[max(date_list)].sort_values(ascending=False).index)
        ind_mv = ind_mv.reset_index()
        ind_mv['INDUSTRY_NAME'] = ind_mv['INDUSTRY_NAME'].astype('category')
        ind_mv['INDUSTRY_NAME'].cat.reorder_categories(rank_list, inplace=True)
        ind_mv = ind_mv.sort_values('INDUSTRY_NAME')
        ind_mv = ind_mv.set_index('INDUSTRY_NAME')[date_list]

        plt.figure(figsize=(12, 8))
        sns.heatmap(ind_mv, annot=True, fmt='.2f', cmap='OrRd')
        plt.xlabel('')
        plt.ylabel('行业市值（百亿）')
        plt.tight_layout()
        plt.savefig('{0}/mv.png'.format(self.file_path))
        return

    def IndustryRet(self):
        ind_ret = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'RET'], 'industry_technology', self.sw_type)
        ind_ret = ind_ret[ind_ret['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_ret['RET'] = ind_ret['RET'].apply(lambda x: round(x * 100.0, 2))
        ind_ret = ind_ret.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values='RET')
        date_list = sorted(list(ind_ret.columns))[-12:]
        rank_list = list(ind_ret[max(date_list)].sort_values(ascending=False).index)
        ind_ret = ind_ret.reset_index()
        ind_ret['INDUSTRY_NAME'] = ind_ret['INDUSTRY_NAME'].astype('category')
        ind_ret['INDUSTRY_NAME'].cat.reorder_categories(rank_list, inplace=True)
        ind_ret = ind_ret.sort_values('INDUSTRY_NAME')
        ind_ret = ind_ret.set_index('INDUSTRY_NAME')[date_list]

        plt.figure(figsize=(12, 8))
        sns.heatmap(ind_ret, annot=True, fmt='.2f', cmap='OrRd')
        plt.xlabel('')
        plt.ylabel('行业季度涨跌幅（%）')
        plt.tight_layout()
        plt.savefig('{0}/ret.png'.format(self.file_path))
        return

    def IndustryTech(self):
        ind_tech = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'RET', 'VOL', 'BETA', 'ALPHA'], 'industry_technology', self.sw_type)
        ind_tech = ind_tech[ind_tech['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_tech['RET'] = ind_tech['RET'].apply(lambda x: round(x * 100.0, 2))
        ind_tech['VOL'] = ind_tech['VOL'].apply(lambda x: round(x * 100.0, 2))
        ind_tech['BETA'] = ind_tech['BETA'].apply(lambda x: round(x, 2))
        ind_tech['ALPHA'] = ind_tech['ALPHA'].apply(lambda x: round(x * 100.0, 2))

        fig, ax = plt.subplots(2, 2, figsize=(24, 16))
        tech_list = [['RET', 'VOL'], ['BETA', 'ALPHA']]
        for i in range(2):
            for j in range(2):
                ind_item = ind_tech.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values=tech_list[i][j])
                date_list = sorted(list(ind_item.columns))[-12:]
                rank_list = list(ind_item[max(date_list)].sort_values(ascending=False).index)
                ind_item = ind_item.reset_index()
                ind_item['INDUSTRY_NAME'] = ind_item['INDUSTRY_NAME'].astype('category')
                ind_item['INDUSTRY_NAME'].cat.reorder_categories(rank_list, inplace=True)
                ind_item = ind_item.sort_values('INDUSTRY_NAME')
                ind_item = ind_item.set_index('INDUSTRY_NAME')[date_list]
                ylabel = '涨跌幅（%）' if tech_list[i][j] == 'RET' else '波动率（%）' if tech_list[i][j] == 'VOL' else 'BETA' if tech_list[i][j] == 'BETA' else 'ALPHA（%）'
                axij = sns.heatmap(ind_item, ax=ax[i][j], annot=True, fmt='.2f', cmap='OrRd')
                axij.set_xlabel('')
                axij.set_ylabel(ylabel)
        plt.tight_layout()
        plt.savefig('{0}/tech.png'.format(self.file_path))
        return

    def IndustryNewhigh(self):
        calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df = get_date(self.last_report_date, self.report_date)
        trade_df = trade_df[(trade_df['TRADE_DATE'] > self.last_report_date) & (trade_df['TRADE_DATE'] <= self.report_date)]
        newhigh_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            print(date)
            newhigh = HBDB().read_stock_heightest_given_date(date)
            newhigh_star = HBDB().read_star_stock_heightest_given_date(date)
            newhigh = pd.concat([newhigh, newhigh_star])
            newhigh = newhigh.loc[newhigh['TICKER_SYMBOL'].str.len() == 6]
            newhigh = newhigh.loc[newhigh['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
            newhigh = newhigh[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'HIGHESTPRICE']].sort_values('TICKER_SYMBOL').reset_index().drop('index', axis=1)
            newhigh_list.append(newhigh)
        newhigh = pd.concat(newhigh_list)
        newhigh.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/newhigh_{0}.hdf'.format(self.report_date), key='table', mode='w')

        industry_symbol = get_industry_symbol()
        industry_symbol_sw1 = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == 1]
        industry_symbol_sw1 = industry_symbol_sw1[industry_symbol_sw1['IS_NEW'] == 1]
        industry_symbol_sw1 = industry_symbol_sw1[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        industry_symbol_sw2 = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == 2]
        industry_symbol_sw2 = industry_symbol_sw2[industry_symbol_sw2['IS_NEW'] == 1]
        industry_symbol_sw2 = industry_symbol_sw2[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        stock_industry = get_stock_industry()
        stock_industry_sw1 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
        stock_industry_sw1 = stock_industry_sw1[stock_industry_sw1['IS_NEW'] == 1]
        stock_industry_sw1 = stock_industry_sw1.drop('INDUSTRY_NAME', axis=1).merge(industry_symbol_sw1, on=['INDUSTRY_ID'], how='left')
        stock_industry_sw1 = stock_industry_sw1[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]
        stock_industry_sw2 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 2]
        stock_industry_sw2 = stock_industry_sw2[stock_industry_sw2['IS_NEW'] == 1]
        stock_industry_sw2 = stock_industry_sw2.drop('INDUSTRY_NAME', axis=1).merge(industry_symbol_sw2, on=['INDUSTRY_ID'], how='left')
        stock_industry_sw2 = stock_industry_sw2[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]
        stock_info = get_stock_info()

        newhigh = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/newhigh_{0}.hdf'.format(self.report_date), key='table')
        newhigh = newhigh.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        newhigh = newhigh.merge(stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        newhigh = newhigh[newhigh['TRADE_DATE'] >= newhigh['SAMPLE_DATE']]
        newhigh = newhigh.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'HIGHESTPRICE'])
        total_count = newhigh[['INDUSTRY_NAME', 'TICKER_SYMBOL']].drop_duplicates().groupby('INDUSTRY_NAME').count().reset_index().rename(columns={'TICKER_SYMBOL': 'TOTAL_COUNT'})
        newhigh = newhigh[newhigh['HIGHESTPRICE'] == 1]
        newhigh = newhigh.sort_values(['TICKER_SYMBOL', 'TRADE_DATE']).drop_duplicates('TICKER_SYMBOL', keep='first')
        ind_newhigh = newhigh[['INDUSTRY_NAME', 'HIGHESTPRICE']].groupby('INDUSTRY_NAME').count().reset_index().rename(columns={'HIGHESTPRICE': 'NEWHIGH_COUNT'})
        ind_newhigh = ind_newhigh.merge(total_count, on=['INDUSTRY_NAME'], how='inner')
        ind_newhigh['NEWHIGH_RATIO'] = ind_newhigh['NEWHIGH_COUNT'] / ind_newhigh['TOTAL_COUNT']
        ind_newhigh = ind_newhigh[ind_newhigh['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_newhigh = ind_newhigh.sort_values('NEWHIGH_RATIO', ascending=False)

        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.bar(ind_newhigh['INDUSTRY_NAME'].values, ind_newhigh['NEWHIGH_COUNT'].values, color=bar_color_list[0], label='创历史新高个股数量')
        ax2.plot(ind_newhigh['INDUSTRY_NAME'].values, ind_newhigh['NEWHIGH_RATIO'].values, color=bar_color_list[7], label='创历史新高个股比例（右轴）')
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.3), ncol=2)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        ax1.set_xticklabels(labels=ind_newhigh['INDUSTRY_NAME'].values, rotation=45)
        ax2.set_xticklabels(labels=ind_newhigh['INDUSTRY_NAME'].values, rotation=45)
        plt.title('创历史新高情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=False, left=False)
        plt.savefig('{0}/newhigh.png'.format(self.file_path))

        newhigh = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/newhigh_{0}.hdf'.format(self.report_date), key='table')
        newhigh = newhigh.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW1'}), on=['TICKER_SYMBOL'], how='inner')
        newhigh = newhigh.merge(stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW2'}), on=['TICKER_SYMBOL'], how='inner')
        newhigh = newhigh.merge(stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        newhigh = newhigh[newhigh['TRADE_DATE'] >= newhigh['SAMPLE_DATE']]
        newhigh = newhigh.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW2', 'HIGHESTPRICE'])

        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        ind_newhigh_select = ['电力设备', '汽车', '有色金属', '机械设备']
        newhigh_list = [[ind_newhigh_select[0], ind_newhigh_select[1]], [ind_newhigh_select[2], ind_newhigh_select[3]]]
        for i in range(2):
            for j in range(2):
                newhigh_sw2 = newhigh[newhigh['INDUSTRY_NAME_SW1'] == newhigh_list[i][j]]
                newhigh_sw2 = newhigh_sw2[newhigh_sw2['HIGHESTPRICE'] == 1]
                newhigh_sw2 = newhigh_sw2.sort_values(['TICKER_SYMBOL', 'TRADE_DATE']).drop_duplicates('TICKER_SYMBOL', keep='first')
                ind_newhigh_sw2 = newhigh_sw2[['INDUSTRY_NAME_SW2', 'TICKER_SYMBOL']].groupby('INDUSTRY_NAME_SW2').count().reset_index().rename(columns={'TICKER_SYMBOL': 'NEWHIGH_COUNT'})
                ind_newhigh_sw2 = ind_newhigh_sw2.sort_values('NEWHIGH_COUNT', ascending=False)
                ax[i][j].pie(ind_newhigh_sw2['NEWHIGH_COUNT'].values, labels=ind_newhigh_sw2['INDUSTRY_NAME_SW2'].values, autopct= '%0.1f%%', colors=line_color_list)
                ax[i][j].set_xlabel('')
                ax[i][j].set_ylabel('')
                ax[i][j].set_title(newhigh_list[i][j], fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        plt.savefig('{0}/newhigh_sw2.png'.format(self.file_path))
        return

    def IndustryVal(self):
        ind_pe = FEDB().read_industry_data(['TRADE_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM'], 'industry_daily_valuation', self.sw_type)
        ind_pe = ind_pe[ind_pe['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_pe_latest = ind_pe[ind_pe['TRADE_DATE'] == ind_pe['TRADE_DATE'].max()]
        ind_pe_min = ind_pe[['INDUSTRY_NAME', 'PE_TTM']].groupby('INDUSTRY_NAME').min().reset_index().rename(columns={'PE_TTM': 'PE_TTM_MIN'})
        ind_pe_mean = ind_pe[['INDUSTRY_NAME', 'PE_TTM']].groupby('INDUSTRY_NAME').mean().reset_index().rename(columns={'PE_TTM': 'PE_TTM_MEAN'})
        ind_pe_median = ind_pe[['INDUSTRY_NAME', 'PE_TTM']].groupby('INDUSTRY_NAME').median().reset_index().rename(columns={'PE_TTM': 'PE_TTM_MEDIAN'})
        ind_pe_max = ind_pe[['INDUSTRY_NAME', 'PE_TTM']].groupby('INDUSTRY_NAME').max().reset_index().rename(columns={'PE_TTM': 'PE_TTM_MAX'})
        ind_pe_quantile = ind_pe[['INDUSTRY_NAME', 'TRADE_DATE', 'PE_TTM']].groupby('INDUSTRY_NAME').apply(lambda x: (1.0 - np.count_nonzero(x.sort_values('TRADE_DATE')['PE_TTM'].iloc[-1] <= x['PE_TTM']) / x['PE_TTM'].size) * 100.0)
        ind_pe_quantile = pd.DataFrame(ind_pe_quantile).reset_index().rename(columns={0: 'PE_TTM_QUANTILE'})
        ind_pe_disp = ind_pe_latest.merge(ind_pe_min, on=['INDUSTRY_NAME'], how='left') \
                                   .merge(ind_pe_mean, on=['INDUSTRY_NAME'], how='left') \
                                   .merge(ind_pe_median, on=['INDUSTRY_NAME'], how='left') \
                                   .merge(ind_pe_max, on=['INDUSTRY_NAME'], how='left') \
                                   .merge(ind_pe_quantile, on=['INDUSTRY_NAME'], how='left')
        ind_pe_disp = ind_pe_disp.sort_values('PE_TTM_QUANTILE', ascending=False)
        for col in ['PE_TTM', 'PE_TTM_QUANTILE', 'PE_TTM_MIN', 'PE_TTM_MEAN', 'PE_TTM_MEDIAN', 'PE_TTM_MAX']:
            ind_pe_disp[col] = ind_pe_disp[col].apply(lambda x: round(x, 2))
        ind_pe_disp['PE_TTM_QUANTILE'] = ind_pe_disp['PE_TTM_QUANTILE'].apply(lambda x: '{0}%'.format(x))
        ind_pe_disp = ind_pe_disp[['INDUSTRY_NAME', 'PE_TTM_QUANTILE', 'PE_TTM', 'PE_TTM_MIN', 'PE_TTM_MEAN', 'PE_TTM_MEDIAN', 'PE_TTM_MAX']]
        ind_pe_disp.columns = ['行业名称', '分位水平', 'PE_TTM', '最小值', '平均值', '中位数', '最大值']
        ind_pe_disp.to_excel('{0}/pettm.xlsx'.format(self.file_path))

        ind_pe = ind_pe.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='PE_TTM').sort_index()
        ind_list = ind_pe_disp['行业名称'].unique().tolist()[::-1]
        ind_pe_list = [ind_pe[ind] for ind in ind_list]
        ind_pe_latest['INDUSTRY_NAME'] = ind_pe_latest['INDUSTRY_NAME'].astype('category')
        ind_pe_latest['INDUSTRY_NAME'].cat.reorder_categories(ind_list, inplace=True)
        ind_pe_latest = ind_pe_latest.sort_values('INDUSTRY_NAME')
        plt.figure(figsize=(12, 12))
        plt.boxplot(ind_pe_list, labels=ind_list, vert=False, patch_artist=True, boxprops={'color':'white', 'facecolor': bar_color_list[0]}, flierprops={'marker': 'o', 'markersize': 1}, meanline=True, showmeans=True, zorder=1)
        plt.scatter(ind_pe_latest['PE_TTM'], range(1, len(ind_pe_latest) + 1), marker='o', zorder=2)
        plt.tight_layout()
        plt.savefig('{0}/pettm.png'.format(self.file_path))

        # rank_list = [self.report_date, self.last_report_date]
        # ind_pe = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM'], 'industry_valuation', self.sw_type)
        # ind_pe = ind_pe[ind_pe['INDUSTRY_NAME'].isin(self.select_industry)]
        # ind_pe = ind_pe[ind_pe['REPORT_DATE'].isin(rank_list)]
        # ind_pe['PE_TTM'] = ind_pe['PE_TTM'].apply(lambda x: round(x, 2))
        # ind_pe = ind_pe.sort_values(['REPORT_DATE', 'PE_TTM'], ascending=[False, False])
        # ind_pe = ind_pe[['REPORT_DATE', 'INDUSTRY_NAME', 'PE_TTM']]
        # #####画柱状图#####
        # plt.figure(figsize=(12, 6))
        # sns.barplot(x='INDUSTRY_NAME', y='PE_TTM', data=ind_pe, hue='REPORT_DATE', hue_order=rank_list, palette=[bar_color_list[0], bar_color_list[7]])
        # plt.legend(loc=8, bbox_to_anchor=(0.5, -0.3), ncol=2)
        # plt.xlabel('')
        # plt.ylabel('')
        # plt.xticks(rotation=45)
        # plt.title('PE_TTM', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        # plt.tight_layout()
        # sns.despine(top=True, bottom=False, right=True, left=False)
        # plt.savefig('{0}/pettm_r2.png'.format(self.file_path))
        #
        # rank_list = [self.report_date, self.last_report_date]
        # ind_pb = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PB_LF'], 'industry_valuation', self.sw_type)
        # ind_pb = ind_pb[ind_pb['INDUSTRY_NAME'].isin(self.select_industry)]
        # ind_pb = ind_pb[ind_pb['REPORT_DATE'].isin(rank_list)]
        # ind_pb['PB_LF'] = ind_pb['PB_LF'].apply(lambda x: round(x, 2))
        # ind_pb = ind_pb.sort_values(['REPORT_DATE', 'PB_LF'], ascending=[False, False])
        # ind_pb = ind_pb[['REPORT_DATE', 'INDUSTRY_NAME', 'PB_LF']]
        # #####画柱状图#####
        # plt.figure(figsize=(12, 6))
        # sns.barplot(x='INDUSTRY_NAME', y='PB_LF', data=ind_pb, hue='REPORT_DATE', hue_order=rank_list, palette=[bar_color_list[0], bar_color_list[7]])
        # plt.legend(loc=8, bbox_to_anchor=(0.5, -0.3), ncol=2)
        # plt.xlabel('')
        # plt.ylabel('')
        # plt.xticks(rotation=45)
        # plt.title('PB_LF', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        # plt.tight_layout()
        # sns.despine(top=True, bottom=False, right=True, left=False)
        # plt.savefig('{0}/pblf_r2.png'.format(self.file_path))

        ind_val = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM', 'PB_LF'], 'industry_valuation', self.sw_type)
        ind_val = ind_val[ind_val['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_val['PE_TTM'] = ind_val['PE_TTM'].apply(lambda x: round(x, 2))
        ind_val['PB_LF'] = ind_val['PB_LF'].apply(lambda x: round(x, 2))
        #####画热力图#####
        fig, ax = plt.subplots(1, 2, figsize=(24, 8))
        val_list = ['PE_TTM', 'PB_LF']
        for i in range(2):
            ind_item = ind_val.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values=val_list[i])
            date_list = sorted(list(ind_item.columns))[-12:]
            rank_list = list(ind_item[max(date_list)].sort_values(ascending=False).index)
            ind_item = ind_item.reset_index()
            ind_item['INDUSTRY_NAME'] = ind_item['INDUSTRY_NAME'].astype('category')
            ind_item['INDUSTRY_NAME'].cat.reorder_categories(rank_list, inplace=True)
            ind_item = ind_item.sort_values('INDUSTRY_NAME')
            ind_item = ind_item.set_index('INDUSTRY_NAME')[date_list]
            axi = sns.heatmap(ind_item, ax=ax[i], annot=True, fmt='.2f', cmap='OrRd')
            axi.set_xlabel('')
            axi.set_ylabel(val_list[i])
        plt.tight_layout()
        plt.savefig('{0}/val.png'.format(self.file_path))
        return

    def IndustryFmt(self):
        date_list = ['20191231', '20201231', '20210331', '20210630', '20210930', '20211231', '20220331', '20220630', '20220930']
        ind_fmt = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'NET_PROFIT_ACCUM_YOY'], 'industry_fundamental_derive', self.sw_type)
        ind_fmt = ind_fmt[ind_fmt['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_fmt = ind_fmt[ind_fmt['REPORT_DATE'].isin(date_list)]
        ind_fmt = ind_fmt.pivot(index='INDUSTRY_NAME', columns='REPORT_DATE', values='NET_PROFIT_ACCUM_YOY').reset_index()
        ind_fmt['THEME'] = ind_fmt['INDUSTRY_NAME'].apply(lambda x: industry_theme_dic[x])
        ind_fmt['THEME'] = ind_fmt['THEME'].astype('category')
        ind_fmt['THEME'].cat.reorder_categories(['周期', '制造', '消费', '大金融', 'TMT', '其他'], inplace=True)
        ind_fmt = ind_fmt.sort_values(['THEME', self.report_date], ascending=[True, False])
        for date in date_list:
            ind_fmt[date] = ind_fmt[date].apply(lambda x: '{0}%'.format(round(x * 100.0, 2)))
        ind_fmt = ind_fmt[['THEME', 'INDUSTRY_NAME'] + date_list]
        ind_fmt.columns = ['主题', '行业', '2019A', '2020A', '2021Q1', '2021Q2', '2021Q3', '2021A', '2022Q1', '2022Q2', '2022Q3']
        ind_fmt.to_excel('{0}/net_profit_accum_yoy.xlsx'.format(self.file_path))

        for index_name in ['ROE_TTM', 'GROSS_INCOME_RATIO_TTM']:
            ylabel = 'ROE_TTM' if index_name == 'ROE_TTM' else '毛利率_TTM'
            rank_list = [self.report_date, self.last_report_date]
            ind_fmt = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', index_name], 'industry_fundamental', self.sw_type)
            ind_fmt = ind_fmt[ind_fmt['INDUSTRY_NAME'].isin(self.select_industry)]
            ind_fmt = ind_fmt[ind_fmt['REPORT_DATE'].isin(rank_list)]
            ind_fmt[index_name] = ind_fmt[index_name].apply(lambda x: round(x, 2))
            ind_fmt = ind_fmt[['REPORT_DATE', 'INDUSTRY_NAME', index_name]]
            ind_fmt_date = ind_fmt[ind_fmt['REPORT_DATE'] == self.report_date].rename(columns={index_name: self.report_date})
            ind_fmt_last_date = ind_fmt[ind_fmt['REPORT_DATE'] == self.last_report_date].rename(columns={index_name: self.last_report_date})
            ind_fmt = ind_fmt_date.merge(ind_fmt_last_date.drop('REPORT_DATE', axis=1), on=['INDUSTRY_NAME'], how='left')
            mom_abs = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', index_name + '_MOM_ABS'], 'industry_fundamental_derive', self.sw_type)
            mom_abs = mom_abs[mom_abs['INDUSTRY_NAME'].isin(self.select_industry)]
            mom_abs = mom_abs[mom_abs['REPORT_DATE'].isin([self.report_date])]
            mom_abs[index_name + '_MOM_ABS'] = mom_abs[index_name + '_MOM_ABS'].apply(lambda x: round(x, 2))
            mom_abs = mom_abs[['REPORT_DATE', 'INDUSTRY_NAME', index_name + '_MOM_ABS']]
            ind_fmt = ind_fmt.merge(mom_abs.drop('REPORT_DATE', axis=1), on=['INDUSTRY_NAME'], how='left')
            ind_fmt = ind_fmt.sort_values(self.report_date, ascending=False)
            yoy = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', index_name + '_YOY'], 'industry_fundamental_derive', self.sw_type)
            yoy = yoy[yoy['INDUSTRY_NAME'].isin(self.select_industry)]
            yoy = yoy[yoy['REPORT_DATE'].isin([self.report_date])]
            yoy[index_name + '_YOY'] = yoy[index_name + '_YOY'].apply(lambda x: round(x * 100.0, 2))
            yoy = yoy[['REPORT_DATE', 'INDUSTRY_NAME', index_name + '_YOY']]
            ind_fmt = ind_fmt.merge(yoy.drop('REPORT_DATE', axis=1), on=['INDUSTRY_NAME'], how='left')
            ind_fmt = ind_fmt.sort_values(self.report_date, ascending=False)

            fig, ax = plt.subplots(2, 1, figsize=(12, 6))
            bar_width = 0.3
            ax[0].bar(np.arange(len(ind_fmt)) - 0.5 * bar_width, ind_fmt[self.report_date].values, bar_width, label=self.report_date, color=bar_color_list[0])
            ax[0].bar(np.arange(len(ind_fmt)) + 0.5 * bar_width,  ind_fmt[self.last_report_date].values, bar_width, label=self.last_report_date, color=bar_color_list[7])
            ax[1].bar(np.arange(len(ind_fmt)), ind_fmt[index_name + '_YOY'].values, bar_width, label='{0}同比增长率'.format(self.report_date), color=bar_color_list[14])
            h1, l1 = ax[0].get_legend_handles_labels()
            h2, l2 = ax[1].get_legend_handles_labels()
            plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.45), ncol=3)
            ax[0].set_xticks(np.arange(len(ind_fmt)))
            ax[0].set_xticklabels(labels=[''] * len(ind_fmt), rotation=45)
            ax[1].set_xticks(np.arange(len(ind_fmt)))
            ax[1].set_xticklabels(labels=ind_fmt['INDUSTRY_NAME'].unique().tolist(), rotation=45)
            ax[0].yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax[1].yaxis.set_major_formatter(FuncFormatter(to_percent))
            ax[0].set_xlabel('')
            ax[1].set_xlabel('')
            ax[0].set_ylabel('')
            ax[1].set_ylabel('')
            ax[0].set_title(ylabel + '及同比增长情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
            plt.tight_layout()
            sns.despine(ax=ax[0], top=True, right=True, left=False, bottom=True)
            sns.despine(ax=ax[1], top=True, right=True, left=False, bottom=False)
            plt.savefig('{0}/{1}.png'.format(self.file_path, index_name.lower()))
        return

    def IndustryCon(self):
        ind_con_sw1 = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'EXCEED_RATIO_NEW'], 'industry_consensus', 1)
        ind_con_sw1 = ind_con_sw1[ind_con_sw1['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_con_sw1 = ind_con_sw1[ind_con_sw1['REPORT_DATE'] == self.con_date]
        ind_con_sw1['EXCEED_RATIO_NEW'] = ind_con_sw1['EXCEED_RATIO_NEW'].apply(lambda x: round(x * 100.0, 2))
        ind_con_sw1 = ind_con_sw1.sort_values('EXCEED_RATIO_NEW', ascending=False)
        ind_con_sw1 = ind_con_sw1[['REPORT_DATE', 'INDUSTRY_NAME', 'EXCEED_RATIO_NEW']]

        plt.figure(figsize=(12, 6))
        sns.barplot(x='INDUSTRY_NAME', y='EXCEED_RATIO_NEW', data=ind_con_sw1, palette=[bar_color_list[0]])
        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(rotation=45)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('超预期个股占比', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, bottom=False, right=True, left=False)
        plt.savefig('{0}/exceed.png'.format(self.file_path))

        industry_symbol = get_industry_symbol()
        industry_symbol_sw1 = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == 1]
        industry_symbol_sw1 = industry_symbol_sw1[industry_symbol_sw1['IS_NEW'] == 1]
        industry_symbol_sw1 = industry_symbol_sw1[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        industry_symbol_sw2 = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == 2]
        industry_symbol_sw2 = industry_symbol_sw2[industry_symbol_sw2['IS_NEW'] == 1]
        industry_symbol_sw2 = industry_symbol_sw2[['INDUSTRY_ID', 'INDUSTRY_NAME']]
        stock_industry = get_stock_industry()
        stock_industry_sw1 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
        stock_industry_sw1 = stock_industry_sw1[stock_industry_sw1['IS_NEW'] == 1]
        stock_industry_sw1 = stock_industry_sw1.drop('INDUSTRY_NAME', axis=1).merge(industry_symbol_sw1, on=['INDUSTRY_ID'], how='left')
        stock_industry_sw1 = stock_industry_sw1[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]
        stock_industry_sw2 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 2]
        stock_industry_sw2 = stock_industry_sw2[stock_industry_sw2['IS_NEW'] == 1]
        stock_industry_sw2 = stock_industry_sw2.drop('INDUSTRY_NAME', axis=1).merge(industry_symbol_sw2, on=['INDUSTRY_ID'], how='left')
        stock_industry_sw2 = stock_industry_sw2[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]
        stock_industry_sw1 = stock_industry_sw1.rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW1'})
        stock_industry_sw2 = stock_industry_sw2.rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW2'})
        stock_industry = stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME_SW1']].drop_duplicates().merge(stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME_SW2']].drop_duplicates(), on=['TICKER_SYMBOL'], how='left')

        ind_con_sw2 = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'EXCEED_RATIO_NEW'], 'industry_consensus', 2)
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        ind_con_top4 = ind_con_sw1['INDUSTRY_NAME'].unique().tolist()[:4]
        ind_con_list = [[ind_con_top4[0], ind_con_top4[1]], [ind_con_top4[2], ind_con_top4[3]]]
        for i in range(2):
            for j in range(2):
                ind_sw2 = ind_con_sw2[ind_con_sw2['INDUSTRY_NAME'].isin(stock_industry[stock_industry['INDUSTRY_NAME_SW1'] == ind_con_list[i][j]]['INDUSTRY_NAME_SW2'].unique().tolist())]
                ind_sw2 = ind_sw2[ind_sw2['REPORT_DATE'] == self.con_date]
                ind_sw2['EXCEED_RATIO_NEW'] = ind_sw2['EXCEED_RATIO_NEW'].apply(lambda x: round(x * 100.0, 2))
                ind_sw2 = ind_sw2.sort_values('EXCEED_RATIO_NEW', ascending=False)
                ind_sw2 = ind_sw2[['REPORT_DATE', 'INDUSTRY_NAME', 'EXCEED_RATIO_NEW']]
                ax[i][j].pie(ind_sw2['EXCEED_RATIO_NEW'].values, labels=ind_sw2['INDUSTRY_NAME'].values, autopct='%0.2f%%', colors=line_color_list)
                ax[i][j].set_xlabel('')
                ax[i][j].set_ylabel('')
                ax[i][j].set_title(ind_con_list[i][j], fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        plt.savefig('{0}/exceed_sw2.png'.format(self.file_path))

        rank_list = [self.report_date, self.last_report_date]
        ind_con = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'EST_NET_PROFIT_FY1'], 'industry_consensus', self.sw_type)
        ind_con = ind_con[ind_con['INDUSTRY_NAME'].isin(self.select_industry)]
        ind_con = ind_con[ind_con['REPORT_DATE'].isin(rank_list)]
        ind_con['EST_NET_PROFIT_FY1'] = ind_con['EST_NET_PROFIT_FY1'].apply(lambda x: round(x, 2))
        ind_con = ind_con.sort_values(['REPORT_DATE', 'EST_NET_PROFIT_FY1'], ascending=[False, False])
        ind_con = ind_con[['REPORT_DATE', 'INDUSTRY_NAME', 'EST_NET_PROFIT_FY1']]
        ind_con_date = ind_con[ind_con['REPORT_DATE'] == self.report_date].rename(columns={'EST_NET_PROFIT_FY1': self.report_date})
        ind_con_last_date = ind_con[ind_con['REPORT_DATE'] == self.last_report_date].rename(columns={'EST_NET_PROFIT_FY1': self.last_report_date})
        ind_con = ind_con_date.merge(ind_con_last_date.drop('REPORT_DATE', axis=1), on=['INDUSTRY_NAME'], how='left')
        yoy = FEDB().read_industry_data(['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'EST_NET_PROFIT_YOY'], 'industry_consensus', self.sw_type)
        yoy = yoy[yoy['INDUSTRY_NAME'].isin(self.select_industry)]
        yoy = yoy[yoy['REPORT_DATE'].isin([self.report_date])]
        yoy['EST_NET_PROFIT_YOY'] = yoy['EST_NET_PROFIT_YOY'].apply(lambda x: round(x, 2))
        yoy = yoy[['REPORT_DATE', 'INDUSTRY_NAME', 'EST_NET_PROFIT_YOY']]
        ind_con = ind_con.merge(yoy.drop('REPORT_DATE', axis=1), on=['INDUSTRY_NAME'], how='left')
        ind_con = ind_con.sort_values(self.report_date, ascending=False)

        fig, ax = plt.subplots(2, 1, figsize=(12, 6))
        bar_width = 0.3
        ax[0].bar(np.arange(len(ind_con)) - 0.5 * bar_width, ind_con[self.report_date].values, bar_width, label=self.report_date, color=bar_color_list[0])
        ax[0].bar(np.arange(len(ind_con)) + 0.5 * bar_width, ind_con[self.last_report_date].values, bar_width, label=self.last_report_date, color=bar_color_list[7])
        ax[1].bar(np.arange(len(ind_con)), ind_con['EST_NET_PROFIT_YOY'].values, bar_width, label='{0}一致预期同比增长率'.format(self.report_date), color=bar_color_list[14])
        h1, l1 = ax[0].get_legend_handles_labels()
        h2, l2 = ax[1].get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.45), ncol=3)
        ax[0].set_xticks(np.arange(len(ind_con)))
        ax[0].set_xticklabels(labels=[''] * len(ind_con), rotation=45)
        ax[1].set_xticks(np.arange(len(ind_con)))
        ax[1].set_xticklabels(labels=ind_con['INDUSTRY_NAME'].unique().tolist(), rotation=45)
        ax[1].yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax[0].set_xlabel('')
        ax[1].set_xlabel('')
        ax[0].set_ylabel('')
        ax[1].set_ylabel('')
        ax[0].set_title('一致预期净利润及同比增长情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(ax=ax[0], top=True, right=True, left=False, bottom=True)
        sns.despine(ax=ax[1], top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}/con_netprofit.png'.format(self.file_path))
        return

    def IndustryCrowding(self):
        industry_symbol = get_industry_symbol()
        industry_symbol = industry_symbol[industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        industry_symbol = industry_symbol[industry_symbol['IS_NEW'] == 1]
        industry_symbol = industry_symbol[['INDEX_SYMBOL', 'INDUSTRY_NAME']]
        industry_symbol['INDEX_SYMBOL'] = industry_symbol['INDEX_SYMBOL'].apply(lambda x: '{0}.SI'.format(x))
        index_list = industry_symbol['INDEX_SYMBOL'].unique().tolist()
        index_name_dic = industry_symbol.set_index('INDEX_SYMBOL')['INDUSTRY_NAME'].to_dict()
        index_crowding_list = []
        for index in index_list:
            index_data = Crowding(index, index_name_dic, '20180101', self.end_date, self.file_path + '/crowding/').get_crowding()
            index_crowding_list.append(index_data)
        index_crowding = pd.concat(index_crowding_list)
        index_crowding.to_hdf('{0}index_crowding.hdf'.format(self.file_path), key='table', mode='w')
        index_crowding = pd.read_hdf('{0}index_crowding.hdf'.format(self.file_path), key='table')
        index_crowding = index_crowding.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CROWDING')
        index_crowding_up = index_crowding.rolling(window=250, min_periods=1, center=False).mean() + 1.0 * index_crowding.rolling(window=250, min_periods=1, center=False).std(ddof=1)
        index_crowding_down = index_crowding.rolling(window=250, min_periods=1, center=False).mean() - 1.0 * index_crowding.rolling(window=250, min_periods=1, center=False).std(ddof=1)
        index_relative_crowding = (index_crowding - index_crowding_down) / (index_crowding_up - index_crowding_down)
        index_relative_crowding_change = index_relative_crowding - index_relative_crowding.shift(20 * 3)

        plt.figure(figsize=(12, 12))
        plt.scatter(index_relative_crowding.iloc[-1], index_relative_crowding_change.iloc[-1], color=line_color_list[1])
        for i in range(len(index_relative_crowding.iloc[-1])):
            plt.annotate([index_name_dic[index] for index in list(index_relative_crowding.iloc[-1].index)][i], xy=(index_relative_crowding.iloc[-1][i], index_relative_crowding_change.iloc[-1][i]), xytext=(index_relative_crowding.iloc[-1][i], index_relative_crowding_change.iloc[-1][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('拥挤度相对水平', fontsize=16)
        plt.ylabel('拥挤度相对水平近一季度绝对变化', fontsize=16)
        plt.xlim([-2.0, 2.0])
        plt.ylim([-2.0, 2.0])
        plt.hlines(y=0, xmin=-2.0, xmax=2.0, linestyles='-', color='#959595')
        plt.vlines(x=0, ymin=-2.0, ymax=2.0, linestyles='-', color='#959595')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('拥挤度情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        plt.savefig('{0}/crowding.png'.format(self.file_path))
        return

    def IndustryHolding(self):
        rank_list = [self.report_date, self.last_report_date]
        fund_industry_1st = FEDB().read_data(self.report_date, 'INDUSTRY_SW1')
        fund_industry_1st = fund_industry_1st[fund_industry_1st['IS_ZC'] == 1]
        fund_industry_1st = fund_industry_1st[fund_industry_1st['LABEL_NAME'].isin(self.select_industry)]
        fund_industry_1st = fund_industry_1st[fund_industry_1st['REPORT_HISTORY_DATE'].isin(rank_list)]
        fund_industry_1st['LABEL_VALUE'] = fund_industry_1st['LABEL_VALUE'].apply(lambda x: round(x * 100.0, 2))
        fund_industry_1st = fund_industry_1st.sort_values(['REPORT_HISTORY_DATE', 'LABEL_VALUE'], ascending=[False, False])
        fund_industry_1st = fund_industry_1st[['REPORT_HISTORY_DATE', 'LABEL_NAME', 'LABEL_VALUE']]
        fund_industry_1st_date = fund_industry_1st[fund_industry_1st['REPORT_HISTORY_DATE'] == self.report_date].rename(columns={'LABEL_VALUE': self.report_date})
        fund_industry_1st_last_date = fund_industry_1st[fund_industry_1st['REPORT_HISTORY_DATE'] == self.last_report_date].rename(columns={'LABEL_VALUE': self.last_report_date})
        ind_mutual = fund_industry_1st_date.merge(fund_industry_1st_last_date.drop('REPORT_HISTORY_DATE', axis=1), on=['LABEL_NAME'], how='left')
        ind_mutual['LABEL_VALUE_MOM_ABS'] = ind_mutual[self.report_date] - ind_mutual[self.last_report_date]
        ind_mutual = ind_mutual.sort_values(self.report_date, ascending=False)

        fig, ax = plt.subplots(2, 1, figsize=(12, 6))
        bar_width = 0.3
        ax[0].bar(np.arange(len(ind_mutual)) - 0.5 * bar_width, ind_mutual[self.report_date].values, bar_width, label=self.report_date, color=bar_color_list[0])
        ax[0].bar(np.arange(len(ind_mutual)) + 0.5 * bar_width, ind_mutual[self.last_report_date].values, bar_width, label=self.last_report_date, color=bar_color_list[7])
        ax[1].bar(np.arange(len(ind_mutual)), ind_mutual['LABEL_VALUE_MOM_ABS'].values, bar_width, label='{0}环比变化绝对值'.format(self.report_date), color=bar_color_list[14])
        h1, l1 = ax[0].get_legend_handles_labels()
        h2, l2 = ax[1].get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.45), ncol=3)
        ax[0].set_xticks(np.arange(len(ind_mutual)))
        ax[0].set_xticklabels(labels=[''] * len(ind_mutual), rotation=45)
        ax[1].set_xticks(np.arange(len(ind_mutual)))
        ax[1].set_xticklabels(labels=ind_mutual['LABEL_NAME'].unique().tolist(), rotation=45)
        ax[0].yaxis.set_major_formatter(FuncFormatter(to_percent_r1))
        ax[1].yaxis.set_major_formatter(FuncFormatter(to_percent_r1))
        ax[0].set_xlabel('')
        ax[1].set_xlabel('')
        ax[0].set_ylabel('')
        ax[1].set_ylabel('')
        ax[0].set_title('公募持仓及环比绝对变化情况', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(ax=ax[0], top=True, right=True, left=False, bottom=True)
        sns.despine(ax=ax[1], top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}/mutual.png'.format(self.file_path))
        return

    def get_all(self):
        self.IndustryMarketValue()
        self.IndustryRet()
        self.IndustryTech()
        self.IndustryNewhigh()
        self.IndustryVal()
        self.IndustryFmt()
        self.IndustryCon()
        self.IndustryCrowding()
        self.IndustryHolding()
        return


if __name__ == '__main__':
    start_date = '20170101'
    end_date = '20220930'
    last_report_date = '20220630'
    report_date = '20220930'
    con_date = '20211231'
    file_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/'
    sw_type = 1
    IndustryAnalysis(start_date, end_date, last_report_date, report_date, con_date, sw_type, file_path).get_all()
    # sw_type = 3
    # select_industry = ['钴', '锂', '铝', '锂电池', '电池化学品', '硅料硅片', '光伏电池组件', '逆变器', '航空装备', '军工电子', '电动乘用车', '车身附件及饰件', '底盘与发动机系统', '空调', '冰洗', '酒店', '白酒', '数字芯片设计', '模拟芯片设计', '半导体设备', '医疗研发外包']
    # IndustryAnalysis(start_date, end_date, last_report_date, report_date, con_date, sw_type, file_path, select_industry).get_all()