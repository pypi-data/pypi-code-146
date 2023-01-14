from rdreturnnotice import operation as db
from rdreturnnotice import metadata as mt
from rdreturnnotice import EcsInterface as se

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

    index = 0

    for i in data:

        materialSKU = "" if str(i['FPrdNumber']) == '1' else str(i['FPrdNumber'])

        result = db.checkFlot(app2, str(i['FDELIVERYNO']), str(i['FLOT']),
                              str(i['FRETURNQTY']), str(materialSKU))

        res=json_model(app2,i,api_sdk,index, result, materialSKU)

        if res:

            list.append(res)
        else:
            return []

    return list


def json_model(app2,model_data,api_sdk,index, result, materialSKU):

    try:

        # materialSKU="7.1.000001" if str(model_data['FPrdNumber'])=='1' else str(model_data['FPrdNumber'])
        materialId=db.code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU,"104","FMATERIALID")

        if materialSKU=="7.1.000001":

            materialId="466653"

        # result=mt.saleOrder_view(api_sdk,str(model_data['FDELIVERYNO']),materialId)

        if result!=[] and materialId!="":

            model={
                    "FRowType": "Standard" if model_data['FPrdNumber']!='1' else "Service",
                    "FMaterialId": {
                        "FNumber": "7.1.000001" if model_data['FPrdNumber']=='1' else str(db.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPrdNumber']))
                    },
                    # "FUnitID": {
                    #     "FNumber": "01"
                    # },
                    "FQty": str(model_data['FRETURNQTY']),
                    "FPRODUCEDATE": str(model_data['FPRODUCEDATE']) if db.iskfperiod(app2,model_data['FPrdNumber'])=='1' else "",
                    "FExpiryDate": str(model_data['FEFFECTIVEDATE']) if db.iskfperiod(app2,model_data['FPrdNumber'])=='1' else "",
                    "FTaxPrice": str(model_data['FRETSALEPRICE']),
                    "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
                    "FLot": {
                        "FNumber": str(model_data['FLOT']) if db.isbatch(app2,model_data['FPrdNumber'])=='1' else ""
                    },
                    "FPriceBaseQty": str(model_data['FRETURNQTY']),
                    # "FASEUNITID": {
                    #     "FNumber": "01"
                    # },
                    "FDeliverydate": str(model_data['FReturnTime']),
                    "FStockId": {
                        "FNumber": "SK01"
                    },
                    "FRmType": {
                        "FNumber": "THLX01_SYS"
                    },
                    "FIsReturnCheck": True,
                    # "FStockUnitID": {
                    #     "FNumber": "01"
                    # },
                    "FStockQty": str(model_data['FRETURNQTY']),
                    "FStockBaseQty": str(model_data['FRETURNQTY']),
                    "FOwnerTypeID": "BD_OwnerOrg",
                    "FOwnerID": {
                        "FNumber": "104"
                    },
                    "FRefuseFlag": False,
                    "FEntity_Link": [{
                        "FEntity_Link_FRuleId":"OutStock-SalReturnNotice",
                        "FEntity_Link_FSTableName": "T_SAL_OUTSTOCKENTRY",
                        "FEntity_Link_FSBillId": result[index]['Fid'],
                        "FEntity_Link_FSId": result[index]['FENTRYID'],
                        "FEntity_Link_FBaseUnitQtyOld ": str(model_data['FRETURNQTY']),
                        "FEntity_Link_FBaseUnitQty ": str(model_data['FRETURNQTY']),
                        "FEntity_Link_FStockBaseQtyOld ": str(model_data['FRETURNQTY']),
                        "FEntity_Link_FStockBaseQty ": str(model_data['FRETURNQTY']),
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

    page = se.viewPage(url, 1, 1000, "ge", "le", "v_sales_return", startDate, endDate, "UPDATETIME")

    for i in range(1, page + 1):
        df = se.ECS_post_info2(url, i, 1000, "ge", "le", "v_sales_return", startDate, endDate, "UPDATETIME")

        df=df.fillna("")

        db.insert_sales_return(app2,app3, df)

    pass