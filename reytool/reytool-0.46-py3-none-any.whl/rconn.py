# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's database connect type
"""


from typing import Any, List, Dict, Iterable, Optional, Literal, Union
import re
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import LegacyCursorResult
from sqlalchemy.engine.result import Result
from sqlalchemy.sql.elements import TextClause
from types import MethodType

from .rbasic import get_first_notnull, is_iterable, error
from .rtext import rprint
from .rtime import time_to_str


def fetch_table(data: Union[LegacyCursorResult, Iterable], fields: Optional[Iterable] = None) -> List[Dict]:
        """
        Fetch SQL result to List[Dict[str, Any]] table format.
        """

        if type(data) == LegacyCursorResult:
            if fields == None:
                fields = data.keys()
            table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
        else:
            data_fields_len = max([len(row) for row in data])
            if fields == None:
                data = [list(row) + [None] * (data_fields_len - len(row)) for row in data]
                field_range = range(data_fields_len)
                table = [dict(zip(field_range, [time_to_str(val) for val in row])) for row in data]
            else:
                field_len = len(fields)
                if data_fields_len > field_len:
                    fields += list(range(data_fields_len - field_len))
                data = [list(row) + [None] * (field_len - len(row)) for row in data]
                table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
        return table

def fetch_df(data: Union[LegacyCursorResult, Iterable], fields: Optional[Iterable] = None) -> DataFrame:
        """
        Fetch SQL result to DataFrame object.
        """

        if type(data) == LegacyCursorResult:
            if fields == None:
                fields = data.keys()
            else:
                fields_len = len(data.keys())
                fields = fields[:fields_len]
            df = DataFrame(data, columns=fields)
        else:
            if fields == None:
                df = DataFrame(data)
            else:
                data_fields_len = max([len(row) for row in data])
                field_len = len(fields)
                if data_fields_len > field_len:
                    fields += list(range(data_fields_len - field_len))
                data = [list(row) + [None] * (field_len - len(row)) for row in data]
                df = DataFrame(data, columns=fields)
        return df

def fetch_sql(data: Union[LegacyCursorResult, Iterable], fields: Optional[Iterable] = None) -> str:
    """
    Fetch SQL result to SQL sentence.
    """

    if type(data) == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] for row in data]
    else:
        if fields == None:
            data_fields_len = max([len(row) for row in data])
            fields = ["field_%d" % i for i in range(data_fields_len)]
        sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] + ["NULL"] * (data_fields_len - len(row)) for row in data]
    sqls[0] = "SELECT " + ",".join(["%s AS `%s`" % (val, fie) for val, fie in list(zip(sqls[0], fields))])
    sqls[1:] = ["SELECT " + ",".join(sql) for sql in sqls[1:]]
    sql = " UNION ALL ".join(sqls)
    return sql

def monkey_patch_more_fetch() -> None:
    """
    Add more methods to object Result of sqlalchemy package.
    """

    # Fetch SQL result to list[dict{field: value,},] table format.
    Result.fetch_table = fetch_table

    # Fetch SQL result to DataFrame object.
    Result.fetch_df = fetch_df

    # Fetch SQL result to DataFrame object.
    Result.fetch_sql = fetch_sql

monkey_patch_more_fetch()

class RConn(object):
    """
    Rey's database connect type.
    """

    # Values to be converted to None.
    none_values: List = ["", " ", b"", [], (), {}, set()]
    
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        only_once: bool = True,
        conn: Optional[Union[Engine, Connection]] = None
    ) -> None:
        """
        Set database connect parameters.
        """

        if type(conn) == Connection:
            conn = conn.engine
        if type(conn) == Engine:
            user = get_first_notnull(user, conn.url.username)
            password = get_first_notnull(password, conn.url.password)
            host = get_first_notnull(host, conn.url.host)
            port = get_first_notnull(port, conn.url.port)
            database = get_first_notnull(database, conn.url.database)
            charset = get_first_notnull(charset, conn.url.query.get("charset"))
            conn = conn.connect(close_with_result=only_once)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.charset = charset
        self.only_once = only_once
        self.conn = conn
        self.fetch_table = fetch_table
        self.fetch_df = fetch_df
        self.fetch_sql = fetch_sql
    
    def create_conn(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        only_once: bool = True
    ) -> Connection:
        """
        Get database connect engine.
        """

        if self.conn and [user, password, host, port, database, charset] == [None] * 6:
            return self.conn

        user: str = get_first_notnull(user, self.user, default="error")
        password: str = get_first_notnull(password, self.password, default="error")
        host: str = get_first_notnull(host, self.host, default="error")
        port: Union[str, int] = get_first_notnull(port, self.port, default="error")
        database: str = get_first_notnull(database, self.database, default="error")
        charset: str = get_first_notnull(charset, self.charset, default="utf8")
        only_once: str = get_first_notnull(only_once, self.only_once, default=True)
 
        try:
            url = f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        except ModuleNotFoundError:
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        conn = engine.connect(close_with_result=only_once)
        if not self.conn and not only_once:
            self.conn = conn
        return conn
    
    def fill_sql_none(
        self,
        sql: Union[str, TextClause],
        parms: Union[Dict, List[Dict]],
        fill_field: bool = True,
        none_values: List = none_values
    ) -> Union[Dict, List[Dict]]:
        """
        Fill missing parameters according to contents of sqlClause object of sqlalchemy module.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.

        parms : Parameters set for filling sqlalchemy.text.

        fill_field : Whether fill missing fields.

        none_values : Values to be converted to None.

        Returns
        -------
        Filled parameters.
            - When parameter parms is Dict, then return Dict.
            - When parameter parms is List[Dict], then return List[Dict].
        """

        if type(sql) == TextClause:
            sql = sql.text
        pattern = "(?<!\\\):(\w+)"
        sql_keys = re.findall(pattern, sql)
        if type(parms) == dict:
            for key in sql_keys:
                if fill_field:
                    val = parms.get(key)
                else:
                    val = parms[key]
                if val in none_values:
                    val = None
                parms[key] = val
        else:
            for parm in parms:
                for key in sql_keys:
                    if fill_field:
                        val = parm.get(key)
                    else:
                        val = parm[key]
                    if val in none_values:
                        val = None
                    parm[key] = val
        return parms

    def execute(
        self,
        sql: str,
        parms: Optional[Union[List, Dict]] = None,
        database: Optional[str] = None,
        fill_field: bool = True,
        none_values: List = none_values,
        only_once: bool = True,
        **kw_parms: Any
    ) -> LegacyCursorResult:
        """
        Execute SQL and add methods fetch_table and fetch_df.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format.

        parms : Parameters set for filling sqlalchemy.text.

        database : Database name.

        fill_field : Whether fill missing fields.

        none_values : Values to be converted to None.

        only_once : Whether the database connect engine is one-time (i.e. real time creation).

        **kw_parms : Keyword parameters for filling sqlalchemy.text.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        only_once = get_first_notnull(only_once, self.only_once, default=True)

        if self.conn == None:
            self.conn = self.create_conn(database=database, only_once=only_once)
        if parms != None or kw_parms != {}:
            if parms != None and kw_parms != {}:
                if type(parms) == list:
                    for parm in parms:
                        parm.update(kw_parms)
                else:
                    parms.update(kw_parms)
            elif kw_parms != {}:
                parms = kw_parms
            if parms != None:
                parms = self.fill_sql_none(sql, parms, fill_field, none_values)
            sql = text(sql)
            result = self.conn.execute(sql, parms)
        else:
            result = self.conn.execute(sql)
        fetch_table = lambda _self, fields=None: self.fetch_table(_self, fields)
        fetch_df = lambda _self, fields=None: self.fetch_df(_self, fields)
        fetch_sql = lambda _self, fields=None: self.fetch_sql(_self, fields)
        # result.fetch_table = MethodType(fetch_table, result)
        result.fetch_df = MethodType(fetch_df, result)
        result.fetch_sql = MethodType(fetch_sql, result)
        if only_once:
            self.conn.close()
            del self.conn
            self.conn = None
        return result

    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable]] = None,
            where: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, Iterable[Union[int, str]]]] = None,
            print_sql: bool = False
        ) -> LegacyCursorResult:
        """
        Execute select SQL.

        Parameters
        ----------
        table : Table name.

        database : Database name.

        fields : Select syntax content.
            - None : Is 'SELECT *'.
            - str : Join as 'SELECT str'.
            - Iterable[str] : Join as 'SELECT \`str\`, ...'.

        where : 'WHERE' syntax content, join as 'WHERE str'.

        order : 'ORDER BY' syntax content, join as 'ORDER BY str'.

        limit : 'LIMIT' syntax content.
            - Union[int, str] : Join as 'LIMIT int/str'.
            - Iterable[Union[str, int]] with length of 1 or 2 : Join as 'LIMIT int/str, ...'.

        print_sql : Whether print SQL.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        sqls = []
        if database == None:
            _database = self.database
        else:
            _database = database
        if fields == None:
            fields = "*"
        elif is_iterable(fields):
                fields = ",".join(["`%s`" % field for field in fields])
        select_sql = (
            f"SELECT {fields}\n"
            f"FROM `{_database}`.`{table}`"
        )
        sqls.append(select_sql)
        if where != None:
            where_sql = "WHERE %s" % where
            sqls.append(where_sql)
        if order != None:
            order_sql = "ORDER BY %s" % order
            sqls.append(order_sql)
        if limit != None:
            list_type = type(limit)
            if list_type in [str, int]:
                limit_sql = f"LIMIT {limit}"
            else:
                if len(limit) in [1, 2]:
                    limit_content = ",".join([str(val) for val in limit])
                    limit_sql = "LIMIT %s" % limit_content
                else:
                    error("The length of the limit parameter value must be 1 or 2", ValueError)
            sqls.append(limit_sql)
        sql = "\n".join(sqls)
        if print_sql:
            rprint(sql, title="SQL", frame="half")
        result = self.execute(sql, database=database)
        return result


    def execute_update(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        primary_key: Optional[str] = None,
        print_sql: bool = False
    ) -> None:
        """
        Update the data of table in the datebase.
    
        Parameters
        ----------
        data : Updated data.

        table : Table name.

        database : Database name.

        primary_key : 'WHERE' syntax content.
            - str : Is f'WHERE `{str}` = :{str}'.
            - None : Is 'WHERE `%s` = :%s' % (first field name and value of each item).

        print_sql : Whether print SQL.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.fetch_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        for row in data:
            if primary_key == None:
                primary_key = list(row.keys())[0]
            set_content = ",".join(["`%s` = :%s" % (key, key)for key in row if key != primary_key])
            sql = (
                f"UPDATE `{_database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE `{primary_key}` = :{primary_key}"
            )
            if print_sql:
                rprint(sql, title="SQL", frame="half")
            self.execute(sql, row, database, only_once=False)
        if self.only_once:
            self.conn == None

    def execute_insert(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        duplicate_method: Optional[Literal["ignore", "update"]] = None,
        print_sql: bool = False
    ) -> None:
        """
        Insert the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.

        table : Table name.

        database : Database name.

        duplicate_method : Syntax method when constraint error.
            - 'ignore' : Is 'UPDATE IGNORE INTO'.
            - 'update' : Is 'ON DUPLICATE KEY UPDATE'.
            - None : Then no syntax.

        print_sql : bool, default False
            Whether print SQL.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.fetch_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        fields = list({key for row in data for key in row})
        fields_str = ",".join(["`%s`" % field for field in fields])
        fields_str_position = ",".join([":" + field for field in fields])
        if duplicate_method == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate_method == "update":
            update_content = ",".join(["`%s` = VALUES(`%s`)" % (field, field) for field in fields])
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        if print_sql:
            rprint(sql, title="SQL", frame="half")
        self.execute(sql, data, database)