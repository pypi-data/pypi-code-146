from __future__ import annotations

from tcsoa.gen.Core._2019_06.DataManagement import DeleteIn
from tcsoa.gen.Core._2019_06.Session import LicAdminInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def licenseAdmin(cls, licAdminInput: List[LicAdminInput]) -> ServiceData:
        """
        This operation provides licensing related operations such as check-out and check-in of a license feature key.
        """
        return cls.execute_soa_method(
            method_name='licenseAdmin',
            library='Core',
            service_date='2019_06',
            service_name='Session',
            params={'licAdminInput': licAdminInput},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def unlinkAndDeleteObjects(cls, deleteInput: List[DeleteIn]) -> ServiceData:
        """
        This operation unlinks the input objects from their corresponding container and then attempts to deletes them.
        The input objects are related to the container as the reference or relation property supplied as part of the
        input. The operation also takes a flag whether to unlink the objects from the container in case the deletion
        fails.
        
        After unlinking the objects from the input container, if the objects being deleted are still referenced by
        other objects then error is returned to the caller. Any other error in deletion of the objects are also
        returned to the caller.
        
        In case the input argument objectsToDelete contains objects of type Item, then the operation also deletes all
        ItemRevision objects, associated ItemMaster, ItemRevisionMaster form objects.
        
        If the input argument objectsToDelete are of type ItemRevision and if is the last revision of the Item then the
        operation deletes the Item, associated ItemMaster, ItemRevisionMaster form objects.
        
        The input argument objectsToDelete can be an ImanRelation.
        """
        return cls.execute_soa_method(
            method_name='unlinkAndDeleteObjects',
            library='Core',
            service_date='2019_06',
            service_name='DataManagement',
            params={'deleteInput': deleteInput},
            response_cls=ServiceData,
        )
