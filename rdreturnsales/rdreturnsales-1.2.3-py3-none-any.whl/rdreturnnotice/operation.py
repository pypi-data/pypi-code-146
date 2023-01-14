def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FMRBBILLNO from RDS_ECS_ODS_sal_returnstock where FIsdo=0 and FIsFree!=1"

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


def code_conversion_org(app2, tableName, param, param2, param3, param4):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql = f"select {param4} from {tableName} where {param}='{param2}' and FOrgNumber='{param3}'"

    res = app2.select(sql)

    if res == []:

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

    sql=f"update a set a.Fisdo={status} from RDS_ECS_ODS_sal_returnstock a where FMRBBILLNO='{fnumber}'"

    app3.update(sql)

def isbatch(app2,FNumber):
    '''
    判断是否启用批号管理
    :param app2:
    :param FNumber:
    :return:
    '''

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


def insert_sales_return(app2,app3,data):
    '''
    销售退货
    :param app2:
    :param data:
    :return:
    '''



    for i in data.index:

        if checkDataExist(app3,data.iloc[i]['FADDID']):

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
        if code_conversion(app2, "rds_vw_customer", "FNAME", data.loc[i]['FCUSTOMNAME']) != "":

            if code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", data.loc[i]['FPRDNUMBER']) != "" or \
                    data.loc[i]['FPRDNUMBER'] == "1":

                if (iskfperiod(app2, data.loc[i]['FPRDNUMBER']) == "1" and data.loc[i]['FPRODUCEDATE'] != "") or \
                        (data.loc[i]['FPRDNUMBER'] == "1") or (iskfperiod(app2, data.loc[i]['FPRDNUMBER']) == "0"):

                    continue

                else:

                    insertLog(app3, "退货通知单",data.loc[i]['FMRBBILLNO'], "生产日期和有效期不能为空","2")

                    flag = False

                    break

            else:

                insertLog(app3, "退货通知单",data.loc[i]['FMRBBILLNO'], "物料不存在","2")

                flag = False

                break
        else:

            insertLog(app3, "退货通知单",data.loc[i]['FMRBBILLNO'], "客户不存在","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in data.index:

        try:

            sql = f"""insert into RDS_ECS_SRC_sal_returnstock(FMRBBILLNO,FTRADENO,FSALEORDERENTRYSEQ,FBILLTYPE,FRETSALESTATE,FPRDRETURNSTATUS,OPTRPTENTRYDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FCUSTCODE,FPrdNumber,FPrdName,FRETSALEPRICE,FRETURNQTY,FREQUESTTIME,FBUSINESSDATE,FCOSTPRICE,FMEASUREUNIT,FRETAMOUNT,FTAXRATE,FLOT,FSALER,FAUXSALER,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FCHECKSTATUS,UPDATETIME,FDELIVERYNO,FIsDo,FIsFree,FADDID,FCurrencyName) values('{data.loc[i]['FMRBBILLNO']}','{data.loc[i]['FTRADENO']}','{data.loc[i]['FSALEORDERENTRYSEQ']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FRETSALESTATE']}','{data.loc[i]['FPRDRETURNSTATUS']}','{data.loc[i]['OPTRPTENTRYDATE']}','{data.loc[i]['FSTOCKID']}','{data.loc[i]['FCUSTNUMBER']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FCUSTCODE']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FRETSALEPRICE']}','{data.loc[i]['FRETURNQTY']}','{data.loc[i]['FREQUESTTIME']}','{data.loc[i]['FBUSINESSDATE']}','{data.loc[i]['FCOSTPRICE']}','{data.loc[i]['FMEASUREUNITID']}','{data.loc[i]['FRETAMOUNT']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FLOT']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FAUXSALERID']}','{data.loc[i]['FSUMSUPPLIERLOT']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}','{data.loc[i]['FCHECKSTATUS']}','{data.loc[i]['UPDATETIME']}','{data.loc[i]['FDELIVERYNO']}',0,0,'{data.loc[i]['FADDID']}','{data.loc[i]['FCURRENCYID']}')"""

            app3.insert(sql)

            insertLog(app3, "退货通知单", data.loc[i]['FMRBBILLNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "退货通知单",data.loc[i]['FMRBBILLNO'], "插入SRC数据异常，请检查数据","2")

    pass



def checkFlot(app2,FBillNo,FLot,REALQTY,FSKUNUM):
    '''
    查看批号
    :return:
    '''

    try:

        sql=f"""
            select a.Fid,b.FENTRYID,b.FLOT,b.FLOT_TEXT,c.F_SZSP_SKUNUMBER,d.FTAXPRICE from T_SAL_OUTSTOCK a
            inner join T_SAL_OUTSTOCKENTRY b
            on a.FID=b.FID
            inner join T_SAL_OUTSTOCKENTRY_F d
            on d.FENTRYID=b.FENTRYID
            inner join rds_vw_material c
            on c.FMATERIALID=b.FMATERIALID
            where a.FBILLNO='{FBillNo}' and FLOT_TEXT='{FLot}' and b.FREALQTY='{REALQTY}' and c.F_SZSP_SKUNUMBER='{FSKUNUM}' 
        """

        res=app2.select(sql)

        if res:

            return res

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