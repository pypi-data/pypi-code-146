#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SqlBuilder(object):

    INSERT_SQL = 1
    UPDATE_SQL = 2
    DELETE_SQL = 3
    SELECT_SQL = 4

    def __init__(self, table_name):
        self._tablename = table_name
        self._data_dic: dict = {}
        self._where_dic: dict = {}
        self._where_sql = ''
        self._where_sql_params: tuple = ()
        self._select_fields: tuple = ()

    def new_pool(self):
        self._data_dic = {}
        self._where_dic = {}
        self._where_sql = ''
        self._where_sql_params = ()
        self._select_fields = ()

    def data(self, data: dict):
        if isinstance(data, list) or isinstance(data, set) or isinstance(data, tuple):
            data = dict(data)
        self._data_dic = data

    def add_data(self, data: dict):
        self._data_dic = SqlBuilder._merge_dicts(self._data_dic, data)

    def put_data(self, key, value):
        self._data_dic[key] = value

    def where(self, datas: dict):
        self.add_where(datas)
        #self._where_dic = data

    def put_where(self, key, value):
        self.add_where_equals(key, value)
        #self._where_dic[key] = value

    def add_where(self, datas: dict):
        if isinstance(datas, list) or isinstance(datas, set) or isinstance(datas, tuple):
            datas = dict(datas)
        for key in datas.keys():
            self.add_where_equals(key, datas.get(key))
        # self._where_dic = SqlBuilder._merge_dicts(self._where_dic, data)

    def add_where_in(self, key, data, is_match=True):
        if not data or len(data) <= 0:
            raise RuntimeError('data is Null')
        if is_match:
            self._add_sql('{key} is in ({instr}) '.format(key=key, instr=','.join(['%s'] * len(data))), data)
        else:
            self._add_sql('{key} is not ({instr}) '.format(key=key, instr=','.join(['%s'] * len(data))), data)

    def add_where_isnull(self, key, is_match=True):
        if is_match:
            self._add_sql('{key} is NULL '.format(key=key))
        else:
            self._add_sql('{key} is not NULL '.format(key=key))

    def add_where_like(self, key, data, is_match=True):
        if not data or data is None:
            raise RuntimeError('data is Null')
        if is_match:
            self._add_sql('{key} like %s '.format(key=key), data)
        else:
            self._add_sql('{key} not like %s '.format(key=key), data)

    def add_where_between(self, key, value1=None, value2=None, is_match=True):
        if is_match:
            if value1 is None:
                self._add_sql('{key} < %s '.format(key=key), (value1,))
            elif value1 is None:
                self._add_sql('{key} > %s '.format(key=key), (value1,))
            else:
                self._add_sql('{key} BETWEEN %s AND %s '.format(key=key), (value1, value2))
        else:
            self._add_sql('{key} not BETWEEN %s AND %s '.format(key=key), (value1, value2))

    def add_where_equals(self, key, data=None, equals=True):
        if equals:
            self._add_sql('{key} = %s '.format(key=key), data)
        else:
            self._add_sql('{key} <> %s '.format(key=key), data)

    def add_where_greater_than(self, key, data, is_equal=False):
        if not data or data is None:
            raise RuntimeError('data is Null')
        if is_equal:
            self._add_sql('{key} >= %s '.format(key=key), data)
        else:
            self._add_sql('{key} > %s '.format(key=key), data)

    def add_where_less_than(self, key, data, is_equal=False):
        if not data or data is None:
            raise RuntimeError('data is Null')
        if is_equal:
            self._add_sql('{key} <= %s '.format(key=key), data)
        else:
            self._add_sql('{key} < %s '.format(key=key), data)

    def add_where_sql(self, sql, data=()):
        self._add_sql(sql, data)

    def get(self, key) -> dict:
        if key in self._data_dic:
            return self._data_dic[key]
        return None

    def _add_sql(self, sql_str, data=()):
        if sql_str is not None:
            if self._where_sql != '':
                self._where_sql += " AND "
            self._where_sql += sql_str
        if data is not None:
            if isinstance(data, tuple):
                self._where_sql_params = self._where_sql_params + data
            elif isinstance(data, list):
                self._where_sql_params = self._where_sql_params + tuple(data)
            else:
                self._where_sql_params = self._where_sql_params + (data,)

    @staticmethod
    def _merge_dicts(x, y) -> dict:
        return {**x, **y}

    @property
    def tablename(self) -> str:
        return self._tablename

    def _get_wsql(self) -> str:
        if len(self._where_dic) <= 0 and self._where_sql == '':
            return ''
        if len(self._where_dic) > 0 and self._where_sql != '':
            return 'WHERE {wsql} AND {wsql2} '.format(
                wsql='AND '.join(["{key} = %s".format(key=key) for key in self._where_dic]),
                wsql2=self._where_sql
            )
        elif len(self._where_dic) > 0:
            return 'WHERE {wsql} '.format(
                wsql='AND '.join(["{key} = %s".format(key=key) for key in self._where_dic]),
            )
        else:
            return 'WHERE {wsql2}'.format(wsql2=self._where_sql)
        return sql_where

    def select_field(self, field=None):
        if isinstance(field, tuple):
            self._select_fields = self._select_fields + field
        elif isinstance(field, set):
            self._select_fields = self._select_fields + tuple(list(set(field)))
        elif isinstance(field, list):
            self._select_fields = self._select_fields + tuple(field)
        else:
            self._select_fields = self._select_fields + (field,)

    def get_db_type(self):
        from pywkdb.db.db_mssql import MsSQLDb
        from pywkdb.db.db_mysql import MySQLDb
        from pywkdb.db.db_sqlite import SqliteDb
        db_type = 1
        try:
            if self._sql_db:
                if isinstance(self._sql_db, MySQLDb) or isinstance(self._sql_db, SqliteDb):
                    db_type = 1
                elif isinstance(self._sql_db, MsSQLDb):
                    db_type = 2
        except Exception as e:
            db_type = 1
        return db_type

    def _get_select_sql(self, limit=None, row_num=None) -> (str, tuple):
        if self._select_fields is None or len(self._select_fields) <= 0:
            self._select_fields = ('*',)
        sql = 'SELECT {fields_str} FROM {tables} {whersql}'.format(
            fields_str=','.join(["{key}".format(key=key) for key in self._select_fields]),
            tables=self._tablename,
            whersql=self._get_wsql()
        )
        if limit:
            sql = '{sql} limit {limit} '.format(sql=sql,limit=limit)
        if row_num:
            if limit:
                sql = '{sql} , {row_num} '.format(sql=sql,row_num=row_num)
            else:
                sql = '{sql} limit {limit}, {row_num} '.format(sql=sql,limit=limit,row_num = row_num)
        sql_params = tuple(self._data_dic.values()) + tuple(self._where_dic.values()) + self._where_sql_params
        return sql, sql_params

    def _get_insert_sql(self, allow_null=False) -> (str, tuple):
        if self._data_dic is None or len(self._data_dic) <= 0:
            raise RuntimeError('Data dic is Null')
        if allow_null:
            del_keys = ()
            for key in self._data_dic.keys():
                if self._data_dic.get(key) is None:
                    del_keys = del_keys + (key,)
                    #self._data_dic.pop(key)
            for key in del_keys:
                self._data_dic.pop(key)
        sql = 'INSERT INTO {tables} ({keys}) VALUES({values})'.format(
            tables=self._tablename,
            keys=','.join(self._data_dic.keys()),
            values=','.join(['%s'] * len(self._data_dic))
        )
        sql_params = tuple(self._data_dic.values())
        return sql, sql_params

    def _get_update_sql(self) -> (str, tuple):
        if self._data_dic is None or len(self._data_dic) <= 0:
            raise RuntimeError('Data dic is Null')
        sql = 'UPDATE {tables} SET {values} {whersql}'.format(
            tables=self._tablename,
            values=','.join(["{key} = %s".format(key=key) for key in self._data_dic]),
            whersql=self._get_wsql()
        )
        sql_params = tuple(self._data_dic.values()) + tuple(self._where_dic.values()) + self._where_sql_params
        return sql, sql_params

    def _get_delete_sql(self) -> (str, tuple):
        sql = 'DELETE TABLE {tables} {whersql}'.format(
            tables=self._tablename,
            values=','.join(["{key} = %s".format(key=key) for key in self._data_dic]),
            whersql=self._get_wsql()
        )
        sql_params = tuple(self._where_dic.values()) + self._where_sql_params
        return sql, sql_params

    def build(self, sql_type=SELECT_SQL, limit=None, row_num=None) -> (str, tuple):
        if sql_type == self.INSERT_SQL:
            return self._get_insert_sql()
        elif sql_type == self.UPDATE_SQL:
            return self._get_update_sql()
        elif sql_type == self.DELETE_SQL:
            return self._get_delete_sql()
        elif sql_type == self.SELECT_SQL:
            return self._get_select_sql(limit, row_num)


if __name__ == '__main__':
    pass
