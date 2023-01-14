import pandas as pd
import SaleOrder.rdSaleOrder.operation as sro
import SaleOrder.rdSaleOrder.EcsInterface as se
import SaleOrder.rdSaleOrder.operation as db


def classification_process(app2, data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    df = pd.DataFrame(data)

    df.drop_duplicates("FSALEORDERNO", keep="first", inplace=True)

    codeList = df['FSALEORDERNO'].tolist()

    res = fuz(app2, codeList)

    return res


def fuz(app2, codeList):
    '''
    通过编码分类，将分类好的数据装入列表
    :param app2:
    :param codeList:
    :return:
    '''

    singleList = []

    for i in codeList:
        data = sro.getClassfyData(app2, i)
        singleList.append(data)

    return singleList


def order_view(api_sdk, value):
    '''
    单据查询
    :param value: 订单编码
    :return:
    '''

    res = api_sdk.ExecuteBillQuery(
        {"FormId": "SAL_SaleOrder", "FieldKeys": "FDate,FBillNo,FId,FSaleOrderEntry_FEntryID", "FilterString": [
            {"Left": "(", "FieldName": "FBillNo", "Compare": ">=", "Value": value, "Right": ")", "Logic": "AND"},
            {"Left": "(", "FieldName": "FBillNo", "Compare": "<=", "Value": value, "Right": ")", "Logic": ""}],
         "TopRowCount": 0})

    return res


def writeSRC(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_order_details", startDate, endDate, "FSALEDATE")

    for i in range(1, page + 1):
        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_order_details", startDate, endDate, "FSALEDATE")

        db.insert_SAL_ORDER_Table(app3, df)

    pass
