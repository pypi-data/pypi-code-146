def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FMRBBILLNO from RDS_ECS_ODS_pur_return where FIsDo=3"

    res=app3.select(sql)

    return res

def getClassfyData(app3,code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    try:

        sql=f"select FMRBBILLNO,FPURORDERNO,FPOORDERSEQ,FBILLTYPEID,FCUSTOMERNUMBER,FSUPPLIERFIELD,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FGOODSTYPEID,FBARCODE,FGOODSID,FPRDNAME,FRETSALEPRICE,FTAXRATE,FLOT,FRETQTY,FRETAMOUNT,FCHECKSTATUS,FUploadDate,FIsDo,FINISHTIME,FDATE,MANUFACTUREDATE,EFFECTDATE,FReturnId from RDS_ECS_ODS_pur_return where FMRBBILLNO='{code['FMRBBILLNO']}'"

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

def code_conversion_org(app2,tableName,param,param2,param3,param4):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select {param4} from {tableName} where {param}='{param2}' and FOrgNumber='{param3}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0][param4]

def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.Fisdo={status} from RDS_ECS_ODS_pur_return a where FMRBBILLNO='{fnumber}'"

    app3.update(sql)



def isbatch(app2,FNumber):

    sql=f"select FISBATCHMANAGE from rds_vw_fisbatch where F_SZSP_SKUNUMBER='{FNumber}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FISBATCHMANAGE']


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


def checkDataExist(app2, FReturnId):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FReturnId from RDS_ECS_SRC_pur_return where FReturnId='{FReturnId}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def insert_procurement_return(app2,data):
    '''
    采购退货
    :param app2:
    :param data:
    :return:
    '''



    for i in data.index:

        if checkDataExist(app2,data.iloc[i]['FReturnId']):

            try:

                sql=f"""insert into RDS_ECS_SRC_pur_return(FMRBBILLNO,FPURORDERNO,FPOORDERSEQ,FBILLTYPEID,FCUSTOMERNUMBER,FSUPPLIERFIELD,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FGOODSTYPEID,FBARCODE,FGOODSID,FPRDNAME,FRETSALEPRICE,FTAXRATE,FLOT,FRETQTY,FRETAMOUNT,FCHECKSTATUS,FUploadDate,FIsDo,FINISHTIME,FDATE,MANUFACTUREDATE,EFFECTDATE,FReturnId) values('{data.iloc[i]['FMRBBILLNO']}','{data.iloc[i]['FPURORDERNO']}','{data.iloc[i]['FPOORDERSEQ']}','{data.iloc[i]['FBILLTYPEID']}','{data.iloc[i]['FSUPPLIERFIELD']}','{data.iloc[i]['FCUSTOMERNUMBER']}','{data.iloc[i]['FSUPPLIERNAME']}','{data.iloc[i]['FSUPPLIERABBR']}','{data.iloc[i]['FSTOCKID']}','{data.iloc[i]['FGOODSTYPEID']}','{data.iloc[i]['FBARCODE']}','{data.iloc[i]['FGOODSID']}','{data.iloc[i]['FPRDNAME']}','{data.iloc[i]['FRETSALEPRICE']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FLOT']}','{data.iloc[i]['FRETQTY']}','{data.iloc[i]['FRETAMOUNT']}','{data.iloc[i]['FCHECKSTATUS']}',getdate(),0,'{data.iloc[i]['FINISHTIME']}','{data.iloc[i]['FDATE']}','{data.iloc[i]['MANUFACTUREDATE']}','{data.iloc[i]['EFFECTDATE']}','{data.iloc[i]['FReturnId']}')"""

                app2.insert(sql)

                insertLog(app2, "采购退料单", data.iloc[i]['FMRBBILLNO'], "数据成功插入", "1")

            except Exception as e:

                insertLog(app2, "采购退料单", data.iloc[i]['FMRBBILLNO'], "数据异常，请检查数据","2")



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