import json
from rdpurchasesbilling import utility as ut
from rdpurchasesbilling import operation as db
def ERP_Save(api_sdk,data,option,app2,app3):

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

    erro_list = []
    sucess_num = 0
    erro_num = 0

    for i in data:

        try:

            FNo = str(i[0]['FINVOICENO'])[0:8]

            if check_order_exists(api_sdk,FNo)!=True:

                    model={
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "YFD01_SYS"
                            },
                            "FBillNo": FNo,
                            "FISINIT": False,
                            "FDATE": str(i[0]['FINVOICEDATE']),
                            "FDOCUMENTSTATUS": "Z",
                            "FSUPPLIERID": {
                                "FNumber": db.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                            },
                            "FCURRENCYID": {
                                "FNumber": "PRE001"
                            },
                            # "FPayConditon": {
                            #     "FNumber": "003"
                            # },
                            "FISPRICEEXCLUDETAX": True,
                            "FBUSINESSTYPE": "CG",
                            "FISTAX": True,
                            "FSETTLEORGID": {
                                "FNumber": "104"
                            },
                            "FPAYORGID": {
                                "FNumber": "104"
                            },
                            "FSetAccountType": "1",
                            "FISTAXINCOST": False,
                            "FISHookMatch": False,
                            "FPURCHASEDEPTID": {
                                "FNumber": "BM000040"
                            },
                            "FPURCHASERID": {
                                "FNumber": db.code_conversion(app2,"rds_vw_buyer","FNAME",str(i[0]['FPURCHASERINAME']))
                            },
                            "FCancelStatus": "A",
                            "FISBYIV": False,
                            "FISGENHSADJ": False,
                            "FISINVOICEARLIER": False,
                            "FWBOPENQTY": False,
                            "FIsGeneratePlanByCostItem": False,
                            "F_SZSP_FPHM": FNo,
                            "FsubHeadSuppiler": {
                                "FORDERID": {
                                    "FNumber": db.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                                },
                                "FTRANSFERID": {
                                    "FNumber": db.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                                },
                                "FChargeId": {
                                    "FNumber": db.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104","FNUMBER")
                                }
                            },
                            "FsubHeadFinc": {
                                "FMAINBOOKSTDCURRID": {
                                    "FNumber": "PRE001"
                                },
                                "FEXCHANGETYPE": {
                                    "FNumber": "HLTX01_SYS"
                                },
                                "FExchangeRate": 1.0,
                                "FISCARRIEDDATE": False
                            },
                            "FEntityDetail": ut.data_splicing(app2,api_sdk,i)
                        }
                    }

                    save_result=json.loads(api_sdk.Save("AP_Payable",model))
                    if save_result['Result']['ResponseStatus']['IsSuccess']:

                        FNumber = save_result['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                        submit_res = ERP_submit(api_sdk, FNumber)

                        db.insertLog(app3, "应付单", str(i[0]['FINVOICENO']), "数据同步成功", "1")

                        db.changeStatus(app3, str(i[0]['FINVOICENO']), "1")

                        sucess_num=sucess_num+1

                        # if submit_res:
                        #
                        #     audit_res = ERP_Audit(api_sdk, FNumber)
                        #
                        #     if audit_res:
                        #
                        #         db.changeStatus(app3, str(i[0]['FBILLNO']), "3")
                        #
                        #     else:
                        #         pass
                        # else:
                        #     pass
                    else:

                        db.insertLog(app3, "应付单", str(i[0]['FINVOICENO']), save_result['Result']['ResponseStatus']['Errors'][0]['Message'],"2")

                        db.changeStatus(app3, str(i[0]['FINVOICENO']), "2")
                        erro_num=erro_num+1
                        erro_list.append(save_result)

        except Exception as e:

            db.insertLog(app3, "应付单", str(i[0]['FINVOICENO']), "数据异常","2")

    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict



def json_model(app2,model_data,api_sdk):

    try:
        materialSKU = "" if str(model_data['FPRDNUMBER']) == '1' else str(model_data['FPRDNUMBER'])
        materialId = db.code_conversion_org(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", materialSKU, "104", "FMATERIALID")

        # if materialSKU == "7.1.000001":
        #     materialId = "466653"

        # result = Order_view(api_sdk, str(model_data['FGODOWNNO']), materialId)str(model_data['FQTY'])

        result=db.checkCode(app2,str(model_data['FGODOWNNO']),str(model_data['FQTY']),str(model_data['FLot']),materialSKU)

        if result != [] and materialId != "":

            model={
                    "FMATERIALID": {
                        "FNumber": "7.1.000001" if str(model_data['FPRDNUMBER']) == '1' else str(model_data['FPRDNUMBER'])
                    },
                    "FPrice": str(model_data['FUNITPRICE']),
                    "FPriceQty": str(model_data['FQTY']),
                    "FEntryTaxRate": float(model_data['FTAXRATE'])*100,
                    "FNoTaxAmountFor_D": str(model_data['FSUMVALUE']),
                    "FINCLUDECOST": False,
                    "FISOUTSTOCK": False,
                    "FLot": {
                        "FNumber": str(model_data['FLot'])
                    },
                    "FIsFree": False,
                    "FStockQty": str(model_data['FQTY']),
                    "FStockBaseQty": str(model_data['FQTY']),
                    "FPriceBaseDen": 1.0,
                    "FStockBaseNum": 1.0,
                    "FNOINVOICEQTY": str(model_data['FQTY']),
                    "FTAILDIFFFLAG": False,
                    "FEntityDetail_Link": [{
                        "FEntityDetail_Link_FRuleId": "AP_InStockToPayableMap",
                        "FEntityDetail_Link_FSTableName": "T_STK_INSTOCKENTRY",
                        "FEntityDetail_Link_FSBillId ": result['FID'],
                        "FEntityDetail_Link_FSId": result['FENTRYID'],
                        "FEntityDetail_Link_FBASICUNITQTYOld": str(model_data['FQTY']),
                        "FEntityDetail_Link_FBASICUNITQTY": str(model_data['FQTY']),
                        "FEntityDetail_Link_FStockBaseQtyOld": str(model_data['FQTY']),
                        "FEntityDetail_Link_FStockBaseQty": str(model_data['FQTY']),
                    }]
                }

            return model

        else:

            return {}

    except Exception as e:

        return {}


def Order_view(api_sdk,value,materialID):
    '''
    采购入库单据查询
    :param value: 订单编码
    :return:
    '''

    res=json.loads(api_sdk.ExecuteBillQuery({"FormId": "STK_InStock", "FieldKeys": "FDate,FBillNo,FId,FInStockEntry_FEntryID,FMaterialId", "FilterString": [{"Left":"(","FieldName":"FMaterialId","Compare":"=","Value":materialID,"Right":")","Logic":"AND"},{"Left":"(","FieldName":"FBillNo","Compare":"=","Value":value,"Right":")","Logic":"AND"}], "TopRowCount": 0}))

    return res

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

        res=json.loads(api_sdk.View("AP_Payable",model))

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

        res=json.loads(api_sdk.Submit("AP_Payable",model))

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

        res = json.loads(api_sdk.Audit("AP_Payable", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    except Exception as e:

        return False