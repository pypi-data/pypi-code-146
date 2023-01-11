from __future__ import annotations

from tcsoa.gen.Manufacturing._2008_06.TimeManagement import TimeAnalysisInputs, AllocatedTime, TimeAnalysisRollupResponse, AllocatedTimeResponse
from tcsoa.gen.BusinessObjects import BusinessObject, Folder
from tcsoa.gen.Manufacturing._2008_06.DataManagement import CreateOrUpdateMEActivityFolderResponse, MEActivityFolderInfo, CreateOrUpdateMENXObjectResponse, MENXObjectInfo
from tcsoa.gen.Manufacturing._2008_06.Core import FindCheckedOutsInStructureResponse
from typing import List
from tcsoa.base import TcService


class TimeManagementService(TcService):

    @classmethod
    def timeAnalysisRollup(cls, inputs: TimeAnalysisInputs) -> TimeAnalysisRollupResponse:
        """
        Calculates the total time for each activity category under a requested bop line.
        An additional calculation is all the run time propertie related to the bop line time calculations
        such as total time and duration time.
        """
        return cls.execute_soa_method(
            method_name='timeAnalysisRollup',
            library='Manufacturing',
            service_date='2008_06',
            service_name='TimeManagement',
            params={'inputs': inputs},
            response_cls=TimeAnalysisRollupResponse,
        )

    @classmethod
    def allocatedTimeRollUp(cls, object: AllocatedTime) -> AllocatedTimeResponse:
        """
        Calculates the allocated time for each requested bop line.
        """
        return cls.execute_soa_method(
            method_name='allocatedTimeRollUp',
            library='Manufacturing',
            service_date='2008_06',
            service_name='TimeManagement',
            params={'object': object},
            response_cls=AllocatedTimeResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateMEActivityFolders(cls, activityInfos: List[MEActivityFolderInfo]) -> CreateOrUpdateMEActivityFolderResponse:
        """
        Allows the user to create and/or update a MEActivityFolder.  If the given MEActivity object
        exists but the input attribute values that differ from those already set, an attempt is made
        to update the values if possible.
        If multiple level of sub activities are to be created those activities can be passed in as
        the objects if they already exist in database. The created folder and updated folders are returned
        to the client through the createdObjects and updatedObject list of the service data respectively.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateMEActivityFolders',
            library='Manufacturing',
            service_date='2008_06',
            service_name='DataManagement',
            params={'activityInfos': activityInfos},
            response_cls=CreateOrUpdateMEActivityFolderResponse,
        )

    @classmethod
    def createOrUpdateMENXObjects(cls, meObjectInfos: List[MENXObjectInfo], container: Folder) -> CreateOrUpdateMENXObjectResponse:
        """
        Allows the user to create and/or update a MENXObject. If the given MENXObject object
        exists but the input attribute values that differ from those already set, an attempt
        is made to update the values if possible.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateMENXObjects',
            library='Manufacturing',
            service_date='2008_06',
            service_name='DataManagement',
            params={'meObjectInfos': meObjectInfos, 'container': container},
            response_cls=CreateOrUpdateMENXObjectResponse,
        )


class CoreService(TcService):

    @classmethod
    def findCheckedOutsInStructure(cls, searchScope: List[BusinessObject]) -> FindCheckedOutsInStructureResponse:
        """
        Finds all the checked out items in the objects.
        """
        return cls.execute_soa_method(
            method_name='findCheckedOutsInStructure',
            library='Manufacturing',
            service_date='2008_06',
            service_name='Core',
            params={'searchScope': searchScope},
            response_cls=FindCheckedOutsInStructureResponse,
        )
