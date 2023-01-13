# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.xwq.analysis.orm.plot import plot
from hbshare.fe.xwq.analysis.utils.const_var import TimeDateFormat
from hbshare.fe.xwq.analysis.utils.timedelta_utils import TimeDateUtil
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})
industry_theme_dic = {'银行': '大金融', '非银金融': '大金融', '房地产': '大金融',
                      '食品饮料': '消费', '家用电器': '消费', '医药生物': '消费', '社会服务': '消费', '农林牧渔': '消费', '商贸零售': '消费', '美容护理': '消费',
                      '通信': 'TMT', '计算机': 'TMT', '电子': 'TMT', '传媒': 'TMT', '国防军工': 'TMT',
                      '交通运输': '制造', '机械设备': '制造', '汽车': '制造', '纺织服饰': '制造', '轻工制造': '制造', '电力设备': '制造',
                      '钢铁': '周期', '有色金属': '周期', '建筑装饰': '周期', '建筑材料': '周期', '基础化工': '周期', '石油石化': '周期', '煤炭': '周期', '公用事业': '周期', '环保': '周期',
                      '综合': '其他'}


def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def to_percent_r2(temp, position):
    return '%0.01f'%(temp) + '%'

def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'

def to_100percent_r2(temp, position):
    return '%0.01f'%(temp * 100) + '%'

def fund_overview_plot(date, pic_path):
    """
    基金分布画图
    """
    label_type = 'OVERVIEW'
    fund_overview = FEDB().read_data(date, label_type)
    fund_overview = fund_overview[fund_overview['IS_ZC'] == 1]
    fund_overview['FUND_TYPE'] = fund_overview['LABEL_NAME'].apply(lambda x: x.split('_')[0])
    fund_overview['OPEN_CLOSE'] = fund_overview['LABEL_NAME'].apply(lambda x: x.split('_')[1])
    fund_overview = fund_overview[fund_overview['OPEN_CLOSE'] == '开放式基金']
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(fund_overview['LABEL_VALUE'].values, labels=fund_overview['FUND_TYPE'].values, autopct='%0.2f%%', colors=['#D55659', '#8588B7', '#7D7D7E'])
    plt.title('基金类型分布')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '类型分布'))
    return

