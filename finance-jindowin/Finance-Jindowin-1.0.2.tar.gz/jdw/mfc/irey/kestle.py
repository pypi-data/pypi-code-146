import os, copy, datetime, warnings
import numpy as np
import pandas as pd
from pymongo import InsertOne, DeleteOne
try:
    from ultron.tradingday import *
except ImportError:
    warnings.warn(
        "If you need high-performance computing, please install Finance-Ultron.First make sure that the C++ compilation environment has been installed"
    )
from jdw.mfc import IREY_URL, IREY_COLL
from jdw.kdutils.data.mongodb import MongoDBManager
from jdw.kdutils.logger import kd_logger
from jdw.data.DataAPI.mg import FetchEngine, FutBasic
import jdw.mfc.experimental.DataAPI.mg as ExperimentalAPI
from jdw.kdutils.file_utils import load_df_csv


class Kestle(object):

    class Base(object):

        def __init__(self):
            pass

        def calc_trade(self, interval=1):
            current_time = datetime.datetime.now()
            try:
                last_date = advanceDateByCalendar('china.sse',
                                                  current_time.date(),
                                                  '-{0}b'.format(interval))
            except:
                last_date = current_time - datetime.timedelta(days=interval)
            return last_date

        def load_positions(self, file_name):
            raise NotImplementedError

        def fetch_positions(self, engine, account, password, plt):
            account_info = ExperimentalAPI.Account(engine).operation(
                account_id=account,
                password=password,
                plt=plt,
                columns=['account_id', 'plt'],
                method='fetch')

            if len(account_info) == 0:
                raise ValueError('Account not found')

            postions = ExperimentalAPI.Positions(engine).operation(
                account_id=[account], trade_date=None, method='fetch')
            return postions

    class Fast(Base):

        def __init__(self):
            pass

        def load_positions(self, file_name):
            positions = load_df_csv(file_name, encoding='gbk')
            positions = positions.rename(columns={
                u'合约代码': 'symbol',
                u'总仓': 'act',
                u'买卖': 'dicrtion'
            })
            positions = positions[['symbol', 'act', 'dicrtion']]
            positions['dicrtion'] = np.where(positions['dicrtion'] == u'卖', -1,
                                             1)
            positions['position'] = positions['act'] * positions['dicrtion']
            positions = positions.drop(['act', 'dicrtion'], axis=1)
            return positions

    class Rohon(Base):

        def __init__(self):
            pass

        def load_positions(self, file_name):
            positions = load_df_csv(file_name, encoding='gbk')
            positions = positions.rename(columns={
                u'合约': 'symbol',
                u'总持仓': 'act',
                u'买卖': 'dicrtion'
            })
            positions = positions[['symbol', 'act', 'dicrtion']]
            positions['dicrtion'] = np.where(positions['dicrtion'] == u'卖', -1,
                                             1)
            positions['position'] = positions['act'] * positions['dicrtion']
            positions = positions.drop(['act', 'dicrtion'], axis=1)
            return positions

    def __init__(self, name='kn'):
        self._fetch_engine = FetchEngine.create_engine(name='kn')
        self._axtell_engine = ExperimentalAPI.OperatorEngine.create_engine(
            name='atl')
        self._mongo_client = MongoDBManager(uri=IREY_URL)

    def create_engine(self, plt):
        if plt == 'rohon':
            return Kestle.Rohon()
        elif plt == 'fast':
            return Kestle.Fast()
        else:
            return Kestle.Base()

    def _future_basic(self, codes):
        basic_info = FutBasic(self._fetch_engine).result(
            codes=codes, columns=['code', 'contractObject', 'exchangeCD'])
        basic_info = basic_info.drop_duplicates(
            subset=['code', 'contractObject'])
        basic_info = basic_info.rename(columns={
            'code': 'symbol',
            'exchangeCD': 'exchange',
            'contractObject': 'code'
        })
        return basic_info

    def _transformer(self, positions, basic_info):

        def exchange_mapping(x):
            mapping = {'XDCE': 'DCE', 'XSGE': 'SHFE', 'XZCE': 'CZCE'}
            return np.nan if x not in mapping else mapping[x]

        data = positions.merge(basic_info, on=['symbol'], how='outer')
        data['exchange'] = data['exchange'].apply(
            lambda x: exchange_mapping(x))
        data['vt_symbol'] = data['symbol'] + '.' + data['exchange']
        return data.dropna(subset=['exchange']).drop(['exchange'], axis=1)

    def file(self, account, filename=None, plt='rohon'):
        engine = self.create_engine(plt)
        positions = engine.load_positions(filename)
        basic_info = self._future_basic(positions['symbol'].unique().tolist())
        positions = self._transformer(copy.deepcopy(positions), basic_info)
        positions['account_id'] = account
        positions['last_update'] = int(engine.calc_trade().strftime('%Y%m%d'))
        positions['last_trade'] = engine.calc_trade().strftime('%Y%m%d')
        positions['order_list'] = positions['account_id'].apply(lambda x: {})
        positions['open_target'] = 0.0
        return positions

    def mongo(self, account, password, plt):
        engine = self.create_engine(plt)
        positions = engine.fetch_positions(engine=self._axtell_engine,
                                           account=account,
                                           password=password,
                                           plt=plt)
        positions = positions[[
            'account_id', 'symbol', 'exchange', 'vt_symbol', 'volume',
            'direction', 'trade_date'
        ]]
        positions['position'] = positions['volume'] * positions['direction']
        positions['last_update'] = positions['trade_date']
        positions['last_trade'] = positions['trade_date']
        positions['order_list'] = positions['account_id'].apply(lambda x: {})
        positions['open_target'] = 0.0
        positions = positions.drop(['volume', 'direction', 'trade_date'],
                                   axis=1)
        target_positions = positions.set_index([
            'vt_symbol'
        ]).groupby(level=['vt_symbol']).apply(lambda x: x['position'].sum())
        target_positions.name = 'position'
        target_positions = target_positions.reset_index()
        positions = target_positions.merge(positions.drop_duplicates(
            subset=['symbol', 'vt_symbol']).drop(['position'], axis=1),
                                           on=['vt_symbol'],
                                           how='left').reset_index(drop=True)
        return positions

    def save(self, account_id, positions):
        delete_request = [
            DeleteOne({
                'account_id': account_id,
                'vt_symbol': pos['vt_symbol']
            }) for pos in positions.to_dict('records')
        ]

        _ = self._mongo_client[IREY_COLL][str(account_id)].bulk_write(
            delete_request, bypass_document_validation=True)

        insert_request = [
            InsertOne({
                'account_id': pos['account_id'],
                'symbol': pos['symbol'],
                'vt_symbol': pos['vt_symbol'],
                'last_update': pos['last_update'],
                'position': pos['position'],
                'last_trade': pos['last_trade'],
                'order_list': pos['order_list'],
                'open_target': pos['open_target']
            }) for pos in positions.to_dict('records')
        ]
        _ = self._mongo_client[IREY_COLL][str(account_id)].bulk_write(
            insert_request, bypass_document_validation=True)

    def update(self, account, password=None, filename=None, plt='rohon'):
        if filename is not None:
            positions = self.file(account, filename, plt)
        elif password is not None:
            positions = self.mongo(account, password, plt)
        else:
            positions = pd.DataFrame()
        self.save(account, positions)
