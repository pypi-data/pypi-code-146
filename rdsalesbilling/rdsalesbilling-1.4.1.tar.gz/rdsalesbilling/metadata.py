import json
from rdsalesbilling import operation as db
from rdsalesbilling import utility as ut


def ERP_Save(api_sdk, data, option, app2, app3):
    '''
    调用ERP保存接口
    :param api_sdk: 调用ERP对象
    :param data:  要插入的数据
    :param option: ERP密钥
    :param app2: 数据库执行对象
    :return:
    '''


    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        try:

            if check_order_exists(api_sdk, i[0]['FBILLNO']) != True:

                model = {
                    "Model": {
                        "FID": 0,
                        "FBillTypeID": {
                            "FNUMBER": "YSD01_SYS"
                        },
                        "FBillNo": str(i[0]['FBILLNO']),
                        "FDATE": str(i[0]['FINVOICEDATE']),
                        "FISINIT": False,
                        # "FENDDATE_H": str(i[0]['FINVOICEDATE']),
                        "FCUSTOMERID": {
                            "FNumber": "C003142" if i[0]['FCUSTOMNAME'] == "苏州亚通生物医疗科技有限公司" else db.code_conversion(app2,
                                                                                                                    "rds_vw_customer",
                                                                                                                    "FNAME",
                                                                                                                    i[0][
                                                                                                                        'FCUSTOMNAME'])
                        },
                        "FCURRENCYID": {
                            "FNumber": "PRE001" if i[0]['FCurrencyName'] == '' else db.code_conversion(app2,
                                                                                                       "rds_vw_currency",
                                                                                                       "FNAME", i[0][
                                                                                                           'FCurrencyName'])
                        },
                        "FPayConditon": {
                            "FNumber": "SKTJ05_SP"
                        },
                        "FISPRICEEXCLUDETAX": True,
                        "FSETTLEORGID": {
                            "FNumber": "104"
                        },
                        "FPAYORGID": {
                            "FNumber": "104"
                        },
                        "FSALEORGID": {
                            "FNumber": "104"
                        },
                        "FISTAX": True,
                        "FSALEDEPTID": {
                            "FNumber": view(api_sdk, i[0]['FOUTSTOCKBILLNO'], "SaleDeptID")
                        },
                        "FSALEERID": {
                            "FNumber": db.findSalesNo(app2,i[0]['FOUTSTOCKBILLNO'])
                        },
                        # "FSALEDEPTID": {
                        #     "FNumber": "BM000036"
                        # },
                        "FCancelStatus": "A",
                        "FBUSINESSTYPE": "BZ",
                        "FSetAccountType": "1",
                        "FISHookMatch": False,
                        "FISINVOICEARLIER": False,
                        "FWBOPENQTY": False,
                        "FISGENERATEPLANBYCOSTITEM": False,
                        "F_SZSP_FPHM": str(i[0]['FINVOICENO']),
                        "F_SZSP_XSLX": {
                            "FNumber": "1"
                        },
                        "FsubHeadSuppiler": {
                            "FORDERID": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME'] == "苏州亚通生物医疗科技有限公司" else db.code_conversion(
                                    app2, "rds_vw_customer", "FNAME", i[0]['FCUSTOMNAME'])
                            },
                            "FTRANSFERID": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME'] == "苏州亚通生物医疗科技有限公司" else db.code_conversion(
                                    app2, "rds_vw_customer", "FNAME", i[0]['FCUSTOMNAME'])
                            },
                            "FChargeId": {
                                "FNumber": "C003142" if i[0]['FCUSTOMNAME'] == "苏州亚通生物医疗科技有限公司" else db.code_conversion(
                                    app2, "rds_vw_customer", "FNAME", i[0]['FCUSTOMNAME'])
                            }
                        },
                        "FsubHeadFinc": {
                            # "FACCNTTIMEJUDGETIME": str(i[0]['FINVOICEDATE']),
                            "FMAINBOOKSTDCURRID": {
                                "FNumber": "PRE001" if i[0]['FCurrencyName'] == '' else db.code_conversion(app2,
                                                                                                           "rds_vw_currency",
                                                                                                           "FNAME", i[0][
                                                                                                               'FCurrencyName'])
                            },
                            "FEXCHANGETYPE": {
                                "FNumber": "HLTX01_SYS"
                            },
                            "FExchangeRate": 1.0,
                            "FISCARRIEDDATE": False
                        },
                        "FEntityDetail": ut.data_splicing(app2, api_sdk, i),
                        "FEntityPlan": [
                            {
                                # "FENDDATE": str(i[0]['FINVOICEDATE']),
                                "FPAYRATE": 100.0,
                            }
                        ]
                    }
                }
                save_result = json.loads(api_sdk.Save("AR_receivable", model))
                if save_result['Result']['ResponseStatus']['IsSuccess']:

                    FNumber = save_result['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                    submit_res = ERP_submit(api_sdk, FNumber)

                    if submit_res:

                        # audit_res = ERP_Audit(api_sdk, FNumber)
                        db.insertLog(app3, "应收单", str(i[0]['FBILLNO']), "数据同步成功", "1")

                        db.changeStatus(app3, str(i[0]['FBILLNO']), "1")

                        sucess_num = sucess_num + 1

                        # if audit_res:
                        #
                        #     db.changeStatus(app3, str(i[0]['FBILLNO']), "3")
                        #
                        #     sucess_num=sucess_num+1
                        #
                        # else:
                        #     pass
                    else:
                        pass
                else:

                    db.insertLog(app3, "应收单", str(i[0]['FBILLNO']),save_result['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                    db.changeStatus(app3, str(i[0]['FBILLNO']), "2")
                    erro_num = erro_num + 1
                    erro_list.append(save_result)

        except Exception as e:

            db.insertLog(app3, "应收单", str(i[0]['FBILLNO']),"数据异常","2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict



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

        res = json.loads(api_sdk.Submit("AR_receivable", model))

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
            "IgnoreInterationFlag": ""
        }

        res = json.loads(api_sdk.Audit("AR_receivable", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False


def json_model(app2, model_data, api_sdk,index,result,materialSKU):

    try:

        materialId = db.code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU, "104", "FMATERIALID")

        if materialSKU == "7.1.000001":
            materialId = "466653"


        if result != [] and materialId != "":

            model = {
                "FMATERIALID": {
                    "FNumber": "7.1.000001" if model_data['FPrdNumber'] == '1' else str(
                        db.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", model_data['FPrdNumber']))
                },
                "FPriceQty": str(model_data['FQUANTITY']),
                "FTaxPrice": str(result[index]['FTAXPRICE']),
                "FPrice": str(model_data['FUNITPRICE']),
                "FEntryTaxRate": float(model_data['FTAXRATE']) * 100,
                "FNoTaxAmountFor_D": str(model_data['FSUMVALUE']),
                "FDeliveryControl": False,
                "FLot": {
                    "FNumber": str(model_data['FLot'])
                },
                "FStockQty": str(model_data['FQUANTITY']),
                # "FIsFree": False,
                "FStockBaseQty": str(model_data['FQUANTITY']),
                "FSalQty": str(model_data['FQUANTITY']),
                "FSalBaseQty": str(model_data['FQUANTITY']),
                "FPriceBaseDen": 1.0,
                "FSalBaseNum": 1.0,
                "FStockBaseNum": 1.0,
                "FNOINVOICEQTY": str(model_data['FQUANTITY']),
                "FTAILDIFFFLAG": False,
                "FEntityDetail_Link": [{
                    "FEntityDetail_Link_FRuleId": "AR_OutStockToReceivableMap" if int(model_data['FQUANTITY'])>0 else "",
                    "FEntityDetail_Link_FSTableName": "T_SAL_OUTSTOCKENTRY" if int(model_data['FQUANTITY'])>0 else "",
                    "FEntityDetail_Link_FSBillId ": result[index]['Fid'],
                    "FEntityDetail_Link_FSId": result[index]['FENTRYID'],
                    "FEntityDetail_Link_FBASICUNITQTYOld": str(model_data['FQUANTITY']),
                    "FEntityDetail_Link_FBASICUNITQTY": str(model_data['FQUANTITY']),
                    "FEntityDetail_Link_FStockBaseQtyOld": str(model_data['FQUANTITY']),
                    "FEntityDetail_Link_FStockBaseQty": str(model_data['FQUANTITY']),
                }]
            }

            return model

        else:

            return {}

    except Exception as e:

        return {}


def check_order_exists(api_sdk, FNumber):
    '''
    查看订单是否在ERP系统存在
    :param api: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model = {
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res = json.loads(api_sdk.View("AR_receivable", model))

    return res['Result']['ResponseStatus']['IsSuccess']


def outOrder_view(api_sdk, value, materialID,qtyValue,dlotValue):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res = json.loads(api_sdk.ExecuteBillQuery(
        {"FormId": "SAL_OUTSTOCK", "FieldKeys": "FDate,FBillNo,FId,FEntity_FENTRYID,FMaterialID,FTaxPrice",
         "FilterString": [{"Left": "(", "FieldName": "FMaterialID", "Compare": "=", "Value": materialID, "Right": ")",
                           "Logic": "AND"},
                          {"Left": "(", "FieldName": "FBillNo", "Compare": "=", "Value": value, "Right": ")",
                           "Logic": "AND"},
                            {"Left": "(", "FieldName": "FRealQty", "Compare": "=", "Value": qtyValue, "Right": ")",
                           "Logic": "AND"},
                          {"Left": "(", "FieldName": "FLot", "Compare": "=", "Value": dlotValue, "Right": ")",
                           "Logic": "AND"}], "TopRowCount": 0}))

    return res


def view(api_sdk, FNumber, param):
    '''
    通过查询接口，查询销售员和销售部门
    :param api_sdk:
    :param FNumber:
    :param param:
    :return:
    '''

    try:

        model = {
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res = json.loads(api_sdk.View("SAL_SaleOrder", model))

        if res['Result']['ResponseStatus']['IsSuccess']:

            return res['Result']['Result'][param]['Number']

        else:
            return ""

    except Exception as e:

        return "BSP00068_GW000159_111785"
