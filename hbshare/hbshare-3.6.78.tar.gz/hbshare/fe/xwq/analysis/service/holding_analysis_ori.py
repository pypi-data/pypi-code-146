# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.xwq.analysis.utils.const_var import TimeDateFormat
from hbshare.fe.xwq.analysis.utils.timedelta_utils import TimeDateUtil
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                  '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功


def to_percent(temp, position):
    return '%1.0f'%(temp) + '%'

def to_percent_r2(temp, position):
    return '%0.01f'%(temp) + '%'

def to_100percent(temp, position):
    return '%1.0f'%(temp * 100) + '%'

def to_100percent_r2(temp, position):
    return '%0.01f'%(temp * 100) + '%'

def filter_extreme_percentile(ser, min=0.1, max=0.9):
    ser = ser.sort_values()
    ser_q = ser.quantile([min, max])
    return np.clip(ser, ser_q.iloc[0], ser_q.iloc[1])

def get_cal_and_trade_cal(start, end):
    """
    获取交易日期
    """
    cal = HBDB().read_cal(start, end)
    cal = cal.rename(columns={'JYRQ': 'TRADE_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    cal['IS_OPEN'] = cal['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    cal['IS_WEEK_END'] = cal['IS_WEEK_END'].fillna(0).astype(int)
    cal['IS_MONTH_END'] = cal['IS_MONTH_END'].fillna(0).astype(int)
    cal = cal.sort_values('TRADE_DATE')
    trade_cal = cal[cal['IS_OPEN'] == 1]
    trade_cal['RECENT_TRADE_DATE'] = trade_cal['TRADE_DATE']
    trade_cal['PREV_TRADE_DATE'] = trade_cal['TRADE_DATE'].shift(1)
    trade_cal = trade_cal[['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
    cal = cal.merge(trade_cal[['TRADE_DATE', 'RECENT_TRADE_DATE']], on=['TRADE_DATE'], how='left')
    cal['RECENT_TRADE_DATE'] = cal['RECENT_TRADE_DATE'].fillna(method='ffill')
    cal = cal.merge(trade_cal[['TRADE_DATE', 'PREV_TRADE_DATE']], on=['TRADE_DATE'], how='left')
    cal['PREV_TRADE_DATE'] = cal['PREV_TRADE_DATE'].fillna(method='bfill')
    cal = cal[['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
    return cal, trade_cal

def preload_stock_valuation(dates):
    """
    获取股票估值数据
    """
    stock_valuation_list = []
    star_stock_valuation_list = []
    for date in dates:
        print(date)
        stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
        stock_valuation_list.append(stock_valuation_date)
        star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
        star_stock_valuation_list.append(star_stock_valuation_date)
    stock_valuation = pd.concat(stock_valuation_list)
    stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_valuation.hdf', key='table', mode='w')
    star_stock_valuation = pd.concat(star_stock_valuation_list)
    star_stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/star_stock_valuation.hdf', key='table', mode='w')
    return stock_valuation, star_stock_valuation

def preload_index_cons():
    """
    获取指数成分股数据
    """
    index_dic = {
        'HS300': '3145',
        'ZZ500': '4978',
        'ZZ1000': '39144',
        'ZZ100': '4293',
        'SZ50': '46',
        'SZ100': '16898',
        'SZ180': '30',
        'JCDP': '3472',
        'JCZP': '3473',
        'JCXP': '3474',
        'JCCZ': '10052',
        'JCJZ': '10053',
        'JCDPCZ': '10054',
        'JCDPJZ': '10055',
        'JCZPCZ': '10056',
        'JCZPJZ': '10057',
        'JCXPCZ': '10058',
        'JCXPJZ': '10059'
    }
    index_cons_list = []
    for index in index_dic.keys():
        print(index)
        index_cons = HBDB().read_index_cons(index_dic[index])
        index_cons['INDEX'] = index
        index_cons_list.append(index_cons)
    index_cons = pd.concat(index_cons_list)
    index_cons.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/index_cons.hdf', key='table', mode='w')
    return

def fund_info(date):
    """
    研究对象
    # todo: 读取基金数据的时候已做了存续中处理
    # todo: kffb字段nan值的处理
    """
    # 正常运行中的普通股票型、偏股混合型、灵活配置型公募基金
    fund = HBDB().read_stock_fund_info()
    fund = fund.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'BEGIN_DATE', 'zzrq': 'END_DATE', 'ejfl': 'FUND_TYPE', 'kffb': 'OPEN_CLOSE'})
    fund = fund.dropna(subset=['BEGIN_DATE'])
    fund['END_DATE'] = fund['END_DATE'].fillna(20990101)
    fund['BEGIN_DATE'] = fund['BEGIN_DATE'].astype(str)
    fund['END_DATE'] = fund['END_DATE'].astype(str)
    # 成立距计算日期满2年
    date_before = TimeDateUtil.get_previous_date_str(date, TimeDateFormat.YMD.value, TimeDateFormat.YMD.value, 730)
    fund = fund[fund['END_DATE'] >= date]
    # fund = fund[(fund['BEGIN_DATE'] <= date_before) & (fund['END_DATE'] >= date)]
    # fund = fund.sort_values(['FUND_FULL_NAME', 'FUND_CODE']).drop_duplicates('FUND_FULL_NAME')
    # 成立以来股票占基金净资产的比例均值不低于60%
    fund_gptzzjb = HBDB().read_fund_gptzzjb_given_codes(fund['FUND_CODE'].unique().tolist())
    fund_gptzzjb = fund_gptzzjb.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'gptzzjb': 'EQUITY_IN_NA'})
    fund_gptzzjb['REPORT_DATE'] = fund_gptzzjb['REPORT_DATE'].astype(str)
    fund_gptzzjb_mean = fund_gptzzjb[['FUND_CODE', 'EQUITY_IN_NA']].groupby('FUND_CODE').mean().reset_index()
    fund_gptzzjb_mean = fund_gptzzjb_mean[fund_gptzzjb_mean['EQUITY_IN_NA'] >= 60]
    fund = fund[fund['FUND_CODE'].isin(fund_gptzzjb_mean['FUND_CODE'].unique().tolist())]
    # 近2年以来股票占基金净资产的比例均不低于50%
    fund_gptzzjb = fund_gptzzjb[(fund_gptzzjb['REPORT_DATE'] >= date_before) & (fund_gptzzjb['REPORT_DATE'] <= date)]
    fund_gptzzjb_min = fund_gptzzjb[['FUND_CODE', 'EQUITY_IN_NA']].groupby('FUND_CODE').min().reset_index()
    fund_gptzzjb_min = fund_gptzzjb_min[fund_gptzzjb_min['EQUITY_IN_NA'] >= 50]
    fund = fund[fund['FUND_CODE'].isin(fund_gptzzjb_min['FUND_CODE'].unique().tolist())]
    # 统计分析
    fund['OPEN_CLOSE'] = fund['OPEN_CLOSE'].fillna('0')
    fund_overview = pd.DataFrame(index=['普通股票型基金', '偏股混合型基金', '灵活配置型基金'], columns=['开放式基金', '封闭式基金'])
    fund_overview.loc['普通股票型基金', '开放式基金'] = len(fund[(fund['FUND_TYPE'] == '13') & (fund['OPEN_CLOSE'] == '0')])
    fund_overview.loc['普通股票型基金', '封闭式基金'] = len(fund[(fund['FUND_TYPE'] == '13') & (fund['OPEN_CLOSE'] == '1')])
    fund_overview.loc['偏股混合型基金', '开放式基金'] = len(fund[(fund['FUND_TYPE'] == '37') & (fund['OPEN_CLOSE'] == '0')])
    fund_overview.loc['偏股混合型基金', '封闭式基金'] = len(fund[(fund['FUND_TYPE'] == '37') & (fund['OPEN_CLOSE'] == '1')])
    fund_overview.loc['灵活配置型基金', '开放式基金'] = len(fund[(fund['FUND_TYPE'] == '35') & (fund['OPEN_CLOSE'] == '0')])
    fund_overview.loc['灵活配置型基金', '封闭式基金'] = len(fund[(fund['FUND_TYPE'] == '35') & (fund['OPEN_CLOSE'] == '1')])
    # 入库
    data = fund_overview.unstack().reset_index()
    data.columns = ['OPEN_CLOSE', 'TYPE', 'COUNT']
    data['REPORT_DATE'] = date
    data['REPORT_HISTORY_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'OVERVIEW'
    data['LABEL_NAME'] = data.apply(lambda x: x['TYPE'] + '_' + x['OPEN_CLOSE'], axis=1)
    data['LABEL_VALUE'] = data['COUNT']
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return fund

def fund_valuation(date, fund_zc_holding, fund_zc_holding_diff):
    """
    估值分析
    # todo: 港股估值数据暂时取不到
    # todo: 平均估值差算法(去除了PE<=0的，占比2.44%)
    """
    preload_stock_valuation(fund_zc_holding['RECENT_TRADE_DATE'].unique().tolist())
    stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_valuation.hdf', key='table')
    star_stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/star_stock_valuation.hdf', key='table')
    stock_valuation = stock_valuation.rename(columns={'PE_TTM': 'PE(TTM)', 'PB_LF': 'PB(LF)'})
    star_stock_valuation = star_stock_valuation.rename(columns={'PE_TTM': 'PE(TTM)', 'PB_LF': 'PB(LF)'})
    stock_valuation = stock_valuation[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE', 'PE(TTM)', 'PB(LF)']]
    star_stock_valuation = star_stock_valuation[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE', 'PE(TTM)', 'PB(LF)']]
    stock_valuation = pd.concat([stock_valuation, star_stock_valuation]).sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
    fund_zc_holding = fund_zc_holding.merge(stock_valuation.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    fund_zc_holding_diff = fund_zc_holding_diff.merge(stock_valuation.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    pe = fund_zc_holding.dropna(subset=['PE(TTM)'])
    pb = fund_zc_holding.dropna(subset=['PB(LF)'])

    pe['PE_MARK'] = np.nan
    pe.loc[(pe['PE(TTM)'] > 0) & (pe['PE(TTM)'] <= 30), 'PE_MARK'] = 'low'
    pe.loc[(pe['PE(TTM)'] > 30) & (pe['PE(TTM)'] <= 50), 'PE_MARK'] = 'middle'
    pe.loc[(pe['PE(TTM)'] > 50) | (pe['PE(TTM)'] <= 0), 'PE_MARK'] = 'high'
    pe = pe[['REPORT_DATE', 'PE_MARK', 'TICKER_SYMBOL']].groupby(['REPORT_DATE', 'PE_MARK']).count().reset_index().rename(columns={'TICKER_SYMBOL': 'PE_COUNT'})
    pe = pe.pivot(index='REPORT_DATE', columns='PE_MARK', values='PE_COUNT').fillna(0)
    # 入库
    data = pe.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'VALUATION'
    data['LABEL_NAME'] = data['LABEL_NAME'].apply(lambda x: 'PE_' + x)
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    pb['PB_MARK'] = np.nan
    pb.loc[(pb['PB(LF)'] > 0) & (pb['PB(LF)'] <= 5), 'PB_MARK'] = 'low'
    pb.loc[(pb['PB(LF)'] > 5) | (pb['PB(LF)'] <= 0), 'PB_MARK'] = 'high'
    pb = pb[['REPORT_DATE', 'PB_MARK', 'TICKER_SYMBOL']].groupby(['REPORT_DATE', 'PB_MARK']).count().reset_index().rename(columns={'TICKER_SYMBOL': 'PB_COUNT'})
    pb = pb.pivot(index='REPORT_DATE', columns='PB_MARK', values='PB_COUNT').fillna(0)
    # 入库
    data = pb.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'VALUATION'
    data['LABEL_NAME'] = data['LABEL_NAME'].apply(lambda x: 'PB_' + x)
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    # 估值变化
    # 去掉前后两期持仓数量无变化的
    date_list = sorted(fund_zc_holding['REPORT_DATE'].unique().tolist())
    fund_zc_holding_date = fund_zc_holding[fund_zc_holding['REPORT_DATE'] == date_list[-1]]
    fund_zc_holding_last_date = fund_zc_holding[fund_zc_holding['REPORT_DATE'] == date_list[-2]]
    fund_zc_holding_date = fund_zc_holding_date[['FUND_CODE', 'TICKER_SYMBOL', 'HOLDING_AMOUNT']].rename(columns={'HOLDING_AMOUNT': 'HOLDING_AMOUNT_DATE'})
    fund_zc_holding_last_date = fund_zc_holding_last_date[['FUND_CODE', 'TICKER_SYMBOL', 'HOLDING_AMOUNT']].rename(columns={'HOLDING_AMOUNT': 'HOLDING_AMOUNT_LAST_DATE'})
    fund_zc_holding_nc = fund_zc_holding_date.merge(fund_zc_holding_last_date, on=['FUND_CODE', 'TICKER_SYMBOL'], how='outer').fillna(0.0)
    fund_zc_holding_nc = fund_zc_holding_nc[fund_zc_holding_nc['HOLDING_AMOUNT_DATE'] == fund_zc_holding_nc['HOLDING_AMOUNT_LAST_DATE']]
    fund_zc_holding_nc['IS_REMOVE'] = 1.0
    fund_zc_holding_diff = fund_zc_holding_diff.merge(fund_zc_holding_nc[['FUND_CODE', 'TICKER_SYMBOL', 'IS_REMOVE']], on=['FUND_CODE', 'TICKER_SYMBOL'], how='left')
    fund_zc_holding_diff['IS_REMOVE'] = fund_zc_holding_diff['IS_REMOVE'].fillna(0.0)
    fund_zc_holding_diff = fund_zc_holding_diff[fund_zc_holding_diff['IS_REMOVE'] == 0.0]
    # 去掉价格涨跌因素
    trade_date_list = sorted(stock_valuation['TRADE_DATE'].unique().tolist())
    stock_daily_k_date = HBDB().read_stock_daily_k_given_date(trade_date_list[-1])
    star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(trade_date_list[-1])
    stock_daily_k_date = pd.concat([stock_daily_k_date, star_stock_daily_k_date])
    stock_daily_k_last_date = HBDB().read_stock_daily_k_given_date(trade_date_list[-2])
    star_stock_daily_k_last_date = HBDB().read_star_stock_daily_k_given_date(trade_date_list[-2])
    stock_daily_k_last_date = pd.concat([stock_daily_k_last_date, star_stock_daily_k_last_date])
    fund_aum_date = HBDB().read_fund_scale_given_date(date_list[-1])
    fund_aum_date = fund_aum_date[fund_aum_date['BBLB1'] == 13]
    fund_aum_date = fund_aum_date.sort_values(['JJDM', 'JSRQ', 'GGRQ']).drop_duplicates(['JJDM', 'JSRQ'], keep='last')
    fund_aum_date = fund_aum_date.rename(columns={'JJDM': 'FUND_CODE', 'ZCJZ': 'AUM'})
    fund_aum_last_date = HBDB().read_fund_scale_given_date(date_list[-2])
    fund_aum_last_date = fund_aum_last_date[fund_aum_last_date['BBLB1'] == 13]
    fund_aum_last_date = fund_aum_last_date.sort_values(['JJDM', 'JSRQ', 'GGRQ']).drop_duplicates(['JJDM', 'JSRQ'], keep='last')
    fund_aum_last_date = fund_aum_last_date.rename(columns={'JJDM': 'FUND_CODE', 'ZCJZ': 'AUM'})
    fund_zc_holding_date = fund_zc_holding_date.merge(stock_daily_k_date[['TICKER_SYMBOL', 'CLOSE_PRICE']], on=['TICKER_SYMBOL'], how='left').rename(columns={'CLOSE_PRICE': 'CLOSE_PRICE_DATE'})
    fund_zc_holding_last_date = fund_zc_holding_last_date.merge(stock_daily_k_last_date[['TICKER_SYMBOL', 'CLOSE_PRICE']], on=['TICKER_SYMBOL'], how='left').rename(columns={'CLOSE_PRICE': 'CLOSE_PRICE_LAST_DATE'})
    fund_zc_holding_date = fund_zc_holding_date.merge(fund_aum_date[['FUND_CODE', 'AUM']], on=['FUND_CODE'], how='left').rename(columns={'AUM': 'AUM_DATE'})
    fund_zc_holding_last_date = fund_zc_holding_last_date.merge(fund_aum_last_date[['FUND_CODE', 'AUM']], on=['FUND_CODE'], how='left').rename(columns={'AUM': 'AUM_LAST_DATE'})
    fund_zc_holding_date = fund_zc_holding_date.dropna()
    fund_zc_holding_last_date = fund_zc_holding_last_date.dropna()
    fund_zc_holding_p = fund_zc_holding_date.merge(fund_zc_holding_last_date, on=['FUND_CODE', 'TICKER_SYMBOL'], how='outer').fillna(0.0)
    fund_zc_holding_p['MV_IN_NA_DATE'] = fund_zc_holding_p['HOLDING_AMOUNT_LAST_DATE'] * fund_zc_holding_p['CLOSE_PRICE_DATE'] / fund_zc_holding_p['AUM_LAST_DATE']
    fund_zc_holding_p['MV_IN_NA_LAST_DATE'] = fund_zc_holding_p['HOLDING_AMOUNT_LAST_DATE'] * fund_zc_holding_p['CLOSE_PRICE_LAST_DATE'] / fund_zc_holding_p['AUM_LAST_DATE']
    fund_zc_holding_p['MV_IN_NA_P_DIFF'] = fund_zc_holding_p['MV_IN_NA_DATE'] - fund_zc_holding_p['MV_IN_NA_LAST_DATE']
    fund_zc_holding_diff = fund_zc_holding_diff.merge(fund_zc_holding_p[['FUND_CODE', 'TICKER_SYMBOL', 'MV_IN_NA_P_DIFF']], on=['FUND_CODE', 'TICKER_SYMBOL'], how='left').fillna(0.0)
    fund_zc_holding_diff['MV_IN_NA_DIFF'] = fund_zc_holding_diff['MV_IN_NA_DIFF'] - fund_zc_holding_diff['MV_IN_NA_P_DIFF'] * 100.0
    # 计算平均估值差
    pe_diff = fund_zc_holding_diff.dropna(subset=['PE(TTM)'])
    pe_diff = pe_diff[pe_diff['PE(TTM)'] > 0]
    pe_diff_up = pe_diff[pe_diff['MV_IN_NA_DIFF'] > 0]
    pe_diff_up_weight = pe_diff_up[['REPORT_DATE', 'MV_IN_NA_DIFF']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'MV_IN_NA_DIFF': 'TOTAL_MV_IN_NA_DIFF'})
    pe_diff_up = pe_diff_up.merge(pe_diff_up_weight, on=['REPORT_DATE'], how='left')
    pe_diff_up['WEIGHTED_PE(TTM)_UP_DIFF'] = pe_diff_up['PE(TTM)'] * pe_diff_up['MV_IN_NA_DIFF'] / pe_diff_up['TOTAL_MV_IN_NA_DIFF']
    pe_diff_up = pe_diff_up[['REPORT_DATE', 'WEIGHTED_PE(TTM)_UP_DIFF']].groupby(['REPORT_DATE']).sum().reset_index()
    pe_diff_down = pe_diff[pe_diff['MV_IN_NA_DIFF'] < 0]
    pe_diff_down['MV_IN_NA_DIFF'] = pe_diff['MV_IN_NA_DIFF'] * (-1.0)
    pe_diff_down_weight = pe_diff_down[['REPORT_DATE', 'MV_IN_NA_DIFF']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'MV_IN_NA_DIFF': 'TOTAL_MV_IN_NA_DIFF'})
    pe_diff_down = pe_diff_down.merge(pe_diff_down_weight, on=['REPORT_DATE'], how='left')
    pe_diff_down['WEIGHTED_PE(TTM)_DOWN_DIFF'] = pe_diff_down['PE(TTM)'] * pe_diff_down['MV_IN_NA_DIFF'] / pe_diff_down['TOTAL_MV_IN_NA_DIFF']
    pe_diff_down = pe_diff_down[['REPORT_DATE', 'WEIGHTED_PE(TTM)_DOWN_DIFF']].groupby(['REPORT_DATE']).sum().reset_index()
    pe_diff = pe_diff_up.merge(pe_diff_down, on=['REPORT_DATE'], how='left').fillna(0.0)
    pe_diff['VALUATION_DIFF'] = pe_diff['WEIGHTED_PE(TTM)_UP_DIFF'] - pe_diff['WEIGHTED_PE(TTM)_DOWN_DIFF']
    # 入库
    data = pe_diff[['REPORT_DATE', 'VALUATION_DIFF']].copy()
    data.columns = ['REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'VALUATION_DIFF'
    data['LABEL_NAME'] = 'PE_平均估值差'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    # 核心资产估值溢价：基金重仓股 / 非基金重仓股的PEPB中位数之比
    fund_zc_holding['IS_ZC'] = 1
    stock = stock_valuation[stock_valuation['TRADE_DATE'].isin(fund_zc_holding['RECENT_TRADE_DATE'].unique().tolist())]
    stock = stock.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}).merge(fund_zc_holding[['RECENT_TRADE_DATE', 'TICKER_SYMBOL', 'IS_ZC']].drop_duplicates(), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    # fund_zc_holding_ = fund_zc_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).groupby(['FUND_CODE', 'REPORT_DATE']).head(10)
    # fund_zc_holding_['IS_ZC'] = 1
    # stock = stock_valuation[stock_valuation['TRADE_DATE'].isin(fund_zc_holding['RECENT_TRADE_DATE'].unique().tolist())]
    # stock = stock.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}).merge(fund_zc_holding_[['RECENT_TRADE_DATE', 'TICKER_SYMBOL', 'IS_ZC']].drop_duplicates(), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    stock['IS_ZC'] = stock['IS_ZC'].fillna(0)
    stock = stock.merge(fund_zc_holding[['RECENT_TRADE_DATE', 'REPORT_DATE']].drop_duplicates(), on=['RECENT_TRADE_DATE'], how='left')
    pe_quantile = stock[['REPORT_DATE', 'IS_ZC', 'PE(TTM)']].groupby(['REPORT_DATE', 'IS_ZC']).quantile().reset_index()
    pe_quantile = pe_quantile.pivot(index='REPORT_DATE', columns='IS_ZC', values='PE(TTM)')
    pe_quantile['RATIO'] = pe_quantile[1] / pe_quantile[0]
    # 入库
    data = pe_quantile[['RATIO']].unstack().reset_index().drop('IS_ZC', axis=1)
    data.columns = ['REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'VALUATION_PREMIUM'
    data['LABEL_NAME'] = 'PE_核心资产估值溢价'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    pb_quantile = stock[['REPORT_DATE', 'IS_ZC', 'PB(LF)']].groupby(['REPORT_DATE', 'IS_ZC']).quantile().reset_index()
    pb_quantile = pb_quantile.pivot(index='REPORT_DATE', columns='IS_ZC', values='PB(LF)')
    pb_quantile['RATIO'] = pb_quantile[1] / pb_quantile[0]
    # 入库
    data = pb_quantile[['RATIO']].unstack().reset_index().drop('IS_ZC', axis=1)
    data.columns = ['REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'VALUATION_PREMIUM'
    data['LABEL_NAME'] = 'PB_核心资产估值溢价'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_sector(date, fund_zc_holding):
    """
    板块分析
    """
    fund_zc_holding['SECTOR'] = fund_zc_holding['TICKER_SYMBOL'].apply(lambda x: '主板-上海' if x[:2] == '60' else '主板-深圳' if x[:2] == '00' else '创业板-深圳'if x[:2] == '30' else '科创版-上海' if x[:2] == '68' else '主板-香港')
    fund_zc_holding_sector = fund_zc_holding[['REPORT_DATE', 'SECTOR', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'SECTOR']).sum().reset_index()
    fund_zc_holding_sector = fund_zc_holding_sector.pivot(index='REPORT_DATE', columns='SECTOR', values='HOLDING_MARKET_VALUE').fillna(0.0)
    # 入库
    data = fund_zc_holding_sector.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'SECTOR'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_theme(date, fund_zc_holding):
    """
    主题分析
    """
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna(20990101)
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
    stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
    fund_zc_holding_industry = fund_zc_holding.merge(stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID']], on=['TICKER_SYMBOL'], how='left')
    industry_theme = HBDB().read_industry_theme()
    industry_theme.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/industry_theme.hdf', key='table', mode='w')
    industry_theme = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/industry_theme.hdf', key='table')
    industry_theme = industry_theme.rename(columns={'fldm': 'INDUSTRY_ID', 'hyzt': 'THEME_NAME', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE'})
    industry_theme = industry_theme.dropna(subset=['BEGIN_DATE'])
    industry_theme['END_DATE'] = industry_theme['END_DATE'].fillna(20990101)
    industry_theme['BEGIN_DATE'] = industry_theme['BEGIN_DATE'].astype(int).astype(str)
    industry_theme['END_DATE'] = industry_theme['END_DATE'].astype(int).astype(str)
    fund_zc_holding_theme = fund_zc_holding_industry.merge(industry_theme[['INDUSTRY_ID', 'THEME_NAME', 'BEGIN_DATE', 'END_DATE']], on=['INDUSTRY_ID'], how='left')
    fund_zc_holding_theme = fund_zc_holding_theme[(fund_zc_holding_theme['REPORT_DATE'] >= fund_zc_holding_theme['BEGIN_DATE']) & (fund_zc_holding_theme['REPORT_DATE'] < fund_zc_holding_theme['END_DATE'])]
    fund_zc_holding_theme = fund_zc_holding_theme.drop(['BEGIN_DATE', 'END_DATE'], axis=1)
    fund_zc_holding_theme = fund_zc_holding_theme.dropna(subset=['THEME_NAME'])
    fund_zc_holding_theme = fund_zc_holding_theme[['REPORT_DATE', 'THEME_NAME', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'THEME_NAME']).sum().reset_index()
    fund_zc_holding_theme_total = fund_zc_holding_theme[['REPORT_DATE', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'HOLDING_MARKET_VALUE': 'TOTAL_HOLDING_MARKET_VALUE'})
    fund_zc_holding_theme = fund_zc_holding_theme.merge(fund_zc_holding_theme_total, on=['REPORT_DATE'], how='left')
    fund_zc_holding_theme['WEIGHT'] = fund_zc_holding_theme['HOLDING_MARKET_VALUE'] / fund_zc_holding_theme['TOTAL_HOLDING_MARKET_VALUE']
    fund_zc_holding_theme = fund_zc_holding_theme.pivot(index='REPORT_DATE', columns='THEME_NAME', values='WEIGHT').fillna(0.0)
    # 入库
    data = fund_zc_holding_theme.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'THEME'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_industry(date, fund_zc_holding):
    """
    行业分析
    """
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna(20990101)
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]

    stock_industry_sw1 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
    fund_zc_holding_industry_sw1 = fund_zc_holding.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
    fund_zc_holding_industry_sw1 = fund_zc_holding_industry_sw1.dropna(subset=['INDUSTRY_NAME'])
    fund_zc_holding_industry_sw1 = fund_zc_holding_industry_sw1[['REPORT_DATE', 'INDUSTRY_NAME', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
    fund_zc_holding_industry_sw1_total = fund_zc_holding_industry_sw1[['REPORT_DATE', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'HOLDING_MARKET_VALUE': 'TOTAL_HOLDING_MARKET_VALUE'})
    fund_zc_holding_industry_sw1 = fund_zc_holding_industry_sw1.merge(fund_zc_holding_industry_sw1_total, on=['REPORT_DATE'], how='left')
    fund_zc_holding_industry_sw1['WEIGHT'] = fund_zc_holding_industry_sw1['HOLDING_MARKET_VALUE'] / fund_zc_holding_industry_sw1['TOTAL_HOLDING_MARKET_VALUE']
    fund_zc_holding_industry_sw1 = fund_zc_holding_industry_sw1.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='WEIGHT').fillna(0.0)
    # 入库
    data = fund_zc_holding_industry_sw1.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'INDUSTRY_SW1'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    stock_industry_sw2 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 2]
    fund_zc_holding_industry_sw2 = fund_zc_holding.merge(stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
    fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.dropna(subset=['INDUSTRY_NAME'])
    fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2[['REPORT_DATE', 'INDUSTRY_NAME', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
    fund_zc_holding_industry_sw2_total = fund_zc_holding_industry_sw2[['REPORT_DATE', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'HOLDING_MARKET_VALUE': 'TOTAL_HOLDING_MARKET_VALUE'})
    fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.merge(fund_zc_holding_industry_sw2_total, on=['REPORT_DATE'], how='left')
    fund_zc_holding_industry_sw2['WEIGHT'] = fund_zc_holding_industry_sw2['HOLDING_MARKET_VALUE'] / fund_zc_holding_industry_sw2['TOTAL_HOLDING_MARKET_VALUE']
    fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='WEIGHT').fillna(0.0)
    # 入库
    data = fund_zc_holding_industry_sw2.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'INDUSTRY_SW2'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_market_value(date, fund_zc_holding):
    """
    市值分析
    """
    preload_index_cons()
    index_cons_all = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/index_cons.hdf', key='table')
    index_cons_all = index_cons_all.rename(columns={'SECUCODE': 'TICKER_SYMBOL', 'ENDDATE': 'END_DATE'})
    index_cons_all['END_DATE'] = index_cons_all['END_DATE'].apply(lambda x: x[:10].replace('-', ''))

    index_cons_mv1 = index_cons_all[index_cons_all['INDEX'].isin(['HS300', 'ZZ500', 'ZZ1000'])]
    fund_zc_holding_mv1 = fund_zc_holding.merge(index_cons_mv1[['TICKER_SYMBOL', 'END_DATE', 'INDEX']].rename(columns={'END_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
    fund_zc_holding_mv1['INDEX'] = fund_zc_holding_mv1['INDEX'].fillna('非成分股')
    fund_zc_holding_mv1 = fund_zc_holding_mv1[['REPORT_DATE', 'INDEX', 'TICKER_SYMBOL']].groupby(['REPORT_DATE', 'INDEX']).count().reset_index().rename(columns={'TICKER_SYMBOL': 'COUNT'})
    fund_zc_holding_mv1 = fund_zc_holding_mv1.pivot(index='REPORT_DATE', columns='INDEX', values='COUNT').fillna(0.0)
    # 入库
    data = fund_zc_holding_mv1.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'MARKET_VALUE_1'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    index_cons_mv2 = index_cons_all[index_cons_all['INDEX'].isin(['SZ50', 'ZZ100', 'SZ180', 'HS300'])]
    count_list = [fund_zc_holding[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': 'TOTAL'})]
    for index in ['SZ50', 'ZZ100', 'SZ180', 'HS300']:
        fund_zc_holding_index = fund_zc_holding.copy(deep=True)
        index_cons_mv2_index = index_cons_mv2[index_cons_mv2['INDEX'] == index]
        fund_zc_holding_mv2_index = fund_zc_holding_index.merge(index_cons_mv2_index[['TICKER_SYMBOL', 'END_DATE', 'INDEX']].rename(columns={'END_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
        fund_zc_holding_mv2_index = fund_zc_holding_mv2_index.dropna(subset=['INDEX'])
        fund_zc_holding_wm2_index_count = fund_zc_holding_mv2_index[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': index})
        count_list.append(fund_zc_holding_wm2_index_count)
    fund_zc_holding_mv2 = pd.concat(count_list, axis=1)
    # 入库
    data = fund_zc_holding_mv2.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'MARKET_VALUE_2'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_style(date, fund_zc_holding):
    """
    风格分析
    """
    preload_index_cons()
    index_cons_all = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/index_cons.hdf', key='table')
    index_cons_all = index_cons_all.rename(columns={'SECUCODE': 'TICKER_SYMBOL', 'ENDDATE': 'END_DATE'})
    index_cons_all['END_DATE'] = index_cons_all['END_DATE'].apply(lambda x: x[:10].replace('-', ''))
    # stock_style = HBDB().read_stock_style()
    # stock_style.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_style.hdf', key='table', mode='w')
    # stock_style = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_style.hdf', key='table')
    # stock_style = stock_style.rename(columns={'ticker': 'TICKER_SYMBOL', 'trade_date': 'TRADE_DATE', 'type': 'IS_ZC', 'cap_score': 'CAP_SCORE', 'vcg_score': 'VCG_SCORE', 'category': 'CATEGORY'})
    # stock_style = stock_style[stock_style['IS_ZC'] == 'main']
    # if stock_style['TRADE_DATE'].max() != fund_zc_holding['RECENT_TRADE_DATE'].max():
    #     stock_style_latest = stock_style[stock_style['TRADE_DATE'] == stock_style['TRADE_DATE'].max()]
    #     stock_style_latest['TRADE_DATE'] = fund_zc_holding['RECENT_TRADE_DATE'].max()
    #     stock_style = pd.concat([stock_style, stock_style_latest])
    wind_stock_style = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/wind_stock_style.xlsx')
    wind_stock_style = wind_stock_style.rename(columns={'股票代码': 'TICKER_SYMBOL'})
    wind_stock_style['TICKER_SYMBOL'] = wind_stock_style['TICKER_SYMBOL'].apply(lambda x: str(x).split('.')[0])
    wind_stock_style = wind_stock_style.set_index('TICKER_SYMBOL')
    stock_style_list = []
    for date in fund_zc_holding['RECENT_TRADE_DATE'].unique().tolist():
        wind_stock_style_date = wind_stock_style[[str(int(date[:4]) - 1)]]
        wind_stock_style_date = wind_stock_style_date.rename(columns={str(int(date[:4]) - 1): date})
        stock_style_list.append(wind_stock_style_date)
    stock_style = pd.concat(stock_style_list, axis=1)
    stock_style = stock_style.unstack().reset_index()
    stock_style.columns = ['TRADE_DATE', 'TICKER_SYMBOL', 'CATEGORY']
    stock_style = stock_style.dropna(subset=['CATEGORY'])
    stock_style['CATEGORY'] = stock_style['CATEGORY'].replace('大盘均衡型', '大盘平衡型').replace('中盘均衡型', '中盘平衡型').replace('小盘均衡型', '小盘平衡型')

    index_cons_style1 = index_cons_all[index_cons_all['INDEX'].isin(['JCCZ', 'JCJZ'])]
    fund_zc_holding_style1 = fund_zc_holding.copy(deep=True)
    fund_zc_holding_style1 = fund_zc_holding_style1.merge(index_cons_style1[['TICKER_SYMBOL', 'END_DATE', 'INDEX']].rename(columns={'END_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
    fund_zc_holding_style1 = fund_zc_holding_style1.merge(stock_style[['TICKER_SYMBOL', 'TRADE_DATE', 'CATEGORY']].rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
    fund_zc_holding_style1['INDEX'] = fund_zc_holding_style1['INDEX'].astype(str)
    fund_zc_holding_style1['CATEGORY'] = fund_zc_holding_style1['CATEGORY'].astype(str)
    fund_zc_holding_style1['MARK'] = fund_zc_holding_style1.apply(lambda x:
             '价值' if x['INDEX'][-2:] == 'JZ' else '成长' if x['INDEX'][-2:] == 'CZ'
        else '价值' if x['CATEGORY'][-3:] == '价值型' else '成长' if x['CATEGORY'][-3:] == '成长型' else '平衡' if x['CATEGORY'][-3:] == '平衡型'
        else np.nan, axis=1)
    fund_zc_holding_style1 = fund_zc_holding_style1.dropna(subset=['MARK'])
    count_list = [fund_zc_holding_style1[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': 'TOTAL'})]
    for mark in ['价值', '成长', '平衡']:
        fund_zc_holding_style1_mark = fund_zc_holding_style1[fund_zc_holding_style1['MARK'] == mark]
        fund_zc_holding_style1_mark_count = fund_zc_holding_style1_mark[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': mark})
        count_list.append(fund_zc_holding_style1_mark_count)
    fund_zc_holding_style1 = pd.concat(count_list, axis=1)
    # 入库
    data = fund_zc_holding_style1.fillna(0).unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'STYLE_1'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)

    index_cons_style2 = index_cons_all[index_cons_all['INDEX'].isin(['JCDPCZ', 'JCDPJZ', 'JCZPCZ', 'JCZPJZ', 'JCXPCZ', 'JCXPJZ'])]
    fund_zc_holding_style2 = fund_zc_holding.copy(deep=True)
    fund_zc_holding_style2 = fund_zc_holding_style2.merge(index_cons_style2[['TICKER_SYMBOL', 'END_DATE', 'INDEX']].rename(columns={'END_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
    fund_zc_holding_style2 = fund_zc_holding_style2.merge(stock_style[['TICKER_SYMBOL', 'TRADE_DATE', 'CATEGORY']].rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['TICKER_SYMBOL', 'RECENT_TRADE_DATE'], how='left')
    fund_zc_holding_style2['INDEX'] = fund_zc_holding_style2['INDEX'].astype(str)
    fund_zc_holding_style2['CATEGORY'] = fund_zc_holding_style2['CATEGORY'].astype(str)
    fund_zc_holding_style2['MARK'] = fund_zc_holding_style2.apply(lambda x:
             '大盘价值' if x['INDEX'] == 'JCDPJZ' else '大盘成长' if x['INDEX'] == 'JCDPCZ'
        else '中盘价值' if x['INDEX'] == 'JCZPJZ' else '中盘成长' if x['INDEX'] == 'JCZPCZ'
        else '小盘价值' if x['INDEX'] == 'JCXPJZ' else '小盘成长' if x['INDEX'] == 'JCXPCZ'
        else '大盘价值' if x['CATEGORY'] == '大盘价值型' else '大盘成长' if x['CATEGORY'] == '大盘成长型' else '大盘平衡' if x['CATEGORY'] == '大盘平衡型'
        else '中盘价值' if x['CATEGORY'] == '中盘价值型' else '中盘成长' if x['CATEGORY'] == '中盘成长型' else '中盘平衡' if x['CATEGORY'] == '中盘平衡型'
        else '小盘价值' if x['CATEGORY'] == '小盘价值型' else '小盘成长' if x['CATEGORY'] == '小盘成长型' else '小盘平衡' if x['CATEGORY'] == '小盘平衡型'
        else np.nan, axis=1)
    fund_zc_holding_style2 = fund_zc_holding_style2.dropna(subset=['MARK'])
    count_list = [fund_zc_holding_style2[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': 'TOTAL'})]
    for mark in ['大盘价值', '大盘成长', '大盘平衡', '中盘价值', '中盘成长', '中盘平衡', '小盘价值', '小盘成长', '小盘平衡']:
        fund_zc_holding_style2_mark = fund_zc_holding_style2[fund_zc_holding_style2['MARK'] == mark]
        fund_zc_holding_style2_mark_count = fund_zc_holding_style2_mark[['REPORT_DATE', 'TICKER_SYMBOL']].groupby(['REPORT_DATE']).count().rename(columns={'TICKER_SYMBOL': mark})
        count_list.append(fund_zc_holding_style2_mark_count)
    fund_zc_holding_style2 = pd.concat(count_list, axis=1)
    # 入库
    data = fund_zc_holding_style2.fillna(0).unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'STYLE_2'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def fund_barra(date, fund_zc_holding):
    """
    Barra风格分析
    """
    barra = HBDB().read_barra_style_exposure_given_dates(fund_zc_holding['RECENT_TRADE_DATE'].unique().tolist())
    barra.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/barra_style_exposure.hdf', key='table', mode='w')
    barra = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/barra_style_exposure.hdf', key='table')
    barra = barra.rename(columns={'ticker': 'TICKER_SYMBOL', 'trade_date': 'TRADE_DATE'})
    factor_list = [factor for factor in list(barra.columns) if factor != 'TICKER_SYMBOL' and factor != 'TRADE_DATE']
    fund_zc_holding_barra = fund_zc_holding.merge(barra.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
    fund_zc_holding_barra_weight = fund_zc_holding[['REPORT_DATE', 'FUND_CODE', 'MV_IN_NA']].groupby(['REPORT_DATE', 'FUND_CODE']).sum().reset_index().rename(columns={'MV_IN_NA': 'TOTAL_MV_IN_NA'})
    fund_zc_holding_barra = fund_zc_holding_barra.merge(fund_zc_holding_barra_weight, on=['REPORT_DATE', 'FUND_CODE'], how='left')
    fund_zc_holding_barra_list = []
    for factor in factor_list:
        fund_zc_holding_barra['WEIGHTED_{}'.format(factor)] = fund_zc_holding_barra[factor] * fund_zc_holding_barra['MV_IN_NA'] / fund_zc_holding_barra['TOTAL_MV_IN_NA']
        fund_zc_holding_barra_factor = fund_zc_holding_barra[['FUND_CODE', 'REPORT_DATE', 'WEIGHTED_{}'.format(factor)]].groupby(['FUND_CODE', 'REPORT_DATE']).sum().reset_index()
        fund_zc_holding_barra_factor = fund_zc_holding_barra_factor[['REPORT_DATE', 'WEIGHTED_{}'.format(factor)]].groupby(['REPORT_DATE']).mean().rename(columns={'WEIGHTED_{}'.format(factor): factor})
        fund_zc_holding_barra_list.append(fund_zc_holding_barra_factor)
    fund_zc_holding_barra = pd.concat(fund_zc_holding_barra_list, axis=1)
    # 入库
    data = fund_zc_holding_barra.unstack().reset_index()
    data.columns = ['LABEL_NAME', 'REPORT_HISTORY_DATE', 'LABEL_VALUE']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'BARRA'
    data['LABEL_VALUE_STRING'] = np.nan
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def stock_holding(date, fund_zc_holding):
    """
    持股变动
    """
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna(20990101)
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1]
    stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]

    stock_name = fund_zc_holding[['REPORT_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME']].drop_duplicates()
    fund_zc_holding_stock = fund_zc_holding[['REPORT_DATE', 'SEC_SHORT_NAME', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'SEC_SHORT_NAME']).sum().reset_index()
    fund_zc_holding_stock_weight = fund_zc_holding[['REPORT_DATE', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'HOLDING_MARKET_VALUE': 'TOTAL_HOLDING_MARKET_VALUE'})
    fund_zc_holding_stock = fund_zc_holding_stock.merge(fund_zc_holding_stock_weight, on=['REPORT_DATE'], how='left')
    fund_zc_holding_stock['RATIO'] = fund_zc_holding_stock['HOLDING_MARKET_VALUE'] / fund_zc_holding_stock['TOTAL_HOLDING_MARKET_VALUE']
    fund_zc_holding_stock = fund_zc_holding_stock.merge(stock_name, on=['REPORT_DATE', 'SEC_SHORT_NAME'], how='left')
    fund_zc_holding_stock = fund_zc_holding_stock.merge(stock_industry[['TICKER_SYMBOL', 'INDUSTRY_ID', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
    fund_zc_holding_stock = fund_zc_holding_stock.sort_values(['REPORT_DATE', 'INDUSTRY_NAME', 'RATIO'], ascending=[True, True, False])
    fund_zc_holding_stock_top3 = fund_zc_holding_stock.groupby(['REPORT_DATE', 'INDUSTRY_NAME']).head(3)
    # 入库
    data = fund_zc_holding_stock_top3[['REPORT_DATE', 'INDUSTRY_NAME', 'RATIO', 'SEC_SHORT_NAME']]
    data.columns = ['REPORT_HISTORY_DATE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']
    data['REPORT_DATE'] = date
    data['FUND_UNIVERSE'] = 'FOCUS_MUTUAL_FUND_UNIVERSE'
    data['IS_ZC'] = 1
    data['LABEL_TYPE'] = 'STOCK'
    data['LABEL_NAME'] = data['LABEL_NAME'].apply(lambda x: x + '_stock')
    data = data[['REPORT_DATE', 'REPORT_HISTORY_DATE', 'FUND_UNIVERSE', 'IS_ZC', 'LABEL_TYPE', 'LABEL_NAME', 'LABEL_VALUE', 'LABEL_VALUE_STRING']]
    FEDB().insert_df(data)
    return

def holding_analysis_v1(date):
    """
    公募基金持仓分析
    """
    # 基金池
    fund = fund_info(date)
    fund.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table', mode='w')
    fund = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table')
    # 基金持仓
    fund_holding = HBDB().read_fund_holding_given_codes(fund['FUND_CODE'].unique().tolist())
    fund_holding.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table', mode='w')
    fund_holding = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table')
    fund_holding = fund_holding.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ccsz': 'HOLDING_MARKET_VALUE', 'ccsl': 'HOLDING_AMOUNT', 'zjbl': 'MV_IN_NA'})
    fund_holding['REPORT_DATE'] = fund_holding['REPORT_DATE'].astype(str)
    fund_holding_diff = HBDB().read_fund_holding_diff_given_codes(fund['FUND_CODE'].unique().tolist())
    fund_holding_diff.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table', mode='w')
    fund_holding_diff = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table')
    fund_holding_diff = fund_holding_diff.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'zclb': 'IS_ZC', 'zgblbd': 'MV_IN_NA_DIFF', 'sfsqzcg': 'IS_LAST_ZC'})
    fund_holding_diff['REPORT_DATE'] = fund_holding_diff['REPORT_DATE'].astype(str)
    fund_holding_diff = fund_holding_diff.dropna(subset=['IS_ZC'])
    fund_holding_diff['IS_ZC'] = fund_holding_diff['IS_ZC'].astype(int)
    # 基金重仓
    fund_zc_holding = fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).groupby(['FUND_CODE', 'REPORT_DATE']).head(10)
    fund_zc_holding_diff = fund_holding_diff[fund_holding_diff['IS_ZC'] == 1]
    # # 基金全仓
    # fund_zc_holding = fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).copy(deep=True)
    # fund_zc_holding_diff = fund_holding_diff[fund_holding_diff['IS_ZC'] == 2]
    # 分析区间
    report_dates = sorted(fund_zc_holding[fund_zc_holding['REPORT_DATE'] <= date]['REPORT_DATE'].unique().tolist())[-40:]
    # report_dates = [date for date in report_dates if date[4:] == '0630' or date[4:] == '1231']
    fund_zc_holding = fund_zc_holding[fund_zc_holding['REPORT_DATE'].isin(report_dates)]
    fund_zc_holding_diff = fund_zc_holding_diff[fund_zc_holding_diff['REPORT_DATE'].isin(report_dates)]
    cal, trade_cal = get_cal_and_trade_cal('19900101', date)
    fund_zc_holding = fund_zc_holding.merge(cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
    fund_zc_holding_diff = fund_zc_holding_diff.merge(cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
    # 持仓分析
    fund_valuation(date, fund_zc_holding, fund_zc_holding_diff)
    fund_sector(date, fund_zc_holding)
    fund_theme(date, fund_zc_holding)
    fund_industry(date, fund_zc_holding)
    fund_market_value(date, fund_zc_holding)
    fund_style(date, fund_zc_holding)
    fund_barra(date, fund_zc_holding)
    stock_holding(date, fund_zc_holding)
    return

class holding_analysis_v2:
    def __init__(self, date, data_path):
        self.date = date
        self.data_path = data_path
        self.load()

    def load(self):
        # 基金池
        self.fund = fund_info(date)
        self.fund.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table', mode='w')
        self.fund = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table')
        # 基金持仓
        self.fund_holding = HBDB().read_fund_holding_given_codes(self.fund['FUND_CODE'].unique().tolist())
        self.fund_holding.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table', mode='w')
        self.fund_holding = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table')
        self.fund_holding = self.fund_holding.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ccsz': 'HOLDING_MARKET_VALUE', 'ccsl': 'HOLDING_AMOUNT', 'zjbl': 'MV_IN_NA'})
        self.fund_holding['REPORT_DATE'] = self.fund_holding['REPORT_DATE'].astype(str)
        self.fund_holding_diff = HBDB().read_fund_holding_diff_given_codes(self.fund['FUND_CODE'].unique().tolist())
        self.fund_holding_diff.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table', mode='w')
        self.fund_holding_diff = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table')
        self.fund_holding_diff = self.fund_holding_diff.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'zclb': 'IS_ZC', 'zgblbd': 'MV_IN_NA_DIFF', 'sfsqzcg': 'IS_LAST_ZC'})
        self.fund_holding_diff['REPORT_DATE'] = self.fund_holding_diff['REPORT_DATE'].astype(str)
        self.fund_holding_diff = self.fund_holding_diff.dropna(subset=['IS_ZC'])
        self.fund_holding_diff['IS_ZC'] = self.fund_holding_diff['IS_ZC'].astype(int)
        # 基金重仓
        self.fund_zc_holding = self.fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).groupby(['FUND_CODE', 'REPORT_DATE']).head(10)
        self.fund_zc_holding_diff = self.fund_holding_diff[self.fund_holding_diff['IS_ZC'] == 1]
        # # 基金全仓
        # self.fund_zc_holding = self.fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).copy(deep=True)
        # self.fund_zc_holding_diff = self.fund_holding_diff[self.fund_holding_diff['IS_ZC'] == 2]
        # 分析区间
        self.report_dates = sorted(self.fund_zc_holding[self.fund_zc_holding['REPORT_DATE'] <= self.date]['REPORT_DATE'].unique().tolist())[-40:]
        # self.report_dates = [date for date in self.report_dates if date[4:] == '0630' or date[4:] == '1231']
        self.fund_zc_holding = self.fund_zc_holding[self.fund_zc_holding['REPORT_DATE'].isin(self.report_dates)]
        self.fund_zc_holding_diff = self.fund_zc_holding_diff[self.fund_zc_holding_diff['REPORT_DATE'].isin(self.report_dates)]
        self.cal, self.trade_cal = get_cal_and_trade_cal('19900101', self.date)
        self.fund_zc_holding = self.fund_zc_holding.merge(self.cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
        self.fund_zc_holding_diff = self.fund_zc_holding_diff.merge(self.cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')

        # 基金规模
        fund_aum_list = []
        for idx, td in enumerate(self.report_dates):
            fund_aum_date = HBDB().read_fund_scale_given_date(td)
            fund_aum_date = fund_aum_date if len(fund_aum_date) > 0 else pd.DataFrame(columns=['ZCJZ', 'BBLB1', 'JSRQ', 'JJDM', 'GGRQ', 'ROW_ID'])
            fund_aum_date = fund_aum_date[fund_aum_date['BBLB1'] == 13]
            fund_aum_date = fund_aum_date.sort_values(['JJDM', 'JSRQ', 'GGRQ']).drop_duplicates(['JJDM', 'JSRQ'], keep='last')
            fund_aum_list.append(fund_aum_date)
            print('[PreloadFundAum][{0}/{1}]'.format(idx, len(self.report_dates)))
        self.fund_aum = pd.concat(fund_aum_list, ignore_index=True)
        self.fund_aum.to_hdf('{0}fund_aum.hdf'.format(self.data_path), key='table', mode='w')
        self.fund_aum = pd.read_hdf('{0}fund_aum.hdf'.format(self.data_path), key='table')
        self.fund_aum = self.fund_aum[['JJDM', 'JSRQ', 'ZCJZ']]
        self.fund_aum.columns = ['FUND_CODE', 'REPORT_DATE', 'AUM']
        self.fund_aum['REPORT_DATE'] = self.fund_aum['REPORT_DATE'].astype(str)

        # 基金仓位
        fund_position_list = []
        for idx, td in enumerate(self.report_dates):
            fund_position_date = HBDB().read_fund_position_given_date(td)
            fund_position_date = fund_position_date if len(fund_position_date) > 0 else pd.DataFrame(columns=['gptzsz', 'jjzzc', 'zqzsz', 'hbzjsz', 'jjdm', 'jsrq', 'jjtzszhj'])
            fund_position_list.append(fund_position_date)
            print('[PreloadFundPosition][{0}/{1}]'.format(idx, len(self.report_dates)))
        self.fund_position = pd.concat(fund_position_list, ignore_index=True)
        self.fund_position.to_hdf('{0}fund_position.hdf'.format(self.data_path), key='table', mode='w')
        self.fund_position = pd.read_hdf('{0}fund_position.hdf'.format(self.data_path), key='table')
        self.fund_position = self.fund_position[['jjdm', 'jsrq', 'gptzsz', 'jjzzc']]
        self.fund_position.columns = ['FUND_CODE', 'REPORT_DATE', 'STOCK', 'TOTAL']
        self.fund_position['REPORT_DATE'] = self.fund_position['REPORT_DATE'].astype(str)
        self.fund_position['STOCK_RATIO'] = self.fund_position['STOCK'].fillna(0.0) / self.fund_position['TOTAL'] * 100.0

        # 行业个股对应关系
        self.stock_industry = HBDB().read_stock_industry()
        self.stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table', mode='w')
        self.stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_industry.hdf', key='table')
        self.stock_industry = self.stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
        self.stock_industry = self.stock_industry.dropna(subset=['BEGIN_DATE'])
        self.stock_industry['END_DATE'] = self.stock_industry['END_DATE'].fillna(20990101)
        self.stock_industry['BEGIN_DATE'] = self.stock_industry['BEGIN_DATE'].astype(int).astype(str)
        self.stock_industry['END_DATE'] = self.stock_industry['END_DATE'].astype(int).astype(str)
        self.stock_industry['INDUSTRY_VERSION'] = self.stock_industry['INDUSTRY_VERSION'].astype(int)
        self.stock_industry['INDUSTRY_TYPE'] = self.stock_industry['INDUSTRY_TYPE'].astype(int)
        self.stock_industry['IS_NEW'] = self.stock_industry['IS_NEW'].astype(int)
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_VERSION'] == 2]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]

    def all_fund_scale(self):
        all_fund = HBDB().read_fund_info()
        all_fund = all_fund.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'BEGIN_DATE', 'zzrq': 'END_DATE', 'jjfl': 'FUND_TYPE_1ST', 'ejfl': 'FUND_TYPE_2ND', 'kffb': 'OPEN_CLOSE'})
        all_fund = all_fund.dropna(subset=['BEGIN_DATE'])
        all_fund['END_DATE'] = all_fund['END_DATE'].fillna(20990101)
        all_fund['BEGIN_DATE'] = all_fund['BEGIN_DATE'].astype(int).astype(str)
        all_fund['END_DATE'] = all_fund['END_DATE'].astype(int).astype(str)
        all_fund['FUND_TYPE_1ST'] = all_fund['FUND_TYPE_1ST'].replace(
            {'f': 'FOF型', '1': '股票型', '2': '债券型', '3': '混合型', '4': '另类投资型', '7': '货币型', '9': 'QDII型'})
        all_fund['FUND_TYPE_2ND'] = all_fund['FUND_TYPE_2ND'].replace(
            {'f3': '债券型FOF', 'f4': '货币型FOF', 'f1': '股票型FOF', 'f2': '混合型FOF', 'f5': '另类投资FOF',
             '13': '普通股票型', '14': '股票型', '15': '增强指数型', '16': '被动指数型',
             '21': '被动指数型债券', '22': '短期纯债型', '23': '混合债券型一级', '24': '混合债券型二级', '25': '增强指数型债券', '26': '债券型', '27': '中长期纯债型', '28': '可转换债券型',
             '34': '平衡混合型', '35': '灵活配置型', '36': '混合型', '37': '偏股混合型', '38': '偏债混合型',
             '41': '股票多空', '42': '商品型', '43': 'REITs',
             '91': '股票型QDII', '93': '混合型QDII', '94': '债券型QDII', '95': '另类型QDII'})
        all_fund['FUND_TYPE'] = all_fund['FUND_TYPE_1ST']
        all_fund.loc[all_fund['FUND_TYPE_2ND'] == 'REITs', 'FUND_TYPE'] = 'REITs'
        fund_aum = self.fund_aum.merge(all_fund[['FUND_CODE', 'FUND_TYPE', 'FUND_FULL_NAME']], on=['FUND_CODE'], how='left')
        fund_aum = fund_aum.dropna(subset=['FUND_TYPE'])
        fund_aum = fund_aum[['REPORT_DATE', 'FUND_TYPE', 'AUM']].groupby(['REPORT_DATE', 'FUND_TYPE']).sum().reset_index()
        fund_count = pd.DataFrame(index=range(len(self.report_dates)), columns=['REPORT_DATE', 'COUNT'])
        for idx, date in enumerate(self.report_dates):
            all_fund_date = all_fund[(all_fund['BEGIN_DATE'] < date) & (all_fund['END_DATE'] >= date)]
            all_fund_date = all_fund_date.drop_duplicates('FUND_FULL_NAME')
            fund_count['REPORT_DATE'].iloc[idx] = date
            fund_count['COUNT'].iloc[idx] = len(all_fund_date)

        type_list = ['股票型', '混合型', '债券型', '货币型', '另类投资型', 'QDII型', 'FOF型', 'REITs']
        color_list = [bar_color_list[0], bar_color_list[1], bar_color_list[2], bar_color_list[7], bar_color_list[8], bar_color_list[9], bar_color_list[14], bar_color_list[15]]
        fund_aum_disp = fund_aum.copy(deep=True)
        fund_aum_disp['AUM'] = fund_aum_disp['AUM'] / 100000000.0
        fund_aum_disp = fund_aum_disp.pivot(index='REPORT_DATE', columns='FUND_TYPE', values='AUM').reset_index()
        fund_aum_disp = fund_aum_disp[['REPORT_DATE'] + type_list].sort_index()
        fund_count_disp = fund_count.copy(deep=True)
        for i in range(1, len(type_list)):
            fund_aum_disp[type_list[i]] = fund_aum_disp[type_list[i]] + fund_aum_disp[type_list[i - 1]]
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        for i in range(len(type_list) - 1, -1, -1):
            sns.barplot(ax=ax1, x='REPORT_DATE', y=type_list[i], data=fund_aum_disp, label=type_list[i], color=color_list[i])
        sns.lineplot(ax=ax2, x='REPORT_DATE', y='COUNT', data=fund_count_disp, label='总数量', color=line_color_list[0])
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        ax1.set_xticklabels(labels=self.report_dates, rotation=90)
        ax2.set_xticklabels(labels=self.report_dates, rotation=90)
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('规模（亿元）')
        ax2.set_ylabel('数量（只）')
        ax1.set_ylim([0, 300000])
        ax2.set_ylim([0, 12000])
        plt.title('公募基金规模及数量')
        plt.tight_layout()
        plt.savefig('{0}all_fund_aum.png'.format(self.data_path))
        return

    def all_fund_position(self):
        fund_position = self.fund_position[self.fund_position['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        fund_position = fund_position[['REPORT_DATE', 'STOCK_RATIO']].groupby('REPORT_DATE').mean().reset_index()
        fund_zc_position = self.fund_zc_holding[self.fund_zc_holding['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        fund_zc_position = fund_zc_position[['REPORT_DATE', 'FUND_CODE', 'MV_IN_NA']].groupby(['REPORT_DATE', 'FUND_CODE']).sum().reset_index()
        fund_zc_position = fund_zc_position[['REPORT_DATE', 'MV_IN_NA']].groupby('REPORT_DATE').mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(ax=ax, x='REPORT_DATE', y='STOCK_RATIO', data=fund_position, label='股票仓位', color=area_color_list[0])
        sns.lineplot(ax=ax, x='REPORT_DATE', y='MV_IN_NA', data=fund_zc_position, label='前十大重仓仓位', color=area_color_list[7])
        plt.fill_between(fund_position['REPORT_DATE'], 0, fund_position['STOCK_RATIO'], color=area_color_list[0], alpha=0.5)
        plt.fill_between(fund_zc_position['REPORT_DATE'], 0, fund_zc_position['MV_IN_NA'], color=area_color_list[7], alpha=0.5)
        plt.legend(loc=2)
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('')
        plt.ylim([0, 100])
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('公募基金股票及前十大仓位')
        plt.tight_layout()
        plt.savefig('{0}fund_position.png'.format(self.data_path))
        return

    def all_fund_industry_select(self, industry_list):
        for industry in industry_list:
            stock_industry_sw1 = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == 1]
            stock_industry_sw1 = stock_industry_sw1[stock_industry_sw1['INDUSTRY_NAME'] == industry]
            stock_industry_sw2 = self.stock_industry[self.stock_industry['TICKER_SYMBOL'].isin(stock_industry_sw1['TICKER_SYMBOL'].unique().tolist())]
            stock_industry_sw2 = stock_industry_sw2[stock_industry_sw2['INDUSTRY_TYPE'] == 2]
            fund_zc_holding_industry_sw2 = self.fund_zc_holding.merge(stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
            fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.dropna(subset=['INDUSTRY_NAME'])
            sw2_industry_list = fund_zc_holding_industry_sw2[fund_zc_holding_industry_sw2['REPORT_DATE'] == self.date].sort_values('MV_IN_NA', ascending=False)['INDUSTRY_NAME'].unique().tolist()
            fund_zc_holding_industry_sw2 = FEDB().read_data(self.date, 'INDUSTRY_SW2')
            fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2[fund_zc_holding_industry_sw2['IS_ZC'] == 1]
            fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.pivot(index='LABEL_NAME', columns='REPORT_HISTORY_DATE', values='LABEL_VALUE').reindex(sw2_industry_list).fillna(0.0)
            fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.T.sort_index().iloc[-4:].T
            fund_zc_holding_industry_sw2 = fund_zc_holding_industry_sw2.unstack().reset_index()
            fund_zc_holding_industry_sw2.columns = ['REPORT_DATE', '二级行业', 'MV_IN_NA']
            plt.subplots(figsize=(6, 6))
            sns.barplot(x='MV_IN_NA', y='REPORT_DATE', data=fund_zc_holding_industry_sw2, hue='二级行业', hue_order=sw2_industry_list, palette=line_color_list)
            plt.xlabel('')
            plt.ylabel('')
            plt.xlim([0, 0.15])
            plt.legend(loc=1)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_100percent))
            plt.title(industry)
            plt.tight_layout()
            plt.savefig('{0}fund_industry_{1}.png'.format(self.data_path, industry))
        return

    def all_fund_industry_excess(self):
        sector_dic = {'制造板块': ['建筑装饰', '电力设备', '机械设备', '国防军工'],
                      '材料板块': ['基础化工', '钢铁', '建筑材料'],
                      '资源板块': ['有色金属', '煤炭', '石油石化'],
                      '可选消费板块': ['汽车', '家用电器', '轻工制造', '社会服务', '美容护理'],
                      '必选消费板块': ['农林牧渔', '食品饮料', '纺织服饰', '商贸零售'],
                      'TMT板块': ['电子', '计算机', '传媒', '通信'],
                      '基础设施板块': ['公用事业', '交通运输', '环保'],
                      '医药生物板块': ['医药生物'],
                      '金融地产板块': ['房地产', '银行', '非银金融']}

        market_weight = pd.read_excel('{0}windA_cons.xlsx'.format(self.data_path))
        market_weight['代码'] = market_weight['代码'].apply(lambda x: str(x).split('.')[0])
        industry_match = market_weight[['代码', '申银万国一级行业', '申银万国三级行业']].drop_duplicates()
        industry_match.columns = ['TICKER_SYMBOL', 'INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW3']
        market_weight = market_weight[['申银万国三级行业', '自由流通市值(亿)']]
        market_weight.columns = ['INDUSTRY_NAME_SW3', 'HOLDING_MARKET_VALUE']
        market_weight = market_weight.groupby(['INDUSTRY_NAME_SW3']).sum().reset_index()
        market_weight['MARKET_WEIGHT'] = market_weight['HOLDING_MARKET_VALUE'] / market_weight['HOLDING_MARKET_VALUE'].sum()
        market_weight = market_weight[['INDUSTRY_NAME_SW3', 'MARKET_WEIGHT']]

        fund_weight = self.fund_zc_holding[self.fund_zc_holding['REPORT_DATE'] == self.date]
        fund_weight = fund_weight.merge(industry_match[['TICKER_SYMBOL', 'INDUSTRY_NAME_SW3']], on=['TICKER_SYMBOL'], how='left')
        fund_weight = fund_weight.dropna(subset=['INDUSTRY_NAME_SW3'])
        fund_weight = fund_weight[['INDUSTRY_NAME_SW3', 'HOLDING_MARKET_VALUE']].groupby('INDUSTRY_NAME_SW3').sum().reset_index()
        fund_weight['FUND_WEIGHT'] = fund_weight['HOLDING_MARKET_VALUE'] / fund_weight['HOLDING_MARKET_VALUE'].sum()
        fund_weight = fund_weight[['INDUSTRY_NAME_SW3', 'FUND_WEIGHT']]

        weight = market_weight.merge(fund_weight, on=['INDUSTRY_NAME_SW3'], how='left').fillna(0.0)
        weight['EXCESS'] = weight['FUND_WEIGHT'] - weight['MARKET_WEIGHT']
        for sector in sector_dic.keys():
            industry_list = sector_dic[sector]
            sector_weight_list = []
            for industry_sw1 in industry_list:
                industry_sw3 = industry_match[industry_match['INDUSTRY_NAME_SW1'] == industry_sw1]['INDUSTRY_NAME_SW3'].unique().tolist()
                industry_weight = weight[weight['INDUSTRY_NAME_SW3'].isin(industry_sw3)]
                industry_weight = industry_weight.sort_values('FUND_WEIGHT', ascending=False)
                industry_weight_filter = industry_weight[industry_weight['FUND_WEIGHT'] >= 0.0005]
                industry_weight = industry_weight_filter if len(industry_weight_filter) > 3 else industry_weight.head(3) if len(industry_weight) > 3 else industry_weight
                industry_weight['INDUSTRY_NAME_SW1'] = industry_sw1
                sector_weight_list.append(industry_weight)
            sector_weight = pd.concat(sector_weight_list)
            sector_weight = sector_weight[['INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW3', 'FUND_WEIGHT', 'MARKET_WEIGHT', 'EXCESS']]
            sector_weight_fund = sector_weight[['INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW3', 'FUND_WEIGHT', 'EXCESS']].rename( columns={'FUND_WEIGHT': 'WEIGHT'})
            sector_weight_fund['TYPE'] = '公募配置比例'
            sector_weight_market = sector_weight[['INDUSTRY_NAME_SW1', 'INDUSTRY_NAME_SW3', 'MARKET_WEIGHT', 'EXCESS']].rename(columns={'MARKET_WEIGHT': 'WEIGHT'})
            sector_weight_market['TYPE'] = '市场配置比例'
            sector_weight_disp = pd.concat([sector_weight_fund, sector_weight_market])
            type_list = ['公募配置比例', '市场配置比例']
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            sns.barplot(ax=ax1, x='INDUSTRY_NAME_SW3', y='WEIGHT', data=sector_weight_disp, hue='TYPE', hue_order=type_list, palette=[bar_color_list[0], bar_color_list[7]])
            sns.barplot(ax=ax2, x='INDUSTRY_NAME_SW3', y='EXCESS', data=sector_weight, label='公募超配比例', palette=[bar_color_list[14]])
            ax1.legend(loc=2)
            ax2.legend(loc=1)
            ax1.set_xticklabels(labels=sector_weight['INDUSTRY_NAME_SW3'].unique().tolist(), rotation=90)
            ax2.set_xticklabels(labels=sector_weight['INDUSTRY_NAME_SW3'].unique().tolist(), rotation=90)
            ax1.set_ylim([0, (sector_weight_disp['WEIGHT'].max() + (sector_weight['EXCESS'].max() - sector_weight['EXCESS'].min())) * 1.5])
            ax2.set_ylim([(sector_weight['EXCESS'].min() - (sector_weight_disp['WEIGHT'].max() - sector_weight_disp['WEIGHT'].min())) * 1.5, sector_weight['EXCESS'].max() * 3])
            ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent_r2))
            ax2.yaxis.set_major_formatter(FuncFormatter(to_100percent_r2))
            ax1.set_xlabel('')
            ax2.set_xlabel('')
            ax1.set_ylabel('')
            ax2.set_ylabel('')
            plt.title('{0}公募/市场配置对比'.format(sector))
            plt.tight_layout()
            plt.savefig('{0}fund_market_{1}.png'.format(self.data_path, sector))
        return

    def all_fund_stock_holding(self):
        stock_name = self.fund_zc_holding.sort_values(['TICKER_SYMBOL', 'REPORT_DATE'])[['TICKER_SYMBOL', 'SEC_SHORT_NAME']].drop_duplicates('TICKER_SYMBOL', keep='last')
        stock_industry_sw1 = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == 1]
        fund_zc_holding_stock = self.fund_zc_holding[['REPORT_DATE', 'TICKER_SYMBOL', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'TICKER_SYMBOL']).sum().reset_index()
        fund_zc_holding_stock_weight = fund_zc_holding_stock[['REPORT_DATE', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE']).sum().reset_index().rename(columns={'HOLDING_MARKET_VALUE': 'TOTAL_HOLDING_MARKET_VALUE'})
        fund_zc_holding_stock = fund_zc_holding_stock.merge(fund_zc_holding_stock_weight, on=['REPORT_DATE'], how='left')
        fund_zc_holding_stock['RATIO'] = fund_zc_holding_stock['HOLDING_MARKET_VALUE'] / fund_zc_holding_stock['TOTAL_HOLDING_MARKET_VALUE']
        fund_zc_holding_stock = fund_zc_holding_stock.merge(stock_name, on=['TICKER_SYMBOL'], how='left')
        fund_zc_holding_stock = fund_zc_holding_stock.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
        fund_zc_holding_diff_stock = fund_zc_holding_stock[fund_zc_holding_stock['REPORT_DATE'].isin(self.report_dates[-2:])]
        fund_zc_holding_diff_stock = fund_zc_holding_diff_stock[['TICKER_SYMBOL', 'REPORT_DATE', 'RATIO']].drop_duplicates().pivot(index='TICKER_SYMBOL', columns='REPORT_DATE', values='RATIO')
        fund_zc_holding_diff_stock['DIFF'] = fund_zc_holding_diff_stock[self.report_dates[-1]] - fund_zc_holding_diff_stock[self.report_dates[-2]]
        fund_zc_holding_diff_stock = fund_zc_holding_diff_stock.reset_index().merge(stock_name, on=['TICKER_SYMBOL'], how='left')
        fund_zc_holding_diff_stock = fund_zc_holding_diff_stock.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
        fund_zc_holding_stock.to_excel('{0}fund_stock_holding.xlsx'.format(self.data_path))
        fund_zc_holding_diff_stock.to_excel('{0}fund_stock_holding_diff.xlsx'.format(self.data_path))

        fund_stock_10 = fund_zc_holding_stock.sort_values(['REPORT_DATE', 'HOLDING_MARKET_VALUE'], ascending=[True, False]).groupby(['REPORT_DATE']).head(10)
        fund_stock_20 = fund_zc_holding_stock.sort_values(['REPORT_DATE', 'HOLDING_MARKET_VALUE'], ascending=[True, False]).groupby(['REPORT_DATE']).head(20)
        fund_stock_30 = fund_zc_holding_stock.sort_values(['REPORT_DATE', 'HOLDING_MARKET_VALUE'], ascending=[True, False]).groupby(['REPORT_DATE']).head(30)
        fund_stock_100 = fund_zc_holding_stock.sort_values(['REPORT_DATE', 'HOLDING_MARKET_VALUE'], ascending=[True, False]).groupby(['REPORT_DATE']).head(100)
        fund_stock_10 = fund_stock_10.groupby(['REPORT_DATE']).apply(lambda x: x['HOLDING_MARKET_VALUE'].sum() / x['TOTAL_HOLDING_MARKET_VALUE'].mean()).reset_index().rename(columns={0: 'HOLDING_RATIO_10'})
        fund_stock_20 = fund_stock_20.groupby(['REPORT_DATE']).apply(lambda x: x['HOLDING_MARKET_VALUE'].sum() / x['TOTAL_HOLDING_MARKET_VALUE'].mean()).reset_index().rename(columns={0: 'HOLDING_RATIO_20'})
        fund_stock_30 = fund_stock_30.groupby(['REPORT_DATE']).apply(lambda x: x['HOLDING_MARKET_VALUE'].sum() / x['TOTAL_HOLDING_MARKET_VALUE'].mean()).reset_index().rename(columns={0: 'HOLDING_RATIO_30'})
        fund_stock_100 = fund_stock_100.groupby(['REPORT_DATE']).apply(lambda x: x['HOLDING_MARKET_VALUE'].sum() / x['TOTAL_HOLDING_MARKET_VALUE'].mean()).reset_index().rename(columns={0: 'HOLDING_RATIO_100'})
        index = HBDB().read_index_daily_k_given_date_and_indexs('20100101', ['881001'])
        index['jyrq'] = index['jyrq'].astype(str)
        index = index.pivot(index='jyrq', columns='zqdm', values='spjg')
        index = self.cal[['TRADE_DATE']].set_index('TRADE_DATE').merge(index, left_index=True, right_index=True, how='left')
        index = index.interpolate().dropna()
        index = index[index.index >= self.report_dates[0]]
        index = index / index.iloc[0]
        index = index.reset_index()
        index.columns = ['REPORT_DATE', '万得全A']
        index = index.merge(fund_stock_10, on=['REPORT_DATE'], how='left').merge(fund_stock_20, on=['REPORT_DATE'], how='left').merge(fund_stock_30, on=['REPORT_DATE'], how='left')
        index['LABEL'] = index.apply(lambda x: x['REPORT_DATE'] if not np.isnan(x['HOLDING_RATIO_10']) else '', axis=1)
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        sns.lineplot(ax=ax2, x='REPORT_DATE', y='万得全A', data=index, label='万得全A', color=area_color_list[0])
        ax2.fill_between(index['REPORT_DATE'], 0, index['万得全A'], color=area_color_list[0], alpha=0.5)
        # sns.lineplot(ax=ax2, x='REPORT_DATE', y='偏股混合型基金指数', data=index, label='偏股混合型基金指数', color=area_color_list[1])
        # ax2.fill_between(index['REPORT_DATE'], 0, index['偏股混合型基金指数'], color=area_color_list[1], alpha=0.5)
        sns.lineplot(ax=ax1, x='REPORT_DATE', y='HOLDING_RATIO_10', data=index, label='前10大核心资产占比', color=area_color_list[8])
        sns.lineplot(ax=ax1, x='REPORT_DATE', y='HOLDING_RATIO_20', data=index, label='前20大核心资产占比', color=area_color_list[9])
        sns.lineplot(ax=ax1, x='REPORT_DATE', y='HOLDING_RATIO_30', data=index, label='前30大核心资产占比', color=area_color_list[10])
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        ax1.set_xticklabels(labels=index['LABEL'].to_list(), rotation=90)
        ax2.set_xticklabels(labels=index['LABEL'].to_list(), rotation=90)
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        ax1.set_ylim([0.0, 0.8])
        ax2.set_ylim([1.0, 3.5])
        # ax1.set_ylim([0.0, 0.6])
        # ax2.set_ylim([1.0, 3.5])
        ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('公募基金持仓集中度与市场表现')
        plt.tight_layout()
        plt.savefig('{0}fund_cen.png'.format(self.data_path))

        windA_finance = pd.read_excel('{}windA_finance.xlsx'.format(self.data_path))
        windA_finance['REPORT_DATE'] = windA_finance['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        windA_finance = windA_finance[windA_finance['REPORT_DATE'].isin(self.report_dates)]
        windA_finance = windA_finance[['REPORT_DATE', 'YOY']]
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        sns.lineplot(ax=ax1, x='REPORT_DATE', y='HOLDING_RATIO_100', data=fund_stock_100, label='前100大核心资产占比', color=line_color_list[0])
        sns.lineplot(ax=ax2, x='REPORT_DATE', y='YOY', data=windA_finance, label='A股市场归母净利润同比增速', color=line_color_list[1])
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        ax1.set_xticklabels(labels=self.report_dates, rotation=90)
        ax2.set_xticklabels(labels=self.report_dates, rotation=90)
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        ax1.set_ylim([0.3, 1.0])
        ax2.set_ylim([-30, 60])
        # ax1.set_ylim([0, 0.8])
        # ax2.set_ylim([-20, 60])
        ax1.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('公募基金持仓集中度与A股业绩表现')
        plt.tight_layout()
        plt.savefig('{0}fund_finance.png'.format(self.data_path))
        return

    def all_fund_industry_compare(self):
        label_type = 'INDUSTRY_SW2'
        fund_industry_1st = FEDB().read_data(self.date, label_type)
        fund_industry_1st = fund_industry_1st[fund_industry_1st['IS_ZC'] == 1]
        fund_industry_1st = fund_industry_1st.pivot(index='REPORT_HISTORY_DATE', columns='LABEL_NAME', values='LABEL_VALUE')
        fund_industry_1st = fund_industry_1st.sort_index()
        fund_industry_1st = pd.DataFrame(fund_industry_1st.loc[self.report_dates[-1]] - fund_industry_1st.loc[self.report_dates[-2]])
        fund_industry_1st.columns = ['公募持仓']
        stock_industry_sw1 = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == 2]
        hk_list = []
        for date in self.report_dates[-2:]:
            hk_date = pd.read_excel('{0}wind_hk_cash_{1}.xlsx'.format(self.data_path, date))
            hk_date = hk_date[['证券代码', '交易日期', '持股市值(亿元)']]
            hk_date.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'HOLDING_MARKET_VALUE']
            hk_date['TICKER_SYMBOL'] = hk_date['TICKER_SYMBOL'].apply(lambda x: str(x).split('.')[0])
            hk_date['REPORT_DATE'] = hk_date['REPORT_DATE'].apply(lambda x: str(x)[:10].replace('-', ''))
            hk_date = hk_date.merge(stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='left')
            hk_date = hk_date[['REPORT_DATE', 'INDUSTRY_NAME', 'HOLDING_MARKET_VALUE']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
            hk_date['HOLDING_RATIO'] = hk_date['HOLDING_MARKET_VALUE'] / hk_date['HOLDING_MARKET_VALUE'].sum()
            hk_list.append(hk_date)
        hk_industry_1st = pd.concat(hk_list)
        hk_industry_1st = hk_industry_1st.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='HOLDING_RATIO')
        hk_industry_1st = hk_industry_1st.sort_index().diff().dropna().T.rename(columns={self.date: '外资持仓'})
        fund_industry_1st['公募持仓_abs'] = fund_industry_1st['公募持仓'].abs()
        fund_industry_1st['公募持仓排名'] = fund_industry_1st['公募持仓_abs'].rank()
        fund_industry_1st_up = fund_industry_1st[fund_industry_1st['公募持仓'] > 0]
        fund_industry_1st_up['公募持仓排名'] = fund_industry_1st_up['公募持仓排名'] * (1.0)
        fund_industry_1st_down = fund_industry_1st[fund_industry_1st['公募持仓'] < 0]
        fund_industry_1st_down['公募持仓排名'] = fund_industry_1st_down['公募持仓排名'] * (-1.0)
        fund_industry_1st = pd.concat([fund_industry_1st_up, fund_industry_1st_down])
        hk_industry_1st['外资持仓_abs'] = hk_industry_1st['外资持仓'].abs()
        hk_industry_1st['外资持仓排名'] = hk_industry_1st['外资持仓_abs'].rank()
        hk_industry_1st_up = hk_industry_1st[hk_industry_1st['外资持仓'] > 0]
        hk_industry_1st_up['外资持仓排名'] = hk_industry_1st_up['外资持仓排名'] * (1.0)
        hk_industry_1st_down = hk_industry_1st[hk_industry_1st['外资持仓'] < 0]
        hk_industry_1st_down['外资持仓排名'] = hk_industry_1st_down['外资持仓排名'] * (-1.0)
        hk_industry_1st = pd.concat([hk_industry_1st_up, hk_industry_1st_down])
        fund_industry_1st = fund_industry_1st[['公募持仓排名']].merge(hk_industry_1st[['外资持仓排名']], left_index=True, right_index=True, how='left')
        plt.figure(figsize=(12, 12))
        plt.scatter(fund_industry_1st['公募持仓排名'], fund_industry_1st['外资持仓排名'], color=bar_color_list[0])
        for i in range(len(fund_industry_1st)):
            plt.annotate(list(fund_industry_1st.index)[i], xy=(fund_industry_1st['公募持仓排名'][i], fund_industry_1st['外资持仓排名'][i]), xytext=(fund_industry_1st['公募持仓排名'][i] + 0.1, fund_industry_1st['外资持仓排名'][i] + 0.1))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('公募增减持排名')
        plt.ylabel('外资增减持排名')
        plt.xlim([-150, 150])
        plt.ylim([-150, 150])
        plt.hlines(y=0, xmin=-150, xmax=150, linestyles='dashed', color='#959595')
        plt.vlines(x=0, ymin=-150, ymax=150, linestyles='dashed', color='#959595')
        plt.title('公募/外资增减持对比')
        plt.tight_layout()
        plt.savefig('{0}fund_compare_sw2.png'.format(self.data_path))
        return

    def get_analysis(self):
        self.all_fund_scale()
        self.all_fund_position()
        self.all_fund_industry_select(['电力设备', '食品饮料', '医药生物', '电子'])
        self.all_fund_industry_excess()
        self.all_fund_stock_holding()
        self.all_fund_industry_compare()

class holding_analysis_v3:
    def __init__(self, date, data_path):
        self.date = date
        self.data_path = data_path
        self.load()

    def load(self):
        # 基金池
        self.fund = fund_info(date)
        self.fund.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table', mode='w')
        self.fund = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund.hdf', key='table')
        # 基金持仓
        self.fund_holding = HBDB().read_fund_holding_given_codes(self.fund['FUND_CODE'].unique().tolist())
        self.fund_holding.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table', mode='w')
        self.fund_holding = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding.hdf', key='table')
        self.fund_holding = self.fund_holding.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'ccsz': 'HOLDING_MARKET_VALUE', 'ccsl': 'HOLDING_AMOUNT', 'zjbl': 'MV_IN_NA'})
        self.fund_holding['REPORT_DATE'] = self.fund_holding['REPORT_DATE'].astype(str)
        self.fund_holding_diff = HBDB().read_fund_holding_diff_given_codes(self.fund['FUND_CODE'].unique().tolist())
        self.fund_holding_diff.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table', mode='w')
        self.fund_holding_diff = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/fund_holding_diff.hdf', key='table')
        self.fund_holding_diff = self.fund_holding_diff.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'zqdm': 'TICKER_SYMBOL', 'zqmc': 'SEC_SHORT_NAME', 'zclb': 'IS_ZC', 'zgblbd': 'MV_IN_NA_DIFF', 'sfsqzcg': 'IS_LAST_ZC'})
        self.fund_holding_diff['REPORT_DATE'] = self.fund_holding_diff['REPORT_DATE'].astype(str)
        self.fund_holding_diff = self.fund_holding_diff.dropna(subset=['IS_ZC'])
        self.fund_holding_diff['IS_ZC'] = self.fund_holding_diff['IS_ZC'].astype(int)
        # 基金重仓
        self.fund_zc_holding = self.fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).groupby(['FUND_CODE', 'REPORT_DATE']).head(10)
        self.fund_zc_holding_diff = self.fund_holding_diff[self.fund_holding_diff['IS_ZC'] == 1]
        # # 基金全仓
        # self.fund_zc_holding = self.fund_holding.sort_values(['FUND_CODE', 'REPORT_DATE', 'MV_IN_NA'], ascending=[True, True, False]).copy(deep=True)
        # self.fund_zc_holding_diff = self.fund_holding_diff[self.fund_holding_diff['IS_ZC'] == 2]
        # 分析区间
        self.report_dates = sorted(self.fund_zc_holding[self.fund_zc_holding['REPORT_DATE'] <= self.date]['REPORT_DATE'].unique().tolist())[-40:]
        # self.report_dates = [date for date in self.report_dates if date[4:] == '0630' or date[4:] == '1231']
        self.fund_zc_holding = self.fund_zc_holding[self.fund_zc_holding['REPORT_DATE'].isin(self.report_dates)]
        self.fund_zc_holding_diff = self.fund_zc_holding_diff[self.fund_zc_holding_diff['REPORT_DATE'].isin(self.report_dates)]
        self.cal, self.trade_cal = get_cal_and_trade_cal('19900101', self.date)
        self.fund_zc_holding = self.fund_zc_holding.merge(self.cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
        self.fund_zc_holding_diff = self.fund_zc_holding_diff.merge(self.cal[['TRADE_DATE', 'RECENT_TRADE_DATE']].rename(columns={'TRADE_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')

        # 基金规模
        fund_aum_list = []
        for idx, td in enumerate(self.report_dates):
            fund_aum_date = HBDB().read_fund_scale_given_date(td)
            fund_aum_date = fund_aum_date if len(fund_aum_date) > 0 else pd.DataFrame(columns=['ZCJZ', 'BBLB1', 'JSRQ', 'JJDM', 'GGRQ', 'ROW_ID'])
            fund_aum_date = fund_aum_date[fund_aum_date['BBLB1'] == 13]
            fund_aum_date = fund_aum_date.sort_values(['JJDM', 'JSRQ', 'GGRQ']).drop_duplicates(['JJDM', 'JSRQ'], keep='last')
            fund_aum_list.append(fund_aum_date)
            print('[PreloadFundAum][{0}/{1}]'.format(idx, len(self.report_dates)))
        self.fund_aum = pd.concat(fund_aum_list, ignore_index=True)
        self.fund_aum.to_hdf('{0}fund_aum.hdf'.format(self.data_path), key='table', mode='w')
        self.fund_aum = pd.read_hdf('{0}fund_aum.hdf'.format(self.data_path), key='table')
        self.fund_aum = self.fund_aum[['JJDM', 'JSRQ', 'ZCJZ']]
        self.fund_aum.columns = ['FUND_CODE', 'REPORT_DATE', 'AUM']
        self.fund_aum['REPORT_DATE'] = self.fund_aum['REPORT_DATE'].astype(str)

        self.fund['FUND_CODE_OF'] = self.fund['FUND_CODE'].apply(lambda x: '{0}.OF'.format(x))
        start_date_hyphen = datetime.strptime(self.report_dates[0], '%Y%m%d').strftime('%Y-%m-%d')
        end_date_hyphen = datetime.strptime(self.report_dates[-1], '%Y%m%d').strftime('%Y-%m-%d')
        self.fund_netprofit = w.wsd(','.join(self.fund['FUND_CODE_OF'].unique().tolist()), "anal_avgnavreturn", start_date_hyphen, end_date_hyphen, "Period=Q;Days=Alldays", usedf=True)[1].reset_index()
        self.fund_netprofit.to_hdf('{0}fund_netprofit.hdf'.format(self.data_path), key='table', mode='w')
        self.fund_netprofit = pd.read_hdf('{0}fund_netprofit.hdf'.format(self.data_path), key='table')
        self.fund_netprofit['index'] = self.fund_netprofit['index'].apply(lambda x: str(x).replace('-', ''))
        self.fund_netprofit = self.fund_netprofit.set_index('index').sort_index()
        self.fund_netprofit = self.fund_netprofit.unstack().reset_index().dropna()
        self.fund_netprofit.columns = ['FUND_CODE', 'REPORT_DATE', 'ANAL_AVGNAVRETURN']
        self.fund_netprofit['FUND_CODE'] = self.fund_netprofit['FUND_CODE'].apply(lambda x: x.split('.')[0])

        self.all_fund = HBDB().read_fund_info()
        self.all_fund = self.all_fund.rename(columns={'jjdm': 'FUND_CODE', 'jjmc': 'FUND_FULL_NAME', 'jjjc': 'FUND_SHORT_NAME', 'clrq': 'BEGIN_DATE', 'zzrq': 'END_DATE', 'jjfl': 'FUND_TYPE_1ST', 'ejfl': 'FUND_TYPE_2ND', 'kffb': 'OPEN_CLOSE'})
        self.all_fund = self.all_fund.dropna(subset=['BEGIN_DATE'])
        self.all_fund['END_DATE'] = self.all_fund['END_DATE'].fillna(20990101)
        self.all_fund['BEGIN_DATE'] = self.all_fund['BEGIN_DATE'].astype(int).astype(str)
        self.all_fund['END_DATE'] = self.all_fund['END_DATE'].astype(int).astype(str)
        self.all_fund['FUND_TYPE_1ST'] = self.all_fund['FUND_TYPE_1ST'].replace({'f': 'FOF型', '1': '股票型', '2': '债券型', '3': '混合型', '4': '另类投资型', '7': '货币型', '9': 'QDII型'})
        self.all_fund['FUND_TYPE_2ND'] = self.all_fund['FUND_TYPE_2ND'].replace(
            {'f3': '债券型FOF', 'f4': '货币型FOF', 'f1': '股票型FOF', 'f2': '混合型FOF', 'f5': '另类投资FOF',
             '13': '普通股票型', '14': '股票型', '15': '增强指数型', '16': '被动指数型',
             '21': '被动指数型债券', '22': '短期纯债型', '23': '混合债券型一级', '24': '混合债券型二级', '25': '增强指数型债券', '26': '债券型',
             '27': '中长期纯债型', '28': '可转换债券型',
             '34': '平衡混合型', '35': '灵活配置型', '36': '混合型', '37': '偏股混合型', '38': '偏债混合型',
             '41': '股票多空', '42': '商品型', '43': 'REITs',
             '91': '股票型QDII', '93': '混合型QDII', '94': '债券型QDII', '95': '另类型QDII'})
        self.all_fund['FUND_TYPE'] = self.all_fund['FUND_TYPE_1ST']
        self.all_fund.loc[self.all_fund['FUND_TYPE_2ND'] == 'REITs', 'FUND_TYPE'] = 'REITs'

        # 中报、半年报
        self.all_fund['FUND_CODE_OF'] = self.all_fund['FUND_CODE'].apply(lambda x: '{0}.OF'.format(x))
        date_hyphen = datetime.strptime(self.date, '%Y%m%d').strftime('%Y-%m-%d')
        self.all_fund_netprofit = w.wsd(','.join(self.all_fund['FUND_CODE_OF'].unique().tolist()), "anal_avgnavreturn", date_hyphen, date_hyphen, "Period=Q;Days=Alldays", usedf=True)[1].reset_index()
        self.all_fund_netprofit.to_hdf('{0}all_fund_netprofit.hdf'.format(self.data_path), key='table', mode='w')
        self.all_fund_netprofit = pd.read_hdf('{0}all_fund_netprofit.hdf'.format(self.data_path), key='table')
        ###################################
        self.all_fund_netprofit = pd.read_excel('{0}all_fund_netprofit.xlsx'.format(self.data_path))
        self.all_fund_netprofit['REPORT_DATE'] = '20220630'
        self.all_fund_netprofit.columns = ['FUND_CODE', 'ANAL_AVGNAVRETURN', 'REPORT_DATE']
        self.all_fund_netprofit['FUND_CODE'] = self.all_fund_netprofit['FUND_CODE'].apply(lambda x: x.split('.')[0])
        ###################################

    def index_compare(self):
        index_daily_k = HBDB().read_index_daily_k_given_date_and_indexs('20190101', ['885001', '881001'])
        index_daily_k = index_daily_k.rename(columns={'zqdm': 'INDEX_SYMBOL', 'zqmc': 'INDEX_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX', 'cjjs': 'TURNOVER_VALUE', 'ltsz': 'NEG_MARKET_VALUE'})
        index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].astype(str)
        index_daily_k = index_daily_k.sort_values('TRADE_DATE')
        index_daily_k = index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX')
        index_daily_k = index_daily_k.rename(columns={'885001': '万得偏股混合型基金指数（885001）', '881001': '万得全A（881001）'})
        index_daily_k = index_daily_k[index_daily_k.index <= self.date]
        index_daily_k_2019 = index_daily_k / index_daily_k.iloc[0]
        index_daily_k_2022 = index_daily_k[index_daily_k.index >= '20220101'] / index_daily_k[index_daily_k.index >= '20220101'].iloc[0]
        index_daily_k_2019.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), index_daily_k_2019.index)
        index_daily_k_2022.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), index_daily_k_2022.index)

        plt.figure(figsize=(12, 6))
        plt.plot(index_daily_k_2019.index, index_daily_k_2019['万得偏股混合型基金指数（885001）'].values, label='万得偏股混合型基金指数（885001）', color='#F04950')
        plt.plot(index_daily_k_2019.index, index_daily_k_2019['万得全A（881001）'].values, label='万得全A（881001）', color='#6268A2')
        plt.legend(loc=2)
        plt.title('2019年以来指数走势比较')
        plt.tight_layout()
        plt.savefig('{0}index_compare_2019.png'.format(self.data_path))

        plt.figure(figsize=(12, 6))
        plt.plot(index_daily_k_2022.index, index_daily_k_2022['万得偏股混合型基金指数（885001）'].values, label='万得偏股混合型基金指数（885001）', color='#F04950')
        plt.plot(index_daily_k_2022.index, index_daily_k_2022['万得全A（881001）'].values, label='万得全A（881001）', color='#6268A2')
        plt.legend(loc=2)
        plt.title('2022年以来指数走势比较')
        plt.tight_layout()
        plt.savefig('{0}index_compare_2022.png'.format(self.data_path))
        return

    def aum_group(self):
        fund_aum_date = self.fund_aum[self.fund_aum['REPORT_DATE'] == self.date]
        fund = self.fund.merge(fund_aum_date[['FUND_CODE', 'AUM']], on=['FUND_CODE'], how='left').dropna(subset='AUM')
        fund = fund[['FUND_FULL_NAME', 'AUM']].groupby('FUND_FULL_NAME').sum()
        fund['AUM'] = fund['AUM'] / 100000000.0
        fund = fund.rename(columns={'AUM': '规模（亿元）'})

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.distplot(fund['规模（亿元）'], ax=ax, bins=500, hist=True, kde=True, color='#F04950')
        plt.ylabel('概率分布')
        plt.tight_layout()
        plt.savefig('{0}aum_dist.png'.format(self.data_path))

        fund_aum_date = self.fund_aum[self.fund_aum['REPORT_DATE'] == self.date]
        fund = self.fund.merge(fund_aum_date[['FUND_CODE', 'AUM']], on=['FUND_CODE'], how='left').dropna(subset='AUM')
        fund['AUM'] = fund['AUM'] / 100000000.0
        stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/stock_valuation.hdf', key='table')
        star_stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/star_stock_valuation.hdf', key='table')
        stock_valuation = stock_valuation.rename(columns={'PE_TTM': 'PE(TTM)', 'PB_LF': 'PB(LF)'})
        star_stock_valuation = star_stock_valuation.rename(columns={'PE_TTM': 'PE(TTM)', 'PB_LF': 'PB(LF)'})
        stock_valuation = stock_valuation[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE', 'PE(TTM)', 'PB(LF)']]
        star_stock_valuation = star_stock_valuation[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE', 'PE(TTM)', 'PB(LF)']]
        stock_valuation = pd.concat([stock_valuation, star_stock_valuation]).sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        fig, ax = plt.subplots(3, 1, figsize=(12, 18))
        for i in range(3):
            if i == 0:
                fund_group = fund[fund['AUM'] <= 50]
                label = '0-50亿元规模基金'
            elif i == 1:
                fund_group = fund[(fund['AUM'] > 50) & (fund['AUM'] <= 100)]
                label = '50-100亿元规模基金'
            else:
                fund_group = fund[fund['AUM'] > 100]
                label = '100亿元以上规模基金'
            fund_zc_holding = self.fund_zc_holding[self.fund_zc_holding['FUND_CODE'].isin(fund_group['FUND_CODE'].unique().tolist())]
            fund_zc_holding = fund_zc_holding.merge(stock_valuation.rename(columns={'TRADE_DATE': 'RECENT_TRADE_DATE'}), on=['RECENT_TRADE_DATE', 'TICKER_SYMBOL'], how='left')
            pe = fund_zc_holding.dropna(subset=['PE(TTM)'])

            pe['PE_MARK'] = np.nan
            pe.loc[(pe['PE(TTM)'] > 0) & (pe['PE(TTM)'] <= 30), 'PE_MARK'] = 'low'
            pe.loc[(pe['PE(TTM)'] > 30) & (pe['PE(TTM)'] <= 50), 'PE_MARK'] = 'middle'
            pe.loc[(pe['PE(TTM)'] > 50) | (pe['PE(TTM)'] <= 0), 'PE_MARK'] = 'high'
            pe = pe[['REPORT_DATE', 'PE_MARK', 'TICKER_SYMBOL']].groupby(['REPORT_DATE', 'PE_MARK']).count().reset_index().rename(columns={'TICKER_SYMBOL': 'PE_COUNT'})
            pe = pe.pivot(index='REPORT_DATE', columns='PE_MARK', values='PE_COUNT').fillna(0)

            pe = pe.apply(lambda x: x / x.sum(), axis=1)
            pe = pe.sort_index()
            pe.columns = ['PE>50（含负）', '0<PE<=30', '30<PE<=50']
            pe = pe[['0<PE<=30', '30<PE<=50', 'PE>50（含负）']]
            ax[i].stackplot(pe.index.tolist(), pe.T.values.tolist(), colors=['#D55659', '#8588B7', '#7D7D7E'], labels=pe.columns.tolist())
            ax[i].legend(loc=2)
            ax[i].set_xticklabels(labels=pe.index.tolist(), rotation=90)
            ax[i].yaxis.set_major_formatter(FuncFormatter(to_100percent))
            ax[i].set_title('{0}估值分布（PE）'.format(label))
        plt.tight_layout()
        plt.savefig('{0}aum_group_pe.png'.format(self.data_path))
        return

    def turnover(self):
        fund_turnover = HBDB().read_fund_turnover_given_codes(self.fund['FUND_CODE'].unique().tolist())
        fund_turnover.to_hdf('{0}fund_turnover.hdf'.format(self.data_path), key='table', mode='w')
        fund_turnover = pd.read_hdf('{0}fund_turnover.hdf'.format(self.data_path), key='table')
        fund_turnover = fund_turnover.rename(columns={'jjdm': 'FUND_CODE', 'jsrq': 'REPORT_DATE', 'tjqj': 'TYPE', 'hsl': 'TURNOVER'})
        fund_turnover = fund_turnover[fund_turnover['TYPE'].isin(['1', '3'])]
        fund_turnover['TURNOVER'] = fund_turnover['TURNOVER'] * 2.0
        fund_turnover = fund_turnover[['REPORT_DATE', 'TURNOVER']].groupby(['REPORT_DATE']).mean().reset_index().iloc[-20:]

        plt.figure(figsize=(12, 6))
        sns.barplot(x='REPORT_DATE', y='TURNOVER', data=fund_turnover, color=bar_color_list[0])
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('')
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('年化单边换手率')
        plt.tight_layout()
        plt.savefig('{0}turnover.png'.format(self.data_path))
        return

    def netprofit(self):
        # 不同类型基金差别（中报、年报）
        fund_nav_adj = HBDB().read_mutual_fund_nav_adj_given_date(self.report_dates[-1])
        fund_nav_adj = fund_nav_adj.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'NAV_ADJ'})
        fund_nav_adj = fund_nav_adj[['FUND_CODE', 'NAV_ADJ']].rename(columns={'NAV_ADJ': self.report_dates[-1]})
        fund_nav_adj_last = HBDB().read_mutual_fund_nav_adj_given_date(self.report_dates[-2])
        fund_nav_adj_last = fund_nav_adj_last.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'NAV_ADJ'})
        fund_nav_adj_last = fund_nav_adj_last[['FUND_CODE', 'NAV_ADJ']].rename(columns={'NAV_ADJ': self.report_dates[-2]})
        fund_nav_adj = fund_nav_adj.merge(fund_nav_adj_last, on=['FUND_CODE'], how='left')
        fund_nav_adj['ANAL_RET'] = (fund_nav_adj[self.report_dates[-1]] / fund_nav_adj[self.report_dates[-2]] - 1) * 100
        fund_return = self.all_fund[['FUND_TYPE', 'FUND_CODE']].merge(self.all_fund_netprofit[['FUND_CODE', 'ANAL_AVGNAVRETURN']], on=['FUND_CODE'], how='left').merge(fund_nav_adj[['FUND_CODE', 'ANAL_RET']], on=['FUND_CODE'], how='left')
        fund_return = fund_return.dropna()
        fund_return_navret = fund_return[['FUND_TYPE', 'ANAL_RET']].groupby('FUND_TYPE').mean().reset_index()
        fund_return_navreturn = fund_return[['FUND_TYPE', 'ANAL_AVGNAVRETURN']].groupby('FUND_TYPE').mean().reset_index()
        fund_return = fund_return_navret.merge(fund_return_navreturn, on=['FUND_TYPE'], how='left')
        fund_return['DIFF'] = fund_return['ANAL_RET'] - fund_return['ANAL_AVGNAVRETURN']
        fund_return = fund_return.sort_values('DIFF')
        rank_list = fund_return['FUND_TYPE'].unique().tolist()
        fund_return_navret = fund_return_navret.rename(columns={'ANAL_RET': 'RETURN'})
        fund_return_navret['TYPE'] = '基金净值增长率'
        fund_return_navret['FUND_TYPE'] = fund_return_navret['FUND_TYPE'].astype('category')
        fund_return_navret['FUND_TYPE'].cat.reorder_categories(rank_list, inplace=True)
        fund_return_navret = fund_return_navret.sort_values('FUND_TYPE')
        fund_return_navreturn = fund_return_navreturn.rename(columns={'ANAL_AVGNAVRETURN': 'RETURN'})
        fund_return_navreturn['TYPE'] = '加权平均净值利润率'
        fund_return_navreturn['FUND_TYPE'] = fund_return_navreturn['FUND_TYPE'].astype('category')
        fund_return_navreturn['FUND_TYPE'].cat.reorder_categories(rank_list, inplace=True)
        fund_return_navreturn = fund_return_navreturn.sort_values('FUND_TYPE')
        fund_return_disp = pd.concat([fund_return_navret, fund_return_navreturn])

        fig, ax1 = plt.subplots(figsize=(12, 8))
        ax2 = ax1.twinx()
        sns.barplot(ax=ax1, x='FUND_TYPE', y='RETURN', data=fund_return_disp, hue='TYPE', palette=[bar_color_list[0], bar_color_list[7]])
        sns.barplot(ax=ax2, x='FUND_TYPE', y='DIFF', data=fund_return, label='差值', palette=[bar_color_list[14]])
        for bar in ax2.patches:
            bar.set_width(0.4)
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        ax1.set_xticklabels(labels=fund_return['FUND_TYPE'].unique().tolist())
        ax2.set_xticklabels(labels=fund_return['FUND_TYPE'].unique().tolist())
        ax1.set_ylim([fund_return_disp['RETURN'].min() * 1.5, fund_return_disp['RETURN'].min() * (-1.0) * 1.5])
        ax2.set_ylim([(fund_return['DIFF'].min() - (fund_return_disp['RETURN'].max() - fund_return_disp['RETURN'].min())) * 1.2, fund_return['DIFF'].max() * 3])
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        plt.title('基金净值增长率与加权平均净值利润率')
        plt.tight_layout()
        plt.savefig('{0}fund_return.png'.format(self.data_path))

        # 主动权益型基金基金不同年份差别（年度、半年度）
        fund_netprofit = self.fund_netprofit.dropna()
        fund_netprofit = fund_netprofit[fund_netprofit['REPORT_DATE'].str.slice(4, 8) == '1231']
        fund_netprofit['YEAR'] = fund_netprofit['REPORT_DATE'].apply(lambda x: x[:4])
        year_list = sorted(fund_netprofit['YEAR'].unique().tolist())
        ###################################
        fund_netprofit_last = self.all_fund_netprofit[self.all_fund_netprofit['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        fund_netprofit_last['YEAR'] = '2022H1'
        fund_netprofit_last = fund_netprofit_last[['FUND_CODE', 'REPORT_DATE', 'ANAL_AVGNAVRETURN', 'YEAR']]
        fund_netprofit = pd.concat([fund_netprofit, fund_netprofit_last])
        ###################################
        fund_nav_adj_list = []
        for year in [str(int(year_list[0]) - 1)] + year_list:
            print(year)
            date = self.trade_cal[self.trade_cal['TRADE_DATE'] <= year + '1231']['TRADE_DATE'].iloc[-1]
            fund_nav_adj_date = HBDB().read_mutual_fund_nav_adj_given_date(date)
            fund_nav_adj_date = fund_nav_adj_date.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'NAV_ADJ'})
            fund_nav_adj_date['YEAR'] = year
            fund_nav_adj_list.append(fund_nav_adj_date)
        fund_nav_adj = pd.concat(fund_nav_adj_list)
        fund_nav_adj.to_hdf('{0}fund_nav_adj.hdf'.format(self.data_path), key='table', mode='w')
        fund_nav_adj = pd.read_hdf('{0}fund_nav_adj.hdf'.format(self.data_path), key='table')
        ###################################
        fund_nav_adj_last = HBDB().read_mutual_fund_nav_adj_given_date('20220630')
        fund_nav_adj_last = fund_nav_adj_last.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'NAV_ADJ'})
        fund_nav_adj_last['YEAR'] = '2022H1'
        fund_nav_adj = pd.concat([fund_nav_adj, fund_nav_adj_last])
        ###################################
        fund_nav_adj = fund_nav_adj.pivot(index='YEAR', columns='FUND_CODE', values='NAV_ADJ').sort_index()
        fund_nav_adj = fund_nav_adj.pct_change().unstack().reset_index()
        fund_nav_adj.columns = ['FUND_CODE', 'YEAR', 'ANAL_RET']
        fund_nav_adj['ANAL_RET'] = fund_nav_adj['ANAL_RET'] * 100.0
        fund_return = fund_netprofit.merge(fund_nav_adj, on=['FUND_CODE', 'YEAR'], how='left')
        fund_return = fund_return.dropna()
        fund_return['DIFF'] = fund_return['ANAL_RET'] - fund_return['ANAL_AVGNAVRETURN']
        fund_diff_list = [fund_return[fund_return['YEAR'] == year]['DIFF'] for year in year_list + ['2022H1']]

        plt.figure(figsize=(12, 6))
        plt.boxplot(fund_diff_list, labels=year_list + ['2022H1'], vert=True, widths=0.25, flierprops={'marker': 'o', 'markersize': 1}, meanline=True, showmeans=True, showfliers=False)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.title('主动权益型基金净值增长率与加权平均净值利润率差值分布')
        plt.tight_layout()
        plt.savefig('{0}fund_return_year.png'.format(self.data_path))

        fund_return['EXCEED'] = np.nan
        fund_return.loc[fund_return['DIFF'] >= 0, 'EXCEED'] = 1
        fund_return.loc[fund_return['DIFF'] < 0, 'EXCEED'] = 0
        fund_return_count = fund_return[['YEAR', 'EXCEED', 'FUND_CODE']].groupby(['YEAR', 'EXCEED']).count().reset_index()
        fund_return_count = fund_return_count.pivot(index='YEAR', columns='EXCEED', values='FUND_CODE')
        fund_return_count = fund_return_count.apply(lambda x: x / x.sum(), axis=1)
        fund_return_count = fund_return_count.sort_index()
        fund_return_count.columns = ['基金净值增长率 < 加权平均净值利润率', '基金净值增长率 >= 加权平均净值利润率']
        plt.figure(figsize=(12, 6))
        plt.stackplot(fund_return_count.index.tolist(), fund_return_count.T.values.tolist(), colors=['#D55659', '#8588B7'], labels=fund_return_count.columns.tolist())
        plt.legend(loc=2)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.title('主动权益型基金净值增长率领先/落后加权平均净值利润率的基金数量占比')
        plt.tight_layout()
        plt.savefig('{0}fund_return_year_count.png'.format(self.data_path))

        all_fund_netprofit = self.all_fund_netprofit.dropna()
        all_fund_netprofit = all_fund_netprofit[all_fund_netprofit['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        all_fund_netprofit = all_fund_netprofit.merge(self.all_fund[['FUND_CODE', 'FUND_SHORT_NAME', 'FUND_TYPE_2ND']], on=['FUND_CODE'], how='left')
        all_fund_netprofit['LAST'] = all_fund_netprofit['FUND_SHORT_NAME'].apply(lambda x: x[-1])
        all_fund_netprofit = all_fund_netprofit[all_fund_netprofit['LAST'].isin(['合', '票', '活', '强', '技', '式', '选', '起', '通', ')', '混', '型', '长'])]
        for type in all_fund_netprofit['FUND_TYPE_2ND'].unique().tolist():
            fund_netprofit_type = all_fund_netprofit[all_fund_netprofit['FUND_TYPE_2ND'] == type]
            fund_netprofit_type = fund_netprofit_type.sort_values('ANAL_AVGNAVRETURN', ascending=False).iloc[:10]
            plt.figure(figsize=(12, 6))
            sns.barplot(x='FUND_SHORT_NAME', y='ANAL_AVGNAVRETURN', data=fund_netprofit_type, color=bar_color_list[0])
            plt.xticks(rotation=45)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('')
            plt.ylabel('加权平均净值利润率')
            plt.title('基民实际回报最高的{0}基金TOP10'.format(type))
            plt.tight_layout()
            plt.savefig('{0}{1}.png'.format(self.data_path, type))
        return

    def stock_change(self):
        stock_change = pd.read_excel('{0}stock_change.xlsx'.format(self.data_path))
        stock_change['FUND_CODE'] = stock_change['FUND_CODE'].astype(str)
        stock_change['END_DATE'] = stock_change['END_DATE'].astype(str)
        stock_change['PUBLISH_DATE'] = stock_change['PUBLISH_DATE'].astype(str)
        stock_change = stock_change[stock_change['FUND_CODE'].isin(self.fund['FUND_CODE'].unique().tolist())]
        stock_change.to_hdf('{0}stock_change.hdf'.format(self.data_path), key='table', mode='w')
        stock_change = pd.read_hdf('{0}stock_change.hdf'.format(self.data_path), key='table')
        stock_change = stock_change.merge(self.fund[['FUND_CODE', 'FUND_SHORT_NAME']], on=['FUND_CODE'], how='left')
        stock_change['LAST'] = stock_change['FUND_SHORT_NAME'].apply(lambda x: x[-1])
        stock_change = stock_change[stock_change['LAST'].isin(['合', '票', '活', '强', '技', '式', '选', '起', '通', ')', '混', '型', '长'])]
        stock_change_buy = stock_change[stock_change['CHANGE_TYPE'] == 1]
        stock_change_sell = stock_change[stock_change['CHANGE_TYPE'] == 2]
        return

    def get_analysis(self):
        self.index_compare()
        self.aum_group()
        self.turnover()
        self.netprofit()
        self.stock_change()
        return


if __name__ == "__main__":
    date = '20220630'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/mutual_analysis/'
    holding_analysis_v1(date)
    holding_analysis_v2(date, data_path).get_analysis()
    holding_analysis_v3(date, data_path).get_analysis()