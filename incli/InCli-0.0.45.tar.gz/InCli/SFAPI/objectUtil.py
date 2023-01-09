from cmath import log
import logging
import simplejson

ident = -1
treeObjects = []
keyPath = []
def reset():
    global ident,treeObjects
    ident = -1
    treeObjects = []
    keyPath = []

def getChild(json,name):
    for key in json.keys():
        if key == name:
            return json[key]
    return ''

#renaiming and return root Json dict. 
def setKeyValue(json, selectKey, selectKeyValue,setKey, setKeyValue,logValues=False):
    sibling = parse(json, selectKey, selectKeyValue,setKey, setKeyValue,logValues)
    return json

def Id(obj):
    sibbling = getSibling(obj,'Id')
    Id = sibbling['Id']
    if 'value' in Id:
        Id = Id['value']
    return Id

def getSiblingEx(obj, selectKey, selectKeyValue,logValues=False):
    reset()
    retObject = []
    if isinstance(obj,list)==True:
        for element in obj:
            ret = parseEx(element, selectKey=selectKey, selectKeyValue=selectKeyValue,logValues=logValues)
            retObject.append(ret)
        return retObject
    return parseEx(obj, selectKey=selectKey, selectKeyValue=selectKeyValue,logValues=logValues)

def getSibling(obj, selectKey, selectKeyValue='',logValues=False,multiple=False):
    global treeObjects,keyPath
    reset()
    if isinstance(obj,list)==True:
        rets = []

        for element in obj:
            ret = parse(element, selectKey=selectKey, selectKeyValue=selectKeyValue,logValues=logValues,rets=rets)
            if ret != '':
                if multiple is False:
                    return ret
                rets.append(ret)
        if multiple is False:
            return None
        return rets
    p = parse(obj, selectKey=selectKey, selectKeyValue=selectKeyValue,logValues=logValues)
    treeObjects = treeObjects[0:ident+1]
    keyPath = keyPath[0:ident+1]

    return p

def getSiblingWhere(obj, selectKey,selectKeyValue=None, whereKey=None,whereValue=None,logValues=False):

    result = {
        'level':-1,
        'keys':[],
        'objects':[],
        'object':None
    }

    if isinstance(obj,list)==True:
        for element in obj:
            ret = parseWhere(element, selectKey=selectKey,selectKeyValue=selectKeyValue, whereKey=whereKey, whereValue=whereValue,logValues=logValues,result=result)
            if ret['object'] != None:
                return ret
        return None
    ret = parseWhere(obj, selectKey=selectKey, selectKeyValue=selectKeyValue,whereKey=whereKey, whereValue=whereValue,logValues=logValues,result=result)
    if ret['level']<0:
        ret['level'] = 0
    ret['keys'] = ret['keys'][0:ret['level']]
    ret['objects'] = ret['objects'][0:ret['level']]

    return ret
#------------------------
def check(json,text):
    found = False
    data = simplejson.dumps(json, indent=2)
    if text in data:
        print(text)

def getValue(obj,name):
    value = obj[name]
    if 'value' in obj[name]:
        value = obj[name]['value']  
    return value

#set selecte key where keyvalue is selectKeyValue and return jsonDic 
# if set Key provided, will replace the setKeyValue
def parseWhere(json,result,selectKey='', selectKeyValue=None,whereKey=None, whereValue=None,logValues=False):
    def setret(result,json):
        result['object'] = json
        return result      

    result['level']=result['level']+1
    result['objects'].insert(result['level'], json)

    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return setret(result,None)

    for key in json.keys():
        result['keys'].insert(result['level'],key)

        if key == selectKey:
            if selectKeyValue == None:
                if whereKey == None:
                    return setret(result,json[key])

            else:
                value = getValue(json,selectKey) 
                if value == selectKeyValue:
                    if whereKey == None:
                        return setret(result,json)
                    elif whereKey in json:
                        if json[whereKey] == whereValue:
                            return setret(result,json)

        if isinstance(json[key],dict):
            ret = parseWhere(json[key],result,selectKey, selectKeyValue,whereKey,whereValue,logValues)

            if ret['object'] != None:
                return ret

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parseWhere(l,result,selectKey,selectKeyValue,whereKey,whereValue,logValues)
  
                if ret['object'] != None:
                    return ret
    result['level'] = result['level']-1

    result['object'] = None
    return result

