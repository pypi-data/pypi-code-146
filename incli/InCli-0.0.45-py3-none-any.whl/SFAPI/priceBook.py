from . import query

def pricebookId(pricelistName,field='Name'):
    pb2Id = query.queryField(f" select vlocity_cmt__Pricebook2Id__c from vlocity_cmt__PriceList__c where {field} = '{pricelistName}' ")

    return pb2Id

def pricebookEntryId(pricebook2Id,productCode):
    pricebookEntryId = query.queryField(f" select Id from PricebookEntry where ProductCode='{productCode}' and Pricebook2Id = '{pricebook2Id}' ")

    return pricebookEntryId

def pricebookEntryId_pl(pricelistName,productCode,pricelistField='Name'):
    pb2Id = pricebookId(pricelistName,field=pricelistField)
    pbeId = pricebookEntryId(pb2Id,productCode)
    return pbeId



