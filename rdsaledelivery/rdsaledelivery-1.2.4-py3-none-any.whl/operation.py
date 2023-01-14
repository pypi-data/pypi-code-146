def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FDELIVERYNO from RDS_ECS_ODS_sal_delivery where FIsdo=3 and FIsFree!=1"

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
        number=code['FDELIVERYNO']

        sql=f"select FInterID,FDELIVERYNO,FTRADENO,FBILLTYPE,FDELIVERYSTATUS,FDELIVERDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FORDERTYPE,FPRDNUMBER,FPRDNAME,FPRICE,FNBASEUNITQTY,FLOT,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,Fisdo,FArStatus,FIsfree,UPDATETIME,FOUTID,FCurrencyName from RDS_ECS_ODS_sal_delivery where FDELIVERYNO='{number}'"

        res=app3.select(sql)

        return res
    except Exception as e:

        return []

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


def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.Fisdo={status} from RDS_ECS_ODS_sal_delivery a where FDELIVERYNO='{fnumber}'"

    app3.update(sql)

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


def checkDataExist(app2, FOUTID):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FOUTID from RDS_ECS_SRC_sal_delivery where FOUTID='{FOUTID}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False

def insert_sales_delivery(app2,app3,data):
    '''
    销售发货
    :param app2:
    :param data:数据源
    :return:
    '''


    for i in data.index:

        if data.loc[i]['FNBASEUNITQTY']!=0 and checkDataExist(app3,data.loc[i]['FOUTID']):

            if judgementData(app2,app3,data[data['FDELIVERYNO']==data.loc[i]['FDELIVERYNO']]):

                inert_data(app3,data[data['FDELIVERYNO']==data.loc[i]['FDELIVERYNO']])




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

                if (iskfperiod(app2, data.loc[i]['FPRDNUMBER']) == "1" and data.loc[i]['FPRODUCEDATE'] != "") or \
                        data.loc[i]['FPRDNUMBER'] == "1" or (iskfperiod(app2, data.loc[i]['FGOODSID']) == "0"):

                    continue

                else:

                    insertLog(app3, "销售出库单", data.loc[i]['FDELIVERYNO'], "生产日期和有效期不能为空","2")

                    flag = False

                    break

            else:

                insertLog(app3, "销售出库单", data.loc[i]['FDELIVERYNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "销售出库单", data.loc[i]['FDELIVERYNO'], "客户不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql = f"insert into RDS_ECS_SRC_sal_delivery(FInterID,FDELIVERYNO,FTRADENO,FBILLTYPE,FDELIVERYSTATUS,FDELIVERDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FORDERTYPE,FPRDNUMBER,FPRDNAME,FPRICE,FNBASEUNITQTY,FLOT,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,Fisdo,FArStatus,FIsfree,UPDATETIME,FOUTID,FCurrencyName) values({int(getFinterId(app3, 'RDS_ECS_SRC_sal_delivery')) + 1},'{data.loc[i]['FDELIVERYNO']}','{data.loc[i]['FTRADENO']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FDELIVERYSTATUS']}','{data.loc[i]['FDELIVERDATE']}','{data.loc[i]['FSTOCKID']}','{data.loc[i]['FCUSTNUMBER']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FORDERTYPE']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FNBASEUNITQTY']}','{data.loc[i]['FLOT']}','{data.loc[i]['FSUMSUPPLIERLOT']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}','{data.loc[i]['FMEASUREUNITID']}','{data.loc[i]['DELIVERYAMOUNT']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FAUXSALERID']}',0,0,0,getdate(),'{data.loc[i]['FOUTID']}','{data.loc[i]['FCURRENCYID']}')"

            app3.insert(sql)

            insertLog(app3, "销售出库单", data.loc[i]['FDELIVERYNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "销售出库单", data.loc[i]['FDELIVERYNO'], "插入SRC数据异常，请检查数据","2")

    pass







