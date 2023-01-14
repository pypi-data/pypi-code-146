import datetime
from urllib import parse

from k3cloud_webapi_sdk.main import K3CloudApiSdk

from crmSaleOrder.metadata import ERP_delete, ERP_unAudit
import pandas as pd
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine
from crmSaleOrder.metadata import inser_logging

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
    # 销售订单
    def __init__(self):
        # 连接数据库
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn2['DB_USER'], conn2['DB_PASS'],
                                                                        conn2['DB_HOST'],
                                                                        conn2['DB_PORT'], conn2['DATABASE'])
        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                        conn3['DB_HOST'],
                                                                        conn3['DB_PORT'], conn3['DATABASE'])
        self.dms_engine = create_engine(dms_conn)
        self.crm_engine = create_engine(crm_conn)

    def get_sale_order(self,FDate):
        sql = f"""
        select FSaleorderno,FBillTypeIdName,FDate,FCustId,FCustName,FSaleorderentryseq,FPrdnumber,FPruName,Fqty,Fprice,
        Ftaxrate,Ftaxamount,FTaxPrice,FAllamountfor,FSaleDeptName,FSaleGroupName,FUserName,Fdescription,FIsfree,
        FIsDo,Fpurchasedate,FSalePriorityName,FSaleTypeName,Fmoney,FCollectionTerms,FDocumentStatus,Fapprovesubmittedtime
        from rds_crm_sales_saleorder where Fapprovesubmittedtime > '{FDate}'
        """
        df = pd.read_sql(sql, self.crm_engine)
        return df

    def get_custom_form(self):
        sql = """select * from rds_crm_md_customer
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

    def sale_order_to_dms(self, app3,FDate):
        df_sale_order = self.get_sale_order(FDate)
        sOrder_lis = app3.select('select FSaleorderno from RDS_CRM_SRC_sales_order')
        Saleorderentryseq_lis = []
        for i in sOrder_lis:
            Saleorderentryseq_lis.append(i['FSaleorderno'])
        for i, r in df_sale_order.iterrows():
            if r['FSaleorderno'] not in Saleorderentryseq_lis:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sales_order(FInterId,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FPurchaseDate,FUrgency,FSalesType,FCollectionTerms,FUpDateTime,FDocumentStatus,FSubmitTime) values 
                               ({self.getFinterId(app3, 'RDS_ECS_SRC_sales_order') + 1},'{r['FSaleorderno']}','{r['FBillTypeIdName']}','{datetime.date(*map(int, r['FDate'][:10].split('-')))}','{r['FCustId']}','{r['FCustName']}',{r['FSaleorderentryseq']},'{r['FPrdnumber']}','{r['FPruName']}',
                                {r['Fqty']},'{r['Fprice']}','{r['FMoney']}','{r['Ftaxrate']}','{r['Ftaxamount']}','{r['FTaxPrice']}','{r['FAllamountfor']}','{r['FSaleDeptName']}','{r['FSaleGroupName']}','{r['FUserName']}','{r['Fdescription']}',0,0,'{r['Fpurchasedate']}','{r['FSalePriorityName']}','{r['FSaleTypeName']}','{r['FCollectionTerms']}',getdate(),'{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                        app3.insert(sql1)
                        print("{}该销售订单数据已成功保存".format(r['FSaleorderno']))
                    except:

                        inser_logging(app3,
                                      '销售订单CRM同步到SRC', f'{r["FSaleorderno"]}',
                                      f'{r["FSaleorderno"]}此订单数据异常,无法存入SRC,请检查数据',
                                      )
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                else:
                    inser_logging(app3,
                                  '销售订单CRM同步到SRC', f'{r["FSaleorderno"]}',
                                  f'{r["FSaleorderno"]}该销售订单未批准',
                                  )
                    print("{}该销售订单未批准".format(r['FSaleorderno']))
            else:
                sub_sql = f"""select FSALEORDERNO from RDS_CRM_SRC_sales_order where FSALEORDERNO = '{r['FSaleorderno']}' and FSubmitTime = '{r['Fapprovesubmittedtime']}' and FIsDo =1
                """
                dexist = app3.select(sub_sql)
                if not dexist:
                    del_sql = f"""
                    delete from RDS_CRM_SRC_sales_order where FSALEORDERNO = '{r['FSaleorderno']}'
                    """
                    app3.delete(del_sql)
                    sql1 = f"""insert into RDS_CRM_SRC_sales_order(FInterId,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FPurchaseDate,FUrgency,FSalesType,FCollectionTerms,FUpDateTime,FDocumentStatus,FSubmitTime) values 
                                                   ({self.getFinterId(app3, 'RDS_ECS_SRC_sales_order') + 1},'{r['FSaleorderno']}','{r['FBillTypeIdName']}','{datetime.date(*map(int, r['FDate'][:10].split('-')))}','{r['FCustId']}','{r['FCustName']}',{r['FSaleorderentryseq']},'{r['FPrdnumber']}','{r['FPruName']}',
                                                    {r['Fqty']},'{r['Fprice']}','{r['FMoney']}','{r['Ftaxrate']}','{r['Ftaxamount']}','{r['FTaxPrice']}','{r['FAllamountfor']}','{r['FSaleDeptName']}','{r['FSaleGroupName']}','{r['FUserName']}','{r['Fdescription']}',0,0,'{r['Fpurchasedate']}','{r['FSalePriorityName']}','{r['FSaleTypeName']}','{r['FCollectionTerms']}',getdate(),'{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}')"""
                    app3.insert(sql1)
                    api_sdk = K3CloudApiSdk()
                    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                       option['app_sec'], option['server_url'])
                    res_unAudit = ERP_unAudit(api_sdk, r['FSaleorderno'])
                    res_delete = ERP_delete(api_sdk, r['FSaleorderno'])
                    print(res_unAudit, res_delete)
                    print("{}该销售订单已更新".format(r['FSaleorderno']))

                    inser_logging(app3,
                                  '销售订单CRM同步到SRC', f'{r["FSaleorderno"]}',
                                  f'{res_unAudit}'
                                  )

                    inser_logging(app3,
                                  '销售订单CRM同步到SRC', f'{r["FSaleorderno"]}',
                                  f'{res_delete}'
                                  )
                else:
                    inser_logging(app3,
                                  '销售订单CRM同步到SRC', f'{r["FSaleorderno"]}',
                                  "{}该销售订单已存在".format(r['FSaleorderno'])
                                  )
                    print("{}该销售订单已存在".format(r['FSaleorderno']))

    def get_saleorder(self):
        sql = """
            select FBillNo from rds_crm_sales_saleorder_list
        """
        df = pd.read_sql(sql, self.crm_engine)
        sql1 = """
            select FBillNo from RDS_CRM_SRC_saleOrderList
        """
        df_bill = pd.read_sql(sql1, self.dms_engine)
        d_lis = list(df_bill["FBillNo"])
        for i, d in df.iterrows():
            if d[0] in d_lis:
                df = df.drop(i, axis=0)
        if not df.empty:
            df.loc[:, "FIsDo"] = '0'
            df = df.drop_duplicates('FBillNo', keep='first', )
            df.to_sql("RDS_CRM_SRC_saleOrderList", self.dms_engine, if_exists='append', index=False)



if __name__ == '__main__':
    token_erp = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
    app3 = RdClient(token=token_erp)
    c = CrmToDms()
    c.sale_order_to_dms(app3)
    c.get_saleorder()
