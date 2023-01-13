# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                  '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
new_color_list = ['#F04950', '#959595', '#6268A2', '#333335', '#D57C56', '#628497']


def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def to_percent_r2(temp, position):
    return '%0.01f'%(temp) + '%'

def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'

def to_100percent_r2(temp, position):
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


class TimingAnalysis:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date('19000101', self.end_date)

    def MarketTiming(self):
        # 成交额占比
        turnover_proportion = FEDB().read_timing_data(['TRADE_DATE', 'TURNOVER_PROPORTION_000300', 'TURNOVER_PROPORTION_000905', 'TURNOVER_PROPORTION_000852'], 'timing_market', self.start_date, self.end_date)
        turnover_proportion['TRADE_DATE'] = turnover_proportion['TRADE_DATE'].astype(str)
        turnover_proportion = turnover_proportion[turnover_proportion['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        turnover_proportion = turnover_proportion.sort_values('TRADE_DATE')
        turnover_proportion['TRADE_DATE'] = turnover_proportion['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(turnover_proportion['TRADE_DATE'].values, turnover_proportion['TURNOVER_PROPORTION_000300'].values, color=line_color_list[0], label='沪深300')
        plt.plot(turnover_proportion['TRADE_DATE'].values, turnover_proportion['TURNOVER_PROPORTION_000905'].values, color=line_color_list[1], label='中证500')
        plt.plot(turnover_proportion['TRADE_DATE'].values, turnover_proportion['TURNOVER_PROPORTION_000852'].values, color=line_color_list[2], label='中证1000')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('成交额占比', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '成交额占比'))

        # 北向资金净流入
        hk_cash = FEDB().read_timing_data(['TRADE_DATE', 'SH_NET_PURCHASE', 'SZ_NET_PURCHASE', 'HK_NET_PURCHASE'], 'timing_market', '20071231', self.end_date)
        hk_cash['TRADE_DATE'] = hk_cash['TRADE_DATE'].astype(str)
        hk_cash = hk_cash.set_index('TRADE_DATE').dropna(how='all').reset_index()
        hk_cash = hk_cash.sort_values('TRADE_DATE')
        hk_cash['SH_NET_PURCHASE'] = hk_cash['SH_NET_PURCHASE'].cumsum()
        hk_cash['SZ_NET_PURCHASE'] = hk_cash['SZ_NET_PURCHASE'].cumsum()
        hk_cash['HK_NET_PURCHASE'] = hk_cash['HK_NET_PURCHASE'].cumsum()
        hk_cash['TRADE_DATE'] = hk_cash['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(hk_cash['TRADE_DATE'].values, hk_cash['HK_NET_PURCHASE'].values, color=line_color_list[0], label='北向资金净流入（亿元）')
        plt.plot(hk_cash['TRADE_DATE'].values, hk_cash['SH_NET_PURCHASE'].values, color=line_color_list[1], label='沪股通净流入（亿元）')
        plt.plot(hk_cash['TRADE_DATE'].values, hk_cash['SZ_NET_PURCHASE'].values, color=line_color_list[2], label='深股通净流入（亿元）')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.title('北向资金累计净流入', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '北向资金累计净流入'))

        # 融资融券余额
        margin_balance = FEDB().read_timing_data(['TRADE_DATE', 'MARGIN_BALANCE'], 'timing_market', '20071231', self.end_date)
        margin_balance['TRADE_DATE'] = margin_balance['TRADE_DATE'].astype(str)
        margin_balance = margin_balance.set_index('TRADE_DATE').dropna(how='all').reset_index()
        margin_balance = margin_balance.sort_values('TRADE_DATE')
        margin_balance['TRADE_DATE'] = margin_balance['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.stackplot(margin_balance['TRADE_DATE'].values, margin_balance['MARGIN_BALANCE'].values, color=line_color_list[0], alpha=0.5, labels=['融资融券余额（亿元）'])
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=1)
        plt.title('融资融券余额', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '融资融券余额'))

        # 创近一月/近六月新高个股数量及占比
        new_high = FEDB().read_timing_data(['TRADE_DATE', 'NEW_HIGH_SHORT', 'NEW_HIGH_RATIO_SHORT', 'NEW_HIGH_LONG', 'NEW_HIGH_RATIO_LONG'], 'timing_market', self.start_date, self.end_date)
        new_high['TRADE_DATE'] = new_high['TRADE_DATE'].astype(str)
        new_high = new_high[new_high['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_MONTH_END'] == '1']['TRADE_DATE'].unique().tolist())]
        new_high = new_high.sort_values('TRADE_DATE')
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        bar_width = 0.3
        ax1.bar(np.arange(len(new_high)) - 0.5 * bar_width, new_high['NEW_HIGH_SHORT'].values, bar_width, label='创近一月新高个股数量', color=bar_color_list[0])
        ax1.bar(np.arange(len(new_high)) + 0.5 * bar_width, new_high['NEW_HIGH_LONG'].values, bar_width, label='创近六月新高个股数量', color=bar_color_list[7])
        ax2.plot(np.arange(len(new_high)), new_high['NEW_HIGH_RATIO_SHORT'].values, label='创近一月新高个股占比（右轴）', color=line_color_list[0])
        ax2.plot(np.arange(len(new_high)), new_high['NEW_HIGH_RATIO_LONG'].values, label='创近六月新高个股占比（右轴）',  color=line_color_list[1])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=4)
        ax1.set_xticks(np.arange(len(new_high)))
        ax1.set_xticklabels(labels=new_high['TRADE_DATE'].unique().tolist(), rotation=60)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('创新高个股数量及占比', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '创新高个股数量及占比'))

        # 行业分歧度
        industry_divergence = FEDB().read_timing_data(['TRADE_DATE', 'TURNOVER_VALUE', 'PCA_1ST_SHORT', 'PCA_1ST_LONG'], 'timing_market', self.start_date, self.end_date)
        industry_divergence['TRADE_DATE'] = industry_divergence['TRADE_DATE'].astype(str)
        industry_divergence = industry_divergence[industry_divergence['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_WEEK_END'] == '1']['TRADE_DATE'].unique().tolist())]
        industry_divergence = industry_divergence.sort_values('TRADE_DATE')
        industry_divergence['TURNOVER_VALUE'] = industry_divergence['TURNOVER_VALUE'] / 100000000.0
        industry_divergence['TRADE_DATE'] = industry_divergence['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.plot(industry_divergence['TRADE_DATE'].values, industry_divergence['PCA_1ST_SHORT'].values, color=line_color_list[0], label='近10日行业分歧度')
        ax1.plot(industry_divergence['TRADE_DATE'].values, industry_divergence['PCA_1ST_LONG'].values, color=line_color_list[1], label='近60日行业分歧度')
        ax2.stackplot(industry_divergence['TRADE_DATE'].values, industry_divergence['TURNOVER_VALUE'].values, color=line_color_list[3], alpha=0.5, labels=['市场成交额（亿元， 右轴）'])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.15), ncol=3)
        ax1.set_ylim([0, 1])
        ax2.set_ylim([0, 30000])
        ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('行业分歧度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '行业分歧度'))

        # 偏股基金仓位（公募、私募）
        mutual_position = FEDB().read_timing_data(['TRADE_DATE', 'POSITION_MUTUAL'], 'timing_market', self.start_date, self.end_date)
        mutual_position['TRADE_DATE'] = mutual_position['TRADE_DATE'].astype(str)
        mutual_position = mutual_position[mutual_position['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        mutual_position = mutual_position.sort_values('TRADE_DATE')
        mutual_position['TRADE_DATE'] = mutual_position['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        private_position = FEDB().read_timing_data(['TRADE_DATE', 'POSITION_PRIVATE'], 'timing_market', self.start_date, self.end_date)
        private_position['TRADE_DATE'] = private_position['TRADE_DATE'].astype(str)
        private_position = private_position[private_position['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_WEEK_END'] == '1']['TRADE_DATE'].unique().tolist())]
        private_position = private_position.sort_values('TRADE_DATE')
        private_position['TRADE_DATE'] = private_position['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(mutual_position['TRADE_DATE'].values, mutual_position['POSITION_MUTUAL'].values, color=line_color_list[0], label='偏股混合型公募基金仓位')
        plt.plot(private_position['TRADE_DATE'].values, private_position['POSITION_PRIVATE'].values, color=line_color_list[1], label='主观多头型私募基金仓位')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('偏股基金仓位', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '偏股基金仓位'))

        # 市场景气度
        prosperity = FEDB().read_timing_data(['TRADE_DATE', 'NET_PROFIT_YOY_000300', 'NET_PROFIT_YOY_000905', 'NET_PROFIT_YOY_000852', 'NET_PROFIT_YOY_000985'], 'timing_market', self.start_date, self.end_date)
        prosperity['TRADE_DATE'] = prosperity['TRADE_DATE'].astype(str)
        prosperity = prosperity[prosperity['TRADE_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        prosperity = prosperity.sort_values('TRADE_DATE')
        fig, ax = plt.subplots(figsize=(12, 6))
        bar_width = 0.2
        ax.bar(np.arange(len(prosperity)) - 1.5 * bar_width, prosperity['NET_PROFIT_YOY_000300'].values, bar_width, label='沪深300', color=new_color_list[0])
        ax.bar(np.arange(len(prosperity)) - 0.5 * bar_width, prosperity['NET_PROFIT_YOY_000905'].values, bar_width, label='中证500', color=new_color_list[2])
        ax.bar(np.arange(len(prosperity)) + 0.5 * bar_width, prosperity['NET_PROFIT_YOY_000852'].values, bar_width, label='中证1000', color=new_color_list[1])
        ax.bar(np.arange(len(prosperity)) + 1.5 * bar_width, prosperity['NET_PROFIT_YOY_000985'].values, bar_width, label='中证全指', color=new_color_list[3])
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.25), ncol=4)
        ax.set_xticks(np.arange(len(prosperity)))
        ax.set_xticklabels(labels=prosperity['TRADE_DATE'].unique().tolist(), rotation=60)
        ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('净利润同比增速', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '净利润同比增速'))

        # 股债性价比
        bond_stock = FEDB().read_timing_data(['TRADE_DATE', 'B_GXL_000300', 'B_GXL_000905', 'B_GXL_000852', 'B_GXL_000985'], 'timing_market', self.start_date, self.end_date)
        bond_stock['TRADE_DATE'] = bond_stock['TRADE_DATE'].astype(str)
        bond_stock = bond_stock[bond_stock['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        bond_stock = bond_stock.sort_values('TRADE_DATE')
        bond_stock['TRADE_DATE'] = bond_stock['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(bond_stock['TRADE_DATE'].values, bond_stock['B_GXL_000300'].values, color=line_color_list[0], label='沪深300')
        plt.plot(bond_stock['TRADE_DATE'].values, bond_stock['B_GXL_000905'].values, color=line_color_list[1], label='中证500')
        plt.plot(bond_stock['TRADE_DATE'].values, bond_stock['B_GXL_000852'].values, color=line_color_list[2], label='中证1000')
        plt.plot(bond_stock['TRADE_DATE'].values, bond_stock['B_GXL_000985'].values, color=line_color_list[3], label='中证全指')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=4)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent_r2))
        plt.title('股债性价比', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '股债性价比'))
        return

    def StyleTiming(self):
        # 风格拥挤度
        style_crowding = FEDB().read_timing_data(['TRADE_DATE', 'GROWTH_CROWDING', 'VALUE_CROWDING'], 'timing_style', self.start_date, self.end_date)
        style_crowding['TRADE_DATE'] = style_crowding['TRADE_DATE'].astype(str)
        style_crowding = style_crowding[style_crowding['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        style_crowding = style_crowding.sort_values('TRADE_DATE')
        style_crowding['TRADE_DATE'] = style_crowding['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(style_crowding['TRADE_DATE'].values, style_crowding['GROWTH_CROWDING'].values, color=line_color_list[0], label='成长')
        plt.plot(style_crowding['TRADE_DATE'].values, style_crowding['VALUE_CROWDING'].values, color=line_color_list[1], label='价值')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.title('风格拥挤度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '风格拥挤度'))

        # 规模拥挤度
        size_crowding = FEDB().read_timing_data(['TRADE_DATE', 'SIZE_CROWDING'], 'timing_style', self.start_date, self.end_date)
        size_crowding['TRADE_DATE'] = size_crowding['TRADE_DATE'].astype(str)
        size_crowding = size_crowding[size_crowding['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        size_crowding = size_crowding.sort_values('TRADE_DATE')
        size_crowding['TRADE_DATE'] = size_crowding['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(size_crowding['TRADE_DATE'].values, size_crowding['SIZE_CROWDING'].values, color=line_color_list[0], label='规模')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=1)
        plt.title('规模拥挤度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '规模拥挤度'))

        # 风格离散度
        style_spread = FEDB().read_timing_data(['TRADE_DATE', 'GROWTH_SPREAD', 'VALUE_SPREAD'], 'timing_style', self.start_date, self.end_date)
        style_spread['TRADE_DATE'] = style_spread['TRADE_DATE'].astype(str)
        style_spread = style_spread[style_spread['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        style_spread = style_spread.sort_values('TRADE_DATE')
        style_spread['TRADE_DATE'] = style_spread['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(style_spread['TRADE_DATE'].values, style_spread['GROWTH_SPREAD'].values, color=line_color_list[0], label='成长')
        plt.plot(style_spread['TRADE_DATE'].values, style_spread['VALUE_SPREAD'].values, color=line_color_list[1], label='价值')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.title('风格离散度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '风格离散度'))

        # 规模离散度
        size_spread = FEDB().read_timing_data(['TRADE_DATE', 'SIZE_SPREAD'], 'timing_style', self.start_date, self.end_date)
        size_spread['TRADE_DATE'] = size_spread['TRADE_DATE'].astype(str)
        size_spread = size_spread[size_spread['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        size_spread = size_spread.sort_values('TRADE_DATE')
        size_spread['TRADE_DATE'] = size_spread['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(size_spread['TRADE_DATE'].values, size_spread['SIZE_SPREAD'].values, color=line_color_list[0], label='规模')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=1)
        plt.title('规模离散度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '规模离散度'))

        # 风格动量
        style_momentum = FEDB().read_timing_data(['TRADE_DATE', 'GROWTH_MOMENTUM', 'VALUE_MOMENTUM'], 'timing_style',  self.start_date, self.end_date)
        style_momentum['TRADE_DATE'] = style_momentum['TRADE_DATE'].astype(str)
        style_momentum = style_momentum[style_momentum['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        style_momentum = style_momentum.sort_values('TRADE_DATE')
        style_momentum['TRADE_DATE'] = style_momentum['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(style_momentum['TRADE_DATE'].values, style_momentum['GROWTH_MOMENTUM'].values, color=line_color_list[0], label='成长')
        plt.plot(style_momentum['TRADE_DATE'].values, style_momentum['VALUE_MOMENTUM'].values, color=line_color_list[1], label='价值')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.title('风格动量', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '风格动量'))

        # 规模动量
        size_momentum= FEDB().read_timing_data(['TRADE_DATE', 'SIZE_MOMENTUM'], 'timing_style', self.start_date, self.end_date)
        size_momentum['TRADE_DATE'] = size_momentum['TRADE_DATE'].astype(str)
        size_momentum = size_momentum[size_momentum['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        size_momentum = size_momentum.sort_values('TRADE_DATE')
        size_momentum['TRADE_DATE'] = size_momentum['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(size_momentum['TRADE_DATE'].values, size_momentum['SIZE_MOMENTUM'].values, color=line_color_list[0], label='规模')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=1)
        plt.title('规模动量', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '规模动量'))
        return

    def IndustryTiming(self, index_symbol):
        # 量能维度：成交额占比、换手率
        turnover = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'TURNOVER_PROPORTION', 'TURNOVER_RATE'], 'timing_industry', self.start_date, self.end_date)
        turnover = turnover[turnover['INDEX_SYMBOL'] == index_symbol]
        turnover['TRADE_DATE'] = turnover['TRADE_DATE'].astype(str)
        turnover = turnover[turnover['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        turnover = turnover.sort_values('TRADE_DATE')
        turnover['TRADE_DATE'] = turnover['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(turnover['TRADE_DATE'].values, turnover['TURNOVER_PROPORTION'].values, color=line_color_list[0],  label='成交额占比')
        plt.plot(turnover['TRADE_DATE'].values, turnover['TURNOVER_RATE'].values, color=line_color_list[1], label='换手率')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('量能维度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '量能维度'))

        # 量价相关系数
        corr = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'CORR'], 'timing_industry', self.start_date, self.end_date)
        corr = corr[corr['INDEX_SYMBOL'] == index_symbol]
        corr['TRADE_DATE'] = corr['TRADE_DATE'].astype(str)
        corr = corr[corr['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_WEEK_END'] == '1']['TRADE_DATE'].unique().tolist())]
        corr = corr.sort_values('TRADE_DATE')
        index = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, [index_symbol])
        index = index.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        index = index[['TRADE_DATE', 'INDEX_SYMBOL', 'CLOSE_INDEX']]
        index['TRADE_DATE'] = index['TRADE_DATE'].astype(str)
        index = index.sort_values('TRADE_DATE')
        corr = corr.merge(index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        corr['TRADE_DATE'] = corr['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.plot(corr['TRADE_DATE'].values, corr['CORR'].values, color=line_color_list[0], label='量价相关系数')
        ax2.stackplot(corr['TRADE_DATE'].values, corr['CLOSE_INDEX'].values, color=line_color_list[3], alpha=0.5, labels=['指数走势（右轴）'])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        ax1.set_ylim([-1, 1])
        ax2.set_ylim([2000, 7000])
        plt.title('量价相关系数', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '量价相关系数'))

        # 价格维度：创新高个股数量及占比、均线上个股数量及占比
        price = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'NEW_HIGH', 'NEW_HIGH_RATIO', 'MEAN_ABOVE', 'MEAN_ABOVE_RATIO'], 'timing_industry', self.start_date, self.end_date)
        price = price[price['INDEX_SYMBOL'] == index_symbol]
        price['TRADE_DATE'] = price['TRADE_DATE'].astype(str)
        price = price[price['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_MONTH_END'] == '1']['TRADE_DATE'].unique().tolist())]
        price = price.sort_values('TRADE_DATE')
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        bar_width = 0.3
        ax1.bar(np.arange(len(price)) - 0.5 * bar_width, price['NEW_HIGH'].values, bar_width, label='创60个交易日新高个股数量', color=bar_color_list[0])
        ax1.bar(np.arange(len(price)) + 0.5 * bar_width, price['MEAN_ABOVE'].values, bar_width, label='20个交易日均线上个股数量', color=bar_color_list[7])
        ax2.plot(np.arange(len(price)), price['NEW_HIGH_RATIO'].values, label='创60个交易日新高个股占比（右轴）',  color=line_color_list[0])
        ax2.plot(np.arange(len(price)), price['MEAN_ABOVE_RATIO'].values, label='20个交易日均线上个股占比（右轴）', color=line_color_list[1])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=4)
        ax1.set_xticks(np.arange(len(price)))
        ax1.set_xticklabels(labels=price['TRADE_DATE'].unique().tolist(), rotation=60)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('价格维度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '价格维度'))

        # 资金维度：主力资金净流入率、融资买入情绪
        cash = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'MAIN_CASH_PROPORTION', 'MARGIN_PROPORTION'], 'timing_industry', self.start_date, self.end_date)
        cash = cash[cash['INDEX_SYMBOL'] == index_symbol]
        cash['TRADE_DATE'] = cash['TRADE_DATE'].astype(str)
        cash = cash[cash['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        cash = cash.sort_values('TRADE_DATE')
        cash['TRADE_DATE'] = cash['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(cash['TRADE_DATE'].values, cash['MAIN_CASH_PROPORTION'].values, color=line_color_list[0], label='主力资金净流入率')
        plt.plot(cash['TRADE_DATE'].values, cash['MARGIN_PROPORTION'].values, color=line_color_list[1], label='融资买入情绪')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('资金维度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '资金维度'))

        # 分析师情绪：创新高个股数量及占比、均线上个股数量及占比
        consensus = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'CONSENSUS_UP', 'CONSENSUS_UP_RATIO', 'CONSENSUS_DOWN', 'CONSENSUS_DOWN_RATIO'], 'timing_industry', self.start_date, self.end_date)
        consensus = consensus[consensus['INDEX_SYMBOL'] == index_symbol]
        consensus['TRADE_DATE'] = consensus['TRADE_DATE'].astype(str)
        consensus = consensus[consensus['TRADE_DATE'].isin(self.trade_df[self.trade_df['IS_MONTH_END'] == '1']['TRADE_DATE'].unique().tolist())]
        consensus = consensus.sort_values('TRADE_DATE')
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        bar_width = 0.3
        ax1.bar(np.arange(len(consensus)), consensus['CONSENSUS_UP'].values, bar_width, label='分析师一致预期上调个股数量', color=bar_color_list[0])
        # ax1.bar(np.arange(len(consensus)) + 0.5 * bar_width, consensus['CONSENSUS_DOWN'].values, bar_width, label='分析师一致预期下调个股数量', color=bar_color_list[7])
        ax2.plot(np.arange(len(consensus)), consensus['CONSENSUS_UP_RATIO'].values, label='分析师一致预期上调个股占比（右轴）', color=line_color_list[1])
        # ax2.plot(np.arange(len(consensus)), consensus['CONSENSUS_DOWN_RATIO'].values, label='分析师一致预期下调个股占比（右轴）', color=line_color_list[1])
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=4)
        ax1.set_xticks(np.arange(len(consensus)))
        ax1.set_xticklabels(labels=consensus['TRADE_DATE'].unique().tolist(), rotation=60)
        ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('分析师情绪', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '分析师情绪'))

        # 行业景气度
        prosperity = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'OPER_REVENUE_YOY_DIFF', 'NET_PROFIT_YOY_DIFF', 'ROE_TTM_DIFF'], 'timing_industry', self.start_date, self.end_date)
        prosperity = prosperity[prosperity['INDEX_SYMBOL'] == index_symbol]
        prosperity['TRADE_DATE'] = prosperity['TRADE_DATE'].astype(str)
        prosperity = prosperity[prosperity['TRADE_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        prosperity = prosperity.sort_values('TRADE_DATE')
        prosperity['PROSPERITY'] = (prosperity['OPER_REVENUE_YOY_DIFF'] + prosperity['NET_PROFIT_YOY_DIFF'] + prosperity['ROE_TTM_DIFF']) / 3.0
        fig, ax = plt.subplots(figsize=(12, 6))
        bar_width = 0.2
        ax.bar(np.arange(len(prosperity)), prosperity['PROSPERITY'].values, bar_width,  label='行业景气度', color=bar_color_list[0])
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.25), ncol=1)
        ax.set_xticks(np.arange(len(prosperity)))
        ax.set_xticklabels(labels=prosperity['TRADE_DATE'].unique().tolist(), rotation=60)
        ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('行业景气度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '行业景气度'))

        # 行业动量
        momentum = FEDB().read_timing_data(['TRADE_DATE', 'INDEX_SYMBOL', 'INDUSTRY_MOMENTUM'], 'timing_industry', self.start_date, self.end_date)
        momentum = momentum[momentum['INDEX_SYMBOL'] == index_symbol]
        momentum['TRADE_DATE'] = momentum['TRADE_DATE'].astype(str)
        momentum = momentum[momentum['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        momentum = momentum.sort_values('TRADE_DATE')
        momentum['TRADE_DATE'] = momentum['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.stackplot(momentum['TRADE_DATE'].values, momentum['INDUSTRY_MOMENTUM'].values, color=line_color_list[0], alpha=0.5, labels=['行业动量'])
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('行业动量', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '行业动量'))
        return

    def StockTiming(self):
        # 成交额集中度
        turnover_proportion = FEDB().read_timing_data(['TRADE_DATE', 'TURNOVER_PROPORTION_TOP5', 'TURNOVER_PROPORTION_TOP10'], 'timing_stock', self.start_date, self.end_date)
        turnover_proportion['TRADE_DATE'] = turnover_proportion['TRADE_DATE'].astype(str)
        turnover_proportion = turnover_proportion[turnover_proportion['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        turnover_proportion = turnover_proportion.sort_values('TRADE_DATE')
        turnover_proportion['TRADE_DATE'] = turnover_proportion['TRADE_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(turnover_proportion['TRADE_DATE'].values, turnover_proportion['TURNOVER_PROPORTION_TOP5'].values, color=line_color_list[0], label='前5%个股成交额集中度')
        plt.plot(turnover_proportion['TRADE_DATE'].values, turnover_proportion['TURNOVER_PROPORTION_TOP10'].values, color=line_color_list[1], label='前10%个股成交额集中度')
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('成交额集中度', fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
        plt.tight_layout()
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, '成交额集中度'))
        return


if __name__ == '__main__':
    start_date = '20180101'
    end_date = '20221209'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/timing/'
    TimingAnalysis(start_date, end_date, data_path).MarketTiming()
    TimingAnalysis(start_date, end_date, data_path).StyleTiming()
    TimingAnalysis(start_date, end_date, data_path).IndustryTiming('801010')
    TimingAnalysis(start_date, end_date, data_path).StockTiming()