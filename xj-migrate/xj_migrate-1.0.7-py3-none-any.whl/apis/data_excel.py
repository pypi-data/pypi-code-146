from rest_framework.views import APIView

# from ..services.data_execl_service2 import DataExeclService
from ..services.data_execl_service import DataExeclService
from ..utils.custom_response import util_response


class DataExcel(APIView):
    def data_proving(self):
        """
        数据迁移
        @param configure 连接配置（json）
        @param table_name 表名
        """
        configure = self.POST.get('configure')
        filename = self.POST.get('filename')  # 文件路径
        table_name = self.POST.get('table_name')
        data, err_txt = DataExeclService.excl_import(configure, table_name, filename)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    def data_match_write(self):
        filename = self.POST.get('filename')  # 文件路径
        configure = self.POST.get('configure')
        export_field = self.POST.get('export_field')
        old_table_id = self.POST.get('old_table_id')
        new_table_id = self.POST.get('new_table_id')
        data, err_txt = DataExeclService.data_migrate(filename, configure, export_field, old_table_id,
                                                      new_table_id)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    def data_cover(self):
        filename = self.POST.get('filename')  # 文件路径
        table_name = self.POST.get('table_name')
        configure = self.POST.get('configure')
        cover_where = self.POST.get('cover_where')
        cover_field = self.POST.get('cover_field')
        data, err_txt = DataExeclService.data_cover(filename, configure, table_name, cover_where, cover_field)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
