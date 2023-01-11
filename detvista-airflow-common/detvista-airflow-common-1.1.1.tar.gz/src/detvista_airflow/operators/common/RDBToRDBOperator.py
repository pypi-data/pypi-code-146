#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    需要继承后，修改get_hook方法，无法直接使用
"""
import os
import traceback
from typing import Tuple, Optional, Union, Mapping, Iterable, Any, Dict

from airflow import AirflowException
from airflow.models import BaseOperator


class RDBToRDBOperator(BaseOperator):
    ui_color: str = "#ededed"

    # 一次读取的最大条数，防止内存溢出
    limit = 3000

    def __init__(
            self,
            *,
            from_conn_id: str = None,
            from_database: str = None,
            from_table_name: str = None,
            from_sql: str = None,
            to_conn_id: str = None,
            to_database: str = None,
            to_table_name: str = None,
            pre_check: bool = True,
            parameters: Optional[Union[Mapping, Iterable]] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.from_conn_id: str = from_conn_id
        self.to_conn_id: str = to_conn_id
        self.from_sql: str = self._generate_sql_from_file(from_sql, from_table_name)
        self.parameters: Any = parameters
        self.from_database: str = from_database
        self.to_database: str = to_database
        self.to_table_name = to_table_name
        self.from_hook: Any = None
        self.to_hook: Any = None
        self._from_cursor: Any = None
        self._to_cursor: Any = None
        self.pre_check = pre_check

    @classmethod
    def _generate_sql_from_file(cls, sql_path: str, table_name: str) -> str:
        if sql_path is not None:
            if os.path.exists(sql_path):
                # 是一个sql文件路径
                with open(sql_path, "r", encoding="utf-8") as f:
                    contents = f.readlines()
                sql: str = ""
                for c in contents:
                    sql += c.rstrip("\n")
                return sql
            else:
                return sql_path
        elif table_name:
            # 如果定义了表名，全表查询
            return f"SELECT * FROM {table_name};"
        else:
            raise AirflowException(f"[{cls.task_id}] - 没有明确的sql定义！")

    def execute(self, context: Dict[str, Any]) -> None:
        self.get_hook()
        res: bool = self._transfer()
        if not res:
            raise AirflowException(f"[{self.task_id}] - 执行失败！")

    def _transfer(self) -> bool:
        self.log.info(f"[{self.task_id}] - 执行sql：{self.from_sql}")
        self._from_cursor: Any = self.from_hook.get_cursor()
        self._to_cursor: Any = self.to_hook.get_cursor()

        if self.pre_check:
            try:
                self._to_cursor.execute(self.check_table_exists_sql())
            except:
                self.log.error(f"[{self.task_id}] - 表不存在 {traceback.format_exc()}")
                return False

        try:
            self._from_cursor.execute(self.from_sql)
            str_format = None
            insert_sql = None
            while True:
                res: Tuple[Any] = self._from_cursor.fetchmany(self.limit)
                self.log.info(f"[{self.task_id}] - 准备写入{str(len(res))}条。")
                # 第一次先获取有多少个字段
                if str_format is None:
                    str_format = "%s," * len(res[0])
                    str_format = str_format[0:-1]
                    insert_sql = f"INSERT INTO `{self.to_table_name}` VALUES ({str_format})"
                    self.log.info(f"[{self.task_id}] - 写入语句: {insert_sql}")
                self._to_cursor.execute("begin")
                self._to_cursor.executemany(insert_sql, res)
                self._to_cursor.execute("commit")
                if (len(res) < self.limit) or (not res):
                    break

            self.log.info(f"[{self.task_id}] - 数据全部写入成功！")
            return True
        except:
            self.log.error(f"[{self.task_id}] - 数据转换失败！\n {traceback.format_exc()}")
            return False

    def get_hook(self):
        pass

    def check_table_exists_sql(self) -> str:
        pass