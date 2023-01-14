import os

import dateutil
from .mongodb_queries._search_transfers import Mixin as _search_transfers
from .mongodb_queries._subscriptions import Mixin as _subscriptions
from .mongodb_queries._baker_distributions import Mixin as _distributions
from .mongodb_queries._store_block import Mixin as _store_block
from .mongodb_queries._apy_calculations import Mixin as _apy_calculations

from pymongo import MongoClient
from rich.console import Console
from sharingiscaring.tooter import Tooter, TooterType, TooterChannel
from sharingiscaring.client import ConcordiumClient
console = Console()

class TestMongo:
    def __init__(self):
        pass

class MongoDB(
    _search_transfers,
    _subscriptions,
    _distributions,
    _store_block,
    _apy_calculations
    ):

    def __init__(self, mongo_config, tooter: Tooter):
        self.tooter: Tooter           = tooter
        
        try:
            con = MongoClient(f'mongodb://admin:{mongo_config["MONGODB_PASSWORD"]}@{mongo_config["MONGO_IP"]}:{mongo_config["MONGO_PORT"]}')
            self.db                                     = con.concordium
            self.collection_blocks                      = self.db['blocks']
            self.collection_transactions                = self.db['transactions']
            self.collection_messages                    = self.db['bot_messages']
            self.collection_accounts_involved           = self.db['accounts_involved']
            self.collection_paydays                     = self.db['paydays']
            self.collection_paydays_performance         = self.db['paydays_performance']
            self.collection_paydays_rewards             = self.db['paydays_rewards']
            self.collection_paydays_apy                 = self.db['paydays_apy']
            self.collection_paydays_apy_intermediate    = self.db['paydays_apy_intermediate']

            self.collection_involved_accounts_all       = self.db['involved_accounts_all']
            self.collection_involved_accounts_transfer  = self.db['involved_accounts_transfer']
            self.collection_involved_contracts          = self.db['involved_contracts']
            self.collection_nightly_accounts            = self.db['nightly_accounts']
            self.collection_helpers                     = self.db['helpers']
            # self.collection_transaction_python          = self.db['transaction_python']

            console.log(con.server_info()['version'])
        except Exception as e:
            print (e)
            tooter.send(channel=TooterChannel.NOTIFIER, message=f'BOT ERROR! Cannot connect to MongoDB, with error: {e}', notifier_type=TooterType.MONGODB_ERROR)
            