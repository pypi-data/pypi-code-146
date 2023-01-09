import logging, copy
from . import Sobjects, objectUtil, priceBook, query, utils,restClient
from datetime import date
import simplejson 


_carts = []
def _get(Id):
    for cart in _carts:
        if cart['Id'] == Id:
            return cart
def _set(Id,name,pricelistId,accountId):
    global _carts
    _carts.append({
        'Id':Id,
        'name':name,
        'plId':pricelistId,
        'accId':accountId
    })
#------------------------------------------------------------------------

def stringify(parameters,exclude,initSeparator='?'):
  isFirst = True

  ret = ''
  for name in parameters:
    if name in exclude:
      continue
    if(parameters[name] == None):
      continue
    separator = initSeparator if isFirst == True else '&'
    value = parameters[name]
    if isinstance(value, str) == False:
      value = simplejson.dumps(value)
    paramStr = f'{separator}{name}={value}'
    ret = ret + paramStr
    isFirst = False

  return ret


#------------------------------------------------------------------------
def throw(message):
    msg = simplejson.dumps(message, indent=4)

    logging.error(msg)
    raise ValueError(msg)


#------------------------------------------------------------------------

def checkError():
    lc = restClient.lastCall()
    if lc['error'] is not None:
      utils.raiseException(lc['errorCode'],lc['error'],lc['action'])
 #   response = lastcall['response']
 #   if 'messages' in response:
 #       if len(response['messages']) > 0:
 #           msg = response['messages'][0]
 #           if 'code' in msg:
 #               if msg['code'] == '208' or msg['code'] == '101':
 #                   return False
#
#                if msg['severity'] == 'ERROR':
#                    return throw(msg)

 #   elif lastcall['status_code'] == 600:
 #       return throw(response)

    return False

#------------------------------------------------------------------------
def createQuote(opportunityid,pricelistName,name, recordTypeId,expirationDate = "2023-01-17" ,inputFields = None,fields='Id,Name,EffectiveDate'):
    global _carts

    Body = {
    "methodName": "createCart",
    "objectType": 'Quote',
    "inputFields": [
        {"opportunityid": opportunityid},
        {"Name": name},
        {"ExpirationDate": expirationDate},
        {"RecordTypeId": recordTypeId},
        {"pricelistName": pricelistName}
        ],
    "subaction":'createQuote',
    "fields": fields
    }     

    if inputFields != None:
        Body['inputFields'] = Body['inputFields'] + inputFields

    call = restClient.callAPI('/services/apexrest/vlocity_cmt/v2/carts',
                                method="post",
                                data=Body)
    logging.info(f"Quote {name} created with code {restClient.lastCall()['status_code']}")

  #  _set(call['records'][0]['Id'],name,pricelistId,accountId)
    checkError()
    return  call

def createCart_api(accountId,pricelistId,name='', subaction='createOrder',effectivedate =  date.today().strftime("%Y-%m-%d"),channel='python',inputFields = None,fields='Id,Name,EffectiveDate'):
    global _carts

    objectType = "Order"
    if subaction == 'createQuote':
        objectType = "Quote"

    if subaction == 'createOrder':
        Body = {
            "methodName": "createCart",
            "objectType": objectType,
            "inputFields": [
                {"effectivedate": effectivedate },
                {"status": "Draft"},
                {"Name": name},
                {"AccountId": accountId},
                {"vlocity_cmt__PriceListId__c": pricelistId}, 
                {"vlocity_cmt__OriginatingChannel__c": channel}
                ],
            "subaction":subaction,
            "fields": fields
            }

    if inputFields != None:
        Body['inputFields'].append(inputFields)

    call = restClient.callAPI('/services/apexrest/vlocity_cmt/v2/carts',
                                method="post",
                                data=Body)

    checkError()
    logging.info(f"Card {name} created")

   # _set(call['records'][0]['Id'],name,pricelistId,accountId)

    return call

#------------------------------------------------------------------------
def createCart(accountF,pricelistF,name,checkExists=False,subaction='createOrder',effectivedate =  date.today().strftime("%Y-%m-%d"),channel='python',inputFields=None,fields='Id,Name,EffectiveDate'):
    """
    - CartId: 
    """
    if type(accountF) is dict:
        accountId = utils.Id(accountF)
    else:
        accountId = query.queryIdF('product2',accountF)
    
    pricelistId = query.queryIdF('vlocity_cmt__PriceList__c',pricelistF)

    if checkExists:
        cartId = query.queryField(f" select Id from Order where Name ='{name}' and AccountId='{accountId}' ")
        if cartId != None:
            logging.info(f"Cart with Name {name} exists. Returning existing")
            _set(cartId,name,pricelistId,accountId)
            return cartId

    cartCall= createCart_api(accountId,pricelistId,name,subaction,effectivedate,channel,inputFields,fields)

    return cartCall['records'][0]['Id']

