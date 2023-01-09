from . import restClient,query,digitalCommerceUtil, utils
import simplejson,logging,inspect

#------------------------------------------------------------------------

def stringify(parameters,exclude):
  isFirst = True

  ret = ''
  for name in parameters:
    if name in exclude:
      continue
    if(parameters[name] == None):
      continue
    separator = '?' if isFirst == True else '&'
    value = parameters[name]
    if isinstance(value, str) == False:
      value = simplejson.dumps(value)
    paramStr = f'{separator}{name}={value}'
    ret = ret + paramStr
    isFirst = False

  return ret

#------------------------------------------------------------------------

def checkBasketError():

  lc = restClient.lastCall()
  if lc['error'] is not None:
      utils.raiseException(lc['errorCode'],lc['error'],lc['action'])
  if lc['response']['error']!='OK':
      utils.raiseException(lc['response']['errorCode'],lc['response']['error'],other=lc['action'])
  if 'success' in lc['response'] and lc['response']['success'] == False:
      utils.raiseException(lc['response']['errorCode'],f"{inspect.stack()[1].function}: success:{lc['response']['success']}  isBasketValid:{lc['response']['isBasketValid']}")
  if 'result' in lc['response'] and 'offerDetails' in lc['response']['result']:
      utils.raiseException(f"CreateBasket {lc['response']['result']['offerDetails']['StatusCode']}",lc['response']['result']['offerDetails']['messages'][0])

  #if lc['response']['result']['error'] !='OK':
  #  print()

def checkOfferError():

  lc = restClient.lastCall()
  if lc['error'] is not None:
      utils.raiseException(lc['errorCode'],lc['error'],lc['action'])
  if lc['response']['error']!='OK':
      utils.raiseException(lc['response']['errorCode'],lc['response']['error'],other=lc['action'])
  if 'success' in lc['response'] and lc['response']['success'] == False:
      utils.raiseException(lc['response']['errorCode'],f"{inspect.stack()[1].function}: success:{lc['response']['success']}  isBasketValid:{lc['response']['isBasketValid']}")



#------------------------------------------------------------------------

def getResult(obj):

  if 'result' in obj:
    obj = obj['result']  
  return obj

#------------------------------------------------------------------------

def getCatalogs(catalogueCode=None):
    where = f" where vlocity_cmt__CatalogCode__c = '{catalogueCode}' " if catalogueCode !=None else ''
    call = query.query(f'select Fields(ALL) from vlocity_cmt__Catalog__c {where} limit 100')
    return call['records']

#------------------------------------------------------------------------

def getCatalogProducts(catalogId):
    call = query.query(f"select Fields(ALL) from vlocity_cmt__CatalogProductRelationship__c where vlocity_cmt__CatalogId__c='{catalogId}' limit 100")  
    return call

#------------------------------------------------------------------------

def getCatalogbyField(value,field='Name'):
    call = query.query(f"select Fields(ALL) from vlocity_cmt__Catalog__c where {field}='{value}' limit 100")    
    return call

#------------------------------------------------------------------------

def getOfferByCatalogue(catalogcode,contains=None,contextkey=None,context=None,forceinvalidatecache=None,isloggedin=None,pagesize=None,offset=None,sortby=None,excludeoverridedefinition=None,offerList=None):
  paramStr = stringify(locals(),exclude=['catalogcode'])
  action = f'/services/apexrest/{restClient.getNamespace()}/v3/catalogs/{catalogcode}/offers{paramStr}'
  call = restClient.callAPI(action)
  checkOfferError()

  if 'offers' in call:
    return call['offers']

  return []

#------------------------------------------------------------------------

def getOfferDetails(catalogcode,offercode,contextkey=None,context=None,forceinvalidatecache=None,isloggedin=None):
  paramStr = stringify(locals(),exclude=['catalogcode','offercode'])
  action = f'/services/apexrest/{restClient.getNamespace()}/v3/catalogs/{catalogcode}/offers/{offercode}{paramStr}'
  call = restClient.callAPI(action)
  checkOfferError()


  lc = restClient.lastCall()
  log = {
      'method':'getOfferDetails',
      'action':f"{lc['url']}{lc['action']}",
      'catalog':catalogcode,
      'offer':offercode,
      'contextKey':call['contextKey'],
      'error':call['error'],
      'deltaTime':lc['deltaTime'],
      'elapsedTime':lc['elapsedTime']
  }
  lc['log'] = log
  return call
#------------------------------------------------------------------------

def createBasket(catalogcode,offer,contextKey=None,context=None,forceinvalidatecache=None,isloggedin=None,includeAttachment=None,returnBasket=None,validatebasket=None):
  paramStr = stringify(locals(),exclude=['catalogcode','offer'])
  action = f'/services/apexrest/{restClient.getNamespace()}/v3/catalogs/{catalogcode}/basket{paramStr}'
  restClient.glog().debug(action)

  body = {
    "basketAction": "AddWithNoConfig",
    "offer":offer
  }

  response = restClient.callAPI(action, method="post", data=body)
  checkBasketError()

  lc = restClient.lastCall()
  log = {
      'method':'AddWithNoConfig',
      'action':f"{lc['url']}{lc['action']}",
      'catalog':catalogcode,
      'offer':offer,
      'contextKey':response['cartContextKey'],
      'error':response['error'],
      'deltaTime':lc['deltaTime'],
      'elapsedTime':lc['elapsedTime']              
  }
  lc['log'] = log

  return response

#------------------------------------------------------------------------

