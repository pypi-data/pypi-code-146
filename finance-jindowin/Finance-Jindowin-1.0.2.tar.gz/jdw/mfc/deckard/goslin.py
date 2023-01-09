import datetime
from pymongo import InsertOne, DeleteOne
from jdw.kdutils.data.mongodb import MongoDBManager


class Goslin(object):

    def __init__(self, uri, name='goslin'):
        self.name = name
        self._mongo_client = MongoDBManager(uri="mongodb://" + uri)
        self._codes_pools = [
            'RB', 'I', 'JM', 'HC', 'J', 'SF', 'SM', 'TA', 'MA', 'PF', 'EG',
            'SA', 'L', 'PP', 'V', 'FU', 'BU', 'A', 'Y', 'M', 'OI', 'P', 'C',
            'CS', 'SR', 'CF', 'JD', 'LH', 'RU', 'ZN', 'NI', 'AL', 'CU', 'PB'
        ]

    def create_positions(self, name='CTA_Strategy_Positions', codes=None):
        codes = self._codes_pools if codes is None else codes
        db = self._mongo_client[name]
        for code in codes:
            coll = db['Positions' + code]
            mydict = {}
            coll.insert_one(mydict)

    def create_trader(self,
                      account,
                      listeners,
                      name='CTA_Strategy_Trader',
                      codes=None):
        codes = self._codes_pools if codes is None else codes
        db = self._mongo_client[name]
        for code in codes:
            coll = db['Trader' + code]
            insert_request = [
                InsertOne({
                    'indet':
                    code.lower() + '_1001',
                    "accountIds":
                    listeners,
                    'lastUpdate':
                    datetime.datetime.now().strftime('%Y%m%d'),
                    'position':
                    0,
                    'lastTrader':
                    datetime.datetime.now().strftime('%Y%m%d'),
                    'orderList': {},
                    'openTarget':
                    0,
                    'isRefresh':
                    1,
                    'lastRefresh':
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                })
            ]
            _ = coll.bulk_write(insert_request,
                                bypass_document_validation=True)
