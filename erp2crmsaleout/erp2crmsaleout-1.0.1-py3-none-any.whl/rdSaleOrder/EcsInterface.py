import json
import requests
import hashlib

import pandas as pd

def encryption(pageNum,pageSize,queryList,tableName):
    '''
    ECS的token加密
    :param pageNum:
    :param pageSize:
    :param queryList:
    :param tableName:
    :return:
    '''

    m = hashlib.md5()

    token=f'accessId=skyx@prod&accessKey=skyx@0512@1024@prod&pageNum={pageNum}&pageSize={pageSize}&queryList={queryList}&tableName={tableName}'

    # token = f'accessId=skyx&accessKey=skyx@0512@1024&pageNum={pageNum}&pageSize={pageSize}&queryList={queryList}&tableName={tableName}'

    m.update(token.encode())

    md5 = m.hexdigest()

    return md5


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

    col=["FSALEORDERNO","FBILLTYPEIDNAME","FSALEDATE","FCUSTCODE","FCUSTOMNAME","FSALEORDERENTRYSEQ","FPRDNUMBER","FPRDNAME","FQTY","FPRICE","FMONEY","FTAXRATE","FTAXAMOUNT","FTAXPRICE","FAMOUNT","FSALDEPTID","FSALGROUPID","FSALERID","FDESCRIPTION"]

    df = pd.DataFrame(info['data']['list'],columns=col)

    # df = pd.DataFrame(info['data']['list'])

    return df


def viewPage(url,pageNum,pageSize,qw,qw2,tableName,updateTime,updateTime2,key):
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

    # print(info)

    return info['data']['pages']



















