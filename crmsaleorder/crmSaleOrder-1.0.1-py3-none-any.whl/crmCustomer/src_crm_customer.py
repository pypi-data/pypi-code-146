import datetime
from urllib import parse

import pymssql
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient

from crmCustomer.Metadata import ERP_delete, ERP_unAudit, ERP_CancelAllocate
from crmCustomer import Utility as rc
import pandas as pd
from sqlalchemy import create_engine

bad_password1 = 'rds@2022'
conn2 = {'DB_USER': 'dms',
         'DB_PASS': parse.quote_plus(bad_password1),
         'DB_HOST': '115.159.201.178',
         'DB_PORT': 1433,
         'DATABASE': 'cprds',
         }
bad_password2 = 'lingdangcrm123!@#'
conn3 = {'DB_USER': 'lingdang',
         'DB_PASS': parse.quote_plus(bad_password2),
         'DB_HOST': '123.207.201.140',
         'DB_PORT': 33306,
         'DATABASE': 'ldcrm',
         }

conn1 = {'DB_USER': 'dms',
         'DB_PASS': parse.quote_plus(bad_password1),
         'DB_HOST': '58.211.213.34',
         'DB_PORT': 1433,
         'DATABASE': 'AIS20220926102634',
         }

option = {
    "acct_id": '63310e555e38b1',
    "user_name": '杨斌',
    "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
    # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    "app_sec": '224f05e7023743d9a0ab51d3bf803741',
    "server_url": 'http://cellprobio.gnway.cc/k3cloud',
}