def parse(json, selectKey='', selectKeyValue='',setKey='', setKeyValue='',logValues=False,rets=None):
    global ident,treeObjects
    ident=ident+1
    treeObjects.insert(ident, json)
#    print(ident)


    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return ''  #continue

    for key in json.keys():
        keyPath.insert(ident,key)
        if key == 'PricebookEntry':
            continue

        if key == 'ProductCode' and logValues == True:
            printIdent(f'{key}  {json[key]}')

        if key == selectKey:
            if selectKeyValue == '':
                return json
            value = getValue(json,selectKey) 

         #   printIdent(f'{key}  {value}')

            if value == selectKeyValue:
                if setKey!='':
                    if setKeyValue == None:
                        return json[setKey]
                    if json[setKey] != None and type(json[setKey]) is dict and 'value' in json[setKey]:
                        json[setKey]['value'] = setKeyValue
                    else:
                        json[setKey] = setKeyValue
           #     ident = ident-1

                return json 

        if isinstance(json[key],dict):
            ret = parse(json[key],selectKey, selectKeyValue,setKey,setKeyValue)
          #  ident = ident-1

            if ret != '':
                return ret if rets is None else rets.append(json)

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parse(l,selectKey,selectKeyValue,setKey,setKeyValue)
            #    ident = ident-1
  
                if ret != '':
                    return ret if rets is None else rets.append(json)
    ident = ident-1

    return ''

#set selecte key where keyvalue is selectKeyValue and return jsonDic 
# if set Key provided, will replace the setKeyValue
def parseEx(json, selectKey='', selectKeyValue='',setKey='', setKeyValue='',logValues=False,retObjects=[]):
    global ident
    ident=ident+1
  
    #check(json,"AttributeCategory")
    #check(json,"attributeCategories")

    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return ''  #continue

    for key in json.keys():
        if key == 'PricebookEntry':
            continue

        if key == 'ProductCode' and logValues == True:
            printIdent(f'{key}  {json[key]}')

        if key == selectKey:
            value = json[selectKey]
            if 'value' in json[selectKey]:
                value = json[selectKey]['value']
            if value == selectKeyValue:
                if setKey!='':
                    if setKeyValue == None:
                        return json[setKey]
                    if json[setKey] != None and type(json[setKey]) is dict and 'value' in json[setKey]:
                        json[setKey]['value'] = setKeyValue
                    else:
                        json[setKey] = setKeyValue
                #return json     
                retObjects.append(json[selectKey])

        if isinstance(json[key],dict):
            ret = parse(json[key],selectKey, selectKeyValue,setKey,setKeyValue,retObjects)
            if ret != '':
                retObjects.append(ret)
                #return ret
            ident = ident-1

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parse(l,selectKey,selectKeyValue,setKey,setKeyValue,retObjects)
                if ret != '':
                    retObjects.append(json)
                    #return ret
                ident = ident-1
    return retObjects

def addNode(path,node,level):
    if len(path) > level:
        path[level] = node
    else:
        path.append(node) 

def getField(obj,path,separator=':'):
    paths = path.split(separator)
    _obj = obj
    for p in paths:
        if p in _obj:
            _obj = _obj[p]
        else:
            return None
    return _obj

def getpaths_toField(json,fieldValue,level=0,paths=[],path=[]):
    try:
        if type(json) is dict:
            for key in json.keys():
                addNode(path,key,level)

                if isinstance(json[key],dict):
                    getpaths_toField(json[key],fieldValue,level+1,paths,path)
                if isinstance(json[key],list):
                    for element in json[key]:
                        getpaths_toField(element,fieldValue,level+1,paths,path)
                if (json[key]==fieldValue):
                    addNode(path,key,level+1)
                    path =  path[0:level+1]
                    str = ".".join(path)
                    paths.append(str)
    except Exception as e:
        logging.error(f'{e}')
    return paths

def printIdent(string):
    global ident
    str = ''
    for x in range(ident):
        str = str + ' '
    print(str + string)


def getNode(obj,path):
    if (path == ""):
        return obj
    
    nodeNames = path.split(".")

    for nodeName in nodeNames:
        if '*' in nodeName:
            print()
        if nodeName.isnumeric():
            index = int(nodeName)
            if index>len(obj):
                return "Error"
            obj = obj[index]

        else:
            if nodeName in obj:
                obj = obj[nodeName]
            else:
                return "Error: " + nodeName + " not present in Object"

    return obj



