# from tkinter import NW
# !/usr/bin/python
# -*- coding:UTF-8 -*-
import rdSupplier.Utility as auxiliary
import rdSupplier.DatabaseOperations as rdo
import rdSupplier.Metadata as rm
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient


def insert_into_listSource(data, app3):
    '''
    将数据插入source
    :param FVarDateTime:
    :return:
    '''

    for i in data:

        if i['mainTable']['FStatus'] == '已审核':

            if auxiliary.ListDateIsExist(app3, "RDS_OA_SRC_bd_SupplierList", "FSupplierName", i['mainTable']['FName'],
                                         "FStartDate", i['mainTable']['FVarDateTime']):
                sql = f"insert into RDS_OA_SRC_bd_SupplierList(FInterId,FStartDate,FEndDate,FApplyOrgName,FSupplierName,FUploadDate,Fisdo ) values({str(auxiliary.getFinterId(app3, 'RDS_OA_SRC_bd_SupplierList') + 1)},'{(i['mainTable'])['FVarDateTime']}',getdate(),'{(i['mainTable'])['FUseOrg']}','{(i['mainTable'])['FName']}',getdate(),0)"

                rdo.insertData(app3, sql)


def insert_into_ERP(erp_token, data, app2, app3):
    '''
    将数据插入到ERP系统
    :param erp_token:
    :param data:
    :param app2:
    :param app3:
    :return:
    '''

    api_sdk = K3CloudApiSdk()

    rm.ERP_suppliersave(api_sdk, erp_token, data, app2, auxiliary, app3)


def judgeDetailData(erp_token, app2, app3):
    '''
    判断RDS_OA_ODS_bd_SupplierDetail表中是否有数据
    :param app3:
    :return:
    '''

    sql = "select FInterId ,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCountry,FZipCode,FUniversalCode,FRegisterAddress,FMngrDeptName,FMngrMan,FSullierType,FInvoiceType,FTaxRate,FAccountNumber,FAccountName ,FBankTransferCode,FBankName,FBankAddr,FContact,FMobile,FEMail, FSupplierCategoryNo,FSupplierGradeNo ,FPriceListNo,FSettleCurrencyNo,FSettlementMethodNo,FPaymentConditionNo,FCurrencyNo,FUploadDate,Fisdo from RDS_OA_ODS_bd_SupplierDetail where Fisdo=0"

    res = app3.select(sql)

    if res != []:

        insert_into_ERP(erp_token=erp_token, data=res, app2=app2, app3=app3)

    else:

        pass


