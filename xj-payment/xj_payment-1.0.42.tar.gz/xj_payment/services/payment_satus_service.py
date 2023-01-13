from django.core.paginator import Paginator
from django.db.models import F
from xj_payment.models import PaymentStatus


class PaymentStatusService:
    @staticmethod
    def get(params):
        limit = params.pop('limit', 20)
        page = params.pop('page', 20)
        list_obj = PaymentStatus.objects.filter(**params).order_by('-id')
        count = list_obj.count()
        list_obj = list_obj.values(
            "id",
            "payment_status",
            "group",
            "description",
        )
        res_set = Paginator(list_obj, limit).get_page(page)
        page_list = []
        if res_set:
            page_list = list(res_set.object_list)

        return {'count': count, 'page': page, 'limit': limit, "list": page_list}, None

    @staticmethod
    def post(params):
        try:
            PaymentStatus.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