def fund_valuation_plot(date, pic_path):
    """
    估值分析画图
    """
    label_type = 'VALUATION'
    fund_valuation = FEDB().read_data(date, label_type)
    fund_valuation = fund_valuation[fund_valuation['IS_ZC'] == 1]
    pe_valuation = fund_valuation[fund_valuation['LABEL_NAME'].str.slice(0, 2) == 'PE']
    pe_valuation = pe_valuation.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    pe_valuation = pe_valuation.apply(lambda x: x / x.sum(), axis=1)
    pe_valuation = pe_valuation.sort_index()
    pe_valuation.columns = ['PE>50（含负）', '0<PE<=30', '30<PE<=50']
    pe_valuation = pe_valuation[['0<PE<=30', '30<PE<=50', 'PE>50（含负）']]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(pe_valuation.index.tolist(), pe_valuation.T.values.tolist(), colors=['#D55659', '#8588B7', '#7D7D7E'], labels=pe_valuation.columns.tolist())
    plt.legend(loc=2)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('估值分布（PE）')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '估值分布（PE）'))

    pb_valuation = fund_valuation[fund_valuation['LABEL_NAME'].str.slice(0, 2) == 'PB']
    pb_valuation = pb_valuation.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    pb_valuation = pb_valuation.apply(lambda x: x / x.sum(), axis=1)
    pb_valuation = pb_valuation.sort_index()
    pb_valuation.columns = ['PB>5（含负）', '0<PB<=5']
    pb_valuation = pb_valuation[['0<PB<=5', 'PB>5（含负）']]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(pb_valuation.index.tolist(), pb_valuation.T.values.tolist(), colors=['#D55659', '#8588B7'], labels=pb_valuation.columns.tolist())
    plt.legend(loc=2)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('估值分布（PB）')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '估值分布（PB）'))

    label_type = 'VALUATION_DIFF'
    fund_valuation_diff = FEDB().read_data(date, label_type)
    fund_valuation_diff = fund_valuation_diff[fund_valuation_diff['IS_ZC'] == 1]
    fund_valuation_diff = fund_valuation_diff.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_valuation_diff = fund_valuation_diff.sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(fund_valuation_diff.index)), fund_valuation_diff['PE_平均估值差'], color='#C94649', tick_label=fund_valuation_diff.index)
    plt.xticks(rotation=90)
    plt.title('平均估值差（PE）')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '平均估值差（PE）'))

    label_type = 'VALUATION_PREMIUM'
    fund_valuation_premium = FEDB().read_data(date, label_type)
    fund_valuation_premium = fund_valuation_premium[fund_valuation_premium['IS_ZC'] == 1]
    pe_valuation_premium = fund_valuation_premium[fund_valuation_premium['LABEL_NAME'].str.slice(0, 2) == 'PE']
    pe_valuation_premium = pe_valuation_premium.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    pe_valuation_premium = pe_valuation_premium.sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(pe_valuation_premium.index, pe_valuation_premium['PE_核心资产估值溢价'], '#F04950')
    plt.xticks(rotation=90)
    plt.title('核心资产估值溢价（PE）')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '核心资产估值溢价（PE）'))

    pb_valuation_premium = fund_valuation_premium[fund_valuation_premium['LABEL_NAME'].str.slice(0, 2) == 'PB']
    pb_valuation_premium = pb_valuation_premium.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    pb_valuation_premium = pb_valuation_premium.sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(pe_valuation_premium.index, pb_valuation_premium['PB_核心资产估值溢价'], '#F04950')
    plt.xticks(rotation=90)
    plt.title('核心资产估值溢价（PB）')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '核心资产估值溢价（PB）'))
    return

def fund_sector_plot(date, pic_path):
    """
    板块分析画图
    """
    label_type = 'SECTOR'
    fund_sector = FEDB().read_data(date, label_type)
    fund_sector = fund_sector[fund_sector['IS_ZC'] == 1]
    fund_sector = fund_sector.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_sector = fund_sector.apply(lambda x: x / x.sum(), axis=1)
    fund_sector = fund_sector.sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(fund_sector.index.tolist(), fund_sector.T.values.tolist(), colors=['#D55659', '#E1777A', '#8588B7', '#626697', '#7D7D7E'], labels=fund_sector.columns.tolist())
    plt.legend(loc=2)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('板块分布')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '板块分布'))

    hsi = pd.read_excel('{0}hsi_pe.xlsx'.format(pic_path))
    hsi = hsi[['交易日期', '市盈率TTM']]
    hsi.columns = ['TRADE_DATE', '恒生指数PE_TTM']
    hsi['TRADE_DATE'] = hsi['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
    hsi['YEAR'] = hsi['TRADE_DATE'].apply(lambda x: x[:4])
    hsi['MONTH'] = hsi['TRADE_DATE'].apply(lambda x: x[4:6])
    hsi['YEAR_MONTH'] = hsi['TRADE_DATE'].apply(lambda x: x[:6])
    hsi = hsi.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    hsi = hsi[hsi['MONTH'].isin(['03', '06', '09', '12'])]
    hsi['MONTH_DAY'] = hsi['MONTH'].replace('03', '0331').replace('06', '0630').replace('09', '0930').replace('12', '1231')
    hsi['REPORT_DATE'] = hsi['YEAR'] + hsi['MONTH_DAY']
    hsi = hsi[['REPORT_DATE', '恒生指数PE_TTM']].set_index('REPORT_DATE')
    hk = fund_sector[['主板-香港']].rename(columns={'主板-香港': '港股配置比例'}).merge(hsi, left_index=True, right_index=True, how='left')
    hk = hk[hk['港股配置比例'] != 0]
    hk = hk.sort_index().reset_index().rename(columns={'REPORT_HISTORY_DATE': 'REPORT_DATE'})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    sns.lineplot(ax=ax1, x='REPORT_DATE', y='港股配置比例', data=hk, label='港股配置比例', color='#F04950')
    sns.lineplot(ax=ax2, x='REPORT_DATE', y='恒生指数PE_TTM', data=hk, label='恒生指数PE_TTM', color='#6268A2')
    ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax1.set_xticklabels(labels=hk['REPORT_DATE'].unique().tolist(), rotation=90)
    ax2.set_xticklabels(labels=hk['REPORT_DATE'].unique().tolist(), rotation=90)
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    plt.title('港股配置比例及估值')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '港股配置比例与估值'))
    return

