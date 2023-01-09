import logging
from . import utils
from . import restClient as client
from . import query
import re,simplejson

apiVersion = 'v51.0'

#X can be an Id or the field value. If it is an Id, it is returned. If not, X it the value of the 'field'. 

def getFieldList(objs,name):
    """
    From and array of objects, return an array of field by name. Return a column. 
    """
    return [obj[name] for obj in objs]


def Id(obj):
    if type(obj) is str:
        return obj
    if type(obj) is dict:
        if 'Id' in obj:
            id = obj['Id']
        if 'id' in obj:
            id = obj['id']
        if 'value' in id:
            id = id['value']
        return id

def checkId(id):
    #return re.search(r"[a-zA-Z0-9]{15}|[a-zA-Z0-9]{18}", id)
    return re.search(r"\b[a-z0-9]\w{4}0\w{12}|[a-z0-9]\w{4}0\w{9}\b", id)


def isId(sobjectType,X):
    if X == None:
        return False
    if type(X) is dict:
        return isId(utils.Id(X))
    if sobjectType.lower() == str(getSObjectType(X)).lower():
        return True   
    return False

#---------------------------------
def getSObjectType(id):
    if checkId(id) == None:
        return None
    if id.startswith("a3O"):
        return "vlocity_cmt__PriceList__c"
    if id.startswith("01s"):
        return "Pricebook2"
    if id.startswith("01t"):
        return "product2"
    if id.startswith("a3P"):
        return "vlocity_cmt__PricingElement__c"
    if id.startswith("a4d"):
        return "vlocity_cmt__PricingElement__c"
    if id.startswith("a36"):
        return "vlocity_cmt__Promotion__c"
    if id.startswith("a3S"):
        return "vlocity_cmt__PromotionItem__c"
    if id.startswith("a3i"):
        return "vlocity_cmt__PriceListEntry__c"
    if id.startswith("a3R"):
        return "vlocity_cmt__PricingVariable__c"
    if id.startswith("a4h"):
        return "vlocity_cmt__PricingVariable__c"
    if id.startswith("a1b"):
        return "vlocity_cmt__ProductChildItem__c"
    if id.startswith("a2S"):
        return "vlocity_cmt__ObjectClass__c"
    if id.startswith("a4M"):
        return "vlocity_cmt__PricingPlan__c"
    if id.startswith("a3T"):
        return "vlocity_cmt__TimePlan__c"
    if id.startswith("a3l"):
        return "vlocity_cmt__TimePolicy__c"
    if id.startswith("001"):
        return "Account"     
    if id.startswith("801"):
        return "Order"    
    if id.startswith("802"):
        return "OrderItem"    
    if id.startswith("02i"):
        return "Asset"    
    if id.startswith("01s"):
        return "Pricebook2" 
    if id.startswith("a0I"):
        return "vlocity_cmt__AttributeCategory__c" 
    if id.startswith("a1B"):
        return "vlocity_cmt__AttributeCategory__c" 
    if id.startswith("a1W"):
        return "vlocity_cmt__Picklist__c" 
    if id.startswith("a4W"):
        return "vlocity_cmt__Picklist__c" 
    if id.startswith("a2m"):
        return "vlocity_cmt__PriceList__c" 
    if id.startswith("a4a"):
        return "vlocity_cmt__PriceList__c" 
    if id.startswith("a2j"):
        return "vlocity_cmt__PicklistValue__c"      
    if id.startswith("a3I"):
        return "vlocity_cmt__ContextDimension__c" 
    if id.startswith("a3b"):
        return "vlocity_cmt__ContextMapping__c" 
    if id.startswith("a3r"):
        return "vlocity_cmt__ContextScope__c" 
    if id.startswith("a3q"):
        return "vlocity_cmt__ContextAction__c" 
    if id.startswith("a0w"):
        return "vlocity_cmt__EntityFilter__c"   
    if id.startswith("a1o"):
        return "vlocity_cmt__Rule__c"        
    if id.startswith("a1l"):
        return "vlocity_cmt__RuleFilter__c"        
    if id.startswith("a41"):
        return "vlocity_cmt__RuleAssignment__c"        
    if id.startswith("a4x"):
        return "vlocity_cmt__OfferMigrationPlan__c"         
    if id.startswith("a4"):
        return "vlocity_cmt__OfferMigrationComponentMapping__c"       
    if id.startswith("005"):
        return "User"   
    if id.startswith("a2H"):
        return "vlocity_cmt__Catalog__c"   
    if id.startswith("a1j"):
        return "vlocity_cmt__Catalog__c"  
    if id.startswith("a04"):
        return "vlocity_cmt__CatalogProductRelationship__c"   
    if id.startswith("a5b"):
        return "vlocity_cmt__ServicePoint__c"        

    print(f" getObjectType--> {id} no related to object")
    return None
