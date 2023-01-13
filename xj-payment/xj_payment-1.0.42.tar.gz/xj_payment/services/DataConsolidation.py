import json

import pymysql

class DataConsolidation:
    def __init__(self):
        pass

    @staticmethod
    def consolidation(configure, table_name, configure_configure, target_table_name, export_field, write_field):
        """
        将一张表的指定字段数据导出到另一张表
        @param table_name 表名
        @param export_field 表字段
        @param target_table_name 目标表名
        @param write_field 目标字段

        """
        # 边界检查
        export_field_list = export_field.split(",")
        write_field_list = write_field.split(",")

        if not table_name:
            # print(u"错误，表名必填")
            return None, "错误，表名必填"
        if not target_table_name:
            # print(u"错误，表名必填")
            return None, "错误，目标表名必填"
        if len(export_field_list) != len(write_field_list):
            return None, "错误，替换字段长度不符"

        configure = json.loads(configure)  # 连接数据库配置
        configure_configure = json.loads(configure_configure)  # 连接目标数据库配置
        # 连接数据库
        try:
            db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "数据库连接失败"
        cursor = db.cursor()
        # 连接目标数据库
        try:
            target_db = pymysql.connect(
                host=configure_configure['localhost'],
                port=int(configure_configure['port']),
                user=configure_configure['username'],
                password=configure_configure['password'],
                db=configure_configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        # cursor = connection.cursor()
        # 查询要导出的数据
        query_sql = "select {} from {}".format(export_field, table_name)
        cursor.execute(query_sql)
        # cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        try:
            for row in rows:
                sql = "INSERT INTO `{}` ({}) VALUES {};".format(target_table_name, write_field, row)
                sql = sql.replace("'None'", "NULL").replace("None", "NULL")
                conn.execute(sql)
        except Exception as e:
            return None, e

        db.commit()
        target_db.commit()
        cursor.close()
        conn.close()
        return None, None

    @staticmethod
    def list_col(localhost, port, username, password, database, tabls_name):
        """
         查询所有字段
         @param localhost 连接地址
         @param username 用户名
         @param password 连接密码
         @param database 数据库名
         @param tabls_name 表名

        """
        try:
            db = pymysql.connect(
                host=localhost,
                port=int(port),
                user=username,
                password=password,
                db=database,
                charset="utf8",
            )
        except Exception as err:
            return None, "数据库连接失败"

        cursor = db.cursor()
        cursor.execute("select * from %s" % tabls_name)
        col_name_list = [tuple[0] for tuple in cursor.description]
        db.close()
        return col_name_list, None

    # 列出所有的表
    @staticmethod
    def list_table(localhost, port, username, password, database):
        """
         列出所有的表
         @param localhost 连接地址
         @param username 用户名
         @param password 连接密码
         @param database 数据库名

        """
        try:
            db = pymysql.connect(
                host=localhost,
                port=int(port),
                user=username,
                password=password,
                db=database,
                charset="utf8",
            )
        except Exception as err:
            return None, "数据库连接失败"

        cursor = db.cursor()
        cursor.execute("show tables")
        table_list = [tuple[0] for tuple in cursor.fetchall()]
        db.close()
        return table_list, None

# tables = list_table(localhost, username, password, database) # 获取所有表，返回的是一个可迭代对象
# print(tables)
#
# for table in tables:
#     col_names = list_col(localhost, username, password, database, table)
#     print(col_names) # 输出所有字段名