def fund_theme_plot(date, pic_path):
    """
    主题分析画图
    """
    label_type = 'THEME'
    fund_theme = FEDB().read_data(date, label_type)
    fund_theme = fund_theme[fund_theme['IS_ZC'] == 1]
    fund_theme = fund_theme[['REPORT_HISTORY_DATE', 'LABEL_NAME', 'LABEL_VALUE']]
    fund_theme = fund_theme.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_theme = fund_theme.apply(lambda x: x / x.sum(), axis=1)
    fund_theme = fund_theme.sort_index()
    fund_theme = fund_theme[['大金融', '周期', '制造', 'TMT', '消费', '其他']]
    fund_theme_latest5 = fund_theme.iloc[-5:]
    fig, ax = plt.subplots(figsize=(12, 6))
    color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B']
    for i, theme in enumerate(fund_theme_latest5.columns):
        ax.plot(fund_theme_latest5.index, fund_theme_latest5[theme], color_list[i], label=theme)
    plt.legend(loc=2)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('主题统计')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '主题统计'))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.stackplot(fund_theme.index.tolist(), fund_theme.T.values.tolist(), colors=['#D55659', '#E1777A', '#8588B7', '#626697', '#7D7D7E', '#A7A7A8'], labels=fund_theme.columns.tolist())
    plt.legend(loc=2)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('主题分布')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '主题分布'))
    return

