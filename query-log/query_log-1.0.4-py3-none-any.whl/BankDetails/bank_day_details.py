import pymssql
from sqlalchemy import create_engine
import pandas as pd
import threading
from BankDetails.config import conn, bank_accounts


class BankDetail():
    def __init__(self):
        # 连接数据库
        self.connect_info = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn['DB_USER'], conn['DB_PASS'],
                                                                                 conn['DB_HOST'],
                                                                                 conn['DB_PORT'], conn['DATABASE'])
        self.dms = pymssql.connect(host=conn['DB_HOST'], database=conn['DATABASE'], user=conn['DB_USER'],
                                   password='rds@2022', charset='utf8')
        self.engine = create_engine(self.connect_info)
        self.dms_cursor = self.dms.cursor()

    def get_balance(self, account, Fdatetime):
        """
        :param account: 银行账号
        :param Fdatetime: 日期
        :return: 对应日期的银行账号余额
        """
        sql = """select FBalance from RDS_CAS_SRC_Details where FDate ='{}' 
        and FAccountNo = '{}'
        """.format(Fdatetime, account)
        df = pd.read_sql(sql, self.engine)
        return df['FBalance'][0]

    def get_date_range1(self, start, end, periods=2, format='%Y-%m-%d'):
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

    def get_today_income(self, start, end, account):
        """

        :param start: 起始日期
        :param end: 结束日期
        :param account: 银行账户
        :return: 将起始日期到结束日期对应的银行账号收入插入数据库
        """
        global amount
        sql = 'select FTradeType,FAccountNO,FTradeTime,FAmount from RDS_CAS_SRC_Transaction where FAccountNO = \'{}\' and FIsdo = 0 and FTradeType = 03 and  FTradeTime BETWEEN \'{}\' and \'{}\''.format(
            account, start, end)
        df = pd.read_sql(sql, self.engine)
        all_amount = 0

        if not df.empty:
            for i in df['FAmount'].tolist():
                all_amount += round(float(i), 2)
            code = account + str(all_amount) + start
            df_amount = pd.DataFrame([[code, account, all_amount, start]],
                                     columns=["FCode", "FAccount ", "FAmount", "FDate"])
        else:
            code = account + "0" + start
            df_amount = pd.DataFrame([[code, account, '0', start]], columns=["FCode", "FAccount ", "FAmount", "FDate"])
        sql = "select FCode from RDS_CAS_SRC_Income where FAccount = '{}' and FDate = '{}'".format(account, start)
        df_find = pd.read_sql(sql, self.engine)
        if df_find.empty:
            df_amount.to_sql("RDS_CAS_SRC_Income", con=self.engine, if_exists='append', index=False)
            print(df_amount)
        else:
            try:
                up_sql = "update a set a.FAmount = '{}' from RDS_CAS_SRC_Income a where FAccount = '{}' and FDate = '{}'".format(
                    all_amount, account, start)
                self.dms_cursor.execute(up_sql)
                self.dms.commit()
            except:
                pass

        return df_amount

    def get_today_expenditure(self, start, end, account):
        """
        :param start: 起始日期
        :param end: 结束日期
        :param account: 银行账户
        :return: 将起始日期到结束日期对应的银行账号支出插入数据库
        """
        sql = 'select FTradeType,FAccountNO,FTradeTime,FAmount from RDS_CAS_SRC_Transaction where FAccountNO = \'{}\' and FIsdo = 0 and FTradeType = 02 and  FTradeTime BETWEEN \'{}\' and \'{}\''.format(
            account, start, end)
        df = pd.read_sql(sql,
                         self.engine)
        all_amount = 0
        if not df.empty:
            for i in df['FAmount'].tolist():
                all_amount -= round(float(i), 2)
            code = account + str(all_amount) + start
            df_expenditure = pd.DataFrame([[code, account, all_amount, start]],
                                          columns=["FCode", "FAccount ", "FAmount", "FDate"])
        else:
            code = account + '0' + start
            df_expenditure = pd.DataFrame([[code, account, '0', start]], columns=["FCode", "FAccount ", "FAmount", "FDate"])
        sql = "select FCode from RDS_CAS_SRC_Iexpenditure where  FAccount = '{}' and FDate = '{}'".format(account, start)
        df_find = pd.read_sql(sql, self.engine)
        if df_find.empty:
            df_expenditure.to_sql("RDS_CAS_SRC_Iexpenditure", con=self.engine, if_exists='append', index=False)
            print(df_expenditure)
        else:
            up_sql = "update a set a.FAmount = '{}' from RDS_CAS_SRC_Iexpenditure a where FAccount = '{}' and FDate = '{}'".format(
                all_amount, account, start)
            self.dms_cursor.execute(up_sql)
            self.dms.commit()
        return df_expenditure

    def get_details(self, account):
        """
        从起始日开始往后推算
        :param account: 银行账号
        :return:
        """
        balance_lis = []
        income = []
        expenditure = []
        code = []
        acc_lis = [account]
        sql = """
        SELECT a.FAccount,a.FAmount income,a.FDate,b.FAmount expenditure from RDS_CAS_SRC_Income a INNER JOIN RDS_CAS_SRC_Iexpenditure b on a.FAccount=b.FAccount and a.[FDate] = b.[FDate] where a.FAccount = '{}'
        """.format(account)
        df = pd.read_sql(sql, self.engine)
        df_one = df.query("date=='{}'".format(date_lis[0]))
        balance_first = 11925996.05 + float(df_one['income']) + float(df_one['expenditure'])
        balance_lis.append(balance_first)
        income.append(float(df_one['income']))
        expenditure.append(float(df_one['expenditure']))
        code.append(str(balance_first) + date_lis[0])
        for d in date_lis[1:]:
            df_first = df.query("date=='{}'".format(d))
            if not df_first.empty:
                balance_o = float(balance_lis[-1]) + float(df_first['income']) + float(df_first['expenditure'])
                balance_lis.append(balance_o)
                income.append(df_first.iloc[0]['income'])
                expenditure.append(df_first.iloc[0]['expenditure'])
                code.append(str(balance_o) + d)
                acc_lis.append(account)
        fin_df = pd.DataFrame([code, acc_lis, balance_lis, income, expenditure, date_lis],
                              index=["code", 'account', 'balance', 'income', 'expenditure', 'date']
                              ).T
        fin_df.to_sql("RDS_CAS_SRC_Details", con=self.engine, if_exists='append', index=False)
        return fin_df

    def get_before_details(self, account):
        """
        从起始日开始往前推算
        :param account: 银行账号
        :return:
        """
        balance_lis = []
        income = []
        expenditure = []
        code = []
        acc_lis = [account]
        sql = """
        SELECT a.FAccount,a.FAmount income,a.FDate,b.FAmount expenditure from RDS_CAS_SRC_Income a INNER JOIN RDS_CAS_SRC_Iexpenditure b on a.FAccount=b.FAccount and a.[FDate] = b.[FDate] where a.FAccount = '{}'
        """.format(account)
        df = pd.read_sql(sql, self.engine)
        df_one = df.query("FDate=='{}'".format(date_lis[0]))
        balance_first = 532231.25
        balance_lis.append(balance_first)
        income.append(float(df_one['income']))
        expenditure.append(float(df_one['expenditure']))
        code.append(str(balance_first) + date_lis[0])
        for i, d in enumerate(date_lis[1:]):
            df_first = df.query("FDate=='{}'".format(date_lis[i]))
            df_today = df.query("FDate=='{}'".format(d))
            if not df_first.empty:
                balance_o = float(balance_lis[-1]) - float(df_first['income']) - float(df_first['expenditure'])
                balance_lis.append(balance_o)
                income.append(df_today.iloc[0]['income'])
                expenditure.append(df_today.iloc[0]['expenditure'])
                code.append(str(balance_o) + d)
                acc_lis.append(account)
        fin_df = pd.DataFrame([code, acc_lis, balance_lis, income, expenditure, date_lis],
                              index=["FCode", 'FAccount', 'FBalance', 'FIncome', 'FExpenditure', 'FDate']
                              ).T

        fin_df.to_sql("RDS_CAS_SRC_Details", con=self.engine, if_exists='append', index=False)
        return fin_df

    def updata_balance(self, account, tdate, ydate):
        """
        更新当日收入支出和余额
        :param account: 银行账号
        :param tdate: 今日日期
        :param ydate: 昨日日期
        :return:
        """
        sql = """
               SELECT a.FAccount,a.FAmount income,a.FDate,b.FAmount expenditure from RDS_CAS_SRC_Income a 
               INNER JOIN RDS_CAS_SRC_Iexpenditure b on a.FAccount=b.FAccount and a.[FDate] = b.[FDate]  where a.FAccount = '{}'
               and a.[FDate] = '{}' 
               """.format(account, tdate)
        df = pd.read_sql(sql, self.engine)
        new_sql = """select FBalance from RDS_CAS_SRC_Details where FDate = '{}' and FAccount = '{}'
        """.format(ydate, account)
        update_df = pd.read_sql(new_sql, self.engine)
        today_sql = """select FBalance from RDS_CAS_SRC_Details where FDate = '{}' and FAccount = '{}'
        """.format(tdate, account)
        today_df = pd.read_sql(today_sql, self.engine)
        if not today_df.empty:
            income = float(df['income'][0])
            expenditure = float(df['expenditure'][0])
            balance = update_df['FBalance'][0] + income + expenditure
            code = str(balance) + ydate
            up_sql = """update a set a.FCode='{}',a.FBalance='{}',a.FIncome='{}',a.FExpenditure='{}' from RDS_CAS_SRC_Details a where  FDate = '{}' and FAccount = '{}'
            """.format(code, balance, income, expenditure, tdate, account)
            self.dms_cursor.execute(up_sql)
            self.dms.commit()
            print("{}该账户在{}的收入、支出和余额已更新".format(account, tdate))
        else:
            income = float(df['income'][0])
            expenditure = float(df['expenditure'][0])
            balance = update_df['balance'][0] + income + expenditure
            code = str(balance) + ydate
            fin_df = pd.DataFrame([code, account, balance, income, expenditure, tdate],
                                  index=["FCode", 'FAccount', 'FBalance', 'FIncome', 'FExpenditure', 'FDate']
                                  ).T
            print("{}该账户在{}的收入、支出和余额已插入".format(account, tdate))
            fin_df.to_sql("RDS_CAS_SRC_Details", con=self.engine, if_exists='append', index=False)


if __name__ == '__main__':
    op_bank = BankDetail()
    date_lis = op_bank.get_date_range1('2022-08-01', '2022-11-30')
    date_lis.reverse()
    # for i, j in enumerate(date_lis):
#         # thread1 = threading.Thread(name='t1', target=op_bank.get_today_income, args=(j, date_lis[i + 1], b))
#         # thread2 = threading.Thread(name='t2', target=op_bank.get_today_expenditure, args=(j, date_lis[i + 1], b))
#         # thread1.start()  # 启动线程1
#         # thread2.start()  # 启动线程2
#         print(op_bank.get_today_income(j, date_lis[i + 1], b))
#         print(op_bank.get_today_expenditure(j, date_lis[i + 1], b))
#         if j == '2022-11-29':
#             break
    print(op_bank.get_before_details('552177553917'))

# date_lis = op_bank.get_date_range1('2022-08-01', '2022-11-26')
