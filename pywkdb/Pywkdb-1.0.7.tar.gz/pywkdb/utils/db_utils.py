#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pywkmisc import get_config
from pywkdb.utils.sql_builder import SqlBuilder
from pywkdb.utils.db_base import DbBase
from pywkdb.utils.url_parse import UrlParse
import pandas as pd


class DBUtils(SqlBuilder):

    def __init__(self, table_name, db_base: DbBase = None, db_str: str = None):
        self._sql_db = None
        super(DBUtils, self).__init__(table_name)
        if db_base is not None:
            self._sql_db = db_base

        if db_base is None and db_str is not None:
            self._sql_db = DbBase(db_str)

    def insert(self, sql, params=None):
        if isinstance(sql, tuple):
            sql, params = sql
        return self._sql_db.insert(sql, params)

    def execute(self, sql, params=None) -> int:
        if isinstance(sql, tuple):
            sql, params = sql
        return self._sql_db.update(sql, params)

    def select_sql(self, sql, params=None) -> (tuple, list):
        if isinstance(sql, tuple):
            sql, params = sql
        return self._sql_db.select(sql, params)

    def select_sql_list(self, sql, params=None) -> list:
        if isinstance(sql, tuple):
            sql, params = sql
        return self._sql_db.select_data(sql, params)

    def select_sql_frame_data(self, sql, params=None) -> pd.DataFrame:
        if isinstance(sql, tuple):
            sql, params = sql
        return self._sql_db.select_frame_data(sql, params)

    def save(self, allow_null=False):
        return self.insert(self._get_insert_sql(allow_null))

    def update(self) -> int:
        return self.execute(self.build(self.UPDATE_SQL))

    def delete(self) -> int:
        return self.execute(self.build(self.DELETE_SQL))

    def select(self, limit=None, row_num=None) -> (tuple, list):
        return self.select_sql(self.build(self.SELECT_SQL, limit, row_num))

    def select_list(self, limit=None, row_num=None) -> list:
        return self.select_sql_list(self.build(self.SELECT_SQL, limit, row_num))

    def select_frame_data(self, limit=None, row_num=None) -> pd.DataFrame:
        return self.select_sql_frame_data(self.build(self.SELECT_SQL, limit, row_num))

    def __del__(self):
        if self._sql_db is not None:
            self._sql_db._close()
            del self._sql_db

    @staticmethod
    def get_db(db_str=None):
        if db_str is None:
            db_str = get_config('db')
        """
        mysql://root:123456@127.0.0.1:3306/dbname?charset=utf-8
        mssql://sa:123456@127.0.0.1:1443/dbname?charset=utf-8
        sqlite://:/C:/work/python/data/dbfile.db
        :param db_str:
        :return:
        """
        url_parse = UrlParse(db_str)
        db_base = None
        if url_parse.scheme == 'mysql':
            from pywkdb.db.db_mysql import MySQLDb
            db_base = MySQLDb(db_str)
        elif url_parse.scheme == 'mssql':
            from pywkdb.db.db_mssql import MsSQLDb
            db_base = MsSQLDb(db_str)
        elif url_parse.scheme == 'oracle':
            from pywkdb.db.db_oraclel import OracleDb
            db_base = OracleDb(db_str)
        elif url_parse.scheme == 'sqlite':
            from pywkdb.db.db_sqlite import SqliteDb
            db_base = SqliteDb(db_str)
        db_base.connect(url_parse)
        return db_base


if __name__ == '__main__':
    pass
