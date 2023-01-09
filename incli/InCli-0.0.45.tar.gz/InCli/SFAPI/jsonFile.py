import simplejson as json
import os

from . import file,utils

def writeFileinFolder(folder,filename,data):
    return write(f"{folder}/{filename}",data)

def write(filepath,data):
    filepath = file.addExtension(filepath,'json')
    str = json.dumps(data, indent=2)
    return file.write(filepath,str,'w')

def readFolder(folder,filename):
    read(f"{folder}/{filename}")

def read(filepath):
    filepath = file.addExtension(filepath,'json')
    str = file.read(filepath)
   # obj = None
    try:
        obj= json.loads(str)
    
    except ValueError as e:
        extra = e.args[0] if len(e.args)>0 else ''
        utils.raiseException(f'JSON_PARSING:{type(e)}',f"{e.msg} {extra}",other=f"File {filepath} seems to be a malformed JSON?")
        #utils.printException(e)
    return obj

#looks for a field targetKey with value targeValue and optionally ¡n the same object/dictionary replaces the targetKey with the targetValue
def parse(json, targetKey='', targetKeyValue='',replaceKey='', replaceValue='',printProducts=False):

    #if it is not a dictionary or an array, its a value so return
    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return ''  #continue

    for key in json.keys():
        if key == 'PricebookEntry':  #breaks it
            continue

        if key == targetKey:
            value = json[key]
            if 'value' in json[key]:  #sometime the value is in a nested filed called value
                value = json[key]['value']
            if value == targetKeyValue:
                if replaceKey!='':
                    json[replaceKey] = replaceValue
                return json     

        if isinstance(json[key],dict):
            ret = parse(json[key],targetKey, targetKeyValue,replaceKey,replaceValue)
            if ret != '':
                return ret
            ident = ident-1

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parse(l,targetKey,targetKeyValue,replaceKey,replaceValue)
                if ret != '':
                    return ret
                ident = ident-1
    return ''
    
def getChild(json,name):
    for key in json.keys():
        if key == name:
            return json[key]
    return ''
