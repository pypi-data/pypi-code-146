"""
Wind计算的转债的隐含波动率
"""
import numpy as np
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
import hbshare as hbs
from WindPy import w

w.start()


class CBMarketIV:
    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = "cb_market_iv"
        self._load_data()

    def _load_data(self):
        trading_day_list = get_trading_day_list(self.start_date, self.end_date)
        # data set
        res = w.wset("cbissue", "startdate=2012-01-01;enddate={}".format(datetime.now().strftime('%Y-%m-%d')))
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("Fetching cbissue data error!")
        else:
            data = pd.DataFrame(res.Data, index=res.Fields, columns=res.Codes).T
        # preprocess
        issue_data = data[data['issue_type'].isin(['优先配售和上网定价', '优先配售,网上定价和网下配售'])]
        issue_data = issue_data[['bond_code', 'bond_name', 'listing_date', 'interest_end_date']].dropna()
        issue_data['listing_date'] = issue_data['listing_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        issue_data['interest_end_date'] = issue_data['interest_end_date'].apply(
            lambda x: datetime.strftime(x, '%Y%m%d'))
        # iv data
        iv_list = []
        for date in tqdm(trading_day_list):
            exist_cb = issue_data[(issue_data['listing_date'] < date) & (issue_data['interest_end_date'] > date)]
            cb_code_list = exist_cb['bond_code'].unique()
            res = w.wss(','.join(cb_code_list), "impliedvol", "tradeDate={};rfIndex=7".format(date))
            if res.ErrorCode != 0:
                data = pd.DataFrame()
                print("fetch implied volatility data error: trade_date = {}".format(date))
            else:
                data = pd.DataFrame(res.Data[0], index=res.Codes, columns=res.Times)
            data.columns = ['iv']
            data.index.name = 'bond_code'
            data = data.reset_index().dropna()
            data['trade_date'] = date
            iv_list.append(data)

        iv_df = pd.concat(iv_list)
        iv_df['ticker'] = iv_df['bond_code'].apply(lambda x: x.split('.')[0])
        iv_df['iv'] = iv_df['iv'].round(4)
        self.iv_df = iv_df[['trade_date', 'ticker', 'iv']]

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.iv_df
            sql_script = "delete from {} where trade_date >= {} and trade_date <= {}".format(
                self.table_name, self.start_date, self.end_date)
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table cb_market_iv(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(20),
                iv decimal(7, 4)) 
            """
            create_table(self.table_name, sql_script)
            data = self.iv_df
            WriteToDB().write_to_db(data, self.table_name)


class CBMarketPrice:
    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = "cb_market_price"
        self._load_data()

    def _load_data(self):
        trading_day_list = get_trading_day_list(self.start_date, self.end_date)
        # data set
        res = w.wset("cbissue", "startdate=2012-01-01;enddate={}".format(datetime.now().strftime('%Y-%m-%d')))
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("Fetching cbissue data error!")
        else:
            data = pd.DataFrame(res.Data, index=res.Fields, columns=res.Codes).T
        # preprocess
        issue_data = data[data['issue_type'].isin(['优先配售和上网定价', '优先配售,网上定价和网下配售'])]
        issue_data = issue_data[['bond_code', 'bond_name', 'listing_date', 'interest_end_date']].dropna()
        issue_data['listing_date'] = issue_data['listing_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        issue_data['interest_end_date'] = issue_data['interest_end_date'].apply(
            lambda x: datetime.strftime(x, '%Y%m%d'))
        # price data
        price_list = []
        for date in tqdm(trading_day_list):
            exist_cb = issue_data[(issue_data['listing_date'] < date) & (issue_data['interest_end_date'] > date)]
            cb_code_list = exist_cb['bond_code'].unique()
            # convprice
            res = w.wss(','.join(cb_code_list), 'convpremiumratio,convprice,underlyingcode', "tradeDate={}".format(date))
            if res.ErrorCode != 0:
                data = pd.DataFrame()
                print("fetch convprice data error: trade_date = {}".format(date))
            else:
                data = pd.DataFrame(data=res.Data, index=res.Fields, columns=res.Codes).T
            data.columns = ['premium', 'convprice', 'sec_code']
            data.index.name = 'cb_code'
            conv_price = data.reset_index().dropna()
            conv_price['ticker'] = conv_price['sec_code'].apply(lambda x: x.split('.')[0])
            # close price
            sql_script = "SELECT SYMBOL, TDATE, TCLOSE FROM finchina.CHDQUOTE WHERE" \
                         " TDATE = {}".format(date)
            data = pd.DataFrame(hbs.db_data_query("readonly", sql_script, page_size=5000)['data']).rename(
                columns={"SYMBOL": "ticker", "TCLOSE": "stock_price"})
            # merge
            data = pd.merge(conv_price, data[['ticker', 'stock_price']], on='ticker')
            data['trade_date'] = date
            price_list.append(data)

        price_df = pd.concat(price_list)
        price_df['ticker'] = price_df['cb_code'].apply(lambda x: x.split('.')[0])
        self.price_df = price_df[['trade_date', 'ticker', 'premium', 'convprice', 'stock_price']]

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.price_df
            sql_script = "delete from {} where trade_date >= {} and trade_date <= {}".format(
                self.table_name, self.start_date, self.end_date)
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table cb_market_price(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(20),
                premium decimal(6, 2),
                convprice decimal(6, 2),
                stock_price decimal(6, 2)) 
            """
            create_table(self.table_name, sql_script)
            data = self.price_df
            WriteToDB().write_to_db(data, self.table_name)


