import datetime
from urllib import parse

from k3cloud_webapi_sdk.main import K3CloudApiSdk
import pandas as pd
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine
from crmNoticeShipment.metadata import ERP_delete, ERP_unAudit
import pymssql

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

token_erp = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
app3 = RdClient(token=token_erp)


class CrmToDms():
    # 出库
    def __init__(self):
        # 连接数据库

        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                        conn3['DB_HOST'],
                                                                        conn3['DB_PORT'], conn3['DATABASE'])
        self.new_con = pymssql.connect(host='115.159.201.178', database='cprds', user='dms', port=1433,
                                       password='rds@2022', charset='utf8')
        self.new_cursor = self.new_con.cursor()
        self.crm_engine = create_engine(crm_conn)

        # self.new_con = pymssql.connect(host='115.159.201.178', database='cprds', user='dms', port=1433,
        #                                password='rds@2022', charset='utf-8')
        # self.new_cursor = self.new_con.cursor()

    def get_sale_notice(self, FDate):
        sql = f"""
        select FSaleorderno,FDelivaryNo,FBillTypeIdName,Fdeliverystatus,Fdeliverydate,Fstock,FCustId,FCustName,
        FprNumber,FName,Fcostprice,FPrice,Fqty,Flot,FProductdate,FEffectivedate,FUnit,FdeliverPrice,Ftaxrate,
        FUserName,FOnlineSalesName,FCheakstatus,FMofidyTime,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FDocumentStatus,Fapprovesubmittedtime
        from rds_crm_shippingadvice where Fapprovesubmittedtime >'{FDate}'
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

    def sale_notice(self, app3, FDate):
        df_sale_order = self.get_sale_notice(FDate)
        cust_list = app3.select('select FDELIVERYNO from RDS_CRM_SRC_sal_delivery')
        cus_list = []
        for i in cust_list:
            cus_list.append(i['FDELIVERYNO'])
        for i, r in df_sale_order.iterrows():
            if r['FDelivaryNo'] not in cus_list and r['FDelivaryNo']:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sal_delivery(FINTERID,FTRADENO,FDELIVERYNO,FBILLTYPE,FDELIVERYSTATUS,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,
                                                        FORDERTYPE,FPRDNUMBER,FPRDNAME,FCOSTPRICE,FPRICE,FNBASEUNITQTY,FLOT,FPRODUCEDATE,FEFFECTIVEDATE,
                                                        FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,FCHECKSTATUS,UPDATETIME,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FDocumentStatus,FSubmitTime ) values
                                                      ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_delivery') + 1},'{r['FSaleorderno']}','{r['FDelivaryNo']}',
                                                      '{r['FBillTypeIdName']}','{r['Fdeliverystatus']}','{r['Fstock']}','{r['FCustId']}','{r['FCustName']}','含预售',
                                                      '{r['FprNumber']}','{r['FName']}',{r['FCostPrice']},{r['FPrice']},{r['Fqty']},'{r['Flot']}','{r['FProductdate']}',
                                                      '{r['FEffectivedate']}','{r['FUnit']}',100,'{r['Ftaxrate']}','{r['FUserName']}','{r['FOnlineSalesName']}',
                                                      '{r['FCheakstatus']}','{r['FMofidyTime']}',0,0,'{r['FDATE']}',0,'{r['FOUTID']}','{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                        self.new_cursor.execute(sql1)
                        self.new_con.commit()
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}此订单成功保存至CRM',
                                           1)
                        print("{}该发货通知单已成功保存".format(r['FDelivaryNo']))
                    except:
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}此订单数据异常,无法存入SRC,请检查数据',
                                           2)
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                        print("{}该发货通知单数据异常".format(r['FDelivaryNo']))
                else:
                    self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单已存在', 2)
                    print("{}该发货通知单未批准".format(r['FDelivaryNo']))
            else:
                if r["FDelivaryNo"] != None:
                    sub_sql = f"""select FDELIVERYNO from RDS_CRM_SRC_sal_delivery where FDELIVERYNO = '{r["FDelivaryNo"]}' and FSubmitTime = '{r["Fapprovesubmittedtime"]}' and FIsDo =3
                                   """
                    try:
                        dexist = app3.select(sub_sql)
                        if not dexist:
                            del_sql = f"""
                                                delete from RDS_CRM_SRC_sal_delivery where FDELIVERYNO = '{r["FDelivaryNo"]}'
                                                """
                            app3.delete(del_sql)
                            sql1 = f"""insert into RDS_CRM_SRC_sal_delivery(FINTERID,FTRADENO,FDELIVERYNO,FBILLTYPE,FDELIVERYSTATUS,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,
                                                                                   FORDERTYPE,FPRDNUMBER,FPRDNAME,FCOSTPRICE,FPRICE,FNBASEUNITQTY,FLOT,FPRODUCEDATE,FEFFECTIVEDATE,
                                                                                   FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,FCHECKSTATUS,UPDATETIME,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FDocumentStatus,FSubmitTime ) values
                                                                                 ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_delivery') + 1},'{r['FSaleorderno']}','{r['FDelivaryNo']}',
                                                                                 '{r['FBillTypeIdName']}','{r['Fdeliverystatus']}','{r['Fstock']}','{r['FCustId']}','{r['FCustName']}','含预售',
                                                                                 '{r['FprNumber']}','{r['FName']}',{r['FCostPrice']},{r['FPrice']},{r['Fqty']},'{r['Flot']}','{r['FProductdate']}',
                                                                                 '{r['FEffectivedate']}','{r['FUnit']}',100,'{r['Ftaxrate']}','{r['FUserName']}','{r['FOnlineSalesName']}',
                                                                                 '{r['FCheakstatus']}','{r['FMofidyTime']}',0,0,'{r['FDATE']}',0,'{r['FOUTID']}','{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                            self.new_cursor.execute(sql1)
                            self.new_con.commit()
                            print("{}该发货通知单已更新".format(r['FDelivaryNo']))
                            api_sdk = K3CloudApiSdk()
                            api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                               option['app_sec'], option['server_url'])
                            res_unAudit = ERP_unAudit(api_sdk, r['FDelivaryNo'])
                            res_delete = ERP_delete(api_sdk, r['FDelivaryNo'])
                            print(res_unAudit, res_delete)
                            self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单已更新', 1)
                        else:
                            self.inser_logging(
                                          '发货通知单', f'{r["FDelivaryNo"]}',
                                          "{}该发货通知单已存在".format(r['FDelivaryNo']), 2
                                          )
                            print("{}该发货通知单已存在".format(r['FDelivaryNo']))
                    except:
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单数据异常', 2)
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}',
                                       "{}该销售订单没有下推到发货通知单".format(r['FSaleorderno']), 2)
                    print("{}该销售订单没有下推到发货通知单".format(r['FSaleorderno']))

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data
