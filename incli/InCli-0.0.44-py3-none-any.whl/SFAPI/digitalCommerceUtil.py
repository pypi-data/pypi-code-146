from . import restClient, objectUtil,digitalCommerce,utils,thread,query,CPQ
import time
import sys

def _getItemAtPath(obj,path,field='ProductCode'):
    for p in path.split(':'):
        obj = objectUtil.getSibling(obj,field,p)  
    return obj

def updateOfferField(offerDetails,path,field,value,pathField='ProductCode'):
    obj = _getItemAtPath(offerDetails,path,pathField)
    if obj == '':
        raise ValueError(f'Object does not contain element by path {path}')
    if field in obj:
        obj[field] = value
    else:
        raise ValueError(f'Object does not contain field {field} by path {path}')

    return offerDetails

def updateOfferAttribute(offerDetails,path,AttributeCategory,productAttribute,value):
    obj = _getItemAtPath(offerDetails,path)
    obj = _getItemAtPath(obj,AttributeCategory,field='Code__c')
    obj = _getItemAtPath(obj,productAttribute,field='code')

    obj['userValues'] = value
 
    return offerDetails

def getBasketProductAttributes(basket,path):
    obj = _getItemAtPath(basket,path)
    obj = obj['attributeCategories']

    return obj

def getAction(basket,path,method='addChildBasketAction'):

    lpath = path.split(':')
    xpath = ":".join(lpath[:-1])
    offer = lpath[-1]


    obj = _getItemAtPath(basket,xpath)
    action = _getItemAtPath(obj,method,field='method')

    action['params']['offer'] = offer
    action['link'] = f"/services/apexrest/{restClient.getNamespace()}{action['link']}"



    return action

def printCatalogs(catcatalogueCode=None):
    catalogs = digitalCommerce.getCatalogs(catcatalogueCode)
    print()
    print(f'Catalogs in the Org {utils.CGREEN+ restClient._currentConnectionName + utils.CEND}:')
    utils.printFormated(catalogs,"Name:vlocity_cmt__CatalogCode__c:vlocity_cmt__IsActive__c:vlocity_cmt__Description__c",rename="vlocity_cmt__IsActive__c%Active")
    print() 
    return catalogs

