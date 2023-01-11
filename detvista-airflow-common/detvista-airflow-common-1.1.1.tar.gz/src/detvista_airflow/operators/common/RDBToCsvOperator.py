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


class RDBToCsvOperator(BaseOperator):
    ui_color: str = "#ededed"

    # 一次读取的最大条数，防止内存溢出
    limit = 3000
    # 分隔符
    delimiter = "|!"

    def __init__(
            self,
            *,
            sql: str = None,
            csv_path: str = None,
            conn_id: str = None,
            table_name: str = None,
            database: str = None,
            parameters: Optional[Union[Mapping, Iterable]] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.conn_id: str = conn_id
        self.sql: str = self._generate_sql_from_file(sql, table_name)
        self.parameters: Any = parameters
        self.database: str = database
        self.hook: Any = None
        self._cursor: Any = None
        self._csv_path: str = csv_path

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
        res: bool = self._export()
        if not res:
            raise AirflowException(f"[{self.task_id}] - 执行失败！")

    def _export(self) -> bool:
        self.log.info(f"[{self.task_id}] - 执行sql：{self.sql}")
        self._cursor: Any = self.hook.get_cursor()

        try:
            # sql先做一次转换，其中可能有日期等需要替换的部分，开放出来自己实现
            self.replace_sql()
            self._cursor.execute(self.sql)
            # 建立文件
            self.log.info(f"[{self.task_id}] - 生成csv文件：{self._csv_path}。")
            with open(f"{os.path.join(self._csv_path)}", "w", encoding="utf-8") as fp:
                while True:
                    res: Tuple[Any] = self._cursor.fetchmany(self.limit)
                    self.log.info(f"[{self.task_id}] - 准备写入{str(len(res))}条。")
                    for r in res:
                        content: str = self.delimiter.join(str(i) if i is not None else "" for i in r)
                        fp.write(content)
                        fp.write("\n")
                    if (len(res) < self.limit) or (not res):
                        break
                    self.log.info(f"[{self.task_id}] - 写入成功！")
            self.log.info(f"[{self.task_id}] - 生成csv文件[{self._csv_path}]。")
            return True
        except:
            self.log.error(f"[{self.task_id}] - 导出csv失败！\n {traceback.format_exc()}")
            return False

    def get_hook(self):
        pass

    def replace_sql(self):
        pass