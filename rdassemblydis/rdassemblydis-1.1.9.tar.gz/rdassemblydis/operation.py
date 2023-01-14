def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    try:

        sql="select FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,Fnote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE,FIsdo from RDS_ECS_ODS_DISASS_DELIVERY where FIsdo=0"

        res=app3.select(sql)

        return res

    except Exception as e:

        return []

def code_conversion(app2,tableName,param,param2):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select FNumber from {tableName} where {param}='{param2}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FNumber']

def iskfperiod(app2,FNumber):
    '''
    查看物料是否启用保质期
    :param app2:
    :param FNumber:
    :return:
    '''

    sql=f"select FISKFPERIOD from rds_vw_fiskfperiod where F_SZSP_SKUNUMBER='{FNumber}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FISKFPERIOD']


def getSubEntityCode(app2,FNumber):
    '''
    获得子件信息
    :return:
    '''

    sql=f"select * from RDS_ECS_ODS_ASS_STORAGEACCT where FBillNo='{FNumber}'"

    res=app2.select(sql)

    return res

def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsDo={status} from RDS_ECS_ODS_DISASS_DELIVERY a where a.FBillNo='{fnumber}'"

    app3.update(sql)

def checkDataExist(app2, tableName,FBillNo):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FBillNo from {tableName} where FBillNo='{FBillNo}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def getFinterId(app2,tableName):
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

def insert_assembly_order(app3,data):
    '''
    组装单
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        try:

            if checkDataExist(app3,"RDS_ECS_SRC_ASS_STORAGEACCT",data.loc[i]['FBillNo']):

                sql = f"insert into RDS_ECS_SRC_ASS_STORAGEACCT(FInterID,FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,FBomNumber,FNote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE) values({int(getFinterId(app3,'RDS_ECS_SRC_ASS_STORAGEACCT'))+1},'{data.loc[i]['FBillNo']}','{data.loc[i]['Fseq']}','{data.loc[i]['Fdate']}','{data.loc[i]['FDeptName']}','{data.loc[i]['FItemNumber']}','{data.loc[i]['FItemName']}','{data.loc[i]['FItemModel']}','{data.loc[i]['FUnitName']}','{data.loc[i]['Fqty']}','{data.loc[i]['FStockName']}','{data.loc[i]['Flot']}','{data.loc[i]['FBomNumber']}','{data.loc[i]['Fnote']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}','{data.loc[i]['FSUMSUPPLIERLOT']}','{data.loc[i]['FAFFAIRTYPE']}')"

                app3.insert(sql)

                insertLog(app3, "组装拆卸单", data.loc[i]['FBillNo'], "数据插入组装单SRC成功", "1")

        except Exception as e:

            insertLog(app3, "组装拆卸单", data.loc[i]['FBillNo'], "插入组装单SRC数据异常，请检查数据","2")



def insert_remove_order(app3,data):
    '''
    拆卸单
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        try:

            if checkDataExist(app3,"RDS_ECS_SRC_DISASS_DELIVERY",data.loc[i]['FBillNo']):

                sql = f"insert into RDS_ECS_SRC_DISASS_DELIVERY(FInterID,FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,FNote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE) values({int(getFinterId(app3,'RDS_ECS_SRC_DISASS_DELIVERY'))+1},'{data.loc[i]['FBillNo']}','{data.loc[i]['Fseq']}','{data.loc[i]['Fdate']}','{data.loc[i]['FDeptName']}','{data.loc[i]['FItemNumber']}','{data.loc[i]['FItemName']}','{data.loc[i]['FItemModel']}','{data.loc[i]['FUnitName']}','{data.loc[i]['Fqty']}','{data.loc[i]['FStockName']}','{data.loc[i]['Flot']}','{data.loc[i]['Fnote']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}','{data.loc[i]['FSUMSUPPLIERLOT']}','{data.loc[i]['FAFFAIRTYPE']}')"

                app3.insert(sql)

                insertLog(app3, "组装拆卸单", data.loc[i]['FBillNo'], "数据插入拆卸单SRC成功", "1")

        except Exception as e:

            insertLog(app3, "组装拆卸单", data.loc[i]['FBillNo'], "插入拆卸单SRC数据异常，请检查数据","2")


def isbatch(app2,FNumber):

    sql=f"select FISBATCHMANAGE from rds_vw_fisbatch where F_SZSP_SKUNUMBER='{FNumber}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FISBATCHMANAGE']

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