def fund_industry_plot(date, pic_path, n=2, industry_name_1st='食品饮料'):
    """
    行业分析画图
    """
    row_list = [-(i + 1) for i in range(int(n))]

    label_type = 'INDUSTRY_SW1'
    fund_industry_1st = FEDB().read_data(date, label_type)
    fund_industry_1st = fund_industry_1st[fund_industry_1st['IS_ZC'] == 1]
    fund_industry_1st = fund_industry_1st.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_industry_1st_disp = fund_industry_1st.iloc[row_list, :].T.sort_values(date, ascending=False)
    fund_industry_1st_disp = fund_industry_1st_disp[fund_industry_1st_disp[date] != 0]
    date_list = [sorted(list(fund_industry_1st_disp.columns))[len(sorted(list(fund_industry_1st_disp.columns))) - i - 1] for i in range(len(sorted(list(fund_industry_1st_disp.columns))))]
    data_list = []
    for t in date_list:
        data_date = fund_industry_1st_disp[[t]].rename(columns={t: 'VALUE'})
        data_date['DATE'] = t
        data_list.append(data_date)
    data = pd.concat(data_list).reset_index()
    color_list = ['#C94649'] if n == 1 else ['#C94649', '#8588B7'] if n == 2 else ['#C94649', '#8588B7', '#7D7D7E'] if n == 3 else ['#C94649', '#EEB2B4', '#8588B7', '#7D7D7E'] if n == 4 else ['#C94649', '#EEB2B4', '#8588B7', '#B4B6D1', '#7D7D7E']
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(ax=ax, x='LABEL_NAME', y='VALUE', data=data, hue='DATE', hue_order=date_list, palette=color_list)
    plt.legend(loc=1)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.xlabel('')
    plt.ylabel('')
    plt.title('一级行业持仓统计')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '一级行业持仓统计'))

    mom_abs = pd.DataFrame(fund_industry_1st_disp[date_list[0]] - fund_industry_1st_disp[date_list[1]]).reset_index()
    mom_abs.columns = ['INDUSTRY_NAME', 'MOM_ABS']
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(ax=ax, x='INDUSTRY_NAME', y='MOM_ABS', data=mom_abs, palette=[color_list[0]])
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.xlabel('')
    plt.ylabel('')
    plt.title('一级行业持仓环比变化')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '一级行业持仓环比变化'))

    label_type = 'INDUSTRY_SW2'
    fund_industry_2nd = FEDB().read_data(date, label_type)
    fund_industry_2nd = fund_industry_2nd[fund_industry_2nd['IS_ZC'] == 1]
    fund_industry_2nd = fund_industry_2nd.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_industry_2nd_disp = fund_industry_2nd.iloc[row_list, :].T.sort_values(date, ascending=False).iloc[:20]
    fund_industry_2nd_disp = fund_industry_2nd_disp[fund_industry_2nd_disp[date] != 0]
    date_list = [sorted(list(fund_industry_2nd_disp.columns))[len(sorted(list(fund_industry_2nd_disp.columns))) - i - 1] for i in range(len(sorted(list(fund_industry_2nd_disp.columns))))]
    data_list = []
    for t in date_list:
        data_date = fund_industry_2nd_disp[[t]].rename(columns={t: 'VALUE'})
        data_date['DATE'] = t
        data_list.append(data_date)
    data = pd.concat(data_list).reset_index()
    color_list = ['#C94649'] if n == 1 else ['#C94649', '#8588B7'] if n == 2 else ['#C94649', '#8588B7', '#7D7D7E'] if n == 3 else ['#C94649', '#EEB2B4', '#8588B7', '#7D7D7E'] if n == 4 else ['#C94649', '#EEB2B4', '#8588B7', '#B4B6D1', '#7D7D7E']
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(ax=ax, x='LABEL_NAME', y='VALUE', data=data, hue='DATE', hue_order=date_list, palette=color_list)
    plt.legend(loc=1)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.xlabel('')
    plt.ylabel('')
    plt.title('二级行业持仓统计')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '二级行业持仓统计'))

    fund_industry_1st_single = fund_industry_1st[[industry_name_1st]].sort_index()
    fund_industry_1st_single = fund_industry_1st_single.iloc[[-5, -4, -3, -2, -1], :]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(fund_industry_1st_single.index)), fund_industry_1st_single[industry_name_1st], color='#C94649', tick_label=fund_industry_1st_single.index)
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('{0}行业持仓占比变化'.format(industry_name_1st))
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '{0}行业持仓占比变化'.format(industry_name_1st)))
    return

