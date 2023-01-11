from __future__ import annotations

from tcsoa.gen.Internal.BusinessModeler._2007_01.DataModelManagement import ExportDataModelResponse, ImportDataModelResponse
from tcsoa.base import TcService


class DataModelManagementService(TcService):

    @classmethod
    def importDataModel(cls, custTemplateFileTicket: str, custDependencyFileTicket: str, updateOption: str, runMode: str) -> ImportDataModelResponse:
        """
        Imports data model to database from xml file. This operation is replaced by 'deployDataModel2'.
        """
        return cls.execute_soa_method(
            method_name='importDataModel',
            library='Internal-BusinessModeler',
            service_date='2007_01',
            service_name='DataModelManagement',
            params={'custTemplateFileTicket': custTemplateFileTicket, 'custDependencyFileTicket': custDependencyFileTicket, 'updateOption': updateOption, 'runMode': runMode},
            response_cls=ImportDataModelResponse,
        )

    @classmethod
    def exportDataModel(cls, mode: str) -> ExportDataModelResponse:
        """
        Exports data model to an xml file.
        
        Use cases:
        Teamcenter data model definitions are externally managed in XML format, and are often refered to as Business
        Modeler IDE template definitions. With this operation, the user can export the data model definitions from the
        Teamcenter database to an XML file. This is equivalent to running the business modeler extractor utility. There
        are two different modes ('schema' and 'all') that  export a different amount of information. The 'schema' mode
        will extract the application, classes, and attribute information, whereas 'all' will extract the entire data
        model information including the schema.
        """
        return cls.execute_soa_method(
            method_name='exportDataModel',
            library='Internal-BusinessModeler',
            service_date='2007_01',
            service_name='DataModelManagement',
            params={'mode': mode},
            response_cls=ExportDataModelResponse,
        )
