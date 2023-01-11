# 应用名称
from django.urls import re_path

from .apis import data_migration, data_excel, migrate_platfrom, migrate_foreign_key_mapping, export_api

app_name = 'database'

urlpatterns = [

    re_path(r'^list_table/?$', data_migration.DataMigration.list_table),
    re_path(r'^list_col/?$', data_migration.DataMigration.list_col),
    re_path(r'^consolidation/?$', data_migration.DataMigration.consolidation),
    re_path(r'^data_proving/?$', data_excel.DataExcel.data_proving),
    re_path(r'^data_match_write/?$', data_excel.DataExcel.data_match_write),
    re_path(r'^data_cover/?$', data_excel.DataExcel.data_cover),
    re_path(r'^mapping_rocessing/?$', data_migration.DataMigration.mapping_rocessing),
    re_path(r'^platform/?$', migrate_platfrom.MigratePlatfrom.as_view()),  # 迁移平台
    re_path(r'^foreign_key_mapping/?$', migrate_foreign_key_mapping.MigrateForeignKeyMapping.as_view()),  # 外键映射
    re_path(r'^doc_export/?$', export_api.exportAPIView.doc_export),  # 外键映射
    re_path(r'^excel_export/?$', export_api.exportAPIView.excel_export),  # 外键映射

]
