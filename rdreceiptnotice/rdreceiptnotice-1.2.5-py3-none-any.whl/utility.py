from rdreceiptnotice import operation as db
from rdreceiptnotice import metadata as mt
from rdreceiptnotice import EcsInterface as re


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

def code_conversion(app2,tableName,param,param2):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select FNumber from {tableName} where {param}='{param2}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FNumber']

def code_conversion_org(app2,tableName,param,param2,param3,param4):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select {param4} from {tableName} where {param}='{param2}' and FOrgNumber='{param3}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0][param4]

def data_splicing(app2, api_sdk, data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给
    :param data:
    :return:
    '''

    list = []

    for i in data:

        result=json_model(app2, i, api_sdk)

        if result:

            list.append(result)
        else:
            return []

    return list

def json_model(app2,model_data,api_sdk):

    try:

        materialSKU = "7.1.000001" if str(model_data['FGOODSID']) == '1' else str(model_data['FGOODSID'])
        materialId = code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU, "104", "FMATERIALID")

        if materialSKU == "7.1.000001":
            materialId = "466653"

        result = mt.Order_view(api_sdk, str(model_data['FBILLNO']), materialId)

        if result!=[] and materialId!="":

                model={
                        "FMaterialId": {
                            "FNumber": "7.1.000001" if model_data['FGOODSID']=="1" else code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",str(model_data['FGOODSID']),"104","FNUMBER")
                        },
                        # "FMaterialDesc": str(model_data['FPRDNAME']),
                        # "FUnitId": {
                        #     "FNumber": "01"
                        # },
                        "FActReceiveQty": str(model_data['FINSTOCKQTY']),
                        "FPreDeliveryDate": str(model_data['FArrivalDate']),
                        "FSUPDELQTY": str(model_data['FINSTOCKQTY']),
                        # "FPriceUnitId": {
                        #     "FNumber": "01"
                        # },
                        "FStockID": {
                            "FNumber": "SK01" if model_data['FSTOCKID']=='苏州总仓' else "SK02"
                        },
                        "FStockStatusId": {
                            "FNumber": "KCZT02_SYS"
                        },
                        "FLot": {
                            "FNumber": str(model_data['FLOT'])
                        },
                        # "FProduceDate": "2022-10-31 00:00:00",
                        "FGiveAway": True if float(model_data['FIsFree'])== 1 else False,
                        "FCtrlStockInPercent": True,
                        "FCheckInComing": False,
                        "FIsReceiveUpdateStock": False,
                        # "FExpiryDate": "2025-10-30 00:00:00",
                        "FStockInMaxQty": str(model_data['FINSTOCKQTY']),
                        "FStockInMinQty": str(model_data['FINSTOCKQTY']),
                        "FEntryTaxRate": float(model_data['FTAXRATE'])*100,
                        "FTaxPrice": str(model_data['FPURCHASEPRICE']),
                        "FPriceBaseQty": str(model_data['FINSTOCKQTY']),
                        # "FStockUnitID": {
                        #     "FNumber": "01"
                        # },
                        "FStockQty": str(model_data['FINSTOCKQTY']),
                        "FStockBaseQty": str(model_data['FINSTOCKQTY']),
                        "FActlandQty": str(model_data['FINSTOCKQTY']),
                        "F_SZSP_GYSSHD": str(model_data['FLOT']),
                        "F_SZSP_GYSPH": str(model_data['FLOT']),
                        "FDetailEntity_Link": [
                          {
                            "FDetailEntity_Link_FRuleId": "PUR_PurchaseOrder-PUR_ReceiveBill",
                            "FDetailEntity_Link_FSTableName": "t_PUR_POOrderEntry",
                            "FDetailEntity_Link_FSBillId": result[0][2],
                            "FDetailEntity_Link_FSId": result[0][3],
                            "FDetailEntity_Link_FBaseUnitQtyOld": str(model_data['FINSTOCKQTY']),
                            "FDetailEntity_Link_FBaseUnitQty": str(model_data['FINSTOCKQTY']),
                            "FDetailEntity_Link_FStockBaseQtyOld": str(model_data['FINSTOCKQTY']),
                            "FDetailEntity_Link_FStockBaseQty": str(model_data['FINSTOCKQTY']),
                          }
                        ]
                    }

                return model
        else:
                return {}

    except Exception as e:

        return {}

def writeSRC(startDate, endDate,app2, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = re.viewPage(url, 1, 1000, "ge", "le", "v_procurement_storage", startDate, endDate, "UPDATETIME")

    for i in range(1, page + 1):
        df = re.ECS_post_info2(url, i, 1000, "ge", "le", "v_procurement_storage", startDate, endDate, "UPDATETIME")

        db.insert_procurement_storage(app2,app3, df)

    pass



