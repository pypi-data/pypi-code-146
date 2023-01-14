import EcsToDms.EcsInterface as e
from pyrda.dbms.rds import RdClient
import pandas as pd
app2 = RdClient(token='A597CB38-8F32-40C8-97BC-111823AA7765')
import SaleOrder.rdsalesorder.mainModel as sm

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

def insert_SAL_ORDER_Table(app2,data):
    '''
    销售订单
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        sql=f"insert into rds_sal_order(FInterID,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTNUMBER,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FAMOUNT,FSALDEPTNAME,FSALGROUPNAME,FSALERNAME,FDESCRIPTION,FUploadDate,Fisdo) values({getFinterId(app2,'rds_sal_order')+1},'{data.loc[i]['FSALEORDERNO']}','{data.loc[i]['FBILLTYPEIDNAME']}','{data.loc[i]['FSALEDATE']}','{data.loc[i]['FCUSTNUMBER']}','{data.loc[i]['FCUSTOMNAME']}','{data.loc[i]['FSALEORDERENTRYSEQ']}','{data.loc[i]['FPRDNUMBER']}','{data.loc[i]['FPRDNAME']}','{data.loc[i]['FQTY']}','{data.loc[i]['FPRICE']}','{data.loc[i]['FMONEY']}','{data.loc[i]['FTAXRATE']}','{data.loc[i]['FTAXAMOUNT']}','{data.loc[i]['FTAXPRICE']}','{data.loc[i]['FAMOUNT']}','{data.loc[i]['FSALDEPTID']}','{data.loc[i]['FSALGROUPID']}','{data.loc[i]['FSALERID']}','{data.loc[i]['FDESCRIPTION']}',getdate(),0)"

        app2.insert(sql)


if __name__ == '__main__':

    url= "https://kingdee-api.bioyx.cn/dynamic/query"

    df=e.ECS_post_info(url,1,1000,"ge","v_sales_order_details","2022-08-01 09:19:39.000")

    df=df.fillna("")
    # print(df)

    insert_SAL_ORDER_Table(app2,df)
    #
    # option1 = {
    #     "acct_id": '63310e555e38b1',
    #     "user_name": '张志',
    #     "app_id": '234673_6darRxsuzoGe5U+t5+WCVZ/KTNQY5Nnv',
    #     "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    #     "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    # }
    #
    # sm.perform(option1,"","")