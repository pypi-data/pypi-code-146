def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select FDELIVERYNO from RDS_CRM_SRC_sal_delivery where FIsdo=0 and FIsFree!=1 "

    res=app3.select(sql)

    return res

def getClassfyData(app3,code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql=f"select FInterID,FDELIVERYNO,FTRADENO,FBILLTYPE,FDELIVERYSTATUS,FDELIVERDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FORDERTYPE,FPRDNUMBER,FPRDNAME,FPRICE,FNBASEUNITQTY,FLOT,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,Fisdo,FArStatus,FIsfree,UPDATETIME,FOUTID,FDATE,FCurrencyName from RDS_CRM_SRC_sal_delivery where FDELIVERYNO='{code}'"

    res=app3.select(sql)

    return res

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

    sql=f"update a set a.Fisdo={status} from RDS_CRM_SRC_sal_delivery a where FDELIVERYNO='{fnumber}'"

    app3.update(sql)

def getFinterId(app2, tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''

    sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"

    res = app2.select(sql)

    return res[0]['FMaxId']


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

def insert_sales_delivery(app2,data):
    '''
    销售发货
    :param app2:
    :param data:数据源
    :return:
    '''

    for i in data.index:

        if data.loc[i]['FNBASEUNITQTY']!=0 and checkDataExist(app2,data.loc[i]['FOUTID']):

            sql=f"insert into RDS_ECS_SRC_sal_delivery(FInterID,FDELIVERYNO,FTRADENO,FBILLTYPE,FDELIVERYSTATUS,FDELIVERDATE,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,FORDERTYPE,FPRDNUMBER,FPRDNAME,FPRICE,FNBASEUNITQTY,FLOT,FSUMSUPPLIERLOT,FPRODUCEDATE,FEFFECTIVEDATE,FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,Fisdo,FArStatus,FIsfree,UPDATETIME,FOUTID,FCurrencyName) values({getFinterId(app2,'RDS_ECS_SRC_sal_delivery')+1},'{data.loc[i]['FDELIVERYNO']}','{data.loc[i]['FTRADENO']}','{data.loc[i]['FBILLTYPEID']}','{data.loc[i]['FDELIVERYSTATUS']}','{data.loc[i]['FDELIVERDATE']}','{data.loc[i]['FSTOCKID']}','{data.loc[i]['FCUSTNUMBER']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FORDERTYPE']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FNBASEUNITQTY']}','{data.loc[i]['FLOT']}','{data.loc[i]['FSUMSUPPLIERLOT']}','{data.loc[i]['FPRODUCEDATE']}','{data.loc[i]['FEFFECTIVEDATE']}','{data.loc[i]['FMEASUREUNITID']}','{data.loc[i]['DELIVERYAMOUNT']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FAUXSALERID']}',0,0,0,getdate(),'{data.loc[i]['FOUTID']}','{data.loc[i]['FCURRENCYID']}')"

            app2.insert(sql)