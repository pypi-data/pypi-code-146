#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rdsalesorder import metadata as mt

def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    try:

        sql = "select distinct FSALEORDERNO from RDS_ECS_ODS_Sales_Order where FIsDo=0 and FIsfree!=1"

        res = app3.select(sql)

        return res

    except Exception as e:

        return []


def getClassfyData(app3, code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    number=code['FSALEORDERNO']

    sql = f"""select FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,UPDATETIME,FIsfree,FIsDO,FPurchaseDate,FCollectionTerms,FUrgency,FSalesType,FCurrencyName from RDS_ECS_ODS_Sales_Order where FSALEORDERNO='{number}'"""

    res = app3.select(sql)

    return res



def code_conversion(app2, tableName, param, param2):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    try:

        sql = f"select FNumber from {tableName} where {param}='{param2}'"

        res = app2.select(sql)

        if res == []:

            return ""

        else:

            return res[0]['FNumber']

    except Exception as e:

        return ""


def code_conversion_org(app2, tableName, param, param2, param3):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    try:

        sql = f"select FNumber from {tableName} where {param}='{param2}' and FOrgNumber='{param3}'"

        res = app2.select(sql)

        if res == []:

            return ""

        else:

            return res[0]['FNumber']

    except Exception as e:

        return ""


def changeStatus(app2, fnumber, status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    try:

        sql = f"update a set a.FIsDO={status} from RDS_ECS_ODS_Sales_Order a where FSALEORDERNO='{fnumber}'"

        app2.update(sql)

    except Exception as e:

        return ""


def getFinterId(app2, tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''

    try:

        sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"

        res = app2.select(sql)

        return res[0]['FMaxId']

    except Exception as e:

        return 0


def checkDataExist(app2, FSEQ):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FSALEORDERENTRYSEQ from RDS_ECS_SRC_Sales_Order where FSALEORDERENTRYSEQ={FSEQ}"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def deleteOldDate(app3,FNumber):
    '''
    删除旧数据
    :param app3:
    :param FNumber:
    :return:
    '''

    sql1=f"delete from RDS_ECS_SRC_Sales_Order where FSALEORDERNO='{FNumber}'"

    app3.delete(sql1)

    sql2 = f"delete from RDS_ECS_ODS_Sales_Order where FSALEORDERNO='{FNumber}'"

    app3.delete(sql2)

    return True


def IsUpdate(app3,seq,updateTime,api_sdk,option):

    flag=False

    sql=f"select FSALEORDERNO,UPDATETIME from RDS_ECS_SRC_Sales_Order where FSALEORDERENTRYSEQ='{seq}'"

    res=app3.select(sql)

    if res:

        try:

            if str(res[0]['UPDATETIME'])!=updateTime:

                flag=True

                deleteResult=deleteOldDate(app3,res[0]['FSALEORDERNO'])

                if deleteResult:

                    unAuditResult=mt.unAudit(api_sdk,res[0]['FSALEORDERNO'],option)

                    if unAuditResult:

                        mt.delete(api_sdk,res[0]['FSALEORDERNO'],option)

                else:

                    insertLog(app3, "销售订单",res[0]['FSALEORDERNO'], "反审核失败", "2")


        except Exception as e:

            insertLog(app3, "销售订单", res[0]['FSALEORDERNO'], "更新数据失败", "2")

            return False

    return flag





def insert_SAL_ORDER_Table(app2,app3, data,api_sdk,option):
    '''
    将数据插入销售订单SRC表中
    :param app2: 操作数据库对象
    :param data: 数据源
    :return:
    '''


    for i in data.index:

        if checkDataExist(app3, data.loc[i]['FSALEORDERENTRYSEQ']) or IsUpdate(app3,data.loc[i]['FSALEORDERENTRYSEQ'],data.loc[i]['UPDATETIME'],api_sdk,option):

            if judgementData(app2, app3, data[data['FSALEORDERNO'] == data.loc[i]['FSALEORDERNO']]):

                inert_data(app3, data[data['FSALEORDERNO'] == data.loc[i]['FSALEORDERNO']])




def judgementData(app2, app3, data):
    '''
    判断数据是否合规
    :param app2:
    :param data:
    :return:
    '''

    flag = True

    for i in data.index:
        if code_conversion(app2, "rds_vw_customer", "FNAME", data.loc[i]['FCUSTOMNAME']) != "":

            if code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", data.loc[i]['FPRDNUMBER']) != "" or \
                    data.loc[i]['FPRDNUMBER'] == "1":

                continue

            else:

                insertLog(app3, "销售订单", data.loc[i]['FSALEORDERNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "销售订单", data.loc[i]['FSALEORDERNO'], "客户不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql = f"""insert into RDS_ECS_SRC_Sales_Order(FInterID,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FCollectionTerms,FUrgency,FSalesType,FUpDateTime,FCurrencyName,UPDATETIME) values({int(getFinterId(app3, 'RDS_ECS_SRC_Sales_Order')) + 1},'{data.loc[i]['FSALEORDERNO']}','{data.loc[i]['FBILLTYPEIDNAME']}','{data.loc[i]['FSALEDATE']}','{data.loc[i]['FCUSTCODE']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FSALEORDERENTRYSEQ']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FQTY']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FMONEY']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FTAXAMOUNT']}','{data.loc[i]['FTAXPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FSALDEPTID']}','{data.loc[i]['FSALGROUPID']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FDESCRIPTION']}','0','0','月结30天','一般','内销',getdate(),'{data.loc[i]['FCURRENCYID']}','{data.loc[i]['UPDATETIME']}')"""

            app3.insert(sql)
            insertLog(app3, "销售订单", data.loc[i]['FSALEORDERNO'], "数据成功插入SRC","1")

        except Exception as e:

            insertLog(app3, "销售订单", data.loc[i]['FSALEORDERNO'], "插入SRC数据异常，请检查数据","2")

    pass


def insertLog(app2,FProgramName,FNumber,Message,FIsdo,cp='赛普'):
    '''
    异常数据日志
    :param app2:
    :param FNumber:
    :param Message:
    :return:
    '''

    sql="insert into RDS_ECS_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('"+FProgramName+"','"+FNumber+"','"+Message+"',getdate(),'"+cp+"','"+FIsdo+"')"

    app2.insert(sql)
