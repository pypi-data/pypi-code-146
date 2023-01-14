import pandas as pd
import json
from rdnoticeshipment import operation as db
from rdnoticeshipment import EcsInterface as ne

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
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FEntity
    :param data:
    :return:
    '''

    list=[]

    for i in data:

        result=json_model(app2, i, api_sdk)

        if result:

            list.append(result)

        else:
            return []

    return list


def saleOrder_view(api_sdk,value,materialID):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "SAL_SaleOrder", "FieldKeys": "FDate,FBillNo,FId,FSaleOrderEntry_FEntryID,FMaterialId", "FilterString": [{"Left":"(","FieldName":"FMaterialId","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res

def json_model(app2,model_data,api_sdk):

    try:

        materialSKU="7.1.000001" if str(model_data['FPRDNUMBER'])=='1' else str(model_data['FPRDNUMBER'])
        materialId=db.code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU,"104","FMATERIALID")

        if materialSKU=="7.1.000001":

            materialId="466653"

        result=saleOrder_view(api_sdk,str(model_data['FTRADENO']),materialId)

        # stockMaterial="" if str(model_data['FPRDNUMBER'])=='1' else str(model_data['FPRDNUMBER'])

        # number=True
        #
        # if stockMaterial!="":
        #
        #     number = db.viewInventory(app2, str(model_data['FLOT']),stockMaterial)>=int(model_data['FNBASEUNITQTY'])

        if result!=[] and materialId!="":

            model={
                    "FRowType": "Standard" if model_data['FPRDNUMBER']!='1' else "Service",
                    "FMaterialID": {
                        "FNumber": "7.1.000001" if model_data['FPRDNUMBER']=='1' else str(db.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPRDNUMBER']))
                    },
                    "FQty": str(model_data['FNBASEUNITQTY']),
                    "FDeliveryDate": str(model_data['FDATE']),
                    "FStockID": {
                        "FNumber": "SK01"
                    },
                    "FTaxPrice": str(model_data['FPRICE']),
                    "FIsFree": True if float(model_data['FIsfree']) == 1 else False,
                    "FAllAmount": str(model_data['DELIVERYAMOUNT']),
                    "FEntryTaxRate":float(model_data['FTAXRATE'])*100,
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
                        "FNumber": "104"
                    },
                    "FOutLmtUnit": "SAL",
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

    except Exception as e:

        return ""



def writeSRC(startDate, endDate, app2,app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = ne.viewPage(url, 1, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "UPDATETIME")

    for i in range(1, page + 1):

        df = ne.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "UPDATETIME")

        df = df.replace("Lab'IN Co.", "")

        df = df.fillna("")

        db.insert_sales_delivery(app2,app3, df)

    pass