class OptionIV:
    def __init__(self, start_date, end_date, rolling_window=20, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.rolling_window = rolling_window
        self.is_increment = is_increment
        self.table_name = "etf_market_iv"
        self._load_data()

    def _load_data(self):
        # IV
        res = w.wsd("SH_5100501MIV.WI,SH_5103001MIV.WI,SZ_1599191MIV.WI,CFE_0003001MIV.WI", "close",
                    self.start_date, self.end_date, "")
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("fetch implied volatility data error: start_date = {}, end_date = {}".format(
                self.start_date, self.end_date))
        elif len(res.Data) == 1:
            date_list = [datetime.strftime(x, '%Y%m%d') for x in res.Times]
            data = pd.DataFrame(res.Data[0], index=res.Codes, columns=date_list).T.sort_index()
        else:
            date_list = [datetime.strftime(x, '%Y%m%d') for x in res.Times]
            data = pd.DataFrame(res.Data, index=res.Codes, columns=date_list).T.sort_index()

        data['trade_date'] = data.index
        data = data.reset_index(drop=True)
        iv_df = data
        iv_df.columns = [x.split('.')[0] for x in iv_df.columns]
        # HV
        start_dt = datetime.strptime(self.start_date, '%Y%m%d')
        pre_date = (start_dt - timedelta(days=150)).strftime('%Y%m%d')
        res = w.wsd("510050.SH,510300.SH,159919.SZ,000300.SH", "close", pre_date, self.end_date, "")
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("fetch close data error: start_date = {}, end_date = {}".format(pre_date, self.end_date))
        elif len(res.Data) == 1:
            date_list = [datetime.strftime(x, '%Y%m%d') for x in res.Times]
            data = pd.DataFrame(res.Data[0], index=res.Codes, columns=date_list).T.sort_index()
        else:
            date_list = [datetime.strftime(x, '%Y%m%d') for x in res.Times]
            data = pd.DataFrame(res.Data, index=res.Codes, columns=date_list).T.sort_index()

        return_df = data.pct_change().dropna()
        hv_df = return_df.rolling(self.rolling_window).std().loc[self.start_date:].dropna() * np.sqrt(252)
        hv_df.columns = [x.replace('.', '_') for x in hv_df.columns]
        hv_df['trade_date'] = hv_df.index
        hv_df = hv_df.reset_index(drop=True)

        index_df = data.loc[self.start_date:]
        index_df.columns = [x.split('.')[0] + '_ix' for x in index_df.columns]
        index_df['trade_date'] = index_df.index
        index_df = index_df.reset_index(drop=True)

        assert (iv_df.shape == hv_df.shape)
        assert (iv_df.shape == index_df.shape)

        self.data = iv_df.merge(hv_df, on='trade_date').merge(index_df, on='trade_date')

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.data
            sql_script = "delete from {} where trade_date >= {} and trade_date <= {}".format(
                self.table_name, self.start_date, self.end_date)
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table etf_market_iv(
                id int auto_increment primary key,
                trade_date date not null,
                SH_5100501MIV decimal(5, 4),
                SH_5103001MIV decimal(5, 4),
                SZ_1599191MIV decimal(5, 4),
                CFE_0003001MIV decimal(5, 4),
                510050_SH decimal(5, 4),
                510300_SH decimal(5, 4),
                159919_SZ decimal(5, 4),
                000300_SH decimal(5, 4),
                510050_ix decimal(8, 4),
                510300_ix decimal(8, 4),
                159919_ix decimal(8, 4),
                000300_ix decimal(8, 4)) 
            """
            create_table(self.table_name, sql_script)
            data = self.data
            WriteToDB().write_to_db(data, self.table_name)


if __name__ == '__main__':
    # CBMarketIV('20180101', '20201231').get_construct_result()
    # CBMarketPrice('20190101', '20191231', is_increment=1).get_construct_result()
    OptionIV('20220614', '20220614', is_increment=1).get_construct_result()