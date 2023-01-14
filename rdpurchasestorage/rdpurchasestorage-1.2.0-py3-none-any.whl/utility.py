import pandas as pd
from rdpurchasestorage import operation as db
from rdpurchasestorage import metadata as mt
from rdpurchasestorage import EcsInterface as pe

def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select distinct FGODOWNNO from RDS_ECS_ODS_pur_storageacct where FIsdo=3 and FIsFree!=1"

    res=app3.select(sql)

    return res

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

def data_splicing(app2,api_sdk,data,FNumber):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给
    :param data:
    :return:
    '''

    result = mt.Order_view(api_sdk, FNumber)

    list = []

    if result != [] and len(result) == len(data):

        index = 0

        for i in data:

            list.append(json_model(app2, i, result[index]))

            index = index + 1

        return list
    else:
        return []

def json_model(app2,model_data,value):

    try:

        if model_data['FGOODSID']=="1" or db.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",str(model_data['FGOODSID']),"104","FNUMBER")!="":

            model={
                    "FRowType": "Service" if model_data['FGOODSID']=="1" else "Standard",
                    "FMaterialId": {
                        "FNumber": "7.1.000001" if model_data['FGOODSID']=="1" else db.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",str(model_data['FGOODSID']),"104","FNUMBER")
                    },
                    # "FMaterialDesc": str(model_data['FPRDNAME']),
                    # "FUnitID": {
                    #     "FNumber": "01"
                    # },
                    "FRealQty": str(model_data['FINSTOCKQTY']),
                    # "FPriceUnitID": {
                    #     "FNumber": "01"
                    # },
                    # str(model_data['FLOT']) if db.isbatch(app2,model_data['FPRDNUMBER'])=='1' else ""
                    "FLot": {
                        "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FGOODSID'])=='1' else ""
                    },
                    "FStockId": {
                        "FNumber": "SK01"
                    },
                    "FStockStatusId": {
                        "FNumber": "KCZT01_SYS"
                    },
                    "FGiveAway": True if float(model_data['FIsFree'])== 1 else False,
                    "FProduceDate": str(model_data['FPRODUCEDATE']) if db.iskfperiod(app2,model_data['FGOODSID'])=='1' else "",
                    "FNote": str(model_data['FDESCRIPTION']),
                    # "FProduceDate": "2022-10-31 00:00:00",
                    "FOWNERTYPEID": "BD_OwnerOrg",
                    "FCheckInComing": False,
                    "FIsReceiveUpdateStock": False,
                    "FPriceBaseQty": str(model_data['FINSTOCKQTY']),
                    # "FRemainInStockUnitId": {
                    #     "FNumber": "01"
                    # },
                    "FBILLINGCLOSE": False,
                    "FRemainInStockQty": str(model_data['FINSTOCKQTY']),
                    "FAPNotJoinQty": str(model_data['FINSTOCKQTY']),
                    "FRemainInStockBaseQty": str(model_data['FINSTOCKQTY']),
                    "FTaxPrice": str(model_data['FPURCHASEPRICE']),
                    "FEntryTaxRate": float(model_data['FTAXRATE'])*100,
                    "FExpiryDate": str(model_data['FEFFECTIVEDATE']) if db.iskfperiod(app2,model_data['FGOODSID'])=='1' else "",
                    "FOWNERID": {
                        "FNumber": "104"
                    },
                    "F_SZSP_GYSSHD":  str(model_data['FLOT']),
                    "FInStockEntry_Link": [{
                        "FInStockEntry_Link_FRuleId": "PUR_ReceiveBill-STK_InStock",
                        "FInStockEntry_Link_FSTableName": "T_PUR_ReceiveEntry",
                        "FInStockEntry_Link_FSBillId": value[2],
                        "FInStockEntry_Link_FSId": value[3],
                        "FInStockEntry_Link_FBaseUnitQtyOld": str(model_data['FINSTOCKQTY']),
                        "FInStockEntry_Link_FBaseUnitQty": str(model_data['FINSTOCKQTY']),
                        "FInStockEntry_Link_FRemainInStockBaseQtyOld": str(model_data['FINSTOCKQTY']),
                        "FInStockEntry_Link_FRemainInStockBaseQty": str(model_data['FINSTOCKQTY']),
                    }]
                }

            return model

        else:

            return {}

    except Exception as e:

        return {}

def writeSRC(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = pe.viewPage(url, 1, 1000, "ge", "le", "v_procurement_storage", startDate, endDate, "FBUSINESSDATE")

    for i in range(1, page + 1):
        df = pe.ECS_post_info2(url, i, 1000, "ge", "le", "v_procurement_storage", startDate, endDate, "FBUSINESSDATE")

        db.insert_procurement_storage(app3, df)

    pass