# 客户
import json
import requests
import hashlib
import pandas as pd
from pyrda.dbms.rds import RdClient
import re
from rdecscustomer import ec_DatabaseOperations as db
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from rdecscustomer import ec_Metadata as mt
from rdecscustomer import ec_Utility as ut
import time


def getFinterId(app3, tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''
    sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"
    res = app3.select(sql)

    if res:

        return res[0]['FMaxId']

    else:

        return 0


def encryption(pageNum, pageSize, queryList, tableName):
    '''
    ECS的token加密
    :param pageNum:
    :param pageSize:
    :param queryList:
    :param tableName:
    :return:
    '''
    m = hashlib.md5()
    token = f'accessId=skyx@prod&accessKey=skyx@0512@1024@prod&pageNum={pageNum}&pageSize={pageSize}&queryList={queryList}&tableName={tableName}'
    # token = f'accessId=skyx&accessKey=skyx@0512@1024&pageNum={pageNum}&pageSize={pageSize}&queryList={queryList}&tableName={tableName}'
    m.update(token.encode())
    md5 = m.hexdigest()
    return md5


def ECS_post_info(url, pageNum, pageSize, qw, tableName, updateTime, key):
    '''
    生科云选API接口
    :param url: 地址
    :param pageNum: 页码
    :param pageSize: 页面大小
    :param qw: 查询条件
    :param tableName: 表名
    :param updateTime: 时间戳
    :return: dataframe
    '''
    queryList = '[{"qw":' + f'"{qw}"' + ',"value":' + f'"{updateTime}"' + ',"key":' + f'"{key}"' + '}]'
    # 查询条件
    queryList1 = [{"qw": qw, "value": updateTime, "key": key}]
    # 查询的表名
    tableName = tableName
    data = {
        "tableName": tableName,
        "pageNum": pageNum,
        "pageSize": pageSize,
        "token": encryption(pageNum, pageSize, queryList, tableName),
        "queryList": queryList1
    }
    data = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=data)
    info = response.json()
    # print(info)
    df = pd.DataFrame(info['data']['list'])
    return df


def ECS_post_info2(url,pageNum,pageSize,qw,qw2,tableName,updateTime,updateTime2,key):
    '''
    生科云选API接口
    :param url: 地址
    :param pageNum: 页码
    :param pageSize: 页面大小
    :param qw: 查询条件
    :param tableName: 表名
    :param updateTime: 时间戳
    :return: dataframe
    '''

    queryList='[{"qw":'+f'"{qw}"'+',"value":'+f'"{updateTime}"'+',"key":'+f'"{key}"'+'},{"qw":'+f'"{qw2}"'+',"value":'+f'"{updateTime2}"'+',"key":'+f'"{key}"'+'}]'

    # 查询条件
    queryList1=[{"qw":qw,"value":updateTime,"key":key},{"qw":qw2,"value":updateTime2,"key":key}]

    # 查询的表名
    tableName=tableName

    data ={
        "tableName": tableName,
        "pageNum": pageNum,
        "pageSize": pageSize,
        "token": encryption(pageNum, pageSize, queryList, tableName),
        "queryList": queryList1
    }
    data = json.dumps(data)

    #url = f"http://10.3.1.99:8107/customer/getCustomerList?startDate={startDate}&endDate={endDate}&token={md5}"

    #url = "https://test-kingdee-api.bioyx.cn/dynamic/query"

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers,data=data)

    info = response.json()
    #
    # print(info)
    df = pd.DataFrame(info['data']['list'])
    # df = pd.DataFrame(info['data']['list'])
    return df


