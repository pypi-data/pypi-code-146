"""
    pg 连接类

    engine = PostgreSQLAlchemyEngine(host='localhost', port=5432, user='postgres', pwd='1234', db='postgres')
"""
from typing import List, Union
from sqlalchemy.engine import Result
from sqlalchemy.dialects.postgresql import insert
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase, BaseModel


class PostgreSQLAlchemyEngine(SQLAlchemyEngineBase):
    def __init__(self, host: str = '127.0.0.1', port: int = 5432, user: str = 'postgres', pwd: str = '1234',
                 db: str = 'postgres', **kwargs):
        """

        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """
        super().__init__('postgresql+psycopg2', host, port, user, pwd, db, **kwargs)

    def upsert(
            self,
            instance: Union[List[BaseModel], BaseModel],
            constraint: str = None,
            index_elements: List[str] = None,
            index_where=None,
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作
        详情见：https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

        index_where=my_table.c.user_email.like('%@gmail.com')

        :param instance: 数据
        :param constraint: 表上唯一或排除约束的名称，或者约束对象本身
        :param index_elements: 由字符串列名、列对象或其他列表达式对象组成的序列
        :param index_where: 可用于推断条件目标索引的附加 WHERE 条件
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
        update_keys = {x.name: x for x in insert_sql.excluded if x.name in update_keys}  # 需要更新的字段
        upsert_sql = insert_sql.on_conflict_do_update(
            constraint=constraint,
            index_elements=index_elements,
            index_where=index_where,
            set_=update_keys
        )  # 生成 upsert 语句

        # 执行 sql
        with self.session() as session, session.begin():
            return session.execute(upsert_sql)
