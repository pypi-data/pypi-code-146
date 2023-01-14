from urllib import parse

from pyrda.dbms.rds import RdClient
from requests import *
from sqlalchemy import create_engine
import pandas as pd

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
dms_engine = create_engine(dms_conn)

token_china = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
app3 = RdClient(token=token_china)


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
    for i in d_lis:
        d = data[data['salesorder_no'] == i]
        d = d.set_index('index')
        print(d)
        materisals = materials_no(d)
        save_salebilling(d, materisals)


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
    data = {
        "module": "invoice",
        "data": [
            {
                "mainFields": {
                    "invoice_no": d['invoice_no'][0],
                    "account_no": str(d['FCUSTOMERID'][0]),

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
    print(back2CRM(data))

get_data()