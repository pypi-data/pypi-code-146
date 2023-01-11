from django.db.models import F

from ..models import MigrateTableKeyMap


class MigrateForeignKeyMappingService:

    @staticmethod
    def get():
        currencies = MigrateTableKeyMap.objects.all().annotate(old_table_name=F('old_table__table_name'),
                                                               new_table_name=F('new_table__table_name'))

        return list(
            currencies.values('old_table_name', 'new_table_name', 'old_table_id', 'new_table_id', 'old_key_name',
                              'new_key_name'))

    @staticmethod
    def post(params):
        old_table_id = params.get('old_table_id', '')
        new_table_id = params.get('new_table_id', '')
        old_key_name = params.get('old_key_name', '')
        new_key_name = params.get('new_key_name', '')
        config = params.get('config', '')
        pay_mode_set = MigrateTableKeyMap.objects.filter(old_table_id=old_table_id, new_table_id=new_table_id,
                                                         old_key_name=old_key_name, new_key_name=new_key_name).first()
        if pay_mode_set is not None:
            return None, "数据已存在"
        try:
            MigrateTableKeyMap.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
