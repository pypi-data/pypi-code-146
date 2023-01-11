import datetime
from datetime import datetime
import json
import time

import pymysql
import xlrd
from xlrd import xldate_as_tuple

from ..services.DataConsolidation import DataConsolidation


class DataExeclService:
    @staticmethod
    def excl_import(configure, table_name, file_path):
        # save_dir = "static/upload"
        # filename = "user_base_info.xlsx"
        # 文件地址
        # file_path = re.sub(r"[/\\]{1,3}", "/", f"{str(BASE_DIR)}/{save_dir}/{filename}")
        # 打开上传 excel 表格
        readboot = xlrd.open_workbook(file_path)
        sheet = readboot.sheet_by_index(0)
        # # 获取excel的行和列
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        first_row_values = sheet.row_values(0)  # 第一行数据
        list = []
        num = 1
        for row_num in range(1, nrows):
            row_values = sheet.row_values(row_num)
            if row_values:
                str_obj = {}
            for i in range(len(first_row_values)):
                ctype = sheet.cell(num, i).ctype
                cell = sheet.cell_value(num, i)
                if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(cell)  # 浮点转成整型
                    cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                str_obj[first_row_values[i]] = cell
            list.append(str_obj)
            num = num + 1
        configure = json.loads(configure)  # 连接数据库配置
        # 获得表字段
        field, err_txt = DataConsolidation.list_col(configure['localhost'], configure['port'], configure['username'],
                                                    configure['password'], configure['database'], table_name)
        if err_txt:
            return None, "连接数据库表失败"
        data = {
            "list": list,
            "rows": nrows - 1,
            "table": table_name,
            "field": field
        }
        return data, None

    @staticmethod
    def data_migrate(file_path, configure, export_field, old_table_id, new_table_id):
        configure = json.loads(configure)  # 连接数据库配置
        try:
            target_db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        where = "id = " + new_table_id
        table_name_sql = "SELECT `table_name` FROM migrate_platform_table WHERE {};".format(where)
        conn.execute(table_name_sql)
        table_name = conn.fetchone()
        data = DataExeclService.excl_import(json.dumps(configure), table_name[0], file_path)
        print(data)
        import_data = data[0]["list"]
        # 连接目标数据库
        try:
            num = 0
            for dict in import_data:
                # row = tuple(i)
                if "id" in dict.keys():
                    old_id = dict.pop("id")  # 弹出id 返回旧表主键id
                    field = export_field.lstrip("id,")  # 去除首部id

                row = tuple(dict.values())  # 字典转元组
                sql = "INSERT INTO `{}` ({}) VALUES {};".format(table_name[0], field, row)
                sql = sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
                sql = sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
                conn.execute(sql)
                new_id = conn.lastrowid  # 返回新表主键id
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
                # 迁移映射表数据
                migrate_old_to_new_data = {
                    'old_table_id': old_table_id,
                    'new_table_id': new_table_id,
                    'old_data_id': old_id,
                    'new_data_id': new_id,
                    'created_time': now
                }
                migrate_old_to_new_data = tuple(migrate_old_to_new_data.values())  #
                # 迁移映射表数据插入
                migrate_old_to_new_field = "old_table_id,new_table_id,old_data_id,new_data_id,created_time"
                old_new_sql = "INSERT INTO `{}` ({}) VALUES {};".format("migrate_old_to_new", migrate_old_to_new_field,
                                                                        migrate_old_to_new_data)
                # print(old_new_sql)
                conn.execute(old_new_sql)

                num = num + 1
        except Exception as e:
            return None, e
        target_db.commit()
        conn.close()
        data = {
            "rows": num
        }
        return data, None

    @staticmethod
    def data_cover(file_path, configure, table_name, cover_where, cover_field):
        configure = json.loads(configure)  # 连接数据库配置
        try:
            target_db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        readboot = xlrd.open_workbook(file_path)
        sheet = readboot.sheet_by_index(0)
        # # 获取excel的行和列
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        first_row_values = sheet.row_values(0)  # 第一行数据
        list = []
        try:
            num = 0
            for row_num in range(1, nrows):
                row_values = sheet.row_values(row_num)
                if row_values:
                    str_obj = {}
                for i in range(len(first_row_values)):
                    ctype = sheet.cell(num, i).ctype
                    cell = sheet.cell_value(num, i)
                    if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                        cell = int(cell)  # 浮点转成整型
                        cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                    elif ctype == 3:
                        date = datetime(*xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%m/%d %H:%M:%S')
                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    str_obj[first_row_values[i]] = cell
                list.append(str_obj)
                num = num + 1
            # print(list)

            for dict in list:
                where = cover_where + "=" + "'" + dict[cover_where] + "'"
                li = []
                for i in cover_field.split(","):
                    if len(dict[i]) > 0:
                        update = i + "=" + "'" + dict[i] + "'"
                    else:
                        update = i + "=" + "''"
                    li.append(update)
                str1 = ','.join(li)
                sql = "UPDATE `{}` SET {} WHERE {};".format(table_name, str1, where)
                sql = sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
                sql = sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
                # print(sql)
                conn.execute(sql)
        except Exception as e:
            return None, e
        target_db.commit()
        conn.close()
        data = {
            "rows": num
        }
        return data, None
