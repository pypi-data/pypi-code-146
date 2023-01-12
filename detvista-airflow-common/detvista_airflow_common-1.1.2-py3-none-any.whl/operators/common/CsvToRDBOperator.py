#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    需要继承后，修改get_hook方法，无法直接使用
"""
import os
import traceback
from typing import Tuple, Optional, Union, Mapping, Iterable, Any, Dict, List

from airflow import AirflowException
from airflow.models import BaseOperator


class CsvToRDBOperator(BaseOperator):
    ui_color: str = "#ededed"

    # 一次读取的最大条数，防止内存溢出
    limit = 3000
    # 分隔符
    delimiter = "|!"
    pandas_delimiter = "\|\!"

    def __init__(
            self,
            *,
            csv_path: str = None,
            conn_id: str = None,
            table_name: str = None,
            database: str = None,
            pre_check: bool = True,
            parameters: Optional[Union[Mapping, Iterable]] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.conn_id: str = conn_id
        self.parameters: Any = parameters
        self.database: str = database
        self.table_name: str = table_name
        self.hook: Any = None
        self._cursor: Any = None
        self._csv_path: str = csv_path
        self.pre_check = pre_check

    def execute(self, context: Dict[str, Any]) -> None:
        self.get_hook()
        res: bool = self._import()
        if not res:
            raise AirflowException(f"[{self.task_id}] - 执行失败！")

    def _import(self) -> bool:
        self.log.info(f"[{self.task_id}] - 导入文件{self._csv_path}")
        if not os.path.exists(self._csv_path):
            self.log.error(f"[{self.task_id}] - 文件{self._csv_path}不存在")
            return False
        self._cursor: Any = self.hook.get_cursor()
        if self.pre_check:
            try:
                self._cursor.execute(self.check_table_exists_sql())
            except:
                self.log.error(f"[{self.task_id}] - 表不存在 {traceback.format_exc()}")
                return False

        with open(self._csv_path, "r", encoding='utf8') as fp:
            col_count: int = len(fp.readline().split(self.delimiter))
            str_format = "%s," * col_count
            str_format = str_format[0:-1]

        try:
            insert_sql: str = f"INSERT INTO `{self.table_name}` VALUES ({str_format})"
            # 如果需要清理之前的数据，可以继承后实现这个方法
            self.clear_data()
            insert_res: bool = self._insert_from_file(insert_sql)
            if insert_res:
                return True
        except:
            self.log.error(f"[{self.task_id}] - 导入csv失败！\n {traceback.format_exc()}")
            return False

    def _insert_from_file(self, sql) -> bool:
        self.log.info(f"[{self.task_id}] - 写入语句: {sql}")
        try:
            # import pandas as pd
            # import numpy as np
            # df = pd.read_csv(self._csv_path, encoding="utf8", header=None, delimiter=self.pandas_delimiter, engine="python").replace(np.nan, '').values.tolist()
            with open(self._csv_path, "r", encoding='utf8') as fp:
                values: List[Any] = []
                while True:
                    data = fp.readline()
                    if (data is None) | (data == ''):
                        break
                    val: Tuple = tuple(data.split(self.delimiter))
                    values.append(val)
                    if len(values) >= self.limit:
                        self.log.info(f"[{self.task_id}] - 准备插入{self.limit}条。")
                        self._cursor.executemany(sql, values)
                        values = []

                # 插入剩余数据
                self.log.info(f"[{self.task_id}] - 准备插入{len(values)}条。")
                self._cursor.executemany(sql, values)
                self._cursor.execute("commit")
                self.log.info(f"[{self.task_id}] - 事务提交成功，提交事务。")
            return True
        except:
            self.log.error(f"[{self.task_id}] - 事务失败，回滚事务! \n {traceback.format_exc()}")
            self._cursor.execute("rollback")
            return False

    def get_hook(self):
        pass

    def check_table_exists_sql(self) -> str:
        pass

    def clear_data(self):
        pass
