from datetime import date, timedelta

import pandas as pd
from BankDetails.bank_test import Account
from BankDetails.config import conn, bank_accounts
from BankDetails.bank_day_details import BankDetail


def get_date_range1(start, end, periods=2, format='%Y-%m-%d'):
    """
    使用pandas库的date_range方法生成日期间隔里的所有日期, start, end, periods和freq必须指定三个
    :param start: 起始日期
    :param end: 结束日期
    :param periods: 周期
    :param freq: 时间间隔
    :param format: 格式化输出
    :return: 日期list
    """
    periods = None if start and end else periods
    date_list = pd.date_range(start=start, end=end, periods=periods, freq='1D')
    if len(date_list) < 2:
        date_list = date_list.union(date_list.shift(1)[-1:])
    return [item.strftime(format) for item in date_list]


def run_updata():
    today = date.today().strftime("%Y-%m-%d")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesday = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
    acc = Account(conn['baseUrl'], conn['orgCode'], conn['secretKey'])
    date_lis = get_date_range1(yesday, tomorrow)
    op_bank = BankDetail()
    for account in bank_accounts:
        for i, d in enumerate(date_lis):
            # acc.account_balance_query(account)
            acc.account_details_query(d, d, account)  # 添加银行账户明细到数据库
            op_bank.get_today_income(d, date_lis[i + 1], account)  # 添加银行账户当天的收入到数据库
            op_bank.get_today_expenditure(d, date_lis[i + 1], account)  # 添加银行账户当天的支出到数据库
            if d == today:
                break
    for account in bank_accounts:
        for i, d in enumerate(date_lis):
            op_bank.updata_balance(account, date_lis[i + 1], d)  # 更新当日收入支出和余额
            if d == yesterday:
                break


if __name__ == '__main__':
    run_updata()
