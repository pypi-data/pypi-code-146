# -*- coding: utf-8 -*-

import os
import traceback
from typing import Dict, Optional, Union, Mapping, Iterable, Any

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator


"""
    需要继承后，修改get_hook方法，无法直接使用
"""
class RDBSqlExecutionOperator(BaseOperator):
    ui_color: str = "#ededed"

    def __init__(
            self,
            *,
            sql: str,
            conn_id: str = None,
            database: str = None,
            parameters: Optional[Union[Mapping, Iterable]] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.conn_id: str = conn_id
        self.sql: str = self._generate_sql_from_file(sql) if os.path.exists(sql) else sql
        self.parameters: Any = parameters
        self.database: str = database
        self.hook: Any = None
        self._cursor: Any = None

    @classmethod
    def _generate_sql_from_file(cls, sql_path: str) -> str:
        with open(sql_path, "r", encoding="utf-8") as f:
            contents = f.readlines()

        sql: str = ""
        for c in contents:
            sql += c.rstrip("\n")
        return sql

    def execute(self, context: Dict[str, Any]) -> None:
        self.get_hook()
        res: bool = self._call()
        if not res:
            raise AirflowException(f"[{self.task_id}] - 执行失败！")

    def _call(self) -> bool:
        self.log.info(f"[{self.task_id}] - 执行sql：{self.sql}")
        self._cursor: Any = self.hook.get_cursor()
        try:
            self.log.info(f"[{self.task_id}] - 事务开始")
            self.hook.run(self.sql, autocommit=False)
            self.log.info(f"[{self.task_id}] - 事务成功，提交事务。")
            self.hook.run("commit")
            return True
        except Exception:
            self.log.error(f"[{self.task_id}] - 事务失败，回滚事务！")
            self.hook.run("rollback")
            self.log.error(f"[{self.task_id}] - 执行SQL时失败。\n {traceback.format_exc()}")
            return False

    def get_hook(self):
        pass
