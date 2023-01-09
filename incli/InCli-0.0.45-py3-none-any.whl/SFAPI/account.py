from . import Sobjects,query,utils
import logging

#if the account does not exist, accountX will be used as the account name. 
def createAccount_Id(accountF,fields=None,recordTypeName=None,checkExists=True):

    ef = utils.extendedField(accountF)
    if checkExists == True:
        accountId = query.queryField(f" select Id from Account where {ef['field']}='{ef['value']}' ")
        if accountId != None:
            logging.info(f'Returning existing Account <{accountId}> ')
            return accountId
            
    acc={
        'Name': ef['value'],
        'vlocity_cmt__Active__c':'Yes',
        'vlocity_cmt__Status__c':'Active'
    }
    if fields!= None:
        acc.update(fields)

    if recordTypeName!=None:
        acc['RecordTypeId'] = query.queryField(f"select Id from RecordType where SobjectType='Account' and Name = '{recordTypeName}'")

    call = Sobjects.create('Account',acc)

    accountId = call['id']
    logging.info(f"Account {ef['value']} Created Account <{accountId}> ")

    return accountId

def createAccount(accountF,fields=None,recordTypeName=None,checkExists=True):
    accountId = createAccount_Id(accountF,fields=fields,recordTypeName=recordTypeName,checkExists=checkExists)
    account = Sobjects.get(accountId)

    return account['records'][0]

def getAccount(accountF):
    ef = utils.extendedField(accountF)
    return query.query(f" select fields(all) from Account where {ef['field']}='{ef['value']}' limit 100")

def deleteAccount(accountF):
    ef = utils.extendedField(accountF)

    ids = query.queryFieldList(f" select Id from Account where {ef['field']}='{ef['value']}' ")
    return Sobjects.delete('Account',ids)

def deleteAccountOrders(accountId):
    ids = query.queryField(f" select Id from Order where  AccountId = '{accountId}' ")
    return Sobjects.delete('Account',ids)
