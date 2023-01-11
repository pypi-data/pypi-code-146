from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.assets.contracts.directoryPayload import DirectoryPayload
from nerualpha.providers.assets.contracts.listAssetsPayload import ListAssetsPayload
from nerualpha.providers.assets.contracts.removeAssetPayload import RemoveAssetPayload
from nerualpha.session.requestInterfaceWithParams import RequestInterfaceWithParams
from nerualpha.providers.assets.contracts.linkPayload import LinkPayload
from nerualpha.providers.assets.contracts.assetLinkResponse import AssetLinkResponse
from nerualpha.providers.assets.contracts.assetListResponse import AssetListResponse


#interface
class IAssets(ABC):
    @abstractmethod
    def createDir(self,name):
        pass
    @abstractmethod
    def remove(self,remoteFilePath,recursive):
        pass
    @abstractmethod
    def getRemoteFile(self,remoteFilePath):
        pass
    @abstractmethod
    def generateLink(self,remoteFilePath,duration):
        pass
    @abstractmethod
    def uploadFiles(self,localFilePaths,remoteDir):
        pass
    @abstractmethod
    def list(self,remotePath,recursive,limit):
        pass
