from __future__ import annotations

from tcsoa.gen.Internal.GlobalMultiSite._2008_06.Synchronizer import TransferFormula, GetExportedObjectsResponse
from typing import List
from tcsoa.gen.Internal.GlobalMultiSite._2007_06.Synchronizer import SyncResponse, ObjectsByClass
from tcsoa.base import TcService


class SynchronizerService(TcService):

    @classmethod
    def getCandidatesForClasseswOpts(cls, targetSite: int, classList: List[str], transferFormula: TransferFormula) -> SyncResponse:
        """
        This is an internal operation which returns a list of candidates that need to be synchronized based on the
        input set of classes and target site. Candidates for the synchronization will be identified based on the
        ImanExportRecord availability for the objects of input class or transfer formula passed to this operation.
        
        Use cases:
        
        """
        return cls.execute_soa_method(
            method_name='getCandidatesForClasseswOpts',
            library='Internal-GlobalMultiSite',
            service_date='2008_06',
            service_name='Synchronizer',
            params={'targetSite': targetSite, 'classList': classList, 'transferFormula': transferFormula},
            response_cls=SyncResponse,
        )

    @classmethod
    def getCandidatesForObjectswOpts(cls, targetSite: int, objectList: List[ObjectsByClass], transferFormula: TransferFormula) -> SyncResponse:
        """
        This is an internal operation. It returns a list of candidates for synchronization. User can specify particular
        objects and class to which it belongs. If objects are specified then only those objects are checked for
        modification. If objects are not specified, all the objects belonging to that class are checked for
        synchronization. Objects that are replicated at target site are taken into account. If invalid class is
        provided, it gets ignored.
        
        Use cases:
        Find modified objects since last export for a particular class and set of objects belonging to that class.
        """
        return cls.execute_soa_method(
            method_name='getCandidatesForObjectswOpts',
            library='Internal-GlobalMultiSite',
            service_date='2008_06',
            service_name='Synchronizer',
            params={'targetSite': targetSite, 'objectList': objectList, 'transferFormula': transferFormula},
            response_cls=SyncResponse,
        )

    @classmethod
    def getExportedObjects(cls, targetSiteId: int, classList: List[str]) -> GetExportedObjectsResponse:
        """
        This operation returns a list of objects that were exported to the target site for a given list of classes.
        
        Use cases:
        
        """
        return cls.execute_soa_method(
            method_name='getExportedObjects',
            library='Internal-GlobalMultiSite',
            service_date='2008_06',
            service_name='Synchronizer',
            params={'targetSiteId': targetSiteId, 'classList': classList},
            response_cls=GetExportedObjectsResponse,
        )
