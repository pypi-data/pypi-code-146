from urllib import parse

from pyrda.dbms.rds import RdClient
from requests import *
from sqlalchemy import create_engine
import pandas as pd

from erp2crmsaleout.config import conn3

'''
* http://123.207.201.140:88/test/crmapi-demo/outboundorder.php
'''

bad_password1 = 'rds@2022'
conn = {'DB_USER': 'dms',
        'DB_PASS': parse.quote_plus(bad_password1),
        'DB_HOST': '115.159.201.178',
        'DB_PORT': 1433,
        'DATABASE': 'cprds',
        }
dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn['DB_USER'], conn['DB_PASS'],
                                                                conn['DB_HOST'],
                                                                conn['DB_PORT'], conn['DATABASE'])
crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                conn3['DB_HOST'],
                                                                conn3['DB_PORT'], conn3['DATABASE'])
dms_engine = create_engine(dms_conn)
crm_engine = create_engine(crm_conn)

token_china = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
app3 = RdClient(token=token_china)
erp_token = "4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227"
app2 = RdClient(token=erp_token)


def back2CRM(data):
    r = post(url="http://123.207.201.140:3000/crmapi/add", json=data)
    res = r.json()
    return res


def get_data():
    sql = """
            select * from RDS_CRM_SRC_saleic where FIsdo =0
        """
    data = pd.read_sql(sql, dms_engine, )
    saleorderno_lis = data['salesorder_no'].values
    d_lis = set(saleorderno_lis)
    ret_data = []
    for i in d_lis:
        d = data[data['salesorder_no'] == i]
        d = d.set_index('index')
        print(d)
        materisals = materials_no(d)
        res = save_salebilling(d, materisals)
        ret_data.append(res)
    ret_dict = {
        'code': '1',
        'message': ret_data
    }
    return ret_dict


def materials_no(data):
    data_lis = []
    for i, d in data.iterrows():
        model = {
            "product_no": d['FMATERIALID'],
            "salesorder_no": d['salesorder_no'],
        }
        data_lis.append(model)
    return data_lis


def save_salebilling(d, materisals):
    sql = 'select FNUMBER,FNAME from rds_vw_customer where FCUSTID = {}'.format(d['FCUSTOMERID'][0])
    cus = app2.select(sql)
    sql_cus = "select account_no from ld_account where accountname = '{}'".format(cus[0]['FNAME'])
    df_cust = pd.read_sql(sql_cus, crm_engine)
    print(df_cust)
    if not df_cust.empty:
        account_no = df_cust['account_no'][0]
        data = {
            "module": "invoice",
            "data": [
                {
                    "mainFields": {
                        "invoice_no": d['invoice_no'][0],
                        "account_no": account_no,
                        "invoicetype": '增票' if d['F_SZSP_XSLX'][0] == '62d8b3a30d26ff' else '普票',
                        "invoice_num": str(d['FINVOICENO'][0]),

                    },
                    "detailFields": materisals
                }
            ]
        }
        sql = "update a set a.FisDo=1 from RDS_CRM_SRC_saleic a where salesorder_no = '{}'".format(
            d['salesorder_no'][0])
        app3.update(sql)
        res = back2CRM(data)
        return res


get_data()
