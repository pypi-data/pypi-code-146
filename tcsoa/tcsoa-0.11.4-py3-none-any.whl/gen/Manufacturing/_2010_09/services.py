from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2010_09.TimeManagement import CalculateCriticalPathResponseEx, GetActivityTimesResponse
from tcsoa.gen.Manufacturing._2010_09.Core import FindNodeInContextResponse, GetAffectedPropertiesArg, FindNodeInContextInputInfo
from tcsoa.gen.Manufacturing._2010_09.ImportExport import ImportInput, ImportResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importManufaturingFeatures(cls, input: ImportInput) -> ImportResponse:
        """
        imports MFGs from a given PLMXML file to TC.
        """
        return cls.execute_soa_method(
            method_name='importManufaturingFeatures',
            library='Manufacturing',
            service_date='2010_09',
            service_name='ImportExport',
            params={'input': input},
            response_cls=ImportResponse,
        )


class TimeManagementService(TcService):

    @classmethod
    def populateAllocatedTimeProperties(cls, rootNodes: List[BusinessObject], propagateZeroValues: bool, stopLevel: int, precedence: List[str]) -> ServiceData:
        """
        Updates the allocated time property recursively for all nodes of a list of process or operation trees.
        """
        return cls.execute_soa_method(
            method_name='populateAllocatedTimeProperties',
            library='Manufacturing',
            service_date='2010_09',
            service_name='TimeManagement',
            params={'rootNodes': rootNodes, 'propagateZeroValues': propagateZeroValues, 'stopLevel': stopLevel, 'precedence': precedence},
            response_cls=ServiceData,
        )

    @classmethod
    def updateTimeManagementProperties(cls, rootNodes: List[BusinessObject], fieldNames: List[str]) -> ServiceData:
        """
        Recomputes the cached values of the runtime properties related to TimeManagement for one or more process or
        operation trees. This will affect the properties of all nodes of the tree structures defined by the rootNodes
        parameter.
        """
        return cls.execute_soa_method(
            method_name='updateTimeManagementProperties',
            library='Manufacturing',
            service_date='2010_09',
            service_name='TimeManagement',
            params={'rootNodes': rootNodes, 'fieldNames': fieldNames},
            response_cls=ServiceData,
        )

    @classmethod
    def getActivityTimes(cls, rootNodes: List[BusinessObject]) -> GetActivityTimesResponse:
        """
        Traverses a set of process or operation trees and computes the effective accumulated times of all leaf
        activities, ignoring any flows between processes, operations or activities.  For each activity category that is
        encountered, a distinct value is returned.
        """
        return cls.execute_soa_method(
            method_name='getActivityTimes',
            library='Manufacturing',
            service_date='2010_09',
            service_name='TimeManagement',
            params={'rootNodes': rootNodes},
            response_cls=GetActivityTimesResponse,
        )

    @classmethod
    def calculateCriticalPathEx(cls, roots: List[BusinessObject], processLeafNodes: bool) -> CalculateCriticalPathResponseEx:
        """
        This operation computes the critical paths for processes or operations. The critical path is the sequence of
        processes or operations that determine the minimum duration of a specific object.  If the processLeafNodes flag
        is set, the algorithm will traverse down the structure until it finds all leaf nodes that make up the path.
        Otherwise only the direct children will be taken into account.
        """
        return cls.execute_soa_method(
            method_name='calculateCriticalPathEx',
            library='Manufacturing',
            service_date='2010_09',
            service_name='TimeManagement',
            params={'roots': roots, 'processLeafNodes': processLeafNodes},
            response_cls=CalculateCriticalPathResponseEx,
        )


class CoreService(TcService):

    @classmethod
    def findNodeInContext(cls, input: List[FindNodeInContextInputInfo]) -> FindNodeInContextResponse:
        """
        Finding parallel line in a given window of a given line.
        """
        return cls.execute_soa_method(
            method_name='findNodeInContext',
            library='Manufacturing',
            service_date='2010_09',
            service_name='Core',
            params={'input': input},
            response_cls=FindNodeInContextResponse,
        )

    @classmethod
    def getAffectedProperties(cls, arguments: List[GetAffectedPropertiesArg], requestedProperties: List[str]) -> ServiceData:
        """
        Returns the runtime properties of dependent nodes which are affected when the duration of one or more nodes has
        been changed in a process or operation structure.
        """
        return cls.execute_soa_method(
            method_name='getAffectedProperties',
            library='Manufacturing',
            service_date='2010_09',
            service_name='Core',
            params={'arguments': arguments, 'requestedProperties': requestedProperties},
            response_cls=ServiceData,
        )
