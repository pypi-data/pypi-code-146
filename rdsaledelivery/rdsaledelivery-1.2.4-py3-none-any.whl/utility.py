import pandas as pd
from rdsaledelivery import operation as db
from rdsaledelivery import metadata as mt
from rdsaledelivery import EcsInterface as se

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
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''

    result=mt.delivery_view(api_sdk,FNumber)

    list=[]

    if result != [] and len(result)==len(data):

        index=0

        for i in data:

            list.append(json_model(app2,i,result[index]))

            index=index+1

        return list
    else:
        return []


def json_model(app2,model_data,value):

    try:

        if model_data['FPRDNUMBER'] == '1' or str(db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPRDNUMBER']))!="":

            model = {
                "FRowType": "Standard" if model_data['FPRDNUMBER'] != '1' else "Service",
                "FMaterialID": {
                    "FNumber": "7.1.000001" if model_data['FPRDNUMBER'] == '1' else str(db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPRDNUMBER']))
                },
                "FRealQty": str(model_data['FNBASEUNITQTY']),
                "FTaxPrice": str(model_data['FPRICE']),
                "FIsFree": True if model_data['FIsfree']==1 else False,
                "FOwnerTypeID": "BD_OwnerOrg",
                "FOwnerID": {
                    "FNumber": "104"
                },
                "FLot": {
                    "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FPRDNUMBER'])=='1' else ""
                },
                "FProduceDate":  str(model_data['FPRODUCEDATE']) if db.iskfperiod(app2,model_data['FPRDNUMBER'])=='1' else "",
                "FExpiryDate": str(model_data['FEFFECTIVEDATE']) if db.iskfperiod(app2,model_data['FPRDNUMBER'])=='1' else "",
                "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
                "FStockID": {
                    "FNumber": "SK01"
                },
                "FStockStatusID": {
                    "FNumber": "KCZT01_SYS"
                },
                "FSALUNITQTY": str(model_data['FNBASEUNITQTY']),
                "FSALBASEQTY": str(model_data['FNBASEUNITQTY']),
                "FPRICEBASEQTY": str(model_data['FNBASEUNITQTY']),
                "FOUTCONTROL": False,
                "FIsOverLegalOrg": False,
                "FARNOTJOINQTY": str(model_data['FNBASEUNITQTY']),
                "FCheckDelivery": False,
                "FSettleBySon": False,
                "FMaterialID_Sal": {
                    "FNUMBER": "7.1.000001" if model_data['FPRDNUMBER'] == '1' else str(db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPRDNUMBER']))
                },
                "FEntity_Link": [{
                    "FEntity_Link_FRuleId ": "DeliveryNotice-OutStock",
                    "FEntity_Link_FSTableName ": "T_SAL_DELIVERYNOTICEENTRY",
                    "FEntity_Link_FSBillId ": str(value[2]),
                    "FEntity_Link_FSId ": str(value[3]),
                    "FEntity_Link_FBaseUnitQtyOld ": str(model_data['FNBASEUNITQTY']),
                    "FEntity_Link_FBaseUnitQty ": str(model_data['FNBASEUNITQTY']),
                    "FEntity_Link_FStockBaseQtyOld ": str(model_data['FNBASEUNITQTY']),
                    "FEntity_Link_FStockBaseQty ": str(model_data['FNBASEUNITQTY']),
                }]
            }

            return model
        else:
            {}

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

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "FDELIVERDATE")

    for i in range(1, page + 1):

        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_delivery", startDate, endDate, "FDELIVERDATE")

        df = df.replace("Lab'IN Co.", "")

        df = df.fillna("")

        db.insert_sales_delivery(app2,app3, df)


