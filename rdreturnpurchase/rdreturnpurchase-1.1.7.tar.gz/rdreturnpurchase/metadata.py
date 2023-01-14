from rdreturnpurchase import utility as ut
from rdreturnpurchase import operation as db
import json

def associated(app2,api_sdk,option,data,app3):

        erro_list = []
        sucess_num = 0
        erro_num = 0

        api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                           option['app_sec'], option['server_url'])

        for i in data:

            try:

                if check_outstock_exists(api_sdk,i[0]['FMRBBILLNO'])!=True:

                        model = {
                            "Model": {
                                "FID": 0,
                                "FBillTypeID": {
                                    "FNUMBER": "TLD01_SYS"
                                },
                                "FBillNo": str(i[0]['FMRBBILLNO']),
                                "FDate": str(i[0]['FDATE']),
                                "FMRTYPE": "B",
                                "FMRMODE": "A",
                                "FStockOrgId": {
                                    "FNumber": "104"
                                },
                                "FMRDeptId": {
                                    "FNumber": "BM000040"
                                },
                                "FSTOCKERID": {
                                    "FNumber": "BSP00040"
                                },
                                "FSTOCKERGROUPID": {
                                    "FNumber": "SKCKZ01"
                                },
                                "FIsConvert": False,
                                "FCorrespondOrgId": {
                                    "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                                },

                                "FMRREASON": {
                                    "FNumber": "01"
                                },
                                "FRequireOrgId": {
                                    "FNumber": "104"
                                },
                                "FPurchaseOrgId": {
                                    "FNumber": "104"
                                },
                                "FSupplierID": {
                                    "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                                },
                                "FACCEPTORID": {
                                    "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                                },
                                "FSettleId": {
                                    "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                                },
                                "FCHARGEID": {
                                    "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                                },
                                "FOwnerTypeIdHead": "BD_OwnerOrg",
                                "FOwnerIdHead": {
                                    "FNumber": "104"
                                },
                                "FACCTYPE": "Q",
                                "FPURMRBFIN": {
                                    "FSettleOrgId": {
                                        "FNumber": "104"
                                    },
                                    "FSETTLETYPEID": {
                                        "FNumber": "JSFS04_SYS"
                                    },
                                    "FSettleCurrId": {
                                        "FNumber": "PRE001"
                                    },
                                    "FIsIncludedTax": True,
                                    "FPRICETIMEPOINT": "1",
                                    "FLOCALCURRID": {
                                        "FNumber": "PRE001"
                                    },
                                    "FEXCHANGETYPEID": {
                                        "FNumber": "HLTX01_SYS"
                                    },
                                    "FEXCHANGERATE": 1.0,
                                    "FISPRICEEXCLUDETAX": True
                                },
                                "FPURMRBENTRY": ut.data_splicing(app2,api_sdk,i,i[0]['FMRBBILLNO'])
                            }
                        }
                        res = json.loads(api_sdk.Save("PUR_MRB", model))

                        if res['Result']['ResponseStatus']['IsSuccess']:

                            submit_res = ERP_submit(api_sdk, str(i[0]['FMRBBILLNO']))

                            if submit_res:

                                audit_res = ERP_Audit(api_sdk, str(i[0]['FMRBBILLNO']))

                                if audit_res:

                                    db.insertLog(app3, "采购退料单", str(i[0]['FMRBBILLNO']),"数据同步成功", "1")

                                    db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"1")

                                    sucess_num=sucess_num+1

                                else:
                                    db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                            else:
                                db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                        else:
                            db.insertLog(app3, "采购退料单", i[0]['FMRBBILLNO'],res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                            db.changeStatus(app3,str(i[0]['FMRBBILLNO']),"2")

                            erro_num=erro_num+1

                            erro_list.append(res)

            except Exception as e:

                db.insertLog(app3, "采购退料单", str(i[0]['FMRBBILLNO']),"数据异常", "2")



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

    res=json.loads(api_sdk.View("PUR_MRB",model))

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

    res=json.loads(api_sdk.Submit("PUR_MRB",model))

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

    res = json.loads(api_sdk.Audit("PUR_MRB", model))

    return res['Result']['ResponseStatus']['IsSuccess']

def delivery_view(api_sdk,value):
    '''
    订单单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "PUR_MRAPP", "FieldKeys": "FDate,FBillNo,FId,FEntity_FEntryID", "FilterString": [{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res