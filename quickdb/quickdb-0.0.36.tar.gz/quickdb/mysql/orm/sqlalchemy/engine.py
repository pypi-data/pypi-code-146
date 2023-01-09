"""
    MYSQL 连接类

    示例：
        engine = MysqlSQLAlchemyEngine(host='localhost', port=3306, user='root', pwd='1234', db='test')
"""
from typing import List, Union
from sqlalchemy.engine import Result
from sqlalchemy.dialects.mysql import insert
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase, BaseModel


class MysqlSQLAlchemyEngine(SQLAlchemyEngineBase):
    def __init__(self, db: str, host: str = '127.0.0.1', port: int = '3306', user: str = 'root', pwd: str = None,
                 **kwargs):
        """

        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """
        super().__init__('mysql+pymysql', host, port, user, pwd, db, **kwargs)

    def upsert(
            self,
            instance: Union[List[BaseModel], BaseModel],
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作
        详情见：https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

        :param instance: 数据
        :param update_keys: 需要更新的字段（无则全更）
        :param exclude_keys: 需要排除的字段（无则全更）
        :return:
        """
        if not isinstance(instance, list):
            instance = [instance]

        # 处理好要更新的数据
        instance_list = []
        for i in instance:
            instance_list.append(self._get_dict(i))

        # 需要更新的字段
        update_keys = list(self._get_update_data(instance_list[0], update_keys, exclude_keys).keys())

        # 生成 sql
        insert_sql = insert(instance[0].__table__).values(instance_list)  # 生成 insert 语句
        update_keys = {x.name: x for x in insert_sql.inserted if x.name in update_keys}  # 需要更新的字段
        upsert_sql = insert_sql.on_duplicate_key_update(**update_keys)  # 生成 upsert 语句

        # 执行 sql
        with self.session() as session, session.begin():
            return session.execute(upsert_sql)
