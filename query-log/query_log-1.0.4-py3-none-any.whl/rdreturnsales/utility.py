import pandas as pd
from rdreturnsales import operation as db
from rdreturnsales import metadata as mt
from rdreturnsales import EcsInterface as se
def classification_process(app3,data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    df=pd.DataFrame(data)

    df.drop_duplicates("FMRBBILLNO",keep="first",inplace=True)

    codeList=df['FMRBBILLNO'].tolist()

    res=fuz(app3,codeList)

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

    if model_data['FPrdNumber'] == '1' or db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPrdNumber']):

        model = {
                "FRowType": "Standard" if model_data['FPrdNumber'] != '1' else "Service",
                "FMaterialId": {
                    "FNumber": "7.1.000001" if model_data['FPrdNumber'] == '1' else str(db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPrdNumber']))
                },
                # "FUnitID": {
                #     "FNumber": "01"
                # },
                "FRealQty": str(model_data['FRETURNQTY']),
                "FTaxPrice": str(model_data['FRETSALEPRICE']),
                "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
                "FIsFree": True if float(model_data['FIsFree'])== 1 else False,
                "FReturnType": {
                    "FNumber": "THLX01_SYS"
                },
                "FOwnerTypeId": "BD_OwnerOrg",
                "FOwnerId": {
                    "FNumber": "104"
                },
                "FStockId": {
                    "FNumber": "SK01"
                },
                "FStockstatusId": {
                    "FNumber": "KCZT01_SYS"
                },
                "FLot": {
                    "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FPrdNumber'])=='1' else ""
                },
                "FDeliveryDate": str(model_data['FReturnTime']),
                # "FSalUnitID": {
                #     "FNumber": "01"
                # },
                "FSalUnitQty": str(model_data['FRETURNQTY']),
                "FSalBaseQty": str(model_data['FRETURNQTY']),
                "FPriceBaseQty": str(model_data['FRETURNQTY']),
                "FIsOverLegalOrg": False,
                "FARNOTJOINQTY": str(model_data['FRETURNQTY']),
                "FIsReturnCheck": False,
                "F_SZSP_ReleaseFlag": False,
                "FSettleBySon": False,
                "FMaterialID_Sal": {
                    "FNUMBER": "7.1.000001" if model_data['FPrdNumber'] == '1' else str(db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPrdNumber']))
                },
                "FEntity_Link": [{
                    "FEntity_Link_FRuleId ": "SalReturnNotice-SalReturnStock",
                    "FEntity_Link_FSTableName ": "T_SAL_RETURNNOTICEENTRY",
                    "FEntity_Link_FSBillId ": str(value[2]),
                    "FEntity_Link_FSId ": str(value[3]),
                    "FEntity_Link_FBaseUnitQtyOld ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FBaseUnitQty ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FStockBaseQtyOld ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FStockBaseQty ": str(model_data['FRETURNQTY']),
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

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_return", startDate, endDate, "OPTRPTENTRYDATE")

    for i in range(1, page + 1):
        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_return", startDate, endDate, "OPTRPTENTRYDATE")

        db.insert_sales_return(app3, df)

    pass