def combination(data_info, data_address, data_contact):
    '''
    组装数据
    :return:
    '''

    model = {
        # "FInterId":'',
        "FApplyOrgName": '苏州生科云选生物科技有限公司',
        "FApplyDeptName": '',
        "FApplierName": '',
        "FDate": data_info['FCREATEDATE'],
        "FNumber": data_info['CUSTOMER_SEQ'],
        "FName": data_info['CUSTOMERNAME'],
        "FShortName": '',
        "FCOUNTRY": data_info['FCOUNTRY'],
        "FPROVINCIAL": data_info['FPROVINCIAL'],
        "FTEL": data_address.get('FTEL'),
        "FINVOICETITLE": '',
        "FTAXREGISTERCODE": data_info['FTAXREGISTERCODE'],
        "FBankName": data_info['BANK_NAME'],
        "FINVOICETEL": data_info['INVOICE_TEL'],
        "FAccountNumber": data_info['BANK_ACCOUNT'],
        "FINVOICEADDRESS": data_info['FINVOICEADDRESS'],
        "FINVOICETYPE": data_info['FINVOICETYPE'],
        "FTaxRate": data_address.get('FTAXRATE'),
        "FCONTACT": data_contact.get('FCONTACT'),
        "FBizAddress": data_contact.get('FBIZADDRESS'),
        "FMOBILE": data_contact.get('FMOBILEPHONE'),
        "FSalesman": data_address.get('FSELLER'),
        "FAalesDeptName": data_info['FSALDEPTID'],
        "FCustTypeNo": data_info['FCUSTTYPEID'],
        "FGroupNo": data_info['FPRIMARYGROUP'],
        "F_SZSP_KHFLNo": data_info['F_SZSP_KHFL'],
        "FSalesGroupNo": data_address.get('FSALGROUPID'),
        "FTRADINGCURRNO": data_address.get('FSETTLECURRID'),
        "FSETTLETYPENO": data_info['FSETTLETYPEID'],
        "FRECCONDITIONNO": data_info['FRECCONDITIONID'],
        "FPRICELISTNO": data_info['FPRICELISTID'],
        "FUploadDate": data_info['FMODIFYDATE'],
        # "FUploadDate": data_info['FAPPROVEDATE'],
        # "FIsdo":'',
        "F_SZSP_BLOCNAME": data_info['F_SZSP_BLOCNAME'],
        "F_SZSP_KHZYJBNo": data_info['F_SZSP_KHZYJB'],
        "F_SZSP_KHGHSXNo": data_info['F_SZSP_KHGHSX'],
        "F_SZSP_XSMSNo": data_info['F_SZSP_XSMS'],
        "F_SZSP_XSMSSXNo": data_info['F_SZSP_XSMSSX'],
        "F_SZSP_Text": ''
    }

    for key in model:
        if model.get(key) == None:
            model[key] = ''
    model['FName'] = re.sub("'", '', model['FName'])

    return model


def checkExist(app2,FName):
    '''
    查看数据是否存在
    :return:
    '''

    sql=f"select FNumber from RDS_ECS_SRC_BD_CUSTOMER where FName='{FName}'"

    res=app2.select(sql)

    if res:

        return False

    else:
        return True



def insert_data(app3, data):
    '''
    数据库写入语句
    :param app2:
    :param data:
    :return:
    '''

    if checkExist(app3,data.get('FName', '')):

        sql = f"""insert into RDS_ECS_SRC_BD_CUSTOMER(FInterId,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,
        FShortName,FCOUNTRY,FPROVINCIAL,FTEL,FINVOICETITLE,FTAXREGISTERCODE,FBankName,FINVOICETEL,FAccountNumber,
        FINVOICEADDRESS,FINVOICETYPE,FTaxRate,FCONTACT,FBizAddress,FMOBILE,FSalesman,FAalesDeptName,FCustTypeNo,FGroupNo,
        F_SZSP_KHFLNo,FSalesGroupNo,FTRADINGCURRNO,FSETTLETYPENO,FRECCONDITIONNO,FPRICELISTNO,FUploadDate,FIsdo,
        F_SZSP_BLOCNAME,F_SZSP_KHZYJBNo,F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo,F_SZSP_Text
        ) values({getFinterId(app3, 'RDS_ECS_SRC_BD_CUSTOMER') + 1},'苏州生科云选生物科技有限公司','{data.get('FApplyDeptName', '')}', 
        '{data.get('FApplierName', '')}', '{data.get('FDate', '')}','{data.get('FNumber', '')}', '{data.get('FName', '')}',
        '{data.get('FShortName', '')}', '{data.get('FCOUNTRY', '')}', '{data.get('FPROVINCIAL', '')}', '{data.get('FTEL', '')}',
        '{data.get('FINVOICETITLE', '')}', '{data.get('FTAXREGISTERCODE', '')}', '{data.get('FBankName', '')}',
        '{data.get('FINVOICETEL', '')}', '{data.get('FAccountNumber', '')}', '{data.get('FINVOICEADDRESS', '')}',
        '{data.get('FINVOICETYPE', '')}', '{data.get('FTaxRate', '')}', '{data.get('FCONTACT', '')}','{data.get('FBizAddress', '')}',
        '{data.get('FMOBILE', '')}', '{data.get('FSalesman', '')}', '{data.get('FAalesDeptName', '')}', '{data.get('FCustTypeNo', '')}',
        '{data.get('FGroupNo', '')}', '{data.get('F_SZSP_KHFLNo', '')}', '{data.get('FSalesGroupNo', '')}', 
        '{data.get('FTRADINGCURRNO', '')}', '{data.get('FSETTLETYPENO', '')}', '{data.get('FRECCONDITIONNO', '')}', 
        '{data.get('FPRICELISTNO', '')}', '{data.get('FUploadDate', '')}', 0,'{data.get('F_SZSP_BLOCNAME', '')}',
        '{data.get('F_SZSP_KHZYJBNo', '')}','{data.get('F_SZSP_KHGHSXNo', '')}','{data.get('F_SZSP_XSMSNo', '')}',
        '{data.get('F_SZSP_XSMSSXNo', '')}','{data.get('F_SZSP_Text', '')}'
        )"""
        db.insertData(app3, sql)

        db.insertLog(app3, "ECS客户", data.get('FNumber', ''), "数据插入成功", "1")


