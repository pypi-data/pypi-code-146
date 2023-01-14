import datetime

import pymssql
from urllib import parse
import pandas as pd
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine

from crmSaleBilling.metadata import ERP_unAudit, ERP_delete, ERP_Audit

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
option = {
    "acct_id": '63310e555e38b1',
    "user_name": '杨斌',
    "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
    # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    "app_sec": '224f05e7023743d9a0ab51d3bf803741',
    "server_url": 'http://cellprobio.gnway.cc/k3cloud',
}


class CrmToDms():
    # 发票
    def __init__(self):
        # 连接数据库
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn2['DB_USER'], conn2['DB_PASS'],
                                                                        conn2['DB_HOST'],
                                                                        conn2['DB_PORT'], conn2['DATABASE'])
        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                        conn3['DB_HOST'],
                                                                        conn3['DB_PORT'], conn3['DATABASE'])
        self.new_con = pymssql.connect(host='115.159.201.178', database='cprds', user='dms', port=1433,
                                       password='rds@2022', charset='utf8')
        self.new_cursor = self.new_con.cursor()
        self.dms_engine = create_engine(dms_conn)
        self.crm_engine = create_engine(crm_conn)

    def get_salebilling(self, FDate):
        sql = f"""
        select FInvoiceid,FSaleorderno,FDelivaryNo,FBillNO,FBillTypeNumber,FInvoiceType,FCustId,FSaleorderentryseq,FCustName,
        FPrdNumber,FName,Fqty,FUnitprice,Fmoney,FBillTypeId,FNoteType,FBankBillNo,FBillCode,FTaxrate,FInvoicedate,FUpdatetime,FIspackingBillNo,
        FIsDo,FCurrencyName,FDocumentStatus,Fapprovesubmittedtime
        from rds_crm_sales_invoice where Fapprovesubmittedtime > '{FDate}'
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

    def salebilling_to_dms(self, app3, FDate):
        df_sale_order = self.get_salebilling(FDate)
        invoiceId_lis = app3.select("select FBILLNO from RDS_CRM_SRC_sal_billreceivable")
        invoice_lis = []
        for i in invoiceId_lis:
            invoice_lis.append(i['FBILLNO'])
        for i, r in df_sale_order.iterrows():
            if r['FBIllNo'] not in invoice_lis:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                        FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                        FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime)values
                                  ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                  {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                  '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                  '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                        self.new_cursor.execute(sql1)
                        self.new_con.commit()
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据保存成功", 1)
                        print("{}该发票数据已成功保存".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据异常,清检查该条数据", 2)
                        print("{}该发票数据异常".format(r['FBIllNo']))
                else:
                    self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据未批准", 2)
                    print("{}该发票数据未批准".format(r['FBIllNo']))
            else:
                if r["FBIllNo"] != None:
                    sub_sql = f"""select FBIllNo from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}' and FSubmitTime = '{r['Fapprovesubmittedtime']}' and FIsDo = 3
                                   """
                    try:
                        dexist = app3.select(sub_sql)
                        if not dexist:
                            del_sql = f"""
                                        delete from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}'
                                        """
                            self.new_cursor.execute(del_sql)
                            self.new_con.commit()
                            sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                                                   FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                                                   FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime)values
                                                             ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                                             {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                                             '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                                             '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                            self.new_cursor.execute(sql1)
                            self.new_con.commit()
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                '该销售开票已更新', 1
                            )
                            api_sdk = K3CloudApiSdk()
                            api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                               option['app_sec'], option['server_url'])
                            res_Audit = ERP_Audit(api_sdk, r['FBIllNo'])
                            res_unAudit = ERP_unAudit(api_sdk, r['FBIllNo'])
                            res_delete = ERP_delete(api_sdk, r['FBIllNo'])
                            print(res_Audit, res_unAudit, res_delete)
                            print("{}该销售开票已更新".format(r['FBIllNo']))
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_unAudit}', 1
                            )

                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_delete}', 1
                            )
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据已存在", 2)
                        print("{}该发票数据已存在".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售开票', f'{r["FBIllNo"]}', f'{r["FBIllNo"]}该销售开票数据异常', 2)
                        print(f"{r['FBIllNo']}此销售开票数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('销售开票', f'{r["FBIllNo"]}',
                                       "{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']), 2)
                    print("{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']))

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data
