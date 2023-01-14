import json
from rdpurchasestorage import utility as pru
from rdpurchasestorage import operation as pro

def associated(app2,api_sdk,option,data,app3):


    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            purchase = ""

            if ERP_view(api_sdk, i[0]['FBILLNO'])['Result']['ResponseStatus']['IsSuccess']:
                purchase = ERP_view(api_sdk, i[0]['FBILLNO'])['Result']['Result']['PurchaserId']['Number']

            if check_order_exists(api_sdk,str(i[0]['FGODOWNNO']))!=True:

                    model={
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "RKD01_SYS"
                            },
                            "FBillNo": str(i[0]['FGODOWNNO']),
                            "FDate": str(i[0]['FBUSINESSDATE']),
                            "FStockOrgId": {
                                "FNumber": "104"
                            },
                            "FStockDeptId": {
                                "FNumber": "BM000040"
                            },
                            "FStockerGroupId": {
                                "FNumber": "SKCKZ01"
                            },
                            "FStockerId": {
                                "FNumber": "BSP00040"
                            },
                            "FDemandOrgId": {
                                "FNumber": "104"
                            },
                            "FCorrespondOrgId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FPurchaseOrgId": {
                                "FNumber": "104"
                            },
                            "FPurchaseDeptId": {
                                "FNumber": "BM000040"
                            },
                            "FPurchaserGroupId": {
                                "FNumber": "SKYX02"
                            },
                            "FPurchaserId": {
                                "FNumber": purchase
                            },
                            "FSupplierId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FSupplyId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FSettleId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FChargeId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FOwnerTypeIdHead": "BD_OwnerOrg",
                            "FOwnerIdHead": {
                                "FNumber": "104"
                            },
                            "FSplitBillType": "A",
                            "F_SZSP_Assistant": {
                                "FNumber": "LX07"
                            },
                            "FInStockFin": {
                                "FSettleOrgId": {
                                    "FNumber": "104"
                                },
                                "FSettleTypeId": {
                                    "FNumber": "JSFS04_SYS"
                                },
                                "FSettleCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FIsIncludedTax": True,
                                "FPriceTimePoint": "1",
                                "FLocalCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FExchangeTypeId": {
                                    "FNumber": "HLTX01_SYS"
                                },
                                "FExchangeRate": 1.0,
                                "FISPRICEEXCLUDETAX": True
                            },
                            "FInStockEntry": pru.data_splicing(app2,api_sdk,i,i[0]['FGODOWNNO'])
                        }
                    }

                    save_result=json.loads(api_sdk.Save("STK_InStock",model))

                    if save_result['Result']['ResponseStatus']['IsSuccess']:

                        submit_result = ERP_submit(api_sdk, str(i[0]['FGODOWNNO']))

                        if submit_result:

                            audit_result = ERP_Audit(api_sdk, str(i[0]['FGODOWNNO']))

                            if audit_result:

                                pro.insertLog(app3, "采购入库单", str(i[0]['FGODOWNNO']), "数据同步成功", "1")

                                pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"1")

                                sucess_num=sucess_num+1

                            else:
                                pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"2")
                        else:
                            pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"2")
                    else:

                        pro.insertLog(app3, "采购入库单",str(i[0]['FGODOWNNO']), save_result['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                        pro.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")

                        erro_num=erro_num+1

                        erro_list.append(save_result)

            else:
                pro.changeStatus(app3, str(i[0]['FGODOWNNO']), "1")

        except Exception as e:

            pro.insertLog(app3, "采购入库单",str(i[0]['FGODOWNNO']),"数据异常","2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }
    return dict



def ERP_submit(api_sdk,FNumber):

    try:

        model={
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": ""
        }

        res=json.loads(api_sdk.Submit("STK_InStock",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False

def ERP_Audit(api_sdk,FNumber):
    '''
    将订单审核
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    try:

        model={
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "InterationFlags": "",
            "NetworkCtrl": "",
            "IsVerifyProcInst": "",
            "IgnoreInterationFlag": ""
        }

        res = json.loads(api_sdk.Audit("STK_InStock", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False

def Order_view(api_sdk,value):
    '''
    收料通知单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "PUR_ReceiveBill", "FieldKeys": "FDate,FBillNo,FId,FDetailEntity_FEntryID", "FilterString": [{"Left":"(","FieldName":"FBillNo","Compare":">=","Value":value,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"<=","Value":value,"Right":")","Logic":""}], "TopRowCount": 0}))

    return res

def ERP_view(api_sdk,FNumber):


    model={
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res=json.loads(api_sdk.View("PUR_PurchaseOrder",model))

    return res

def check_order_exists(api_sdk,FNumber):
    '''
    查看订单是否在ERP系统存在
    :param api: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    try:

        model={
                "CreateOrgId": 0,
                "Number": FNumber,
                "Id": "",
                "IsSortBySeq": "false"
            }

        res=json.loads(api_sdk.View("STK_InStock",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True