def ecs_ods_erp(app2, app3, option1):
    '''
    :param app3: token_china
    :param app2: token_erp
    :param option1: 金蝶用户信息
    :return: 写入金蝶
    '''
    sql4 = "select FInterId, FApplyOrgName, FApplyDeptName, FApplierName, FDate, FNumber, FName,FShortName, FCOUNTRY, FPROVINCIAL, FTEL, FINVOICETITLE, FTAXREGISTERCODE, FBankName, FINVOICETEL, FAccountNumber,FINVOICEADDRESS, FINVOICETYPE, FTaxRate, FCONTACT, FBizAddress, FMOBILE, FSalesman, FAalesDeptName, FCustTypeNo, FGroupNo,F_SZSP_KHFLNo, FSalesGroupNo, FTRADINGCURRNO, FSETTLETYPENO, FRECCONDITIONNO, FPRICELISTNO, FUploadDate, FIsdo,F_SZSP_BLOCNAME, F_SZSP_KHZYJBNo, F_SZSP_KHGHSXNo, F_SZSP_XSMSNo, F_SZSP_XSMSSXNo, F_SZSP_Text from RDS_ECS_ODS_BD_CUSTOMER where FIsdo = 0"

    result = db.getData(app3, sql4)

    if result:

        api_sdk = K3CloudApiSdk()

        mt.ERP_customersave(api_sdk, option1, result, app3, ut, app2, 'RDS_ECS_SRC_BD_CUSTOMER', 'RDS_ECS_ODS_BD_CUSTOMER')

# def select_Unique_key(app2, table_name, key):
#     '''
#     查询需要写入数据表的唯一字段值，用于后续判断数据是否存在数据库
#     :param app2:
#     :param table_name:
#     :param key:
#     :return:
#     '''
#     key_list = []
#     sql = f"select {key} from {table_name}"
#     key_data = app2.select(sql)
#     for key_dict in key_data:
#         key_list.append(key_dict[key])
#     return key_list



def delete_data(app2, data):
    '''
    数据库删除语句
    :param app2:
    :param data:
    :return:
    '''

    sql = f"""delete from RDS_ECS_SRC_BD_CUSTOMER where FName='{data['FName']}'"""
    app2.delete(sql)


def customer(FDate):

    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
    app2 = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
    # A59 培训账套token
    # app3 = RdClient(token='B405719A-772E-4DF9-A560-C24948A3A5D6')
    # app2 = RdClient(token='A597CB38-8F32-40C8-97BC-111823AA7765')

    # option1 = {
    #     "acct_id": '63310e555e38b1',
    #     "user_name": '于洋',
    #     "app_id": '234676_7cfM7ZvE7lC+38SvW47B26yv3h6+xpqp',
    #     "app_sec": '7f81905ad6af4deb992253b2520a8b70',
    #     "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    # }

    option1 = {
        "acct_id": '62777efb5510ce',
        "user_name": 'DMS',
        "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
        # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        "app_sec": 'b105890b343b40ba908ed51453940935',
        "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    }

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    data = ECS_post_info(url, 1, 1000, "like", "v_customer_info", FDate, "UPDATE_TIME")

    for i,d in data.iterrows():

        if d['FCustomerType']=="成交客户" and d['FTAXREGISTERCODE']!="":

            data_address = ECS_post_info(url, 1, 1000, "eq", "v_customer_address", d['CUSTOMER_SEQ'],
                                         "CUSTOMER_SEQ")
            data_contact = ECS_post_info(url, 1, 1000, "eq", "v_customer_contact", d['CUSTOMER_SEQ'],
                                         "CUSTOMER_SEQ")

            try:

                result=combination(d,data_address.iloc[0],data_contact.iloc[0])

                insert_data(app3,result)

            except Exception as e:

                db.insertLog(app3,"ECS客户",d['CUSTOMER_SEQ'],"数据异常请检查数据","2")


    ecs_ods_erp(app2=app2,app3=app3,option1=option1)

    return "数据同步完毕"







