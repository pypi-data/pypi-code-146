import pandas as pd
from rdreturnpurchase import operation as db
from rdreturnpurchase import metadata as mt
from rdreturnpurchase import EcsInterface as pe

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

        if model_data['FGOODSID']=='1' or str(db.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FGOODSID'])):

            model = {
                    "FRowType": "Standard" if model_data['FGOODSID'] != '1' else "Service",
                    "FMATERIALID": {
                        "FNumber": "7.1.000001" if model_data['FGOODSID']=='1' else str(db.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FGOODSID']))
                    },
                    "FRMREALQTY": str(model_data['FRETQTY']),
                    "FREPLENISHQTY": str(model_data['FRETQTY']),
                    "FKEAPAMTQTY": str(model_data['FRETQTY']),
                    "FSTOCKID": {
                        "FNumber": "SK01" if model_data['FSTOCKID']=="苏州总仓" or model_data['FSTOCKID']=="" else "SK02"
                    },
                    "FStockStatusId": {
                        "FNumber": "KCZT01_SYS"
                    },
                    "FIsReceiveUpdateStock": False,
                    "FGiveAway": False,
                    "FPrice": str(model_data['FRETSALEPRICE']),
                    "FPriceBaseQty": str(model_data['FRETQTY']),
                    "FCarryQty": str(model_data['FRETQTY']),
                    "FCarryBaseQty": str(model_data['FRETQTY']),
                    "FBILLINGCLOSE": False,
                    "FOWNERTYPEID": "BD_OwnerOrg",
                    "FOWNERID": {
                        "FNumber": "104"
                    },
                    "FENTRYTAXRATE": float(model_data['FTAXRATE']) * 100,
                    "FLot": {
                        "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FGOODSID'])=='1' else ""
                    },
                    "FProduceDate": str(model_data['MANUFACTUREDATE']) if db.iskfperiod(app2,model_data['FGOODSID'])=='1' else "",
                    "FEXPIRYDATE": str(model_data['EFFECTDATE']) if db.iskfperiod(app2,model_data['FGOODSID'])=='1' else "",
                    "FIsStock": False,
                    "FPURMRBENTRY_Link": [{
                            "FPURMRBENTRY_Link_FRuleId": "PUR_MRAPP-PUR_MRB",
                            "FPURMRBENTRY_Link_FSTableName": "T_PUR_MRAPPENTRY",
                            "FPURMRBENTRY_Link_FSBillId": str(value[2]),
                            "FPURMRBENTRY_Link_FSId": str(value[3]),
                            "FPURMRBENTRY_Link_FCarryBaseQtyOld": str(model_data['FRETQTY']),
                            "FPURMRBENTRY_Link_FCarryBaseQty": str(model_data['FRETQTY']),
                            "FPURMRBENTRY_Link_FBASEUNITQTYOld": str(model_data['FRETQTY']),
                            "FPURMRBENTRY_Link_FBASEUNITQTY": str(model_data['FRETQTY']),
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

    page = pe.viewPage(url, 1, 1000, "ge", "le", "v_procurement_return", startDate, endDate, "FDATE")

    for i in range(1, page + 1):
        df = pe.ECS_post_info2(url, i, 1000, "ge", "le", "v_procurement_return", startDate, endDate, "FDATE")

        db.insert_procurement_return(app3, df)

    pass