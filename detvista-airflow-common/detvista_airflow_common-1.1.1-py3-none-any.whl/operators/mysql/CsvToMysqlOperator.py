#!/usr/bin/python
# -*- coding: utf-8 -*-
from airflow.providers.mysql.hooks.mysql import MySqlHook

from detvista_airflow.operators.common.CsvToRDBOperator import CsvToRDBOperator


class CsvToMysqlOperator(CsvToRDBOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.hook: MySqlHook = MySqlHook(mysql_conn_id=self.conn_id, schema=self.database)

    def check_table_exists_sql(self) -> str:
        return f"DESC `{self.table_name}`"
