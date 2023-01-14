import json
import re
import time
from rdecscustomer import ec_DatabaseOperations as db
def checkExist(app2,FName):
    '''
    查看数据是否已存在
    :param app2:
    :param Fnumber:
    :return:
    '''

    # sql=f"select distinct FNUMBER from rds_vw_customer where FNAME='{FName}' and FORGNUMBER='100'"
    sql = f"select distinct FNUMBER from  rds_vw_customer where FNAME='{FName}'"

    res=app2.select(sql)

    return res


def get_FCurrencyNo(app2,fname):
    sql = f"""select fnumber from rds_vw_currency where fname = '{fname}'"""
    res = app2.select(sql)
    if res:
        return res[0]['fnumber']
    else:
        return 'PRE001'


def ERP_customersave(api_sdk, option, dData, app3, rc, app2, src_table_name, ods_table_name):
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

            if i['FTAXREGISTERCODE'] == '':
                db.insertLog(app3,"ECS客户",i['FNumber'],"纳税登记号为空","2")
                continue

            i['FTAXREGISTERCODE'] = re.sub('[" "\?]','',i['FTAXREGISTERCODE'])
            i['FAccountNumber'] = re.sub('[" "\?]','',i['FAccountNumber'])
            i['FName'] = i['FName'].strip()

            if rc.getStatus(app3, i['FNumber'], ods_table_name) and  checkExist(app2,i['FName']) ==[]:
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
                        "FINVOICETITLE": i['FName'],
                        "FTAXREGISTERCODE": i['FTAXREGISTERCODE'],
                        "FINVOICEBANKNAME": i['FBankName'],
                        "FINVOICETEL": i['FINVOICETEL'],
                        "FINVOICEBANKACCOUNT": i['FAccountNumber'],
                        "FINVOICEADDRESS": i['FINVOICEADDRESS'],
                        "FSOCIALCRECODE": i['FTAXREGISTERCODE'],
                        "FIsGroup": False,
                        "FIsDefPayer": False,
                        "FSETTLETYPEID": {
                            "FNumber": "JSFS04_SYS"
                        },
                        "FCustTypeId": {
                            "FNumber": i['FCustTypeNo']
                        },
                        "FGroup": {
                            "FNumber": i['FGroupNo']
                        },
                        "FTRADINGCURRID": {
                            "FNumber": "PRE001" if i['FTRADINGCURRNO'] == '' else  get_FCurrencyNo(app2,i['FTRADINGCURRNO'])
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
                        "F_SZSP_Text": i['FNumber'],
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
                                "FACCOUNTNAME": i['FName'],
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
                sri = json.loads(savedResultInformation)

                if sri['Result']['ResponseStatus']['IsSuccess']:

                    submittedResultInformation = ERP_customersubmit(
                        sri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'], api_sdk)

                    subri = json.loads(submittedResultInformation)

                    if subri['Result']['ResponseStatus']['IsSuccess']:

                        auditResultInformation = ERP_audit('BD_Customer',
                                                           subri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'],
                                                           api_sdk)

                        auditres = json.loads(auditResultInformation)

                        if auditres['Result']['ResponseStatus']['IsSuccess']:

                            result = ERP_allocate('BD_Customer', getCodeByView('BD_Customer',
                                                                               auditres['Result']['ResponseStatus'][
                                                                                   'SuccessEntitys'][0]['Number'], api_sdk),
                                                  rc.getOrganizationCode(app2, i['FApplyOrgName']), api_sdk)

                            AlloctOperation('BD_Customer',
                                            auditres['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'], api_sdk, i,
                                            rc, app2,sri,app3)

                            rc.changeStatus(app3, "1", src_table_name, "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "1", ods_table_name, "FNumber", i['FNumber'])

                            db.insertLog(app3,"ECS客户",i['FNumber'],"数据同步完毕","1")

                        else:
                            db.insertLog(app3,"ECS客户",i['FNumber'],auditres,"2")
                            rc.changeStatus(app3, "2", src_table_name, "FNumber", i['FNumber'])
                            rc.changeStatus(app3, "2", ods_table_name, "FNumber", i['FNumber'])

                    else:
                        db.insertLog(app3,"ECS客户",i['FNumber'],subri,"2")
                        rc.changeStatus(app3, "2", src_table_name, "FNumber", i['FNumber'])
                        rc.changeStatus(app3, "2", ods_table_name, "FNumber", i['FNumber'])

                else:
                    db.insertLog(app3,"ECS客户",i['FNumber'],sri,"2")
                    rc.changeStatus(app3, "2", src_table_name, "FNumber", i['FNumber'])
                    rc.changeStatus(app3, "2", ods_table_name, "FNumber", i['FNumber'])

        except Exception as e:

            db.insertLog(app3, "ECS客户", i['FNumber'], "数据异常", "2")


    return "数据同步完毕"


def SaveAfterAllocation(api_sdk, i, rc, app2,sri,app3):
    FOrgNumber = rc.getOrganizationFNumber(app2, i['FApplyOrgName'])
    i['FNUMBER'] = sri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']
    model = {
        "Model": {
            "FCUSTID": queryDocuments(app2, sri['Result']['ResponseStatus']['SuccessEntitys'][0]['Number'], FOrgNumber['FORGID']),
            "FCreateOrgId": {
                "FNumber": "100"
            },
            "FUseOrgId": {
                "FNumber": str(FOrgNumber['FNUMBER'])
            },
            "FName": str(i['FName']),
            "FNUMBER":i['FNUMBER'],
            "FCOUNTRY": {
                "FNumber": "China"
            },
            "FTRADINGCURRID": {
                "FNumber": "PRE001" if i['FTRADINGCURRNO'] == '' else  get_FCurrencyNo(app2,i['FTRADINGCURRNO'])
            },
            "FSALDEPTID": {
                "FNumber": rc.getcode(app2, "FNUMBER", "rds_vw_department", "FNAME", i['FAalesDeptName'])
            },
            "FSALGROUPID": {
                "FNumber": "SKYX01"
            },
            "FSELLER": {
                "FNumber": rc.getcode(app2, "FNUMBER", "rds_vw_salesman", "FNAME", i['FSalesman'])
            },
            "FSETTLETYPEID": {
                "FNumber": i['FSETTLETYPENO']
            },
            "FRECCONDITIONID": {
                "FNumber": i['FRECCONDITIONNO']
            },
        }
    }
    res = api_sdk.Save("BD_Customer", model)
    save_res = json.loads(res)
    if save_res['Result']['ResponseStatus']['IsSuccess']:
        submit_res = ERP_customersubmit(i['FNumber'], api_sdk)
        audit_res=ERP_audit("BD_Customer",i['FNumber'],api_sdk)
    else:
        db.insertLog(app3,"ECS客户",i['FNumber'],"数据分配异常","2")



def ERP_CustomerCancelAllocate(forbid, PkIds, TOrgIds, api_sdk):
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


def ERP_CustomerUnAudit(number, api_sdk):
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

    res = api_sdk.UnAudit("BD_Customer", data)

    return res


def ERP_CustomerDelete(number, api_sdk):
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
    res = api_sdk.Delete("BD_Customer", data)

    return res


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


def AlloctOperation(forbid, number, api_sdk, i, rc, app2,sri,app3):
    '''
    数据分配后进行提交审核
    :param forbid:
    :param number:
    :param api_sdk:
    :return:
    '''

    SaveAfterAllocation(api_sdk, i, rc, app2,sri,app3)


def judgeDate(FNumber, api_sdk):
    '''
    查看数据是否在ERP系统存在
    :param FNumber: 客户编码
    :param api_sdk:
    :return:
    '''

    data = {
        "CreateOrgId": 0,
        "Number": FNumber,
        "Id": "",
        "IsSortBySeq": "false"
    }

    res = json.loads(api_sdk.View("BD_Customer", data))

    return res['Result']['ResponseStatus']['IsSuccess']


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