def checkOffers(path=None,quantity=None,catcatalogueCode=None,account=None,basketOps=False):

    catalogs = printCatalogs(catcatalogueCode)

    catsOffers = []
    numOffersList = []
    print()

    print(utils.CLIGHT_CYAN+"GetOffers per catalog."+utils.CEND)
    getOfferTimes = []
    def getOffersPerCatalog(catalog):

        if catalog['vlocity_cmt__IsActive__c'] == False:
            return 
        try:
            times = {
                'name':catalog['vlocity_cmt__CatalogCode__c'],
                'Error':'',
                "__color__":utils.CEND
            }
            offers = digitalCommerce.getOfferByCatalogue(catalog['vlocity_cmt__CatalogCode__c'],pagesize=400)
            times['elapsed'] = restClient.getLastCallTime()
            l = len(offers) if offers is not None else 0
            numOffersList.append(l)
            times['# Offers'] = l

        except Exception as e:
            times['elapsed'] = restClient.getLastCallTime()
            times['Error'] = e.args[0]['error']
            times['__color__'] = utils.CRED
            getOfferTimes.append(times)
            return   

        if offers == None:
            times['Error'] = "Has no offers."
            times['__color__'] = utils.CYELLOW
            getOfferTimes.append(times)
            return 
       #             obj['off effDate'] = offer[0]['vlocity_cmt__EffectiveStartDate__c'] if obj['type'] == 'Promotion' else offer[0]['vlocity_cmt__Product2Id__r'] 


        relationships = query.queryRecords(f"""select vlocity_cmt__SequenceNumber__c,
                                                        vlocity_cmt__EffectiveDate__c,
                                                        Name,
                                                        Id,
                                                        vlocity_cmt__Product2Id__r.Name,
                                                        vlocity_cmt__Product2Id__r.vlocity_cmt__EffectiveDate__c,
                                                        vlocity_cmt__Product2Id__r.ProductCode,
                                                        vlocity_cmt__PromotionId__r.Name,
                                                        vlocity_cmt__PromotionId__r.vlocity_cmt__EffectiveStartDate__c,
                                                        vlocity_cmt__PromotionId__r.vlocity_cmt__Code__c,
                                                        vlocity_cmt__IsActive__c,
                                                        vlocity_cmt__ItemType__c,
                                                        IsDeleted 
                                                        from vlocity_cmt__CatalogProductRelationship__c 
                                                        where vlocity_cmt__CatalogId__c = '{catalog['Id']}' order by vlocity_cmt__SequenceNumber__c limit 200""")

        catOffers = {
            'catCode':catalog['vlocity_cmt__CatalogCode__c'],
            'catId':catalog['Id'],
            'offers':offers,
            'relationships':relationships
        }
        catsOffers.append(catOffers)
        getOfferTimes.append(times)

    thread.processList(getOffersPerCatalog,catalogs,10)
    utils.printFormated(getOfferTimes)
    totalOffers = sum(numOffersList)

    for catOffers in catsOffers:
        print()
        print()

        print(utils.CLIGHT_CYAN+ f"Product relationships and offers in the API for catalog {catOffers['catCode']} "+utils.CEND)
        objs = []
        for relationship in catOffers['relationships']:
          #  if relationship['vlocity_cmt__ItemType__c'] == 'Promotion':
                fields = ['Name','Id','vlocity_cmt__ItemType__c','vlocity_cmt__IsActive__c','vlocity_cmt__Product2Id__c','vlocity_cmt__PromotionId__c']
                obj = {
                    "seq":relationship['vlocity_cmt__SequenceNumber__c'],
                    "effDate":relationship['vlocity_cmt__EffectiveDate__c'],
                    "Name_Relationship":relationship['Name'],
                    "Id_Relationship":relationship['Id'],
                    "type":relationship['vlocity_cmt__ItemType__c'],
                    "Actv":relationship['vlocity_cmt__IsActive__c'],
                    "Name_prod":relationship['vlocity_cmt__Product2Id__r']['Name'] if relationship['vlocity_cmt__Product2Id__r']!=None else '',
                    "Name_promo":relationship['vlocity_cmt__PromotionId__r']['Name'] if relationship['vlocity_cmt__PromotionId__r']!=None else '',
                    "P_effDate":relationship['vlocity_cmt__Product2Id__r']['vlocity_cmt__EffectiveDate__c'] if relationship['vlocity_cmt__Product2Id__r']!=None else relationship['vlocity_cmt__PromotionId__r']['vlocity_cmt__EffectiveStartDate__c'],
                    "P_Code":relationship['vlocity_cmt__Product2Id__r']['ProductCode'] if relationship['vlocity_cmt__Product2Id__r']!=None else relationship['vlocity_cmt__PromotionId__r']['vlocity_cmt__Code__c']
                }
                if 'T' in obj["P_effDate"]:
                    obj["P_effDate"] = obj["P_effDate"].split('T')[0]

                if obj['type'] == 'Promotion':
                    offer = [ offer for offer in catOffers['offers'] if offer['offerType'] == 'Promotion' and offer['Name']==obj['Name_promo']]
                if obj['type'] == 'Product':
                    offer = [ offer for offer in catOffers['offers'] if offer['offerType'] == 'Product' and offer['Name']==obj['Name_prod']]
                if len(offer)>0:
                    obj['Offer Name'] = offer[0]['Name']
                    obj['Offer Code'] = offer[0]['vlocity_cmt__Code__c'] if obj['type'] == 'Promotion' else offer[0]['ProductCode']
                    obj['P_isActive'] = offer[0]['vlocity_cmt__IsActive__c'] if obj['type'] == 'Promotion' else offer[0]['IsActive']
                    obj['isOrderable'] = offer[0]['vlocity_cmt__IsOrderable__c']
                    obj['__color__'] = utils.CEND
                else:
                    obj['NameP'] = 'No Offer'
                    obj['Code'] = ""
                    obj['PActv'] = ""
                    obj['isOrderable'] = ""     
                    obj['__color__'] = utils.CRED if obj['Actv'] == True else utils.CFAINT 

                obj['Name_promo'] = f"Promo: {obj['Name_promo']}" if obj['Name_promo']!='' else f"Prod: {obj['Name_prod']}"

                objs.append(obj)
        utils.printFormated(objs,exclude="Id_Relationship:type:Name_prod")

    print()
    print()

    if basketOps == True:
        print(utils.CLIGHT_CYAN+f"Getting offerDetails, createBasket, createBasket with config per offer. total offers {totalOffers}"+utils.CEND)
    else:        
        print(utils.CLIGHT_CYAN+f"Getting offerDetails. total offers {totalOffers}"+utils.CEND)


    offersList = []

    accountId = None

    if account != None:
        chunks = account.split(':')
        id = query.queryField(f" select Id from Account where {chunks[0]} = '{chunks[1]}'")
        if id==None:
            print(utils.CLIGHT_RED+ f"Cannot find an account where {chunks[0]} = '{chunks[1]}'"+utils.CEND)
        else:
            accountId=id

    for catOffers in catsOffers:
        for offerCount,offer in enumerate(catOffers['offers']):
            _offer = {
                'catalogCode':catOffers['catCode'],
                'offerCode':digitalCommerce.getOfferCode(offer),
                'basketOps':basketOps
            }
            if accountId != None:
                _offer['accountId']=id
            offersList.append(_offer)

    thread.processList(dba,offersList,10)
    newlist = sorted(_theTimes, key=lambda d: f"{d['catalog']}{d['offerCode']}")
    utils.printFormated(newlist)
    for error in _errors:
        utils.printException(error)

    print()

