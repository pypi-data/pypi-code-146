import SaleOrder.rdSaleOrder.operation as sro
import json


def json_model(app2,model_data):
    '''
    物料单元model
    :param model_data: 物料信息
    :return:
    '''
    if sro.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPRDNUMBER'])!="" or model_data['FPRDNUMBER']=='1':

        model={
                "FRowType": "Standard" if model_data['FPRDNUMBER']!='1' else "Service",
                "FMaterialId": {
                    "FNumber": "7.1.000001" if model_data['FPRDNUMBER']=='1' else str(sro.code_conversion(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPRDNUMBER']))
                },
                "FQty": str(model_data['FQTY']),
                "FPrice": str(model_data['FPRICE']),
                "FTaxPrice": str(model_data['FTAXPRICE']),
                "FIsFree": True if float(model_data['FIsfree'])== 1 else False,
                "FEntryTaxRate": float(model_data['FTAXRATE'])*100,
                "FExpPeriod": 1095,
                "FExpUnit": "D",
                "FDeliveryDate": str(model_data['FPurchaseDate']),
                "FStockOrgId": {
                    "FNumber": "104"
                },
                "FSettleOrgIds": {
                    "FNumber": "104"
                },
                "FSupplyOrgId": {
                    "FNumber": "104"
                },
                "FOwnerTypeId": "BD_OwnerOrg",
                "FOwnerId": {
                    "FNumber": "104"
                },
                "FEntryNote": str(model_data['FDESCRIPTION']),
                "FReserveType": "1",
                "FPriceBaseQty": str(model_data['FQTY']),
                "FStockQty": str(model_data['FQTY']),
                "FStockBaseQty": str(model_data['FQTY']),
                "FOUTLMTUNIT": "SAL",
                "FISMRP": False,
                "F_SZSP_FSPC1": False,
                "FAllAmountExceptDisCount": str(model_data['FALLAMOUNTFOR']),
                "FOrderEntryPlan": [
                    {
                        "FPlanQty": str(model_data['FQTY'])
                    }
                ]
            }

        return model
    else:
        return {}

def data_splicing(app2,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''
    list=[]

    for i in data:

        result=json_model(app2,i)

        if result=={}:

            list=[]

            break

        list.append(result)

    return list

def ERP_Save(api_sdk,data,option,app2,app3):

    '''
    调用ERP保存接口
    :param api_sdk: 调用ERP对象
    :param data:  要插入的数据
    :param option: ERP密钥
    :param app2: 数据库执行对象
    :return:
    '''

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        if check_order_exists(api_sdk,i[0]['FSALEORDERNO'])!=True:

                model = {
                    "Model": {
                        "FID": 0,
                        "FBillTypeID": {
                            "FNUMBER": "XSDD01_SYS"

                        },
                        "FBillNo": str(i[0]['FSALEORDERNO']),
                        "FDate": str(i[0]['FSALEDATE']),
                        "FSaleOrgId": {
                            "FNumber": "104"
                        },
                        "FCustId": {
                            "FNumber": "C003142"if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FReceiveId": {
                            "FNumber": "C003142"if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FSaleDeptId": {
                            "FNumber": sro.code_conversion(app2,"rds_vw_department","FNAME","销售部")
                        },
                        "FSaleGroupId": {
                            "FNumber": "SKYX01"
                        },
                        "FSalerId": {
                            "FNumber": sro.code_conversion_org(app2,"rds_vw_salesman","FNAME",i[0]['FSALER'],'104')
                        },
                        "FSettleId": {
                            "FNumber": "C003142"if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FChargeId": {
                            "FNumber": "C003142"if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                        },
                        "FISINIT": False,
                        "FIsMobile": False,
                        "FIsUseOEMBomPush": False,
                        "FIsUseDrpSalePOPush": False,
                        "F_SZSP_XSLX": {
                            "FNumber": "1" if i[0]['FSalesType']=='内销' else "2"
                        },
                        "F_SZSP_JJCD": {
                            "FNumber": "YB" if i[0]['FUrgency']=='一般' else "JJ"
                        },
                        "FSaleOrderFinance": {
                            "FSettleCurrId": {
                                "FNumber": "PRE001"
                            },
                            "FRecConditionId": {
                                "FNumber": "SKTJ05_SP" if i[0]['FCollectionTerms']=='月结30天' else "SKTJ01_SP"
                            },
                            "FIsPriceExcludeTax": True,
                            "FIsIncludedTax": True,
                            "FExchangeTypeId": {
                                "FNumber": "HLTX01_SYS"
                            },
                            "FOverOrgTransDirect": False
                        },
                        "FSaleOrderEntry": data_splicing(app2,i),
                        "FSaleOrderPlan": [
                            {
                                "FNeedRecAdvance": False,
                                "FRecAdvanceRate": 100.0,
                                "FIsOutStockByRecamount": False
                            }
                        ]
                    }
                }

                save_result=api_sdk.Save("SAL_SaleOrder", model)

                res=json.loads(save_result)

                if res['Result']['ResponseStatus']['IsSuccess']:

                    submit_result=ERP_Submit(api_sdk,i[0]['FSALEORDERNO'])

                    if submit_result:

                        sudit_result=ERP_Audit(api_sdk,i[0]['FSALEORDERNO'])

                        if sudit_result:

                            sro.changeStatus(app3,i[0]['FSALEORDERNO'],"1")

                else:
                    sro.changeStatus(app3, i[0]['FSALEORDERNO'], "2")
                    print(res)
                    print(i[0]['FSALEORDERNO'])

        else:
            sro.changeStatus(app3,i[0]['FSALEORDERNO'],"1")

def check_order_exists(api_sdk,FNumber):
    '''
    查看订单是否在ERP系统存在
    :param api: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

    res=json.loads(api_sdk.View("SAL_SaleOrder",model))

    return res['Result']['ResponseStatus']['IsSuccess']

def ERP_Submit(api_sdk,FNumber):
    '''
    将订单进行提交
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }

    res=json.loads(api_sdk.Submit("SAL_SaleOrder",model))

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
        "IgnoreInterationFlag": ""
    }

    res = json.loads(api_sdk.Audit("SAL_SaleOrder", model))

    return res['Result']['ResponseStatus']['IsSuccess']
