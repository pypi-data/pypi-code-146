import datetime
import time
import re
import json
from datetime import datetime
import pymysql
import xlrd
from main.settings import BASE_DIR
from xlrd import xldate_as_tuple
from ..services.DataConsolidation import DataConsolidation
from ..models import *


class DataExeclService:
    @staticmethod
    def excl_import(configure, table_name, file_path):
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
        target_db.commit()
        conn.close()
        data = {
            # "rows": num
        }
        return data, None
