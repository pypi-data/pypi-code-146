#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""desc: 项目中所使用的 日期、时间 通用方法

"""

import time
import datetime
import calendar
import pytz

TIME_ZONE = "Asia/Shanghai"  # TODO: 放入环境变量


class _date_time:
    __standard__ = 'ISO 8601:2004(E)'


# 年份格式
BASIC_YEAR = '%Y'
SHORT_YEAR = '%y'
# 月份格式
BASIC_MONTH = '%Y%m'
EXTEND_MONTH = '%Y-%m'
# 日期格式
BASIC_DATE = '%Y%m%d'
EXTEND_DATE = '%Y-%m-%d'
# BasicDateOriFmt = '%Y%j'  # 一年中的第几天
# ExtendDateOriFmt = '%Y-%j'  # 一年中的第几天
# BasicDateWeek = '%YW%U%w'  # 2020W013 2020 01 01 星期三  星期天作为每个星期的第一天   0-6
# ExtendDateWeek = '%Y-W%U-%w'  # 2020-W01-3
# 时间格式
EXTEND_TIME = '%H:%M:%S'
EXTEND_MICRO_TIME = '%H:%M:%S.%f'
# ExtendTimeZone = '%H:%M:%S%Z'
# ExtendTimeZoneMicro = '%H:%M:%S.%f%Z'
# 日期时间格式
EXTEND_DT = '%Y-%m-%d %H:%M:%S'  # 2020-01-01 01:01:01
EXTEND_T_DT = '%Y-%m-%dT%H:%M:%S'  # 2020-01-01T01:01:01
EXTEND_T_DT__ = '%Y-%m-%dT%H-%M-%S'  # 2020-01-01T01:01:01
EXTEND_MICRO_DT = '%Y-%m-%d %H:%M:%S.%f'  # 2020-01-01 01:01:01.000000
EXTEND_T_ZONE_DT = '%Y-%m-%dT%H:%M:%SZ'  # 2020-01-01T01:01:01Z
EXTEND_T_ZONE_MICRO_DT = '%Y-%m-%dT%H:%M:%S.%fZ'  # 2020-01-01T01:01:01.000000Z
EXTEND_DT_DAY_START = '%Y-%m-%d 00:00:00'
EXTEND_DT_DAY_END = '%Y-%m-%d 23:59:59'


TZ_LOCAL = pytz.timezone(TIME_ZONE)
TZ_UTC = pytz.timezone('UTC')
ONE_MICRO_SECONDS = datetime.timedelta(microseconds=1)
ONE_SECOND = datetime.timedelta(seconds=1)
ONE_HOUR = datetime.timedelta(hours=1)
ONE_DAY = datetime.timedelta(days=1)


class UtcUtil(object):
    """ 与 utc 相关的一些转化

    可将所有与时间转化的函数封装至此类
    """

    def __init__(self, time_zone=TIME_ZONE):
        """
        :param time_zone: 时区
        """
        self.time_zone = time_zone
        self.tz = pytz.timezone(self.time_zone)

    def dt2utcdt(self, dt, tzinfo=False):
        """ datetime -> datetime  本地时间-> UTC 时间

        :param dt: 本地时间  datetime.datetime
        :param tzinfo: 是否带时区信息  如果带，返回的是 2020-09-08 17:57:42.874000+00:00   如果不带  2020-09-08 17:57:42.874000
        """
        utc_dt = self.tz.localize(dt).astimezone(pytz.utc)
        if not tzinfo:
            utc_dt = utc_dt.replace(tzinfo=None)
        return utc_dt

    def utcdt2dt(self, utcdt, tzinfo=False):
        """ datetime -> datetime:  utc 时间转化为本地时间

        :param utcdt: utc 时间  datetime.datetime
        :param tzinfo: 是否带时区信息  如果带，返回的是 2020-09-08 17:57:42.874000+08:00   如果不带  2020-09-08 17:57:42.874000
        """
        dt = pytz.utc.localize(utcdt).astimezone(self.tz)
        if not tzinfo:
            dt = dt.replace(tzinfo=None)
        return dt

    def utcnow(self):
        return datetime.datetime.utcnow()

    def dt2timestamp(self, dt):
        """ 时间转对应的时间戳 """
        return time.mktime(dt.timetuple())

    def dt2timestampmicro(self, dt):
        """ 毫秒级时间戳 """
        timestamp = time.mktime(dt.timetuple())
        return int(timestamp * 1000)

    def dt2utctimestamp(self, dt):
        """ 本地时间转 utc 时间戳 """
        return self.dt2timestamp(self.dt2utcdt(dt))

    def dt_str_to_utc_str(self, dt_str):
        """ dt_str:  2020-01-01 08:00:00 格式的字符串
        ->  2020-01-01T00:00:00Z 格式的字符串
        """
        dt = datetime.datetime.strptime(dt_str, EXTEND_DT)
        utc_dt = self.dt2utcdt(dt)
        return utc_dt.strftime(EXTEND_T_ZONE_DT)

    def dt_str_to_utc_str2(self, dt_str):
        """ dt_str:  2020-01-01 08:00:00 格式的字符串
        ->  2020-01-01T00:00:00.000Z 格式的字符串
        """
        dt = datetime.datetime.strptime(dt_str, EXTEND_DT)
        utc_dt = self.dt2utcdt(dt)
        milli = int(round(utc_dt.microsecond / 1000, 0))
        suffix = '.%03dZ' % milli
        return utc_dt.strftime(EXTEND_T_DT) + suffix

    def utc_str_to_datetime(self, utc_str, utc_format=EXTEND_T_ZONE_DT):
        """ utc 字符串转为 datetime utc_str: """
        utc_dt = datetime.datetime.strptime(utc_str, utc_format)
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(self.tz).replace(tzinfo=None)

    @staticmethod
    def get_date_month_start_and_end(date=None):
        if date is None:
            temp_date = datetime.datetime.now()
        else:
            temp_date = date

        start = datetime.datetime(temp_date.year, temp_date.month, 1)

        wday, days = calendar.monthrange(temp_date.year, temp_date.month)

        end = datetime.datetime(temp_date.year, temp_date.month, days)

        return start, end

    @staticmethod
    def get_every_month(start_time, end_time):
        date_list = []
        while start_time.year < end_time.year or (start_time.month <= end_time.month and start_time.year <= end_time.year):
            date_str = start_time.strftime("%Y-%m")
            date_list.append(date_str)
            start_time += datetime.timedelta(days=28)

        ret = []
        for d_str in date_list:
            if d_str not in ret:
                ret.append(d_str)
        return ret

    @staticmethod
    def get_every_day(start_time, end_time):
        date_list = []
        while start_time <= end_time:
            date_str = start_time.strftime("%Y-%m-%d")
            date_list.append(date_str)
            start_time += datetime.timedelta(days=1)
        return date_list

    @staticmethod
    def get_date_by_str(str=None, fmt=EXTEND_DATE):
        if str is None:
            return datetime.datetime.now()

        return datetime.datetime.strptime(str, fmt)

    def get_dt_with_tz(self, dt):
        """ 返回带有时区信息的时间格式

        如  2020-06-18 17:28:23  变为 2020-06-18 17:28:23+08:00

        :param dt:  datetime 格式，必须是与 self.time_zone 相同时区的时间
        :return:
        """
        return self.tz.localize(dt)

    def utc_with_tz(self, dt):
        """ 标准时间加上时间戳

        如 2020-06-18 00:00:00 -> 2020-06-18 00:00:00+00:00

        :param dt: datetime 格式，必须为 0 时区时间
        """
        return TZ_UTC.localize(dt)

    def winnt_timestamp_to_dt(self, ntstamp, local=True):
        """ 将 windows NT 时间戳转化为 datetime 类型

        windows nt 时间戳实际上是从 1602 年 1 月 1 日 UTC 时间至今的 100 ns 数
        :param ntstamp: 100 ns 数
        :param local: 本地时间还是 UTC 时间 True 返回本地时间 False 返回 UTC 时间
        :return: datetime.datetime 类型 的 UTC 时间
        """
        utc = datetime.datetime(1601, 1, 1) + \
            datetime.timedelta(microseconds=ntstamp//10)

        if local:
            return self.utcdt2dt(utc)

        return utc


class DatetimeUtil(object):
    """ 可封装一些 与 date 或 time 有关的方法 """

    def __init__(self):

        pass

    def datetime_to_weekday(self, source_date):
        """
        :param source_date: datetime类型-- 2020-08-01
        :return: str类型 : "周一"
        """
        week_dic = {0: "周一",
                    1: "周二",
                    2: "周三",
                    3: "周四",
                    4: "周五",
                    5: "周六",
                    6: "周日"
                    }
        week_num = source_date.weekday()
        return week_dic.get(week_num, None)

    @staticmethod
    def date_range(start, end, step=1):
        """ 返回开始时间结束时间内的日期。

        注意: 返回的日期列表包含 start 和 end

         :param start: 开始日期  datetime.date 或 'yyyy-mm-dd'  必须与 end 类型相同
         :param end: 结束日期  datetime.date 或 'yyyy-mm-dd'  必须与 start 类型相同
         :param step: 步长
        """
        is_str = isinstance(start, str)

        if is_str:
            start = datetime.datetime.strptime(start, EXTEND_DATE).date()
            end = datetime.datetime.strptime(end, EXTEND_DATE).date()

        result = [start+datetime.timedelta(days=delta)
                  for delta in range(0, (end-start).days+1, step)]
        if is_str:
            result = [day.strftime(EXTEND_DATE) for day in result]

        return result

    @staticmethod
    def yesterday():
        return datetime.datetime.today() - datetime.timedelta(days=1)

    def get_weekday_le_date(self, date, weekday_number):
        """
        返回 date 或date之前的第一个指定星期几的日期：类型为datetime
        :param date: datetime类型-- 2021-09-25
        :param weekday_number 想要设定的周几 int 类型 例如 周5就输入 4
                    {0: "周一",
                    1: "周二",
                    2: "周三",
                    3: "周四",
                    4: "周五",
                    5: "周六",
                    6: "周日" }
        :return: datetime类型 2021-09-24 (周五)
        """
        week_num = date.weekday()
        if week_num == weekday_number:
            return date
        else:
            if week_num > weekday_number:
                return date - datetime.timedelta(abs(weekday_number-week_num))
            else:
                return date - datetime.timedelta(days=abs(weekday_number - week_num + 5))

    @staticmethod
    def str2dt(dt_str):
        ''' 字符串转 datetime.datetime
        YYYY-mm-dd HH:MM:SS
        YYYY-mm-dd
        '''
        if len(dt_str) == 19:
            return datetime.datetime.strptime(dt_str, EXTEND_DT)
        if len(dt_str) == 12:
            return datetime.datetime.strptime(dt_str, EXTEND_DATE)
        # TODO: 完善其他格式


class IsHoliday(object):
    """ 节假日检测

     未解决国家农历法定节假日检测
    """

    @staticmethod
    def isHoliday(date_like):
        date_like = IsHoliday.get_datetime(date_like)
        w = date_like.strftime('%w')
        if int(w) in [0, 6]:
            return True
        elif (date_like.month, date_like.day) in IsHoliday.legal_holidays():
            return True
        else:
            return 0

    @staticmethod
    def get_datetime(date_like):
        if isinstance(date_like, datetime.date):
            return datetime.datetime.strptime(date_like.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        elif isinstance(date_like, datetime.datetime):
            return date_like
        elif isinstance(date_like, str):
            if date_like.count(':') == 2 and date_like.count('-') == 2 and len(date_like.strip()) == 19:
                return datetime.datetime.strptime(date_like, '%Y-%m-%d %H:%M:%S')
            elif date_like.count(':') == 0 and date_like.count('-') == 2 and len(date_like.strip()) == 10:
                return datetime.datetime.strptime(date_like + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        raise ValueError(date_like)

    @staticmethod
    def legal_holidays():
        # 元组表示的月和日
        new_years_days = [(12, 30), (12, 31), (1, 1)]
        labor_days = [(4, 29), (4, 30), (5, 1)]
        national_days = [(10, d) for d in range(1, 8)]
        all_holidays = new_years_days + labor_days + national_days
        return all_holidays


def get_next_month(month_str):
    """获取下个月的字符串
    :param month_str: 如 2018-09
    :return: 字符串表示的月份: 如 2018-10
    """
    return get_month_later(month_str, 1)


def get_month_later(month_str, interval):
    """获取几个月之后

    :param month_str: 参考月
    :param interval: 间隔，正整数
    :return:
    """
    return get_month_by_interval(month_str, interval)


def get_month_earlier(month_str, interval):
    """获取几个月之前

    :param month_str: 参考月
    :param interval: 间隔，正整数
    :return:
    """
    return get_month_by_interval(month_str, -interval)


def get_month_by_interval(month_str, interval):
    """ 由间隔月份获取新月份 """
    if len(month_str) > 7:
        month_str = month_str[:7]
    year, month = [int(x) for x in month_str.split('-')]
    weight = year * 12 + month - 1
    weight_new = weight + interval
    return "%04d-%02d" % (weight_new // 12, weight_new % 12 + 1)


def get_month_list(start_month, end_month, border=True):
    """获取两个月份之间的所有月份列表

    border: 是否包含两端边界
    """
    month_lst = list()
    start_month, end_month = min(
        start_month, end_month), max(start_month, end_month)
    month = get_next_month(start_month)
    while month < end_month:
        month_lst.append(month)
        month = get_next_month(month)

    if border:
        month_lst = [start_month] + month_lst + [end_month]
    return month_lst


if __name__ == '__main__':

    pass