def createCartX(accountX,pricelistX,name,checkExists=False,subaction='createOrder',effectivedate =  date.today().strftime("%Y-%m-%d"),channel='python',inputFields=None,fields='Id,Name,EffectiveDate'):
    if type(accountX) is dict:
        accountId = utils.Id(accountX)
    else:
        accountId = query.queryField(f" select Id from Account where $X='{accountX}' ")

    pricelistId = query.queryField(f" select Id from vlocity_cmt__PriceList__c where $X='{pricelistX}' ")

    if checkExists:
        cartId = query.queryField(f" select Id from Order where Name ='{name}' and AccountId='{accountId}' ")
        if cartId != None:
            logging.info(f"Cart with Name {name} exists. Returning existing")
            _set(cartId,name,pricelistId,accountId)
            return cartId

    cartCall= createCart_api(accountId,pricelistId,name,subaction,effectivedate,channel,inputFields,fields)

    return cartCall['records'][0]['Id']

#------------------------------------------------------------------------

def createCartFromAsset_api(orderName, assetId, accountId, date, raiseEx=True):
    if type(assetId) == list:
        assetId = ",".join(assetId)

    data = {
        "subaction": "assetToOrder",
        "id": assetId,
        "accountId": accountId,
        "requestDate": date
    }

    call = restClient.callAPI('/services/apexrest/vlocity_cmt/v2/carts',method="post",data=data)

    call = checkError(call, raiseEx=raiseEx)
    if call == None:
        return None

    id = None
    try:
        id = call['records'][0]['cartId']
    except:
        raise ValueError(str(call['messages']))

    data = {"Name": orderName}
    Sobjects.update(id, data)
    logging.info(f"Created cart {id} from Asset. Order Name <{orderName}>")
    return call

#------------------------------------------------------------------------

def getCartSummary_api(cartid,validate=None,price=None,headerFieldSet=None,translation=None):

    paramStr = stringify(locals(),exclude=['cartid'])
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartid}{paramStr}'

    call = restClient.callAPI(action)
    checkError()
    return call

#------------------------------------------------------------------------

def deleteCart(cartId,cartType='Order'):
    delete = Sobjects.delete('Order',cartId)
    checkError()
    return delete

#------------------------------------------------------------------------

def getCartAttributes_api(cartId):
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/attributes'

    call = restClient.callAPI(action)
    checkError()
    return call

#------------------------------------------------------------------------

def runCartValidation_api(cartid,validate=None,price=None):

    paramStr = stringify(locals(),exclude=['cartid'])
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartid}{paramStr}'

    body=    {
        "cartId":cartid,
        "methodName":"runCartValidation"#,
      #  "price":true,
      #  "validate":true
        }
    call = restClient.callAPI(action,method='post',data=body)
    checkError()
    return call

#-------------------------------------------------------------------------------------------------------------

def getCartItems_api(cartId, query=None,id=None,lastRecordId=None,pagesize=None,hierarchy=None,includeAttachment=None,headerFieldSet=None,filter=None,price=None,validate=None):
    paramStr = stringify(locals(),exclude=['cartid'])

    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items{paramStr}'

    call = restClient.callAPI(action)
    checkError()
    return call

#-------------------------------------------------------------------------------------------------------------
def addItemstoCart(cartId,productCode,parentId=None,parentHierarchyPath=None,parentRecord=None,price=None,validate=None,hierarchy=None,pagesize=None,includeAttachment=None,expandAll=None,fields=None,noResponseNeeded=False):
    priceBookEntryId = priceBook.pricebookEntryId_pl(_get(cartId)['plId'],productCode,pricelistField='Id')
    return addItemstoCart_api(cartId,priceBookEntryId,parentId,parentHierarchyPath,parentRecord,price,validate,hierarchy,pagesize,includeAttachment,expandAll,fields,noResponseNeeded)

