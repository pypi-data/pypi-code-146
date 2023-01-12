#!/usr/bin/python
# -*- coding: utf-8 -*-
from airflow.providers.postgres.hooks.postgres import PostgresHook

from detvista_airflow.operators.common.RDBToRDBOperator import RDBToRDBOperator


class PostgresToPostgresOperator(RDBToRDBOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.from_hook: PostgresHook = PostgresHook(postgres_conn_id=self.from_conn_id, database=self.from_database)
        self.to_hook: PostgresHook = PostgresHook(postgres_conn_id=self.to_conn_id, database=self.to_database)

    def check_table_exists_sql(self) -> str:
        return f"SELECT COUNT(1) FROM {self.to_table_name}"