def insert_into_detailSource(app3, data):
    '''
    将明细信息插入RDS_OA_SRC_bd_SupplierDetail表
    :param app3:
    :param data:
    :return:
    '''

    for i in data:

        d = auxiliary.getOADetailDataW(str(i['FSupplierName']), str(i['FEndDate']))

        if d != []:
            try:

                if auxiliary.DetailDateIsExist(app3, "FNumber", d[0]['mainTable']['FNumber'],
                                               "RDS_OA_SRC_bd_SupplierDetail"):
                    sql3 = f"insert into RDS_OA_SRC_bd_SupplierDetail(FInterId ,FApplyOrgName,FApplyDeptName,FApplierName,FDate,FNumber,FName,FShortName,FCountry,FZipCode,FUniversalCode,FRegisterAddress,FMngrDeptName,FMngrMan,FSullierType,FInvoiceType,FTaxRate,FAccountNumber,FAccountName ,FBankTransferCode,FBankName,FBankAddr,FContact,FMobile,FEMail, FSupplierCategoryNo,FSupplierGradeNo ,FPriceListNo,FSettleCurrencyNo,FSettlementMethodNo,FPaymentConditionNo,FCurrencyNo,FUploadDate,Fisdo ) values({str(auxiliary.getFinterId(app3, 'RDS_OA_SRC_bd_SupplierDetail') + 1)},'{(d[0]['mainTable'])['FUseOrg']}','{(d[0]['mainTable'])['FDeptId1']}','{(d[0]['mainTable'])['FUserId']}','{(d[0]['mainTable'])['FVarDateTime']}','{(d[0]['mainTable'])['FNumber']}','{(d[0]['mainTable'])['FName']}','{(d[0]['mainTable'])['FShortName']}','{(d[0]['mainTable'])['FCountry']}','{(d[0]['mainTable'])['FZip']}','{(d[0]['mainTable'])['FSOCIALCRECODE']}','{(d[0]['mainTable'])['FRegisterAddress']}','{(d[0]['mainTable'])['FDeptId']}','{(d[0]['mainTable'])['FStaffId']}','{(d[0]['mainTable'])['FSupplyClassify']}','{(d[0]['mainTable'])['FInvoiceType']}','{(d[0]['mainTable'])['FTaxRateName']}','{(d[0]['mainTable'])['FBankCode']}','{(d[0]['mainTable'])['FBankHolder']}','{(d[0]['mainTable'])['FCNAPS']}','{(d[0]['mainTable'])['FOpenBankName']}','{(d[0]['mainTable'])['FOpenAddressRec']}','{(d[0]['mainTable'])['FContact']}','{(d[0]['mainTable'])['FMobile']}','{(d[0]['mainTable'])['FEMail']}','{(d[0]['mainTable'])['FSupplierClassifyNo']}','{(d[0]['mainTable'])['FSupplierGradeNo']}','{(d[0]['mainTable'])['FPRICELISTNO']}','{(d[0]['mainTable'])['FPayCurrencyNo']}','{(d[0]['mainTable'])['FSettlementNo']}','{(d[0]['mainTable'])['FPayConditionNo']}','{(d[0]['mainTable'])['FBankCurrencyNo']}',getdate(),0)"

                    rdo.insertData(app3, sql3)

                    auxiliary.changeStatus(app3, "1", 'RDS_OA_ODS_bd_SupplierList', "FSupplierName",
                                           (d[0]['mainTable'])['FName'])
                    print(f"该编码{d[0]['mainTable']['FNumber']}已保存到SRC中")

                else:
                    print(f"该编码{d[0]['mainTable']['FNumber']}已存在于数据库")
                    auxiliary.changeStatus(app3, "2", 'RDS_OA_SRC_bd_SupplierDetail', "FNumber", d[0]['mainTable']['FNumber'])
            except:
                auxiliary.changeStatus(app3, "2", 'RDS_OA_ODS_bd_SupplierList', "FSupplierName", i['FSupplierName'])
        else:
            print(f"该公司名称{i['FSupplierName']}不在今日审批中")
            auxiliary.changeStatus(app3, "2", 'RDS_OA_ODS_bd_SupplierList', "FSupplierName", i['FSupplierName'])


def judgeListData(app3):
    '''
    判断RDS_OA_ODS_bd_SupplierList表中是否有新增的数据
    :param app3:
    :return:
    '''

    sql = "select FSupplierName,FStartDate,FEndDate from RDS_OA_ODS_bd_SupplierList where Fisdo=0"

    res = app3.select(sql)

    if res != []:

        insert_into_detailSource(app3, res)

    else:

        pass


def judgeOAData(FVarDateTime, app3):
    '''
    将数据插入source
    :param FVarDateTime:
    :return:
    '''

    OADataList = auxiliary.getOAListW(FVarDateTime)

    # for i in OADataList:
    #     print(i)

    if OADataList != []:

        insert_into_listSource(OADataList, app3)

    else:

        pass


def supplierInterface(option1, FVarDateTime, erp_token, china_token):
    '''
    功能入口函数
    :param option1: ERP用户信息
    :param FVarDateTime: 日期
    :param token:  操作数据库底层包token
    :return:
    '''
    app2 = RdClient(token=erp_token)
    app3 = RdClient(token=china_token)

    judgeOAData(FVarDateTime, app3)

    judgeListData(app3)

    judgeDetailData(option1, app2, app3)
