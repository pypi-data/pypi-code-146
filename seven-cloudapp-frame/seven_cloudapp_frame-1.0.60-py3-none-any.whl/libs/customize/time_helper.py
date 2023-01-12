# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-07-15 11:54:54
@LastEditTime: 2022-11-16 16:13:04
@LastEditors: HuangJianYi
:description: 时间帮助类
"""
from seven_framework import *
import datetime



class TimeExHelper:
    """
    :description: 时间帮助类
    """

    @classmethod
    def get_now_int(self, hours=0, minutes=0, fmt='%Y%m%d%H%M%S'):
        """
        :description: 获取整形的时间 格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010
        :param hours: 需要增加的小时数
        :param hours: 需要增加的分钟数
        :param fmt: 时间格式
        :return:
        :last_editors: HuangJianYi
        """
        now_date = (datetime.datetime.now() + datetime.timedelta(minutes=minutes, hours=hours))
        return int(now_date.strftime(fmt))

    @classmethod
    def get_now_hour_int(self, hours=0):
        """
        :description: 获取整形的小时2020050612
        :param hours: 需要增加的小时数
        :return: int（2020050612）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours, fmt='%Y%m%d%H')

    @classmethod
    def get_now_day_int(self, hours=0):
        """
        :description: 获取整形的天20200506
        :param hours: 需要增加的小时数
        :return: int（20200506）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours, fmt='%Y%m%d')

    @classmethod
    def get_now_month_int(self, hours=0):
        """
        :description: 获取整形的月202005
        :param hours: 需要增加的小时数
        :return: int（202005）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours,fmt='%Y%m')

    @classmethod
    def get_date_list(self, start_date, end_date):
        """
        :description: 两个日期之间的日期列表
        :param start_date：开始日期
        :param end_date：结束日期
        :return: list
        :last_editors: HuangJianYi
        """
        if not start_date or not end_date:
            return []
        if ":" not in start_date:
            start_date+=" 00:00:00"
        if ":" not in end_date:
            end_date += " 00:00:00"
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        date_list = []

        while datestart < dateend:
            date_list.append(datestart.strftime('%Y-%m-%d'))
            datestart += datetime.timedelta(days=1)
        return date_list

    @classmethod
    def convert_custom_date(self, dt):
        """
        :description: 转换自定义文本时间
        :param dt: datetime格式时间或时间字符串
        :return: str
        :last_editors: HuangJianYi
        """
        now_timestamp = TimeHelper.get_now_timestamp()
        difference_seconds = TimeHelper.difference_seconds(now_timestamp, dt)
        if difference_seconds <= 1:
            return "刚刚"
        elif difference_seconds < 60:
            return  str(difference_seconds) + "秒前"
        elif difference_seconds >= 60 and difference_seconds < 3600:
            return str(int(difference_seconds / 60)) + "分钟前"
        elif difference_seconds >= 3600 and difference_seconds < 24 * 3600:
            return str(int(difference_seconds / 3600)) + "小时前"
        else:
            return str(int(difference_seconds / (24 * 3600))) + "天前"
