# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})


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

class Index:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_backup = (datetime.strptime(start_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d')
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date_backup, self.end_date)

        self.fund = HBDB().read_fund_info()
        self.fund = self.fund.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'BEGIN_DATE', 'zzrq': 'END_DATE', 'cpfl': 'FUND_TYPE', 'jjfl': 'FUND_TYPE_1ST', 'ejfl': 'FUND_TYPE_2ND', 'kffb': 'OPEN_CLOSE'})
        self.fund = self.fund.dropna(subset=['BEGIN_DATE'])
        self.fund['END_DATE'] = self.fund['END_DATE'].fillna('20990101')
        self.fund['BEGIN_DATE'] = self.fund['BEGIN_DATE'].astype(int).astype(str)
        self.fund['END_DATE'] = self.fund['END_DATE'].astype(int).astype(str)
        self.fund = self.fund[self.fund['FUND_TYPE_2ND'] == '37']
        self.fund['INTO_DATE'] = self.fund['BEGIN_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(90)).strftime('%Y%m%d'))
        self.fund['OUT_DATE'] = self.fund['END_DATE']

        self.fund_share = HBDB().read_fund_share_given_codes(self.fund['FUND_CODE'].unique().tolist())
        self.fund_share.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_share.hdf', key='table', mode='w')
        self.fund_share = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_share.hdf', key='table')
        self.fund_share = self.fund_share.rename(columns={'jjdm': 'FUND_CODE', 'bblb': 'REPORT_TYPE', 'jsrq': 'END_DATE', 'plrq': 'PUBLISH_DATE', 'qsrq': 'BEGIN_DATE', 'qcfe': 'BEGIN_SHARES', 'qjsgfe': 'PURCHASE_SHARES', 'cfzjfe': 'SPLIT_SHARES', 'wjshfe': 'REDEEM_SHARES', 'qmfe': 'END_SHARES'})
        self.fund_share['BEGIN_DATE'] = self.fund_share['BEGIN_DATE'].astype(str)
        self.fund_share['END_DATE'] = self.fund_share['END_DATE'].astype(str)
        self.fund_share['PUBLISH_DATE'] = self.fund_share['PUBLISH_DATE'].astype(str)
        self.fund_share = self.fund_share[self.fund_share['REPORT_TYPE'].isin(['3', '5', '6', '7'])]
        self.fund_share = self.fund_share.sort_values(['FUND_CODE', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['FUND_CODE', 'END_DATE'], keep='last')
        self.fund_share = self.fund_share[['FUND_CODE', 'END_DATE', 'BEGIN_SHARES', 'SPLIT_SHARES', 'PURCHASE_SHARES', 'REDEEM_SHARES', 'END_SHARES']].fillna(0.0).rename(columns={'END_DATE': 'REPORT_DATE'})

        fund_nav_list = []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            print(date)
            fund_nav_date = HBDB().read_fund_nav_given_date(date, self.fund['FUND_CODE'].unique().tolist())
            fund_nav_list.append(fund_nav_date)
        self.fund_nav = pd.concat(fund_nav_list)
        self.fund_nav.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav.hdf', key='table', mode='w')
        self.fund_nav = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav.hdf', key='table')
        self.fund_nav = self.fund_nav.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'jjjz': 'FUND_NAV', 'ljjz': 'FUND_CUM_NAV'})
        self.fund_nav['TRADE_DATE'] = self.fund_nav['TRADE_DATE'].astype(str)
        self.fund_nav = self.fund_nav[['FUND_CODE', 'TRADE_DATE', 'FUND_NAV']]
        self.fund_nav['REPORT_DATE'] = self.fund_nav['TRADE_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')

        fund_nav_adj_list = []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            print(date)
            fund_nav_adj_date = HBDB().read_fund_nav_adj_given_date(date, self.fund['FUND_CODE'].unique().tolist())
            fund_nav_adj_list.append(fund_nav_adj_date)
        self.fund_nav_adj = pd.concat(fund_nav_adj_list)
        self.fund_nav_adj.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav_adj.hdf', key='table', mode='w')
        self.fund_nav_adj = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav_adj.hdf', key='table')
        self.fund_nav_adj = self.fund_nav_adj.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'FUND_NAV_ADJ'})
        self.fund_nav_adj['TRADE_DATE'] = self.fund_nav_adj['TRADE_DATE'].astype(str)
        self.fund_nav_adj = self.fund_nav_adj[['FUND_CODE', 'TRADE_DATE', 'FUND_NAV_ADJ']]
        self.fund_nav_adj['REPORT_DATE'] = self.fund_nav_adj['TRADE_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')
        return

    def get_index_v1(self):
        fund_share = self.fund_share.pivot(index='REPORT_DATE', columns='FUND_CODE', values='END_SHARES')
        fund_nav = self.fund_nav.pivot(index='REPORT_DATE', columns='FUND_CODE', values='FUND_NAV')
        report_df = self.report_df[(self.report_df['REPORT_DATE'] >= self.start_date) & (self.report_df['REPORT_DATE'] <= self.end_date)]
        date_list = sorted(report_df['REPORT_DATE'].unique().tolist())
        index = pd.DataFrame(index=date_list, columns=['885001（考虑申赎）'])
        for i, date in enumerate(date_list):
            fund = self.fund[(self.fund['INTO_DATE'] <= date) & (self.fund['OUT_DATE'] >= date)]
            fund_list = list((set(fund['FUND_CODE'].unique().tolist())).intersection(set(list(fund_share.columns))).intersection(set(list(fund_nav.columns))))
            if len(fund_list) == 0 or i == 0:
                continue
            last_date = date_list[i - 1]
            fund_share_date = pd.DataFrame(fund_share[fund_list].loc[date]).rename(columns={date: 'END_SHARES_DATE'})
            fund_nav_date = pd.DataFrame(fund_nav[fund_list].loc[date]).rename(columns={date: 'FUND_NAV_DATE'})
            fund_date = pd.concat([fund_share_date, fund_nav_date], axis=1)
            fund_date[date] = (fund_date['END_SHARES_DATE'] * fund_date['FUND_NAV_DATE'])
            fund_share_last_date = pd.DataFrame(fund_share[fund_list].loc[last_date]).rename(columns={last_date: 'END_SHARES_LAST_DATE'})
            fund_nav_last_date = pd.DataFrame(fund_nav[fund_list].loc[last_date]).rename(columns={last_date: 'FUND_NAV_LAST_DATE'})
            fund_last_date = pd.concat([fund_share_last_date, fund_nav_last_date], axis=1)
            fund_last_date[last_date] = (fund_last_date['END_SHARES_LAST_DATE'] * fund_last_date['FUND_NAV_LAST_DATE'])
            fund_date = pd.concat([fund_date[[date]], fund_last_date[[last_date]]], axis=1).fillna(0.0)
            index.loc[date, '885001（考虑申赎）'] = fund_date[date].sum() / fund_date[last_date].sum() - 1
        index['885001（考虑申赎）'] = (index['885001（考虑申赎）'].fillna(0.0) + 1.0).cumprod()
        return index

    def get_index_v2(self):
        fund_share = self.fund_share.pivot(index='REPORT_DATE', columns='FUND_CODE', values='BEGIN_SHARES')
        fund_nav_adj = self.fund_nav_adj.pivot(index='REPORT_DATE', columns='FUND_CODE', values='FUND_NAV_ADJ')
        report_df = self.report_df[(self.report_df['REPORT_DATE'] >= self.start_date) & (self.report_df['REPORT_DATE'] <= self.end_date)]
        date_list = sorted(report_df['REPORT_DATE'].unique().tolist())
        index = pd.DataFrame(index=date_list, columns=['885001（考虑申赎）'])
        for date in date_list:
            fund = self.fund[(self.fund['INTO_DATE'] <= date) & (self.fund['OUT_DATE'] >= date)]
            fund_list = list((set(fund['FUND_CODE'].unique().tolist())).intersection(set(list(fund_share.columns))).intersection(set(list(fund_nav_adj.columns))))
            if len(fund_list) == 0:
                continue
            fund_share_date = pd.DataFrame(fund_share[fund_list].loc[date]).rename(columns={date: 'BEGIN_SHARES_DATE'})
            fund_nav_adj_date = pd.DataFrame(fund_nav_adj.sort_index().pct_change()[fund_list].loc[date]).rename(columns={date: 'RET_DATE'})
            fund_date = pd.concat([fund_share_date, fund_nav_adj_date], axis=1).fillna(0.0)
            fund_date['WEIGHT'] = fund_share_date['BEGIN_SHARES_DATE'] / fund_share_date['BEGIN_SHARES_DATE'].sum()
            index.loc[date, '885001（考虑申赎）'] = (fund_date['RET_DATE'] * fund_date['WEIGHT']).sum()
        index['885001（考虑申赎）'] = (index['885001（考虑申赎）'].fillna(0.0) + 1.0).cumprod()
        return index

    def get_index_shares(self):
        fund_purchase_share = self.fund_share.pivot(index='REPORT_DATE', columns='FUND_CODE', values='PURCHASE_SHARES')
        fund_redeem_share = self.fund_share.pivot(index='REPORT_DATE', columns='FUND_CODE', values='REDEEM_SHARES')
        fund_end_share = self.fund_share.pivot(index='REPORT_DATE', columns='FUND_CODE', values='END_SHARES')
        fund_nav = self.fund_nav.pivot(index='REPORT_DATE', columns='FUND_CODE', values='FUND_NAV')
        fund_nav_mean = fund_nav.rolling(2).mean()
        report_df = self.report_df[(self.report_df['REPORT_DATE'] >= self.start_date) & (self.report_df['REPORT_DATE'] <= self.end_date)]
        date_list = sorted(report_df['REPORT_DATE'].unique().tolist())
        index_shares = pd.DataFrame(index=date_list, columns=['申购额（亿元）', '赎回额（亿元）', '规模（亿元）'])
        for date in date_list:
            fund = self.fund[(self.fund['INTO_DATE'] <= date) & (self.fund['OUT_DATE'] >= date)]
            fund_list = list((set(fund['FUND_CODE'].unique().tolist())).intersection(set(list(fund_purchase_share.columns))).intersection(set(list(fund_redeem_share.columns))).intersection(set(list(fund_end_share.columns))).intersection(set(list(fund_nav.columns))))
            if len(fund_list) == 0:
                continue
            fund_purchase_share_date = pd.DataFrame(fund_purchase_share[fund_list].loc[date]).rename(columns={date: 'PURCHASE_SHARES_DATE'})
            fund_redeem_share_date = pd.DataFrame(fund_redeem_share[fund_list].loc[date]).rename(columns={date: 'REDEEM_SHARES_DATE'})
            fund_end_share_date = pd.DataFrame(fund_end_share[fund_list].loc[date]).rename(columns={date: 'END_SHARES_DATE'})
            fund_nav_date = pd.DataFrame(fund_nav[fund_list].loc[date]).rename(columns={date: 'FUND_NAV'})
            fund_nav_mean_date = pd.DataFrame(fund_nav_mean[fund_list].loc[date]).rename(columns={date: 'FUND_NAV_MEAN'})
            index_shares_date = pd.concat([fund_purchase_share_date, fund_redeem_share_date, fund_end_share_date, fund_nav_date, fund_nav_mean_date], axis=1).fillna(0.0)
            index_shares.loc[date, '申购额（亿元）'] = (index_shares_date['PURCHASE_SHARES_DATE'] * index_shares_date['FUND_NAV_MEAN']).sum() / 100000000.0
            index_shares.loc[date, '赎回额（亿元）'] = (index_shares_date['REDEEM_SHARES_DATE'] * index_shares_date['FUND_NAV_MEAN']).sum() / 100000000.0
            index_shares.loc[date, '规模（亿元）'] = (index_shares_date['END_SHARES_DATE'] * index_shares_date['FUND_NAV']).sum() / 100000000.0
        return index_shares


