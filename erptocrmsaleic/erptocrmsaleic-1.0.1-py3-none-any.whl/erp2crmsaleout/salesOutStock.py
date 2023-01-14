import datetime
from urllib import parse

from pyrda.dbms.rds import RdClient
import requests
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


def log_crm():
    log_url = 'http://123.207.201.140:88/crm/crmapi/apiKey.php'
    parm = {'authen_code': '3BBf3C56'}
    log_res = requests.post(log_url, data=parm)
    result = log_res.json()

    return result


def back2CRM(data):
    r = requests.post(url="http://123.207.201.140:3000/crmapi/add", json=data)
    res = r.json()
    return res


def get_data():
    sql = """
            select * from RDS_CRM_SRC_saleout where FIsdo =0
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
        res = save_saleout(d, materisals)
        ret_data.append(res)
    ret_dict = {
        'code': '1',
        'message': ret_data
    }
    return ret_dict


def query_customer(key, token, name):
    url = 'http://123.207.201.140:88/crm/crmapi/crmoperation.php'
    model = {
        "module": "Accounts",
        "func": "getList",
        "apikey": key,
        "token": token,
        "username": "admin",
        "pagesize": "1",
        "pagenum": "1",
        "searchtext": [{
            "groupid": 1,
            "fieldname": "accountname",
            "module": "Accounts",
            "comparator": "等于",
            "value": name,
        }]
    }
    res = requests.post(url, json=model)
    return res


def materials_no(data):
    data_lis = []
    for i, d in data.iterrows():
        model = {
            "product_no": d['FMATERIALID'],
            "salesorder_no": d['salesorder_no'],
            "quantity": str(d['FREALQTY']),
            "name": '其他仓' if d['FSTOCKID'] else '赠品仓',
            "sf2080": str(d["FCUSTMATID"]),
            # "sf2291": d['CustMatName'],
            "sf2713": str(d['FMUSTQTY']),
            "sf2924": str(d['FISFREE'])
        }
        data_lis.append(model)
    return data_lis


def save_saleout(d, materials):
    """
    从DMS回写到CRM
    :return:
    """
    sql = 'select FNUMBER,FNAME from rds_vw_customer where FCUSTID = {}'.format(d['FCUSTOMERID'][0])
    cus = app2.select(sql)
    sql_cus = "select account_no from ld_account where accountname = '{}' and approvestatus ='已批准'".format(cus[0]['FNAME'])
    df_cust = pd.read_sql(sql_cus, crm_engine)
    # d_cus = query_customer(result['key'], result['token'], cus[0]['FNAME']).json()
    print(df_cust)
    if not df_cust.empty:
        account_no = df_cust['account_no'][0]
        model = {
            "module": "outboundorder",
            "data": [
                {
                    "mainFields": {
                        "out_no": d['FBILLNO'][0],
                        "account_no": account_no,
                        "approvestatus": d['FDOCUMENTSTATUS'][0],
                        # "last_name": "系統管理員",
                        "createdtime": str(d['FCREATEDATE'][0]),
                        "modifiedtime": str(d['FMODIFYDATE'][0]),
                        "outdate": str(d['FDate'][0]),
                        "express_no": d['FCARRIAGENO'][0],
                        "cf_4755": str(d['FSTOCKORGID'][0]),
                        "cf_4749": str(d['FHEADLOCATIONID'][0]),
                        "cf_4750": str(d['FDELIVERYDEPTID'][0]),
                        "cf_4751": str(d['FCARRIERID'][0]),
                        "cf_4752": str(d['FSTOCKERGROUPID'][0]),
                        "cf_4756": str(d['FSTOCKERID'][0]),
                        "cf_4753": str(d['FSALEORGID'][0])
                    },
                    "detailFields": materials
                }
            ]
        }
        res = back2CRM(model)
        if res['code'] == "success":
            inser_logging('销售出库', f"{d['FBILLNO'][0]}", f'{res["msg"]}', 1)
        else:
            inser_logging('销售出库', f"{d['FBILLNO'][0]}", f'{res["msg"]}', 2)
        sql = "update a set a.FisDo=3 from RDS_CRM_SRC_saleout a where FBillNo = '{}'".format(
            d['FBILLNO'][0])
        app3.update(sql)
        return res


def inser_logging(FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                  FCompanyName='CP'):
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
    sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
        FIsdo) + ")"
    data = app3.insert(sql)
    return data
