"""
    SQL 连接类

    官网及文档：https://www.sqlalchemy.org/
    连接池文档：https://www.osgeo.cn/sqlalchemy/core/pooling.html

    示例：
        engine = SQLAlchemyEngineBase(drivername='mysql+pymysql', host='localhost', port=3306, user='root', pwd='1234', db='test')

        # 案例 1
        with engine.session as session, session.begin():
            session.xxxx    # session 操作
            method.xxxx     # method 操作

        # 案例 2
        engine.reverse_table_model(path='./modules.py', tables=[])
        res = method.execute(sql='select * from table', fetchone=True, back_dict=True)

    注意：
        默认就是 QueuePool
        Session 在使用 with 时，会丢失方法的提示，所以套了一层 SessionBase 使得能够正常访问，书写更舒服

        with engine.session() as session：(自动关闭 session)
            with session.begin():   (自动提交回滚捕获错误)

        同时使用：
            with engine.session() as session, session.begin():

        如果是 Table 类，那可能不起作用
"""
import subprocess
from pathlib import Path
from copy import deepcopy
from typing import List, Union
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import declarative_base
from quickdb.orm.sqlalchemy.exception import SuffixError

BaseModel = declarative_base()


# SessionBase 作用是使得 with 时能够正常访问到对应的属性方法
class SessionBase(Session):
    def __enter__(self):
        return self


class SQLAlchemyEngineBase:
    def __init__(self, drivername: str, host: str, port: int, user: str, pwd: str, db: str, **kwargs):
        """

        :param drivername: 连接方式如：mysql 的 mysql+pymysql
        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """

        # 创建连接 url
        self.conn_url = URL.create(
            drivername=drivername,
            username=user,
            password=pwd,
            host=host,
            port=port,
            database=db
        )

        # 更新默认配置
        config_default = {
            'pool_size': 5,  # 连接池大小
            'pool_pre_ping': True,  # 检查连接状态
            'pool_recycle': 3600,  # 连接回收时间 s，-1 为不启用
            'max_overflow': 10,  # 允许连接池溢出的最大数量
            'echo': False,  # 打印日志（可以看到 sql，默认就是 False）
        }
        config_default.update(kwargs)

        # 创建 engine
        self.engine = create_engine(self.conn_url, **config_default)  # 创建连接

    def session(self, **kwargs) -> SessionBase:
        """
        获取执行的 session

        :return:
        """
        return SessionBase(bind=self.engine, **kwargs)

    def connection(self, close_with_result: bool = False) -> Connection:
        """
        原始连接

        :param close_with_result:
        :return:
        """
        return self.engine.connect(close_with_result)

    def reverse_table_model(self, path: str = None, tables: List[str] = None, commands: str = None):
        """
        逆向表模型

        无 path 则生成：models/数据库类型/host/database.py

        注意：pip install sqlacodegen

        注意，若生成的是 Table 而不是 class 类，有以下 3 种情况
            1、表无主键
            2、表是其他表之间的关联表
            3、使用了 -noclasses 参数

        :param path: 最终生成的 models.py 文件路径
        :param tables: 需要逆向的表，默认是所有表
        :param commands: 其他命令
        :return:
        """
        if path:
            if Path(path).suffix != '.py':
                raise SuffixError(f'请输入文件路径，而非文件夹路径，输入：{path}')

            # 创建文件夹和 __init__.py
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)

            init_file_name = '__init__.py'
            if not p.parent.joinpath(init_file_name).exists():
                with open(p.parent.joinpath(init_file_name), 'w', encoding='utf-8') as f:
                    pass
        else:
            path = self._get_model_path()

        conn_url = self.conn_url.render_as_string(hide_password=False)  # 将 url 类转换为 url 字符串

        command = f"sqlacodegen {conn_url} > {path}"

        if tables:
            command += f" --tables {','.join(tables)}"

        if commands:
            command += f" {commands}"

        result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, encoding='utf-8')
        if result.stderr:
            print('执行失败：', result.stderr)

    def insert(self, instance: Union[List[BaseModel], BaseModel]):
        """
        插入

        :param instance: 模型类列表
        :return:
        """
        if not isinstance(instance, list):
            instance = [instance]

        with self.session() as session, session.begin():
            session.add_all(instance)

    def merge(self, instance, load: bool = True, options=None):
        """
        根据主键 upsert

        :param instance: 模型类
        :param load:
        :param options:
        :return:
        """
        with self.session() as session, session.begin():
            session.merge(instance, load, options)

    def execute(self, sql: str, fetchone: bool = False, fetchmany: int = None, fetchall: bool = False,
                back_dict: bool = False, **kwargs) -> Union[Result, Row, dict, List[dict], None]:
        """

        :param sql: sql
        :param fetchone: 返回一条
        :param fetchmany: 返回指定数量
        :param fetchall: 返回多条
        :param back_dict: 以字典形式返回
        :return:
        """
        with self.session() as session, session.begin():
            result = session.execute(sql, **kwargs)

            if fetchone:
                back = result.fetchone()
            elif fetchmany:
                back = result.fetchmany(size=fetchmany)
            elif fetchall:
                back = result.fetchall()
            else:
                return result

        # 判断是否需要生成字典
        if back_dict and back:
            if isinstance(back, list):
                back = [dict(zip(result.keys(), i)) for i in back]
            else:
                back = dict(zip(result.keys(), back))

        return back

    def delete(self, instance: BaseModel):
        """
        删除数据

        :param instance:
        :return:
        """
        with self.session() as session, session.begin():
            session.delete(instance)

    def close_all(self):
        """
        关闭所有连接

        :return:
        """
        self.engine.dispose()

    @staticmethod
    def _get_dict(instance: BaseModel) -> dict:
        """
        将类实例转化为字典

        :param instance:
        :return:
        """
        instance_dict = {}
        for key, value in instance.__dict__.items():
            if not key.startswith('_'):
                instance_dict[key] = value

        return instance_dict

    @staticmethod
    def _get_update_data(instance_dict: dict, update_keys: List[str], exclude_keys: List[str]) -> dict:
        """
        获取更新的数据

        :param instance_dict: 数据字典
        :param update_keys: 需要更新的字段
        :param exclude_keys: 需要排除的字段
        :return:
        """
        update_dict = {}

        if not update_keys:
            update_dict = deepcopy(instance_dict)
        else:
            for key, value in instance_dict.items():
                if key in update_keys:
                    update_dict[key] = value

        if exclude_keys:
            for key in exclude_keys:
                if key in update_dict:
                    del update_dict[key]

        return update_dict

    def _get_model_path(self) -> Path:
        """
        获取并创建 models 文件夹的路径

        命名规则：models/数据库类型_host/database.py

        :return:
        """
        # 构建路径
        path = Path('./models')

        # 取数据库的类型
        db = self.conn_url.drivername
        if '+' in db:
            db = db.split('+')[0]

        # 取数据库的 host 后几位
        host = self.conn_url.host
        if '.' in host:
            host = host.split('.')[-1]

        path = path.joinpath(db + '_' + host).joinpath(self.conn_url.database + '.py')

        # 创建路径并创建 __init__.py
        init_file_name = '__init__.py'
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.parent.joinpath(init_file_name).exists():
            with open(path.parent.joinpath(init_file_name), 'w', encoding='utf-8') as f:
                pass
        if not path.parent.parent.joinpath(init_file_name).exists():
            with open(path.parent.parent.joinpath(init_file_name), 'w', encoding='utf-8') as f:
                pass

        return path
