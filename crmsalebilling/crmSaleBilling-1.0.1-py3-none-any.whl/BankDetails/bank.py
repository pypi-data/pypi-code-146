import json
import requests
from requests import *
from urllib import parse
from pyrda.dbms.rds import RdClient


def casPost(url, data):
    '''
    post data to cas server
    :param url: url paramer partially
    :param data: data
    :return:
    '''
    par = {}
    par["params"] = data
    text = parse.urlencode(par)
    r = post(url, params=text)
    print(r.url)
    res = r.json()
    return (res)


def bankCode_insert(ledgerBankCode, bankName, bankCode, ownerName, dms_token):
    sql = " insert into RDS_CAS_SRC_md_BankCode values('" + ledgerBankCode + "','" + bankName + "','" + bankCode + "','" + ownerName + "')"
    app = RdClient(token=dms_token)
    res = app.insert(sql)
    return (res)


# 3 基础代码接口
class BankAccount:
    def __init__(self, baseUrl, orgCode,
                 secretKey):
        '''
        intial the BankAccount class
        :param baseUrl: base url from cas
        :param orgCode: organization code
        :param secretKey: key for orgcode
        '''
        self.baseUrl = baseUrl
        self.orgCode = orgCode
        self.secretKey = secretKey

    # 3.1、联行号查询
    def bankCodeQuery(self, bankCode=''):
        '''
        query all the ledger bank code under one bank.
        :param bankCode: bankCode such as BOC
        :return:
        '''
        self.bankCode = bankCode
        entry = "app/basequery/queryLedgerBankCode.html"
        api = self.baseUrl + entry
        data = {'orgCode': self.orgCode,
                "secretKey": self.secretKey,
                "bankCode": self.bankCode}
        res = casPost(api, data)
        return (res)

    # 3.2、单个联行号查询
    def onebankCodeQuery(self, ledgerBankCode='', bankName=''):
        '''
        query the specific bankCode.
        :param ledgerBankCode:  1st param
        :param bankName: 2nd param.
        :return:
        '''
        self.ledgerBankCode = ledgerBankCode
        self.bankName = bankName
        entry = "app/basequery/queryLedgerBankCode.html"
        api = self.baseUrl + entry
        data = {'orgCode': self.orgCode,
                "secretKey": self.secretKey,
                "ledgerBankCode": self.ledgerBankCode,
                "bankName": self.bankName
                }
        res = casPost(api, data)
        return (res)

    # 3.3、审批流参数信息查询
    def WorkflowInfoQuery(self):
        entry = "app/basequery/queryWorkflowInfo.html"
        api = self.baseUrl + entry
        data = {'orgCode': self.orgCode,
                "secretKey": self.secretKey}
        res = casPost(api, data)
        return (res)


