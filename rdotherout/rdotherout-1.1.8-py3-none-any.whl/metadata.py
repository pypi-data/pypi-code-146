import json
from rdotherout import operation as db
from rdotherout import utility as ut

def erp_save(app2,api_sdk,option,data,app3):

        erro_list = []
        sucess_num = 0
        erro_num = 0


        api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                           option['app_sec'], option['server_url'])

        for i in data:

            try:

                if exist_order(api_sdk,i[0]['FDELIVERYNO'])!=True:

                        model={
                                "Model": {
                                    "FID": 0,
                                    "FBillNo": str(i[0]['FDELIVERYNO']),
                                    "FBillTypeID": {
                                        "FNUMBER": "QTCKD01_SYS"
                                    },
                                    "FStockOrgId": {
                                        "FNumber": "104"
                                    },
                                    "FPickOrgId": {
                                        "FNumber": "104"
                                    },
                                    "FStockDirect": "GENERAL",
                                    "FDate": str(i[0]['FDELIVERDATE']),
                                    "FCustId": {
                                        "FNumber": db.code_conversion(app2,"rds_vw_customer","FNAME",i[0]['FCUSTOMNAME'])
                                    },
                                    "FDeptId": {
                                        "FNumber": "BM000035"
                                    },
                                    "FStockerId": {
                                        "FNumber": "BSP00040"
                                    },
                                    "FStockerGroupId": {
                                        "FNumber": "SKCKZ01"
                                    },
                                    "FOwnerTypeIdHead": "BD_OwnerOrg",
                                    "FOwnerIdHead": {
                                        "FNumber": "104"
                                    },
                                    "FNote": str(i[0]['FTRADENO']),
                                    "FBaseCurrId": {
                                        "FNumber": "PRE001"
                                    },
                                    "F_SZSP_Assistant": {
                                        "FNumber": "LX04"
                                    },
                                    "FEntity": ut.data_splicing(app2,i)
                                }
                            }

                        save_res=json.loads(api_sdk.Save("STK_MisDelivery",model))

                        if save_res['Result']['ResponseStatus']['IsSuccess']:

                            submit_result = ERP_submit(api_sdk, str(i[0]['FDELIVERYNO']))

                            if submit_result:

                                audit_result = ERP_Audit(api_sdk, str(i[0]['FDELIVERYNO']))

                                if audit_result:

                                    db.insertLog(app3, "其他出库单", str(i[0]['FDELIVERYNO']), "数据同步成功", "1")

                                    db.changeStatus(app3, str(i[0]['FDELIVERYNO']), "1")

                                    sucess_num=sucess_num+1

                                else:
                                    db.changeStatus(app3, str(i[0]['FDELIVERYNO']), "2")
                            else:
                                db.changeStatus(app3, str(i[0]['FDELIVERYNO']), "2")
                        else:

                            db.insertLog(app3, "其他出库单", str(i[0]['FDELIVERYNO']),save_res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                            db.changeStatus(app3, str(i[0]['FDELIVERYNO']), "2")

                            erro_num=erro_num+1

                            erro_list.append(save_res)

            except Exception as e:
                db.insertLog(app3, "其他出库单", str(i[0]['FDELIVERYNO']),"数据异常","2")

        dict = {
            "sucessNum": sucess_num,
            "erroNum": erro_num,
            "erroList": erro_list
        }
        return dict


def ERP_submit(api_sdk,FNumber):

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }

    res=json.loads(api_sdk.Submit("STK_MisDelivery",model))

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

    res = json.loads(api_sdk.Audit("STK_MisDelivery", model))

    return res['Result']['ResponseStatus']['IsSuccess']

def exist_order(api_sdk,FNumber):
    '''
    查看订单是否存在
    :param api_sdk:
    :param FNumber:
    :return:
    '''
    model = {
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res = json.loads(api_sdk.View("STK_MisDelivery", model))

    return res['Result']['ResponseStatus']['IsSuccess']
