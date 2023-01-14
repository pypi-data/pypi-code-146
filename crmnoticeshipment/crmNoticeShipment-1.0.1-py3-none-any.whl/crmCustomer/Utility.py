import datetime

import requests
import hashlib
import time
from urllib import parse
import json


def getcode(app2, param, tableName, param1, param2):
    '''
    通过传入的参数获得相应的编码
    :param app2 执行sql语句对象:
    :param param 需要查询的字段:
    :param tableName 表名:
    :param param1 查询条件字段:
    :param param2 条件:
    :return 将查询的到的结果返回:
    '''

    if param2 == "销售四部":
        param2 = "国际销售部"

    sql = f"select {param} from {tableName} where {param1}='{param2}'"

    res = app2.select(sql)
    if res:

        return res[0][f'{param}']
    else:
        return ""


def getSullierTypeCode(param):
    '''
    转换code码
    :param param: 条件
    :return:
    '''
    d = {"采购": "CG", "委外": "WW", "服务": "FW", "综合": "ZH"}

    res = d[param]

    return res


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


def DetailDateIsExist(app2, FNumber, FNumber_value, tableName):
    '''
    判断从OA里面获得的数据在rds明细表中是否存在
    :param app2:  sql语句执行对象
    :param fNumber: 编码
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''
    sql = f"select * from {tableName} where {FNumber}='{FNumber_value}'"

    if app2.select(sql) == []:
        return True
    else:
        return False


def ListDateIsExist(app2, tableName, FName, FName_value, FStartDate, FStartDate_value):
    '''
    判断从OA里面获得的数据在rds列表中是否存在
    :param app2: sql语句执行对象
    :param js: 数据
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''
    sql = f"select * from {tableName} where {FName}='{FName_value}' and {FStartDate}='{FStartDate_value}'"
    if app2.select(sql) == []:
        return True
    else:
        return False


def changeStatus(app2, status, tableName, param, param2):
    '''
    改变数据状态
    :param app2: sql语句执行对象
    :param status: 状态
    :param tableName: 表名
    :param param: 条件名
    :param param2: 条件
    :return:
    '''
    sql = f"update a set a.Fisdo={status} from {tableName} a where {param}='{param2}'"

    app2.update(sql)


def getStatus(app2, fNumber, tableName):
    '''
    获得数据状态
    :param app2: sql语句执行对象
    :param fNumber: 编码
    :param tableName: 表名
    :return:
    '''

    sql = f"select Fisdo from {tableName} where FNumber='{fNumber}'"

    if app2.select(sql) != []:

        res = app2.select(sql)[0]['Fisdo']

        if res == 1:
            return False
        elif res == 0:
            return True
        else:
            return 2


def getTaxRateCode(app2, param):
    '''
    转换税率编码
    :param app2: sql语句执行对象
    :param param: 条件
    :return:
    '''

    if param == "1":
        param = 13
    elif param == "0":
        param = "零"

    sql = f"select FNUMBER from rds_vw_taxrate where  FNAME like '{param}%'"
    res = app2.select(sql)

    return res


def getOrganizationCode(app2, FUseOrg):
    '''
    获取分配组织id
    :param FUseOrg:
    :return:
    '''
    if FUseOrg == "赛普总部":
        FUseOrg = "苏州赛普"
    elif FUseOrg == '苏州赛普生物科技有限公司':
        FUseOrg = "苏州赛普"

    elif FUseOrg == "南通分厂":
        FUseOrg = "赛普生物科技（南通）有限公司"

    sql = f"select FORGID from rds_vw_organizations where FNAME like '%{FUseOrg}%'"

    oResult = app2.select(sql)

    return oResult[0]['FORGID']


def exchangeBooleanValue(param):
    '''
    逻辑值转换
    :param param:
    :return:
    '''

    if param == "是":
        return param
    elif param == "否":
        return param


def exchangeDateCode(param):
    if param == "天":
        return "1"
    elif param == "周":
        return "2"
    elif param == "月":
        return "3"


def dateConstraint(date):
    list = date.split("-")

    year = int(list[0])

    month = int(list[1])

    day = int(list[2])

    return datetime.date(year, month, day)


def md5_encryption(now_time):
    m = hashlib.md5()
    username = "Customer"
    password = "abccus123"
    token = username + password + now_time
    m.update(token.encode())
    md5 = m.hexdigest()

    return md5


