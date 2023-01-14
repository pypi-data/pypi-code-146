#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from rdsalesorder import EcsInterface as se
from rdsalesorder import operation as db

def classification_process(app3, data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    res = fuz(app3, data)

    return res


def fuz(app3, codeList):
    '''
    通过编码分类，将分类好的数据装入列表
    :param app2:
    :param codeList:
    :return:
    '''


    singleList = []

    for i in codeList:

        data = db.getClassfyData(app3, i)

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


def writeSRC(startDate, endDate, app2,app3,api_sdk,option):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_order_details", startDate, endDate, "UPDATETIME")

    if page:

        for i in range(1, page + 1):

            df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_order_details", startDate, endDate, "UPDATETIME")

            db.insert_SAL_ORDER_Table(app2,app3, df,api_sdk,option)

