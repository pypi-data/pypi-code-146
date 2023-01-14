import json
from rdreturnrequest import operation as db
from rdreturnrequest import utility as ut

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
                            "FNUMBER": "TLSQDD01_SYS"
                        },
                        "FBillNo": str(i[0]['FMRBBILLNO']),
                        "FDate": str(i[0]['FDATE']),
                        "FAPPORGID": {
                            "FNumber": "104"
                        },
                        "FRequireOrgId": {
                            "FNumber": "104"
                        },
                        "FRMTYPE": "B",
                        "FRMMODE": "A",
                        "FCorrespondOrgId": {
                            "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                        },
                        "FRMREASON": {
                            "FNumber": "01"
                        },
                        "FPURCHASEORGID": {
                            "FNumber": "104"
                        },
                        "FSUPPLIERID": {
                            "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                        },
                        "F_SubEntity_FIN": {
                            "FSettleTypeId": {
                                "FNumber": "104"
                            },
                            "FLOCALCURRID": {
                                "FNumber": "PRE001"
                            },
                            "FExchangeTypeId": {
                                "FNUMBER": "HLTX01_SYS"
                            },
                            "FISPRICEEXCLUDETAX": True
                        },
                        "FEntity": ut.data_splicing(app2,api_sdk,i)
                    }
                }


                res=json.loads(api_sdk.Save("PUR_MRAPP",model))

                if res['Result']['ResponseStatus']['IsSuccess']:

                    FNumber = res['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                    submit_res=ERP_submit(api_sdk,FNumber)

                    if submit_res:

                        audit_res=ERP_Audit(api_sdk,FNumber)

                        if audit_res:

                            db.insertLog(app3, "退料申请单", i[0]['FMRBBILLNO'], "数据同步成功", "1")

                            db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"3")

                            sucess_num=sucess_num+1

                            pass

                        else:
                            pass
                    else:
                        pass
                else:

                    db.insertLog(app3, "退料申请单", i[0]['FMRBBILLNO'],res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                    db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                    erro_num=erro_num+1

                    erro_list.append(res)
            else:
                db.changeStatus(app3, str(i[0]['FMRBBILLNO']), "3")

        except Exception as e:

            db.insertLog(app3, "退料申请单", i[0]['FMRBBILLNO'],"数据异常","2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict



def check_deliveryExist(api_sdk,FNumber):

    model={
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res=json.loads(api_sdk.View("PUR_MRAPP",model))

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

    res=json.loads(api_sdk.Submit("PUR_MRAPP",model))

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

    res = json.loads(api_sdk.Audit("PUR_MRAPP", model))

    return res['Result']['ResponseStatus']['IsSuccess']



def PurchaseOrder_view(api_sdk,value,materialID):
    '''
    单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "PUR_PurchaseOrder", "FieldKeys": "FDate,FBillNo,FId,FPOOrderEntry_FEntryID,FMaterialId", "FilterString": [{"Left":"(","FieldName":"FMaterialId","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res