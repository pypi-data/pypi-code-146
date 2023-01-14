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

        return ""


def checkDataExist(app2, FInvoiceid):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FInvoiceid from RDS_ECS_SRC_pur_invoice where FInvoiceid='{FInvoiceid}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def insert_procurement_contract(app2,app3,data):
    '''
    采购开票
    :param app2:
    :param data:
    :return:
    '''



    for i in data.index:

        if checkDataExist(app2,data.loc[i]['FInvoiceid']):

            if judgementData(app2, app3, data[data['FINVOICENO'] == data.loc[i]['FINVOICENO']]):

                inert_data(app3, data[data['FINVOICENO'] == data.loc[i]['FINVOICENO']])


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

            if code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", data.loc[i]['FPRDNUMBER']) != "" or \
                    data.loc[i]['FPRDNUMBER'] == "1":

                continue

            else:

                insertLog(app3, "应付单", data.loc[i]['FINVOICENO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "应付单", data.loc[i]['FINVOICENO'], "客户不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql=f"insert into RDS_ECS_SRC_pur_invoice(FPURORDERNO,FGODOWNNO,FBILLTYPEINAME,FINVOICEDATE,FINVOICETYPE,FINVOICENO,FDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FAMOUNTALL,FPURCHASEDEPTNAME,FPURCHASEGROUPNAME,FPURCHASERINAME,FDESCRIPTION,FUPLOADDATE,FISDO,FInvoiceid,FLot) values('{data.loc[i]['FPURORDERNO']}','{data.loc[i]['FGODOWNNO']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FINVOICEDATE']}','{data.loc[i]['FINVOICETYPE']}','{data.loc[i]['FINVOICENO']}','{data.loc[i]['FDATE']}','{data.loc[i]['FCUSTOMERNUMBER']}','{data.loc[i]['FSUPPLIERNAME']}','{data.loc[i]['FPOORDERSEQ']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FQTY']}','{data.loc[i]['FUNITPRICE']}','{data.loc[i]['FSUMVALUE']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FTAXAMOUNT']}','{data.loc[i]['FTAXPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FPURCHASEDEPTID']}','{data.loc[i]['FPURCHASEGROUPID']}','{data.loc[i]['FPURCHASERID']}','{data.loc[i]['FDESCRIPTION']}',getdate(),0,'{data.loc[i]['FInvoiceid']}','{data.loc[i]['FLOT']}')"

            app3.insert(sql)

            insertLog(app3, "应付单", data.loc[i]['FINVOICENO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "应付单", data.loc[i]['FINVOICENO'], "插入SRC数据异常，请检查数据","2")

    pass


def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql = "select distinct FINVOICENO from RDS_ECS_ODS_pur_invoice where FIsDo=0"

    res = app3.select(sql)

    return res

def getClassfyData(app3, code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    try:

        number=code['FINVOICENO']

        sql = f"select FPURORDERNO,FGODOWNNO,FBILLTYPEINAME,FINVOICEDATE,FINVOICETYPE,FINVOICENO,FDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FAMOUNTALL,FPURCHASEDEPTNAME,FPURCHASEGROUPNAME,FPURCHASERINAME,FDESCRIPTION,FUPLOADDATE,FISDO,FInvoiceid,FLot from RDS_ECS_ODS_pur_invoice where FINVOICENO='{number}'"

        res = app3.select(sql)

        return res

    except Exception as e:

        return 0


def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.Fisdo={status} from RDS_ECS_ODS_pur_invoice a where FINVOICENO='{fnumber}'"

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


def checkCode(app2,FNumber,FralQty,FLot,FSKU):
    '''
    查看单据内码
    :param app2:
    :param FNumber: 单据编码
    :param FralQty: 实际数量
    :param FLot: 批号
    :param FSKU: SKU编码
    :return:
    '''

    try:

        sql=f"""
            select a.FID,b.FENTRYID,b.FLOT,b.FLOT_TEXT,c.FNUMBER from t_STK_InStock a
            inner join T_STK_INSTOCKENTRY b
            on a.FID=b.FID
            inner join rds_vw_material c
            on c.FMATERIALID=b.FMATERIALID
            where a.FBILLNO='{FNumber}' and FREALQTY='{FralQty}' and b.FLOT_TEXT='{FLot}' and c.F_SZSP_SKUNUMBER='{FSKU}'          
            """

        res=app2.select(sql)

        if res:

            return res[0]

        else:

            return []

    except Exception as e:

        return []


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


