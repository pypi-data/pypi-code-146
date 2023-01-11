# -*- coding: utf-8 -*-
from airflow.providers.oracle.hooks.oracle import OracleHook

from detvista_airflow.operators.common.RDBToCsvOperator import RDBToCsvOperator


class OracleToCsvOperator(RDBToCsvOperator):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_hook(self):
        self.hook: OracleHook = OracleHook(oracle_conn_id=self.conn_id)
