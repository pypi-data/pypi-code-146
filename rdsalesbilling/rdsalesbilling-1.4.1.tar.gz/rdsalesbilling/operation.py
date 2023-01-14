def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql = "select distinct FBILLNO from RDS_ECS_ODS_sal_billreceivable where FIsDo=0"

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

        number=code['FBILLNO']

        sql = f"select FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,FCUSTOMNAME,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,FBILLCODE,FINVOICENO,FINVOICEDATE,UPDATETIME,Fisdo,FCurrencyName,FInvoiceid,FLot from RDS_ECS_ODS_sal_billreceivable where FBILLNO='{number}'"

        res = app3.select(sql)

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


def checkDataExist(app2, FInvoiceid):
    '''
    判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FInvoiceid from RDS_ECS_SRC_sal_billreceivable where FInvoiceid='{FInvoiceid}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def changeStatus(app3, fnumber, status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql = f"update a set a.Fisdo={status} from RDS_ECS_ODS_sal_billreceivable a where FBILLNO='{fnumber}'"

    app3.update(sql)


def insert_sales_invoice(app2,app3, data):
    '''
    销售开票
    :param app2:
    :param data:
    :return:
    '''



    for i in data.index:

        if checkDataExist(app3, data.iloc[i]['FInvoiceid']) and data.iloc[i]['FQUANTITY'] != '':

            if judgementData(app2, app3, data[data['FBILLNO'] == data.loc[i]['FBILLNO']]):

                inert_data(app3, data[data['FBILLNO'] == data.loc[i]['FBILLNO']])




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


def findSalesNo(app3,fnumber):
    '''
    通过销售出库单号查出对应的销售员编码
    :param app3:
    :param fnumber:
    :return:
    '''

    sql=f"""
    select a.FSALESMANID,b.FNAME,b.FNUMBER from T_SAL_OUTSTOCK a
    inner join rds_vw_salesman b
    on a.FSALESMANID=b.fid
    where a.FBILLNO='{fnumber}'
    """

    res=app3.select(sql)

    if res:

        return res[0]['FNUMBER']

    else:

        return ""

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


def findRreturnID(app2,FBILLNO,F_SZSP_SKUNUMBER,FLOT_TEXT,FREALQTY):
    '''
    找到退货单id
    :param app2:
    :return:
    '''

    sql=f"""
        select a.FID,b.FENTRYID,b.FLOT_TEXT,b.FREALQTY,c.F_SZSP_SKUNUMBER,d.FTAXPRICE from T_SAL_RETURNSTOCK a
        inner join T_SAL_RETURNSTOCKENTRY b
        on a.FID=b.FID
        inner join rds_vw_material c
        on c.FMATERIALID=b.FMATERIALID
        inner join T_SAL_RETURNSTOCKENTRY_F d
        on d.FENTRYID=b.FENTRYID
        where a.FBILLNO='{FBILLNO}'and c.F_SZSP_SKUNUMBER='{F_SZSP_SKUNUMBER}' and b.FLOT_TEXT='{FLOT_TEXT}' and b.FREALQTY='{FREALQTY}'"""

    res=app2.select(sql)

    if res:

        return res

    else:

        return []


def judgementData(app2, app3, data):
    '''
    判断数据是否合规
    :param app2:
    :param data:
    :return:
    '''

    flag = True

    for i in data.index:

        if data.loc[i]['FQUANTITY'] != "":

            if code_conversion(app2, "rds_vw_customer", "FNAME", data.loc[i]['FCUSTOMNAME']) != "":

                if code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", data.loc[i]['FPrdNumber']) != "" or \
                        data.loc[i]['FPrdNumber'] == "1":

                    continue

                else:

                    insertLog(app3, "应收单", data.loc[i]['FBILLNO'], "物料不存在","2")

                    flag = False

                    break
            else:

                insertLog(app3, "应收单", data.loc[i]['FBILLNO'], "客户不存在","2")

                flag = False

                break

        else:

            insertLog(app3, "应收单", data.loc[i]['FBILLNO'], "数量为空","2")

            flag = False

            break

    return flag


def inert_data(app3,data):

    for i in range(0,len(data)):

        try:

            sql = f"""insert into RDS_ECS_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,FCUSTOMNAME,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,FBILLCODE,FINVOICENO,FINVOICEDATE,UPDATETIME,Fisdo,FCurrencyName,FInvoiceid,FLot) values({int(getFinterId(app3, 'RDS_ECS_SRC_sal_billreceivable')) + 1},'{data.iloc[i]['FCUSTNUMBER']}','{data.iloc[i]['FOUTSTOCKBILLNO']}','{data.iloc[i]['FSALEORDERENTRYSEQ']}','{data.iloc[i]['FBILLTYPEID']}','{data.iloc[i]['FCUSTOMNAME']}','{data.iloc[i]['FBILLNO']}','{data.iloc[i]['FPrdNumber']}','{data.iloc[i]['FPrdName']}','{int(data.iloc[i]['FQUANTITY'])}','{data.iloc[i]['FUNITPRICE']}','{data.iloc[i]['FSUMVALUE']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FTRADENO']}','{data.iloc[i]['FNOTETYPE']}','{data.iloc[i]['FISPACKINGBILLNO']}','{data.iloc[i]['FBILLCODE']}','{data.iloc[i]['FINVOICENO']}','{data.iloc[i]['FINVOICEDATE']}',getdate(),0,'{data.iloc[i]['FCURRENCYID']}','{data.iloc[i]['FInvoiceid']}','{data.iloc[i]['FLOT']}')"""

            app3.insert(sql)

            insertLog(app3, "应收单", data.iloc[i]['FBILLNO'], "数据插入成功", "1")

        except Exception as e:

            insertLog(app3, "应收单", data.iloc[i]['FBILLNO'], "插入SRC数据异常，请检查数据","2")

    pass


