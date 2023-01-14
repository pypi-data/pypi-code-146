from rdreturnnotice import operation as db
from rdreturnnotice import utility as ut
import json

def associated(app2,api_sdk,option,data,app3):


    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

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
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "F_SZSP_Remarks": "其他",
                            # "FHeadLocId": {
                            #     "FNumber": "BIZ202103081651391"
                            # },
                            "FSalesGroupID": {
                                "FNumber": "SKYX01"
                            },
                            "FSalesManId": {
                                "FNumber": db.code_conversion_org(app2,"rds_vw_salesman","FNAME",i[0]['FSALER'],'104',"FNUMBER")
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
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FSettleCusId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FPayCusId": {
                                "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                            },
                            "FOwnerTypeIdHead": "BD_OwnerOrg",
                            "FManualClose": False,
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
                            "FEntity": ut.data_splicing(app2,api_sdk,i)
                        }
                    }


                res=json.loads(api_sdk.Save("SAL_RETURNNOTICE",model))

                if res['Result']['ResponseStatus']['IsSuccess']:

                    FNumber = res['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                    submit_res=ERP_submit(api_sdk,FNumber)

                    if submit_res:

                        audit_res=ERP_Audit(api_sdk,FNumber)

                        if audit_res:

                            db.insertLog(app3, "退货通知单", i[0]['FMRBBILLNO'], "数据同步成功", "1")

                            db.changeStatus(app3,str(i[0]['FMRBBILLNO']),'3')

                            sucess_num=sucess_num+1
                            pass

                        else:
                            pass
                    else:
                        pass
                else:

                    db.insertLog(app3, "退货通知单", i[0]['FMRBBILLNO'],res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                    db.changeStatus(app3,str(i[0]['FMRBBILLNO']),'2')

                    erro_num=erro_num+1

                    erro_list.append(res)

        except Exception as e:

            db.insertLog(app3, "退货通知单", i[0]['FMRBBILLNO'],"数据异常","2")


    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }
    return dict


def check_deliveryExist(api_sdk,FNumber):

    try:

        model={
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res=json.loads(api_sdk.View("SAL_RETURNNOTICE",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True


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

        res=json.loads(api_sdk.Submit("SAL_RETURNNOTICE",model))

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
            "IgnoreInterationFlag": "",
        }

        res = json.loads(api_sdk.Audit("SAL_RETURNNOTICE", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False

def saleOrder_view(api_sdk,value,materialID):
    '''
    销售出库单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "SAL_OUTSTOCK", "FieldKeys": "FDate,FBillNo,FId,FEntity_FENTRYID,FMaterialID", "FilterString": [{"Left":"(","FieldName":"FMaterialID","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res