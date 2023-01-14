# from tkinter import NW
# !/usr/bin/python
# -*- coding:UTF-8 -*-
import datetime

from crmCustomer import Utility as rc
from crmCustomer import DatabaseOperations as op
from crmCustomer import Metadata as rm

from pyrda.dbms.rds import RdClient
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from crmCustomer.src_crm_customer import CrmToDms


def customerInterface(option1, token_erp, token_china):
    app3 = RdClient(token=token_erp)
    app2 = RdClient(token=token_china)
    c = CrmToDms()
    FDate = str(datetime.datetime.now())[:10]
    c.crm_customer(app2, app3, FDate)
    sql4 = "select FInterId,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCOUNTRY,FPROVINCIAL," \
           "FTEL,FINVOICETITLE,FTAXREGISTERCODE,FBankName,FINVOICETEL,FAccountNumber,FINVOICEADDRESS,FINVOICETYPE,FTaxRate," \
           "FCONTACT,FBizAddress,FMOBILE,FSalesman,FAalesDeptName,FCustTypeNo,FGroupNo,F_SZSP_KHFLNo,FSalesGroupNo,FTRADINGCURRNO," \
           "FSETTLETYPENO,FRECCONDITIONNO,FPRICELISTNO,FUploadDate,FIsdo,F_SZSP_Text,F_SZSP_KHZYJBNo,F_SZSP_KHGHSXNo,F_SZSP_XSMSNo," \
           "F_SZSP_XSMSSXNo,F_SZSP_BLOCNAME from RDS_CRM_SRC_Customer where FIsdo = 0"
    # sleep(30)
    result = op.getData(app2, sql4)
    print(result)

    api_sdk = K3CloudApiSdk()

    print("开始保存数据")
    res = rm.ERP_customersave(api_sdk, option1, result, app3, rc, app2)
    return res