def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FMRBBILLNO from RDS_ECS_ODS_pur_return where FIsDo=0"

    res=app3.select(sql)

    return res


def isbatch(app2,FNumber):

    sql=f"select FISBATCHMANAGE from rds_vw_fisbatch where F_SZSP_SKUNUMBER='{FNumber}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FISBATCHMANAGE']


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


def insert_procurement_return(app2,app3,data):
    '''
    采购退货
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        if checkDataExist(app3,data.loc[i]['FReturnId']):

            if judgementData(app2, app3, data[data['FMRBBILLNO'] == data.loc[i]['FMRBBILLNO']]):

                inert_data(app3, data[data['FMRBBILLNO'] == data.loc[i]['FMRBBILLNO']])


def judgementData(app2, app3, data):
    '''
    判断数据是否合规
    :param app2:
    :param data:
    :return:
    '''

    flag = True

    for i in data.index:
        if code_conversion(app2, "rds_vw_supplier", "FNAME", data.loc[i]['FSUPPLIERNAME']) != "":

            if code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", data.loc[i]['FGOODSID']) != "" or \
                    data.loc[i]['FGOODSID'] == "1":

                continue

            else:

                insertLog(app3, "退料申请单", data.loc[i]['FMRBBILLNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "退料申请单", data.loc[i]['FMRBBILLNO'], "客户不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql=f"insert into RDS_ECS_SRC_pur_return(FMRBBILLNO,FPURORDERNO,FPOORDERSEQ,FBILLTYPEID,FCUSTOMERNUMBER,FSUPPLIERFIELD,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FGOODSTYPEID,FBARCODE,FGOODSID,FPRDNAME,FRETSALEPRICE,FTAXRATE,FLOT,FRETQTY,FRETAMOUNT,FCHECKSTATUS,FUploadDate,FIsDo,FINISHTIME,FDATE,MANUFACTUREDATE,EFFECTDATE,FReturnId) values('{data.loc[i]['FMRBBILLNO']}','{data.loc[i]['FPURORDERNO']}','{data.loc[i]['FPOORDERSEQ']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FSUPPLIERFIELD']}','{data.loc[i]['FCUSTOMERNUMBER']}','{data.loc[i]['FSUPPLIERNAME']}','{data.loc[i]['FSUPPLIERABBR']}','{data.loc[i]['FSTOCKID']}','{data.loc[i]['FGOODSTYPEID']}','{data.loc[i]['FBARCODE']}','{data.loc[i]['FGOODSID']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FRETSALEPRICE']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FLOT']}','{data.loc[i]['FRETQTY']}','{data.loc[i]['FRETAMOUNT']}','{data.loc[i]['FCHECKSTATUS']}',getdate(),0,'{data.loc[i]['FINISHTIME']}','{data.loc[i]['FDATE']}','{data.loc[i]['MANUFACTUREDATE']}','{data.loc[i]['EFFECTDATE']}','{data.loc[i]['FReturnId']}')"

            app3.insert(sql)

            insertLog(app3, "退料申请单", data.loc[i]['FMRBBILLNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "退料申请单", data.loc[i]['FMRBBILLNO'], "插入SRC数据异常，请检查数据","2")

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