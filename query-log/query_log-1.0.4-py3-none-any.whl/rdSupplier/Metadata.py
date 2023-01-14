import json
from k3cloud_webapi_sdk.main import K3CloudApiSdk


def ERP_suppliersave(api_sdk, option, dData, app2, rc, app3):
    '''
    将数据进行保存
    :param option:
    :param dData:
    :return:
    '''

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in dData:

        # getStatus(app3,i['FNumber'],'RDS_OA_ODS_bd_SupplierDetail') and

        if rc.supplierISExist(app2, i['FName'], "100") == []:

            rc.changeStatus(app3, "0", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])

            if rc.getStatus(app3, i['FNumber'], 'RDS_OA_ODS_bd_SupplierDetail') :
                model = {
                    "Model": {
                        "FSupplierId": 0,
                        "FCreateOrgId": {
                            "FNumber": "100"
                        },
                        "FUseOrgId": {
                            "FNumber": "100"
                        },
                        "FGroup": {
                            "FNumber": i['FSupplierCategoryNo']
                        },
                        "FName": i['FName']
                        # "FNumber": i['FNumber']
                        ,
                        "FShortName": i['FShortName'],
                        "FBaseInfo": {
                            "FCountry": {
                                "FNumber": "China" if i['FCountry'] == "" or i[
                                    'FCountry'] == "中国" else rc.getCountryCode(
                                    app2, i['FCountry'])
                            },
                            "FSOCIALCRECODE": i['FUniversalCode'],
                            "FRegisterAddress": i['FRegisterAddress'],
                            "FZip": i['FZipCode'],
                            "FFoundDate": str(i['FDate']),
                            "FRegisterCode": str(i['FUniversalCode']),
                            "FSupplyClassify": "CG" if i['FSullierType'] == "" else rc.getSullierTypeCode(
                                i['FSullierType']),
                            "FSupplierGrade": {
                                "FNumber": i['FSupplierGradeNo']
                            }
                        },
                        "FBusinessInfo": {
                            "FSettleTypeId": {
                                "FNumber": i['FSettlementMethodNo']
                            },
                            "FPRICELISTID": {
                                "FNumber": i['FPriceListNo']
                            },
                            "FVmiBusiness": False,
                            "FEnableSL": False
                        },
                        "FFinanceInfo": {
                            "FPayCurrencyId": {
                                "FNumber": "PRE001" if i['FCurrencyNo'] == "" else i['FCurrencyNo']
                            },
                            "FPayCondition": {
                                "FNumber": i['FPaymentConditionNo']
                            },
                            "FTaxType": {
                                "FNumber": "SFL02_SYS"
                            },
                            "FTaxRegisterCode": str(i['FUniversalCode']),
                            "FInvoiceType": "1" if (i['FInvoiceType'] == "" or i['FInvoiceType'] == "增值税专用发票") else "2",
                            "FTaxRateId": {
                                "FNUMBER": "SL02_SYS" if i['FTaxRate'] == "" else rc.getTaxRateCode(app2, i['FTaxRate'])
                            }
                        },
                        "FBankInfo": [
                            {
                                "FBankCountry": {
                                    "FNumber": "China" if i['FCountry'] == "" or i[
                                        'FCountry'] == "中国" else rc.getCountryCode(app2, i['FCountry'])
                                },
                                "FBankCode": i['FAccountNumber'],
                                "FBankHolder": i['FAccountName'],
                                "FOpenBankName": i['FBankName'],
                                "FCNAPS": i['FBankTransferCode'],
                                "FOpenAddressRec": i['FBankAddr'],
                                "FBankCurrencyId": {
                                    "FNumber": "PRE001" if i['FCurrencyNo'] == "" else i['FCurrencyNo']
                                },
                                "FBankIsDefault": False
                            }
                        ],
                        "FSupplierContact": [
                            {
                                "FContactId": 0,
                                "FContact ": i['FContact'],
                                "FMobile": i['FMobile'],
                                "FEMail": i['FEMail']
                            }
                        ]
                    }
                }
                res = api_sdk.Save("BD_Supplier", model)
                print("保存数据结果为:" + res)

                rj = json.loads(res)
                k3FNumber = rj['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']
                # print(res)
                #       rj是保存后的结果

                if rj['Result']['ResponseStatus']['IsSuccess']:

                    returnResult = ERP_suppliersubmit(rj['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'],
                                                      api_sdk)
                    #           rs是提交后的结果
                    rs = json.loads(returnResult)

                    if rs['Result']['ResponseStatus']['IsSuccess']:
                        resAudit = ERP_audit('BD_Supplier',
                                             rs['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'],
                                             api_sdk)
                        ra = json.loads(resAudit)
                        # ra是审核后的结果信息
                        if ra['Result']['ResponseStatus']['IsSuccess']:
                            r = ERP_allocate('BD_Supplier', getCodeByView('BD_Supplier', rs['Result']['ResponseStatus'][
                                'SuccessEntitys'][0]['Number'], api_sdk),
                                             rc.getOrganizationCode(app2, i['FApplyOrgName']), api_sdk)

                            AlloctOperation(api_sdk, i, rc, app2,k3FNumber)

                            rc.changeStatus(app3, "1", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "1", "RDS_OA_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                            print(r)
                        else:
                            rc.changeStatus(app3, "2", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "2", "RDS_OA_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                            print(ra)
                    else:
                        rc.changeStatus(app3, "2", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                        rc.changeStatus(app3, "2", "RDS_OA_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                        print(rs)
                else:
                    rc.changeStatus(app3, "2", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                    rc.changeStatus(app3, "2", "RDS_OA_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                    print(rj)
            else:
                print("该编码{}已存在于金蝶".format(i['FNumber']))
        else:
            rc.changeStatus(app3, "2", "RDS_OA_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
            rc.changeStatus(app3, "2", "RDS_OA_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
            pass


def ERP_suppliersubmit(number, api_sdk):
    '''
    对创建的数据进行提交
    :param number 单据编号:
    :return:
    '''

    data = {
        "CreateOrgId": 0,
        "Numbers": [number],
        "Ids": "",
        "InterationFlags": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": "",
        "IgnoreInterationFlag": ""
    }

    res = api_sdk.Submit("BD_Supplier", data)

    return res


def ERP_audit(forbid, number, api_sdk):
    '''
    将状态为审核中的数据审核
    :param forbid: 表单ID
    :param number: 编码
    :param api_sdk: 接口执行对象
    :return:
    '''

    data = {
        "CreateOrgId": 0,
        "Numbers": [number],
        "Ids": "",
        "InterationFlags": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": "",
        "IgnoreInterationFlag": ""
    }

    res = api_sdk.Audit(forbid, data)

    return res


def ERP_allocate(forbid, PkIds, TOrgIds, api_sdk):
    '''
    分配
    :param forbid: 表单
    :param PkIds: 被分配的基础资料内码集合
    :param TOrgIds: 目标组织内码集合
    :param api_sdk: 接口执行对象
    :return:
    '''

    data = {
        "PkIds": int(PkIds),
        "TOrgIds": TOrgIds
    }

    res = api_sdk.Allocate(forbid, data)

    return res


def getCodeByView(forbid, number, api_sdk):
    '''
    通过编码找到对应的内码
    :param forbid: 表单ID
    :param number: 编码
    :param api_sdk: 接口执行对象
    :return:
    '''

    data = {
        "CreateOrgId": 0,
        "Number": number,
        "Id": "",
        "IsSortBySeq": "false"
    }
    # 将结果转换成json类型
    rs = json.loads(api_sdk.View(forbid, data))
    res = rs['Result']['Result']['Id']

    return res


def AlloctOperation(api_sdk, i, rc, app2,k3FNumber):
    '''
    数据分配后进行提交审核
    :param forbid:
    :param number:
    :param api_sdk:
    :return:
    '''

    SaveAfterAllocation(api_sdk, i, rc, app2,k3FNumber)


def SaveAfterAllocation(api_sdk, i, rc, app2,k3FNumber):
    FOrgNumber = rc.getOrganizationFNumber(app2, i['FApplyOrgName'])

    model = {
        "Model": {
            "FSupplierId": queryDocuments(app2, api_sdk, k3FNumber, FOrgNumber['FORGID']),
            "FCreateOrgId": {
                "FNumber": "100"
            },
            "FUseOrgId": {
                "FNumber": str(FOrgNumber['FNumber'])
            },
            "FGroup": {
                "FNumber": i['FSupplierCategoryNo']
            },
            "FName": str(i['FName']),
            'FNumber':str(k3FNumber),
            "FShortName": i['FShortName'],
            "FBaseInfo": {
                "FCountry": {
                    "FNumber": "China" if i['FCountry'] == "" or i['FCountry'] == "中国" else rc.getCountryCode(app2, i[
                        'FCountry'])
                },
                "FSOCIALCRECODE": i['FUniversalCode'],
                "FRegisterAddress": i['FRegisterAddress'],
                "FDeptId": {
                    "FNumber": 'BM000040' if str(FOrgNumber['FNumber'])=='104' else rc.codeConversionOrg(app2, "rds_vw_department", i['FMngrDeptName'],
                                                    str(FOrgNumber['FNumber']))
                },
                "FStaffId": {
                    "FNumber": rc.codeConversion(app2, "rds_vw_employees", i['FMngrMan'])
                },
                "FZip": i['FZipCode'],
                "FFoundDate": str(i['FDate']),
                "FRegisterCode": str(i['FUniversalCode']),
                "FSupplyClassify": "CG" if i['FSullierType'] == "" else rc.getSullierTypeCode(i['FSullierType']),
                "FSupplierGrade": {
                    "FNumber": i['FSupplierGradeNo']
                }
            },
            "FBusinessInfo": {
                "FSettleTypeId": {
                    "FNumber": str(i['FSettlementMethodNo'])
                },
                "FPRICELISTID": {
                    "FNumber": str(i['FPriceListNo'])
                },
                "FProviderId": {
                    "FNumber": str(k3FNumber)
                },
                "FVmiBusiness": False,
                "FEnableSL": False
            },
            "FFinanceInfo": {
                "FPayCurrencyId": {
                    "FNumber": "PRE001" if i['FCurrencyNo'] == "" else i['FCurrencyNo']
                },
                "FPayCondition": {
                    "FNumber": i['FPaymentConditionNo']
                },
                "FSettleId": {
                    "FNumber":str(k3FNumber)
                },
                "FTaxType": {
                    "FNumber": "SFL02_SYS"
                },
                "FTaxRegisterCode": str(i['FUniversalCode']),
                "FChargeId": {
                    "FNumber": str(i['FNumber'])
                },
                "FInvoiceType": "1" if (i['FInvoiceType'] == "" or i['FInvoiceType'] == "增值税专用发票") else "2",
                "FTaxRateId": {
                    "FNUMBER": "SL02_SYS" if i['FTaxRate'] == "" else rc.getTaxRateCode(app2, i['FTaxRate'])
                }
            },
        }
    }
    res = json.loads(api_sdk.Save("BD_Supplier", model))

    print("修改数据结果为:" + str(res))

    if res['Result']['ResponseStatus']['IsSuccess']:
        submit_res = json.loads(ERP_suppliersubmit(str(k3FNumber), api_sdk))
        audit_res = json.loads(ERP_audit("BD_Supplier", str(k3FNumber), api_sdk))


def queryDocuments(app2, api_sdk, number, forgid):
    sql = f"""
        select a.FNUMBER,a.FSUPPLIERID,a.FMASTERID,a.FUSEORGID,a.FCREATEORGID,b.FNAME from T_BD_SUPPLIER  
        a inner join takewiki_t_organization b
        on a.FUSEORGID = b.FORGID
        where a.FNUMBER = '{number}' and b.FORGID = '{forgid}'
        """
    res = app2.select(sql)

    if res != []:

        return res[0]['FSUPPLIERID']

    else:

        return "0"


def judgeDate(FNumber, api_sdk):
    '''
    查看数据是否在ERP系统存在
    :param FNumber: 物料编码
    :param api_sdk:
    :return:
    '''

    data = {
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res = json.loads(api_sdk.View("BD_Supplier", data))

    return res['Result']['ResponseStatus']['IsSuccess']
