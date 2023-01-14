import json
from rdreturnsales import utility as ut
from rdreturnsales import operation as db


def associated(app2,api_sdk,option,data,app3):

    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        if check_outstock_exists(api_sdk,i[0]['FMRBBILLNO'])!=True:

                model = {
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "XSTHD01_SYS"
                            },
                            "FBillNo": str(i[0]['FMRBBILLNO']),
                            "FDate": str(i[0]['OPTRPTENTRYDATE']),
                            "FSaleOrgId": {
                                "FNumber": "104"
                            },
                            "FRetcustId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FReturnReason": {
                                "FNumber": "QT"
                            },
                            "FSalesGroupID": {
                                "FNumber": "SKYX01"
                            },
                            "FSalesManId": {
                                "FNumber": db.code_conversion_org(app2, "rds_vw_salesman", "FNAME", i[0]['FSALER'],
                                                               '104', "FNUMBER")
                            },
                            # "FHeadLocId": {
                            #     "FNumber": "BIZ202103081651391"
                            # },
                            "FTransferBizType": {
                                "FNumber": "OverOrgSal"
                            },
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
                            "FReceiveCustId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            # "FReceiveAddress": "江苏生物镇江市京口区丁卯街道经十五路99号科技园江苏金斯瑞生物科技有限公司",
                            "FSettleCustId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FPayCustId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FOwnerTypeIdHead": "BD_OwnerOrg",
                            "FIsTotalServiceOrCost": False,
                            # "FLinkPhone": "13770535847",
                            "SubHeadEntity": {
                                "FSettleCurrId": {
                                    "FNumber": "PRE001" if i[0]['FCurrencyName']=="" else db.code_conversion(app2,"rds_vw_currency","FNAME",i[0]['FCurrencyName'])
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
                            "FEntity": ut.data_splicing(app2,api_sdk,i,i[0]['FMRBBILLNO'])
                        }
                    }
                res = json.loads(api_sdk.Save("SAL_RETURNSTOCK", model))

                if res['Result']['ResponseStatus']['IsSuccess']:

                    submit_res = ERP_submit(api_sdk, str(i[0]['FMRBBILLNO']))

                    if submit_res:

                        audit_res = ERP_Audit(api_sdk, str(i[0]['FMRBBILLNO']))

                        if audit_res:

                            db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"1")

                            sucess_num=sucess_num+1

                        else:
                            db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                    else:
                        db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                else:
                    db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                    erro_num=erro_num+1

                    erro_list.append(res)
        else:
            db.changeStatus(app3, str(i[0]['FMRBBILLNO']), "1")


    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict


def check_outstock_exists(api_sdk,FNumber):
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

    res=json.loads(api_sdk.View("SAL_RETURNSTOCK",model))

    return res['Result']['ResponseStatus']['IsSuccess']

def ERP_submit(api_sdk,FNumber):

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }

    res=json.loads(api_sdk.Submit("SAL_RETURNSTOCK",model))

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

    res = json.loads(api_sdk.Audit("SAL_RETURNSTOCK", model))

    return res['Result']['ResponseStatus']['IsSuccess']

def delivery_view(api_sdk,value):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "SAL_RETURNNOTICE", "FieldKeys": "FDate,FBillNo,FId,FEntity_FENTRYID", "FilterString": [{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res