def fund_market_value_plot(date, pic_path):
    """
    市值分析画图
    """
    label_type = 'MARKET_VALUE_1'
    fund_mv1 = FEDB().read_data(date, label_type)
    fund_mv1 = fund_mv1[fund_mv1['IS_ZC'] == 1]
    fund_mv1 = fund_mv1.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_mv1 = fund_mv1[['HS300', 'ZZ500', 'ZZ1000', '非成分股']]
    fund_mv1.columns = ['沪深300', '中证500', '中证1000', '非成分股']
    fund_mv1 = fund_mv1.apply(lambda x: x / x.sum(), axis=1)
    fund_mv1_latest = fund_mv1.iloc[-6:]
    fig, ax1 = plt.subplots(figsize=(6, 6))
    ax2 = ax1.twinx()
    ax1.plot(fund_mv1_latest.index, fund_mv1_latest['沪深300'], color='#F04950', label='沪深300')
    ax2.plot(fund_mv1_latest.index, fund_mv1_latest['中证500'], color='#6268A2', label='中证500')
    ax2.plot(fund_mv1_latest.index, fund_mv1_latest['中证1000'], color='#959595', label='中证1000')
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax1.set_ylim([0.4, 0.6])
    ax2.set_ylim([0.1, 0.2])
    ax1.set_xticklabels(labels=fund_mv1_latest.index, rotation=90)
    ax2.set_xticklabels(labels=fund_mv1_latest.index, rotation=90)
    plt.xticks(rotation=90)
    ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('成分股占比变化')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '成分股占比变化'))
    # fig, ax = plt.subplots(figsize=(6, 6))
    # ax.plot(fund_mv1_latest.index, fund_mv1_latest['沪深300'], color='#F04950', label='沪深300')
    # ax.plot(fund_mv1_latest.index, fund_mv1_latest['中证500'], color='#6268A2', label='中证500')
    # ax.plot(fund_mv1_latest.index, fund_mv1_latest['中证1000'], color='#959595', label='中证1000')
    # ax.legend(loc=2)
    # ax.set_ylim([0.0, 0.5])
    # ax.set_xticklabels(labels=fund_mv1_latest.index, rotation=90)
    # ax.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    # plt.title('成分股占比变化')
    # plt.tight_layout()
    # plt.savefig('{0}{1}'.format(pic_path, '成分股占比变化'))

    label_type = 'MARKET_VALUE_2'
    fund_mv2 = FEDB().read_data(date, label_type)
    fund_mv2 = fund_mv2[fund_mv2['IS_ZC'] == 1]
    fund_mv2 = fund_mv2.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_mv2 = fund_mv2[['SZ50', 'ZZ100', 'SZ180', 'HS300', 'TOTAL']]
    fund_mv2.columns = ['上证50', '中证100', '上证180', '沪深300', '总计']
    fund_mv2 = fund_mv2.apply(lambda x: x / x.iloc[-1], axis=1)
    fund_mv2_latest = fund_mv2.iloc[-6:, :-1]
    fig, ax = plt.subplots(figsize=(6, 6))
    color_list = ['#F04950', '#6268A2', '#959595', '#333335']
    for i, index in enumerate(fund_mv2_latest.columns):
        ax.plot(fund_mv2_latest.index, fund_mv2_latest[index], color_list[i], label=index)
    plt.legend(loc=2)
    # plt.ylim([0.0, 0.5])
    plt.xticks(rotation=90)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('权重股占比变化')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '权重股占比变化'))
    return

