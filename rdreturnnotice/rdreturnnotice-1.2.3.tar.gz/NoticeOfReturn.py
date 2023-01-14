from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
import pandas as pd
import json


def json_model(app2,model_data,api_sdk):

    materialSKU="7.1.000001" if str(model_data['FPrdNumber'])=='1' else str(model_data['FPrdNumber'])
    materialId=code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU,"104","FMATERIALID")

    if materialSKU=="7.1.000001":

        materialId="466653"

    result=saleOrder_view(api_sdk,str(model_data['FDELIVERYNO']),materialId)

    if result!=[] and materialId!="":

        model={
                "FRowType": "Standard" if model_data['FPrdNumber']!='1' else "Service",
                "FMaterialId": {
                    "FNumber": "7.1.000001" if model_data['FPrdNumber']=='1' else str(code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPrdNumber']))
                },
                # "FUnitID": {
                #     "FNumber": "01"
                # },
                "FQty": str(model_data['FRETURNQTY']),
                "FPRODUCEDATE": str(model_data['FPRODUCEDATE']) if iskfperiod(app2,model_data['FPrdNumber'])=='1' else "",
                "FExpiryDate": str(model_data['FEFFECTIVEDATE']) if iskfperiod(app2,model_data['FPrdNumber'])=='1' else "",
                "FTaxPrice": str(model_data['FRETSALEPRICE']),
                "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
                "FLot": {
                    "FNumber": str(model_data['FLOT']) if isbatch(app2,model_data['FPrdNumber'])=='1' else ""
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
                    "FEntity_Link_FSBillId": result[0][2],
                    "FEntity_Link_FSId": result[0][3],
                    "FEntity_Link_FBaseUnitQtyOld ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FBaseUnitQty ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FStockBaseQtyOld ": str(model_data['FRETURNQTY']),
                    "FEntity_Link_FStockBaseQty ": str(model_data['FRETURNQTY']),
                }]
            }

        return model
    else:
        #
        # print(materialSKU)
        # print(model_data['FDELIVERYNO'])
        return {}

def isbatch(app2,FNumber):
    '''
    判断是否启用批号管理
    :param app2:
    :param FNumber:
    :return:
    '''

    sql=f"select FISBATCHMANAGE from rds_vw_fisbatch where F_SZSP_SKUNUMBER='{FNumber}'"

    res = app2.select(sql)

    if res == []:

        return ""

    else:

        return res[0]['FISBATCHMANAGE']


def iskfperiod(app2,FNumber):
    '''
    查看物料是否启用保质期
    :param app2:
    :param FNumber:
    :return:
    '''

    sql=f"select FISKFPERIOD from rds_vw_fiskfperiod where F_SZSP_SKUNUMBER='{FNumber}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FISKFPERIOD']



