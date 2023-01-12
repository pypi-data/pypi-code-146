#!/usr/bin/python
# -*- coding: utf-8 -*-
from airflow.providers.oracle.hooks.oracle import OracleHook

from detvista_airflow.operators.common.CsvToRDBOperator import CsvToRDBOperator


class CsvToOracleOperator(CsvToRDBOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.hook: OracleHook = OracleHook(oracle_conn_id=self.conn_id)

    def check_table_exists_sql(self) -> str:
        return f"SELECT COUNT(1) FROM {self.table_name}"
