# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.xwq.analysis.service.industry_analysis_data import get_stock_info
import numpy as np
import pandas as pd


if __name__ == '__main__':
    # 给定date，九种创新高类型
    date = '20220630'
    report_date = '20220331'
    last_report_date = '20210331'
    mark_list = ['HighestPrice', 'HighestPriceRW', 'HighestPriceTW', 'HighestPriceRM', 'HighestPriceTM',
                 'HighestPriceRMThree', 'HighestPriceRMSix', 'HighestPriceRY', 'HighestPriceYTD']
    mark_dict = {'HighestPrice': '创历史新高', 'HighestPriceRW': '创近一周新高', 'HighestPriceTW': '本周以来新高',
                 'HighestPriceRM': '创近一月新高', 'HighestPriceTM': '本月以来新高', 'HighestPriceRMThree': '创近三月新高',
                 'HighestPriceRMSix': '创近半年新高', 'HighestPriceRY': '创近一年新高', 'HighestPriceYTD': '今年以来新高'}
    df_list = []
    for mark in mark_list:
        print(mark)
        df = HBDB().read_stock_heightest_given_date(date)
        df_star = HBDB().read_star_stock_heightest_given_date(date)
        df = pd.concat([df, df_star])
        df = df.loc[df['TICKER_SYMBOL'].str.len() == 6]
        df = df.loc[df['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        df = df[['TICKER_SYMBOL', 'SEC_SHORT_NAME', mark.upper()]]
        df = df[df[mark.upper()] == 1]
        df['MARK'] = mark_dict[mark]
        df = df[['MARK', 'TICKER_SYMBOL', 'SEC_SHORT_NAME']].sort_values('TICKER_SYMBOL').reset_index().drop('index', axis=1)

        stock_industry = HBDB().read_stock_industry()
        stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/stock_industry.hdf', key='table', mode='w')
        stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/stock_industry.hdf', key='table')
        stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW', 'credt_etl': 'CREDT_ETL'})
        stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
        stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
        stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
        stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
        stock_industry = stock_industry.sort_values(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL', 'CREDT_ETL']).drop_duplicates(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL'], keep='last')
        stock_industry_sw = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
        stock_industry_sw1 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 1]
        stock_industry_sw2 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 2]
        stock_industry_sw3 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 3]
        stock_industry_sw1 = stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW1'})
        stock_industry_sw2 = stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW2'})
        stock_industry_sw3 = stock_industry_sw3[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW3'})

        mv = HBDB().read_stock_market_value_given_date(date)
        mv_star = HBDB().read_star_stock_market_value_given_date(date)
        mv = pd.concat([mv, mv_star])
        mv = mv[['TICKER_SYMBOL', 'MARKET_VALUE']]
        mv.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/mv.hdf', key='table', mode='w')
        mv = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/mv.hdf', key='table')

        val = HBDB().read_stock_valuation_given_date(date)
        val_star = HBDB().read_star_stock_valuation_given_date(date)
        val = pd.concat([val, val_star])
        val = val[['TICKER_SYMBOL', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]
        val.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/val.hdf', key='table', mode='w')
        val = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/val.hdf', key='table')

        fmt = HBDB().read_stock_finance_given_date(report_date)
        fmt_star = HBDB().read_star_stock_finance_given_date(report_date)
        fmt = pd.concat([fmt, fmt_star])
        fmt = fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        last_fmt = HBDB().read_stock_finance_given_date(last_report_date)
        last_fmt_star = HBDB().read_star_stock_finance_given_date(last_report_date)
        last_fmt = pd.concat([last_fmt, last_fmt_star])
        last_fmt = last_fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        last_fmt = last_fmt[['TICKER_SYMBOL', 'ROE_TTM', 'GROSS_TTM']]
        last_fmt.columns = ['TICKER_SYMBOL', 'LAST_ROE_TTM', 'LAST_GROSS_TTM']
        fmt = fmt.merge(last_fmt, on=['TICKER_SYMBOL'], how='left')
        fmt['ROE_TTM_YOY'] = (fmt['ROE_TTM'] - fmt['LAST_ROE_TTM']) / abs(fmt['LAST_ROE_TTM'])
        fmt['GROSS_TTM_YOY'] = (fmt['GROSS_TTM'] - fmt['LAST_GROSS_TTM']) / abs(fmt['LAST_GROSS_TTM'])
        fmt = fmt[['TICKER_SYMBOL', 'MAIN_INCOME_YOY', 'NET_PROFIT_YOY', 'ROE_TTM_YOY', 'GROSS_TTM_YOY']]
        fmt.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt.hdf', key='table', mode='w')
        fmt = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt.hdf', key='table')

        df = df.merge(stock_industry_sw1, on=['TICKER_SYMBOL'], how='left') \
            .merge(stock_industry_sw2, on=['TICKER_SYMBOL'], how='left') \
            .merge(stock_industry_sw3, on=['TICKER_SYMBOL'], how='left') \
            .merge(mv, on=['TICKER_SYMBOL'], how='left') \
            .merge(val, on=['TICKER_SYMBOL'], how='left') \
            .merge(fmt, on=['TICKER_SYMBOL'], how='left')
        df['MARKET_VALUE'] = df['MARKET_VALUE'].apply(lambda x: round(x / 100000000.0, 2))
        df['PE_TTM'] = df['PE_TTM'].apply(lambda x: round(x, 2))
        df['PB_LF'] = df['PB_LF'].apply(lambda x: round(x, 2))
        df['PEG'] = df['PEG'].apply(lambda x: round(x, 2))
        df['DIVIDEND_RATIO_TTM'] = df['DIVIDEND_RATIO_TTM'].apply(lambda x: round(x, 2))
        df['MAIN_INCOME_YOY'] = df['MAIN_INCOME_YOY'].apply(lambda x: round(x, 2))
        df['NET_PROFIT_YOY'] = df['NET_PROFIT_YOY'].apply(lambda x: round(x, 2))
        df['ROE_TTM_YOY'] = df['ROE_TTM_YOY'].apply(lambda x: round(x * 100.0, 2))
        df['GROSS_TTM_YOY'] = df['GROSS_TTM_YOY'].apply(lambda x: round(x * 100.0, 2))
        df.columns = ['创新高类型', '股票代码', '股票名称', '申万一级行业', '申万二级行业', '申万三级行业', '市值(亿)', 'PE(TTM)', 'PB(LF)', 'PEG', '股息率(%)', '营业收入同比增长(%)', '归母净利润同比增长(%)', 'ROE(TTM)同比增长(%)', '毛利率(TTM)同比增长(%)']
        df.loc[df.shape[0]] = [np.nan] * df.shape[1]
        df_list.append(df)
    df = pd.concat(df_list)
    df.to_excel('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/创新高_{0}.xlsx'.format(date))

    ####################################################################################################################
    ####################################################################################################################
    # 给定创新高类型，汇总区间内创新高个股
    start_date = '20220101'
    end_date = '20220630'
    mark = 'HighestPrice'
    mark_name = '创历史新高'
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    date_list = trade_df['TRADE_DATE'].unique().tolist()

    df_list = []
    for date in date_list:
        print(date)
        df = HBDB().read_stock_heightest_given_date(date)
        df_star = HBDB().read_star_stock_heightest_given_date(date)
        df = pd.concat([df, df_star])
        df = df.loc[df['TICKER_SYMBOL'].str.len() == 6]
        df = df.loc[df['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        df = df[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE', mark.upper()]]
        df = df[df[mark.upper()] == 1]
        df['MARK'] = mark_name
        df = df[['MARK', 'TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'CLOSE_PRICE']].sort_values('TICKER_SYMBOL').reset_index().drop('index', axis=1)

        stock_industry = HBDB().read_stock_industry()
        stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/stock_industry.hdf', key='table', mode='w')
        stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/stock_industry.hdf', key='table')
        stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'fljb': 'INDUSTRY_TYPE', 'hyhfbz': 'INDUSTRY_VERSION', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW', 'credt_etl': 'CREDT_ETL'})
        stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
        stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
        stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
        stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
        stock_industry = stock_industry.sort_values(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL', 'CREDT_ETL']).drop_duplicates(['INDUSTRY_VERSION', 'INDUSTRY_TYPE', 'TICKER_SYMBOL'], keep='last')
        stock_industry_sw = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
        stock_industry_sw1 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 1]
        stock_industry_sw2 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 2]
        stock_industry_sw3 = stock_industry_sw[stock_industry_sw['INDUSTRY_TYPE'] == 3]
        stock_industry_sw1 = stock_industry_sw1[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW1'})
        stock_industry_sw2 = stock_industry_sw2[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW2'})
        stock_industry_sw3 = stock_industry_sw3[['TICKER_SYMBOL', 'INDUSTRY_NAME']].rename(columns={'INDUSTRY_NAME': 'INDUSTRY_NAME_SW3'})

        mv = HBDB().read_stock_market_value_given_date(date)
        mv_star = HBDB().read_star_stock_market_value_given_date(date)
        mv = pd.concat([mv, mv_star])
        mv = mv[['TICKER_SYMBOL', 'MARKET_VALUE']]

        val = HBDB().read_stock_valuation_given_date(date)
        val_star = HBDB().read_star_stock_valuation_given_date(date)
        val = pd.concat([val, val_star])
        val = val[['TICKER_SYMBOL', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]

        # fmt = HBDB().read_stock_finance_given_date('20211231')
        # fmt_star = HBDB().read_star_stock_finance_given_date('20211231')
        # fmt = pd.concat([fmt, fmt_star])
        # fmt = fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        # last_fmt = HBDB().read_stock_finance_given_date('20201231')
        # last_fmt_star = HBDB().read_star_stock_finance_given_date('20201231')
        # last_fmt = pd.concat([last_fmt, last_fmt_star])
        # last_fmt = last_fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        # last_fmt = last_fmt[['TICKER_SYMBOL', 'ROE_TTM', 'GROSS_TTM']]
        # last_fmt.columns = ['TICKER_SYMBOL', 'LAST_ROE_TTM', 'LAST_GROSS_TTM']
        # fmt = fmt.merge(last_fmt, on=['TICKER_SYMBOL'], how='left')
        # fmt['ROE_TTM_YOY'] = (fmt['ROE_TTM'] - fmt['LAST_ROE_TTM']) / abs(fmt['LAST_ROE_TTM'])
        # fmt['GROSS_TTM_YOY'] = (fmt['GROSS_TTM'] - fmt['LAST_GROSS_TTM']) / abs(fmt['LAST_GROSS_TTM'])
        # fmt = fmt[['TICKER_SYMBOL', 'MAIN_INCOME_YOY', 'NET_PROFIT_YOY', 'ROE_TTM_YOY', 'GROSS_TTM_YOY']]
        # fmt.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt_2021A.hdf', key='table', mode='w')
        # fmt = HBDB().read_stock_finance_given_date('20220331')
        # fmt_star = HBDB().read_star_stock_finance_given_date('20220331')
        # fmt = pd.concat([fmt, fmt_star])
        # fmt = fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        # last_fmt = HBDB().read_stock_finance_given_date('20210331')
        # last_fmt_star = HBDB().read_star_stock_finance_given_date('20210331')
        # last_fmt = pd.concat([last_fmt, last_fmt_star])
        # last_fmt = last_fmt.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        # last_fmt = last_fmt[['TICKER_SYMBOL', 'ROE_TTM', 'GROSS_TTM']]
        # last_fmt.columns = ['TICKER_SYMBOL', 'LAST_ROE_TTM', 'LAST_GROSS_TTM']
        # fmt = fmt.merge(last_fmt, on=['TICKER_SYMBOL'], how='left')
        # fmt['ROE_TTM_YOY'] = (fmt['ROE_TTM'] - fmt['LAST_ROE_TTM']) / abs(fmt['LAST_ROE_TTM'])
        # fmt['GROSS_TTM_YOY'] = (fmt['GROSS_TTM'] - fmt['LAST_GROSS_TTM']) / abs(fmt['LAST_GROSS_TTM'])
        # fmt = fmt[['TICKER_SYMBOL', 'MAIN_INCOME_YOY', 'NET_PROFIT_YOY', 'ROE_TTM_YOY', 'GROSS_TTM_YOY']]
        # fmt.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt_2022Q1.hdf', key='table', mode='w')
        if date <= '20220331':
            fmt = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt_2021A.hdf', key='table')
        else:
            fmt = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/fmt_2022Q1.hdf', key='table')

        df = df.merge(stock_industry_sw1, on=['TICKER_SYMBOL'], how='left') \
            .merge(stock_industry_sw2, on=['TICKER_SYMBOL'], how='left') \
            .merge(stock_industry_sw3, on=['TICKER_SYMBOL'], how='left') \
            .merge(mv, on=['TICKER_SYMBOL'], how='left') \
            .merge(val, on=['TICKER_SYMBOL'], how='left') \
            .merge(fmt, on=['TICKER_SYMBOL'], how='left')
        df['MARKET_VALUE'] = df['MARKET_VALUE'].apply(lambda x: round(x / 100000000.0, 2))
        df['PE_TTM'] = df['PE_TTM'].apply(lambda x: round(x, 2))
        df['PB_LF'] = df['PB_LF'].apply(lambda x: round(x, 2))
        df['PEG'] = df['PEG'].apply(lambda x: round(x, 2))
        df['DIVIDEND_RATIO_TTM'] = df['DIVIDEND_RATIO_TTM'].apply(lambda x: round(x, 2))
        df['MAIN_INCOME_YOY'] = df['MAIN_INCOME_YOY'].apply(lambda x: round(x, 2))
        df['NET_PROFIT_YOY'] = df['NET_PROFIT_YOY'].apply(lambda x: round(x, 2))
        df['ROE_TTM_YOY'] = df['ROE_TTM_YOY'].apply(lambda x: round(x * 100.0, 2))
        df['GROSS_TTM_YOY'] = df['GROSS_TTM_YOY'].apply(lambda x: round(x * 100.0, 2))
        df.columns = ['创新高类型', '创新高日期', '股票代码', '股票名称', '收盘价格', '申万一级行业', '申万二级行业', '申万三级行业', '市值(亿)', 'PE(TTM)', 'PB(LF)', 'PEG', '股息率(%)', '营业收入同比增长(%)', '归母净利润同比增长(%)', 'ROE(TTM)同比增长(%)', '毛利率(TTM)同比增长(%)']
        df_list.append(df)
    df = pd.concat(df_list)
    df_first = df.sort_values(['股票代码', '创新高日期']).drop_duplicates('股票代码', keep='first')
    df_first['区间内首次创新高'] = 1
    df_last = df.sort_values(['股票代码', '创新高日期']).drop_duplicates('股票代码', keep='last')
    df_last['区间内收盘价最高'] = 1
    df = df.merge(df_first[['股票代码', '创新高日期', '区间内首次创新高']], on=['股票代码', '创新高日期'], how='left')\
           .merge(df_last[['股票代码', '创新高日期', '区间内收盘价最高']], on=['股票代码', '创新高日期'], how='left')
    df = df[['创新高类型', '创新高日期', '区间内首次创新高', '股票代码', '股票名称', '区间内收盘价最高', '收盘价格', '申万一级行业', '申万二级行业', '申万三级行业', '市值(亿)', 'PE(TTM)', 'PB(LF)', 'PEG', '股息率(%)', '营业收入同比增长(%)', '归母净利润同比增长(%)', 'ROE(TTM)同比增长(%)', '毛利率(TTM)同比增长(%)']]
    df.to_excel('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/创新高.xlsx')

    df = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/创新高.xlsx', index_col=0)
    df['股票代码'] = df['股票代码'].apply(lambda x: str(x).zfill(6))
    df['创新高日期'] = df['创新高日期'].apply(lambda x: str(x))
    stock_info = get_stock_info()[['TICKER_SYMBOL', 'SAMPLE_DATE']].rename(columns={'TICKER_SYMBOL': '股票代码', 'SAMPLE_DATE': '入选样本日期'})
    df = df.merge(stock_info, on=['股票代码'], how='inner')
    df = df[df['创新高日期'] >= df['入选样本日期']]
    df = df.reset_index().drop(['index', '入选样本日期'], axis=1)
    # df = df[df['创新高日期'] >= '20220501']
    # df = df.sort_values(['股票代码', '创新高日期']).drop_duplicates('股票代码', keep='first')
    # df = df.sort_values(['申万一级行业', '股票代码'])
    # df = df.reset_index().drop(['index', '创新高日期', '区间内首次创新高', '区间内收盘价最高', '收盘价格'], axis=1)
    df.to_excel('D:/Git/hbshare/hbshare/fe/xwq/data/new_high/创新高_new.xlsx')