#!/usr/bin/python
# -*- coding: utf-8 -*-
from airflow.providers.mysql.hooks.mysql import MySqlHook

from detvista_airflow.operators.common.RDBToRDBOperator import RDBToRDBOperator


class MysqlToMysqlOperator(RDBToRDBOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.from_hook: MySqlHook = MySqlHook(mysql_conn_id=self.from_conn_id, schema=self.from_database)
        self.to_hook: MySqlHook = MySqlHook(mysql_conn_id=self.to_conn_id, schema=self.to_database)

    def check_table_exists_sql(self) -> str:
        return f"DESC `{self.to_table_name}`"
