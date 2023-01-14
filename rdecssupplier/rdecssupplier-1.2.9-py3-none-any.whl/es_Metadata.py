import json
from rdecssupplier import es_DatabaseOperations as db


def get_FCurrencyNo(app2,fname):
    sql = f"""select fnumber from rds_vw_currency where fname = '{fname}'"""
    res = app2.select(sql)
    if res:
        return res[0]
    else:
        return 'PRE001'

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

        try:

            if i['FName'] == "苏州赛普生物科技有限公司":

                continue

            if rc.getStatus(app3, i['FNumber'], 'RDS_ECS_ODS_bd_SupplierDetail') and checkExist(app2,i['FName']) == []:

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
                        "FName": i['FName'],
                        # "FNumber": i['FNumber'],
                        "FShortName": i['FShortName'],
                        "F_SZSP_Text": i['FNumber'],
                        "FBaseInfo": {
                            "FCountry": {
                                "FNumber": "China" if i['FCountry'] == "" or i[
                                    'FCountry'] == "中国" else rc.getCountryCode(
                                    app2, i['FCountry'])
                            },
                            "FSOCIALCRECODE": i['FUniversalCode'],
                            "FRegisterAddress": i['FRegisterAddress'],
                            "FZip": i['FZipCode'],
                            "FFoundDate": "",
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
                                "FNumber": "PRE001" if i['FCurrencyNo'] == '' else get_FCurrencyNo(app2, i['FCurrencyNo'])
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
                                    "FNumber": "PRE001" if i['FCurrencyNo'] == '' else get_FCurrencyNo(app2, i['FCurrencyNo'])
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

                rj = json.loads(res)

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

                            AlloctOperation(api_sdk, i, rc, app2,rj,app3)

                            db.insertLog(app3, "ECS供应商", i['FNumber'], "数据同步成功", "1")

                            rc.changeStatus(app3, "1", "RDS_ECS_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "1", "RDS_ECS_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])

                        else:
                            db.insertLog(app3, "ECS供应商", i['FNumber'], ra, "2")
                            rc.changeStatus(app3, "2", "RDS_ECS_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "2", "RDS_ECS_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                    else:
                        db.insertLog(app3, "ECS供应商", i['FNumber'], rs, "2")
                        rc.changeStatus(app3, "2", "RDS_ECS_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                        rc.changeStatus(app3, "2", "RDS_ECS_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
                else:
                    db.insertLog(app3, "ECS供应商", i['FNumber'], rj, "2")
                    rc.changeStatus(app3, "2", "RDS_ECS_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                    rc.changeStatus(app3, "2", "RDS_ECS_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])
            else:

                rc.changeStatus(app3, "1", "RDS_ECS_ODS_bd_SupplierDetail", "FNumber", i['FNumber'])
                rc.changeStatus(app3, "1", "RDS_ECS_SRC_bd_SupplierDetail", "FNumber", i['FNumber'])


        except Exception as e:

            db.insertLog(app3, "ECS供应商", i['FNumber'], "数据异常", "2")




def ERP_supplierUnAudit(number, api_sdk):
    '''
    反审核
    :param number:
    :param api_sdk:
    :return:
    '''
    data = {
        "CreateOrgId": 0,
        "Numbers": [number],
        "Ids": "",
        "InterationFlags": "",
        "IgnoreInterationFlag": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": ""
    }
    res = api_sdk.UnAudit("BD_Supplier", data)

    return res


def ERP_supplierDelete(number, api_sdk):
    '''
    删除
    :param number:
    :param api_sdk:
    :return:
    '''
    data = {
        "CreateOrgId": 0,
        "Numbers": [number],
        "Ids": "",
        "NetworkCtrl": ""
    }
    res = api_sdk.Delete("BD_Supplier", data)

    return res

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


def ERP_CancelAllocate(forbid, PkIds, TOrgIds, api_sdk):
    '''
    取消分配
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

    res = api_sdk.CancelAllocate(forbid, data)

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


def AlloctOperation(api_sdk, i, rc, app2,rj,app3):
    '''
    数据分配后进行提交审核
    :param forbid:
    :param number:
    :param api_sdk:
    :return:
    '''

    SaveAfterAllocation(api_sdk, i, rc, app2,rj,app3)


def SaveAfterAllocation(api_sdk, i, rc, app2,rj,app3):

    try:

        FOrgNumber = rc.getOrganizationFNumber(app2, i['FApplyOrgName'])
        i['FNumber'] = rj['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']
        model = {
            "Model": {
                "FSupplierId": queryDocuments(app2, api_sdk, i['FNumber'], FOrgNumber['FORGID']),
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
                "FNumber": str(i['FNumber'])
                ,
                "FShortName": i['FShortName'],
                "FBaseInfo": {
                    "FCountry": {
                        "FNumber": "China" if i['FCountry'] == "" or i['FCountry'] == "中国" else rc.getCountryCode(app2, i[
                            'FCountry'])
                    },
                    "FSOCIALCRECODE": i['FUniversalCode'],
                    "FRegisterAddress": i['FRegisterAddress'],
                    # "FDeptId": {
                    #     "FNumber": rc.codeConversionOrg(app2, "rds_vw_department", i['FMngrDeptName'],
                    #                                     str(FOrgNumber['FNumber']))
                    # },
                    "FDeptId": {
                        "FNumber":'BM000040'
                    },
                    "FStaffId": {
                        "FNumber": rc.codeConversion(app2, "rds_vw_employees", i['FMngrMan'])
                    },
                    # "FStaffId": {
                    #     "FNumber": 'BSP00019'
                    # },
                    "FZip": i['FZipCode'],
                    "FFoundDate": '',
                    "FRegisterCode": str(i['FUniversalCode']),
                    "FSupplyClassify": "CG" if i['FSullierType'] == "" else rc.getSullierTypeCode(i['FSullierType']),
                    "FSupplierGrade": {
                        "FNumber": i['FSupplierGradeNo']
                    }
                },
                "FBusinessInfo": {
                    "FPurchaserGroupId": {
                        "FNumber": "SKYX02"
                    },
                    "FSettleTypeId": {
                        "FNumber": str(i['FSettlementMethodNo'])
                    },
                    "FPRICELISTID": {
                        "FNumber": str(i['FPriceListNo'])
                    },
                    "FProviderId": {
                        "FNumber": str(i['FNumber'])
                    },
                    "FVmiBusiness": False,
                    "FEnableSL": False
                },
                "FFinanceInfo": {
                    "FPayCurrencyId": {
                        "FNumber": "PRE001" if i['FCurrencyNo'] == '' else get_FCurrencyNo(app2, i['FCurrencyNo'])
                    },
                    "FPayCondition": {
                        "FNumber": i['FPaymentConditionNo']
                    },
                    "FSettleId": {
                        "FNumber": str(i['FNumber'])
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
                            "FNumber": "PRE001" if i['FCurrencyNo'] == '' else get_FCurrencyNo(app2, i['FCurrencyNo'])
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
        res = json.loads(api_sdk.Save("BD_Supplier", model))

        if res['Result']['ResponseStatus']['IsSuccess']:
            submit_res = json.loads(ERP_suppliersubmit(i['FNumber'], api_sdk))
            audit_res = json.loads(ERP_audit("BD_Supplier", i['FNumber'], api_sdk))

    except Exception as e:

        db.insertLog(app3, "ECS供应商", i['FNumber'], "分配时异常", "1")



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


def checkExist(app2,FName):
    '''
    查看数据是否已存在
    :param app2:
    :param Fnumber:
    :return:
    '''

    sql=f"select FNUMBER from rds_vw_supplier where FNAME='{FName}'"
    res=app2.select(sql)

    return res


def judgeDate(FNumber, api_sdk):
    '''
    查看数据是否在ERP系统存在
    :param FNumber: 供应商编码
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
