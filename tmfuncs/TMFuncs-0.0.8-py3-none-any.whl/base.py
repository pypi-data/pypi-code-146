# 常用小模块
import datetime
import time
from pytz import timezone


def time_taken(end_time, start_time):
    time_spend = end_time - start_time
    m, s = divmod(time_spend, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def get_date(days=1, str_format='%Y-%m-%d', time_zone='Asia/Shanghai', current_day=None):
    """
    基于今天的日期，返回指定间隔的日期字符串，
    :param days: 距离“今天”的日期，0表示今天，1表示昨天，依次类推
    :param str_format: 格式化后的字符串
    :param time_zone: 目标时间的时区，例如 Asia/Shanghai，America/New_York
    :param current_day: 当前日志，默认是字符串格式
    :return: 字符串格式的日期，例如 2022-12-20
    """
    # 获取当天时间——服务器时间
    if current_day is None: # 如果不指定，则使用系统当前日期
        dt_loc_today = datetime.datetime.now()
    else: # 否则使用指定的
        dt_loc_today = datetime.datetime.strptime(current_day, str_format)
    # 获取对应时区的时间——转换为目标时区时间
    utc8 = timezone(time_zone)
    dt_utc8 = dt_loc_today.astimezone(utc8)
    # 获取日期间隔的时间——基于目标时区时间
    the_day = dt_utc8 - datetime.timedelta(days=int(days))
    return the_day.strftime(str_format)


def get_current_timestamp(str_format='%Y%m%d%H%M%S'):
    return time.strftime(str_format, time.localtime(time.time()))