_theTimes = []
_errors = []
def dba(offerCodes):
    try:
        offerCode = offerCodes['offerCode']
        catalogCode = offerCodes['catalogCode']
        times = {
            'catalog':catalogCode,
            'offerCode':offerCode,
            'details':'',
            'createBasket':'',
            'afterConfig':'',
            '__color__':utils.CEND,
            "error":''
        }

        details = digitalCommerce.getOfferDetails(catalogCode,offerCode)
        times['details'] = restClient.getLastCallTime()

        if offerCodes['basketOps'] == True:
            basket = digitalCommerce.createBasket(catalogCode,offerCode)
            times['createBasket'] = restClient.getLastCallTime()

            if details['result']['offerDetails']['offer']['offerType'] == 'Promotion':
                try:
                    offerDetails = updateOfferField(details,'ATT_NOS_OTT_SUBSCRIPTION_ID','values','xxxxxx','code')
                except Exception as e:
                    if e.args[0] == 'Object does not contain element by path ATT_NOS_OTT_SUBSCRIPTION_ID':
                        offerDetails = updateOfferField(details,'ATT_NOS_PRICE_CONDITIONS','values','PRICE_COND_003','code')
                    else:
                        raise
            else:
                offerDetails = updateOfferField(details,'0001','Quantity',4,'lineNumber')

            basket2 = digitalCommerce.createBasketAfterConfig(catalogCode,offerDetails)
            times['afterConfig'] = restClient.getLastCallTime()
        if 'accountId' in offerCodes and 1==2:
            times['cart']=''
            cart = digitalCommerce.createCart(offerCodes['accountId'],catalogCode,basket2['cartContextKey'],createAsset=False)
            times['cart']=restClient.getLastCallTime()

            times['delete']=''
            delete = CPQ.deleteCart(cart['orderId'])
            times['delete']=restClient.getLastCallTime()

            print()

    except Exception as e:
        if len(e.args)> 0  and 'error' in e.args[0]:
            times['error']=e.args[0]['errorCode']
        else:
            times['error']=f"{e}"

        _errors.append(e)

        times['__color__'] = utils.CLIGHT_RED

    _theTimes.append(times)

