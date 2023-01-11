import json

import pymysql


class MappingProcess:
    def __init__(self):
        pass

    @staticmethod
    def handle():
        try:
            db = pymysql.connect(
                host="192.168.2.252",
                port=63306,
                user="abmin",
                password="Hh.v0254",
                db="spss_muztak_cn",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = db.cursor()

        try:
            # 查询表字段映射
            foreign_key_mapping_sql = "SELECT a.*,b.table_name as table_name,c.table_name as map_table_name FROM migrate_table_key_map a LEFT JOIN migrate_platform_table b ON a.old_table_id = b.id LEFT JOIN migrate_platform_table c ON a.new_table_id= c.id "
            conn.execute(foreign_key_mapping_sql)
            data = conn.fetchall()

            for v in data:
                # 如果是主键则更改关联外键否则去根据配置更改
                if v['is_primary_key'] == 1:
                    # 查询映射表中映射关系    旧表id->新表id
                    map_sql = "SELECT * FROM migrate_old_to_new WHERE is_handle = 0 and  new_table_id = {};".format(
                        v['new_table_id'])
                    conn.execute(map_sql)
                    map_data = conn.fetchall()
                    sql_list = []
                    for m in map_data:
                        sql = "SELECT * FROM {} WHERE {} = {};".format(v['table_name'], v['old_key_name'],
                                                                       m['old_data_id'])
                        conn.execute(sql)
                        data = conn.fetchone()
                        if isinstance(data, dict):
                            # "UPDATE 表名 SET 映射字段id = 导入新产生的映射id WHERE 映射字段id = 老数据id AND id = （主键id）"
                            update_sql = "UPDATE {} SET {} = {} WHERE {} = {} AND id = {};".format(v['table_name'],
                                                                                                   v['old_key_name'],
                                                                                                   m['new_data_id'],
                                                                                                   v['old_key_name'],
                                                                                                   m['old_data_id'],
                                                                                                   data['id'])

                            # 为了不重复更改已修改的映射数据 改过的数据进行标注
                            sql = "UPDATE migrate_old_to_new SET  is_handle = 1 WHERE id = {} ;".format(m['id'])
                            sql_list.append(update_sql)
                            sql_list.append(sql)

                    for s in sql_list:
                        conn.execute(s)
                else:
                    config = json.loads(v['config'])
                    sql = "SELECT * FROM {};".format(v['table_name'])
                    conn.execute(sql)
                    data = conn.fetchall()
                    for d in data:
                        new_key_name = str(d[v['new_key_name']])
                        if new_key_name in config:
                            update_sql = "UPDATE {} SET {} = '{}' WHERE {} = '{}' AND id = {};".format(v['table_name'],
                                                                                                       v[
                                                                                                           'new_key_name'],
                                                                                                       config[
                                                                                                           new_key_name],
                                                                                                       v[
                                                                                                           'new_key_name'],
                                                                                                       new_key_name,
                                                                                                       d['id'])

                            conn.execute(update_sql)

            db.commit()
            conn.close()
        except Exception as err:
            return None, "脚本执行失败"

        return None, None