def fund_style_plot(date, pic_path):
    """
    风格分析画图
    """
    label_type = 'STYLE_1'
    fund_style1 = FEDB().read_data(date, label_type)
    fund_style1 = fund_style1[fund_style1['IS_ZC'] == 1]
    fund_style1 = fund_style1.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_style1 = fund_style1.drop('TOTAL', axis=1)
    fund_style1 = fund_style1.apply(lambda x: x / x.sum(), axis=1)
    fund_style1_latest = fund_style1[['成长', '平衡', '价值']].iloc[-6:]
    fig, ax1 = plt.subplots(figsize=(6, 6))
    ax2 = ax1.twinx()
    ax1.plot(fund_style1_latest.index, fund_style1_latest['成长'], color='#F04950', label='成长')
    ax2.plot(fund_style1_latest.index, fund_style1_latest['价值'], color='#6268A2', label='价值')
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax1.set_ylim([0.50, 0.85])
    ax2.set_ylim([0.15, 0.40])
    ax1.set_xticklabels(labels=fund_style1_latest.index, rotation=90)
    ax2.set_xticklabels(labels=fund_style1_latest.index, rotation=90)
    plt.xticks(rotation=90)
    ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('风格统计')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '风格统计'))
    # fig, ax1 = plt.subplots(figsize=(6, 6))
    # ax2 = ax1.twinx()
    # ax1.plot(fund_style1_latest.index, fund_style1_latest['成长'], color='#F04950', label='成长')
    # ax2.plot(fund_style1_latest.index, fund_style1_latest['平衡'], color='#6268A2', label='平衡')
    # ax2.plot(fund_style1_latest.index, fund_style1_latest['价值'], color='#959595', label='价值')
    # ax1.legend(loc=2)
    # ax2.legend(loc=1)
    # ax1.set_ylim([0.10, 0.70])
    # ax2.set_ylim([0.10, 0.50])
    # ax1.set_xticklabels(labels=fund_style1_latest.index, rotation=90)
    # ax2.set_xticklabels(labels=fund_style1_latest.index, rotation=90)
    # plt.xticks(rotation=90)
    # ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    # ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    # plt.title('风格统计')
    # plt.tight_layout()
    # plt.savefig('{0}{1}'.format(pic_path, '风格统计'))

    label_type = 'STYLE_2'
    fund_style2 = FEDB().read_data(date, label_type)
    fund_style2 = fund_style2[fund_style2['IS_ZC'] == 1]
    fund_style2 = fund_style2.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_style2 = fund_style2.drop('TOTAL', axis=1)
    fund_style2 = fund_style2.apply(lambda x: x / x.sum(), axis=1)
    fund_style2_latest = fund_style2[['大盘成长', '大盘平衡', '大盘价值', '中盘成长', '中盘平衡', '中盘价值', '小盘成长', '小盘平衡', '小盘价值']].iloc[-6:]
    fig, ax1 = plt.subplots(figsize=(6, 6))
    ax2 = ax1.twinx()
    ax1.plot(fund_style2_latest.index, fund_style2_latest['大盘成长'], color='#F04950', label='大盘成长')
    color_list = ['#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C', '#44488E', '#BA67E9']
    for i, style in enumerate(fund_style2_latest.columns[1:]):
        ax2.plot(fund_style2_latest.index, fund_style2_latest[style], color_list[i], label=style)
    ax1.legend(loc=2)
    ax2.legend(loc=1)
    ax1.set_ylim([0.3, 0.7])
    ax2.set_ylim([0.0, 0.3])
    ax1.set_xticklabels(labels=fund_style2_latest.index, rotation=90)
    ax2.set_xticklabels(labels=fund_style2_latest.index, rotation=90)
    plt.xticks(rotation=90)
    ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    plt.title('细分风格统计')
    plt.tight_layout()
    plt.savefig('{0}{1}'.format(pic_path, '细分风格统计'))
    # fig, ax1 = plt.subplots(figsize=(6, 6))
    # ax2 = ax1.twinx()
    # color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C', '#44488E', '#BA67E9']
    # ax1.plot(fund_style2_latest.index, fund_style2_latest['大盘成长'], color='#F04950', label='大盘成长')
    # ax1.plot(fund_style2_latest.index, fund_style2_latest['中盘成长'], color='#6268A2', label='中盘成长')
    # ax1.plot(fund_style2_latest.index, fund_style2_latest['小盘成长'], color='#959595', label='小盘成长')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['大盘平衡'], color='#333335', label='大盘平衡')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['中盘平衡'], color='#EE703F', label='中盘平衡')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['小盘平衡'], color='#7E4A9B', label='小盘平衡')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['大盘价值'], color='#8A662C', label='大盘价值')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['中盘价值'], color='#44488E', label='中盘价值')
    # ax2.plot(fund_style2_latest.index, fund_style2_latest['小盘价值'], color='#BA67E9', label='小盘价值')
    # ax1.legend(loc=2)
    # ax2.legend(loc=1)
    # ax1.set_ylim([0.0, 0.4])
    # ax2.set_ylim([0.0, 0.4])
    # ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    # ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent))
    # ax1.set_xticklabels(labels=fund_style2_latest.index, rotation=90)
    # ax2.set_xticklabels(labels=fund_style2_latest.index, rotation=90)
    # plt.title('细分风格统计')
    # plt.tight_layout()
    # plt.savefig('{0}{1}'.format(pic_path, '细分风格统计'))
    return

