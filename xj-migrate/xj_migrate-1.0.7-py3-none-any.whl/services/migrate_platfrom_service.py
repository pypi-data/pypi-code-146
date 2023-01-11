from ..models import MigratePlatformTable


class MigratePlatfromService:

    @staticmethod
    def get():
        currencies = MigratePlatformTable.objects.all()

        return list(currencies.values('id', 'plaform_id', 'table_name'))

    @staticmethod
    def post(params):
        plaform_id = params.get('plaform_id', '')
        table_name = params.get('table_name', '')
        pay_mode_set = MigratePlatformTable.objects.filter(table_name=table_name, plaform_id=plaform_id).first()
        if pay_mode_set is not None:
            return None, "数据已存在"
        try:
            MigratePlatformTable.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
