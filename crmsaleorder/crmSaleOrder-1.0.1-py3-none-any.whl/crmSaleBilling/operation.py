def getFinterId(app2,tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''

    sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"

    res = app2.select(sql)

    return res[0]['FMaxId']


def checkDataExist(app2, FInvoiceid):
    '''
    判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FInvoiceid from RDS_CRM_SRC_sal_billreceivablee where FInvoiceid={FInvoiceid}"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False

def insert_sales_invoice(app2,data):
    '''
    销售开票
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2,data.iloc[i]['FInvoiceid']):

            sql = f"insert into RDS_CRM_SRC_sal_billreceivablee(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,FCUSTOMNAME,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,FBILLCODE,FINVOICENO,FINVOICEDATE,UPDATETIME,Fisdo,FCurrencyName,FInvoiceid) values({getFinterId(app2, 'RDS_CRM_SRC_sal_billreceivablee') + 1},'{data.iloc[i]['FCUSTNUMBER']}','{data.iloc[i]['FOUTSTOCKBILLNO']}','{data.iloc[i]['FSALEORDERENTRYSEQ']}','{data.iloc[i]['FBILLTYPEID']}','{data.iloc[i]['FCUSTOMNAME']}','{data.iloc[i]['FBILLNO']}','{data.iloc[i]['FPrdNumber']}','{data.iloc[i]['FPrdName']}','{data.iloc[i]['FQUANTITY']}','{data.iloc[i]['FUNITPRICE']}','{data.iloc[i]['FSUMVALUE']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FTRADENO']}','{data.iloc[i]['FNOTETYPE']}','{data.iloc[i]['FISPACKINGBILLNO']}','{data.iloc[i]['FBILLCODE']}','{data.iloc[i]['FINVOICENO']}','{data.iloc[i]['FINVOICEDATE']}',getdate(),0,'{data.iloc[i]['FCURRENCYID']}','{data.iloc[i]['FInvoiceid']}')"

            app2.insert(sql)


def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql = "select * from RDS_CRM_SRC_sal_billreceivable where FIsDo=0"

    res = app3.select(sql)

    return res

def getClassfyData(app3, code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql = f"select FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,FCUSTOMNAME,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FUNITPRICE,FSUMVALUE,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,FBILLCODE,FINVOICENO,FINVOICEDATE,UPDATETIME,Fisdo,FCurrencyName,FInvoiceid from RDS_CRM_SRC_sal_billreceivable where FBILLNO='{code}'"

    res = app3.select(sql)

    return res


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

    sql=f"update a set a.Fisdo={status} from RDS_CRM_SRC_sal_billreceivable a where FBILLNO='{fnumber}'"

    app3.update(sql)