def fund_barra(date, pic_path):
    label_type = 'BARRA'
    fund_barra = FEDB().read_data(date, label_type)
    fund_barra = fund_barra[fund_barra['IS_ZC'] == 1]
    fund_barra = fund_barra.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
    fund_barra.columns = ['Beta', '价值', '盈利', '成长', '杠杆率', '流动性', '动量', '波动率', '市值', '中市值']
    fund_barra = fund_barra.iloc[-2:].T
    fund_barra['变化'] = (fund_barra.iloc[:, -1] - fund_barra.iloc[:, -2])
    fund_barra.to_excel('{0}fund_barra.xlsx'.format(pic_path))
    return

def fund_holding(date, pic_path):
    label_type = 'STOCK'
    fund_stock = FEDB().read_data(date, label_type)
    fund_stock = fund_stock[fund_stock['IS_ZC'] == 1]
    date_list = sorted(fund_stock['REPORT_HISTORY_DATE'].unique().tolist())
    fund_stock = fund_stock[['REPORT_HISTORY_DATE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    fund_stock['LABEL_NAME'] = fund_stock['LABEL_NAME'].apply(lambda x: x.split('_')[0])
    fund_stock['RANK'] = fund_stock[['REPORT_HISTORY_DATE', 'LABEL_NAME', 'LABEL_VALUE']].groupby(['REPORT_HISTORY_DATE', 'LABEL_NAME']).rank(method='first', ascending=False)
    fund_stock_list = []
    for td in date_list[-6:]:
        fund_stock_date = fund_stock[fund_stock['REPORT_HISTORY_DATE'] == td].sort_values(['LABEL_NAME', 'RANK'])
        fund_stock_date['一级行业'] = fund_stock_date.apply(lambda x: x['LABEL_NAME'] + '_' + str(int(x['RANK'])), axis=1)
        fund_stock_date = fund_stock_date.set_index('一级行业')
        fund_stock_date = fund_stock_date[['LABEL_VALUE_STRING']].rename(columns={'LABEL_VALUE_STRING': td})
        fund_stock_list.append(fund_stock_date)
    fund_stock = pd.concat(fund_stock_list, axis=1)
    fund_stock = fund_stock[date_list[::-1][:6]]
    fund_stock = fund_stock.reset_index()
    fund_stock['排名'] = fund_stock['一级行业'].apply(lambda x: x.split('_')[1])
    fund_stock['一级行业'] = fund_stock['一级行业'].apply(lambda x: x.split('_')[0])
    fund_stock['主题'] = fund_stock['一级行业'].apply(lambda x: industry_theme_dic[x])
    fund_stock['主题'] = fund_stock['主题'].astype('category')
    fund_stock['主题'].cat.reorder_categories(['制造', '消费', '周期', 'TMT', '大金融', '其他'], inplace=True)
    fund_stock = fund_stock.sort_values(['主题','一级行业', '排名'], ascending=[True, True, True])
    fund_stock.to_excel('{0}fund_stock.xlsx'.format(pic_path))
    return

def holding_analysis_plot(date, pic_path):
    """
    公募基金持仓分析画图
    """
    fund_overview_plot(date, pic_path)
    fund_valuation_plot(date, pic_path)
    fund_sector_plot(date, pic_path)
    fund_theme_plot(date, pic_path)
    fund_industry_plot(date, pic_path)
    fund_market_value_plot(date, pic_path)
    fund_style_plot(date, pic_path)
    fund_barra(date, pic_path)
    fund_holding(date, pic_path)
    return


if __name__ == "__main__":
    date = '20220630'
    pic_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/'
    holding_analysis_plot(date, pic_path)


