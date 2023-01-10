# encoding: utf-8
"""
@project: djangoModel->user_statistics
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户统计服务
@created_time: 2022/11/3 10:36
"""
import calendar
import datetime

from ..models import BaseInfo


class UserStatisticsService(object):
    @staticmethod
    def user_statistics():
        total_user_num = BaseInfo.objects.count()
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
        month_new_user_num = BaseInfo.objects.filter(register_time__gt=this_month_start, register_time__lt=this_month_end).count()
        # bxtx没有分分用户种类暂时这么做
        return {"total_user_num": total_user_num, "month_new_user_num": month_new_user_num, "work_num": int(total_user_num * 0.2)}, None
