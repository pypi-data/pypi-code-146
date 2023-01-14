import pandas as pd
from rdreturnrequest import operation as db
from rdreturnrequest import metadata as mt
from rdreturnrequest import EcsInterface as pe

def classification_process(app3,data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    res=fuz(app3,data)

    return res

def fuz(app3,codeList):
    '''
    通过编码分类，将分类好的数据装入列表
    :param app2:
    :param codeList:
    :return:
    '''

    singleList=[]

    for i in codeList:

        data=db.getClassfyData(app3,i)

        singleList.append(data)


    return singleList

def data_splicing(app2,api_sdk,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''

    list=[]

    for i in data:

        result=json_model(app2,i,api_sdk)

        if result:

            list.append(result)

        else:

            return []

    return list

def json_model(app2,model_data,api_sdk):

    try:

        materialSKU="7.1.000001" if str(model_data['FGOODSID'])=='1' else str(model_data['FGOODSID'])
        materialId=db.code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU,"104","FMATERIALID")

        if materialSKU=="7.1.000001":

            materialId="466653"

        result=mt.PurchaseOrder_view(api_sdk,str(model_data['FPURORDERNO']),materialId)

        if result!=[] and materialId!="":

            model={
                    "FMATERIALID": {
                        "FNumber": "7.1.000001" if model_data['FGOODSID']=='1' else str(db.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FGOODSID']))
                    },
                    # "FUNITID": {
                    #     "FNumber": "01"
                    # },
                    "FMRAPPQTY": str(model_data['FRETQTY']),
                    # "FPRICEUNITID_F": {
                    #     "FNumber": "01"
                    # },
                    "FREPLENISHQTY": str(model_data['FRETQTY']),
                    "FKEAPAMTQTY": str(model_data['FRETQTY']),
                    # "FRMREASON_M": {
                    #     "FNumber": "01"
                    # },
                    "FGiveAway": False,
                    "FLot": {
                        "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FGOODSID'])=='1' else ""
                    },
                    "FPRICECOEFFICIENT_F": 1.0,
                    "FPRICE_F": str(model_data['FRETSALEPRICE']),
                    "FTAXNETPRICE_F": str(model_data['FRETSALEPRICE']),
                    "FPriceBaseQty": str(model_data['FRETQTY']),
                    # "FPURUNITID": {
                    #     "FNumber": "01"
                    # },
                    "FPurQty": str(model_data['FRETQTY']),
                    "FPurBaseQty": str(model_data['FRETQTY']),
                    "FEntity_Link": [{
                        "FEntity_Link_FRuleId": "PUR_PurchaseOrder-PUR_MRAPP",
                        "FEntity_Link_FSTableName": "t_PUR_POOrderEntry",
                        "FEntity_Link_FSBillId": result[0][2],
                        "FEntity_Link_FSId": result[0][3],
                        "FEntity_Link_FBASEUNITQTYOld ": str(model_data['FRETQTY']),
                        "FEntity_Link_FBASEUNITQTY ": str(model_data['FRETQTY']),
                        "FEntity_Link_FPurBaseQtyOld ": str(model_data['FRETQTY']),
                        "FEntity_Link_FPurBaseQty ": str(model_data['FRETQTY']),
                    }]
                }
            return model
        else:
            return {}

    except Exception as e:

        return {}

def writeSRC(startDate, endDate, app2,app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = pe.viewPage(url, 1, 1000, "ge", "le", "v_procurement_return", startDate, endDate, "UPDATETIME")

    for i in range(1, page + 1):
        df = pe.ECS_post_info2(url, i, 1000, "ge", "le", "v_procurement_return", startDate, endDate, "UPDATETIME")

        db.insert_procurement_return(app2,app3, df)

    pass