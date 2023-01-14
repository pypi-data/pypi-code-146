import json
from rdsaledelivery import operation as sro
from rdsaledelivery import utility as sru

def associated(app2,api_sdk,option,data,app3):

    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            if check_outstock_exists(api_sdk,i[0]['FDELIVERYNO'])!=True:

                    model = {
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "XSCKD01_SYS"
                            },
                            "FBillNo": str(i[0]['FDELIVERYNO']),
                            "FDate": str(i[0]['FDELIVERDATE']),
                            "FSaleOrgId": {
                                "FNumber": "104"
                            },
                            "FCustomerID": {
                                "FNumber": "C003142"if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FSaleDeptID": {
                                "FNumber": "BM000036"
                            },
                            "FSalesManID": {
                                "FNumber": sro.code_conversion_org(app2,"rds_vw_salesman","FNAME",i[0]['FSALER'],'104',"FNUMBER")
                            },
                            "FReceiverID": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FSalesGroupID": {
                                "FNumber": "SKYX01"
                            },
                            "FStockOrgId": {
                                "FNumber": "104"
                            },
                            "FDeliveryDeptID": {
                                "FNumber": "BM000040"
                            },
                            "FStockerGroupID": {
                                "FNumber": "SKCKZ01"
                            },
                            "FStockerID": {
                                "FNumber": "BSP00040"
                            },
                            "FSettleID": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FPayerID": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME']=="苏州亚通生物医疗科技有限公司" else sro.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FOwnerTypeIdHead": "BD_OwnerOrg",
                            "FIsTotalServiceOrCost": False,
                            "F_SZSP_XSLX": {
                                "FNumber": "1"
                            },
                            "SubHeadEntity": {
                                "FSettleCurrID": {
                                    "FNumber": "PRE001" if i[0]['FCurrencyName']=="" else sro.code_conversion(app2,"rds_vw_currency","FNAME",i[0]['FCurrencyName'])
                                },
                                "FSettleOrgID": {
                                    "FNumber": "104"
                                },
                                "FIsIncludedTax": True,
                                "FLocalCurrID": {
                                    "FNumber": "PRE001"
                                },
                                "FExchangeTypeID": {
                                    "FNumber": "HLTX01_SYS"
                                },
                                "FExchangeRate": 1.0,
                                "FIsPriceExcludeTax": True
                            },
                            "FEntity": sru.data_splicing(app2, api_sdk,i,str(i[0]['FDELIVERYNO']))
                        }
                    }

                    res = json.loads(api_sdk.Save("SAL_OUTSTOCK", model))

                    if res['Result']['ResponseStatus']['IsSuccess']:

                        submit_res = ERP_submit(api_sdk, str(i[0]['FDELIVERYNO']))

                        if submit_res:

                            audit_res = ERP_Audit(api_sdk, str(i[0]['FDELIVERYNO']))

                            if audit_res:

                                sro.insertLog(app3, "销售出库单", str(i[0]['FDELIVERYNO']), "数据同步成功", "1")

                                sro.changeStatus(app3,str(i[0]['FDELIVERYNO']),"1")

                                sucess_num=sucess_num+1

                            else:
                                sro.changeStatus(app3,str(i[0]['FDELIVERYNO']),"2")

                        else:
                            sro.changeStatus(app3,str(i[0]['FDELIVERYNO']),"2")

                    else:

                        sro.insertLog(app3, "销售出库单", str(i[0]['FDELIVERYNO']),res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                        sro.changeStatus(app3,str(i[0]['FDELIVERYNO']),"2")

                        erro_num=erro_num+1

                        erro_list.append(res)

        except Exception as e:

            sro.insertLog(app3, "销售出库单", str(i[0]['FDELIVERYNO']),"数据异常","2")

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

        res=json.loads(api_sdk.Submit("SAL_OUTSTOCK",model))

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

        res = json.loads(api_sdk.Audit("SAL_OUTSTOCK", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False



def check_deliveryExist(api_sdk, FNumber):

    try:

        model = {
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res = json.loads(api_sdk.View("SAL_DELIVERYNOTICE", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True

def delivery_view(api_sdk,value):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "SAL_DELIVERYNOTICE", "FieldKeys": "FDate,FBillNo,FId,FEntity_FEntryID", "FilterString": [{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res

def check_outstock_exists(api_sdk,FNumber):
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

        res=json.loads(api_sdk.View("SAL_OUTSTOCK",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True


