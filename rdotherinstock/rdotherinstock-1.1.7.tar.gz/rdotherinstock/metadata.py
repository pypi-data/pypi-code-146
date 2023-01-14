import json
from rdotherinstock import operation as db
from rdotherinstock import utility as ut

def erp_save(app2,api_sdk,option,data,app3):


    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            if exist_order(api_sdk,i[0]['FGODOWNNO'])!=True:

                    model={
                        "Model": {
                            "FID": 0,
                            "FBillNo": str(i[0]['FGODOWNNO']),
                            "FBillTypeID": {
                                "FNUMBER": "QTRKD01_SYS"
                            },
                            "FStockOrgId": {
                                "FNumber": "104"
                            },
                            "FStockDirect": "GENERAL",
                            "FDate": str(i[0]['FBUSINESSDATE']),
                            "FSUPPLIERID": {
                                "FNumber": db.code_conversion(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'])
                            },
                            "FDEPTID": {
                                "FNumber": "BM000040"
                            },
                            "FSTOCKERID": {
                                "FNumber": "BSP00040"
                            },
                            "FSTOCKERGROUPID": {
                                "FNumber": "SKCKZ01"
                            },
                            "FOwnerTypeIdHead": "BD_OwnerOrg",
                            "FOwnerIdHead": {
                                "FNumber": "104"
                            },
                            "FNOTE": str(i[0]['FBILLNO']),
                            "FBaseCurrId": {
                                "FNumber": "PRE001"
                            },
                            "FEntity": ut.data_splicing(app2,i)
                        }
                    }

                    save_res=json.loads(api_sdk.Save("STK_MISCELLANEOUS",model))

                    if save_res['Result']['ResponseStatus']['IsSuccess']:

                        submit_result = ERP_submit(api_sdk, str(i[0]['FGODOWNNO']))

                        if submit_result:

                            audit_result = ERP_Audit(api_sdk, str(i[0]['FGODOWNNO']))

                            if audit_result:

                                db.insertLog(app3, "其他入库单", str(i[0]['FGODOWNNO']), "数据同步成功", "1")

                                db.changeStatus(app3, str(i[0]['FGODOWNNO']), "1")

                                sucess_num=sucess_num+1

                            else:
                                db.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")
                        else:
                            db.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")
                    else:

                        db.insertLog(app3, "其他入库单", str(i[0]['FGODOWNNO']),save_res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                        db.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")

                        erro_num=erro_num+1
                        erro_list.append(save_res)

        except Exception as e:

            db.insertLog(app3, "其他入库单", str(i[0]['FGODOWNNO']),"数据异常","2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict



def exist_order(api_sdk,FNumber):
    '''
    查看订单是否存在
    :param api_sdk:
    :param FNumber:
    :return:
    '''
    try:

        model = {
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res = json.loads(api_sdk.View("STK_MISCELLANEOUS", model))

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

        res=json.loads(api_sdk.Submit("STK_MISCELLANEOUS",model))

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

        res = json.loads(api_sdk.Audit("STK_MISCELLANEOUS", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False