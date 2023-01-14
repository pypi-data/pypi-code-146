from crmSaleBilling import operation as db
from crmSaleBilling import EcsInterface as se
from crmSaleBilling import metadata as mt
import pandas as pd


def writeSRC(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_invoice", startDate, endDate, "FINVOICEDATE")

    for i in range(1, page + 1):
        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_invoice", startDate, endDate, "FINVOICEDATE")

        db.insert_sales_invoice(app3, df)


def classification_process(app2, data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    df = pd.DataFrame(data)

    df.drop_duplicates("FBILLNO", keep="first", inplace=True)

    codeList = df['FBILLNO'].tolist()

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
        data = db.getClassfyData(app2, i)
        singleList.append(data)

    return singleList

def data_splicing(app2,api_sdk,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FEntity
    :param data:
    :return:
    '''

    list=[]

    for i in data:
        if mt.json_model(app2, i, api_sdk):

            list.append(mt.json_model(app2,i,api_sdk))

    return list