def createBasketAfterConfig(catalogcode,offerDetails,contextKey=None,context=None,forceinvalidatecache=None,isloggedin=None,includeAttachment=None,returnBasket=None,validatebasket=None):
  paramStr = stringify(locals(),exclude=['catalogcode','offerDetails'])
  action = f'/services/apexrest/{restClient.getNamespace()}/v3/catalogs/{catalogcode}/basket{paramStr}'
  restClient.glog().debug(action)

  body = {
    "basketAction": "AddAfterConfig",
    "productConfig": getResult(offerDetails)
  }

 # restClient.writeFile('body12xx',body)
  response = restClient.callAPI(action, method="post", data=body)
  checkBasketError()


  lc = restClient.lastCall()
  log = {
      'method':'AddAfterConfig',
      'action':f"{lc['url']}{lc['action']}",
      'catalog':catalogcode,
      'offer':getOfferCode( offerDetails['result']['offerDetails']['offer']),
      'contextKey':response['cartContextKey'] if 'cartContextKey' in response else "",
      'error':response['error'],
      'deltaTime':lc['deltaTime'],
      'elapsedTime':lc['elapsedTime']              
  }
  lc['log'] = log

  return response

#------------------------------------------------------------------------

def executeActions(basketAction):
  action = basketAction['link']
  body = basketAction['params']
  method="post"

  if basketAction['method'] == 'updateBasketAction':
    method = 'put'

  response = restClient.callAPI(action, method=method, data=body)
  response = checkBasketError(response)
  return response

#------------------------------------------------------------------------

def addChildBasket(basket,path):
  basketAction = digitalCommerceUtil.getAction(basket,path,method='addChildBasketAction')
  basket2 = executeActions(basketAction)

  return basket2

#------------------------------------------------------------------------

def deleteFromBasket(basket,path):
  basketAction = digitalCommerceUtil.getAction(basket,path,method='deleteFromBasketAction')
  basket2 = executeActions(basketAction)

  return basket2

#------------------------------------------------------------------------

def setError(error,errorCode):
    restClient.glog().error(f"Error {error}  {errorCode}")
    restClient.setLastCallError( error,errorCode)



#------------------------------------------------------------------------

def updateBasketQuantity(basket,path,value):
  basketAction = digitalCommerceUtil.getAction(basket,path,method='updateBasketAction')
  basketAction['params']['Quantity'] = str(value)
  basket2 = executeActions(basketAction)
  if len(basket2['result']['messages'])==0:
    print('ok')
  else:
    print("Error")
  return checkBasketError(basket2)

#------------------------------------------------------------------------

#{"field":value}
def updateBasketFields(basket,path,fieldsToBeUpdated):
  basketAction = digitalCommerceUtil.getAction(basket,path,method='updateBasketAction')
  basketAction['params']['fieldsToBeUpdated'] = fieldsToBeUpdated
  basket2 = executeActions(basketAction)

  return basket2


#  updates = [
#    {
#      "Category":'ACAT_EQUIPMENT',
#      "Attribute":'ATT_SERIAL_NUMBER',
#      "value":""
#    }
#  ]

#------------------------------------------------------------------------

def updateBasketAttributes(basket,path,updates):
  attributes = digitalCommerceUtil.getBasketProductAttributes(basket,path)

  for update in updates:
    for cat in attributes['records']:
      if cat['Code__c'] == update['Category']:
        for attribute in cat['productAttributes']['records']:
          if attribute['code'] == update['Attribute']:
            attribute['userValues'] = update['value']

  basketAction = digitalCommerceUtil.getAction(basket,path,method='updateBasketAction')
  basketAction['params']['attributeCategories'] = attributes
  basket2 = executeActions(basketAction)

  return basket2

#------------------------------------------------------------------------

def createCart(accountId,catalogCode,cartContextKey,createAsset=False,assetReferenceKey=None):
  if type(cartContextKey) is dict:
    cartContextKey = cartContextKey

  data = {
    "accountId": accountId,
    "catalogCode": catalogCode,
    "cartContextKey": cartContextKey
  }
  action = f'/services/apexrest/{restClient.getNamespace()}/v3/carts?price=false&validate=false'

  if assetReferenceKey != None:
    data['assetReferenceKey'] = assetReferenceKey
    context = 'context={"accountId":"' + accountId + '"}'
    action = f'/services/apexrest/{restClient.getNamespace()}/v3/carts?{context}&isloggedin=true&price=false&validate=false'
   # action = f'/services/apexrest/{client.getNamespace()}/v3/carts?{context}&isloggedin=true'

  if createAsset:
      action = f'{action}&createAsset=true'

  #print(data)
  call = restClient.callAPI(action, method="post", data=data)
  checkBasketError()
  return call

#------------------------------------------------------------------------

def printPricing(offerDetails):
  offer = offerDetails['result']['offerDetails']['offer']
  if 'priceResult' in offer:
    if isinstance(offer['priceResult'],list):
      for priceResult in offer['priceResult']:
        if 'DisplayText__c' in priceResult:
          print(f"{offer['Name']}  {priceResult['DisplayText__c']}")
    else:   #something wrong such as no valid price found.
      print(f"{offer['Name']}  {offer['priceResult']}")

  else:
    print('No price result')
  if 'childProducts' in offer:
    for childProduct in offer['childProducts']:
      if 'priceResult' in childProduct:
        for priceResult in childProduct['priceResult']:
            print(f"{childProduct['Name']}  {priceResult['DisplayText__c']}")
      else:
          print(f"{childProduct['Name']}  <No pricing>")

#------------------------------------------------------------------------

def getOfferCode(offer):
  if offer['offerType'] == 'Product':
      code = offer['ProductCode']
  else:
      code = offer['vlocity_cmt__Code__c']
    
  return code