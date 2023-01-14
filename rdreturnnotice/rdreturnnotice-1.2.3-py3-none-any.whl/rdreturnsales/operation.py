def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FMRBBILLNO from RDS_ECS_ODS_sal_returnstock where FIsdo=3 and FIsFree!=1"

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

        sql=f"select FMRBBILLNO,FTRADENO,FSALEORDERENTRYSEQ,FBILLTYPE,FRETSALESTATE,FPRDRETURNSTATUS,OPTRPTENTRYDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FCUSTCODE,FPrdNumber,FPrdName,FRETSALEPRICE,FRETURNQTY,FREQUESTTIME,FBUSINESSDATE,FCOSTPRICE,FMEASUREUNIT,FRETAMOUNT,FTAXRATE,FLOT,FSALER,FAUXSALER,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FCHECKSTATUS,UPDATETIME,FDELIVERYNO,FIsDo,FIsFree,FADDID,FCurrencyName,FReturnTime from RDS_ECS_ODS_sal_returnstock where FMRBBILLNO='{code['FMRBBILLNO']}'"

        res=app3.select(sql)

        return res

    except Exception as e:

        return []

def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsdo={status} from RDS_ECS_ODS_sal_returnstock a where FMRBBILLNO='{fnumber}'"

    app3.update(sql)


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


def isbatch(app2,FNumber):

    sql=f"select FISBATCHMANAGE from rds_vw_fisbatch where F_SZSP_SKUNUMBER='{FNumber}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FISBATCHMANAGE']


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


def checkDataExist(app2, FADDID):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FADDID from RDS_ECS_SRC_sal_returnstock where FADDID='{FADDID}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def insert_sales_return(app2,data):
    '''
    销售退货
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        if checkDataExist(app2,data.iloc[i]['FADDID']):

            try:

                sql = f"insert into RDS_ECS_SRC_sal_returnstock(FMRBBILLNO,FTRADENO,FSALEORDERENTRYSEQ,FBILLTYPE,FRETSALESTATE,FPRDRETURNSTATUS,OPTRPTENTRYDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FCUSTCODE,FPrdNumber,FPrdName,FRETSALEPRICE,FRETURNQTY,FREQUESTTIME,FBUSINESSDATE,FCOSTPRICE,FMEASUREUNIT,FRETAMOUNT,FTAXRATE,FLOT,FSALER,FAUXSALER,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FCHECKSTATUS,UPDATETIME,FDELIVERYNO,FIsDo,FIsFree,FADDID,FCurrencyName) values('{data.iloc[i]['FMRBBILLNO']}','{data.iloc[i]['FTRADENO']}','{data.iloc[i]['FSALEORDERENTRYSEQ']}','{data.iloc[i]['FBILLTYPEID']}','{data.iloc[i]['FRETSALESTATE']}','{data.iloc[i]['FPRDRETURNSTATUS']}','{data.iloc[i]['OPTRPTENTRYDATE']}','{data.iloc[i]['FSTOCKID']}','{data.iloc[i]['FCUSTNUMBER']}','{data.iloc[i]['FCUSTOMNAME']}','{data.iloc[i]['FCUSTCODE']}','{data.iloc[i]['FPRDNUMBER']}','{data.iloc[i]['FPRDNAME']}','{data.iloc[i]['FRETSALEPRICE']}','{data.iloc[i]['FRETURNQTY']}','{data.iloc[i]['FREQUESTTIME']}','{data.iloc[i]['FBUSINESSDATE']}','{data.iloc[i]['FCOSTPRICE']}','{data.iloc[i]['FMEASUREUNITID']}','{data.iloc[i]['FRETAMOUNT']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FLOT']}','{data.iloc[i]['FSALERID']}','{data.iloc[i]['FAUXSALERID']}','{data.iloc[i]['FSUMSUPPLIERLOT']}','{data.iloc[i]['FPRODUCEDATE']}','{data.iloc[i]['FEFFECTIVEDATE']}','{data.iloc[i]['FCHECKSTATUS']}',getdate(),'{data.iloc[i]['FDELIVERYNO']}',0,0,'{data.iloc[i]['FADDID']}','{data.iloc[i]['FCURRENCYID']}')"

                app2.insert(sql)

            except Exception as e:

                insertLog(app2, "销售退货单数据插入SRC", data.iloc[i]['FMRBBILLNO'], "数据异常，请检查数据")



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