def getOAListW(FVarDateTime):
    now = time.localtime()
    now_time = time.strftime("%Y%m%d%H%M%S", now)

    data = {
        "operationinfo": {
            "operator": "DMS"
        },
        'mainTable': {
            "FDate": FVarDateTime,
            "FStatus": '1',
        },
        "pageInfo": {
            "pageNo": "1",
            "pageSize": "10000"
        },
        "header": {
            "systemid": "Customer",
            "currentDateTime": now_time,
            "Md5": md5_encryption(now_time)
        }
    }

    str = json.dumps(data, indent=2)

    values = parse.quote(str).replace("%20", "")

    url = "http://58.211.213.34:32212/api/cube/restful/interface/getModeDataPageList/CustomerToday"

    payload = 'datajson=' + values
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    info = response.json()['result']
    # lis = []
    # t1 = time.time()
    # t_today = time.strftime("%Y-%m-%d", time.localtime(t1))
    # for i in json.loads(info):
    #     if i['mainTable']['FDate'] == t_today:
    #         lis.append(i)
    # 
    # # print(lis)

    return json.loads(info)


def getOAListN(FVarDateTime):
    now = time.localtime()
    now_time = time.strftime("%Y%m%d%H%M%S", now)

    data = {
        "operationinfo": {
            "operator": "DMS"
        },
        'mainTable': {
            "FDate": FVarDateTime,
        },
        "pageInfo": {
            "pageNo": "1",
            "pageSize": "10000"
        },
        "header": {
            "systemid": "Customer",
            "currentDateTime": now_time,
            "Md5": md5_encryption(now_time)
        }
    }

    str = json.dumps(data, indent=2)

    values = parse.quote(str).replace("%20", "")

    url = "http://192.168.1.15:32212/api/cube/restful/interface/getModeDataPageList/CustomerToday"

    payload = 'datajson=' + values
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    info = response.json()['result']

    js = json.loads(info)

    return js


def getOADetailDataW(FName, FName_value, FStartDate, FStartDate_value):
    '''

    :param option:
    :param FName:
    :param FName_value:
    :param FStartDate:
    :param FStartDate_value:
    :return:
    '''
    now = time.localtime()
    now_time = time.strftime("%Y%m%d%H%M%S", now)

    data = {
        "operationinfo": {
            "operator": "DMS"
        },
        'mainTable': {
            'FName2052': str(FName_value),
            FStartDate: str(FStartDate_value),
            "FStatus": '1'
        },
        "pageInfo": {
            "pageNo": "1",
            "pageSize": "10000"
        },
        "header": {
            "systemid": "Customer",
            "currentDateTime": now_time,
            "Md5": md5_encryption(now_time)
        }
    }

    strs = json.dumps(data, indent=2)

    values = parse.quote(strs).replace("%20", "")

    url = "http://58.211.213.34:32212/api/cube/restful/interface/getModeDataPageList/CustomerReturn"

    payload = 'datajson=' + values
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    info = response.json()['result']

    js = json.loads(info)

    return js


def getOADetailDataN(FName, FName_value, FStartDate, FStartDate_value):
    '''

    :param option:
    :param FName:
    :param FName_value:
    :param FStartDate:
    :param FStartDate_value:
    :return:
    '''
    now = time.localtime()
    now_time = time.strftime("%Y%m%d%H%M%S", now)

    data = {
        "operationinfo": {
            "operator": "DMS"
        },
        'mainTable': {
            FName: str(FName_value),
            FStartDate: str(FStartDate_value)
        },
        "pageInfo": {
            "pageNo": "1",
            "pageSize": "10000"
        },
        "header": {
            "systemid": "Customer",
            "currentDateTime": now_time,
            "Md5": md5_encryption(now_time)
        }
    }

    strs = json.dumps(data, indent=2)

    values = parse.quote(strs).replace("%20", "")

    url = "http://192.168.1.15:32212/api/cube/restful/interface/getModeDataPageList/CustomerReturn"

    payload = 'datajson=' + values
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    info = response.json()['result']

    js = json.loads(info)

    return js


def getOrganizationFNumber(app2, FUseOrg):
    '''
    获取分配组织id
    :param FUseOrg:
    :return:
    '''
    if FUseOrg == "赛普总部":
        FUseOrg = "苏州赛普"
    elif FUseOrg == '苏州赛普生物科技有限公司':
        FUseOrg = "苏州赛普"
    elif FUseOrg == "南通分厂":
        FUseOrg = "赛普生物科技（南通）有限公司"

    sql = f"select FORGID,FNUMBER  from rds_vw_organizations where FNAME like '%{FUseOrg}%'"

    res = app2.select(sql)

    if res == []:
        return ""
    else:
        return res[0]


def checkCustomerExist(app2, FName):
    '''
    通过客户名称判断客户是否已存在
    :param app2: 
    :param FName: 
    :return: 
    '''

    sql = f"select FNUMBER from rds_vw_customer where FNAME='{FName}'".encode('utf-8')

    res = app2.select(sql)

    return res
