def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FGODOWNNO from RDS_ECS_ODS_pur_storageacct where FIsdo=0 and FIsFree!=1"

    res=app3.select(sql)

    return res


def getClassfyData(app3, code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    try:

        number=code['FGODOWNNO']

        sql = f"select FGODOWNNO,FBILLNO,FPOORDERSEQ,FBILLTYPEID,FDOCUMENTSTATUS,FSUPPLIERFIELD,FCUSTOMERNUMBER,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FLIBRARYSIGN,FBUSINESSDATE,FBARCODE,FGOODSID,FPRDNAME,FINSTOCKQTY,FPURCHASEPRICE,FAMOUNT,FTAXRATE,FLOT,FCHECKSTATUS,FDESCRIPTION,FUPDATETIME,FInstockId,FArrivalDate,FUPDATETIME,FIsFree from RDS_ECS_ODS_pur_storageacct where FGODOWNNO='{number}'"

        res = app3.select(sql)

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

    sql=f"update a set a.FIsdo={status} from RDS_ECS_ODS_pur_storageacct a where FGODOWNNO='{fnumber}'"

    app3.update(sql)


def checkDataExist(app2, FInstockId):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FInstockId from RDS_ECS_SRC_pur_storageacct where FInstockId='{FInstockId}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False

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


def insert_procurement_storage(app2,app3,data):
    '''
    采购入库
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        if checkDataExist(app3,data.loc[i]['FInstockId']):

            if judgementData(app2, app3, data[data['FGODOWNNO'] == data.loc[i]['FGODOWNNO']]):
                inert_data(app3, data[data['FGODOWNNO'] == data.loc[i]['FGODOWNNO']])

        else:

            insertLog(app3, "收料通知单数据插入SRC", data.loc[i]['FGODOWNNO'], "订单重复")


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

                if (iskfperiod(app2, data.loc[i]['FGOODSID']) == "1" and data.loc[i]['FPRODUCEDATE'] != "") or \
                        data.loc[i]['FGOODSID'] == "1"  or (iskfperiod(app2, data.loc[i]['FGOODSID']) == "0"):

                    continue

                else:

                    insertLog(app3, "收料通知单", data.loc[i]['FGODOWNNO'], "生产日期和有效期不能为空","2")

                    flag = False

                    break

            else:

                insertLog(app3, "收料通知单", data.loc[i]['FGODOWNNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "收料通知单", data.loc[i]['FGODOWNNO'], "供应商不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql=f"""insert into RDS_ECS_SRC_pur_storageacct(FGODOWNNO,FBILLNO,FPOORDERSEQ,FBILLTYPEID,FDOCUMENTSTATUS,FSUPPLIERFIELD,FCUSTOMERNUMBER,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FLIBRARYSIGN,FBUSINESSDATE,FBARCODE,FGOODSID,FPRDNAME,FINSTOCKQTY,FPURCHASEPRICE,FAMOUNT,FTAXRATE,FLOT,FCHECKSTATUS,FDESCRIPTION,FUPDATETIME,FInstockId,FPRODUCEDATE,FEFFECTIVEDATE) values('{data.loc[i]['FGODOWNNO']}','{data.loc[i]['FBILLNO']}','{data.loc[i]['FPOORDERSEQ']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FDOCUMENTSTATUS']}','{data.loc[i]['FSUPPLIERFIELD']}','{data.loc[i]['FCUSTOMERNUMBER']}','{data.loc[i]['FSUPPLIERNAME']}','{data.loc[i]['FSUPPLIERABBR']}','{data.loc[i]['FSTOCKID']}','{data.loc[i]['FLIBRARYSIGN']}','{data.loc[i]['FBUSINESSDATE']}','{data.loc[i]['FBARCODE']}','{data.loc[i]['FGOODSID']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FINSTOCKQTY']}','{data.loc[i]['FPURCHASEPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FLOT']}','{data.loc[i]['FCHECKSTATUS']}','',getdate(),'{data.loc[i]['FInstockId']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}')"""

            app3.insert(sql)

            insertLog(app3, "收料通知单", data.loc[i]['FGODOWNNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "收料通知单", data.loc[i]['FGODOWNNO'], "插入SRC数据异常，请检查数据","2")

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