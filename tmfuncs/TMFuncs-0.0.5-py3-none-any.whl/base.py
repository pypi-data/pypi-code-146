# 常用小模块
import datetime
import time


def time_taken(end_time, start_time):
    time_spend = end_time - start_time
    m, s = divmod(time_spend, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def get_date(days=1, str_format='%Y-%m-%d'):
    """
    基于今天的日期，返回指定间隔的日期字符串，
    :param days: 距离“今天”的日期，0表示今天，1表示昨天，依次类推
    :param str_format: 格式化后的字符串
    :return: 字符串格式的日期，例如 2022-12-20
    """
    days = int(days)
    today = datetime.datetime.now()
    the_day = today - datetime.timedelta(days=days)
    return the_day.strftime(str_format)


def get_current_timestamp(str_format='%Y%m%d%H%M%S'):
    return time.strftime(str_format, time.localtime(time.time()))
