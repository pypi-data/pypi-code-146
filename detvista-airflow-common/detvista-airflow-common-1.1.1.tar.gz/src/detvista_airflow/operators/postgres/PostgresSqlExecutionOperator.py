# -*- coding: utf-8 -*-
from airflow.providers.postgres.hooks.postgres import PostgresHook

from detvista_airflow.operators.common.RDBSqlExecutionOperator import RDBSqlExecutionOperator


class PostgresSqlExecutionOperator(RDBSqlExecutionOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.hook: PostgresHook = PostgresHook(postgres_conn_id=self.conn_id, database=self.database)
