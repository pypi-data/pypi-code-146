from __future__ import annotations

from tcsoa.gen.AuthorizedDataAccess._2007_06.LicenseManagement import LicenseInput, LicenseTypeAndStatusFilter, LicenseIdsAndTypesResponse, LicenseDetails, GetLicenseDetailsResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LicenseManagementService(TcService):

    @classmethod
    def removeLicenses(cls, removeLicense: List[LicenseInput]) -> ServiceData:
        """
        This operation removes/detaches ADA Licenses from WorkspaceObject business objects such as Item, ItemRevision,
        Dataset, etc. as specified in each LicenseInput. LicenseInput provides details of the licenses to be removed,
        and the WorkspaceObject business objects to remove the licenses from. Users performing this operation will need
        IP_ADMIN privilege to both the workspace objects and the licenses being removed, if the licenses are of type IP
        or Exclude, while the privilege specified in ADA_license_administration_privilege site preference is needed to
        both the workspace objects and the licenses being removed if the licenses are of ITAR license type. If the user
        does not have necessary privilege to remove any licenses, or if there is any other error while removing
        licenses, the errors are returned as partial errors in ServiceData.
        
        Use cases:
        Use case: 
        You can remove ADA_License business objects from classified WorkspaceObject business objects to revoke access
        for users and/or groups listed on the licenses.
        """
        return cls.execute_soa_method(
            method_name='removeLicenses',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'removeLicense': removeLicense},
            response_cls=ServiceData,
        )

    @classmethod
    def setLicenseDetails(cls, licenseInfo: List[LicenseDetails]) -> ServiceData:
        """
        This operation creates or modifies an ADA_License business object for each 'LicenseDetails' supplied. The
        'LicenseDetails' contains information for properties such as license type, license ID, expiry date, reason, and
        associated users and groups, for a given license. If a specified license ID already exists, the rest of the
        property values are updated on that license. However, if the license ID does not exist, then a new license of
        the specified type and ID will be created, and the rest of the properties are set on the created license. The
        user performing the operation will need the privilege specified in the ADA_license_administration_privilege
        site preference to create/modify an ADA License. If a user does not have the necessary privilege or if there is
        a validation error, the operation would fail and the error is returned in the 'ServiceData'.
        
        Use cases:
        Use Case 1: Create an ADA license
        You can create a new ADA license of type ITAR/IP/Exclude using 'setLicenseDetails' operation by providing a
        unique license ID for the license using 'LicenseDetails' structure.
        
        Use Case 2: Modify an ADA License
        The following types of modifications can be done on existing ADA licenses using 'setLicenseDetails' operation.
        Other than the license ID and license type, all other parameters of the ADA licenses can be modified using this
        operation.
        - Set an expiry date on a license
        - Add new users and/or groups to a license
        - Remove users and/or groups from a license
        - Set reason for a license
        
        """
        return cls.execute_soa_method(
            method_name='setLicenseDetails',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'licenseInfo': licenseInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteLicense(cls, licenseIds: List[str]) -> ServiceData:
        """
        This operation deletes all ADA_License business objects specified in 'licenseIds' parameter. Users performing
        this operation will need privilege specified in ADA_license_administration_privilege site preference to delete
        the licenses. If the user does not have necessary privilege to delete the licenses, or if any license is
        attached to workspace objects, or, if there is any other error while deleting the licenses, the errors are
        returned as partial errors in 'ServiceData'.
        
        Use cases:
        You can delete ADA_License business objects of type ITAR/IP/Exclude by providing license IDs for the licenses.
        """
        return cls.execute_soa_method(
            method_name='deleteLicense',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'licenseIds': licenseIds},
            response_cls=ServiceData,
        )

    @classmethod
    def attachLicenses(cls, attachLicense: List[LicenseInput]) -> ServiceData:
        """
        This operation attaches ADA Licenses to WorkspaceObject business objects such as Item, ItemRevision, Dataset,
        etc. as specified in each 'LicenseInput'. 'LicenseInput' provides details on the licenses to be attached, and
        the WorkspaceObject business objects to attach the licenses to. Users performing this operation will need
        IP_ADMIN privilege to both the workspace objects and the licenses being attached, if the licenses are of type
        IP or Exclude, while ITAR_ADMIN privilege is needed to both the workspace objects and the licenses being
        attached if the licenses are of ITAR license type. If the user does not have necessary privilege to attach any
        licenses, or if there is any other error while attaching licenses, the errors are returned as partial errors in
        'ServiceData'.
        
        Use cases:
        You can attach ADA_License business objects to classified WorkspaceObject business objects to grant access for
        users and/or groups listed on the licenses.
        """
        return cls.execute_soa_method(
            method_name='attachLicenses',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'attachLicense': attachLicense},
            response_cls=ServiceData,
        )

    @classmethod
    def getLicenseDetails(cls, licenseIds: List[str]) -> GetLicenseDetailsResponse:
        """
        This operation gets the properties for each ADA_License business object specified in 'licenseIds' and returns
        them in 'LicenseDetails' structures as part of 'GetLicenseDetailsResponse'. The 'LicenseDetails' contains
        information for properties such as license type, license ID,  expiry date, reason, and associated users and
        groups, for a given license. If there is no matching license for a given license ID, 'LicenseDetails' structure
        for that license will contain 'Not_found' as the value for license ID, while the rest of the parameters will
        contain NULL values. However, if the user does not have READ privilege to any license or if there is any
        unexpected error while getting property information, the errors are returned in the 'ServiceData' of
        'GetLicenseDetailsResponse'.
        
        Use cases:
        
        Use Case 1: Get properties of an ADA License
        You can get properties of an ADA_License business object of type ITAR/IP/Exclude using 'getLicenseDetails'
        operation by providing license ID for the license.
        
        Use Case 2: Check the existence of an ADA License
        You can check if an ADA_License businesses object with given license ID exists using 'getLicenseDetails'
        operation.
        """
        return cls.execute_soa_method(
            method_name='getLicenseDetails',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'licenseIds': licenseIds},
            response_cls=GetLicenseDetailsResponse,
        )

    @classmethod
    def getLicenseIdsAndTypes(cls, licenseFilterInput: List[LicenseTypeAndStatusFilter]) -> LicenseIdsAndTypesResponse:
        """
        This operation gets all the ADA_License business objects based on license type and license status specified in
        'licenseFilterInput' parameter. Licenses of a specific type can be queried for by specifying the license type
        as 'ITAR_License',' IP_License' or 'Exclude_License'. A value of  'ALL' for the license type returns all types
        of ADA licenses. If the license status specified is 'ALL', all ADA licenses are returned, else only unlocked
        and unexpired licenses are returned. For the ADA_License business objects found, details like license IDs and
        license types are returned in 'LicenseIdAndType' structures as part of 'LicenseIdsAndTypesResponse'. If there
        is any unexpected error while getting licenses, the errors are returned in the 'serviceData' of
        'LicenseIdsAndTypesResponse'.
        
        Use cases:
        Use Case 1: Get ADA Licenses based on type and status
        You can get ADA_License business objects using 'getLicenseIdsAndTypes' operation based on specified license
        type and license status.
        """
        return cls.execute_soa_method(
            method_name='getLicenseIdsAndTypes',
            library='AuthorizedDataAccess',
            service_date='2007_06',
            service_name='LicenseManagement',
            params={'licenseFilterInput': licenseFilterInput},
            response_cls=LicenseIdsAndTypesResponse,
        )
