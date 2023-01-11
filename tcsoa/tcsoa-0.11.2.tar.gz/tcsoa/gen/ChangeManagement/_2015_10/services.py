from __future__ import annotations

from tcsoa.gen.ChangeManagement._2015_10.ChangeManagement import CreateChangeLineageInputData, CreateChangeLineageResponse, DeleteChangeLineageInputData
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def deleteChangeLineage(cls, inputs: List[DeleteChangeLineageInputData]) -> ServiceData:
        """
        This operation deletes the change lineage by deleting the relations between a group of solution items and their
        respective impacted items that are associated with the lineage group. Each DeleteChangeLineageInputData
        structure passed as input will have the clientId to uniquely identify each input, the ChangeNoticeRevision and
        the list of objects for which the lineage has to be deleted. Lineage group is determined for each object and
        all the relations belonging to the same lineage group will be deleted.
        
        Use cases:
        For a ChangeNoticeRevision, change lineage creation is the ability to relate a group of solution items with
        their respective impacted items and designate an associated lineage group. This operation allows deleting
        change lineage.
        """
        return cls.execute_soa_method(
            method_name='deleteChangeLineage',
            library='ChangeManagement',
            service_date='2015_10',
            service_name='ChangeManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def createChangeLineage(cls, input: List[CreateChangeLineageInputData]) -> CreateChangeLineageResponse:
        """
        This operation creates CMSolutionToImpacted relation between all the Solution Items and all the Impacted Items
        for a ChangeNoticeRevision and then assign a group ID to them. To determine the group ID, the
        CMSolutionToImpacted relations are traversed for ChangeNoticeRevision and then find the largest group ID number
        present for this ChangeNoticeRevision in context. The new group ID is the next incremented number. This group
        number is assigned to all the CMSolutionToImpacted relations created for the input data.
        Each CreateChangeLineageInputData input will have new group id assigned for the relations created for that
        group.
        
        Note: Solution Items and Impacted Items are the objects which are attached to ChangeNoticeRevision using
        CMHasSolutionItem and CMHasImpactedItem relation respectively.
        
        Use cases:
        User selects Solution Items and Impacted Items for a ChangeNoticeRevision and create lineage between them.
        """
        return cls.execute_soa_method(
            method_name='createChangeLineage',
            library='ChangeManagement',
            service_date='2015_10',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=CreateChangeLineageResponse,
        )
