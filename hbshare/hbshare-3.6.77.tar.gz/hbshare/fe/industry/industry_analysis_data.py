# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
import pymysql
import sqlalchemy
import sys
import time
import traceback
import warnings
warnings.filterwarnings('ignore', category=pymysql.Warning)

class InsertTable:
    def __init__(self):
        self.engine = None
        self.connection = None
        self.create_connection()

    def create_connection(self):
        vaild = False
        while not vaild:
            try:
                self.engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
                                            'admin', 'mysql', '192.168.223.152', '3306', 'fe_temp_data'),
                                   connect_args={'charset': 'utf8'}, pool_recycle=360,
                                   pool_size=2, max_overflow=10, pool_timeout=360)
                self.connection = self.engine.connect()
                vaild = True
            except Exception as e:
                self.close_connection()
                print('[InsertTable] mysql connect error')
                time.sleep(5)
        return

    def close_connection(self):
        # 1) close connection
        try:
            if self.connection is not None:
                self.connection.close()
        except Exception as e:
            print('[InsertTable] close connect error')
        # 2) dispose engine
        try:
            if self.engine is not None:
                self.engine.dispose()
        except Exception as e:
            print('[InsertTable] dispose engine error')
        return

    def create_metadata(self, metadata):
        valid = False
        while not valid:
            try:
                metadata.create_all(self.engine)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] create metadata error')
            return metadata

    def insert_data(self, table, params):
        try:
            self.connection.execute(table.insert(), params)
        except Exception as e:
            conn = self.engine.connect()
            conn.execute(table.insert(), params)
            self.connection = conn
            exc_type, exc_value, exc_trackback = sys.exc_info()
            print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
            print('[InsertTable] insert data error')
        return

    def replace_data(self, table, params):
        # @compiles(Insert)
        def replace_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            s = s.replace("INSERT INTO", "REPLACE INTO")
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.connection.execute(table.insert(replace_string=""), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] replace data error')
            return

    def update_data(self, table, params):
        # @compiles(Insert)
        def append_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            if insert.kwards.get('on_duplicates_key_update'):
                fields = s[s.find("(") + 1:s.find(")")].replace(" ", "").split(",")
                generated_directive = ["{0}=VALUES({0})".format(field) for field in fields]
                return s + " ON DUPLICATES KEY UPDATE " + ",".join(generated_directive)
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.connection.execute(table.insert(on_duplicates_key_update=True), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] update data error')
            return

    def insert_industry_technology_df(self, factor_df, cols):
        table_name = 'industry_technology'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('MARKET_VALUE'),
            sqlalchemy.Column('RET'),
            sqlalchemy.Column('VOL'),
            sqlalchemy.Column('TURNOVER'),
            sqlalchemy.Column('BETA'),
            sqlalchemy.Column('ALPHA')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_daily_technology_df(self, factor_df, cols):
        table_name = 'industry_daily_technology'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('TRADE_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('VOL'),
            sqlalchemy.Column('TURNOVER'),
            sqlalchemy.Column('BETA')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_valuation_df(self, factor_df, cols):
        table_name = 'industry_valuation'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('PE_TTM'),
            sqlalchemy.Column('PB_LF'),
            sqlalchemy.Column('PEG'),
            sqlalchemy.Column('DIVIDEND_RATIO_TTM')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_daily_valuation_df(self, factor_df, cols):
        table_name = 'industry_daily_valuation'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('TRADE_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('PE_TTM'),
            sqlalchemy.Column('PB_LF'),
            sqlalchemy.Column('PEG'),
            sqlalchemy.Column('DIVIDEND_RATIO_TTM')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_fundamental_df(self, factor_df, cols):
        table_name = 'industry_fundamental'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('NET_PROFIT'),
            sqlalchemy.Column('NET_PROFIT_ACCUM'),
            sqlalchemy.Column('NET_PROFIT_TTM'),
            sqlalchemy.Column('MAIN_INCOME'),
            sqlalchemy.Column('MAIN_INCOME_ACCUM'),
            sqlalchemy.Column('MAIN_INCOME_TTM'),
            sqlalchemy.Column('ROE_TTM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM'),
            sqlalchemy.Column('EPS_TTM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM'),
            sqlalchemy.Column('NET_ASSET_PS')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_fundamental_derive_df(self, factor_df, cols):
        table_name = 'industry_fundamental_derive'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('NET_PROFIT_YOY'),
            sqlalchemy.Column('NET_PROFIT_ACCUM_YOY'),
            sqlalchemy.Column('NET_PROFIT_TTM_YOY'),
            sqlalchemy.Column('MAIN_INCOME_YOY'),
            sqlalchemy.Column('MAIN_INCOME_ACCUM_YOY'),
            sqlalchemy.Column('MAIN_INCOME_TTM_YOY'),
            sqlalchemy.Column('ROE_TTM_YOY'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY'),
            sqlalchemy.Column('EPS_TTM_YOY'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY'),
            sqlalchemy.Column('NET_ASSET_PS_YOY'),
            sqlalchemy.Column('NET_PROFIT_MOM'),
            sqlalchemy.Column('NET_PROFIT_ACCUM_MOM'),
            sqlalchemy.Column('NET_PROFIT_TTM_MOM'),
            sqlalchemy.Column('MAIN_INCOME_MOM'),
            sqlalchemy.Column('MAIN_INCOME_ACCUM_MOM'),
            sqlalchemy.Column('MAIN_INCOME_TTM_MOM'),
            sqlalchemy.Column('ROE_TTM_MOM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM'),
            sqlalchemy.Column('EPS_TTM_MOM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM'),
            sqlalchemy.Column('NET_ASSET_PS_MOM'),
            sqlalchemy.Column('ROE_TTM_YOY_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('EPS_TTM_YOY_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_YOY_ABS'),
            sqlalchemy.Column('ROE_TTM_MOM_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('EPS_TTM_MOM_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_MOM_ABS')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_consensus_df(self, factor_df, cols):
        table_name = 'industry_consensus'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('IS_EXCEED_NEW'),
            sqlalchemy.Column('EXCEED_RATIO_NEW'),
            sqlalchemy.Column('IS_EXCEED'),
            sqlalchemy.Column('EXCEED_RATIO'),
            sqlalchemy.Column('EST_NET_PROFIT_FY1'),
            sqlalchemy.Column('EST_OPER_REVENUE_FY1'),
            sqlalchemy.Column('EST_ROE_FY1'),
            sqlalchemy.Column('EST_EPS_FY1'),
            sqlalchemy.Column('EST_CFPS_FY1'),
            sqlalchemy.Column('EST_BPS_FY1'),
            sqlalchemy.Column('EST_PE_FY1'),
            sqlalchemy.Column('EST_PB_FY1'),
            sqlalchemy.Column('EST_PEG_FY1'),
            sqlalchemy.Column('EST_DPS_FY1'),
            # sqlalchemy.Column('EST_NET_PROFIT_YEAR'),
            # sqlalchemy.Column('EST_OPER_REVENUE_YEAR'),
            # sqlalchemy.Column('EST_ROE_YEAR'),
            # sqlalchemy.Column('EST_EPS_YEAR'),
            # sqlalchemy.Column('EST_CFPS_YEAR'),
            # sqlalchemy.Column('EST_BPS_YEAR'),
            # sqlalchemy.Column('EST_PE_YEAR'),
            # sqlalchemy.Column('EST_PB_YEAR'),
            # sqlalchemy.Column('EST_PEG_YEAR'),
            # sqlalchemy.Column('EST_DPS_YEAR'),
            sqlalchemy.Column('EST_NET_PROFIT_TTM'),
            sqlalchemy.Column('EST_OPER_REVENUE_TTM'),
            sqlalchemy.Column('EST_EPS_TTM'),
            sqlalchemy.Column('EST_CFPS_TTM'),
            sqlalchemy.Column('EST_PE_TTM'),
            sqlalchemy.Column('EST_PEG_TTM'),
            sqlalchemy.Column('EST_NET_PROFIT_YOY'),
            sqlalchemy.Column('EST_OPER_REVENUE_YOY'),
            sqlalchemy.Column('EST_ROE_YOY'),
            sqlalchemy.Column('EST_EPS_YOY')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_head_df(self, factor_df, cols):
        table_name = 'industry_head'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('TICKER_SYMBOL'),
            sqlalchemy.Column('SEC_SHORT_NAME'),
            sqlalchemy.Column('MARKET_VALUE'),
            sqlalchemy.Column('RET'),
            sqlalchemy.Column('VOL'),
            sqlalchemy.Column('BETA'),
            sqlalchemy.Column('PE_TTM'),
            sqlalchemy.Column('PB_LF'),
            sqlalchemy.Column('PEG'),
            sqlalchemy.Column('DIVIDEND_RATIO_TTM'),
            sqlalchemy.Column('NET_PROFIT'),
            sqlalchemy.Column('NET_PROFIT_TTM'),
            sqlalchemy.Column('MAIN_INCOME'),
            sqlalchemy.Column('MAIN_INCOME_TTM'),
            sqlalchemy.Column('ROE_TTM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM'),
            sqlalchemy.Column('EPS_TTM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM'),
            sqlalchemy.Column('NET_ASSET_PS'),
            sqlalchemy.Column('NET_PROFIT_YOY'),
            sqlalchemy.Column('NET_PROFIT_TTM_YOY'),
            sqlalchemy.Column('MAIN_INCOME_YOY'),
            sqlalchemy.Column('MAIN_INCOME_TTM_YOY'),
            sqlalchemy.Column('ROE_TTM_YOY'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY'),
            sqlalchemy.Column('EPS_TTM_YOY'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY'),
            sqlalchemy.Column('NET_ASSET_PS_YOY'),
            sqlalchemy.Column('NET_PROFIT_MOM'),
            sqlalchemy.Column('NET_PROFIT_TTM_MOM'),
            sqlalchemy.Column('MAIN_INCOME_MOM'),
            sqlalchemy.Column('MAIN_INCOME_TTM_MOM'),
            sqlalchemy.Column('ROE_TTM_MOM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM'),
            sqlalchemy.Column('EPS_TTM_MOM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM'),
            sqlalchemy.Column('NET_ASSET_PS_MOM'),
            sqlalchemy.Column('ROE_TTM_YOY_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('EPS_TTM_YOY_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_YOY_ABS'),
            sqlalchemy.Column('ROE_TTM_MOM_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('EPS_TTM_MOM_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_MOM_ABS'),
            sqlalchemy.Column('IS_EXCEED'),
            sqlalchemy.Column('EST_NET_PROFIT_FY1'),
            sqlalchemy.Column('EST_OPER_REVENUE_FY1'),
            sqlalchemy.Column('EST_ROE_FY1'),
            sqlalchemy.Column('EST_EPS_FY1'),
            sqlalchemy.Column('EST_CFPS_FY1'),
            sqlalchemy.Column('EST_BPS_FY1'),
            sqlalchemy.Column('EST_PE_FY1'),
            sqlalchemy.Column('EST_PB_FY1'),
            sqlalchemy.Column('EST_PEG_FY1'),
            sqlalchemy.Column('EST_DPS_FY1'),
            sqlalchemy.Column('EST_NET_PROFIT_TTM'),
            sqlalchemy.Column('EST_OPER_REVENUE_TTM'),
            sqlalchemy.Column('EST_EPS_TTM'),
            sqlalchemy.Column('EST_CFPS_TTM'),
            sqlalchemy.Column('EST_PE_TTM'),
            sqlalchemy.Column('EST_PEG_TTM')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

def filter_extreme_mad(ser, n=3):
    median = ser.quantile(0.5)
    new_median = ((ser - median).abs()).quantile(0.5)
    max_range = median + n * new_median
    min_range = median - n * new_median
    ser = np.clip(ser, min_range, max_range)
    return ser

def filter_extreme_3sigma(ser, n=3, times=3):
    for i in range(times):
        mean = ser.mean()
        std = ser.std()
        max_range = mean + n * std
        min_range = mean - n * std
        ser = np.clip(ser, min_range, max_range)
    return ser

def filter_extreme_percentile(ser, min=0.025, max=0.075):
    ser = ser.sort_values()
    q = ser.quantile([min, max])
    ser = np.clip(ser, q.iloc[0], q.iloc[1])
    return ser

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

def get_stock_info():
    stock_info = HBDB().read_stock_info()
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqjc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].dropna()
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info['SAMPLE_DATE'] = stock_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(365)).strftime('%Y%m%d'))
    return stock_info

class IndustryTechnology:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.industry_daily_k = HBDB().read_index_daily_k_given_date_and_indexs(self.data_start_date, self.industry_info['INDUSTRY_ID'].unique().tolist())
        self.industry_daily_k = self.industry_daily_k.rename(columns={'zqdm': 'INDUSTRY_ID', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX', 'cjjs': 'TURNOVER_VALUE', 'ltsz': 'NEG_MARKET_VALUE'})
        self.industry_daily_k['TRADE_DATE'] = self.industry_daily_k['TRADE_DATE'].astype(str)
        self.industry_daily_k = self.industry_daily_k.sort_values('TRADE_DATE')
        self.industry_daily_k['TURNOVER_RATE'] = self.industry_daily_k['TURNOVER_VALUE'] / (self.industry_daily_k['NEG_MARKET_VALUE'] * 10000.0)
        self.industry_turnover = self.industry_daily_k.pivot(index='TRADE_DATE', columns='INDUSTRY_ID', values='TURNOVER_RATE').sort_index()
        self.industry_turnover.columns = [self.industry_id_name_dic[col] for col in self.industry_turnover]
        self.industry_turnover = self.industry_turnover.sort_index()
        self.industry_daily_k = self.industry_daily_k.pivot(index='TRADE_DATE', columns='INDUSTRY_ID', values='CLOSE_INDEX').sort_index()
        self.industry_daily_k.columns = [self.industry_id_name_dic[col] for col in self.industry_daily_k]
        self.industry_daily_k = self.industry_daily_k.sort_index()

        self.benchmark_daily_k = HBDB().read_index_daily_k_given_date_and_indexs(self.data_start_date, ['881001'])
        self.benchmark_daily_k = self.benchmark_daily_k.rename(columns={'zqmc': 'BENCHMARK_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        self.benchmark_daily_k['TRADE_DATE'] = self.benchmark_daily_k['TRADE_DATE'].astype(str)
        self.benchmark_daily_k = self.benchmark_daily_k.sort_values('TRADE_DATE')
        self.benchmark_daily_k = self.benchmark_daily_k.pivot(index='TRADE_DATE', columns='BENCHMARK_NAME', values='CLOSE_INDEX').sort_index()
        self.benchmark_daily_k = self.benchmark_daily_k.sort_index()

        self.industry_symbol = get_industry_symbol()
        self.industry_symbol = self.industry_symbol[self.industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_symbol = self.industry_symbol[self.industry_symbol['IS_NEW'] == 1]
        self.industry_symbol = self.industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.drop('INDUSTRY_NAME', axis=1).merge(self.industry_symbol, on=['INDUSTRY_ID'], how='left')
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        stock_market_value_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_market_value.hdf'
        if os.path.isfile(stock_market_value_path):
            existed_stock_market_value = pd.read_hdf(stock_market_value_path, key='table')
            max_date = max(existed_stock_market_value['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_market_value = pd.DataFrame()
            start_date = '20150101'
        report_trade_df = self.report_trade_df[(self.report_trade_df['TRADE_DATE'] > start_date) & (self.report_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_market_value_list = []
        for date in report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            stock_market_value_date = stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            star_stock_market_value_date = star_stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(star_stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            stock_market_value_date = pd.concat([stock_market_value_date, star_stock_market_value_date])
            stock_market_value_list.append(stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat([existed_stock_market_value] + stock_market_value_list, ignore_index=True)
        self.stock_market_value = self.stock_market_value.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_market_value = self.stock_market_value.reset_index().drop('index', axis=1)
        self.stock_market_value.to_hdf(stock_market_value_path, key='table', mode='w')
        self.stock_market_value = pd.read_hdf(stock_market_value_path, key='table')

    def get_ret(self):
        industry_daily_k = self.industry_daily_k[self.industry_daily_k.index.isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        industry_quarter_ret = (industry_daily_k / industry_daily_k.shift() - 1).dropna(how='all')
        industry_quarter_ret.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_ret.index)
        industry_quarter_ret = industry_quarter_ret[(industry_quarter_ret.index > self.start_date) & (industry_quarter_ret.index <= self.end_date)]
        return industry_quarter_ret

    def get_vol(self):
        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        industry_daily_ret['REPORT_DATE'] = industry_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_vol = industry_daily_ret[['REPORT_DATE', 'INDUSTRY_NAME', 'DAILY_RET']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).std(ddof=1).reset_index().rename(columns={'DAILY_RET': 'VOL'})
        industry_quarter_vol = industry_quarter_vol.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='VOL').sort_index()
        industry_quarter_vol = industry_quarter_vol[(industry_quarter_vol.index > self.start_date) & (industry_quarter_vol.index <= self.end_date)]
        return industry_quarter_vol

    def get_turnover(self):
        industry_daily_turnover = self.industry_turnover.unstack().reset_index()
        industry_daily_turnover.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'TURNOVER_RATE']
        industry_daily_turnover['REPORT_DATE'] = industry_daily_turnover['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_turnover = industry_daily_turnover[['REPORT_DATE', 'INDUSTRY_NAME', 'TURNOVER_RATE']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).mean().reset_index().rename(columns={'TURNOVER_RATE': 'TURNOVER'})
        industry_quarter_turnover = industry_quarter_turnover.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='TURNOVER').sort_index()
        industry_quarter_turnover = industry_quarter_turnover[(industry_quarter_turnover.index > self.start_date) & (industry_quarter_turnover.index <= self.end_date)]
        return industry_quarter_turnover

    def get_beta(self):
        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        benchmark_daily_ret = (self.benchmark_daily_k / self.benchmark_daily_k.shift() - 1).dropna(how='all')
        benchmark_daily_ret = benchmark_daily_ret.unstack().reset_index()
        benchmark_daily_ret.columns = ['BENCHMARK_NAME', 'TRADE_DATE', 'BENCHMARK_DAILY_RET']
        industry_daily_ret = industry_daily_ret.merge(benchmark_daily_ret, on=['TRADE_DATE'], how='inner')
        industry_daily_ret['REPORT_DATE'] = industry_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_beta = industry_daily_ret[['REPORT_DATE', 'INDUSTRY_NAME', 'DAILY_RET', 'BENCHMARK_DAILY_RET']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).apply(lambda x: np.cov(x['DAILY_RET'], x['BENCHMARK_DAILY_RET'])[0, 1] / np.var(x['BENCHMARK_DAILY_RET'])).reset_index().rename(columns={0: 'BETA'})
        industry_quarter_beta = industry_quarter_beta.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='BETA').sort_index()
        industry_quarter_beta = industry_quarter_beta[(industry_quarter_beta.index > self.start_date) & (industry_quarter_beta.index <= self.end_date)]
        return industry_quarter_beta

    def get_alpha(self):
        industry_quarter_ret = self.get_ret()
        benchmark_daily_k = self.benchmark_daily_k[self.benchmark_daily_k.index.isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        benchmark_quarter_ret = (benchmark_daily_k / benchmark_daily_k.shift() - 1).dropna(how='all')
        benchmark_quarter_ret.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', benchmark_quarter_ret.index)
        benchmark_quarter_ret = benchmark_quarter_ret[(benchmark_quarter_ret.index > self.start_date) & (benchmark_quarter_ret.index <= self.end_date)]
        industry_quarter_beta = self.get_beta()
        industry_quarter_alpha = (industry_quarter_ret - 0.03 / 4.0) - np.multiply(industry_quarter_beta, benchmark_quarter_ret - 0.03 / 4.0)
        industry_quarter_alpha = industry_quarter_alpha[(industry_quarter_alpha.index > self.start_date) & (industry_quarter_alpha.index <= self.end_date)]
        return industry_quarter_alpha

    def get_market_value(self):
        stock_market_value = self.stock_market_value[self.stock_market_value['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_market_value = stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_market_value = stock_market_value.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE'])
        industry_quarter_market_value = stock_market_value[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_market_value = industry_quarter_market_value.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='MARKET_VALUE').sort_index()
        industry_quarter_market_value.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_market_value.index)
        industry_quarter_market_value = industry_quarter_market_value[(industry_quarter_market_value.index > self.start_date) & (industry_quarter_market_value.index <= self.end_date)]
        return industry_quarter_market_value

    def get_daily_vol(self):
        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        industry_daily_vol = industry_daily_ret.sort_values(['INDUSTRY_NAME', 'TRADE_DATE']).reset_index().drop('index', axis=1)
        industry_daily_vol['VOL'] = industry_daily_vol[['INDUSTRY_NAME', 'DAILY_RET']].groupby('INDUSTRY_NAME').rolling(60).std(ddof=1).reset_index()['DAILY_RET']
        industry_daily_vol = industry_daily_vol.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='VOL').sort_index()
        industry_daily_vol = industry_daily_vol[(industry_daily_vol.index > self.start_date) & (industry_daily_vol.index <= self.end_date)]
        return industry_daily_vol

    def get_daily_turnover(self):
        industry_daily_turnover = self.industry_turnover.unstack().reset_index()
        industry_daily_turnover.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'TURNOVER_RATE']
        industry_daily_turnover = industry_daily_turnover.sort_values(['INDUSTRY_NAME', 'TRADE_DATE']).reset_index().drop('index', axis=1)
        industry_daily_turnover['TURNOVER'] = industry_daily_turnover[['INDUSTRY_NAME', 'TURNOVER_RATE']].groupby('INDUSTRY_NAME').rolling(60).mean().reset_index()['TURNOVER_RATE']
        industry_daily_turnover = industry_daily_turnover.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='TURNOVER').sort_index()
        industry_daily_turnover = industry_daily_turnover[(industry_daily_turnover.index > self.start_date) & (industry_daily_turnover.index <= self.end_date)]
        return industry_daily_turnover

    def get_daily_beta(self):
        def _beta_definition(idxs, daily_df):
            part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
            beta = np.cov(part_df['DAILY_RET'], part_df['BENCHMARK_DAILY_RET'])[0, 1] / np.var(part_df['BENCHMARK_DAILY_RET'])
            return beta

        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        benchmark_daily_ret = (self.benchmark_daily_k / self.benchmark_daily_k.shift() - 1).dropna(how='all')
        benchmark_daily_ret = benchmark_daily_ret.unstack().reset_index()
        benchmark_daily_ret.columns = ['BENCHMARK_NAME', 'TRADE_DATE', 'BENCHMARK_DAILY_RET']
        industry_daily_ret = industry_daily_ret.merge(benchmark_daily_ret, on=['TRADE_DATE'], how='inner')
        industry_daily_ret = industry_daily_ret.sort_values(['INDUSTRY_NAME', 'TRADE_DATE']).reset_index().drop('index', axis=1)
        ind_df_list = []
        for ind in industry_daily_ret['INDUSTRY_NAME'].unique().tolist():
            ind_df = industry_daily_ret[industry_daily_ret['INDUSTRY_NAME'] == ind].sort_values('TRADE_DATE')
            ind_df['IDX'] = range(len(ind_df))
            ind_df['BETA'] = ind_df['IDX'].rolling(60).apply(lambda x: _beta_definition(x, ind_df))
            ind_df_list.append(ind_df)
        industry_daily_beta = pd.concat(ind_df_list)
        industry_daily_beta = industry_daily_beta.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='BETA').sort_index()
        industry_daily_beta = industry_daily_beta[(industry_daily_beta.index > self.start_date) & (industry_daily_beta.index <= self.end_date)]
        return industry_daily_beta

    def get_all(self):
        ret = self.get_ret()
        ret = ret.unstack().reset_index()
        ret.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'RET']
        vol = self.get_vol()
        vol = vol.unstack().reset_index()
        vol.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'VOL']
        turnover = self.get_turnover()
        turnover = turnover.unstack().reset_index()
        turnover.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'TURNOVER']
        beta = self.get_beta()
        beta = beta.unstack().reset_index()
        beta.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'BETA']
        alpha = self.get_alpha()
        alpha = alpha.unstack().reset_index()
        alpha.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'ALPHA']
        market_value = self.get_market_value()
        market_value = market_value.unstack().reset_index()
        market_value.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MARKET_VALUE']
        industry_technology = ret.merge(vol, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(turnover, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(beta, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(alpha, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(market_value, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_technology['INDUSTRY_ID'] = industry_technology['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_technology['INDUSTRY_TYPE'] = self.sw_type
        industry_technology = industry_technology[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'MARKET_VALUE', 'RET', 'VOL', 'TURNOVER', 'BETA', 'ALPHA']]
        industry_technology_columns = industry_technology.columns
        industry_technology[industry_technology_columns[4:]] = industry_technology[industry_technology_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_technology_df(industry_technology, list(industry_technology.columns))

        daily_vol = self.get_daily_vol()
        daily_vol = daily_vol.unstack().reset_index()
        daily_vol.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'VOL']
        daily_turnover = self.get_daily_turnover()
        daily_turnover = daily_turnover.unstack().reset_index()
        daily_turnover.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'TURNOVER']
        daily_beta = self.get_daily_beta()
        daily_beta = daily_beta.unstack().reset_index()
        daily_beta.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'BETA']

        industry_daily_technology = daily_vol.merge(daily_turnover, on=['INDUSTRY_NAME', 'TRADE_DATE'], how='outer') \
                                             .merge(daily_beta, on=['INDUSTRY_NAME', 'TRADE_DATE'], how='outer')
        industry_daily_technology['INDUSTRY_ID'] = industry_daily_technology['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_daily_technology['INDUSTRY_TYPE'] = self.sw_type
        industry_daily_technology = industry_daily_technology[['TRADE_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'VOL', 'TURNOVER', 'BETA']]
        industry_daily_technology_columns = industry_daily_technology.columns
        industry_daily_technology[industry_daily_technology_columns[4:]] = industry_daily_technology[industry_daily_technology_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_daily_technology_df(industry_daily_technology, list(industry_daily_technology.columns))

class IndustryValuation:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.industry_symbol = get_industry_symbol()
        self.industry_symbol = self.industry_symbol[self.industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_symbol = self.industry_symbol[self.industry_symbol['IS_NEW'] == 1]
        self.industry_symbol = self.industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.drop('INDUSTRY_NAME', axis=1).merge(self.industry_symbol, on=['INDUSTRY_ID'], how='left')
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        self.stock_info = get_stock_info()

        stock_valuation_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_valuation.hdf'
        if os.path.isfile(stock_valuation_path):
            existed_stock_valuation = pd.read_hdf(stock_valuation_path, key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = '20150101'
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_valuation_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            stock_valuation_date = stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']] if len(stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM'])
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            star_stock_valuation_date = star_stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']] if len(star_stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM'])
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            stock_valuation_list.append(stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat([existed_stock_valuation] + stock_valuation_list, ignore_index=True)
        self.stock_valuation = self.stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_valuation = self.stock_valuation.reset_index().drop('index', axis=1)
        self.stock_valuation.to_hdf(stock_valuation_path, key='table', mode='w')
        self.stock_valuation = pd.read_hdf(stock_valuation_path, key='table')

    def get_industry_valuation_index_data(self, index_name):
        stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        stock_valuation = stock_valuation.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation[stock_valuation['TRADE_DATE'] >= stock_valuation['SAMPLE_DATE']]
        stock_valuation = stock_valuation.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        stock_valuation[index_name] = filter_extreme_mad(stock_valuation[index_name])
        stock_valuation = stock_valuation[stock_valuation['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        industry_market_value = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_valuation = stock_valuation.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_valuation['WEIGHT_' + index_name] = stock_valuation[index_name] * stock_valuation['MARKET_VALUE'] / stock_valuation['TOTAL_MARKET_VALUE']
        industry_quarter_valuation = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_valuation = industry_quarter_valuation.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_valuation.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_valuation.index)
        industry_quarter_valuation = industry_quarter_valuation[(industry_quarter_valuation.index > self.start_date) & (industry_quarter_valuation.index <= self.end_date)]
        return industry_quarter_valuation

    def get_industry_daily_valuation_index_data(self, index_name):
        stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        stock_valuation = stock_valuation.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation[stock_valuation['TRADE_DATE'] >= stock_valuation['SAMPLE_DATE']]
        stock_valuation = stock_valuation.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        stock_valuation[index_name] = filter_extreme_mad(stock_valuation[index_name])
        industry_market_value = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_valuation = stock_valuation.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_valuation['WEIGHT_' + index_name] = stock_valuation[index_name] * stock_valuation['MARKET_VALUE'] / stock_valuation['TOTAL_MARKET_VALUE']
        industry_valuation = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_valuation = industry_valuation.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_valuation = industry_valuation[(industry_valuation.index > self.start_date) & (industry_valuation.index <= self.end_date)]
        return industry_valuation

    def get_all(self):
        pe_ttm = self.get_industry_valuation_index_data('PE_TTM')
        pe_ttm = pe_ttm.unstack().reset_index()
        pe_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PE_TTM']
        pb_lf = self.get_industry_valuation_index_data('PB_LF')
        pb_lf = pb_lf.unstack().reset_index()
        pb_lf.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PB_LF']
        peg = self.get_industry_valuation_index_data('PEG')
        peg = peg.unstack().reset_index()
        peg.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PEG']
        dividend_ratio_ttm = self.get_industry_valuation_index_data('DIVIDEND_RATIO_TTM')
        dividend_ratio_ttm = dividend_ratio_ttm.unstack().reset_index()
        dividend_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'DIVIDEND_RATIO_TTM']
        industry_valuation = pe_ttm.merge(pb_lf, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                   .merge(peg, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                   .merge(dividend_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_valuation['INDUSTRY_ID'] = industry_valuation['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_valuation['INDUSTRY_TYPE'] = self.sw_type
        industry_valuation = industry_valuation[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]
        industry_valuation_columns = industry_valuation.columns
        industry_valuation[industry_valuation_columns[4:]] = industry_valuation[industry_valuation_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_valuation_df(industry_valuation, list(industry_valuation.columns))

        pe_ttm = self.get_industry_daily_valuation_index_data('PE_TTM')
        pe_ttm = pe_ttm.unstack().reset_index()
        pe_ttm.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'PE_TTM']
        pb_lf = self.get_industry_daily_valuation_index_data('PB_LF')
        pb_lf = pb_lf.unstack().reset_index()
        pb_lf.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'PB_LF']
        peg = self.get_industry_daily_valuation_index_data('PEG')
        peg = peg.unstack().reset_index()
        peg.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'PEG']
        dividend_ratio_ttm = self.get_industry_daily_valuation_index_data('DIVIDEND_RATIO_TTM')
        dividend_ratio_ttm = dividend_ratio_ttm.unstack().reset_index()
        dividend_ratio_ttm.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DIVIDEND_RATIO_TTM']
        industry_daily_valuation = pe_ttm.merge(pb_lf, on=['INDUSTRY_NAME', 'TRADE_DATE'], how='outer') \
                                         .merge(peg, on=['INDUSTRY_NAME', 'TRADE_DATE'], how='outer') \
                                         .merge(dividend_ratio_ttm, on=['INDUSTRY_NAME', 'TRADE_DATE'], how='outer')
        industry_daily_valuation['INDUSTRY_ID'] = industry_daily_valuation['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_daily_valuation['INDUSTRY_TYPE'] = self.sw_type
        industry_daily_valuation = industry_daily_valuation[['TRADE_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]
        industry_daily_valuation_columns = industry_daily_valuation.columns
        industry_daily_valuation[industry_daily_valuation_columns[4:]] = industry_daily_valuation[industry_daily_valuation_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_daily_valuation_df(industry_daily_valuation, list(industry_daily_valuation.columns))

class IndustryFundamental:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.industry_symbol = get_industry_symbol()
        self.industry_symbol = self.industry_symbol[self.industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_symbol = self.industry_symbol[self.industry_symbol['IS_NEW'] == 1]
        self.industry_symbol = self.industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.drop('INDUSTRY_NAME', axis=1).merge(self.industry_symbol, on=['INDUSTRY_ID'], how='left')
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        self.stock_info = get_stock_info()

        stock_finance_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_finance.hdf'
        if os.path.isfile(stock_finance_path):
            existed_stock_finance = pd.read_hdf(stock_finance_path, key='table')
            max_date = max(existed_stock_finance['END_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_finance = pd.DataFrame()
            start_date = '20150101'
        report_df = self.report_df[(self.report_df['REPORT_DATE'] > start_date) & (self.report_df['REPORT_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_finance_list = []
        for date in report_df['REPORT_DATE'].unique().tolist():
            stock_finance_date = HBDB().read_stock_finance_given_date(date)
            stock_finance_date = stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
            star_stock_finance_date = HBDB().read_star_stock_finance_given_date(date)
            star_stock_finance_date = star_stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(star_stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
            stock_finance_date = pd.concat([stock_finance_date, star_stock_finance_date])
            stock_finance_list.append(stock_finance_date)
            print(date)
        self.stock_finance = pd.concat([existed_stock_finance] + stock_finance_list, ignore_index=True)
        self.stock_finance = self.stock_finance.sort_values(['END_DATE', 'TICKER_SYMBOL', 'PUBLISH_DATE'])
        self.stock_finance = self.stock_finance.reset_index().drop('index', axis=1)
        self.stock_finance.to_hdf(stock_finance_path, key='table', mode='w')
        self.stock_finance = pd.read_hdf(stock_finance_path, key='table')

        stock_market_value_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_market_value.hdf'
        if os.path.isfile(stock_market_value_path):
            existed_stock_market_value = pd.read_hdf(stock_market_value_path, key='table')
            max_date = max(existed_stock_market_value['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_market_value = pd.DataFrame()
            start_date = '20150101'
        report_trade_df = self.report_trade_df[(self.report_trade_df['TRADE_DATE'] > start_date) & (self.report_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_market_value_list = []
        for date in report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            stock_market_value_date = stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            star_stock_market_value_date = star_stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(star_stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            stock_market_value_date = pd.concat([stock_market_value_date, star_stock_market_value_date])
            stock_market_value_list.append(stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat([existed_stock_market_value] + stock_market_value_list, ignore_index=True)
        self.stock_market_value = self.stock_market_value.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_market_value = self.stock_market_value.reset_index().drop('index', axis=1)
        self.stock_market_value.to_hdf(stock_market_value_path, key='table', mode='w')
        self.stock_market_value = pd.read_hdf(stock_market_value_path, key='table')

        stock_daily_k_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_daily_k.hdf'
        if os.path.isfile(stock_daily_k_path):
            existed_stock_daily_k = pd.read_hdf(stock_daily_k_path, key='table')
            max_date = max(existed_stock_daily_k['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_daily_k = pd.DataFrame()
            start_date = '20150101'
        report_trade_df = self.report_trade_df[(self.report_trade_df['TRADE_DATE'] > start_date) & (self.report_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_daily_k_list = []
        for date in report_trade_df['TRADE_DATE'].unique().tolist():
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

    def get_net_profit(self):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        accum_net_profit = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='NET_PROFIT')
        accum_net_profit = accum_net_profit.sort_index()
        net_profit_Q1 = accum_net_profit.loc[accum_net_profit.index.str.slice(4, 6) == '03']
        net_profit = accum_net_profit - accum_net_profit.shift()
        net_profit = net_profit.loc[net_profit.index.str.slice(4, 6) != '03']
        net_profit = pd.concat([net_profit_Q1, net_profit])
        net_profit = net_profit.sort_index()
        net_profit_ttm = net_profit.rolling(window=4, min_periods=1).sum()
        net_profit_ttm = net_profit_ttm.sort_index()
        accum_net_profit = accum_net_profit.unstack().reset_index()
        accum_net_profit.columns = ['TICKER_SYMBOL', 'END_DATE', 'ACCUM_NET_PROFIT']
        accum_net_profit = accum_net_profit.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        accum_net_profit = accum_net_profit.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'ACCUM_NET_PROFIT'])
        industry_quarter_accum_net_profit = accum_net_profit[['END_DATE', 'INDUSTRY_NAME', 'ACCUM_NET_PROFIT']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_accum_net_profit = industry_quarter_accum_net_profit.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='ACCUM_NET_PROFIT').sort_index()
        industry_quarter_accum_net_profit = industry_quarter_accum_net_profit[(industry_quarter_accum_net_profit.index > self.start_date) & (industry_quarter_accum_net_profit.index <= self.end_date)]
        net_profit = net_profit.unstack().reset_index()
        net_profit.columns = ['TICKER_SYMBOL', 'END_DATE', 'NET_PROFIT']
        net_profit = net_profit.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        net_profit = net_profit.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'NET_PROFIT'])
        industry_quarter_net_profit = net_profit[['END_DATE', 'INDUSTRY_NAME', 'NET_PROFIT']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_net_profit = industry_quarter_net_profit.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='NET_PROFIT').sort_index()
        industry_quarter_net_profit = industry_quarter_net_profit[(industry_quarter_net_profit.index > self.start_date) & (industry_quarter_net_profit.index <= self.end_date)]
        net_profit_ttm = net_profit_ttm.unstack().reset_index()
        net_profit_ttm.columns = ['TICKER_SYMBOL', 'END_DATE', 'NET_PROFIT_TTM']
        net_profit_ttm = net_profit_ttm.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        net_profit_ttm = net_profit_ttm.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'NET_PROFIT_TTM'])
        industry_quarter_net_profit_ttm = net_profit_ttm[['END_DATE', 'INDUSTRY_NAME', 'NET_PROFIT_TTM']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_net_profit_ttm = industry_quarter_net_profit_ttm.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='NET_PROFIT_TTM').sort_index()
        industry_quarter_net_profit_ttm = industry_quarter_net_profit_ttm[(industry_quarter_net_profit_ttm.index > self.start_date) & (industry_quarter_net_profit_ttm.index <= self.end_date)]
        return industry_quarter_net_profit, industry_quarter_accum_net_profit, industry_quarter_net_profit_ttm

    def get_main_income(self):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='inner')
        stock_finance = stock_finance.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance['MAIN_INCOME'] = stock_finance['MAIN_INCOME_PS'] * (stock_finance['MARKET_VALUE'] / stock_finance['CLOSE_PRICE'])
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        accum_main_income = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='MAIN_INCOME')
        accum_main_income = accum_main_income.sort_index()
        main_income_Q1 = accum_main_income.loc[accum_main_income.index.str.slice(4, 6) == '03']
        main_income = accum_main_income - accum_main_income.shift()
        main_income = main_income.loc[main_income.index.str.slice(4, 6) != '03']
        main_income = pd.concat([main_income_Q1, main_income])
        main_income = main_income.sort_index()
        main_income_ttm = main_income.rolling(window=4, min_periods=1).sum()
        main_income_ttm = main_income_ttm.sort_index()
        accum_main_income = accum_main_income.unstack().reset_index()
        accum_main_income.columns = ['TICKER_SYMBOL', 'END_DATE', 'ACCUM_MAIN_INCOME']
        accum_main_income = accum_main_income.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        accum_main_income = accum_main_income.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'ACCUM_MAIN_INCOME'])
        industry_quarter_accum_main_income = accum_main_income[['END_DATE', 'INDUSTRY_NAME', 'ACCUM_MAIN_INCOME']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_accum_main_income = industry_quarter_accum_main_income.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='ACCUM_MAIN_INCOME').sort_index()
        industry_quarter_accum_main_income = industry_quarter_accum_main_income[(industry_quarter_accum_main_income.index > self.start_date) & (industry_quarter_accum_main_income.index <= self.end_date)]
        main_income = main_income.unstack().reset_index()
        main_income.columns = ['TICKER_SYMBOL', 'END_DATE', 'MAIN_INCOME']
        main_income = main_income.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        main_income = main_income.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MAIN_INCOME'])
        industry_quarter_main_income = main_income[['END_DATE', 'INDUSTRY_NAME', 'MAIN_INCOME']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_main_income = industry_quarter_main_income.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='MAIN_INCOME').sort_index()
        industry_quarter_main_income = industry_quarter_main_income[(industry_quarter_main_income.index > self.start_date) & (industry_quarter_main_income.index <= self.end_date)]
        main_income_ttm = main_income_ttm.unstack().reset_index()
        main_income_ttm.columns = ['TICKER_SYMBOL', 'END_DATE', 'MAIN_INCOME_TTM']
        main_income_ttm = main_income_ttm.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        main_income_ttm = main_income_ttm.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MAIN_INCOME_TTM'])
        industry_quarter_main_income_ttm = main_income_ttm[['END_DATE', 'INDUSTRY_NAME', 'MAIN_INCOME_TTM']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_main_income_ttm = industry_quarter_main_income_ttm.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='MAIN_INCOME_TTM').sort_index()
        industry_quarter_main_income_ttm = industry_quarter_main_income_ttm[(industry_quarter_main_income_ttm.index > self.start_date) & (industry_quarter_main_income_ttm.index <= self.end_date)]
        return industry_quarter_main_income, industry_quarter_accum_main_income, industry_quarter_main_income_ttm

    def get_industry_fundamental_index_data(self, index_name):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='inner')
        stock_finance = stock_finance.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        stock_finance = stock_finance.dropna(subset=['END_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        stock_finance[index_name] = filter_extreme_mad(stock_finance[index_name])
        industry_market_value = stock_finance[['END_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_finance = stock_finance.merge(industry_market_value, on=['END_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_finance['WEIGHT_' + index_name] = stock_finance[index_name] * stock_finance['MARKET_VALUE'] / stock_finance['TOTAL_MARKET_VALUE']
        industry_quarter_fundamental = stock_finance[['END_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_fundamental = industry_quarter_fundamental.pivot(index='END_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_fundamental = industry_quarter_fundamental[(industry_quarter_fundamental.index > self.start_date) & (industry_quarter_fundamental.index <= self.end_date)]
        return industry_quarter_fundamental

    def get_all(self):
        net_profit, net_profit_accum, net_profit_ttm = self.get_net_profit()
        net_profit = net_profit.unstack().reset_index()
        net_profit.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT']
        net_profit_accum = net_profit_accum.unstack().reset_index()
        net_profit_accum.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT_ACCUM']
        net_profit_ttm = net_profit_ttm.unstack().reset_index()
        net_profit_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT_TTM']
        main_income, main_income_accum, main_income_ttm = self.get_main_income()
        main_income = main_income.unstack().reset_index()
        main_income.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MAIN_INCOME']
        main_income_accum = main_income_accum.unstack().reset_index()
        main_income_accum.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MAIN_INCOME_ACCUM']
        main_income_ttm = main_income_ttm.unstack().reset_index()
        main_income_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MAIN_INCOME_TTM']
        roe_ttm = self.get_industry_fundamental_index_data('ROE_TTM')
        roe_ttm = roe_ttm.unstack().reset_index()
        roe_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'ROE_TTM']
        gross_income_ratio_ttm = self.get_industry_fundamental_index_data('GROSS_INCOME_RATIO_TTM')
        gross_income_ratio_ttm = gross_income_ratio_ttm.unstack().reset_index()
        gross_income_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'GROSS_INCOME_RATIO_TTM']
        net_profit_ratio_ttm = self.get_industry_fundamental_index_data('NET_PROFIT_RATIO_TTM')
        net_profit_ratio_ttm = net_profit_ratio_ttm.unstack().reset_index()
        net_profit_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT_RATIO_TTM']
        eps_ttm = self.get_industry_fundamental_index_data('EPS_TTM')
        eps_ttm = eps_ttm.unstack().reset_index()
        eps_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'EPS_TTM']
        oper_cash_flow_ps_ttm = self.get_industry_fundamental_index_data('OPER_CASH_FLOW_PS_TTM')
        oper_cash_flow_ps_ttm = oper_cash_flow_ps_ttm.unstack().reset_index()
        oper_cash_flow_ps_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'OPER_CASH_FLOW_PS_TTM']
        net_asset_ps = self.get_industry_fundamental_index_data('NET_ASSET_PS')
        net_asset_ps = net_asset_ps.unstack().reset_index()
        net_asset_ps.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_ASSET_PS']
        industry_fundamental = net_profit.merge(net_profit_accum, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(net_profit_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(main_income, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(main_income_accum, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(main_income_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(roe_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(gross_income_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(net_profit_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(eps_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(oper_cash_flow_ps_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(net_asset_ps, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_fundamental['INDUSTRY_ID'] = industry_fundamental['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_fundamental['INDUSTRY_TYPE'] = self.sw_type
        industry_fundamental = industry_fundamental[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'NET_PROFIT', 'NET_PROFIT_ACCUM', 'NET_PROFIT_TTM', 'MAIN_INCOME', 'MAIN_INCOME_ACCUM', 'MAIN_INCOME_TTM', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']]
        industry_fundamental_columns = industry_fundamental.columns
        industry_fundamental[industry_fundamental_columns[4:]] = industry_fundamental[industry_fundamental_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_fundamental_df(industry_fundamental, list(industry_fundamental.columns))

class IndustryFundamentalDerive:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.index_data = FEDB().read_industry_fundamental(self.sw_type)

    def get_yoy(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        index_data = index_data.replace(0.0, np.nan)
        yoy_ratio = (index_data - index_data.shift(4)) / abs(index_data.shift(4))
        return yoy_ratio.dropna(how='all')

    def get_mom(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        index_data = index_data.replace(0.0, np.nan)
        mom_ratio = (index_data - index_data.shift()) / abs(index_data.shift())
        return mom_ratio.dropna(how='all')

    def get_yoy_abs(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        index_data = index_data.replace(0.0, np.nan)
        yoy_abs = (index_data - index_data.shift(4))
        return yoy_abs.dropna(how='all')

    def get_mom_abs(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        index_data = index_data.replace(0.0, np.nan)
        mom_abs = (index_data - index_data.shift())
        return mom_abs.dropna(how='all')

    def get_all(self):
        index_list = list(self.index_data.columns)
        index_list = [index for index in index_list if index not in ['ID', 'REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'INSERT_TIME', 'UPDATE_TIME']]
        yoy_list, mom_list = [], []
        for index in index_list:
            yoy = self.get_yoy(index)
            yoy = pd.DataFrame(yoy.unstack())
            yoy.columns = ['{0}_YOY'.format(index)]
            yoy_list.append(yoy)
            mom = self.get_mom(index)
            mom = pd.DataFrame(mom.unstack())
            mom.columns = ['{0}_MOM'.format(index)]
            mom_list.append(mom)
        yoy_abs_list, mom_abs_list = [], []
        for index in index_list[6:]:
            yoy_abs = self.get_yoy_abs(index)
            yoy_abs = pd.DataFrame(yoy_abs.unstack())
            yoy_abs.columns = ['{0}_YOY_ABS'.format(index)]
            yoy_abs_list.append(yoy_abs)
            mom_abs = self.get_mom_abs(index)
            mom_abs = pd.DataFrame(mom_abs.unstack())
            mom_abs.columns = ['{0}_MOM_ABS'.format(index)]
            mom_abs_list.append(mom_abs)
        industry_fundamental_derive = pd.concat(yoy_list + mom_list + yoy_abs_list + mom_abs_list, axis=1)
        industry_fundamental_derive_columns = list(industry_fundamental_derive.columns)
        industry_fundamental_derive = industry_fundamental_derive.reset_index()
        industry_fundamental_derive = industry_fundamental_derive[(industry_fundamental_derive['REPORT_DATE'] > self.start_date) & (industry_fundamental_derive['REPORT_DATE'] <= self.end_date)]
        industry_fundamental_derive['INDUSTRY_ID'] = industry_fundamental_derive['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_fundamental_derive['INDUSTRY_TYPE'] = self.sw_type
        industry_fundamental_derive = industry_fundamental_derive[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE'] + industry_fundamental_derive_columns]
        industry_fundamental_derive_columns = industry_fundamental_derive.columns
        industry_fundamental_derive[industry_fundamental_derive_columns[4:]] = industry_fundamental_derive[industry_fundamental_derive_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_fundamental_derive_df(industry_fundamental_derive, list(industry_fundamental_derive.columns))

class IndustryConsensus:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.industry_symbol = get_industry_symbol()
        self.industry_symbol = self.industry_symbol[self.industry_symbol['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_symbol = self.industry_symbol[self.industry_symbol['IS_NEW'] == 1]
        self.industry_symbol = self.industry_symbol[['INDUSTRY_ID', 'INDUSTRY_NAME']]

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry.drop('INDUSTRY_NAME', axis=1).merge(self.industry_symbol, on=['INDUSTRY_ID'], how='left')
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        stock_market_value_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_market_value.hdf'
        if os.path.isfile(stock_market_value_path):
            existed_stock_market_value = pd.read_hdf(stock_market_value_path, key='table')
            max_date = max(existed_stock_market_value['TRADE_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_market_value = pd.DataFrame()
            start_date = '20150101'
        report_trade_df = self.report_trade_df[(self.report_trade_df['TRADE_DATE'] > start_date) & (self.report_trade_df['TRADE_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_market_value_list = []
        for date in report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            stock_market_value_date = stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            star_stock_market_value_date = star_stock_market_value_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']] if len(star_stock_market_value_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE'])
            stock_market_value_date = pd.concat([stock_market_value_date, star_stock_market_value_date])
            stock_market_value_list.append(stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat([existed_stock_market_value] + stock_market_value_list, ignore_index=True)
        self.stock_market_value = self.stock_market_value.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_market_value = self.stock_market_value.reset_index().drop('index', axis=1)
        self.stock_market_value.to_hdf(stock_market_value_path, key='table', mode='w')
        self.stock_market_value = pd.read_hdf(stock_market_value_path, key='table')

        stock_finance_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_finance.hdf'
        if os.path.isfile(stock_finance_path):
            existed_stock_finance = pd.read_hdf(stock_finance_path, key='table')
            max_date = max(existed_stock_finance['END_DATE'])
            start_date = max(str(max_date), '20150101')
        else:
            existed_stock_finance = pd.DataFrame()
            start_date = '20150101'
        report_df = self.report_df[(self.report_df['REPORT_DATE'] > start_date) & (self.report_df['REPORT_DATE'] < datetime.today().strftime('%Y%m%d'))]
        stock_finance_list = []
        for date in report_df['REPORT_DATE'].unique().tolist():
            stock_finance_date = HBDB().read_stock_finance_given_date(date)
            stock_finance_date = stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
            star_stock_finance_date = HBDB().read_star_stock_finance_given_date(date)
            star_stock_finance_date = star_stock_finance_date[['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']] if len(star_stock_finance_date) > 0 else pd.DataFrame(columns=['END_DATE', 'PUBLISH_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'NET_PROFIT', 'MAIN_INCOME_PS', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS'])
            stock_finance_date = pd.concat([stock_finance_date, star_stock_finance_date])
            stock_finance_list.append(stock_finance_date)
            print(date)
        self.stock_finance = pd.concat([existed_stock_finance] + stock_finance_list, ignore_index=True)
        self.stock_finance = self.stock_finance.sort_values(['END_DATE', 'TICKER_SYMBOL', 'PUBLISH_DATE'])
        self.stock_finance = self.stock_finance.reset_index().drop('index', axis=1)
        self.stock_finance.to_hdf(stock_finance_path, key='table', mode='w')
        self.stock_finance = pd.read_hdf(stock_finance_path, key='table')

        for type in ['FY0', 'FY1', 'FY2', 'FTTM', 'YOY']:
            stock_consensus_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_{0}.hdf'.format(type)
            if os.path.isfile(stock_consensus_path):
                existed_stock_consensus = pd.read_hdf(stock_consensus_path, key='table')
                max_date = max(existed_stock_consensus['EST_DT'])
                start_date = max(str(max_date), '20150101')
            else:
                existed_stock_consensus = pd.DataFrame()
                start_date = '20150101'
            calendar_df = self.calendar_df[(self.calendar_df['CALENDAR_DATE'] > start_date) & (self.calendar_df['CALENDAR_DATE'] < datetime.today().strftime('%Y%m%d'))]
            stock_consensus_list = []
            for date in calendar_df['CALENDAR_DATE'].unique().tolist():
                stock_consensus_date = HBDB().read_consensus_given_date(date, type)
                stock_consensus_list.append(stock_consensus_date)
                print(date)
            self.stock_consensus = pd.concat([existed_stock_consensus] + stock_consensus_list, ignore_index=True)
            self.stock_consensus = self.stock_consensus.sort_values(['EST_DT', 'TICKER_SYMBOL'])
            self.stock_consensus = self.stock_consensus.reset_index().drop('index', axis=1)
            self.stock_consensus.to_hdf(stock_consensus_path, key='table', mode='w')
        self.stock_consensus_fy0 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_fy0.hdf', key='table')
        self.stock_consensus_fy0['TICKER_SYMBOL'] = self.stock_consensus_fy0['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fy0 = self.stock_consensus_fy0.loc[self.stock_consensus_fy0['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fy0 = self.stock_consensus_fy0.loc[self.stock_consensus_fy0['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fy0 = self.stock_consensus_fy0[self.stock_consensus_fy0['EST_DT'] >= str(int(self.start_date[:4]) - 1) + self.start_date[4:]]
        self.stock_consensus_fy1 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_fy1.hdf', key='table')
        self.stock_consensus_fy1['TICKER_SYMBOL'] = self.stock_consensus_fy1['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fy1 = self.stock_consensus_fy1.loc[self.stock_consensus_fy1['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fy1 = self.stock_consensus_fy1.loc[self.stock_consensus_fy1['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fy1 = self.stock_consensus_fy1[ self.stock_consensus_fy1['EST_DT'] >= str(int(self.start_date[:4]) - 1) + self.start_date[4:]]
        self.stock_consensus_fy2 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_fy2.hdf', key='table')
        self.stock_consensus_fy2['TICKER_SYMBOL'] = self.stock_consensus_fy2['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fy2 = self.stock_consensus_fy2.loc[self.stock_consensus_fy2['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fy2 = self.stock_consensus_fy2.loc[self.stock_consensus_fy2['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fy2 = self.stock_consensus_fy2[self.stock_consensus_fy2['EST_DT'] >= str(int(self.start_date[:4]) - 1) + self.start_date[4:]]
        self.stock_consensus_fttm = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_fttm.hdf', key='table')
        self.stock_consensus_fttm['TICKER_SYMBOL'] = self.stock_consensus_fttm['TICKER_SYMBOL'].apply( lambda x: x.split('.')[0])
        self.stock_consensus_fttm = self.stock_consensus_fttm.loc[self.stock_consensus_fttm['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fttm = self.stock_consensus_fttm.loc[self.stock_consensus_fttm['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fttm = self.stock_consensus_fttm[self.stock_consensus_fttm['EST_DT'] >= str(int(self.start_date[:4]) - 1) + self.start_date[4:]]
        self.stock_consensus_yoy = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_yoy.hdf', key='table')
        self.stock_consensus_yoy['TICKER_SYMBOL'] = self.stock_consensus_yoy['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_yoy = self.stock_consensus_yoy.loc[self.stock_consensus_yoy['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_yoy = self.stock_consensus_yoy.loc[self.stock_consensus_yoy['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_yoy = self.stock_consensus_yoy[self.stock_consensus_yoy['EST_DT'] >= str(int(self.start_date[:4]) - 1) + self.start_date[4:]]

    def get_exceed_consensus_new(self):
        stock_con = self.stock_consensus_fy1.copy(deep=True)
        stock_con = stock_con[['EST_DT', 'TICKER_SYMBOL', 'EST_NET_PROFIT']]
        stock_con = stock_con.pivot(index='EST_DT', columns='TICKER_SYMBOL', values='EST_NET_PROFIT').sort_index()
        stock_con = stock_con.fillna(method='ffill')
        stock_con = stock_con.unstack().reset_index()
        stock_con.columns = ['TICKER_SYMBOL', 'EST_DT', 'EST_NET_PROFIT']
        stock_con = stock_con[stock_con['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_con = stock_con.loc[stock_con['EST_DT'].str.slice(4, 8) == '1231']
        stock_con = stock_con.rename(columns={'EST_DT': 'REPORT_DATE', 'EST_NET_PROFIT': 'NET_PROFIT_CON'})
        stock_real = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_real = stock_real.loc[stock_real['END_DATE'].str.slice(4, 8) == '1231']
        stock_real = stock_real.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_real = stock_real[['END_DATE', 'TICKER_SYMBOL', 'NET_PROFIT']]
        stock_real = stock_real.rename(columns={'END_DATE': 'REPORT_DATE', 'NET_PROFIT': 'NET_PROFIT_REAL'})
        stock_exceed = stock_con.merge(stock_real, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='inner')
        stock_exceed['IS_EXCEED'] = stock_exceed['NET_PROFIT_REAL'] > stock_exceed['NET_PROFIT_CON']
        stock_exceed['IS_EXCEED'] = stock_exceed['IS_EXCEED'].astype(int)
        stock_exceed = stock_exceed.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_exceed = stock_exceed.dropna(subset=['REPORT_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'IS_EXCEED'])
        total_count = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'IS_EXCEED']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).count().reset_index().rename(columns={'IS_EXCEED': 'TOTAL_COUNT'})
        stock_exceed_count = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'IS_EXCEED']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'IS_EXCEED': 'IS_EXCEED_COUNT'})
        industry_exceed_consensus_ratio = stock_exceed_count.merge(total_count, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')
        industry_exceed_consensus_ratio['EXCEED_RATIO'] = industry_exceed_consensus_ratio['IS_EXCEED_COUNT'] / industry_exceed_consensus_ratio['TOTAL_COUNT']
        industry_exceed_consensus_ratio = industry_exceed_consensus_ratio.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='EXCEED_RATIO').sort_index()
        industry_exceed_consensus_ratio = industry_exceed_consensus_ratio[(industry_exceed_consensus_ratio.index > self.start_date) & (industry_exceed_consensus_ratio.index <= self.end_date)]
        industry_con = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'NET_PROFIT_CON']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_real = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'NET_PROFIT_REAL']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_exceed_consensus = industry_con.merge(industry_real, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')
        industry_exceed_consensus['IS_EXCEED'] = industry_exceed_consensus['NET_PROFIT_REAL'] > industry_exceed_consensus['NET_PROFIT_CON']
        industry_exceed_consensus['IS_EXCEED'] = industry_exceed_consensus['IS_EXCEED'].astype(int)
        industry_exceed_consensus = industry_exceed_consensus.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='IS_EXCEED').sort_index()
        industry_exceed_consensus = industry_exceed_consensus[(industry_exceed_consensus.index > self.start_date) & (industry_exceed_consensus.index <= self.end_date)]
        return industry_exceed_consensus, industry_exceed_consensus_ratio

    def get_exceed_consensus(self):
        stock_consensus = pd.concat([self.stock_consensus_fy0, self.stock_consensus_fy1])
        stock_consensus = stock_consensus.sort_values(['TICKER_SYMBOL', 'EST_DT', 'ROLLING_TYPE'])
        stock_consensus['YEAR'] = stock_consensus['EST_DT'].apply(lambda x: x[:4])
        stock_consensus_fy0 = self.stock_consensus_fy0.copy(deep=True)
        stock_consensus_fy0 = stock_consensus_fy0.sort_values(['TICKER_SYMBOL', 'EST_DT'])
        change_dates_t1 = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates('EST_NET_PROFIT', keep='last').iloc[:-1])
        change_dates_t2 = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates('EST_NET_PROFIT', keep='first').iloc[1:])
        change_dates_t1 = change_dates_t1[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE_T1'})
        change_dates_t2 = change_dates_t2[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE_T2'})
        change_dates_t1['YEAR'] = change_dates_t1['CHANGE_DATE_T1'].apply(lambda x: x[:4])
        change_dates_t2['YEAR'] = change_dates_t2['CHANGE_DATE_T2'].apply(lambda x: x[:4])
        change_dates_t1 = change_dates_t1.drop_duplicates(['TICKER_SYMBOL', 'YEAR'], keep='first')
        change_dates_t2 = change_dates_t2.drop_duplicates(['TICKER_SYMBOL', 'YEAR'], keep='first')
        change_dates_t1.index = range(len(change_dates_t1))
        change_dates_t2.index = range(len(change_dates_t2))
        stock_con = stock_consensus[stock_consensus['EST_DT'].isin(change_dates_t1['CHANGE_DATE_T1'].unique().tolist())]
        stock_real = stock_consensus[stock_consensus['EST_DT'].isin(change_dates_t2['CHANGE_DATE_T2'].unique().tolist())]
        stock_con = stock_con.merge(change_dates_t1, on=['TICKER_SYMBOL', 'YEAR'], how='left')
        stock_real = stock_real.merge(change_dates_t2, on=['TICKER_SYMBOL', 'YEAR'], how='left')
        stock_con = stock_con[(stock_con['EST_DT'] == stock_con['CHANGE_DATE_T1']) & (stock_con['ROLLING_TYPE'] == 'FY1')]
        stock_con['REPORT_DATE'] = stock_con['YEAR'].apply(lambda x: str(int(x) - 1) + '1231')
        stock_con = stock_con[['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT']].rename(columns={'EST_NET_PROFIT': 'NET_PROFIT_CON'})
        stock_real = stock_real[(stock_real['EST_DT'] == stock_real['CHANGE_DATE_T2']) & (stock_real['ROLLING_TYPE'] == 'FY0')]
        stock_real['REPORT_DATE'] = stock_real['YEAR'].apply(lambda x: str(int(x) - 1) + '1231')
        stock_real = stock_real[['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT']].rename(columns={'EST_NET_PROFIT': 'NET_PROFIT_REAL'})
        stock_exceed = stock_con.merge(stock_real, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='inner')
        stock_exceed['IS_EXCEED'] = stock_exceed['NET_PROFIT_REAL'] > stock_exceed['NET_PROFIT_CON']
        stock_exceed['IS_EXCEED'] = stock_exceed['IS_EXCEED'].astype(int)
        stock_exceed = stock_exceed.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_exceed = stock_exceed.dropna(subset=['REPORT_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'IS_EXCEED'])
        total_count = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'IS_EXCEED']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).count().reset_index().rename(columns={'IS_EXCEED': 'TOTAL_COUNT'})
        stock_exceed_count = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'IS_EXCEED']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'IS_EXCEED': 'IS_EXCEED_COUNT'})
        industry_exceed_consensus_ratio = stock_exceed_count.merge(total_count, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')
        industry_exceed_consensus_ratio['EXCEED_RATIO'] = industry_exceed_consensus_ratio['IS_EXCEED_COUNT'] / industry_exceed_consensus_ratio['TOTAL_COUNT']
        industry_exceed_consensus_ratio = industry_exceed_consensus_ratio.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='EXCEED_RATIO').sort_index()
        industry_exceed_consensus_ratio = industry_exceed_consensus_ratio[(industry_exceed_consensus_ratio.index > self.start_date) & (industry_exceed_consensus_ratio.index <= self.end_date)]
        industry_con = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'NET_PROFIT_CON']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_real = stock_exceed[['REPORT_DATE', 'INDUSTRY_NAME', 'NET_PROFIT_REAL']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_exceed_consensus = industry_con.merge(industry_real, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')
        industry_exceed_consensus['IS_EXCEED'] = industry_exceed_consensus['NET_PROFIT_REAL'] > industry_exceed_consensus['NET_PROFIT_CON']
        industry_exceed_consensus['IS_EXCEED'] = industry_exceed_consensus['IS_EXCEED'].astype(int)
        industry_exceed_consensus = industry_exceed_consensus.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='IS_EXCEED').sort_index()
        industry_exceed_consensus = industry_exceed_consensus[(industry_exceed_consensus.index > self.start_date) & (industry_exceed_consensus.index <= self.end_date)]
        return industry_exceed_consensus, industry_exceed_consensus_ratio

    def get_consensus_sum_fy1(self, index_name):
        # 取FY1数据，20220630/20220930/20221231对应2022预测数据，但20220331有可能对应2022预测数据，有可能对应2021预测数据
        stock_consensus_fy1 = self.stock_consensus_fy1.copy(deep=True)
        stock_consensus_fy1 = stock_consensus_fy1[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_fy1 = stock_consensus_fy1.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_fy1 = stock_consensus_fy1.fillna(method='ffill')
        stock_consensus_fy1 = stock_consensus_fy1.unstack().reset_index()
        stock_consensus_fy1.columns = ['TICKER_SYMBOL', 'EST_DT', index_name]
        stock_consensus_fy1 = stock_consensus_fy1[stock_consensus_fy1['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_consensus_fy1 = stock_consensus_fy1.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_fy1 = stock_consensus_fy1.dropna(subset=['EST_DT', 'TICKER_SYMBOL', 'INDUSTRY_NAME', index_name])
        industry_quarter_consensus_sum_fy1 = stock_consensus_fy1[['EST_DT', 'INDUSTRY_NAME', index_name]].groupby(['EST_DT', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_consensus_sum_fy1 = industry_quarter_consensus_sum_fy1.pivot(index='EST_DT', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_sum_fy1 = industry_quarter_consensus_sum_fy1[(industry_quarter_consensus_sum_fy1.index > self.start_date) & (industry_quarter_consensus_sum_fy1.index <= self.end_date)]
        return industry_quarter_consensus_sum_fy1

    def get_consensus_weighted_sum_fy1(self, index_name):
        # 取FY1数据，20220630/20220930/20221231对应2022预测数据，但20220331有可能对应2022预测数据，有可能对应2021预测数据
        stock_consensus_fy1 = self.stock_consensus_fy1.copy(deep=True)
        stock_consensus_fy1 = stock_consensus_fy1[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_fy1 = stock_consensus_fy1.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_fy1 = stock_consensus_fy1.fillna(method='ffill')
        stock_consensus_fy1 = stock_consensus_fy1.unstack().reset_index()
        stock_consensus_fy1.columns = ['TICKER_SYMBOL', 'TRADE_DATE', index_name]
        stock_consensus_fy1 = stock_consensus_fy1[stock_consensus_fy1['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_consensus_fy1 = stock_consensus_fy1.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_consensus_fy1 = stock_consensus_fy1.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_fy1 = stock_consensus_fy1.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_consensus_fy1[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_consensus_fy1 = stock_consensus_fy1.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_consensus_fy1['WEIGHT_' + index_name] = stock_consensus_fy1[index_name] * stock_consensus_fy1['MARKET_VALUE'] / stock_consensus_fy1['TOTAL_MARKET_VALUE']
        industry_quarter_consensus_weighted_sum_fy1 = stock_consensus_fy1[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_consensus_weighted_sum_fy1 = industry_quarter_consensus_weighted_sum_fy1.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_weighted_sum_fy1.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_consensus_weighted_sum_fy1.index)
        industry_quarter_consensus_weighted_sum_fy1 = industry_quarter_consensus_weighted_sum_fy1[(industry_quarter_consensus_weighted_sum_fy1.index > self.start_date) & (industry_quarter_consensus_weighted_sum_fy1.index <= self.end_date)]
        return industry_quarter_consensus_weighted_sum_fy1

    def get_consensus_sum_year(self, index_name):
       stock_consensus = pd.concat([self.stock_consensus_fy0, self.stock_consensus_fy1, self.stock_consensus_fy2])
       stock_consensus = stock_consensus.sort_values(['TICKER_SYMBOL', 'EST_DT', 'ROLLING_TYPE'])
       stock_consensus['YEAR'] = stock_consensus['EST_DT'].apply(lambda x: x[:4])
       stock_consensus_fy0 = self.stock_consensus_fy0.copy(deep=True)
       stock_consensus_fy0 = stock_consensus_fy0.sort_values(['TICKER_SYMBOL', 'EST_DT'])
       change_dates = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates('EST_NET_PROFIT', keep='last').iloc[:-1])
       change_dates = change_dates[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE'})
       change_dates['YEAR'] = change_dates['CHANGE_DATE'].apply(lambda x: x[:4])
       change_dates = change_dates.drop(['TICKER_SYMBOL', 'YEAR'], keep='first')
       change_dates.index = range(len(change_dates))
       stock_consensus = stock_consensus.merge(change_dates, on=['TICKER_SYMBOL', 'YEAR'], how='left')
       stock_consensus_bf = stock_consensus[stock_consensus['EST_DT'] <= stock_consensus['CHANGE_DATE']]
       stock_consensus_bf = stock_consensus_bf[stock_consensus_bf['ROLLING_TYPE'] == 'FY2']
       stock_consensus_af = stock_consensus[stock_consensus['EST_DT'] > stock_consensus['CHANGE_DATE']]
       stock_consensus_af = stock_consensus_af[stock_consensus_af['ROLLING_TYPE'] == 'FY1']
       stock_consensus_year = pd.concat([stock_consensus_bf, stock_consensus_af])

       stock_consensus_year = stock_consensus_year[['EST_DT', 'TICKER_SYMBOL', index_name]]
       stock_consensus_year = stock_consensus_year.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
       stock_consensus_year = stock_consensus_year.fillna(method='ffill')
       stock_consensus_year = stock_consensus_year.unstack().reset_index()
       stock_consensus_year.columns = ['TICKER_SYMBOL', 'EST_DT', index_name]
       stock_consensus_year = stock_consensus_year[stock_consensus_year['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
       stock_consensus_year = stock_consensus_year.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
       stock_consensus_year = stock_consensus_year.dropna(subset=['EST_DT', 'TICKER_SYMBOL', 'INDUSTRY_NAME', index_name])
       industry_quarter_consensus_sum_year = stock_consensus_year[['EST_DT', 'INDUSTRY_NAME', index_name]].groupby(['EST_DT', 'INDUSTRY_NAME']).sum().reset_index()
       industry_quarter_consensus_sum_year = industry_quarter_consensus_sum_year.pivot(index='EST_DT', columns='INDUSTRY_NAME', values=index_name).sort_index()
       industry_quarter_consensus_sum_year = industry_quarter_consensus_sum_year[(industry_quarter_consensus_sum_year.index > self.start_date) & (industry_quarter_consensus_sum_year.index <= self.end_date)]
       return industry_quarter_consensus_sum_year

    def get_consensus_weighted_sum_year(self, index_name):
        stock_consensus = pd.concat([self.stock_consensus_fy0, self.stock_consensus_fy1, self.stock_consensus_fy2])
        stock_consensus = stock_consensus.sort_values(['TICKER_SYMBOL', 'EST_DT', 'ROLLING_TYPE'])
        stock_consensus['YEAR'] = stock_consensus['EST_DT'].apply(lambda x: x[:4])
        stock_consensus_fy0 = self.stock_consensus_fy0.copy(deep=True)
        stock_consensus_fy0 = stock_consensus_fy0.sort_values(['TICKER_SYMBOL', 'EST_DT'])
        change_dates = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates('EST_NET_PROFIT', kee='last').iloc[:-1])
        change_dates = change_dates[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE'})
        change_dates['YEAR'] = change_dates['CHANGE_DATE'].apply(lambda x: x[:4])
        change_dates = change_dates.drop(['TICKER_SYMBOL', 'YEAR'], keep='first')
        change_dates.index = range(len(change_dates))
        stock_consensus = stock_consensus.merge(change_dates, on=['TICKER_SYMBOL', 'YEAR'], how='left')
        stock_consensus_bf = stock_consensus[stock_consensus['EST_DT'] <= stock_consensus['CHANGE_DATE']]
        stock_consensus_bf = stock_consensus_bf[stock_consensus_bf['ROLLING_TYPE'] == 'FY2']
        stock_consensus_af = stock_consensus[stock_consensus['EST_DT'] > stock_consensus['CHANGE_DATE']]
        stock_consensus_af = stock_consensus_af[stock_consensus_af['ROLLING_TYPE'] == 'FY1']
        stock_consensus_year = pd.concat([stock_consensus_bf, stock_consensus_af])

        stock_consensus_year = stock_consensus_year[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_year = stock_consensus_year.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_year = stock_consensus_year.fillna(method='ffill')
        stock_consensus_year = stock_consensus_year.unstack().reset_index()
        stock_consensus_year.columns = ['TICKER_SYMBOL', 'TRADE_DATE', index_name]
        stock_consensus_year = stock_consensus_year[stock_consensus_year['TRADE_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_consensus_year = stock_consensus_year.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_consensus_year = stock_consensus_year.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_year = stock_consensus_year.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_consensus_year[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_consensus_year = stock_consensus_year.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_consensus_year['WEIGHT_' + index_name] = stock_consensus_year[index_name] * stock_consensus_year['MARKET_VALUE'] / stock_consensus_year['TOTAL_MARKET_VALUE']
        industry_quarter_consensus_weighted_sum_year = stock_consensus_year[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_consensus_weighted_sum_year = industry_quarter_consensus_weighted_sum_year.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_weighted_sum_year.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_consensus_weighted_sum_year.index)
        industry_quarter_consensus_weighted_sum_year = industry_quarter_consensus_weighted_sum_year[(industry_quarter_consensus_weighted_sum_year.index > self.start_date) & (industry_quarter_consensus_weighted_sum_year.index <= self.end_date)]
        return industry_quarter_consensus_weighted_sum_year

    def get_consensus_sum_ttm(self, index_name):
        stock_consensus_ttm = self.stock_consensus_fttm.copy(deep=True)
        stock_consensus_ttm = stock_consensus_ttm[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_ttm = stock_consensus_ttm.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_ttm = stock_consensus_ttm.fillna(method='ffill')
        stock_consensus_ttm = stock_consensus_ttm.unstack().reset_index()
        stock_consensus_ttm.columns = ['TICKER_SYMBOL', 'EST_DT', index_name]
        stock_consensus_ttm = stock_consensus_ttm[stock_consensus_ttm['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_consensus_ttm = stock_consensus_ttm.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_ttm = stock_consensus_ttm.dropna(subset=['EST_DT', 'TICKER_SYMBOL', 'INDUSTRY_NAME', index_name])
        industry_quarter_consensus_sum_ttm = stock_consensus_ttm[['EST_DT', 'INDUSTRY_NAME', index_name]].groupby(['EST_DT', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_consensus_sum_ttm = industry_quarter_consensus_sum_ttm.pivot(index='EST_DT', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_sum_ttm = industry_quarter_consensus_sum_ttm[(industry_quarter_consensus_sum_ttm.index > self.start_date) & (industry_quarter_consensus_sum_ttm.index <= self.end_date)]
        return industry_quarter_consensus_sum_ttm

    def get_consensus_weighted_sum_ttm(self, index_name):
        stock_consensus_ttm = self.stock_consensus_fttm.copy(deep=True)
        stock_consensus_ttm = stock_consensus_ttm[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_ttm = stock_consensus_ttm.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_ttm = stock_consensus_ttm.fillna(method='ffill')
        stock_consensus_ttm = stock_consensus_ttm.unstack().reset_index()
        stock_consensus_ttm.columns = ['TICKER_SYMBOL', 'TRADE_DATE', index_name]
        stock_consensus_ttm = stock_consensus_ttm[stock_consensus_ttm['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_consensus_ttm = stock_consensus_ttm.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_consensus_ttm = stock_consensus_ttm.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_ttm = stock_consensus_ttm.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_consensus_ttm[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_consensus_ttm = stock_consensus_ttm.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_consensus_ttm['WEIGHT_' + index_name] = stock_consensus_ttm[index_name] * stock_consensus_ttm['MARKET_VALUE'] / stock_consensus_ttm['TOTAL_MARKET_VALUE']
        industry_quarter_consensus_weighted_sum_ttm = stock_consensus_ttm[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_consensus_weighted_sum_ttm = industry_quarter_consensus_weighted_sum_ttm.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_weighted_sum_ttm.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_consensus_weighted_sum_ttm.index)
        industry_quarter_consensus_weighted_sum_ttm = industry_quarter_consensus_weighted_sum_ttm[(industry_quarter_consensus_weighted_sum_ttm.index > self.start_date) & (industry_quarter_consensus_weighted_sum_ttm.index <= self.end_date)]
        return industry_quarter_consensus_weighted_sum_ttm

    def get_consensus_yoy(self, index_name):
        stock_consensus_yoy = self.stock_consensus_yoy.copy(deep=True)
        stock_consensus_yoy = stock_consensus_yoy[['EST_DT', 'TICKER_SYMBOL', index_name]]
        stock_consensus_yoy = stock_consensus_yoy.pivot(index='EST_DT', columns='TICKER_SYMBOL', values=index_name).sort_index()
        stock_consensus_yoy = stock_consensus_yoy.fillna(method='ffill')
        stock_consensus_yoy = stock_consensus_yoy.unstack().reset_index()
        stock_consensus_yoy.columns = ['TICKER_SYMBOL', 'TRADE_DATE', index_name]
        stock_consensus_yoy = stock_consensus_yoy[stock_consensus_yoy['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_consensus_yoy = stock_consensus_yoy.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_consensus_yoy = stock_consensus_yoy.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_consensus_yoy = stock_consensus_yoy.dropna(subset=['TRADE_DATE', 'TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_consensus_yoy[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_consensus_yoy = stock_consensus_yoy.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_consensus_yoy['WEIGHT_' + index_name] = stock_consensus_yoy[index_name] * stock_consensus_yoy['MARKET_VALUE'] / stock_consensus_yoy['TOTAL_MARKET_VALUE']
        industry_quarter_consensus_weighted_sum_yoy = stock_consensus_yoy[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_consensus_weighted_sum_yoy = industry_quarter_consensus_weighted_sum_yoy.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_consensus_weighted_sum_yoy.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_consensus_weighted_sum_yoy.index)
        industry_quarter_consensus_weighted_sum_yoy = industry_quarter_consensus_weighted_sum_yoy[(industry_quarter_consensus_weighted_sum_yoy.index > self.start_date) & (industry_quarter_consensus_weighted_sum_yoy.index <= self.end_date)]
        return industry_quarter_consensus_weighted_sum_yoy

    def get_all(self):
        exceed_consensus_new, exceed_consensus_ratio_new = self.get_exceed_consensus_new()
        exceed_consensus_new = exceed_consensus_new.unstack().reset_index()
        exceed_consensus_new.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'IS_EXCEED_NEW']
        exceed_consensus_ratio_new = exceed_consensus_ratio_new.unstack().reset_index()
        exceed_consensus_ratio_new.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'EXCEED_RATIO_NEW']
        exceed_consensus, exceed_consensus_ratio = self.get_exceed_consensus()
        exceed_consensus = exceed_consensus.unstack().reset_index()
        exceed_consensus.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'IS_EXCEED']
        exceed_consensus_ratio = exceed_consensus_ratio.unstack().reset_index()
        exceed_consensus_ratio.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'EXCEED_RATIO']

        index_list_1 = ['EST_NET_PROFIT', 'EST_OPER_REVENUE', 'EST_ROE', 'EST_EPS', 'EST_CFPS', 'EST_BPS', 'EST_PE', 'EST_PB', 'EST_PEG', 'EST_DPS']
        consensus_fy1_list = []
        for index_name in index_list_1:
            if index_name in ['EST_NET_PROFIT', 'EST_OPER_REVENUE']:
                consensus_fy1 = self.get_consensus_sum_fy1(index_name)
            else:
                consensus_fy1 = self.get_consensus_weighted_sum_fy1(index_name)
            consensus_fy1 = pd.DataFrame(consensus_fy1.unstack())
            consensus_fy1.columns = [index_name + '_FY1']
            consensus_fy1_list.append(consensus_fy1)
        consensus_fy1 = pd.concat(consensus_fy1_list, axis=1)
        consensus_fy1 = consensus_fy1.reset_index().rename(columns={'level_1': 'REPORT_DATE'})

        # consensus_year_list = []
        # for index_name in index_list_1:
        #     if index_name in ['EST_NET_PROFIT', 'EST_OPER_REVENUE']:
        #         consensus_year = self.get_consensus_sum_year(index_name)
        #     else:
        #         consensus_year = self.get_consensus_weighted_sum_year(index_name)
        #     consensus_year = pd.DataFrame(consensus_year.unstack())
        #     consensus_year.columns = [index_name + '_YEAR']
        #     consensus_year_list.append(consensus_year)
        # consensus_year = pd.concat(consensus_year_list, axis=1)
        # consensus_year = consensus_year.reset_index().rename(columns={'level_1': 'REPORT_DATE'})

        index_list_2 = ['EST_NET_PROFIT', 'EST_OPER_REVENUE', 'EST_EPS', 'EST_CFPS', 'EST_PE', 'EST_PEG']
        consensus_ttm_list = []
        for index_name in index_list_2:
            if index_name in ['EST_NET_PROFIT', 'EST_OPER_REVENUE']:
                consensus_ttm = self.get_consensus_sum_ttm(index_name)
            else:
                consensus_ttm = self.get_consensus_weighted_sum_ttm(index_name)
            consensus_ttm = pd.DataFrame(consensus_ttm.unstack())
            consensus_ttm.columns = [index_name + '_TTM']
            consensus_ttm_list.append(consensus_ttm)
        consensus_ttm = pd.concat(consensus_ttm_list, axis=1)
        consensus_ttm = consensus_ttm.reset_index().rename(columns={'level_1': 'REPORT_DATE'})

        index_list_3 = ['EST_NET_PROFIT', 'EST_OPER_REVENUE', 'EST_ROE', 'EST_EPS']
        consensus_yoy_list = []
        for index_name in index_list_3:
            consensus_yoy = self.get_consensus_yoy(index_name)
            consensus_yoy = pd.DataFrame(consensus_yoy.unstack())
            consensus_yoy.columns = [index_name + '_YOY']
            consensus_yoy_list.append(consensus_yoy)
        consensus_yoy = pd.concat(consensus_yoy_list, axis=1)
        consensus_yoy = consensus_yoy.reset_index().rename(columns={'level_1': 'REPORT_DATE'})

        industry_consensus = consensus_fy1.merge(consensus_ttm, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left') \
                                          .merge(consensus_yoy, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left') \
                                          .merge(exceed_consensus, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')\
                                          .merge(exceed_consensus_ratio, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')\
                                          .merge(exceed_consensus_new, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left') \
                                          .merge(exceed_consensus_ratio_new, on=['REPORT_DATE', 'INDUSTRY_NAME'], how='left')
        industry_consensus['INDUSTRY_ID'] = industry_consensus['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_consensus['INDUSTRY_TYPE'] = self.sw_type
        industry_consensus = industry_consensus[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'IS_EXCEED_NEW', 'EXCEED_RATIO_NEW', 'IS_EXCEED', 'EXCEED_RATIO'] + [index + '_FY1' for index in index_list_1] + [index + '_TTM' for index in index_list_2] + [index + '_YOY' for index in index_list_3]]
        industry_consensus_columns = industry_consensus.columns
        industry_consensus[industry_consensus_columns[4:]] = industry_consensus[industry_consensus_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_consensus_df(industry_consensus, list(industry_consensus.columns))

class IndustryHead:
    def __init__(self, sw_type, start_date, end_date, head):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.head = head
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        self.benchmark_daily_k = HBDB().read_index_daily_k_given_date_and_indexs(self.data_start_date, ['881001'])
        self.benchmark_daily_k = self.benchmark_daily_k.rename(columns={'zqmc': 'BENCHMARK_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        self.benchmark_daily_k['TRADE_DATE'] = self.benchmark_daily_k['TRADE_DATE'].astype(str)
        self.benchmark_daily_k = self.benchmark_daily_k.sort_values('TRADE_DATE')
        self.benchmark_daily_k = self.benchmark_daily_k.pivot(index='TRADE_DATE', columns='BENCHMARK_NAME', values='CLOSE_INDEX').sort_index()

        stock_market_value_list, star_stock_market_value_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            stock_market_value_list.append(stock_market_value_date)
            star_stock_market_value_list.append(star_stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat(stock_market_value_list)
        self.star_stock_market_value = pd.concat(star_stock_market_value_list)
        self.stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_market_value.hdf', key='table', mode='w')
        self.star_stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_market_value.hdf', key='table', mode='w')
        self.stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_market_value.hdf', key='table')
        self.star_stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_market_value.hdf', key='table')
        self.stock_market_value = pd.concat([self.stock_market_value, self.star_stock_market_value])

        stock_daily_k_list, star_stock_daily_k_list = [], []
        for date in self.trade_df['TRADE_DATE'].unique().tolist():
            stock_daily_k_date = HBDB().read_stock_daily_k_given_date(date)
            star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(date)
            stock_daily_k_list.append(stock_daily_k_date)
            star_stock_daily_k_list.append(star_stock_daily_k_date)
            print(date)
        self.stock_daily_k = pd.concat(stock_daily_k_list)
        self.star_stock_daily_k = pd.concat(star_stock_daily_k_list)
        self.stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_daily_k.hdf', key='table', mode='w')
        self.star_stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_daily_k.hdf', key='table', mode='w')
        self.stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_daily_k.hdf', key='table')
        self.star_stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_daily_k.hdf', key='table')
        self.stock_daily_k = pd.concat([self.stock_daily_k, self.star_stock_daily_k])

        stock_valuation_list, star_stock_valuation_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            stock_valuation_list.append(stock_valuation_date)
            star_stock_valuation_list.append(star_stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat(stock_valuation_list)
        self.star_stock_valuation = pd.concat(star_stock_valuation_list)
        self.stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_valuation.hdf', key='table', mode='w')
        self.star_stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_valuation.hdf', key='table', mode='w')
        self.stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_valuation.hdf', key='table')
        self.star_stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_valuation.hdf', key='table')
        self.stock_valuation = pd.concat([self.stock_valuation, self.star_stock_valuation])

        stock_finance_list, star_stock_finance_list = [], []
        for date in self.report_df['REPORT_DATE'].unique().tolist():
            stock_finance_date = HBDB().read_stock_finance_given_date(date)
            star_stock_finance_date = HBDB().read_star_stock_finance_given_date(date)
            stock_finance_list.append(stock_finance_date)
            star_stock_finance_list.append(star_stock_finance_date)
            print(date)
        self.stock_finance = pd.concat(stock_finance_list)
        self.star_stock_finance = pd.concat(star_stock_finance_list)
        self.stock_finance.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_finance.hdf', key='table', mode='w')
        self.star_stock_finance.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_finance.hdf', key='table', mode='w')
        self.stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_finance.hdf', key='table')
        self.star_stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/star_stock_finance.hdf', key='table')
        self.stock_finance = pd.concat([self.stock_finance, self.star_stock_finance])

        calendar_df = HBDB().read_cal(self.data_start_date, datetime.today().strftime('%Y%m%d'))
        calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
        calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
        calendar_df = calendar_df.sort_values('CALENDAR_DATE')
        for type in ['FY0', 'FY1', 'FY2', 'FTTM']:
            stock_consensus_list = []
            for date in calendar_df['CALENDAR_DATE'].unique().tolist():
                stock_consensus_date = HBDB().read_consensus_given_date(date, type)
                stock_consensus_list.append(stock_consensus_date)
                print(date)
            self.stock_consensus = pd.concat(stock_consensus_list)
            self.stock_consensus.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_{0}.hdf'.format(type), key='table', mode='w')
        self.stock_consensus_fy0 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_FY0.hdf', key='table')
        self.stock_consensus_fy0['TICKER_SYMBOL'] = self.stock_consensus_fy0['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fy0 = self.stock_consensus_fy0.loc[self.stock_consensus_fy0['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fy0 = self.stock_consensus_fy0.loc[self.stock_consensus_fy0['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fy1 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_FY1.hdf', key='table')
        self.stock_consensus_fy1['TICKER_SYMBOL'] = self.stock_consensus_fy1['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fy1 = self.stock_consensus_fy1.loc[self.stock_consensus_fy1['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fy1 = self.stock_consensus_fy1.loc[self.stock_consensus_fy1['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        # self.stock_consensus_fy2 = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_FY2.hdf', key='table')
        # self.stock_consensus_fy2['TICKER_SYMBOL'] = self.stock_consensus_fy2['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        # self.stock_consensus_fy2 = self.stock_consensus_fy2.loc[self.stock_consensus_fy2['TICKER_SYMBOL'].str.len() == 6]
        # self.stock_consensus_fy2 = self.stock_consensus_fy2.loc[self.stock_consensus_fy2['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
        self.stock_consensus_fttm = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/industry_analysis/stock_consensus_FTTM.hdf', key='table')
        self.stock_consensus_fttm['TICKER_SYMBOL'] = self.stock_consensus_fttm['TICKER_SYMBOL'].apply(lambda x: x.split('.')[0])
        self.stock_consensus_fttm = self.stock_consensus_fttm.loc[self.stock_consensus_fttm['TICKER_SYMBOL'].str.len() == 6]
        self.stock_consensus_fttm = self.stock_consensus_fttm.loc[self.stock_consensus_fttm['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]

    def industry_head_stocks(self):
        stock_market_value = self.stock_market_value[self.stock_market_value['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_market_value = stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_market_value = stock_market_value.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE'])
        stock_market_value['REPORT_DATE'] = stock_market_value['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231')
        stock_market_value = stock_market_value.sort_values(['REPORT_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE'], ascending=[True, True, False])
        industry_quarter_head_stocks = stock_market_value.groupby(['REPORT_DATE', 'INDUSTRY_NAME']).head(self.head)
        industry_quarter_head_stocks = industry_quarter_head_stocks[(industry_quarter_head_stocks['REPORT_DATE'] >= self.start_date) & (industry_quarter_head_stocks['REPORT_DATE'] <= self.end_date)]
        industry_quarter_head_stocks = industry_quarter_head_stocks[['REPORT_DATE', 'INDUSTRY_NAME', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE']]
        return industry_quarter_head_stocks

    def industry_head_technology(self, head_stocks):
        head_stocks_daily_k = self.stock_daily_k.copy(deep=True)
        head_stocks_daily_k = head_stocks_daily_k[head_stocks_daily_k['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_daily_k = head_stocks_daily_k[head_stocks_daily_k['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        head_stocks_daily_k = head_stocks_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE')
        industry_quarter_head_ret = (head_stocks_daily_k / head_stocks_daily_k.shift() - 1).dropna(how='all')
        industry_quarter_head_ret.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_head_ret.index)
        industry_quarter_head_ret = industry_quarter_head_ret.unstack().reset_index()
        industry_quarter_head_ret.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'RET']

        head_stocks_daily_k = self.stock_daily_k.copy(deep=True)
        head_stocks_daily_k = head_stocks_daily_k[head_stocks_daily_k['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_daily_k = head_stocks_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE')
        head_stocks_daily_ret = (head_stocks_daily_k / head_stocks_daily_k.shift() - 1).dropna(how='all')
        head_stocks_daily_ret = head_stocks_daily_ret.unstack().reset_index()
        head_stocks_daily_ret.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'DAILY_RET']
        head_stocks_daily_ret['REPORT_DATE'] = head_stocks_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_head_vol = head_stocks_daily_ret[['REPORT_DATE', 'TICKER_SYMBOL', 'DAILY_RET']].groupby(['REPORT_DATE', 'TICKER_SYMBOL']).std(ddof=1).reset_index().rename(columns={'DAILY_RET': 'VOL'})
        industry_quarter_head_vol = industry_quarter_head_vol[['TICKER_SYMBOL', 'REPORT_DATE', 'VOL']]

        head_stocks_daily_k = self.stock_daily_k.copy(deep=True)
        head_stocks_daily_k = head_stocks_daily_k[head_stocks_daily_k['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_daily_k = head_stocks_daily_k.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='CLOSE_PRICE')
        head_stocks_daily_ret = (head_stocks_daily_k / head_stocks_daily_k.shift() - 1).dropna(how='all')
        head_stocks_daily_ret = head_stocks_daily_ret.unstack().reset_index()
        head_stocks_daily_ret.columns = ['TICKER_SYMBOL', 'TRADE_DATE', 'DAILY_RET']
        benchmark_daily_ret = (self.benchmark_daily_k / self.benchmark_daily_k.shift() - 1).dropna(how='all')
        benchmark_daily_ret = benchmark_daily_ret.unstack().reset_index()
        benchmark_daily_ret.columns = ['BENCHMARK_NAME', 'TRADE_DATE', 'BENCHMARK_DAILY_RET']
        head_stocks_daily_ret = head_stocks_daily_ret.merge(benchmark_daily_ret, on=['TRADE_DATE'], how='inner')
        head_stocks_daily_ret['REPORT_DATE'] = head_stocks_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_head_beta = head_stocks_daily_ret[['REPORT_DATE', 'TICKER_SYMBOL', 'DAILY_RET', 'BENCHMARK_DAILY_RET']].groupby(['REPORT_DATE', 'TICKER_SYMBOL']).apply(lambda x: np.cov(x['DAILY_RET'], x['BENCHMARK_DAILY_RET'])[0, 1] / np.var(x['BENCHMARK_DAILY_RET'])).reset_index().rename(columns={0: 'BETA'})
        industry_quarter_head_beta = industry_quarter_head_beta[['TICKER_SYMBOL', 'REPORT_DATE', 'BETA']]

        industry_quarter_technology = industry_quarter_head_ret.merge(industry_quarter_head_vol, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                                               .merge(industry_quarter_head_beta, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')
        return industry_quarter_technology

    def industry_head_valuation(self, head_stocks):
        head_stocks_valuation = self.stock_valuation.copy(deep=True)
        head_stocks_valuation = head_stocks_valuation[head_stocks_valuation['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_valuation = head_stocks_valuation[head_stocks_valuation['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        head_stocks_valuation['REPORT_DATE'] = head_stocks_valuation['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231')
        industry_quarter_valuation = head_stocks_valuation[['TICKER_SYMBOL', 'REPORT_DATE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]
        return industry_quarter_valuation

    def industry_head_fundamental(self, head_stocks):
        head_stocks_finance = self.stock_finance.copy(deep=True)
        head_stocks_finance = head_stocks_finance[head_stocks_finance['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_finance = head_stocks_finance[head_stocks_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        head_stocks_finance = head_stocks_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        head_stocks_finance = head_stocks_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='inner')
        head_stocks_finance = head_stocks_finance.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        head_stocks_finance = head_stocks_finance.merge(self.stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        head_stocks_finance['MAIN_INCOME'] = head_stocks_finance['MAIN_INCOME_PS'] * (head_stocks_finance['MARKET_VALUE'] / head_stocks_finance['CLOSE_PRICE'])

        accum_net_profit = head_stocks_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='NET_PROFIT')
        accum_net_profit = accum_net_profit.sort_index()
        net_profit_Q1 = accum_net_profit.loc[accum_net_profit.index.str.slice(4, 6) == '03']
        net_profit = accum_net_profit - accum_net_profit.shift()
        net_profit = net_profit.loc[net_profit.index.str.slice(4, 6) != '03']
        net_profit = pd.concat([net_profit_Q1, net_profit])
        net_profit = net_profit.sort_index()
        net_profit_ttm = net_profit.rolling(window=4, min_periods=4).sum()
        net_profit = net_profit.unstack().reset_index()
        net_profit_ttm = net_profit_ttm.unstack().reset_index()
        net_profit.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'NET_PROFIT']
        net_profit_ttm.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'NET_PROFIT_TTM']

        accum_main_income = head_stocks_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='MAIN_INCOME')
        accum_main_income = accum_main_income.sort_index()
        main_income_Q1 = accum_main_income.loc[accum_main_income.index.str.slice(4, 6) == '03']
        main_income = accum_main_income - accum_main_income.shift()
        main_income = main_income.loc[main_income.index.str.slice(4, 6) != '03']
        main_income = pd.concat([main_income_Q1, main_income])
        main_income = main_income.sort_index()
        main_income_ttm = main_income.rolling(window=4, min_periods=4).sum()
        main_income = main_income.unstack().reset_index()
        main_income_ttm = main_income_ttm.unstack().reset_index()
        main_income.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'MAIN_INCOME']
        main_income_ttm.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'MAIN_INCOME_TTM']

        head_stocks_finance = head_stocks_finance[['TICKER_SYMBOL', 'END_DATE', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']].rename(columns={'END_DATE': 'REPORT_DATE'})

        industry_quarter_fundamental = net_profit.merge(net_profit_ttm, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                                 .merge(main_income, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left') \
                                                 .merge(main_income_ttm, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left') \
                                                 .merge(head_stocks_finance, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')
        return industry_quarter_fundamental


    def industry_head_fundamental_derive(self, head_fundamental):
        def get_yoy(index):
            index_data = head_fundamental[['REPORT_DATE', 'TICKER_SYMBOL', index]]
            index_data = index_data.pivot(index='REPORT_DATE', columns='TICKER_SYMBOL', values=index).sort_index()
            index_data = index_data.replace(0.0, np.nan)
            yoy_ratio = (index_data - index_data.shift(4)) / abs(index_data.shift(4))
            return yoy_ratio.dropna(how='all')

        def get_mom(index):
            index_data = head_fundamental[['REPORT_DATE', 'TICKER_SYMBOL', index]]
            index_data = index_data.pivot(index='REPORT_DATE', columns='TICKER_SYMBOL', values=index).sort_index()
            index_data = index_data.replace(0.0, np.nan)
            mom_ratio = (index_data - index_data.shift()) / abs(index_data.shift())
            return mom_ratio.dropna(how='all')

        def get_yoy_abs(index):
            index_data = head_fundamental[['REPORT_DATE', 'TICKER_SYMBOL', index]]
            index_data = index_data.pivot(index='REPORT_DATE', columns='TICKER_SYMBOL', values=index).sort_index()
            index_data = index_data.replace(0.0, np.nan)
            yoy_abs = (index_data - index_data.shift(4))
            return yoy_abs.dropna(how='all')

        def get_mom_abs(index):
            index_data = head_fundamental[['REPORT_DATE', 'TICKER_SYMBOL', index]]
            index_data = index_data.pivot(index='REPORT_DATE', columns='TICKER_SYMBOL', values=index).sort_index()
            index_data = index_data.replace(0.0, np.nan)
            mom_abs = (index_data - index_data.shift())
            return mom_abs.dropna(how='all')

        index_list = ['NET_PROFIT', 'NET_PROFIT_TTM', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']

        yoy_list, mom_list = [], []
        for index in index_list:
            yoy = get_yoy(index)
            yoy = pd.DataFrame(yoy.unstack())
            yoy.columns = ['{0}_YOY'.format(index)]
            yoy_list.append(yoy)
            mom = get_mom(index)
            mom = pd.DataFrame(mom.unstack())
            mom.columns = ['{0}_MOM'.format(index)]
            mom_list.append(mom)
        yoy_abs_list, mom_abs_list = [], []
        for index in index_list[4:]:
            yoy_abs = get_yoy_abs(index)
            yoy_abs = pd.DataFrame(yoy_abs.unstack())
            yoy_abs.columns = ['{0}_YOY_ABS'.format(index)]
            yoy_abs_list.append(yoy_abs)
            mom_abs = get_mom_abs(index)
            mom_abs = pd.DataFrame(mom_abs.unstack())
            mom_abs.columns = ['{0}_MOM_ABS'.format(index)]
            mom_abs_list.append(mom_abs)
        industry_head_fundamental_derive = pd.concat(yoy_list + mom_list + yoy_abs_list + mom_abs_list, axis=1)
        industry_head_fundamental_derive = industry_head_fundamental_derive.reset_index()
        return industry_head_fundamental_derive

    def industry_head_consensus(self, head_stocks, index_name='EST_NET_PROFIT'):
        stock_consensus = pd.concat([self.stock_consensus_fy0, self.stock_consensus_fy1])
        stock_consensus = stock_consensus[stock_consensus['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        stock_consensus = stock_consensus.sort_values(['TICKER_SYMBOL', 'EST_DT', 'ROLLING_TYPE'])
        stock_consensus['YEAR'] = stock_consensus['EST_DT'].apply(lambda x: x[:4])
        stock_consensus_fy0 = self.stock_consensus_fy0.copy(deep=True)
        stock_consensus_fy0 = stock_consensus_fy0[stock_consensus_fy0['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        stock_consensus_fy0 = stock_consensus_fy0.sort_values(['TICKER_SYMBOL', 'EST_DT'])
        change_dates_t1 = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates(index_name, keep='last').iloc[:-1])
        change_dates_t2 = stock_consensus_fy0.groupby('TICKER_SYMBOL').apply(lambda x: x.sort_values('EST_DT').drop_duplicates(index_name, keep='first').iloc[1:])
        change_dates_t1 = change_dates_t1[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE_T1'})
        change_dates_t2 = change_dates_t2[['TICKER_SYMBOL', 'EST_DT']].rename(columns={'EST_DT': 'CHANGE_DATE_T2'})
        change_dates_t1['YEAR'] = change_dates_t1['CHANGE_DATE_T1'].apply(lambda x: x[:4])
        change_dates_t2['YEAR'] = change_dates_t2['CHANGE_DATE_T2'].apply(lambda x: x[:4])
        change_dates_t1 = change_dates_t1.drop_duplicates(['TICKER_SYMBOL', 'YEAR'], keep='first')
        change_dates_t2 = change_dates_t2.drop_duplicates(['TICKER_SYMBOL', 'YEAR'], keep='first')
        change_dates_t1.index = range(len(change_dates_t1))
        change_dates_t2.index = range(len(change_dates_t2))
        stock_con = stock_consensus[stock_consensus['EST_DT'].isin(change_dates_t1['CHANGE_DATE_T1'].unique().tolist())]
        stock_real = stock_consensus[stock_consensus['EST_DT'].isin(change_dates_t2['CHANGE_DATE_T2'].unique().tolist())]
        stock_con = stock_con.merge(change_dates_t1, on=['TICKER_SYMBOL', 'YEAR'], how='left')
        stock_real = stock_real.merge(change_dates_t2, on=['TICKER_SYMBOL', 'YEAR'], how='left')
        stock_con = stock_con[(stock_con['EST_DT'] == stock_con['CHANGE_DATE_T1']) & (stock_con['ROLLING_TYPE'] == 'FY1')]
        stock_con['REPORT_DATE'] = stock_con['YEAR'].apply(lambda x: str(int(x) - 1) + '1231')
        stock_con = stock_con[['TICKER_SYMBOL', 'REPORT_DATE', index_name]].rename(columns={index_name: index_name + '_CON'})
        stock_real = stock_real[(stock_real['EST_DT'] == stock_real['CHANGE_DATE_T2']) & (stock_real['ROLLING_TYPE'] == 'FY0')]
        stock_real['REPORT_DATE'] = stock_real['YEAR'].apply(lambda x: str(int(x) - 1) + '1231')
        stock_real = stock_real[['TICKER_SYMBOL', 'REPORT_DATE', index_name]].rename(columns={index_name: index_name + '_REAL'})
        stock_exceed = stock_con.merge(stock_real, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='inner')
        stock_exceed['IS_EXCEED'] = stock_exceed[index_name + '_REAL'] > stock_exceed[index_name + '_CON']
        stock_exceed['IS_EXCEED'] = stock_exceed['IS_EXCEED'].astype(int)
        stock_exceed = stock_exceed[['TICKER_SYMBOL', 'REPORT_DATE', 'IS_EXCEED']]

        head_stocks_consensus_fy1 = self.stock_consensus_fy1.copy(deep=True)
        head_stocks_consensus_fy1 = head_stocks_consensus_fy1[head_stocks_consensus_fy1['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_consensus_fy1 = head_stocks_consensus_fy1[head_stocks_consensus_fy1['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        head_stocks_consensus_fy1['REPORT_DATE'] = head_stocks_consensus_fy1['EST_DT']
        head_stocks_consensus_fy1 = head_stocks_consensus_fy1[['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT', 'EST_OPER_REVENUE', 'EST_ROE', 'EST_EPS', 'EST_CFPS', 'EST_BPS', 'EST_PE', 'EST_PB', 'EST_PEG', 'EST_DPS']]
        head_stocks_consensus_fy1.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT_FY1', 'EST_OPER_REVENUE_FY1', 'EST_ROE_FY1', 'EST_EPS_FY1', 'EST_CFPS_FY1', 'EST_BPS_FY1', 'EST_PE_FY1', 'EST_PB_FY1', 'EST_PEG_FY1', 'EST_DPS_FY1']

        head_stocks_consensus_fttm = self.stock_consensus_fttm.copy(deep=True)
        head_stocks_consensus_fttm = head_stocks_consensus_fttm[head_stocks_consensus_fttm['TICKER_SYMBOL'].isin(head_stocks['TICKER_SYMBOL'].unique().tolist())]
        head_stocks_consensus_fttm = head_stocks_consensus_fttm[head_stocks_consensus_fttm['EST_DT'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        head_stocks_consensus_fttm['REPORT_DATE'] = head_stocks_consensus_fttm['EST_DT']
        head_stocks_consensus_fttm = head_stocks_consensus_fttm[['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT', 'EST_OPER_REVENUE', 'EST_EPS', 'EST_CFPS', 'EST_PE', 'EST_PEG']]
        head_stocks_consensus_fttm.columns = ['TICKER_SYMBOL', 'REPORT_DATE', 'EST_NET_PROFIT_FTTM', 'EST_OPER_REVENUE_FTTM', 'EST_EPS_FTTM', 'EST_CFPS_FTTM', 'EST_PE_FTTM', 'EST_PEG_FTTM']

        industry_head_consensus = head_stocks_consensus_fy1.merge(head_stocks_consensus_fttm, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                                           .merge(stock_exceed, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')
        industry_head_consensus = industry_head_consensus[['TICKER_SYMBOL', 'REPORT_DATE', 'IS_EXCEED', 'EST_NET_PROFIT_FY1', 'EST_OPER_REVENUE_FY1', 'EST_ROE_FY1', 'EST_EPS_FY1', 'EST_CFPS_FY1', 'EST_BPS_FY1', 'EST_PE_FY1', 'EST_PB_FY1', 'EST_PEG_FY1', 'EST_DPS_FY1', 'EST_NET_PROFIT_FTTM', 'EST_OPER_REVENUE_FTTM', 'EST_EPS_FTTM', 'EST_CFPS_FTTM', 'EST_PE_FTTM', 'EST_PEG_FTTM']]
        return industry_head_consensus


    def get_all(self):
        head_stocks = self.industry_head_stocks()
        head_technology = self.industry_head_technology(head_stocks)
        head_valuation = self.industry_head_valuation(head_stocks)
        head_fundamental = self.industry_head_fundamental(head_stocks)
        head_fundamental_derive = self.industry_head_fundamental_derive(head_fundamental)
        head_consensus = self.industry_head_consensus(head_stocks)

        industry_head = head_stocks.merge(head_technology, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                   .merge(head_valuation, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                   .merge(head_fundamental, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                   .merge(head_fundamental_derive, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')\
                                   .merge(head_consensus, on=['TICKER_SYMBOL', 'REPORT_DATE'], how='left')
        industry_head_columns = list(industry_head.columns)[4:]
        industry_head['INDUSTRY_ID'] = industry_head['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_head['INDUSTRY_TYPE'] = self.sw_type
        industry_head = industry_head[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME'] + industry_head_columns]
        industry_head_columns = industry_head.columns
        industry_head[industry_head_columns[6:]] = industry_head[industry_head_columns[6:]].replace(np.nan, None)
        InsertTable().insert_industry_head_df(industry_head, list(industry_head.columns))

if __name__ == "__main__":
    start_date = '20220630'
    end_date = '20220930'
    head = 5
    for sw_type in [1, 2, 3]:
        IndustryTechnology(sw_type, start_date, end_date).get_all()
        IndustryValuation(sw_type, start_date, end_date).get_all()
        IndustryFundamental(sw_type, start_date, end_date).get_all()
        IndustryFundamentalDerive(sw_type, start_date, end_date).get_all()
        IndustryConsensus(sw_type, start_date, end_date).get_all()
        IndustryHead(sw_type, start_date, end_date, head).get_all()