def associated(app2,api_sdk,option,data):

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        if check_deliveryExist(api_sdk,i[0]['FMRBBILLNO'])!=True:

            model={
                    "Model": {
                        "FID": 0,
                        "FBillTypeID": {
                            "FNUMBER": "THTZD01_SYS"
                        },
                        "FBillNo": str(i[0]['FMRBBILLNO']),
                        "FDate": str(i[0]['OPTRPTENTRYDATE']),
                        "FApproveDate": str(i[0]['OPTRPTENTRYDATE']),
                        "FSaleOrgId": {
                            "FNumber": "104"
                        },
                        "FRetcustId": {
                            "FNumber": code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FReturnReason": {
                            "FNumber": "QT"
                        },
                        # "FHeadLocId": {
                        #     "FNumber": "BIZ202103081651391"
                        # },
                        "FSalesGroupID": {
                            "FNumber": "SKYX01"
                        },
                        "FSalesManId": {
                            "FNumber": code_conversion_org(app2,"rds_vw_salesman","FNAME",i[0]['FSALER'],'104',"FNUMBER")
                        },
                        "FRetorgId": {
                            "FNumber": "104"
                        },
                        "FRetDeptId": {
                            "FNumber": "BM000040"
                        },
                        "FStockerGroupId": {
                            "FNumber": "SKCKZ01"
                        },
                        "FStockerId": {
                            "FNAME": "刘想良"
                        },
                        "FReceiveCusId": {
                            "FNumber": code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FSettleCusId": {
                            "FNumber": code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FPayCusId": {
                            "FNumber": code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FOwnerTypeIdHead": "BD_OwnerOrg",
                        "FManualClose": False,
                        "SubHeadEntity": {
                            "FSettleCurrId": {
                                "FNumber": "PRE001"
                            },
                            "FSettleOrgId": {
                                "FNumber": "104"
                            },
                            "FLocalCurrId": {
                                "FNumber": "PRE001"
                            },
                            "FExchangeTypeId": {
                                "FNumber": "HLTX01_SYS"
                            },
                            "FExchangeRate": 1.0
                        },
                        "FEntity": data_splicing(app2,api_sdk,i)
                    }
                }


            res=json.loads(api_sdk.Save("SAL_RETURNNOTICE",model))

            if res['Result']['ResponseStatus']['IsSuccess']:

                FNumber = res['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                submit_res=ERP_submit(api_sdk,FNumber)

                if submit_res:

                    audit_res=ERP_Audit(api_sdk,FNumber)

                    if audit_res:

                        changeStatus(app3,str(i[0]['FMRBBILLNO']),'1')
                        pass

                    else:
                        pass
                else:
                    pass
            else:

                changeStatus(app3,str(i[0]['FMRBBILLNO']),'2')
                print(res)
                print(str(i[0]['FMRBBILLNO']))


def ERP_submit(api_sdk,FNumber):

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }

    res=json.loads(api_sdk.Submit("SAL_RETURNNOTICE",model))

    return res['Result']['ResponseStatus']['IsSuccess']

def ERP_Audit(api_sdk,FNumber):
    '''
    将订单审核
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "InterationFlags": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": "",
        "IgnoreInterationFlag": "",
    }

    res = json.loads(api_sdk.Audit("SAL_RETURNNOTICE", model))

    return res['Result']['ResponseStatus']['IsSuccess']


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

def data_splicing(app2,api_sdk,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''

    list=[]

    for i in data:

        list.append(json_model(app2,i,api_sdk))

    return list


def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select FMRBBILLNO from RDS_ECS_ODS_sal_returnstock where FIsdo=0 and FIsFree!=1"

    res=app3.select(sql)

    return res

def saleOrder_view(api_sdk,value,materialID):
    '''
    销售出库单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "SAL_OUTSTOCK", "FieldKeys": "FDate,FBillNo,FId,FEntity_FENTRYID,FMaterialID", "FilterString": [{"Left":"(","FieldName":"FMaterialID","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res

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

        data=getClassfyData(app3,i)
        singleList.append(data)


    return singleList

def getClassfyData(app3,code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql=f"select * from RDS_ECS_ODS_sal_returnstock where FMRBBILLNO='{code}'"

    res=app3.select(sql)

    return res


def check_deliveryExist(api_sdk,FNumber):

    model={
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res=json.loads(api_sdk.View("SAL_RETURNNOTICE",model))

    return res['Result']['ResponseStatus']['IsSuccess']


def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.Fisdo={status} from RDS_ECS_ODS_sal_returnstock a where FMRBBILLNO='{fnumber}'"

    app3.update(sql)



if __name__ == '__main__':

    app2 = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')

    data = getCode(app3)

    res = classification_process(app3, data)

    # print(len(res))

    list = []
    # 23

    for i in range(0, 1):
        list.append(res[i])

    # 新账套

    option1 = {
        "acct_id": '62777efb5510ce',
        "user_name": '张志',
        "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
        # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        "app_sec": 'b105890b343b40ba908ed51453940935',
        "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    }
    api_sdk = K3CloudApiSdk()

    associated(app2,api_sdk,option1,list)



