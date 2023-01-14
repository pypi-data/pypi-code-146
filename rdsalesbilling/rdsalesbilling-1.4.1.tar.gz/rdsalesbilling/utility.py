import pandas as pd
from rdsalesbilling import operation as db
from rdsalesbilling import metadata as mt
from rdsalesbilling import EcsInterface as se


def writeSRC(startDate, endDate, app2,app3):
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

        df = df.fillna("")

        db.insert_sales_invoice(app2,app3, df)

# FBILLNO

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


def classification_process(app2, data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    res = fuz(app2, data)

    return res


def data_splicing(app2, api_sdk, data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FEntity
    :param data:
    :return:
    '''

    list = []

    index = 0

    for i in data:

        materialSKU = "" if str(i['FPrdNumber']) == '1' else str(i['FPrdNumber'])

        result=[]

        if int(i['FQUANTITY'])>0:

            result = db.checkFlot(app2, str(i['FOUTSTOCKBILLNO']), str(i['FLot']),
                                  str(i['FQUANTITY']), str(materialSKU))
        else:

            result=db.findRreturnID(app2,str(i['FOUTSTOCKBILLNO']),str(materialSKU),str(i['FLot']),-int(i['FQUANTITY']))

        if index == len(result):

            index = 0

        res = mt.json_model(app2, i, api_sdk, index, result, materialSKU)

        if res:

            list.append(res)

            index = index + 1

            if index == len(result):
                index = 0

        else:

            return []

    return list
