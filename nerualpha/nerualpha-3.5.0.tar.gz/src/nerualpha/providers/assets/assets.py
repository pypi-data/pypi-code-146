from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.config.IConfig import IConfig
from nerualpha.session.ISession import ISession
from nerualpha.providers.assets.IAssets import IAssets
from nerualpha.providers.assets.contracts.directoryPayload import DirectoryPayload
from nerualpha.providers.assets.contracts.removeAssetPayload import RemoveAssetPayload
from nerualpha.providers.assets.contracts.listAssetsPayload import ListAssetsPayload
from nerualpha.IBridge import IBridge
from nerualpha.providers.assets.assetsActions import AssetsActions
from nerualpha.request.requestMethods import RequestMethods
from nerualpha.session.requestInterfaceWithParams import RequestInterfaceWithParams
from nerualpha.request.requestParams import RequestParams
from nerualpha.providers.assets.contracts.linkPayload import LinkPayload
from nerualpha.services.config.urlObject import UrlObject
from nerualpha.providers.assets.contracts.assetLinkResponse import AssetLinkResponse
from nerualpha.providers.assets.contracts.assetListResponse import AssetListResponse

@dataclass
class Assets(IAssets):
    bridge: IBridge
    session: ISession
    config: IConfig
    provider: str = field(default = "vonage-assets")
    def __init__(self,session):
        self.session = session
        self.bridge = session.bridge
        self.config = session.config
    
    def createDir(self,name):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = DirectoryPayload(name)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Mkdir)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def remove(self,remoteFilePath,recursive = False):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = RemoveAssetPayload(remoteFilePath,recursive)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Remove)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def getRemoteFile(self,remoteFilePath):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.GET
        url = self.config.getExecutionUrl(self.provider,AssetsActions.Binary)
        url.query["key"] = remoteFilePath
        requestParams.url = url
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def generateLink(self,remoteFilePath,duration = "5m"):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = LinkPayload(remoteFilePath,duration)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.Link)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def uploadFiles(self,localFilePaths,remoteDir):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        data = {}
        for i in range(0,localFilePaths.__len__()):
            data[f'files[{i}]'] = self.bridge.createReadStream(localFilePaths[i])
        
        requestParams.data = data
        url = self.config.getExecutionUrl(self.provider,AssetsActions.Copy)
        url.query["dst"] = remoteDir
        requestParams.url = url
        requestParams.headers = self.session.constructRequestHeaders()
        requestParams.headers["Content-Type"] = "multipart/form-data"
        return RequestInterfaceWithParams(self.session,requestParams)
    
    def list(self,remotePath,recursive = False,limit = 1000):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.data = ListAssetsPayload(remotePath,recursive,limit)
        requestParams.url = self.config.getExecutionUrl(self.provider,AssetsActions.List)
        requestParams.headers = self.session.constructRequestHeaders()
        return RequestInterfaceWithParams(self.session,requestParams)
    
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