class CrmToDms():
    # 销售订单
    def __init__(self):
        # 连接数据库
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn2['DB_USER'], conn2['DB_PASS'],
                                                                        conn2['DB_HOST'],
                                                                        conn2['DB_PORT'], conn2['DATABASE'])
        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                        conn3['DB_HOST'],
                                                                        conn3['DB_PORT'], conn3['DATABASE'])
        self.crm_con = pymssql.connect(host='58.211.213.34', database='AIS20220926102634', user='dms', port=1433,
                                       password='rds@2022')
        self.new_cursor = self.crm_con.cursor()
        self.dms_engine = create_engine(dms_conn)
        self.crm_engine = create_engine(crm_conn)

    def get_customer(self, FDate):
        sql = f"""
        select FApplyOrgName,FApplierName,FDate,FCustId,FNumber,FName,
        FShortName,FINVOICETITLE,FBankName,FINVOICEADDRESS,
        FINVOICETEL,FAccountNumber,FRECCONDITIONNO,FINVOICETYPE,
        FTaxRate,FPRICELISTNO,FCONTACT,FMOBILE,FBizAddress,
        FCOUNTRY,FPROVINCIAL,FTAXREGISTERCODE,FTEL,FSalesGroupNo,
        FAalesDeptName,FDeptNumber,FDeptName,FSaleGroupNumber,
        FSaleGroupName,FSalesman,FSETTLETYPENO,FEmpNumber,
        FTRADINGCURRNO,FUploadDate,F_SZSP_KHFLNo,FCustTypeNo,
        FGroupNo,F_SZSP_KHZYJBNo,FIsdo,F_SZSP_BLOCNAME,
        F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo,F_SZSP_Text,
        Fapprovestatus
        from rds_crm_md_customer WHERE FUploadDate > '{FDate}'
        """
        df = pd.read_sql(sql, self.crm_engine)
        return df

    def getFinterId(self, app2, tableName):
        '''
        在两张表中找到最后一列数据的索引值
        :param app2: sql语句执行对象
        :param tableName: 要查询数据对应的表名表名
        :return:
        '''

        sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"

        res = app2.select(sql)

        return res[0]['FMaxId']

    def crm_customer(self, app3, app2, FDate):
        df_sale_order = self.get_customer(FDate)
        cust_lis = app3.select('select FNumber from RDS_CRM_SRC_Customer')
        custNum_lis = []
        for i in cust_lis:
            custNum_lis.append(i['FNumber'])
        for i, r in df_sale_order.iterrows():
            if r['FNumber'] not in custNum_lis:
                if r['Fapprovestatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_Customer(FInterId,FApplyOrgName,FApplierName,FDate,FCustId,FNumber,FName,
                                            FShortName,FINVOICETITLE,FBankName,FINVOICEADDRESS,
                                            FINVOICETEL,FAccountNumber,FRECCONDITIONNO,FINVOICETYPE,
                                            FTaxRate,FPRICELISTNO,FCONTACT,FMOBILE,FBizAddress,
                                            FCOUNTRY,FPROVINCIAL,FTAXREGISTERCODE,FTEL,FSalesGroupNo,
                                            FAalesDeptName,FDeptNumber,FDeptName,FSaleGroupNumber,
                                            FSaleGroupName,FSalesman,FSETTLETYPENO,FEmpNumber,
                                            FTRADINGCURRNO,FUploadDate,F_SZSP_KHFLNo,FCustTypeNo,
                                            FGroupNo,F_SZSP_KHZYJBNo,FIsdo,F_SZSP_BLOCNAME,
                                            F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo,F_SZSP_Text,
                                            Fapprovestatus) values 
                               ({self.getFinterId(app3, 'RDS_CRM_SRC_Customer') + 1},'{r['FApplyOrgName']}',
                            '{r['FApplierName']}','{r['FDate']}','{r['FCustId']}','{r['FNumber']}','{r['FName']}','{r['FShortName']}',
                                '{r['FINVOICETITLE']}','{r['FBankName']}','{r['FINVOICEADDRESS']}','{r['FINVOICETEL']}',
                                '{r['FAccountNumber']}','{r['FRECCONDITIONNO']}',
                            '{r['FINVOICETYPE']}','{r['FTaxRate']}','{r['FPRICELISTNO']}','{r['FCONTACT']}','{r['FMOBILE']}','{r['FBizAddress']}','{r['FCOUNTRY']}',
                            '{r['FPROVINCIAL']}',
                            '{r['FTAXREGISTERCODE']}',
                            '{r['FTEL']}','{r['FSalesGroupNo']}','{r['FAalesDeptName']}',
                            '{r['FDeptNumber']}','{r['FDeptName']}','{r['FSaleGroupNumber']}',
                            '{r['FSaleGroupName']}','{r['FSalesman']}','{r['FSETTLETYPENO']}',
                            '{r['FEmpNumber']}','{r['FTRADINGCURRNO']}','{r['FUploadDate']}',
                            '{r['F_SZSP_KHFLNo']}','{r['FCustTypeNo']}',
                            '{r['FGroupNo']}','{r['F_SZSP_KHZYJBNo']}',0,'{r['F_SZSP_BLOCNAME']}',
                            '{r['F_SZSP_KHGHSXNo']}','{r['F_SZSP_XSMSNo']}','{r['F_SZSP_XSMSSXNo']}','{r['F_SZSP_Text']}','{r['Fapprovestatus']}')
                        """
                        app3.insert(sql1)
                        self.inser_logging('客户', f'{r["FNumber"]}', f'{r["FNumber"]}此订单已成功保存', FIsdo=1)
                        print("{}该客户数据已成功保存".format(r['FNumber']))
                    except:
                        self.inser_logging('客户', f'{r["FNumber"]}', f'{r["FNumber"]}此订单数据异常,无法存入SRC,请检查数据',
                                           FIsdo=2)
                        print(f"{r['FNumber']}此订单数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('客户', f'{r["FNumber"]}', f'{r["FNumber"]}该销售订单未批准', FIsdo=2)
                    print("{}该客户未批准".format(r['FNumber']))
            else:
                sub_sql = f"""select FNumber from RDS_CRM_SRC_Customer where FNumber = '{r['FNumber']}' and FUploadDate = '{r['FUploadDate']}' and FIsDo =1
                """
                dexist = app3.select(sub_sql)
                if not dexist:
                    del_sql = f"""
                    delete from RDS_CRM_SRC_Customer where FNumber = '{r['FNumber']}'
                    """
                    app3.delete(del_sql)
                    sql1 = f"""insert into RDS_CRM_SRC_Customer(FInterId,FApplyOrgName,FApplierName,FDate,FCustId,FNumber,FName,
                                                              FShortName,FINVOICETITLE,FBankName,FINVOICEADDRESS,
                                                              FINVOICETEL,FAccountNumber,FRECCONDITIONNO,FINVOICETYPE,
                                                              FTaxRate,FPRICELISTNO,FCONTACT,FMOBILE,FBizAddress,
                                                              FCOUNTRY,FPROVINCIAL,FTAXREGISTERCODE,FTEL,FSalesGroupNo,
                                                              FAalesDeptName,FDeptNumber,FDeptName,FSaleGroupNumber,
                                                              FSaleGroupName,FSalesman,FSETTLETYPENO,FEmpNumber,
                                                              FTRADINGCURRNO,FUploadDate,F_SZSP_KHFLNo,FCustTypeNo,
                                                              FGroupNo,F_SZSP_KHZYJBNo,FIsdo,F_SZSP_BLOCNAME,
                                                              F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo,F_SZSP_Text,
                                                              Fapprovestatus) values 
                                                 ({self.getFinterId(app3, 'RDS_CRM_SRC_Customer') + 1},'{r['FApplyOrgName']}',
                                              '{r['FApplierName']}','{r['FDate']}','{r['FCustId']}','{r['FNumber']}','{r['FName']}','{r['FShortName']}',
                                                  '{r['FINVOICETITLE']}','{r['FBankName']}','{r['FINVOICEADDRESS']}','{r['FINVOICETEL']}',
                                                  '{r['FAccountNumber']}','{r['FRECCONDITIONNO']}',
                                              '{r['FINVOICETYPE']}','{r['FTaxRate']}','{r['FPRICELISTNO']}','{r['FCONTACT']}','{r['FMOBILE']}','{r['FBizAddress']}','{r['FCOUNTRY']}',
                                              '{r['FPROVINCIAL']}',
                                              '{r['FTAXREGISTERCODE']}',
                                              '{r['FTEL']}','{r['FSalesGroupNo']}','{r['FAalesDeptName']}',
                                              '{r['FDeptNumber']}','{r['FDeptName']}','{r['FSaleGroupNumber']}',
                                              '{r['FSaleGroupName']}','{r['FSalesman']}','{r['FSETTLETYPENO']}',
                                              '{r['FEmpNumber']}','{r['FTRADINGCURRNO']}','{r['FUploadDate']}',
                                              '{r['F_SZSP_KHFLNo']}','{r['FCustTypeNo']}',
                                              '{r['FGroupNo']}','{r['F_SZSP_KHZYJBNo']}',0,'{r['F_SZSP_BLOCNAME']}',
                                              '{r['F_SZSP_KHGHSXNo']}','{r['F_SZSP_XSMSNo']}','{r['F_SZSP_XSMSSXNo']}','{r['F_SZSP_Text']}','{r['Fapprovestatus']}')
                                          """
                    app3.insert(sql1)
                    self.inser_logging('客户', f'{r["FNumber"]}', '该客户信息已更新', FIsdo=1)
                    print("{}该客户数据已更新".format(r['FNumber']))
                    api_sdk = K3CloudApiSdk()
                    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                       option['app_sec'], option['server_url'])
                    FNumber = \
                    app2.select("select FNumber from rds_vw_customer where FNAME = '{}'".format(r['FName']))[0][
                        'FNumber']
                    res_unAudit = ERP_unAudit(api_sdk, FNumber)
                    res_cancelallocate = ERP_CancelAllocate(app2, rc, api_sdk, FNumber, r['FApplyOrgName'])
                    res_delete = ERP_delete(api_sdk, FNumber)
                    print(res_cancelallocate, res_unAudit, res_delete)

                    self.inser_logging('客户', f'{r["FNumber"]}', f'{res_unAudit}', FIsdo=1)

                    self.inser_logging('客户', f'{r["FNumber"]}', f'{res_delete}', FIsdo=1)
                else:
                    self.inser_logging('客户', f'{r["FNumber"]}', "{}该客户已存在".format(r['FNumber']), FIsdo=2)
                    print("{}该客户已存在".format(r['FNumber']))

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data

    def queryDocuments(self, number, name):
        sql = f"""
            select a.FNUMBER,a.FCUSTID,a.FMASTERID,a.FUSEORGID,a.FCREATEORGID from T_BD_Customer a
            where a.FNUMBER = '{number}' and a.FUSEORGID = '{name}'
            """
        self.new_cursor.execute(sql)
        Funmber = self.new_cursor.fetchone()[1]

        if Funmber:

            return Funmber

        else:

            return "0"
