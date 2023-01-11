from rest_framework.views import APIView
from ..services.DataConsolidation import DataConsolidation
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data


class Data(APIView):
    def consolidation(self):
        """
          数据迁移
          @param configure 连接配置（json）
          @param table_name 表名
          @param export_field 查询字段（逗号分割）
          @param configure 目标连接配置（json）
          @param target_table_name 目标表名
          @param write_field 目标字段（逗号分割）

         """
        configure = self.POST.get('configure')
        table_name = self.POST.get('table_name')
        export_field = self.POST.get('export_field')
        target_configure = self.POST.get('target_configure')
        target_table_name = self.POST.get('target_table_name', "")
        write_field = self.POST.get('write_field', "")

        data, err_txt = DataConsolidation.consolidation(configure, table_name, target_configure, target_table_name,
                                                        export_field, write_field)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    def list_table(self):
        """
          查询所有字段
          @param localhost 连接地址
          @param username 用户名
          @param password 连接密码
          @param database 数据库名
          @param tabls_name 表名

        """
        localhost = self.POST.get('localhost', '127.0.0.1')
        port = self.POST.get('port', 3306)
        username = self.POST.get('username', "root")
        password = self.POST.get('password', "")
        database = self.POST.get('database', "")

        data, err_txt = DataConsolidation.list_table(localhost, port, username, password, database)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    def list_col(self):
        """
          查询所有字段
          @param localhost 连接地址 192.168.2.252
          @param username 用户名 admin
          @param password 连接密码 Hh.v0254
          @param database 数据库名 spss_muztak_cn
          @param tabls_name 表名

        """
        localhost = self.POST.get('localhost', '127.0.0.1')
        port = self.POST.get('port', 3306)
        username = self.POST.get('username', "root")
        password = self.POST.get('password', "")
        database = self.POST.get('database', "")
        tabls_name = self.POST.get('tabls_name', "")

        data, err_txt = DataConsolidation.list_col(localhost, port, username, password, database, tabls_name)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
