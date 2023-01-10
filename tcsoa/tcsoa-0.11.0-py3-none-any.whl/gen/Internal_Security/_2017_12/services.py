from __future__ import annotations

from tcsoa.gen.Internal.Security._2017_12.AwLicensing import LicenseInput, LicensesWithTypesResponse
from tcsoa.base import TcService


class AwLicensingService(TcService):

    @classmethod
    def getLicensesWithTypes(cls, licenseInputs: LicenseInput) -> LicensesWithTypesResponse:
        """
        This operation retrieves the Licenses attached to the given workspace objects . In case of multiple objects,
        only the licenses that are attached to all of the objects will be returned . It also retrieves level or
        structure information in case of ActiveWorkspace Content context. In ActiveWorkspace Content context, if the
        selected object do not have additional child objects then level or structure information are not be returned.
        """
        return cls.execute_soa_method(
            method_name='getLicensesWithTypes',
            library='Internal-Security',
            service_date='2017_12',
            service_name='AwLicensing',
            params={'licenseInputs': licenseInputs},
            response_cls=LicensesWithTypesResponse,
        )
