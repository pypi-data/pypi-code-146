import logging,json,simplejson
#from posixpath import split
from . import restClient as client
from . import Sobjects,utils
" select fields(all) from vlocity_cmt__EntityFilter__c where Id in ('a5W7Z0000009gEiUAI','a5W7Z0000009gdtUAA','a5W7Z0000009gFfUAI','a5W7Z0000009gEdUAI')"

def _query(q,raiseEx=True,logResponse = False):
    logging.debug(q)
    call = client.callAPI(f'/services/data/v55.0/query?q={q}')
    lc = client.lastThreadCall()

    lc['query']=q
    if lc['error'] != None:
        lc['query'] = q
        if raiseEx==True:
            utils.raiseException(lc['errorCode'],lc['error'],'query',f"{lc['errorOther']} . {q}")
            raise ValueError(simplejson.dumps(call, indent=4))
        logging.warn(simplejson.dumps(call, indent=4))

        return None

    if logResponse == True:
        utils.printJSON(call)

    return call

#--------------------------------------------------------------------------------------------------------------------------------------------------------
def query(q,raiseEx=True,X=['Id','Name'],logResponse=False):
    """
    Executes a query in Salesforce.
    - q: the query string. "select.... from... limit..."
        the where clause can specify a normal field or $X and $Z. 
    - X: by default it will query for Id and Name. 
    - logResponse: 
    """
    if '$X=' not in q and '$Z=' not in q:
        return _query(q,raiseEx,logResponse)

    if '$Z='  in q:
        X=['Id','ProductCode','Name']
        q = q.replace('$Z=','$X=')

    selectfields = q.strip().split()

    for x in range(len(selectfields)):
        if selectfields[x].lower() == 'from':
            objectType = selectfields[x+1]

        if  '$X' in selectfields[x]:
            where = selectfields[x].split("'")
            value = where[1]

    for field in X:
        if field == 'Id':
            if Sobjects.isId(objectType,value) == False:
                continue
        q1 = q.replace('$X',field)
        call = _query(q1,raiseEx=False)      
        if call['totalSize'] > 0:
            return call

    return None

def queryRecords(q,raiseEx=True,X=['Id','Name']):
    select = query(q,raiseEx,X)
    if select == None:
        return None
    return select['records']

cache = {}
def queryFieldList(q,field=None,raiseEx=False,X=['Id','Name']):
    if '$X=' in q or '$Z=' in q:
        print(q)
        if q in cache:
            return cache[q]
    records = queryRecords(q,raiseEx,X)

    if records == None:
        return None

    if field == None:
        field = q.strip().split()[1]
    
    fieldList = []
  
    for record in records:
        fieldList.append(record[field])
        
    if '$X=' in q or '$Z=' in q:
        cache[q]=fieldList

    return fieldList

#" select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__AttributeUniqueCode__c='ATT_MOBILE_CREDITS' and  vlocity_cmt__ObjectId__c='01t7Z00000AVpCLQA1' "
def queryField(q,field=None,raiseEx=False,X=['Id','Name']):
    fieldList = queryFieldList(q,field,raiseEx,X)

    if fieldList == None or len(fieldList) == 0:
        return None

    if len(fieldList) > 1:
        logging.warn(f"There is more than one record returned. total records {len(fieldList)}, query={q}")

    return fieldList[0]

def queryIdF(objName,extendedF):
    if extendedF == None:
        return None
    ef = utils.extendedField(extendedF)
    if ef['field'] == 'Id':
        return ef['value']
    return queryField(f" select Id from {objName} where {ef['field']} = '{ef['value']}' ")
def logQuery(q,filename,raiseEx=False):
    if filename != None:
        client.logCall(filename)
    call = query(q,raiseEx)

    return call


def process( call):
    for asset in call['records']:
        asset['vlocity_cmt__PricingLogData__c'] = json.loads( asset['vlocity_cmt__PricingLogData__c'])

def take_snapshot(fileName,q,postProcessing=None):
    client.debugFile(fileName)
    client.setDebugReplyProcessing(postProcessing)
    query(q)

def records(call):
    return call['records']

def  IN_clause(list):
    values = []
    for p in list:
        values.append(f"'{p}'")
    return ",".join(values)