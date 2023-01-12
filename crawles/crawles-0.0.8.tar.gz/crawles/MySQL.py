import pymysql


class SqlSave:
    def __init__(self):
        self.cursor = None
        self.db = None
        self.table = None

    def connect(self,
                host='localhost',  # 主机名 127.0.0.1
                user=None,  # 账号
                password=None,  # 密码
                database=None,  # 需要连接的数据库名字
                table=None,
                ):

        if user is None or \
                password is None or \
                database is None or \
                table is None:
            raise Exception('连接参数填写不完整!')

        self.table = table
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def save(self, field_name, table_data):
        """[1,2,3]"""
        if len(field_name) != len(table_data):
            raise Exception('字段名长度与数据不同')

        sql = f"""INSERT INTO {self.table}({','.join(field_name)})VALUES (%s,%s,%s)"""
        try:
            # 执行sql语句
            self.cursor.execute(sql, tuple(table_data))
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            raise Exception(f'数据插入失败:{e}')

    # def save_many(self,list_data: list[list]):
    #     """[[1,2,3],[4,5,6],[7,8,9]]"""

    def close(self):
        self.db.close()


sql_save = SqlSave()


if __name__ == '__main__':
    sql_save.connect(user='root',  # 账号
                     password='000000',  # 密码
                     database='python_mysql',  # 需要连接的数据库名字
                     table='a'
                     )
    sql_save.save(['url_id', 'url_title', 'url_author'], [1, 2, 3])
    sql_save.close()
