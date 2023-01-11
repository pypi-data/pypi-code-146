from __future__ import annotations

from typing import List
from tcsoa.gen.Manufacturing._2019_06.DataManagement import SelectedSyncPublishStudyInput, SelectedStudySourceResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def publishSelectionFromStudyToSource(cls, input: List[SelectedSyncPublishStudyInput]) -> SelectedStudySourceResponse:
        """
        This service operation publishes the changes from Mfg0BvrSimStudy (simulation study) structure to the
        associated Bill Of Process (BOP) structure. It publishes the changes from complete simulation study structure
        or the selected BOPLine objects from the simulation study structure.
        
        Use cases:
        Following use cases are supported.
        &bull;    Use Case 1: User selects one or more object(s) from simulation study structure and selects "Publish
        From Study" command. Only the selected objects are published to the associated BOP structure.
        
        &bull;    Use Case 2: User selects "Publish From Study" command without any selection, all the BOPLine nodes
        under simulation study structure are published to the associated BOP structure.
        """
        return cls.execute_soa_method(
            method_name='publishSelectionFromStudyToSource',
            library='Manufacturing',
            service_date='2019_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=SelectedStudySourceResponse,
        )

    @classmethod
    def syncSelectionInStudyWithSource(cls, input: List[SelectedSyncPublishStudyInput]) -> SelectedStudySourceResponse:
        """
        This service operation synchronizes Mfg0BvrSimStudy (simulation study) structure with the associated Bill Of
        Process (BOP) structure. It synchronizes the complete study structure or the selected BOPLine objects from the
        study.
        
        Use cases:
        Following use cases are supported. 
        &bull;    Use Case 1: User selects one or more object(s) from simulation study and selects "synchronize study"
        command . Only the selected objects are synchronized with the associated Bill Of Process (BOP) structure.
        
        &bull;    Use Case 2: User selects "synchronize study" command without any selection, all the BOPLine nodes
        under simulation study are synchronized with the associated Bill Of Process (BOP) structure.
        """
        return cls.execute_soa_method(
            method_name='syncSelectionInStudyWithSource',
            library='Manufacturing',
            service_date='2019_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=SelectedStudySourceResponse,
        )
