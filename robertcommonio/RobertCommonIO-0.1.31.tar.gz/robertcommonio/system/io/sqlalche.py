from typing import Optional, Any, Union, List, Dict

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool.impl import QueuePool
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.declarative import declarative_base


class SQLAlCheAccessor:

    def __init__(self):
        self.engine: dict = {}

    def add_engine(self, engine_name: str, engine_conn: str, engine_pool_class: Any = QueuePool, engine_pool_recycle: int = 60):
        """
                添加一个数据库连接池
                quote_plus(psw)
                @Example:
                    PostgreSQL
                        # default
                        engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
                        # psycopg2
                        engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
                        # pg8000
                        engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')

                    MySQL
                        # default
                        engine = create_engine('mysql://scott:tiger@localhost/foo')
                        # mysqlclient (a maintained fork of MySQL-Python)
                        engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
                        # PyMySQL
                        engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
                        # mysql+pymysql://root:XXX@localhost:3306/foo?charset=utf8

                    Oracle
                        engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
                        engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')

                    SQL Server
                        # pyodbc
                        engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')
                        # pymssql
                        engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')

                    SQLite
                        engine = create_engine('sqlite:///foo.db')  # 相对地址
                        engine = create_engine('sqlite:///C:\\path\\to\\foo.db')    # 绝对地址

            """
        if engine_name not in self.engine.keys():
            engine = create_engine(engine_conn, poolclass=engine_pool_class, pool_recycle=engine_pool_recycle)
            if engine:
                self.engine[engine_name] = engine
        return self.engine.get(engine_name)

    def get_engine(self, engine_name: str):
        return self.engine.get(engine_name)

    def to_dict(self, records: Union[List[Optional[Dict]], Dict]):
        if isinstance(records, Dict):
            values = {}
            for k, v in records.items():
                values[k] = v
            return values
        elif isinstance(records, List):
            values = []
            for record in records:
                value = {}
                for k, v in record.items():
                    value[k] = v
                values.append(value)
            return values
        return records

    def read_sql(self, engine_name: str, sql_cmd: str, to_dict: bool = True):
        with self.get_engine(engine_name).connect() as conn:
            records = conn.execute(sql_cmd).mappings().all()
            if to_dict is True:
                return self.to_dict(records)
            return records

    def read_sql_dataframe(self, engine_name: str, sql_cmd: str):
        with self.get_engine(engine_name).connect() as conn:
            return pd.read_sql_query(sql_cmd, conn)

    def execute_sql(self, engine_name: str, sql_cmd: str, params: Optional[list] = None):
        with self.get_engine(engine_name).connect() as conn:
            return conn.execute(text(sql_cmd), params).rowcount

    def execute_multi_sql(self, engine_name: str, cmd_tuple: list):
        with self.get_engine(engine_name).begin() as conn:
            rowcount = 0
            for cmd in cmd_tuple:
                rowcount = conn.execute(text(cmd[0]), cmd[1]).rowcount + rowcount
            return rowcount

    def get_table_struct(self, engine_name: str, table_name: str):
        engine = self.get_engine(engine_name)
        if engine is not None:
            base = declarative_base()
            base.metadata.reflect(engine)
            # 获取原表对象
            old_table = base.metadata.tables[table_name]
            # 获取原表建表语句
            crate_sql = str(CreateTable(old_table))
            base.metadata.clear()
            return crate_sql
        return None

    def generate_sql_format(self, table_name: str, action: str = 'replace', colums: Optional[list] = None, filter_column: Optional[list] = None, add_syntax: bool = False):
        filed_format = '{}' if add_syntax is False else '`{}`'
        filed_format1 = '{} = :{}' if add_syntax is False else '`{}` = :{}'
        if action in ['replace', 'append']:
            return f"insert into {table_name} ({', '.join(filed_format.format(k) for k in colums)}) VALUES ({', '.join(':{}'.format(k) for k in colums)})"
        elif action == 'update':
            return f"update {table_name} set {', '.join(filed_format1.format(k, k) for k in colums)} where {', '.join(filed_format1.format(k, k) for k in filter_column)}"
        elif action == 'delete':
            return f"delete from {table_name} where {', '.join(filed_format1.format(k, k) for k in filter_column)}"

    def generate_sql_cmds(self, table_name: str, records: list, action: str = 'replace', colums: list = None, filter_column: list = None):
        cmds = []
        if len(records) > 0:
            if action == 'replace':
                if filter_column is None:
                    cmds.append((f"delete from {table_name}", None))
                else:
                    cmds.append((self.generate_sql_format(table_name, 'delete', None, filter_column), records))

            cmds.append((self.generate_sql_format(table_name, action, records[0].keys() if colums is None else colums, filter_column), records))
        return cmds

    def copy_table_struct(self, engine_name: str, table_name: str, new_table_name: str):
        crate_sql = self.get_table_struct(engine_name, table_name)
        if crate_sql is not None:
            return self.execute_sql(engine_name, crate_sql.replace("CREATE TABLE " + table_name, "CREATE TABLE if not exists " + new_table_name))

    def syn_table_record(self, engine_name: str, sql_cmd: str, engine_name_new: str, table_name_new: str,  if_exists: str = 'replace'):
        engine = self.get_engine(engine_name)
        engine_new = self.get_engine(engine_name_new)
        if engine and engine_new:
            pd.read_sql(sql_cmd, engine).to_sql(table_name_new, engine_new, if_exists=if_exists)
            return True
        return False
