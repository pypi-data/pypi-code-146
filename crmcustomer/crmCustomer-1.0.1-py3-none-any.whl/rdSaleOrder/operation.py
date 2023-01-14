# from pyrda.dbms.rds import RdClient
# app2 = RdClient(token='A597CB38-8F32-40C8-97BC-111823AA7765')

def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql = "select FSALEORDERNO from RDS_ECS_ODS_Sales_Order where FIsDo=0 and FIsfree!=1"

    res = app3.select(sql)

    return res


def getClassfyData(app3, code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql = f"select FInterID,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,UPDATETIME,FIsfree,FIsDO,FPurchaseDate,FCollectionTerms,FUrgency,FSalesType from RDS_ECS_ODS_Sales_Order where FSALEORDERNO='{code}'"

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

    sql = f"select FNumber from {tableName} where {param}='{param2}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FNumber']


def code_conversion_org(app2, tableName, param, param2, param3):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql = f"select FNumber from {tableName} where {param}='{param2}' and FOrgNumber='{param3}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FNumber']


def changeStatus(app2, fnumber, status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql = f"update a set a.FIsDO={status} from RDS_ECS_ODS_Sales_Order a where FSALEORDERNO='{fnumber}'"

    app2.update(sql)


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


def insert_SAL_ORDER_Table(app2, data):
    '''
    将数据插入销售订单SRC表中
    :param app2: 操作数据库对象
    :param data: 数据源
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2, data.loc[i]['FSALEORDERENTRYSEQ']):
            sql = f"insert into RDS_ECS_SRC_Sales_Order(FInterID,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FCollectionTerms,FUrgency,FSalesType,FUpDateTime) values({getFinterId(app2, 'RDS_ECS_SRC_Sales_Order') + 1},'{data.loc[i]['FSALEORDERNO']}','{data.loc[i]['FBILLTYPEIDNAME']}','{data.loc[i]['FSALEDATE']}','{data.loc[i]['FCUSTCODE']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FSALEORDERENTRYSEQ']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FQTY']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FMONEY']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FTAXAMOUNT']}','{data.loc[i]['FTAXPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FSALDEPTID']}','{data.loc[i]['FSALGROUPID']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FDESCRIPTION']}','0','0','月结30天','一般','内销',getdate())"

            app2.insert(sql)