# 4 转帐支付接口
class bankTransfers:
    def __init__(self, baseUrl, orgCode, secretKey):
        self.baseUrl = baseUrl
        self.orgCode = orgCode
        self.secretKey = secretKey

    # 4.1 发起单笔人民币转帐支付
    def bankTransfersQuery(self, clientNo='', recBankAccNo='', payBankAccNo='', receiveBankCode='', ledgerBankCode='',
                           receiveAccName='',
                           accType='', use='', amount='', remark='', crashFlag=''):
        self.clientNo = clientNo
        self.recBankAccNo = recBankAccNo
        self.payBankAccNo = payBankAccNo
        self.receiveBankCode = receiveBankCode
        self.ledgerBankCode = ledgerBankCode
        self.receiveAccName = receiveAccName
        self.accType = accType
        self.use = use
        self.amount = amount
        self.remark = remark
        self.crashFlag = crashFlag
        entry = "app/pay/bankTransfers.html"
        api = self.baseUrl + entry
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "clientNo": self.clientNo,
                "recBankAccNo": self.recBankAccNo,
                "payBankAccNo": self.payBankAccNo,
                "receiveBankCode": self.receiveBankCode,
                "ledgerBankCode": self.ledgerBankCode,
                "receiveAccName": self.receiveAccName,
                "accType": self.accType,
                "use": self.use,
                "amount": self.amount,
                "remark": self.remark,
                "crashFlag": self.crashFlag
                }
        res = casPost(api, data)
        return (res)

    # 4.2、发起批量人民币转帐支付(支持单笔)
    def batchBankTransfersQuery(self, isNeedCheck='', clientNo='', operatorType='', operator='',
                                workflowKey='', isSubmit='', dataFrom='', transferData=''):
        entry = "app/pay/batchBankTransfers.html"
        api = self.baseUrl + entry
        self.isNeedCheck = isNeedCheck
        self.clientNo = clientNo
        self.operatorType = operatorType
        self.operator = operator
        self.workflowKey = workflowKey
        self.isSubmit = isSubmit
        self.dataFrom = dataFrom
        self.transferData = transferData
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "isNeedCheck": self.isNeedCheck,
                "clientNo": self.clientNo,
                "operatorType": self.operatorType,
                "operator": self.operator,
                "workflowKey": self.workflowKey,
                "isSubmit": self.isSubmit,
                "dataFrom": self.dataFrom,
                "transferData": self.transferData
                }
        res = casPost(api, data)
        print(self.transferData)
        print(data)
        return (res)

    # 4.3、发起工资报销支付（人民币）
    def bexecuteSalarysQuery(self, payAccNo='', clientNo='', isNeedCheck='', operator='', workflowKey='', isSubmit='',
                             bizType='02', pUse='', dataFrom='', transferData=''):
        entry = "app/pay/executeSalarys.html"
        api = self.baseUrl + entry
        self.payAccNo = payAccNo
        self.clientNo = clientNo
        self.isNeedCheck = isNeedCheck
        self.operator = operator
        self.workflowKey = workflowKey
        self.isSubmit = isSubmit
        self.bizType = bizType
        self.pUse = pUse
        self.dataFrom = dataFrom
        self.transferData = transferData
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "payAccNo": self.payAccNo,
                "clientNo": self.clientNo,
                "isNeedCheck": self.isNeedCheck,
                "operator": self.operator,
                "workflowKey": self.workflowKey,
                "isSubmit": self.isSubmit,
                "bizType": self.bizType,
                "pUse": self.pUse,
                "dataFrom": self.dataFrom,
                "transferData": self.transferData
                }
        print(self.transferData)
        print(data)
        res = casPost(api, data)

        return (res)

    # 4.4、转账结果查询（人民币）
    def TransfersResQuery(self, serialNos='', bizIds=''):
        entry = "app/basequery/queryTransfersRes.html"
        api = self.baseUrl + entry
        self.serialNos = serialNos
        self.bizIds = bizIds
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "serialNos": self.serialNos,
                "bizIds": self.bizIds,
                }
        res = casPost(api, data)
        return (res)


# 5 账户查询接口
class Payment:
    def __init__(self, baseUrl, orgCode, secretKey):
        self.baseUrl = baseUrl
        self.orgCode = orgCode
        self.secretKey = secretKey

    # 5.1、帐户明细查询（根据交易时间查询）
    def PaymentDetailQuery(self, startDate='', endDate='', accountNo='', tradeType=''):
        entry = "app/basequery/queryPyamentDetail.html"
        api = self.baseUrl + entry
        self.startDate = startDate
        self.endDate = endDate
        self.accountNo = accountNo
        self.tradeType = tradeType
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "startDate": self.startDate,
                "endDate": self.endDate,
                "accountNo": self.accountNo,
                "tradeType": self.tradeType,
                }
        res = casPost(api, data)
        return (res)

    # 5.2、帐户明细查询（根据入库时间查询）
    def PaymentDetailCreateQuery(self, startDate='', endDate='', accountNo='', activePay='', tradeType=''):
        entry = "app/basequery/queryPyamentDetailCreate.html"
        api = self.baseUrl + entry
        self.startDate = startDate
        self.endDate = endDate
        self.accountNo = accountNo
        self.activePay = activePay
        self.tradeType = tradeType
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "startDate": self.startDate,
                "endDate": self.endDate,
                "accountNo": self.accountNo,
                "activePay": self.activePay,
                "tradeType": self.tradeType,
                }
        res = casPost(api, data)
        print(data)
        return (res)

    # 5.3、帐户余额查询
    def AccBalanceQuery(self, accountNo=''):
        entry = "app/basequery/queryAccBalance.html"
        api = self.baseUrl + entry
        self.accountNo = accountNo
        data = {"orgCode": self.orgCode,
                "secretKey": self.secretKey,
                "accountNo": self.accountNo,
                }
        r = casPost(api, data)
        # print(r)
        res = {}
        res['companyName'] = r['data']['accountName']
        res['accountNo'] = r['data']['accountNo']
        res['balanceDate'] = r['data']['balanceDate']
        res['balance'] = r['data']['balance']
        res['currencyCode'] = r['data']['currencyCode']
        res['createTime'] = r['data']['createTime']
        return (res)
