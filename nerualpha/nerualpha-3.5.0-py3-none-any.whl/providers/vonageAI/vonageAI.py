from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.vonageAI.vonageAIActions import VonageAIActions
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.vonageAI.IVonageAI import IVonageAI
from nerualpha.session.ISession import ISession
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAI.contracts.vonageAiAnalyzePayload import VonageAiAnalyzePayload
from nerualpha.providers.vonageAI.contracts.importPayload import ImportPayload
from nerualpha.providers.vonageAI.contracts.vonageAiImportModelPayload import VonageAiImportModelPayload
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback

@dataclass
class VonageAI(IVonageAI):
    session: ISession
    provider: str = field(default = "vonage-overai")
    def __init__(self,session):
        self.session = session
    
    def analyze(self,analyze,callback):
        payload = VonageAiAnalyzePayload(analyze,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,VonageAIActions.Analyze,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def importModel(self,modelAssetName,callback):
        modelAsset = ImportPayload(modelAssetName)
        wrappedCallback = self.session.wrapCallback(callback,[])
        payload = VonageAiImportModelPayload(modelAsset,wrappedCallback)
        action = ActionPayload(self.provider,VonageAIActions.ImportModel,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
