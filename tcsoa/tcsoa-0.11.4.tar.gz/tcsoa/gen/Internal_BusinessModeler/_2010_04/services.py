from __future__ import annotations

from tcsoa.gen.Internal.BusinessModeler._2010_04.DataModelManagement import DataModelDeploymentInput, TemplateFilesResponse, TemplateFileInput, ChangedTemplateFileInput
from tcsoa.gen.Internal.BusinessModeler._2007_01.DataModelManagement import ImportDataModelResponse
from typing import List
from tcsoa.base import TcService


class DataModelManagementService(TcService):

    @classmethod
    def getTemplateFiles(cls, inputs: List[TemplateFileInput]) -> TemplateFilesResponse:
        """
        Template files store Teamcenter data model definition information. This operation gets the specified template
        ('inputs') related files from the respective server directories.  In a Teamcenter installed environment, all
        template files are located at '$(TC_DATA)\model' directory. This is an unpublished operation.
        
        Use cases:
        A user can get all templates that a custom template is dependent on from the server $(TC_DATA)\model directory
        using this operation
        """
        return cls.execute_soa_method(
            method_name='getTemplateFiles',
            library='Internal-BusinessModeler',
            service_date='2010_04',
            service_name='DataModelManagement',
            params={'inputs': inputs},
            response_cls=TemplateFilesResponse,
        )

    @classmethod
    def deployDataModel(cls, inputs: List[DataModelDeploymentInput], deployOption: str, updaterUpdateOption: str, updaterModeOption: str) -> ImportDataModelResponse:
        """
        This operation deploys the data model into the database using an XML file based on the input deploy and updater
        options.  Business model updater is used to update the database. Localization (language) files are also
        maintained through this operation.  This operation is deprecated. Please use 'deployDataModel2' Operation.
        """
        return cls.execute_soa_method(
            method_name='deployDataModel',
            library='Internal-BusinessModeler',
            service_date='2010_04',
            service_name='DataModelManagement',
            params={'inputs': inputs, 'deployOption': deployOption, 'updaterUpdateOption': updaterUpdateOption, 'updaterModeOption': updaterModeOption},
            response_cls=ImportDataModelResponse,
        )

    @classmethod
    def getChangedTemplateFiles(cls, inputs: List[ChangedTemplateFileInput], retrieveFiles: bool) -> TemplateFilesResponse:
        """
        Detects if any of the given template related files ('inputs') have changed. Gets the changes template files if
        the 'retriveFiles' option set to 'true'.
        """
        return cls.execute_soa_method(
            method_name='getChangedTemplateFiles',
            library='Internal-BusinessModeler',
            service_date='2010_04',
            service_name='DataModelManagement',
            params={'inputs': inputs, 'retrieveFiles': retrieveFiles},
            response_cls=TemplateFilesResponse,
        )
