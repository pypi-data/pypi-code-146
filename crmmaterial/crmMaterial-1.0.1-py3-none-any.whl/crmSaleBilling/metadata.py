import datetime
import json
from crmSaleBilling import operation as db
from crmSaleBilling import utility as ut


def ERP_Save(api_sdk, data, option, app2, app3):
    '''
    调用ERP保存接口
    :param api_sdk: 调用ERP对象
    :param data:  要插入的数据
    :param option: ERP密钥
    :param app2: 数据库执行对象
    :return:
    '''

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])
    ret_data = []
    for i in data:

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
                    "FENDDATE_H": str(i[0]['FINVOICEDATE']),
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
                    "FISPRICEEXCLUDETAX": True,
                    "FSETTLEORGID": {
                        "FNumber": "101"
                    },
                    "FPAYORGID": {
                        "FNumber": "101"
                    },
                    "FSALEORGID": {
                        "FNumber": "101"
                    },
                    "FISTAX": True,
                    "FSALEDEPTID": {
                        "FNumber": "BM000036"
                    },
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
                        "FACCNTTIMEJUDGETIME": str(i[0]['FINVOICEDATE']),
                        "FMAINBOOKSTDCURRID": {
                            "FNumber": "PRE001" if i[0]['FCurrencyName'] == None else db.code_conversion(app2,
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
                            "FENDDATE": str(i[0]['FINVOICEDATE']),
                            "FPAYRATE": 100.0,
                        }
                    ]
                }
            }
            save_result = json.loads(api_sdk.Save("AR_receivable", model))
            print(save_result)
            if save_result['Result']['ResponseStatus']['IsSuccess']:

                FNumber = save_result['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                submit_res = ERP_submit(api_sdk, FNumber)

                if submit_res:
                    db.changeStatus(app3, str(i[0]['FBILLNO']), "3")
                else:
                    pass
                ret_data.append(save_result['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']+"保存成功")
            else:
                inser_logging(app3, '销售开票保存到ERP', i[0]['FBILLNO'],
                              save_result['Result']['ResponseStatus']['Errors'][0]['Message'])
                db.changeStatus(app3, str(i[0]['FBILLNO']), "2")
                ret_data.append(save_result)
                print(str(i[0]['FBILLNO']))
    ret_dict = {
        "code":"1",
        "message":ret_data,

    }
    return ret_dict


def ERP_submit(api_sdk, FNumber):
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


def ERP_Audit(api_sdk, FNumber):
    '''
    将订单审核
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

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


def json_model(app2, model_data, api_sdk):
    materialId = db.code_conversion_org(app2, "rds_vw_material", "FNUMBER", model_data['FPrdNumber'], "101",
                                        "FMATERIALID")

    result = outOrder_view(api_sdk, model_data['FOUTSTOCKBILLNO'], materialId)

    if result != [] and materialId != "":

        model = {
            "FMATERIALID": {
                "FNumber": model_data['FPrdNumber']
            },
            "FPriceQty": str(model_data['FQUANTITY']),
            "FPrice": str(model_data['FUNITPRICE']),
            "FEntryTaxRate": float(model_data['FTAXRATE']),
            "FNoTaxAmountFor_D": str(model_data['FSUMVALUE']),
            "FDeliveryControl": False,
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
            'FSourceBillNo': model_data['FOUTSTOCKBILLNO'],
            "FEntityDetail_Link": [{
                "FEntityDetail_Link_FRuleId": "AR_OutStockToReceivableMap",
                "FEntityDetail_Link_FSTableName": "T_SAL_OUTSTOCKENTRY",
                "FEntityDetail_Link_FSBillId ": result[0][2],
                "FEntityDetail_Link_FSId": result[0][3],
                "FEntityDetail_Link_FBASICUNITQTYOld": str(model_data['FQUANTITY']),
                "FEntityDetail_Link_FBASICUNITQTY": str(model_data['FQUANTITY']),
                "FEntityDetail_Link_FStockBaseQtyOld": str(model_data['FQUANTITY']),
                "FEntityDetail_Link_FStockBaseQty": str(model_data['FQUANTITY']),
            }]
        }
        return model

    else:

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


def outOrder_view(api_sdk, value, materialID):
    '''
    销售订单单据查询
    :param value: 订单编码
    :return:
    '''

    res = json.loads(api_sdk.ExecuteBillQuery(
        {"FormId": "SAL_OUTSTOCK", "FieldKeys": "FDate,FBillNo,FId,FEntity_FENTRYID,FMaterialID", "FilterString": [
            {"Left": "(", "FieldName": "FMaterialID", "Compare": "=", "Value": materialID, "Right": ")",
             "Logic": "AND"},
            {"Left": "(", "FieldName": "FBillNo", "Compare": "=", "Value": value, "Right": ")", "Logic": "AND"}],
         "TopRowCount": 0}))

    return res


def ERP_unAudit(api_sdk, FNumber):
    model = {
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "InterationFlags": "",
        "IgnoreInterationFlag": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": ""
    }
    res = json.loads(api_sdk.UnAudit("AR_receivable", model))

    if res['Result']['ResponseStatus']['IsSuccess']:
        return f'{FNumber}订单删除成功'
    else:
        return res['Result']['ResponseStatus']['Errors'][0]['Message']


def ERP_delete(api_sdk, FNumber):
    model = {
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "NetworkCtrl": ""
    }
    res = json.loads(api_sdk.Delete("AR_receivable", model))

    if res['Result']['ResponseStatus']['IsSuccess']:
        return f'{FNumber}订单删除成功'
    else:
        return res['Result']['ResponseStatus']['Errors'][0]['Message']


def inser_logging(app3, FProgramName, FNumber, FMessage, FOccurrenceTime=str(datetime.datetime.now())[:19],
                  FCompanyName='CP'):
    sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "')"
    data = app3.insert(sql)
    return data
