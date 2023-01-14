from pyrda.dbms.rds import RdClient
app2 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
import pandas as pd

if __name__ == '__main__':

    sql="select * from RDS_ECS_ODS_sal_delivery where FTRADENO='202210280043' and FDELIVERYNO='D202210280062' and FLOT='B202210170005'"

    res=app2.select(sql)

    print(len(res))

    for i in res:

        print(i)

    # df=pd.DataFrame(res)
    #
    # df.to_excel("D:\\test_skyx.xlsx")

