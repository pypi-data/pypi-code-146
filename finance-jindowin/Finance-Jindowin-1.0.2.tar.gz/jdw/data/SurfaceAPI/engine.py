# -*- coding: utf-8 -*-
import six, os
from jdw.kdutils.singleton import Singleton
from jdw.data.DataAPI.db.fetch_engine import FetchEngine


@six.add_metaclass(Singleton)
class FetchKDEngine(FetchEngine):

    def __init__(self):
        super(FetchKDEngine, self).__init__('kd', os.environ['DB_URL'])

    def client(self):
        return self._engine.sql_engine()

    def table_model(self, name):
        return self._base.classes[name]
