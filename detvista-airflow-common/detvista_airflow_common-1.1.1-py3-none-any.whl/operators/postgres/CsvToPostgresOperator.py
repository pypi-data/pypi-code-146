#!/usr/bin/python
# -*- coding: utf-8 -*-
from airflow.providers.postgres.hooks.postgres import PostgresHook

from detvista_airflow.operators.common.CsvToRDBOperator import CsvToRDBOperator


class CsvToPostgresOperator(CsvToRDBOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.hook: PostgresHook = PostgresHook(postgres_conn_id=self.conn_id, database=self.database)

    def check_table_exists_sql(self) -> str:
        return f"SELECT COUNT(1) FROM {self.table_name}"
