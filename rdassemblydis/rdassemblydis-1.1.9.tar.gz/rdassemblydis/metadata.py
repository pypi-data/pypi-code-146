import json
from rdassemblydis import operation as db
from rdassemblydis import utility as ut


def ERP_Save(app2,app3,api_sdk,option,data):
    '''
    组装拆卸单
    :return:
    '''

    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            if check_order_exists(api_sdk,i['FBillNo'])!=True:

                model={
                        "Model": {
                            "FID": 0,
                            "FBillNo":str(i['FBillNo']),
                            "FBillTypeID": {
                                "FNUMBER": "ZZCX01_SYS"
                            },
                            "FStockOrgId": {
                                "FNumber": "104"
                            },
                            "FAffairType": "Assembly" if i['FAFFAIRTYPE']=="组装" else "Dassembly",
                            "FDate": str(i['Fdate']),
                            "FDeptID": {
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
                            "FSubProOwnTypeIdH": "BD_OwnerOrg",
                            "FSubProOwnerIdH": {
                                "FNumber": "104"
                            },
                            "FEntity": [
                                {
                                    "FMaterialID": {
                                        "FNumber": db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER",i['FItemNumber'])
                                    },
                                    # "FUnitID": {
                                    #     "FNumber": "01"
                                    # },
                                    "FQty": str(i['Fqty']),
                                    "FStockID": {
                                        "FNumber": "SK01"
                                    },
                                    "FStockLocId": {
                                        "FSTOCKLOCID__FF100002": {
                                            "FNumber": "SK01"
                                        }
                                    },
                                    "FStockStatusID": {
                                        "FNumber": "KCZT01_SYS"
                                    },
                                    "FLOT": {
                                        "FNumber": str(i['Flot']) if db.isbatch(app2,i['FItemNumber'])=='1' else ""
                                    },
                                    # "FBaseUnitID": {
                                    #     "FNumber": "01"
                                    # },
                                    "FRefBomID": {
                                        "FNumber": ""
                                    },
                                    "FOwnerTypeID": "BD_OwnerOrg",
                                    "FOwnerID": {
                                        "FNumber": "104"
                                    },
                                    "FKeeperTypeID": "BD_KeeperOrg",
                                    "FKeeperID": {
                                        "FNumber": "104"
                                    },
                                    "FProduceDate": str(i['FPRODUCEDATE']) if db.iskfperiod(app2,i['FItemNumber'])=='1' else "",
                                    "FEXPIRYDATE": str(i['FEFFECTIVEDATE']) if db.iskfperiod(app2,i['FItemNumber'])=='1' else "",
                                    # "FInstockDate": "2022-11-12 00:00:00",
                                    "FSubEntity": ut.data_splicing(app2,app3,i['FBillNo'])
                                }
                            ]
                        }
                    }

                save_res=json.loads(api_sdk.Save("STK_AssembledApp",model))

                if save_res['Result']['ResponseStatus']['IsSuccess']:

                    submit_res=ERP_submit(api_sdk,i['FBillNo'])

                    if submit_res:

                        audit_res=ERP_Audit(api_sdk,i['FBillNo'])

                        if audit_res:
                            db.insertLog(app3, "组装拆卸单", i['FBillNo'],
                                         "数据同步成功", "1")

                            db.changeStatus(app3,i['FBillNo'],"1")

                            sucess_num=sucess_num+1

                    else:
                        pass
                else:

                    db.insertLog(app3, "组装拆卸单", i['FBillNo'],
                                 save_res['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                    db.changeStatus(app3, i['FBillNo'], "2")

                    erro_num=erro_num+1

                    erro_list.append(save_res)

        except Exception as e:

            db.insertLog(app3, "组装拆卸单", i['FBillNo'],
                         "数据异常", "2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }
    return dict



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

        res=json.loads(api_sdk.View("STK_AssembledApp",model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return True


def ERP_submit(api_sdk, FNumber):

    try:

        model = {
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": ""
        }

        res = json.loads(api_sdk.Submit("STK_AssembledApp", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False

def ERP_Audit(api_sdk, FNumber):
    '''
    将订单审核
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    try:

        model = {
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "InterationFlags": "",
            "NetworkCtrl": "",
            "IsVerifyProcInst": "",
            "IgnoreInterationFlag": "",
        }

        res = json.loads(api_sdk.Audit("STK_AssembledApp", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False


def json_model(app2,i):
    '''
    子件数据模型
    :param app2:
    :param i:
    :return:
    '''

    try:

        model={
                "FMaterialIDSETY": {
                    "FNumber": db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER",i['FItemNumber'])
                },
                # "FUnitIDSETY": {
                #     "FNumber": "01"
                # },
                "FQtySETY": str(i['Fqty']),
                "FStockIDSETY": {
                    "FNumber": "SK01"
                },
                "FStockLocIdSETY": {
                    "FSTOCKLOCIDSETY__FF100002": {
                        "FNumber": "SK01"
                    }
                },
                "FStockStatusIDSETY": {
                    "FNumber": "KCZT01_SYS"
                },
                "FLOTSETY": {
                    "FNumber": str(i['Flot']) if db.isbatch(app2,i['FItemNumber'])=='1' else ""
                },
                # "FBaseUnitIDSETY": {
                #     "FNumber": "01"
                # },
                "FKeeperTypeIDSETY": "BD_KeeperOrg",
                "FKeeperIDSETY": {
                    "FNumber": "104"
                },
                "FOwnerTypeIDSETY": "BD_OwnerOrg",
                "FOwnerIDSETY": {
                    "FNumber": "104"
                },
                "FProduceDateSETY": str(i['FPRODUCEDATE']) if db.iskfperiod(app2,i['FItemNumber'])=='1' else "",
                "FEXPIRYDATESETY": str(i['FEFFECTIVEDATE']) if db.iskfperiod(app2,i['FItemNumber'])=='1' else "",
            }


        return model

    except Exception as e:

        return {}