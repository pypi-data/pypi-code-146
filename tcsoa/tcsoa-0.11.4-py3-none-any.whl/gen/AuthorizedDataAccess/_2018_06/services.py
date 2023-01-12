from __future__ import annotations

from tcsoa.gen.AuthorizedDataAccess._2018_06.LicenseManagement import LicenseDetails
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LicenseManagementService(TcService):

    @classmethod
    def createOrUpdateLicense(cls, licenseInfo: List[LicenseDetails]) -> ServiceData:
        """
        This operation creates or modifies an ADA_License business object for each LicenseDetails supplied. The
        LicenseDetails contains information for properties such as license type, license ID, category, citizenship,
        expiry date, lock date, reason, in accordance with, and associated users and groups, for a given license. If a
        specified license ID already exists, the rest of the property values are updated on that license. However, if
        the license ID does not exist, then a new license of the specified type and ID will be created, and the rest of
        the properties are set on the created license. The user performing the operation will need the privilege
        specified in the ADA_license_administration_privilege site preference to create or modify an ADA License. If a
        user does not have the necessary privilege or if there is a validation error, the operation would fail and the
        error is returned in the ServiceData.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateLicense',
            library='AuthorizedDataAccess',
            service_date='2018_06',
            service_name='LicenseManagement',
            params={'licenseInfo': licenseInfo},
            response_cls=ServiceData,
        )
