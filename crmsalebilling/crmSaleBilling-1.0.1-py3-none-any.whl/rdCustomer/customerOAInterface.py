# from tkinter import NW
# !/usr/bin/python
# -*- coding:UTF-8 -*-
import rdCustomer.Utility as rc
import rdCustomer.DatabaseOperations as op
import rdCustomer.Metadata as rm

from pyrda.dbms.rds import RdClient
from time import sleep
from k3cloud_webapi_sdk.main import K3CloudApiSdk


def customerInterface(option1, FVarDateTime, token_erp, token_china):
    app3 = RdClient(token=token_erp)
    app2 = RdClient(token=token_china)
    OADataList = rc.getOAListW(FVarDateTime)

    if OADataList == []:
        pass
    else:
        for i in OADataList:
            if rc.ListDateIsExist(app2, "RDS_OA_SRC_bd_CustomerList", "FCustomerName", i['mainTable']['FName2052'],
                                  "FStartDate", i['mainTable']['FVarDateTime']) and i['mainTable']['FStatus'] == '已审核':
                sql1 = f"insert into RDS_OA_SRC_bd_CustomerList(FInterId,FStartDate,FEndDate,FApplyOrgName,FcustomerName,FUploadDate,FIsdo) values({rc.getFinterId(app2, 'RDS_OA_SRC_bd_CustomerList') + 1},'{i['mainTable']['FVarDateTime']}',getdate(),'{i['mainTable']['FUseOrgIdName']}','{i['mainTable']['FName2052']}',getdate(),0)"
                op.insertData(app2, sql1)

        sql2 = "select FCustomerName,FStartDate,FEndDate from RDS_OA_ODS_bd_CustomerList where FIsdo = 0"
        res = op.getData(app2, sql2)

        for k in res:
            d = rc.getOADetailDataW('FName2052', k['FCustomerName'], 'FVarDateTime', k['FEndDate'])
            if d != []:

                if rc.DetailDateIsExist(app2, "FNumber", d[0]['mainTable']['FNameId'], "RDS_OA_ODS_bd_CustomerDetail"):
                    sql3 = f"insert into RDS_OA_SRC_bd_CustomerDetail(FInterId,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCOUNTRY,FPROVINCIAL,FTEL,FINVOICETITLE,FTAXREGISTERCODE,FBankName,FINVOICETEL,FAccountNumber,FINVOICEADDRESS,FINVOICETYPE,FTaxRate,FCONTACT,FBizAddress,FMOBILE,FSalesman,FAalesDeptName,FCustTypeNo,FGroupNo,F_SZSP_KHFLNo,FSalesGroupNo,FTRADINGCURRNO,FSETTLETYPENO,FRECCONDITIONNO,FPRICELISTNO,FUploadDate,FIsdo,F_SZSP_Text,F_SZSP_KHZYJBNo,F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo) values({rc.getFinterId(app2, 'RDS_OA_SRC_bd_CustomerDetail') + 1},'{d[0]['mainTable']['FUseOrgIdName']}','{d[0]['mainTable']['FDeptId']}','{d[0]['mainTable']['FUserId']}','{d[0]['mainTable']['FVarDateTime']}','{d[0]['mainTable']['FNameId']}','{d[0]['mainTable']['FName2052']}','{d[0]['mainTable']['FShortName2052']}','{d[0]['mainTable']['FCOUNTRYName']}','{d[0]['mainTable']['FPROVINCIALName']}','{d[0]['mainTable']['FTEL']}','{d[0]['mainTable']['FINVOICETITLE']}','{d[0]['mainTable']['FTAXREGISTERCODE']}','{d[0]['mainTable']['FINVOICEBANKNAME']}','{d[0]['mainTable']['FINVOICETEL']}','{d[0]['mainTable']['FINVOICEBANKACCOUNT']}','{d[0]['mainTable']['FINVOICEADDRESS']}','{d[0]['mainTable']['FInvoiceType']}','{d[0]['mainTable']['FTaxRateName']}','{d[0]['mainTable']['FContactIdName']}','{d[0]['mainTable']['FADDRESS1']}','{d[0]['mainTable']['FMOBILE']}','{d[0]['mainTable']['FSELLERName1']}','{d[0]['mainTable']['FSALDEPTIDDeptId']}','{d[0]['mainTable']['FCustTypeNo']}','{d[0]['mainTable']['FGroupNo']}','{d[0]['mainTable']['F_SZSP_KHFLNo']}','{d[0]['mainTable']['FSalesGroupNo']}','{d[0]['mainTable']['FTRADINGCURRNO']}','{d[0]['mainTable']['FSETTLETYPENO']}','{d[0]['mainTable']['FRECCONDITIONNO']}','{d[0]['mainTable']['FPRICELISTNO']}',getdate(),0,'{d[0]['mainTable']['F_SZSP_Text']}','{d[0]['mainTable']['F_SZSP_KHZYJBNo']}','{d[0]['mainTable']['F_SZSP_KHGHSXNo']}','{d[0]['mainTable']['F_SZSP_XSMSNo']}','{d[0]['mainTable']['F_SZSP_XSMSSXNo']}')"

                    op.insertData(app2, sql3)
                    print(f"{d[0]['mainTable']['FNameId']}保存到SRC,5分钟后同步到ODS")

                    rc.changeStatus(app2, "1", 'RDS_OA_ODS_bd_CustomerList', "FCustomerName",
                                    (d[0]['mainTable'])['FName2052'])
                else:
                    rc.changeStatus(app2, "2", 'RDS_OA_ODS_bd_CustomerList', "FCustomerName", k['FCustomerName'])
                    print(f"编码{d[0]['mainTable']['FNameId']}已存在于数据库，请手动录入")
            else:
                print(f"该客户不在今日审批中{k['FCustomerName']}")
                rc.changeStatus(app2, "2", 'RDS_OA_ODS_bd_CustomerList', "FCustomerName", k['FCustomerName'])

        sql4 = "select FInterId,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCOUNTRY,FPROVINCIAL,FTEL,FINVOICETITLE,FTAXREGISTERCODE,FBankName,FINVOICETEL,FAccountNumber,FINVOICEADDRESS,FINVOICETYPE,FTaxRate,FCONTACT,FBizAddress,FMOBILE,FSalesman,FAalesDeptName,FCustTypeNo,FGroupNo,F_SZSP_KHFLNo,FSalesGroupNo,FTRADINGCURRNO,FSETTLETYPENO,FRECCONDITIONNO,FPRICELISTNO,FUploadDate,FIsdo,F_SZSP_Text,F_SZSP_KHZYJBNo,F_SZSP_KHGHSXNo,F_SZSP_XSMSNo,F_SZSP_XSMSSXNo,F_SZSP_BLOCNAME from RDS_OA_ODS_bd_CustomerDetail where FIsdo = 0"
        # sleep(30)
        result = op.getData(app2, sql4)
        print(result)

        api_sdk = K3CloudApiSdk()

        print("开始保存数据")
        rm.ERP_customersave(api_sdk, option1, result, app3, rc, app2)
