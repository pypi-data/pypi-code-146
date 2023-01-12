from __future__ import annotations

from tcsoa.gen.AuthorizedDataAccess._2009_10.LicenseManagement import LicenseInput, GetLicenseDetailsResponse, LicenseDetails
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LicenseManagementService(TcService):

    @classmethod
    def setLicenseDetails(cls, licenseInfo: List[LicenseDetails]) -> ServiceData:
        """
        This operation creates or modifies an ADA_License business object for each 'LicenseDetails' supplied. The
        'LicenseDetails' contains information for properties such as license type, license ID, expiry date, lock date,
        reason, in accordance with, and associated users and groups, for a given license. If a specified license ID
        already exists, the rest of the property values are updated on that license. However, if the license ID does
        not exist, then a new license of the specified type and ID will be created, and the rest of the properties are
        set on the created license. The user performing the operation will need the privilege specified in the
        ADA_license_administration_privilege site preference to create/modify an ADA License. If a user does not have
        the necessary privilege or if there is a validation error, the operation would fail and the error is returned
        in the 'ServiceData'.
        
        Use cases:
        Use Case 1: Create an ADA license
        You can create a new ADA license of type ITAR/IP/Exclude using 'setLicenseDetails' operation by providing a
        unique license ID for the license using 'LicenseDetails' structure.
        
        Use Case 2: Modify an ADA License
        The following types of modifications can be done on existing ADA licenses using 'setLicenseDetails' operation.
        Other than the license ID and license type, all other parameters of the ADA licenses can be modified using this
        operation.
        - Set an expiry or lock date on a license
        - Unlock licenses by specifying a NULL date or a future date for lockDate parameter
        - Add new users and/or groups to a license
        - Remove users and/or groups from a license
        - Specify value for qualifying code of federal regulations for ITAR licenses
        - Set reason for a license
        
        """
        return cls.execute_soa_method(
            method_name='setLicenseDetails',
            library='AuthorizedDataAccess',
            service_date='2009_10',
            service_name='LicenseManagement',
            params={'licenseInfo': licenseInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def attachLicenses(cls, attachLicense: List[LicenseInput]) -> ServiceData:
        """
        This operation attaches ADA_License business objects to WorkspaceObject business objects such as Item,
        ItemRevision, Dataset, etc. as specified in each 'LicenseInput'. Optionally, this operation can set/update
        authorizing paragraph information for the ITAR licenses being attached. Users performing this operation will
        need IP_ADMIN privilege to both the workspace objects and the licenses being attached, if the licenses are of
        type IP or Exclude, while ITAR_ADMIN privilege is needed to both the workspace objects and the licenses being
        attached, if the licenses are of ITAR license type. If the user does not have necessary privilege to attach any
        licenses, or if there is any other error while attaching licenses, the errors are returned as partial errors in
        'ServiceData'.
        
        Use cases:
        Use case 1: Attach ADA licenses to WorkspaceObject business objects
        You can attach ADA_License business objects of ITAR/IP/Exclude type to classified WorkspaceObject business
        objects using 'attachLicenses' operation to grant access for users and/or groups listed on the licenses.
        Optionally, authorizing paragraph information can be specified for the ITAR licenses being attached through
        'LicenseInput' structure.
        
        Use Case 2: Modify authorizing paragraph for an attached ITAR license
        You can modify the authorizing paragraph information associated with an ITAR license already attached to a
        WorkspaceObject business object by passing in the license ID of the ITAR license, the WorkspaceObject business
        object and the modified authorizing paragraph information in 'LicenseInput' structure using 'attachLicenses'
        operation.
        """
        return cls.execute_soa_method(
            method_name='attachLicenses',
            library='AuthorizedDataAccess',
            service_date='2009_10',
            service_name='LicenseManagement',
            params={'attachLicense': attachLicense},
            response_cls=ServiceData,
        )

    @classmethod
    def getLicenseDetails2(cls, licenseIds: List[str]) -> GetLicenseDetailsResponse:
        """
        This operation gets the properties for each ADA_License business object specified in 'licenseIds' and returns
        them in 'LicenseDetails' structures as part of 'GetLicenseDetailsResponse'. The 'LicenseDetails' contains
        information for properties such as license type, license ID, expiry date, lock date, reason, in accordance
        with, and associated users and groups, for a given license. If there is no matching license for a given license
        ID, LicenseDetails structure for that license will contain 'Not_found' as the value for license ID, while the
        rest of the parameters will contain NULL values. However, if the user does not have READ privilege to any
        license or if there is any unexpected error while getting property information, the errors are returned in the
        'ServiceData' of 'GetLicenseDetailsResponse'.
        
        Use cases:
        Use Case 1: Get properties of an ADA License
        You can get properties of an ADA_License business object of type ITAR/IP/Exclude using 'getLicenseDetails2'
        operation by providing license ID for the license.
        
        Use Case 2: Check the existence of an ADA License
        You can check if an ADA_License businesses object with given license ID exists using 'getLicenseDetails2'
        operation.
        """
        return cls.execute_soa_method(
            method_name='getLicenseDetails2',
            library='AuthorizedDataAccess',
            service_date='2009_10',
            service_name='LicenseManagement',
            params={'licenseIds': licenseIds},
            response_cls=GetLicenseDetailsResponse,
        )
