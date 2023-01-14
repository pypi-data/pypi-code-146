import pandas as pd
import json
from crmNoticeShipment import operation as db
from crmNoticeShipment import EcsInterface as ne


def classification_process(app3, data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    df = pd.DataFrame(data)

    df.drop_duplicates("FDELIVERYNO", keep="first", inplace=True)

    codeList = df['FDELIVERYNO'].tolist()

    res = fuz(app3, codeList)

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


def data_splicing(app2, api_sdk, data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''

    list = []

    for i in data:
        if json_model(app2, i, api_sdk):

            list.append(json_model(app2, i, api_sdk))

        else:
            return []

    return list


def saleOrder_view(api_sdk, value, materialID):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res = json.loads(api_sdk.ExecuteBillQuery(
        {"FormId": "SAL_SaleOrder", "FieldKeys": "FDate,FBillNo,FId,FSaleOrderEntry_FEntryID,FMaterialId",
         "FilterString": [{"Left": "(", "FieldName": "FMaterialId", "Compare": "=", "Value": materialID, "Right": ")",
                           "Logic": "AND"},
                          {"Left": "(", "FieldName": "FBillNo", "Compare": "=", "Value": value, "Right": ")",
                           "Logic": "AND"}], "TopRowCount": 0}))

    return res


def json_model(app2, model_data, api_sdk):
    materialId = db.code_conversion_org(app2, "rds_vw_material", "FNUMBER", model_data['FPRDNUMBER'], "101", "FMATERIALID")


    result = saleOrder_view(api_sdk, str(model_data['FTRADENO']), materialId)

    if result != [] and materialId != "":

        model = {
            "FRowType": "Standard" if model_data['FPRDNUMBER'] != '1' else "Service",
            "FMaterialID": {
                "FNumber":  model_data['FPRDNUMBER']
            },
            "FQty": str(model_data['FNBASEUNITQTY']),
            "FDeliveryDate": str(model_data['FDATE']),
            "FStockID": {
                "FNumber": "SK01" if model_data['FSTOCK'] == "苏州总仓" or model_data['FSTOCK'] == "" else "SK02"
            },
            "FTaxPrice": str(model_data['FPRICE']),
            "FIsFree": True if float(model_data['FIsfree']) == 1 else False,
            "FAllAmount": str(model_data['DELIVERYAMOUNT']),
            "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
            "FLot": {
                "FNumber": str(model_data['FLOT'])
            },
            "FPRODUCEDATE": str(model_data['FPRODUCEDATE']),
            "FEXPIRYDATE": str(model_data['FEFFECTIVEDATE']),

            "FStockStatusId": {
                "FNumber": "KCZT01_SYS"
            },
            "FOutContROL": True,
            "FOutMaxQty": str(model_data['FNBASEUNITQTY']),
            "FOutMinQty": str(model_data['FNBASEUNITQTY']),
            "FPriceBaseQty": str(model_data['FNBASEUNITQTY']),
            "FPlanDeliveryDate": str(model_data['FDELIVERDATE']),
            "FStockQty": str(model_data['FNBASEUNITQTY']),
            "FStockBaseQty": str(model_data['FNBASEUNITQTY']),
            "FOwnerTypeID": "BD_OwnerOrg",
            "FOwnerID": {
                "FNumber": "101"
            },
            "FOutLmtUnit": "SAL",
            'FSrcBillNo': model_data['FTRADENO'],
            "FCheckDelivery": False,
            "FLockStockFlag": False,
            "FEntity_Link": [{
                "FEntity_Link_FRuleId ": "SaleOrder-DeliveryNotice",
                "FEntity_Link_FSTableName ": "T_SAL_ORDERENTRY",
                "FEntity_Link_FSBillId ": result[0][2],
                "FEntity_Link_FSId ": result[0][3],
                "FEntity_Link_FBaseUnitQtyOld ": str(model_data['FNBASEUNITQTY']),
                "FEntity_Link_FBaseUnitQty ": str(model_data['FNBASEUNITQTY']),
                "FEntity_Link_FStockBaseQtyOld ": str(model_data['FNBASEUNITQTY']),
                "FEntity_Link_FStockBaseQty ": str(model_data['FNBASEUNITQTY']),
            }]
        }

        return model

    else:

        return {}


def writeSRC(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = ne.viewPage(url, 1, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "FDELIVERDATE")

    for i in range(1, page + 1):
        df = ne.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "FDELIVERDATE")

        df = df.replace("Lab'IN Co.", "")

        df = df.fillna("")

        db.insert_sales_delivery(app3, df)

    pass