def addItemstoCart_api(cartId,priceBookEntryId,parentId=None,parentHierarchyPath=None,parentRecord=None,price=None,validate=None,hierarchy=None,pagesize=None,includeAttachment=None,expandAll=None,fields=None,noResponseNeeded=False):
    paramStr = stringify(locals(),exclude=['cartid','itemIds'])

    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items{paramStr}'

    data = {
        "items": [{
            "itemId": priceBookEntryId,  
        }]
    }

    if parentId != None:
        data = {
            "items": [{
                "parentId": parentId,
                "parentHierarchyPath": parentHierarchyPath,
                "itemId": priceBookEntryId,  
                "parentRecord": {
                    "records": [
                        parentRecord
                    ]
                }
            }]
        }
    if noResponseNeeded == True:
        data['noResponseNeeded'] = True

    call = restClient.callAPI(action,method='post',data=data)
    logging.info(f"added {priceBookEntryId} to cart {cartId}")
    checkError(call)
    return call

#-------------------------------------------------------------------------------------------------------------

def updateCartItem_api(cartId, items):

    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items'
    data = {"items": items}
    call = restClient.callAPI( action, method="put",data=data)
    checkError(call)
    return call

#-------------------------------------------------------------------------------------------------------------

def _getItemAtPath(obj,path,field='ProductCode'):
    for p in path.split(':'):
        obj = objectUtil.getSibling(obj,field,p)  
    return obj

#-------------------------------------------------------------------------------------------------------------

def addToCart_action(parentItem,product,field='ProductCode'):
    sibbling = objectUtil.getSiblingWhere(parentItem,field,product,'itemType','childProduct')['object']
    if sibbling == None:
        logging.warn("The expand does not have a reference to the product. {field}:{product}")
        return None

    actions = objectUtil.getSiblingWhere(sibbling,selectKey='actions')['object']

    if 'records' in parentItem:
        parentItem = parentItem['records'][0]
    parentItem = copy.deepcopy(parentItem)
    parentItem['childProducts'] = ""   

    call = executeActions(actions,'addtocart',parentItem=parentItem)

    logging.info(f"Adding to cart with expansion. Product {product}")

    return call

#-------------------------------------------------------------------------------------------------------------

def addToCart(cartId,parentProductName,productName,field='name',cartItems=None):

    restClient.logCall('getCartItems12')
    if cartItems == None:
        cartItems = getCartItems_api(cartId)

    parentItem = _getItemAtPath(cartItems,parentProductName,field)
    #parentItem = jsonUtil.getSibling(cartItems,'name',parentProductName,logValues=True)
    item = objectUtil.getSibling(parentItem,'name',productName)
   # if item == '':
   #     expanditems = 

    parentItem = copy.deepcopy(parentItem)
    parentItem['childProducts'] = ""

    execute = executeActions(item,parentItem=parentItem)
    return execute

#-------------------------------------------------------------------------------------------------------------

def expand_action(cartItems,sibling,field='ProductCode'):    
    sibblingItem = objectUtil.getSiblingWhere(cartItems,field,sibling,'itemType','lineItem')
    if sibblingItem['object'] == None:
        sibblingItem = objectUtil.getSiblingWhere(cartItems,field,sibling,'itemType','productGroup')

    call = executeActions(sibblingItem['object']['actions'],'expanditems')
    logging.info(f"Expanding {sibling}")
    return call

#-------------------------------------------------------------------------------------------------------------

def expand_api(cartId,itemId,productHierarchyPath):
    paramStr = stringify(locals(),exclude=[], initSeparator='?')

    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items/{itemId}/expand{paramStr}'

    call = restClient.callAPI( action, method="get")
    checkError()
    return call

#-------------------------------------------------------------------------------------------------------------

def executeRestAction_api(rest):
    link = rest['link']
    params = rest['params']
    method = f"{rest['method']}".lower()

    call = restClient.callAPI(link, method=method, data=params)
    return call

#-------------------------------------------------------------------------------------------------------------

def executeActions(actionsObject, actionName='addtocart', parentItem=None):
    if 'actions' in actionsObject:
        actions = actionsObject['actions']

    rest = actionsObject[actionName]['rest']
    if actionName == 'addtocart':
        rest['params']['items'][0]['parentRecord'] = {"records": [parentItem]}

    call = executeRestAction_api(rest)
    return call

#-------------------------------------------------------------------------------------------------------------

