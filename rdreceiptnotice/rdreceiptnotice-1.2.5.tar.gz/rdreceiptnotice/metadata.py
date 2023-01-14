import json
from rdreceiptnotice import operation as pro
from rdreceiptnotice import utility as pru

def associated(app2,api_sdk,option,data,app3):
    '''
    将数据保存到ERP
    :param app2:
    :param api_sdk:
    :param option:
    :param data:
    :return:
    '''

    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            purchase = ""

            if ERP_view(api_sdk, i[0]['FBILLNO'])['Result']['ResponseStatus']['IsSuccess']:

                purchase=ERP_view(api_sdk, i[0]['FBILLNO'])['Result']['Result']['PurchaserId']['Number']

            if check_order_exists(api_sdk,i[0]['FGODOWNNO'])!=True:

                model={
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "SLD01_SYS"
                            },
                            "FBusinessType": "CG",
                            "FBillNo": str(i[0]['FGODOWNNO']),
                            "FDate": str(i[0]['FBUSINESSDATE']),
                            "FStockOrgId": {
                                "FNumber": "104"
                            },
                            "FReceiveDeptId": {
                                "FNumber": "BM000040"
                            },
                            "FStockGroupId": {
                                "FNumber": "SKCKZ01"
                            },
                            "FReceiverId": {
                                "FNumber": "BSP00040"
                            },
                            "FDemandOrgId": {
                                "FNumber": "104"
                            },
                            "FPurOrgId": {
                                "FNumber": "104"
                            },
                            "FPurGroupId": {
                                "FNumber": "SKYX02"
                            },
                            "FPurchaserId": {
                                "FNumber": purchase
                            },
                            "FSupplierId": {
                                "FNumber": pru.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FSupplyId": {
                                "FNumber": pru.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FSettleId": {
                                "FNumber": pru.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FChargeId": {
                                "FNumber": pru.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FOwnerTypeIdHead": "BD_Supplier",
                            "FOwnerIdHead": {
                                "FNumber": pru.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FIsInsideBill": False,
                            "FIsMobile": False,
                            "FIsChangeQty": False,
                            "FACCTYPE": "Q",
                            "F_SZSP_CGLX": {
                                "FNumber": "LX07"
                            },
                            "FinanceEntity": {
                                "FSettleOrgId": {
                                    "FNumber": "104"
                                },
                                "FSettleCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FIsIncludedTax": True,
                                "FPricePoint": "1",
                                "FLocalCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FExchangeTypeId": {
                                    "FNumber": "HLTX01_SYS"
                                },
                                "FExchangeRate": 1.0,
                                "FISPRICEEXCLUDETAX": True
                            },
                            "FDetailEntity": pru.data_splicing(app2,api_sdk,i)
                        }
                    }

                save_result=json.loads(api_sdk.Save("PUR_ReceiveBill",model))

                if save_result['Result']['ResponseStatus']['IsSuccess']:

                    submit_result=ERP_submit(api_sdk,str(i[0]['FGODOWNNO']))

                    if submit_result:

                        audit_result=ERP_Audit(api_sdk,str(i[0]['FGODOWNNO']))

                        if audit_result:

                            pro.insertLog(app3, "收料通知单", str(i[0]['FGODOWNNO']), "数据同步成功", "1")

                            pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"3")

                            sucess_num=sucess_num+1

                        else:

                            pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"2")

                    else:

                        pro.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")
                else:

                    pro.insertLog(app3, "收料通知单", str(i[0]['FGODOWNNO']),save_result['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                    pro.changeStatus(app3,str(i[0]['FGODOWNNO']),"2")

                    erro_num=erro_num+1

                    erro_list.append(save_result)
            else:
                pro.changeStatus(app3, str(i[0]['FGODOWNNO']), "3")

        except Exception as e:

            pro.insertLog(app3, "收料通知单", str(i[0]['FGODOWNNO']),"数据异常","2")


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

        res=json.loads(api_sdk.Submit("PUR_ReceiveBill",model))

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

        res = json.loads(api_sdk.Audit("PUR_ReceiveBill", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False

def Order_view(api_sdk,value,materialID):
    '''
    采购订单单据查询
    :param value: 订单编码
    :return:
    '''

    # api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
    #                    option['app_sec'], option['server_url'])

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "PUR_PurchaseOrder", "FieldKeys": "FDate,FBillNo,FId,FPOOrderEntry_FEntryID,FMaterialId", "FilterString": [{"Left":"(","FieldName":"FMaterialId","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res


def ERP_view(api_sdk,FNumber):
    # api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
    #                    option['app_sec'], option['server_url'])

    model={
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res=json.loads(api_sdk.View("PUR_PurchaseOrder",model))

    # return res['Result']['Result']['PurchaserId']['Number']

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

        res=json.loads(api_sdk.View("PUR_ReceiveBill",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True

