from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.scheduler.contracts.schedulerPayload import SchedulerPayload
from nerualpha.providers.scheduler.contracts.IStartAtParams import IStartAtParams
from nerualpha.providers.scheduler.contracts.listAllSchedulersResponse import ListAllSchedulersResponse
from nerualpha.providers.scheduler.contracts.getSchedulerResponse import GetSchedulerResponse
from nerualpha.providers.scheduler.contracts.listAllPayload import ListAllPayload


#interface
class IScheduler(ABC):
    @abstractmethod
    def startAt(self,params):
        pass
    @abstractmethod
    def listAll(self,size = None,cursor = None):
        pass
    @abstractmethod
    def get(self,scheduleId):
        pass
    @abstractmethod
    def cancel(self,scheduleId):
        pass
