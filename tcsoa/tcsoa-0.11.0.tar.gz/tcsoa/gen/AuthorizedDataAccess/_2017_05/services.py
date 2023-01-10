from __future__ import annotations

from tcsoa.gen.AuthorizedDataAccess._2017_05.LicenseManagement import LicenseAttachOrDetachInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LicenseManagementService(TcService):

    @classmethod
    def attachOrDetachLicensesFromObjects(cls, licenseAttachOrDetachInput: List[LicenseAttachOrDetachInput]) -> ServiceData:
        """
        This operation attaches or detaches ADA_License objects to WorkspaceObject objects such as Item, ItemRevision,
        Dataset, etc. as specified in each LicenseAttachOrDetachInput. Optionally, this operation can set/update
        authorizing paragraph information for the ITAR licenses being attached. Users performing this operation will
        need IP_ADMIN privilege to both the workspace objects and the licenses being attached, if the licenses are of
        type IP or Exclude, while ITAR_ADMIN privilege is needed to both the workspace objects and the licenses being
        attached, if the licenses are of ITAR license type. If the user does not have necessary privilege to attach any
        licenses, or if there is any other error while attaching licenses, the errors are returned as partial errors in
        ServiceData.
        
        Use cases:
        - You can attach ADA_License business objects to classified WorkspaceObject business objects to grant access
        for users and/or groups listed on the licenses in context of structure configuration.
        - You can remove ADA_License business objects from classified WorkspaceObject business objects to revoke access
        for users and/or groups listed on the licenses in context of structure configuration.
        
        """
        return cls.execute_soa_method(
            method_name='attachOrDetachLicensesFromObjects',
            library='AuthorizedDataAccess',
            service_date='2017_05',
            service_name='LicenseManagement',
            params={'licenseAttachOrDetachInput': licenseAttachOrDetachInput},
            response_cls=ServiceData,
        )
