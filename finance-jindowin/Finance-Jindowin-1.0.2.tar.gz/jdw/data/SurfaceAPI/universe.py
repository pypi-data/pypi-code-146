# -*- coding: utf-8 -*-
import abc
import pandas as pd
from sqlalchemy import select, and_
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class BaseUniverse(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def condition(self):
        pass

    @classmethod
    def load(cls, u_desc: dict):
        pass


class Universe(BaseUniverse):

    def __init__(self, u_name, table_name=None):
        self._engine = FetchKDEngine()
        self.u_name = u_name.lower()
        self._table_name = table_name
        self._table_model = self._engine.table_model(self._table_name)

    def condition(self):
        return getattr(self._table_model, self.u_name) == 1 and getattr(
            self._table_model, 'flag') == 1

    def query(self, start_date: str = None, end_date: str = None, dates=None):
        query = select([
            self._table_model.trade_date, self._table_model.code
        ]).where(self._query_statements(start_date, end_date, dates)).order_by(
            self._table_model.trade_date, self._table_model.code)
        return pd.read_sql(query, self._engine.client())

    def _query_statements(self,
                          start_date: str = None,
                          end_date: str = None,
                          dates=None):
        return and_(
            self.condition(),
            self._table_model.trade_date.in_(dates) if dates else
            self._table_model.trade_date.between(start_date, end_date))

    def save(self):
        return dict(u_type=self.__class__.__name__, u_name=self.u_name)

    def __eq__(self, other):
        return self.u_name == other.u_name


class FutUniverse(Universe):

    def __init__(self, u_name, table_name=None):
        super(FutUniverse,
              self).__init__(u_name,
                             table_name=('fut_derived_universe' if
                                         table_name is None else table_name))


class StkUniverse(Universe):

    def __init__(self, u_name, table_name=None):
        super(StkUniverse,
              self).__init__(u_name,
                             table_name=('stk_derived_universe' if
                                         table_name is None else table_name))