def deleteCartItems_api(cartId, itemIds,hierarchy=None,lastRecordId=None,pagesize=None,includeAttachment=None,fields=None,query=None):
    paramStr = stringify(locals(),exclude=['cartid','itemIds'],initSeparator='&')

    action =  f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items?id={",".join(itemIds)}{paramStr}'
    requestBody = {
        "items": [{
            "itemId": ",".join(itemIds)
        }]#,
       # "price": True,
       # "validate": True
    }
    call = restClient.callAPI(action,method="delete",data=requestBody)
    checkError()
    return call

#-------------------------------------------------------------------------------------------------------------

def getCartPromotions_api(cartId,getPromotionsAppliedToCart=False,include=None,includePenalties=None,ruleType=None,ruleEvaluationInput=None,filters=None,category=None,fields=None,pagesize=None,commitmentDateFilter=None,appliedPromoStatusFilter=None):
    subaction =  "getPromotionsAppliedToCart" if getPromotionsAppliedToCart == True else None

    paramStr = stringify(locals(),exclude=['cartId','getPromotionsAppliedToCart'])
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/promotions{paramStr}'

    call = restClient.callAPI(action)
    checkError()
    return call['records']

#-------------------------------------------------------------------------------------------------------------

def postCartsPromoItems_api(cartId, promotionId):
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/promotions?cartId={cartId}&id={promotionId}'

    data = {
        "methodName": "postCartsPromoItems",
        "items": [{
            "itemId": promotionId
        }],
        "promotionId": promotionId,
        "cartId": cartId
    }
    call = restClient.callAPI(action, method='post', data=data)
    checkError()

    return call

#-------------------------------------------------------------------------------------------------------------

def deleteCartPromotion_api(cartId, promotionId):
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/promotions?cartId={cartId}&id={promotionId}'
    data = {
        "id": promotionId,
        "cartId": cartId,
        "methodName": "deleteAppliedPromoItems",
        "price": True,
        "validate": True
    }
    call = restClient.callAPI(action, method='delete', data=data)
    checkError()
    return call

#-------------------------------------------------------------------------------------------------------------

def getCartProducts_api(cartId, maxProdListHierarchy=None, query=None, filters=None,getCartProducts=None,lastRecordId=None,includeAttachment=None,offsetSize=None,fields=None,pagesize=None,attributes=None,includeAttributes=None,includeIneligible=True):
    """
    - cartId:  Cart Id (Salesforce Id).Opportunity, Quote or Order Id. - Required. String
    - maxProdListHierarchy: hierarchy depth returned for list of products. Integer. 
    - lastRecordId: The last record ID from the previous search result, if available. string.
    - query: search string. 
    - includeAttachment: Whether product attachments are returned. boolean
    - filters: Filter field values. string
    - offsetSize: Offset from which to start reading products, for pagination. Integet.
    - fields: List of fields to return in the response, separated by commas. 
    - pagesize: Number of records to be returned. integer.
    - attributes: Attribute filters. 
    - includeAttributes: Specifies whether to return a list of attributes and their values for the product. boolean
    """
    paramStr = stringify(locals(),exclude=['cartId'])

    cartId = utils.Id(cartId)
    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/products{paramStr}'

    call = restClient.callAPI(action)

    checkError()
   # if call['messages'][0]['message'] == 'No Results Found.':
   #     return None
    return call['records']

#-------------------------------------------------------------------------------------------------------------

def checkOut_api(cartId,validateSubmittedXLI=True,assetizeFullBundlePerRoot=True,checkOrderStatus=True, provisioningStatus='Active',skipCheckoutValidation=True,waitActivation=False,asyncCall = False):
    cartId = utils.Id(cartId)

    data = {
        "methodName": "checkout",
        "cartId": cartId,
        "ContextId": cartId,
        #     "objectTypeToIdsToClone":"OrderItem:8021N000008NG5t_8021N000008NG5s",
        "validateSubmittedXLI": validateSubmittedXLI,
        "assetizeFullBundlePerRoot": assetizeFullBundlePerRoot,
        "checkOrderStatus": checkOrderStatus,
        "provisioningStatus": provisioningStatus,
        "skipCheckoutValidation": skipCheckoutValidation
    }

    action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items/checkout'
    if asyncCall == True:
        action = f'/services/apexrest/AsyncCPQAppHandler/v1/checkout'
    call = restClient.callAPI(
        action,
        method="post",
        data=data)
    logging.info(f'Cart Check-out with code {call["status_code"]}')
    checkError()
    assert(False)
   # if waitActivation == True:
   #   orderUtils.waitforOrderActivation(cartId)
    
    return call
