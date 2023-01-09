# -*- encoding:utf-8 -*-

import six
from datetime import datetime as dt

K_DEFAULT_DT_FMT = "%Y-%m-%d"


def fmt_date(convert_date):
    """
    将时间格式如20160101转换为2016-01-01日期格式, 注意没有对如 201611
    这样的做fix适配，外部需要明确知道参数的格式，针对特定格式，不使用时间api，
    直接进行字符串解析，执行效率高
    :param convert_date: 时间格式如20160101所示，int类型或者str类型对象
    :return: %Y-%m-%d日期格式str类型对象
    """
    if isinstance(convert_date, float):
        # float先转换int
        convert_date = int(convert_date)
    convert_date = str(convert_date)

    if len(convert_date) > 8 and convert_date.startswith('20'):
        # eg '20160310000000000'
        convert_date = convert_date[:8]

    if '-' not in convert_date:
        if len(convert_date) == 8:
            # 20160101 to 2016-01-01
            convert_date = "%s-%s-%s" % (convert_date[0:4], convert_date[4:6],
                                         convert_date[6:8])
        elif len(convert_date) == 6:
            # 201611 to 2016-01-01
            convert_date = "%s-0%s-0%s" % (
                convert_date[0:4], convert_date[4:5], convert_date[5:6])
        else:
            raise ValueError(
                'fmt_date: convert_date fmt error {}'.format(convert_date))
    return convert_date


def fix_date(date_str):
    """
    修复日期不规范的写法:
                eg. 2016-1-1 fix 2016-01-01
                eg. 2016:01-01 fix 2016-01-01
                eg. 2016,01 01 fix 2016-01-01
                eg. 2016/01-01 fix 2016-01-01
                eg. 2016/01/01 fix 2016-01-01
                eg. 2016/1/1 fix 2016-01-01
                eg. 2016:1:1 fix 2016-01-01
                eg. 2016 1 1 fix 2016-01-01
                eg. 2016 01 01 fix 2016-01-01
                .............................
    不使用时间api，直接进行字符串解析，执行效率高，注意fix_date内部会使用fmt_date
    :param date_str: 检测需要修复的日期str对象或者int对象
    :return: 修复了的日期str对象
    """
    if date_str is not None:
        # 如果是字符串先统一把除了数字之外的都干掉，变成干净的数字串
        if isinstance(date_str, six.string_types):
            # eg, 2016:01-01, 201601-01, 2016,01 01, 2016/01-01 -> 20160101
            date_str = ''.join(list(filter(lambda c: c.isdigit(), date_str)))
        # 再统一确定%Y-%m-%d形式
        date_str = fmt_date(date_str)
        y, m, d = date_str.split('-')
        if len(m) == 1:
            # 月上补0
            m = '0{}'.format(m)
        if len(d) == 1:
            # 日上补0
            d = '0{}'.format(d)
        date_str = "%s-%s-%s" % (y, m, d)
    return date_str


def week_of_date(date_str, fmt=K_DEFAULT_DT_FMT, fix=True):
    """
    输入'2016-01-01' 转换为星期几，返回int 0-6分别代表周一到周日
    :param date_str: 式时间日期str对象
    :param fmt: 如date_str不是%Y-%m-%d形式，对应的格式str对象
    :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
    :return: 返回int 0-6分别代表周一到周日
    """

    if fix and fmt == K_DEFAULT_DT_FMT:
        # 只针对%Y-%m-%d形式格式标准化日期格式
        date_str = fix_date(date_str)
    return dt.strptime(date_str, fmt).weekday()