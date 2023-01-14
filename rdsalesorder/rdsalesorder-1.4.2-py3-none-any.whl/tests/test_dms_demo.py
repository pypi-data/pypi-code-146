from pyrda.dbms.rds import RdClient

app2 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
# app2 = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
import pandas as pd

def inertLog(app2,FProgramName,FNumber,Message):
    '''
    异常数据日志
    :param app2:
    :param FNumber:
    :param Message:
    :return:
    '''

    sql=f"""insert into RDS_CP_ECS_Log(FProgramName,FNumber,FMessage,FOccurrenceTime) values('{FProgramName}','{FNumber}','{Message}',getdate())"""

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


def IsUpdate(app3, seq):
    sql = f"select FSALEORDERNO,UPDATETIME from RDS_ECS_SRC_Sales_Order where FSALEORDERENTRYSEQ='{seq}'"

    res = app3.select(sql)

    for i in res:

        print(i)





if __name__ == '__main__':

    # res=findRreturnID(app2,"R202210240001","BSP10009-1","B202209150002","103")
    #
    # print(res)

    # sql="select * from RDS_ECS_ODS_sal_billreceivable where FINVOICEDATE>='2022-12-01'"
    #
    # res=app2.select(sql)
    # # print(res)
    #
    # for i in res:
    #
    #     print(i)

    # df=pd.DataFrame(res)
    #
    # df.to_excel('D:\\test_skyx.xlsx')

    # sql = "update a set a.FIsDO=0 from RDS_ECS_ODS_Sales_Order a where a.FIsdo=2 and a.FIsFree!=1 and a.FSALEDATE>='2022-10-01'"
    #
    # app2.update(sql)

    # sql = "update a set a.FIsdo=0  from RDS_ECS_ODS_sal_billreceivable a where a.FINVOICEDATE>='2022-12-01'"
    #
    # app2.update(sql)

    # sql = "select * from RDS_ECS_ODS_sal_billreceivable where FBILLNO='S202212010002'"
    #
    # res=app2.select(sql)
    #
    # for i in res:
    #
    #     print(i)

    IsUpdate(app2,"22666")

    # sql = "select * from RDS_ECS_ODS_Sales_Order where FSALEDATE>='2023-01-13'"
    #
    # res = app2.select(sql)
    #
    # for i in res:
    #     print(i)

    # res = checkFlot(app2, "D202211300023", "B202210170006", "20", "BC2019")
    #
    # index=0
    #
    # while(index<=len(res)-1):
    #
    #     print(res[index])
    #
    #     index=index+1

    # res=checkCode(app2,"PI202212210007","200","","BYK10001")
    #
    # print(res)

    # inertLog(app2,"测试","1111111","数据异常")