if __name__ == '__main__':
    start_date = '20041231'
    end_date = '20220630'
    # index = Index(start_date, end_date).get_index_v1()
    index = Index(start_date, end_date).get_index_v2()
    index = index.sort_index()
    index = index / index.iloc[0]
    bmk_index = HBDB().read_index_daily_k_given_date_and_indexs((datetime.strptime(start_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'), ['885001'])
    bmk_index = bmk_index.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'spjg': 'INDEX_POINT'})
    bmk_index['TRADE_DATE'] = bmk_index['TRADE_DATE'].astype(str)
    bmk_index = bmk_index[bmk_index['TRADE_DATE'] <= end_date]
    bmk_index['YEAR_MONTH'] = bmk_index['TRADE_DATE'].apply(lambda x: x[:6])
    bmk_index['MONTH'] = bmk_index['TRADE_DATE'].apply(lambda x: x[4:6])
    bmk_index = bmk_index.sort_values(['INDEX_SYMBOL', 'TRADE_DATE']).drop_duplicates('YEAR_MONTH', keep='last')
    bmk_index = bmk_index[bmk_index['MONTH'].isin(['03', '06', '09', '12'])]
    bmk_index['REPORT_DATE'] = bmk_index['TRADE_DATE'].apply(lambda x: x[:6] + '31' if x[4:6] == '03' or x[4:6] == '12' else x[:6] + '30')
    bmk_index = bmk_index[['INDEX_SYMBOL', 'REPORT_DATE', 'INDEX_POINT']]
    bmk_index = bmk_index.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='INDEX_POINT')
    bmk_index = bmk_index[bmk_index.index >= start_date]
    bmk_index = bmk_index.sort_index()
    bmk_index = bmk_index / bmk_index.iloc[0]
    index = pd.concat([index, bmk_index], axis=1)

    # plt.figure(figsize=(12, 8))
    # plt.plot(index.index, index['885001（考虑申赎）'].values, label='885001（考虑申赎）', color='#F04950')
    # plt.plot(index.index, index['885001'].values, label='885001', color='#6268A2')
    # plt.legend(loc=2)
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/885001（考虑申赎）_v1.png')
    # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/885001（考虑申赎）_v2.png')

    index_shares = Index(start_date, end_date).get_index_shares()
    index = index.reset_index().rename(columns={'index': '报告日期'})
    index_shares = index_shares.reset_index().rename(columns={'index': '报告日期'})
    scale = index_shares[['报告日期', '规模（亿元）']]
    purchase = index_shares[['报告日期', '申购额（亿元）']].rename(columns={'申购额（亿元）': '申赎额（亿元）'})
    purchase['申赎额'] = '申购额（亿元）'
    redeem = index_shares[['报告日期', '赎回额（亿元）']].rename(columns={'赎回额（亿元）': '申赎额（亿元）'})
    redeem['申赎额'] = '赎回额（亿元）'
    purchase_redeem = pd.concat([purchase, redeem]).reset_index().drop('index', axis=1)

    fig, ax = plt.subplots(2, 1, figsize=(16, 16))
    ax0 = ax[0]
    ax1 = ax[1]
    ax2 = ax[1].twinx()
    ax0.plot(index['报告日期'].values, index['885001（考虑申赎）'].values, label='885001（考虑申赎）', linewidth=3, color='#F04950')
    ax0.plot(index['报告日期'].values, index['885001'].values, label='885001', linewidth=3, color='#6268A2')
    ax1.plot(scale['报告日期'].values, scale['规模（亿元）'].values, label='规模（亿元）', linewidth=3, color='#F04950')
    sns.barplot(ax=ax2, x='报告日期', y='申赎额（亿元）', data=purchase_redeem, hue='申赎额', palette=['#C94649', '#8588B7'])
    ax0.legend(loc=2)
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax0.set_xlabel('')
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax0.set_ylabel('')
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    ax0.set_xticklabels(labels=scale['报告日期'].unique().tolist(), rotation=90)
    ax1.set_xticklabels(labels=scale['报告日期'].unique().tolist(), rotation=90)
    ax2.set_xticklabels(labels=scale['报告日期'].unique().tolist(), rotation=90)
    plt.tight_layout()
    plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/885001（考虑申赎）.png')
