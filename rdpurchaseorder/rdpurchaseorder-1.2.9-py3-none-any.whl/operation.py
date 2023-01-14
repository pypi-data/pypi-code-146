from rdpurchaseorder import metadata as mt


def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FPURORDERNO from RDS_ECS_ODS_pur_poorder where FIsdo=0 and FIsFree!=1"

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

        number=code['FPURORDERNO']

        sql=f"select FPURORDERNO,FBILLTYPENAME,FPURCHASEDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FAMOUNT,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FORAMOUNTFALL,FPURCHASEDEPTID,FPURCHASEGROUPID,FPURCHASERID,FDESCRIPTION,FUploadDate,FIsDo,FDeliveryDate,FIsFree from RDS_ECS_ODS_pur_poorder where FPURORDERNO='{number}'"

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

def code_conversion_org(app2,tableName,param,param2,param3):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select FNumber from {tableName} where {param}='{param2}' and FORGNUMBER='{param3}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FNumber']

def changeStatus(app2,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsDo={status} from RDS_ECS_ODS_pur_poorder a where FPURORDERNO='{fnumber}'"

    app2.update(sql)


def checkDataExist(app2, FOrderId):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FOrderId from RDS_ECS_SRC_pur_poorder where FOrderId='{FOrderId}'"

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

    sql1=f"delete from RDS_ECS_SRC_pur_poorder where FPURORDERNO='{FNumber}'"

    app3.delete(sql1)

    sql2 = f"delete from RDS_ECS_ODS_pur_poorder where FPURORDERNO='{FNumber}'"

    app3.delete(sql2)

    return True


def IsUpdate(app3,seq,updateTime,api_sdk,option):

    flag=False

    sql=f"select FPURORDERNO,FUpDateTime from RDS_ECS_SRC_pur_poorder where FOrderId='{seq}'"

    res=app3.select(sql)

    if res:

        try:

            if str(res[0]['FUpDateTime'])!=updateTime:

                flag=True

                deleteResult=deleteOldDate(app3,res[0]['FPURORDERNO'])

                if deleteResult:

                    unAuditResult=mt.unAudit(api_sdk,res[0]['FPURORDERNO'],option)

                    if unAuditResult:

                        mt.delete(api_sdk,res[0]['FPURORDERNO'],option)

                else:

                    insertLog(app3, "采购订单",res[0]['FPURORDERNO'], "反审核失败", "2")


        except Exception as e:

            insertLog(app3, "采购订单", res[0]['FPURORDERNO'], "更新数据失败", "2")

            return False

    return flag


def insert_procurement_order(app2,app3,data,api_sdk,option):
    '''
    采购订单
    :param app2:
    :param data:
    :return:
    '''


    for i in data.index:

        if checkDataExist(app3,data.loc[i]['FOrderId']) or IsUpdate(app3,data.loc[i]['FOrderId'],data.loc[i]['UPDATETIME'],api_sdk,option):

            if judgementData(app2, app3, data[data['FPURORDERNO'] == data.loc[i]['FPURORDERNO']]):

                inert_data(app3, data[data['FPURORDERNO'] == data.loc[i]['FPURORDERNO']])



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

                insertLog(app3, "采购订单",  data.loc[i]['FPURORDERNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "采购订单",  data.loc[i]['FPURORDERNO'], "供应商不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql = f"""insert into RDS_ECS_SRC_pur_poorder(FPURORDERNO,FBILLTYPENAME,FPURCHASEDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FAMOUNT,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FORAMOUNTFALL,FPURCHASEDEPTID,FPURCHASEGROUPID,FPURCHASERID,FUploadDate,FIsDo,FIsFree,FUpDateTime,FOrderId,FDESCRIPTION) values('{data.loc[i]['FPURORDERNO']}','{data.loc[i]['FBILLTYPENAME']}','{data.loc[i]['FPURCHASEDATE']}','{data.loc[i]['FCUSTOMERNUMBER']}','{data.loc[i]['FSUPPLIERNAME']}','{data.loc[i]['FPOORDERSEQ']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FQTY']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FTAXAMOUNT']}','{data.loc[i]['FTAXPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FPURCHASEDEPTID']}','{data.loc[i]['FPURCHASEGROUPID']}','{data.loc[i]['FPURCHASERID']}',getdate(),0,0,'{data.loc[i]['UPDATETIME']}','{data.loc[i]['FOrderId']}','{data.loc[i]['FDESCRIPTION']}')"""

            app3.insert(sql)

            insertLog(app3, "采购订单", data.loc[i]['FPURORDERNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "采购订单", data.loc[i]['FPURORDERNO'], "插入SRC数据异常，请检查数据","2")

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