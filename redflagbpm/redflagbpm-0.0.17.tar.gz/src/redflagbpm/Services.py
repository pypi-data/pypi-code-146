from typing import List, Any
import os
from urllib.parse import urlparse
from redflagbpm.BPMService import BPMService


class Service:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def sendMail(self, msg: dict):
        return self.bpm.call("EBHBPMService.sendMail", msg)

    def execute(self, script: str, context: dict):
        return self.bpm.call("EBHBPMService.execute", body={
            "script": script,
            "context": context
        })

    def notifyUser(self, user: str, title: str, description: str, target: str = None, sound: bool = False):
        return self.bpm.call("EBHBPMService.notifyUser", body={
            "user": user,
            "title": title,
            "description": description,
            "target": target,
            "sound": sound})

    def notifyGroup(self, group: str, title: str, description: str, target: str = None, sound: bool = False):
        return self.bpm.call("EBHBPMService.notifyGroup", body={
            "group": group,
            "title": title,
            "description": description,
            "target": target,
            "sound": sound})

    def now(self):
        return self.bpm.call("EBHBPMService.now", body={})

    def today(self):
        return self.bpm.call("EBHBPMService.today", body={})

    def getProperty(self, code: str, the_property: str):
        return self.bpm.call("EBHBPMService.getProperty", body={
            "code": code,
            "property": the_property})

    def text(self, name: str):
        return self.bpm.call("EBHBPMService.text", body={
            "name": name})

    def code(self, name: str):
        return self.bpm.call("EBHBPMService.code", body={
            "name": name})

    def list(self, name: str, the_filter: dict = None):
        return self.bpm.call("EBHBPMService.list", body={
            "name": name,
            "filter": the_filter})

class ContextInput(object):
    def  __getitem__(self, item):
        return self.context.getInputValue(item)

    def __setitem__(self, key, value):
        self.context.setInputValue(key,value)

class ContextJsonValue(object):
    def  __getitem__(self, item):
        return self.context.getJsonValue(self.item,item)

    def __setitem__(self, key, value):
        self.context.setJsonValue(self.item,key,value)

class ContextJson(object):
    def __getattr__(self, item):
        json_value= ContextJsonValue()
        json_value.context=self.context
        json_value.item=item
        try:
            self.context.getValue(item+"!=null")
        except ValueError:
            raise NameError(item) from None
        return json_value

class Context(object):
    bpm: BPMService
    input: ContextInput
    json: ContextJson

    def __init__(self, bpm: BPMService):
        super(Context,self).__setattr__('bpm', bpm)
        super(Context, self).__setattr__('input', ContextInput())
        super(Context, self).__setattr__('json', ContextJson())
        self.input.context=self
        self.json.context=self

    def __setattr__(self, key, value):
        if key in dir(self):
            super(Context,self).__setattr__(key, value)
        else:
            self.setValue(key,value)

    def __getattr__(self, item):
        try:
            return self.getValue(item)
        except ValueError:
            raise NameError(item) from None

    def  __getitem__(self, item):
        try:
            return self.getValue(item)
        except ValueError:
            raise KeyError(item) from None

    def __setitem__(self, key, value):
        return self.setValue(key,value)

    def setValue(self, variable: str, value: Any, address=None):
        self.bpm.exec(script="_____context_____.setAttribute('" + variable + "',_____variable_____,100)",
                      context={"_____variable_____": value},
                      address=address)

    def setJsonValue(self, variable: str, key: str, value: Any, address=None):
        self.bpm.exec(script=variable + ('.put("%s",_____variable_____)' % key),
                      context={"_____variable_____": value},
                      address=address)

    def setDictValue(self, variable: str, key: str, value: Any, address=None):
        self.bpm.exec(script=variable + ('["%s"]=_____variable_____' % key),
                      context={"_____variable_____": value},
                      address=address)

    def setInputValue(self, key: str, value: Any, address=None):
        self.setJsonValue("input", key, value, address)

    def getValue(self, variable: str, address=None):
        return self.bpm.exec(script=variable, address=address)

    def getJsonValue(self, variable: str, key: str, address=None):
        return self.bpm.exec(script=variable + ('.getValue("%s")' % key),
                             address=address)

    def getDictValue(self, variable: str, key: str, address=None):
        return self.bpm.exec(script=variable + ('["%s"]' % key),
                             address=address)

    def getInputValue(self, key: str, address=None):
        return self.getJsonValue("input", key, address)


