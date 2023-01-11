# encoding: utf-8
"""
@project: djangoModel->enroll_statistics_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名统计接口
@created_time: 2022/10/31 11:31
"""
import datetime

from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDay

from xj_enroll.models import Enroll, EnrollSubitemRecord, EnrollRecord


class EnrollStatisticsService():
    @staticmethod
    def statistics_by_day():
        this_day = str(datetime.date.today())
        this_day_start = this_day + " 00:00:00"
        this_day_end = this_day + " 23:59:59"
        before_seven_day_start = ((datetime.datetime.now()) + datetime.timedelta(days=-7)).strftime("%Y-%m-%d") + " 00:00:00"
        result = {}
        # 今日成交数量
        # this_day_obj_count = Enroll.objects.filter(Q(enroll_status_code=680) | Q(enroll_status_code=80)).filter(create_time__gt=this_day_start, create_time__lt=this_day_end).count()
        this_day_obj_count = Enroll.objects.filter(create_time__gt=this_day_start, create_time__lt=this_day_end).count()
        result["this_day_count"] = this_day_obj_count
        # 近七日的成交数量与金额
        # nearly_seven_days = list(
        #     Enroll.objects.filter(Q(enroll_status_code=680) | Q(enroll_status_code=80))
        #         .filter(create_time__gt=before_seven_day_start, create_time__lt=this_day_end) \
        #         .annotate(created_day=TruncDay("create_time")) \
        #         .values("created_day") \
        #         .annotate(deel_count=Count("id"))
        #         .annotate(deel_amount=Sum("amount"))
        #         .values("created_day", "deel_count", "deel_amount")
        # )

        nearly_seven_days = list(
            Enroll.objects.filter(create_time__gt=before_seven_day_start, create_time__lt=this_day_end) \
                .annotate(created_day=TruncDay("create_time")) \
                .values("created_day") \
                .annotate(deel_count=Count("id"))
                .annotate(deel_amount=Sum("amount"))
                .values("created_day", "deel_count", "deel_amount")
        )
        day_map = {}
        for i in nearly_seven_days:
            i["created_day"] = i["created_day"].strftime('%Y-%m-%d')
            i["deel_amount"] = round(float(i["deel_amount"]), 2) if i["deel_amount"] else 0
            day_map[i["created_day"]] = i
        nearly_seven_days_list = []
        for i in range(7):
            this_day = ((datetime.datetime.now()) + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
            nearly_seven_days_list.append(day_map.get(this_day) if day_map.get(this_day) else {"created_day": this_day, "deel_amount": 0, "deel_count": 0})
        result["nearly_seven_days"] = nearly_seven_days_list

        # 总成交金额和总的成交数量
        # total_deel_amount = Enroll.objects.filter(Q(enroll_status_code=680) | Q(enroll_status_code=80)).aggregate(total_deel_amount=Sum('amount'))
        # total_deel_count = Enroll.objects.filter(Q(enroll_status_code=680) | Q(enroll_status_code=80)).aggregate(total_deel_count=Count('id'))

        total_deel_amount = Enroll.objects.filter().aggregate(total_deel_amount=Sum('amount'))
        total_deel_count = Enroll.objects.filter().aggregate(total_deel_count=Count('id'))

        result["total_deel_amount"] = total_deel_amount["total_deel_amount"] if total_deel_amount["total_deel_amount"] else 0
        result["total_deel_count"] = total_deel_count["total_deel_count"] if total_deel_count["total_deel_count"] else 0

        # 代发佣金和提成
        await_commission_main = EnrollRecord.objects.exclude(Q(enroll_status_code=680) | Q(enroll_status_code=80)).aggregate(total_deel_amount=Sum('amount'))
        await_commission_subitem = EnrollSubitemRecord.objects.exclude(Q(enroll_subitem_status_code=680) | Q(enroll_subitem_status_code=80)).aggregate(total_subitem_amount=Sum('subitem_amount'))

        already_commission_main = EnrollRecord.objects.filter(Q(enroll_status_code=680) | Q(enroll_status_code=80)).aggregate(total_deel_amount=Sum('amount'))
        already_commission_subitem = EnrollSubitemRecord.objects.filter(Q(enroll_subitem_status_code=680) | Q(enroll_subitem_status_code=80)).aggregate(total_subitem_amount=Sum('subitem_amount'))
        result["await_commission_main"] = round(await_commission_main["total_deel_amount"], 2) if await_commission_main["total_deel_amount"] else 0
        result["await_commission_subitem"] = round(await_commission_subitem["total_subitem_amount"], 2) if await_commission_subitem["total_subitem_amount"] else 0
        result["already_commission_main"] = round(already_commission_main["total_deel_amount"], 2) if already_commission_main["total_deel_amount"] else 0
        result["already_commission_subitem"] = round(already_commission_subitem["total_subitem_amount"], 2) if already_commission_subitem["total_subitem_amount"] else 0

        return result, None

    @staticmethod
    def statistics_by_user(user_id=None):
        if not user_id:
            return None, "user_id 不能为空"
        this_day = str(datetime.date.today())
        this_day_start = this_day + " 00:00:00"
        this_day_end = this_day + " 23:59:59"
        today_order_num = Enroll.objects.filter(user_id=user_id).filter(create_time__gt=this_day_start, create_time__lt=this_day_end).count()
        # .filter(Q(enroll_status_code=680) | Q(enroll_status_code=80)) \

        today__undertake_num = EnrollRecord.objects.filter(user_id=user_id) \
            .filter(create_time__gt=this_day_start, create_time__lt=this_day_end, ) \
            .exclude(enroll_status_code=124).count()
        # .filter(Q(enroll_status_code=680) | Q(enroll_status_code=80))
        total_order_num = Enroll.objects.filter(user_id=user_id).count()
        total__undertake_num = EnrollRecord.objects.filter(user_id=user_id).exclude(enroll_status_code=124).count()

        return {"today_order_num": today_order_num, "today__undertake_num": today__undertake_num, "total_order_num": total_order_num, "total__undertake_num": total__undertake_num}, None
