import datetime
import json


def ERP_customersave(api_sdk, option, dData, app2, rc, app3):
    '''
    将数据进行保存
    :param option:
    :param dData:
    :return:
    '''

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])
    ret_data = []
    for i in dData:
        # if ExistFname(app2,'RDS_OA_ODS_bd_CustomerDetail',i['FName']):
        #     print(f"该{i['FName']}已存在 ")
        #     continue
        if rc.getStatus(app3, i['FNumber'], 'RDS_CRM_SRC_Customer') and rc.checkCustomerExist(app2, i['FName']) == []:
            model = {
                "Model": {
                    "FCUSTID": 0,
                    "FCreateOrgId": {
                        "FNumber": "100"
                    },
                    "FUseOrgId": {
                        "FNumber": "100"
                    },
                    "FName": i['FName'],
                    # "FNumber": i['FNumber'],
                    "FShortName": i['FShortName'],
                    "FCOUNTRY": {
                        "FNumber": "China",
                    },
                    "FTEL": i['FTEL'],
                    "FINVOICETITLE": i['FINVOICETITLE'],
                    "FTAXREGISTERCODE": i['FTAXREGISTERCODE'],
                    "FINVOICEBANKNAME": i['FBankName'],
                    "FINVOICETEL": i['FINVOICETEL'],
                    "FINVOICEBANKACCOUNT": i['FAccountNumber'],
                    "FINVOICEADDRESS": i['FINVOICEADDRESS'],
                    "FSOCIALCRECODE": i['FTAXREGISTERCODE'],
                    "FIsGroup": False,
                    "FIsDefPayer": False,
                    "F_SZSP_Text": i['F_SZSP_Text'],
                    'FSETTLETYPEID': {
                        "FNumber": i['FSETTLETYPENO'],
                    },
                    "FRECCONDITIONID": {
                        "FNumber": i['FRECCONDITIONNO'],
                    },
                    "F_SZSP_KHZYJB": {
                        "FNumber": i['F_SZSP_KHZYJBNo']
                    },
                    "F_SZSP_KHGHSX": {
                        "FNumber": i['F_SZSP_KHGHSXNo']
                    },
                    "F_SZSP_XSMS": {
                        "FNumber": i['F_SZSP_XSMSNo']
                    },
                    "F_SZSP_XSMSSX": {
                        "FNumber": i['F_SZSP_XSMSSXNo']
                    },
                    'F_SZSP_BLOCNAME': i['F_SZSP_BLOCNAME'],
                    "FCustTypeId": {
                        "FNumber": i['FCustTypeNo']
                    },
                    "FGroup": {
                        "FNumber": i['FGroupNo']
                    },
                    "FTRADINGCURRID": {
                        "FNumber": 'PRE001'
                    },
                    "FInvoiceType": "1" if i['FINVOICETYPE'] == "" or i['FINVOICETYPE'] == "增值税专用发票" else "2",
                    "FTaxType": {
                        "FNumber": "SFL02_SYS"
                    },
                    "FTaxRate": {
                        "FNumber": "SL02_SYS" if i['FTaxRate'] == "" else rc.getcode(app2, "FNUMBER", "rds_vw_taxRate",
                                                                                     "FNAME", i['FTaxRate'])
                    },
                    "FISCREDITCHECK": True,
                    "FIsTrade": True,
                    "FUncheckExpectQty": False,
                    "F_SZSP_KHFL": {
                        "FNumber": i['F_SZSP_KHFLNo']
                    },
                    "FT_BD_CUSTOMEREXT": {
                        "FEnableSL": False,
                        "FALLOWJOINZHJ": False
                    },
                    "FT_BD_CUSTBANK": [
                        {
                            "FENTRYID": 0,
                            "FCOUNTRY1": {
                                "FNumber": "China",
                            },
                            "FBANKCODE": i['FAccountNumber'],
                            "FACCOUNTNAME": i['FINVOICETITLE'],
                            "FBankTypeRec": {
                                "FNUMBER": ""
                            },
                            "FTextBankDetail": "",
                            "FBankDetail": {
                                "FNUMBER": ""
                            },
                            "FOpenAddressRec": "",
                            "FOPENBANKNAME": i['FBankName'],
                            "FCNAPS": "",
                            "FCURRENCYID": {
                                "FNumber": ""
                            },
                            "FISDEFAULT1": "false"
                        }
                    ],
                }
            }

            savedResultInformation = api_sdk.Save("BD_Customer", model)
            print(f"编码为：{savedResultInformation}")
            sri = json.loads(savedResultInformation)

            if sri['Result']['ResponseStatus']['IsSuccess']:
                submittedResultInformation = ERP_customersubmit(
                    sri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'], api_sdk)
                print(f"编码为：{submittedResultInformation}数据提交成功")

                subri = json.loads(submittedResultInformation)
                ret_data.append(sri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'] + '保存成功')
                if subri['Result']['ResponseStatus']['IsSuccess']:

                    k3FNumber = subri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']

                    auditResultInformation = ERP_audit('BD_Customer',
                                                       k3FNumber,
                                                       api_sdk)

                    auditres = json.loads(auditResultInformation)

                    if auditres['Result']['ResponseStatus']['IsSuccess']:

                        result = ERP_allocate('BD_Customer', getCodeByView('BD_Customer',
                                                                           k3FNumber, api_sdk),
                                              rc.getOrganizationCode(app2, i['FApplyOrgName']), api_sdk)

                        AlloctOperation('BD_Customer',
                                        k3FNumber, api_sdk, i,
                                        rc, app2)

                        rc.changeStatus(app3, "1", "RDS_CRM_SRC_Customer", "FNumber", i['FNumber'])
                        inser_logging(app3, '客户', i['FNumber'], i['FNumber'] + "保存成功"
                                      , FIsdo=1)
                        print(result)

                    else:
                        rc.changeStatus(app3, "2", "RDS_CRM_SRC_Customer", "FNumber", i['FNumber'])
                        print(auditres)
                else:
                    rc.changeStatus(app3, "2", "RDS_CRM_SRC_Customer", "FNumber", i['FNumber'])
                    print(subri)
            else:
                inser_logging(app3, '客户', i['FNumber'],
                              sri['Result']['ResponseStatus']['Errors'][0]['Message'], FIsdo=2)
                rc.changeStatus(app3, "2", "RDS_CRM_SRC_Customer", "FNumber", i['FNumber'])
                print(sri)
                ret_data.append(sri)
        else:
            inser_logging(app3, '客户', i['FNumber'], "该客户{}数据已存在于金蝶".format(i['FName']), FIsdo=2)
            print("{}已存在于金蝶".format(i['FName']))

    ret_dict = {
        "code": "1",
        "message": ret_data,

    }
    return ret_dict


def SaveAfterAllocation(api_sdk, i, rc, app2, FNumber):
    FOrgNumber = rc.getOrganizationFNumber(app2, i['FApplyOrgName'])

    model = {
        "Model": {
            "FCUSTID": queryDocuments(app2, FNumber, FOrgNumber['FORGID']),
            "FCreateOrgId": {
                "FNumber": "100"
            },
            "FUseOrgId": {
                "FNumber": str(FOrgNumber['FNUMBER'])
            },
            "FName": str(i['FName']),
            'FNumber': FNumber,
            "FCOUNTRY": {
                "FNumber": "China"
            },
            "FTRADINGCURRID": {
                "FNumber": "PRE001"
            },
            "FSALDEPTID": {
                "FNumber": rc.getcode(app2, "FNUMBER", "rds_vw_department", "FNAME", i['FAalesDeptName'])
            },
            "FSALGROUPID": {
                "FNumber": rc.getcode(app2, "FNUMBER", "rds_vw_saleGroup", "fname", i['FSalesGroupNo'])
            },
            "FSELLER": {
                "FNumber": rc.getcode(app2, "FNUMBER", "rds_vw_salesman", "FNAME", i['FSalesman'])
            },

        }
    }
    res = api_sdk.Save("BD_Customer", model)
    save_res = json.loads(res)
    if save_res['Result']['ResponseStatus']['IsSuccess']:
        submit_res = ERP_customersubmit(FNumber, api_sdk)
        audit_res = ERP_audit("BD_Customer", FNumber, api_sdk)

    print(f"修改编码为{FNumber}的信息:" + res)


def ERP_customersubmit(fNumber, api_sdk):
    '''
    提交
    :param fNumber:
    :param api_sdk:
    :return:
    '''
    model = {
        "CreateOrgId": 0,
        "Numbers": [fNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }
    res = api_sdk.Submit("BD_Customer", model)

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


def AlloctOperation(forbid, number, api_sdk, i, rc, app2):
    '''
    数据分配后进行提交审核
    :param forbid:
    :param number:
    :param api_sdk:
    :return:
    '''

    SaveAfterAllocation(api_sdk, i, rc, app2, number)


# def judgeDate(FNumber, api_sdk):
#     '''
#     查看数据是否在ERP系统存在
#     :param FNumber: 客户编码
#     :param api_sdk:
#     :return:
#     '''
# 
#     data = {
#         "CreateOrgId": 0,
#         "Number": FNumber,
#         "Id": "",
#         "IsSortBySeq": "false"
#     }
# 
#     res = json.loads(api_sdk.View("BD_Customer", data))
# 
#     return res['Result']['ResponseStatus']['IsSuccess']


def queryDocuments(app2, number, name):
    sql = f"""
        select a.FNUMBER,a.FCUSTID,a.FMASTERID,a.FUSEORGID,a.FCREATEORGID,b.FNAME from T_BD_Customer
        a inner join takewiki_t_organization b
        on a.FUSEORGID = b.FORGID
        where a.FNUMBER = '{number}' and a.FUSEORGID = '{name}'
        """
    res = app2.select(sql)

    if res != []:

        return res[0]['FCUSTID']

    else:

        return "0"


def ExistFname(app2, table, name):
    sql = f"""
            select FNAME from {table} where FNAME = {name}
            """
    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


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
    res = json.loads(api_sdk.UnAudit("BD_Customer", model))

    if res['Result']['ResponseStatus']['IsSuccess']:
        return f'{FNumber}客户反审核成功'
    else:
        return res['Result']['ResponseStatus']['Errors'][0]['Message']


def ERP_delete(api_sdk, FNumber):
    model = {
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "NetworkCtrl": ""
    }
    res = json.loads(api_sdk.Delete("BD_Customer", model))
    if res['Result']['ResponseStatus']['IsSuccess']:
        return f'{FNumber}客户删除成功'
    else:
        return res['Result']['ResponseStatus']['Errors'][0]['Message']


def ERP_CancelAllocate(app2, rc, api_sdk, FNumber, FApplyOrgName):
    FOrgNumber = rc.getOrganizationFNumber(app2, FApplyOrgName)
    FCUSTID = queryDocuments(app2, FNumber, FOrgNumber['FORGID']) - 1
    model = {
        "PkIds": FCUSTID,
        "TOrgIds": str(FOrgNumber['FORGID'])
    }
    res = json.loads(api_sdk.CancelAllocate("BD_Customer", model))

    if res['Result']['ResponseStatus']['IsSuccess']:
        return f'{FNumber}客户取消分配成功'
    else:
        return res['Result']['ResponseStatus']['Errors'][0]['Message']


def inser_logging(app, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                  FCompanyName='CP'):
    sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
        FIsdo) + ")"
    data = app.insert(sql)
    return data
