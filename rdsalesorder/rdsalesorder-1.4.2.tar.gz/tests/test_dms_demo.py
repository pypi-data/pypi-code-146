from pyrda.dbms.rds import RdClient
app2 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
# app3=RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
import pandas as pd
if __name__ == '__main__':

    sql="select * from RDS_ECS_SRC_Test_sales_order"

    res=app2.select(sql)
    # print(res)

    for i in res:

        print(i)

    # df=pd.DataFrame(res)
    #
    # df.to_excel('D:\\test_skyx.xlsx')

    # sql = "update a set a.FIsDO=0 from RDS_ECS_ODS_Sales_Order a where a.FIsdo=2 and a.FIsFree!=1 and a.FSALEDATE>='2022-10-01'"
    #
    # app2.update(sql)


