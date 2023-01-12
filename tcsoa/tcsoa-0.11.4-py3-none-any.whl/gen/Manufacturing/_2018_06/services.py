from __future__ import annotations

from tcsoa.gen.Manufacturing._2018_06.DataManagement import GetOccKinematicsInfoInput, OccKinematicsInfoMap, GetOccurrenceKinematicsInfoResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def setOccurrenceKinematicsInformation(cls, occInfoInputMap: OccKinematicsInfoMap) -> ServiceData:
        """
        In Line Designer (LD) and Process Simulate (PS), resource occurrence used has specific poses and joint values.
        This operation creates a relation between AbsOccData and Mfg0OccKinematicsInfo using relation
        Mfg0OccKinematicsRel. The occurrence kinematics information is stored as an XML reference on the dataset
        Mfg0OccKinematicsInfo
        
        Use cases:
        Line Designer or Process Simulate user wants to set the occurrence kinematics information for occurrence of
        Mfg0MEResourceRevision or ItemRevision
        """
        return cls.execute_soa_method(
            method_name='setOccurrenceKinematicsInformation',
            library='Manufacturing',
            service_date='2018_06',
            service_name='DataManagement',
            params={'occInfoInputMap': occInfoInputMap},
            response_cls=ServiceData,
        )

    @classmethod
    def getOccurrenceKinematicsInformation(cls, occKinematicsInfoinput: List[GetOccKinematicsInfoInput]) -> GetOccurrenceKinematicsInfoResponse:
        """
        In Line Designer (LD) and Process Simulate (PS), resource occurrence has specific poses and joint values. This
        operation retrieves occurrence kinematics information of Mfg0MEResourceRevision or ItemRevision from Bill of
        Equipment structure for the given scope Mfg0BvrWorkarea and context Mfg0BvrWorkarea acting as a root of the
        structure
        
        Use cases:
        Line Designer or Process Simulate user wants to get the occurrence kinematics information for occurrence of
        Mfg0MEResourceRevision or ItemRevision from Bill of Equipment structure
        """
        return cls.execute_soa_method(
            method_name='getOccurrenceKinematicsInformation',
            library='Manufacturing',
            service_date='2018_06',
            service_name='DataManagement',
            params={'occKinematicsInfoinput': occKinematicsInfoinput},
            response_cls=GetOccurrenceKinematicsInfoResponse,
        )