#---------------------------------

def get(id,sobjectName=None):
    if sobjectName == None:
        sobjectName = getSObjectType(id)
    # return select_wherexx_field_value_n(objectName,'Id',id)
    return query.query(f" select fields(all) from {sobjectName} where Id='{id}' limit 200")

#---------------------------------

def create(sobjectname,object):
    call =  client.callAPI(f'/services/data/{apiVersion}/sobjects/{sobjectname}/', method="post", data=object) 
    if client.lastThreadCall()['status_code'] == 201:
        logging.info(f"Object {sobjectname} created sucesfully. Id:{call['id']}")
    else:
        logging.warning(f"Object {sobjectname} creation returned status code {client.lastThreadCall()['status_code']}")
        logging.warning(f"Response {call}")

        raise ValueError(simplejson.dumps(call, indent=4))


    return call

def checkError():
    lc = client.lastThreadCall()
    if lc['status_code'] >= 400:
        logging.error(f"Error in call.  statusCode->{client.lastThreadCall()['status_code']}")
        message = {
            'error':lc['error'],
            'errorCode':lc['errorCode']
        }
        if 'errorOther' in lc:
            message['errorOther'] = lc['errorOther']
        msg = simplejson.dumps(message, indent=4)
        logging.error(msg)
        raise ValueError(msg)

def update(id,data,sobjectname=None,getObject=True):
    if sobjectname == None:
        sobjectname = getSObjectType(id)
    
    call = client.callAPI(f'/services/data/v51.0/sobjects/{sobjectname}/{id}/',method='patch',data=data)
    checkError()
    if getObject == True:
        call = get(id)
    return call

def checkError():
    lc = client.lastCall()

    if 'error' in lc and lc['error'] != None and len(lc['error'])>10:
        if 'response' in lc:
            if 'serverResponse:' in lc['response']:
                s = '{"a":' + lc['response'].split('serverResponse:')[-1] + "}"
                obj = simplejson.loads(s)
                utils.raiseException(obj['a'][0]['errorCode'],obj['a'][0]['message'])
        utils.raiseException(lc['errorCode'],lc['error'])

def delete(sobjectname,id):
    if id==None:
        return None
    if type(id) is list:
        idList = ",".join(id)
        logging.debug(f"deleting {sobjectname} with Id {idList}")
        return client.callAPI(f'/services/data/{apiVersion}/composite/sobjects?ids={idList}', method="delete")
    id = Id(id)
   
    logging.debug(f"deleting {sobjectname} with Id {id}")
    call =  client.callAPI(f'/services/data/{apiVersion}/sobjects/{sobjectname}/{id}', method="delete")
    checkError()
    return call

def listObjects():
    return client.callAPI(f'/services/data/{apiVersion}/sobjects/')['sobjects']

def describe(sobjectName):
    return client.callAPI(f'/services/data/{apiVersion}/sobjects/{sobjectName}/describe')

def listVersions():
    return client.callAPI(f'/services/data')

def recordCount(objectsCommaSeparated):
    return client.callAPI(f'/services/data/{apiVersion}/limits/recordCount?sObjects={objectsCommaSeparated}')

def getOwner(Id):
    recordType = getSObjectType(Id)
    if recordType == None:
        return

    select = f"select OwnerId from {recordType} where Id = '{Id}' limit 50"    
    call = query.query(select)
    OwnerId = call['records'][0]['OwnerId']

    select = f"select FIELDS(ALL) from user where Id = '{OwnerId}' limit 50"    
    user = query.query(select)['records'][0]

    print(user['Name'])

    return call

def getNumOwnedRecords(sobject,ownerId):
    try:
        select = f"select COUNT() from {sobject} where OwnerId = '{ownerId}' "    
        call = query.query(select)

        totalSize = call['totalSize']

        return totalSize

    except Exception as e:
        if 'INVALID_FIELD' in f"{e}":
            return -1
    
    return -2

def getNumOwnedRecords_4_ObjectList(sobjectNameList,ownerId):
    result=[]
    for obj in sobjectNameList:
        res = {
            "object":obj,
            "ownedRecords":getNumOwnedRecords(obj,ownerId)
        }
        result.append(res)

    return result

def selectOwnedRecords(sobjName,ownerId):
    select = f"select Fields(ALL) from {sobjName} where ownerId='{ownerId}'limit 50"
    call = query.query(select)

    return call
