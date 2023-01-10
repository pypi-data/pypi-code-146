from __future__ import annotations

from tcsoa.gen.Internal.BusinessModeler._2010_04.DataModelManagement import DataModelDeploymentInput
from tcsoa.gen.Internal.BusinessModeler._2010_09.DataModelManagement import SiteTemplateDeployInfoResponse, DeployDataModelResponse
from typing import List
from tcsoa.base import TcService


class DataModelManagementService(TcService):

    @classmethod
    def getSiteTemplateDeployInfo(cls, templateNames: List[str]) -> SiteTemplateDeployInfoResponse:
        """
        This operation gets the site information from the current database for the requested list of templates
        ('templateNames').
        
        Exceptions:
        >ServiceException    If the template is not present in the current database (216016).
        """
        return cls.execute_soa_method(
            method_name='getSiteTemplateDeployInfo',
            library='Internal-BusinessModeler',
            service_date='2010_09',
            service_name='DataModelManagement',
            params={'templateNames': templateNames},
            response_cls=SiteTemplateDeployInfoResponse,
        )

    @classmethod
    def deployDataModel2(cls, deployOption: str, updaterUpdateOption: str, updaterModeOption: str, inputs: List[DataModelDeploymentInput]) -> DeployDataModelResponse:
        """
        The user invoking this service should have the system administrative privileges. This operation updates the
        database with the data model changes available in the template project referred in the 'inputs' argument. Based
        on the 'deployOtion' argument value the template will be live deployed or updated. The service acquires a
        database lock before updating the data model so there should not be any active lock before running this service.
        
        Validations done before updating the data model
        - Validate if database is free of any lock.
        - Validate the privileges of the user invoking the service.
        - If preference 'BMIDE_ALLOW_FULL_DEPLOY_FROM_CLIENT' is set to 'FALSE' or 'BMIDE_ALLOW_OPS_DEPLOY' is set to
        'FALSE' in the server then live deploy or live update is restricted.
        - The template that needs to be updated or deployed should have all its dependencies deployed.
        - If the template is being live updated then elements present in the delta should be enabled for the live
        update operation.
        - The element present in the delta files is eligible for live deploy if not then proper error message is
        returned.
        
        """
        return cls.execute_soa_method(
            method_name='deployDataModel2',
            library='Internal-BusinessModeler',
            service_date='2010_09',
            service_name='DataModelManagement',
            params={'deployOption': deployOption, 'updaterUpdateOption': updaterUpdateOption, 'updaterModeOption': updaterModeOption, 'inputs': inputs},
            response_cls=DeployDataModelResponse,
        )
