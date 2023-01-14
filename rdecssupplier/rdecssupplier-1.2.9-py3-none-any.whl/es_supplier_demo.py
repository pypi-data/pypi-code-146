# 供应商

import json
import requests
import hashlib
import pandas as pd
from pyrda.dbms.rds import RdClient
from rdecssupplier import es_DatabaseOperations as db
from rdecssupplier import es_Metadata as mt
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from rdecssupplier import es_Utility as ut


def getFinterId(app2, tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''
    sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"
    res = app2.select(sql)
    return res[0]['FMaxId']


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

    df = info['data']['list']
    return df


def combination(data_info, data_bank, data_base, data_contact, data_business):
    '''
    组装数据
    :return:
    '''

    model = {
        # FInterId
        "FApplyOrgName": '苏州生科云选生物科技有限公司',
        "FApplyDeptName": '',
        "FApplierName": '',
        "FDate": data_info['FCREATEDATE'],
        "FNumber": data_info['FNUMBER'],
        "FName": data_info['FNAME'],
        "FShortName": data_info['FSHORTNAME'],
        "FCountry": data_bank['FCOUNTRY'],
        "FProvince": data_base['FPROVINCIAL'],
        "FZipCode": data_base['FZIP'],
        "FUniversalCode": '',
        "FRegisterAddress": data_base['FREGISTERADDRESS'],
        "FMngrDeptName": data_base['FDEPTID'],
        "FMngrMan": data_base['FSTAFFID'],
        "FSullierType": data_base['FSUPPLIERCLASSIFY'],
        # "FInvoiceType": "",
        "FInvoiceType": data_business['FINVOICETYPE'],
        "FTaxRate": data_business['FTAXRATEID'],
        # "FTaxRate": "",
        "FAccountNumber": data_bank['FBANKCODE'],
        "FAccountName": data_bank['FNAME'],
        "FBankTransferCode": '',
        "FBankName": data_bank['FOPENBANKNAME'],
        "FBankAddr": '',
        "FContact": data_contact['FCONTACT'],
        "FMobile": data_contact['FMOBILE'],
        "FEMail": data_contact['FEMAIL'],
        "FSupplierCategoryNo": '',
        "FSupplierGradeNo": '',
        "FPriceListNo": '',
        # "FSettleCurrencyNo": data_business['FPAYCURRENCYID'],
        "FSettleCurrencyNo": "",
        # "FSettlementMethodNo": data_business['FPAYMENTTYPE'],
        "FSettlementMethodNo": "",
        # "FPaymentConditionNo": data_business['FPAYCONDITION'],
        "FPaymentConditionNo": "",
        "FCurrencyNo": data_bank['FCURRENCYID'],
        "FUploadDate": data_info['FMODIFYDATE'],
        "FPurchaserGroupId": ''
    }
    for key in model:
        if model.get(key) == None:
            model[key] = ''
    return model


def select_Unique_key(app2, table_name, key):
    '''
    查询需要写入数据表的唯一字段值，用于后续判断数据是否存在数据库
    :param app2:
    :param table_name:
    :param key:
    :return:
    '''
    key_list = []
    sql = f"select {key} from {table_name}"
    key_data = app2.select(sql)
    for key_dict in key_data:
        key_list.append(key_dict[key])
    return key_list

def checkExist(app3,FName):

    sql=f"select FNumber from RDS_ECS_SRC_bd_SupplierDetail where FName='{FName}'"

    res=app3.select(sql)

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

    if checkExist(app3, data.get('FName', '')):

        sql = f"""insert into RDS_ECS_SRC_bd_SupplierDetail(FInterId,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,
        FName,FShortName,FCountry,FProvince,FZipCode,FUniversalCode,FRegisterAddress,FMngrDeptName,FMngrMan,FSullierType,
        FInvoiceType,FTaxRate,FAccountNumber,FAccountName,FBankTransferCode,FBankName,FBankAddr,FContact,FMobile,FEMail,
        FSupplierCategoryNo,FSupplierGradeNo,FPriceListNo,FSettleCurrencyNo,FSettlementMethodNo,FPaymentConditionNo,
        FCurrencyNo,FUploadDate,Fisdo,FPurchaserGroupId) values({getFinterId(app3, 'RDS_ECS_SRC_bd_SupplierDetail') + 1},
        '{data.get('FApplyOrgName', '')}','{data.get('FApplyDeptName', '')}','{data.get('FApplierName', '')}', 
        '{data.get('FDate', '')}','{data.get('FNumber', '')}', '{data.get('FName', '')}','{data.get('FShortName', '')}', 
        '{data.get('FCountry', '')}', '{data.get('FProvince', '')}', '{data.get('FZipCode', '')}','{data.get('FUniversalCode', '')}', 
        '{data.get('FRegisterAddress', '')}', '{data.get('FMngrDeptName', '')}','{data.get('FMngrMan', '')}', 
        '{data.get('FSullierType', '')}', '{data.get('FInvoiceType', '')}','{data.get('FTaxRate', '')}', 
        '{data.get('FAccountNumber', '')}', '{data.get('FAccountName', '')}','{data.get('FBankTransferCode', '')}',
        '{data.get('FBankName', '')}', '{data.get('FBankAddr', '')}', '{data.get('FContact', '')}', '{data.get('FMobile', '')}',
        '{data.get('FEMail', '')}', '{data.get('FSupplierCategoryNo', '')}', '{data.get('FSupplierGradeNo', '')}', 
        '{data.get('FPriceListNo', '')}', '{data.get('FSettleCurrencyNo', '')}', '{data.get('FSettlementMethodNo', '')}', 
        '{data.get('FPaymentConditionNo', '')}','{data.get('FCurrencyNo', '')}','{data.get('FUploadDate', '')}',0,
        '{data.get('FPurchaserGroupId', '')}')"""

        db.insertData(app3, sql)

        db.insertLog(app3, "ECS供应商", data.get('FNumber', ''), "数据插入成功", "1")

def ecs_supplier_to_erp(FDate):

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
    data_info_list = ECS_post_info(url, 1, 1000, "like", "v_supplier", FDate,"UPDATETIME")

    if not data_info_list.empty:

        for i ,d in data_info_list.iterrows():

            try:

                data_bank = ECS_post_info(url, 1, 1000, "eq", "v_supplier_bank_property", d['FNUMBER'],
                                          "FNUMBER")
                data_base = ECS_post_info(url, 1, 1000, "eq", "v_supplier_base_property", d['FNUMBER'],
                                          "FNUMBER")
                data_contact = ECS_post_info(url, 1, 1000, "eq", "v_supplier_contact", d['FNUMBER'],
                                             "FNUMBER")
                data_business = ECS_post_info(url, 1, 1000, "eq", "v_supplier_business_property",d['FNUMBER'],
                                              "FNUMBER")

                result = combination(d, data_bank.iloc[0], data_base.iloc[0], data_contact.iloc[0], data_business.iloc[0])

                insert_data(app3,result)

            except Exception as e:

                db.insertLog(app3, "ECS供应商", data_info_list[i]['FNUMBER'], "数据异常", "2")

        # 写入金蝶
    ecs_ods_erp(app2, app3,option1)

    return "数据同步完毕"


def ecs_ods_erp(app2,app3,option):
    '''
    判断RDS_ECS_ODS_bd_SupplierDetail表中是否有数据
    :param app3:
    :return:
    '''

    sql = "select FInterId ,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCountry,FZipCode,FUniversalCode,FRegisterAddress,FMngrDeptName,FMngrMan,FSullierType,FInvoiceType,FTaxRate,FAccountNumber,FAccountName ,FBankTransferCode,FBankName,FBankAddr,FContact,FMobile,FEMail, FSupplierCategoryNo,FSupplierGradeNo ,FPriceListNo,FSettleCurrencyNo,FSettlementMethodNo,FPaymentConditionNo,FCurrencyNo,FUploadDate,Fisdo from RDS_ECS_ODS_bd_SupplierDetail where Fisdo=0"

    res = app3.select(sql)

    if res :

        insert_into_ERP(erp_token=option, data=res, app2=app2, app3=app3)

    else:

        pass

def insert_into_ERP(erp_token, data, app2, app3):
    '''
    将数据插入到ERP系统
    :param erp_token:
    :param data:
    :param app2:
    :param app3:
    :return:
    '''

    api_sdk = K3CloudApiSdk()

    mt.ERP_suppliersave(api_sdk, erp_token, data, app2, ut, app3)