class ResourceService:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def accessFile(self, path: str):
        file_url = self.accessPath(path)
        p = urlparse(file_url)
        return os.path.abspath(os.path.join(p.netloc, p.path))

    def accessTempFile(self, path: str):
        file_url = self.accessTempPath(path)
        p = urlparse(file_url)
        return os.path.abspath(os.path.join(p.netloc, p.path))

    def accessPath(self, path: str):
        return self.bpm.call("EBHBPMResourceService.accessPath", body={"path": path})

    def accessTempPath(self, path: str):
        return self.bpm.call("EBHBPMResourceService.accessTempPath", body={"path": path})

    def getResourceInfo(self, path: str):
        return self.bpm.call("EBHBPMResourceService.getResourceInfo", body={"path": path})

    def listPaths(self, path: str):
        return self.bpm.call("EBHBPMResourceService.listPaths", body={"path": path})


class DocumentService:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def registerCollection(self, schema: dict):
        return self.bpm.call("EBHBPMDocumentService.registerCollection", body={"schema": schema})

    def unregisterCollection(self, collection: str) -> bool:
        return self.bpm.call("EBHBPMDocumentService.unregisterCollection", body={"collection": collection})

    def listCollections(self) -> List[str]:
        return self.bpm.call("EBHBPMDocumentService.listCollections", body={})

    def getSchema(self, collection: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.getSchema", body={"collection": collection})

    def create(self, collection: str, theObject: dict) -> str:
        return self.bpm.call("EBHBPMDocumentService.create", body={"collection": collection, "object": theObject})

    def createList(self, collection: str, theObject: List[dict]):
        return self.bpm.call("EBHBPMDocumentService.createList", body={"collection": collection, "object": theObject})

    def readByOid(self, oid: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.readByOid", body={"oid": oid})

    def readById(self, collection: str, theId: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.readById", body={"collection": collection, "id": theId})

    def readList(self, collection: str, criteria: str = None, parameters: dict = None, sorting: str = None) -> \
            List[dict]:
        return self.bpm.call("EBHBPMDocumentService.readList",
                             body={"collection": collection, "criteria": criteria, "parameters": parameters,
                                   "sorting": sorting})

    def upsert(self, collection: str, theObject: dict) -> str:
        return self.bpm.call("EBHBPMDocumentService.upsert", body={"collection": collection, "object": theObject})

    def updateByCriteria(self, collection: str, toSet: dict, criteria: str = None, parameters: dict = None) -> int:
        return self.bpm.call("EBHBPMDocumentService.updateByCriteria",
                             body={"collection": collection, "criteria": criteria,
                                   "set": toSet,
                                   "parameters": parameters})

    def updateById(self, collection: str, theId: str, toSet: dict) -> bool:
        return self.bpm.call("EBHBPMDocumentService.updateById", body={"collection": collection,
                                                                       "id": theId,
                                                                       "set": toSet})

    def updateByOid(self, collection: str, oid: str, toSet: dict) -> bool:
        return self.bpm.call("EBHBPMDocumentService.updateByOid", body={"collection": collection,
                                                                        "oid": oid,
                                                                        "set": toSet})

    def deleteByOid(self, oid: str) -> bool:
        return self.bpm.call("EBHBPMDocumentService.deleteByOid", body={"oid": oid})

    def deleteById(self, collection: str, theId: str) -> dict:
        return self.bpm.call("EBHBPMDocumentService.deleteById", body={"collection": collection, "id": theId})

    def deleteByCriteria(self, collection: str, criteria: str = None, parameters: dict = None) -> int:
        return self.bpm.call("EBHBPMDocumentService.updateByCriteria",
                             body={"collection": collection, "criteria": criteria, "parameters": parameters})


class RuntimeService:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def startProcessInstanceByKey(self, processDefinitionKey: str, businessKey: str, variables: dict):
        return self.bpm.call("EBHBPMRuntime.startProcessInstanceByKey", body={
            "processDefinitionKey": processDefinitionKey, "businessKey": businessKey, "variables": variables})

    def startProcessInstanceByKeyAndTenantId(self, processDefinitionKey: str, businessKey: str, tenantId: str,
                                             variables: dict):
        return self.bpm.call("EBHBPMRuntime.startProcessInstanceByKeyAndTenantId", body={
            "processDefinitionKey": processDefinitionKey, "businessKey": businessKey, "tenantId": tenantId,
            "variables": variables})

    def startProcessInstanceById(self, processDefinitionId: str, businessKey: str, variables: dict):
        return self.bpm.call("EBHBPMRuntime.startProcessInstanceById", body={
            "processDefinitionId": processDefinitionId, "businessKey": businessKey, "variables": variables})

    def startProcessInstanceByMessage(self, messageName: str, businessKey: str, variables: dict):
        return self.bpm.call("EBHBPMRuntime.startProcessInstanceByMessage", body={
            "messageName": messageName, "businessKey": businessKey, "variables": variables})

    def startProcessInstanceByMessageAndTenantId(self, messageName: str, businessKey: str, tenantId: str,
                                                 variables: dict):
        return self.bpm.call("EBHBPMRuntime.startProcessInstanceByMessageAndTenantId", body={
            "messageName": messageName, "businessKey": businessKey, "tenantId": tenantId,
            "variables": variables})

    def deleteProcessInstance(self, processInstanceId: str, deleteReason: str):
        self.bpm.call("EBHBPMRuntime.deleteProcessInstance", body={
            "processInstanceId": processInstanceId, "deleteReason": deleteReason})

    def updateBusinessKey(self, processInstanceId: str, businessKey: str):
        self.bpm.call("EBHBPMRuntime.updateBusinessKey", body={
            "processInstanceId": processInstanceId, "businessKey": businessKey})

    def setProcessInstanceName(self, processInstanceId: str, name: str):
        self.bpm.call("EBHBPMRuntime.setProcessInstanceName",
                      body={"processInstanceId": processInstanceId, "name": name})

    def getVariables(self, executionId: str):
        return self.bpm.call("EBHBPMRuntime.getVariables", body={"executionId": executionId})

    def getVariable(self, executionId: str, variableName: str):
        return self.bpm.call("EBHBPMRuntime.getVariable",
                             body={"executionId": executionId, "variableName": variableName})

    def hasVariable(self, executionId: str, variableName: str):
        return self.bpm.call("EBHBPMRuntime.hasVariable",
                             body={"executionId": executionId, "variableName": variableName})

    def setVariable(self, executionId: str, variableName: str, value: Any):
        return self.bpm.call("EBHBPMRuntime.setVariable",
                             body={"executionId": executionId, "variableName": variableName, "value": value})

    def removeVariable(self, executionId: str, variableName: str):
        self.bpm.call("EBHBPMRuntime.removeVariable",
                      body={"executionId": executionId, "variableName": variableName})

    def signalEventReceived(self, executionId: str, signalName: str, processVariables: dict):
        self.bpm.call("EBHBPMRuntime.signalEventReceived",
                      body={"executionId": executionId, "signalName": signalName,
                            "processVariables": processVariables})

    def messageEventReceived(self, executionId: str, messageName: str, processVariables: dict):
        self.bpm.call("EBHBPMRuntime.messageEventReceived",
                      body={"executionId": executionId, "messageName": messageName,
                            "processVariables": processVariables})


class ExecutionService:
    bpm: BPMService

    def __init__(self, bpm: BPMService):
        self.bpm = bpm

    def updateBusinessKey(self, businessKey: str):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        self.bpm.call("EBHBPMRuntime.updateBusinessKey", body={
            "processInstanceId": process_instance_id, "businessKey": businessKey})

    def setProcessInstanceName(self, name: str):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        self.bpm.call("EBHBPMRuntime.setProcessInstanceName",
                      body={"processInstanceId": process_instance_id, "name": name})

    def getVariables(self):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        return self.bpm.call("EBHBPMRuntime.getVariables", body={"executionId": process_instance_id})

    def getVariable(self, variableName: str):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        return self.bpm.call("EBHBPMRuntime.getVariable",
                             body={"executionId": process_instance_id, "variableName": variableName})

    def hasVariable(self, variableName: str):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        return self.bpm.call("EBHBPMRuntime.hasVariable",
                             body={"executionId": process_instance_id, "variableName": variableName})

    def setVariable(self, variableName: str, value: Any):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        return self.bpm.call("EBHBPMRuntime.setVariable",
                             body={"executionId": process_instance_id, "variableName": variableName, "value": value})

    def removeVariable(self, variableName: str):
        process_instance_id = self.bpm.context.getValue('execution.getProcessInstanceId()')
        self.bpm.call("EBHBPMRuntime.removeVariable",
                      body={"executionId": process_instance_id, "variableName": variableName})
