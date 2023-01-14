import SaleOrder.rdsalesorder.EcsInterface as se
import SaleOrder.rdsalesorder.operation as db
from pyrda.dbms.rds import RdClient
if __name__ == '__main__':

    app2 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_order_details", "2022-11-01 00:00:00","2022-11-30 23:59:59", "FSALEDATE")

    for i in range(1,page+1):

        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_order_details", "2022-11-01 00:00:00","2022-11-30 23:59:59", "FSALEDATE")

        db.insert_SAL_ORDER_Table(app2,df)

    # sql="select * from rds_vw_billType"
    #
    # res=app2.select(sql)
    #
    # print(res)

    # df = se.ECS_post_info2(url, 1, 1000, "ge", "le", "v_sales_order_details", "2022-11-01 00:00:00",
    #                        "2022-11-30 23:59:59", "FSALEDATE")

    # df.to_excel("D:\\test1.xlsx")

    # print(df)

    # page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_order_details", "2022-11-01 00:00:00", "2022-11-30 23:59:59",
    #                    "FSALEDATE")


