import datetime
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from BankDetails.bank import Payment
from BankDetails.config import conn, bank_accounts


class Account(Payment):
    def __init__(self, baseUrl, orgCode, secretKey):
        super(Account, self).__init__(baseUrl, orgCode, secretKey)
        # 连接数据库
        connect_info = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn['DB_USER'], conn['DB_PASS'],
                                                                            conn['DB_HOST'],
                                                                            conn['DB_PORT'], conn['DATABASE'])
        self.engine = create_engine(connect_info)
        self.app = Payment(baseUrl=baseUrl, orgCode=orgCode, secretKey=secretKey)

    def get_date_range1(self, start, end, periods=2, freq='1D', format='%Y-%m-%d %H:%M:%S'):
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
        date_list = pd.date_range(start=start, end=end, periods=periods, freq=freq)
        if len(date_list) < 2:
            date_list = date_list.union(date_list.shift(1)[-1:])
        return [item.strftime(format) for item in date_list]

    # 5.3、帐户余额查询
    def account_balance_query(self, accountNo):

        res = self.app.AccBalanceQuery(accountNo)
        col = ['FUniqueCode', 'FCompanyName', 'FAccountNO', 'FBalanceDate', 'FBalance', 'FCurrencyCode', 'FCreateTime']
        create_time = np.array(
            pd.read_sql('select FUniqueCode from RDS_CAS_SRC_BANK where FAccountNO = \'{}\''.format(accountNo),
                        con=self.engine)['FUniqueCode']).tolist()
        FUniqueCode = res.get('accountNo', None) + res.get('balanceDate', None) + res.get('balance', None)
        val = [FUniqueCode]
        if res:
            for v in res.values():
                val.append(v)
            balance_df = pd.DataFrame([val], columns=col)
            if FUniqueCode not in create_time:
                print(balance_df)
                balance_df.to_sql(name='RDS_CAS_SRC_BANK', con=self.engine, if_exists='append', index=False)
            else:
                print(f"账户为{accountNo}的今日余额在已存在于数据库")
        else:
            print(f"账户为{accountNo}余额还未更新")

    # 账户明细查询
    def account_details_query(self, startDate, endDate, accountNo):
        res = self.app.PaymentDetailQuery(startDate=startDate, endDate=endDate, accountNo=accountNo, tradeType='01')
        vals = []
        code_lists = np.array(
            pd.read_sql('select FUniqueCode from RDS_CAS_SRC_Transaction where FAccountNO = \'{}\''.format(accountNo),
                        con=self.engine)['FUniqueCode']).tolist()
        col = ['FBankCode', 'FAmount', 'FAccountName', 'FPurpose', 'FBankName',
               'FVirtualAccNO', 'FOppOpenBankName', 'FSerialNO', 'FTradeTime',
               'FUniqueCode', 'FOppAccountName', 'FCreateTime', 'FAccountNO',
               'FDigest', 'FRecordDate', 'FOppAccountNO', 'FTradeType', 'FIsdo']
        if res['data']:
            for i in res['data']:
                val = []
                for v in i.values():
                    val.append(v)
                if val[9] not in code_lists:
                    val.append(0)
                    vals.append(val)
            details_df = pd.DataFrame(vals, columns=col)
            print(details_df)
            details_df.to_sql(name='RDS_CAS_SRC_Transaction', con=self.engine, if_exists='append', index=False)
        else:
            print(f"账户为{accountNo}在{startDate}没有明细数据")

    def get_date_range(self, begin_date, end_date):
        # 定义日期函数
        date_list = []
        while begin_date <= end_date:
            date_list.append(begin_date)
            begin_date_object = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
            days1_timedelta = datetime.timedelta(days=1)
            begin_date = (begin_date_object + days1_timedelta).strftime("%Y-%m-%d")
        return date_list
