from __future__ import annotations

from tcsoa.gen.DocumentManagement._2007_01.DocumentTemplate import GetTemplateInput, GetTemplatesResponse
from tcsoa.base import TcService


class DocumentTemplateService(TcService):

    @classmethod
    def getTemplates(cls, input: GetTemplateInput) -> GetTemplatesResponse:
        """
        This operation is intended to support applications with a Microsoft Office style template system, where the
        user chooses to create a new document, and the application presents the user with a selection of different
        templates to use to create the document. The calling application inputs its search criteria, and getTemplates
        returns the list of DMTemplate objects that match the criteria. The DMTemplate is a business object that is
        used to control the template files provided during Create.
        
        The search criteria are:
        - The name of the calling application. DMTemplate objects are application specific.
        - The version number of the calling application. Optional.
        - The desired measurement type; e.g. inches or metric. Used for CAD applications.
        - The type of Item that will be created using the DMTemplate file.
        - An application defined type value.
        
        
        
        The operation returns a list of DMTemplate names and thumbnail images that can be used by the application to
        present a choice to the user. Once the user selects a DMTemplate to use in the creation of the new object, the
        application can get the files for the selected DMTemplate using the expandPrimaryObjects operation.
        
        Use cases:
        Get a list of templates for creating a new object.
        
        The user decides to create a new ItemRevision in a CAD application. The application calls this operation and
        receives a list of template names and thumbnails to display to the user. The user selects a template and the
        application retrieves the template files using the expandPrimaryObjects operation. The application then creates
        the new ItemRevision and attaches copies of the template files.
        """
        return cls.execute_soa_method(
            method_name='getTemplates',
            library='DocumentManagement',
            service_date='2007_01',
            service_name='DocumentTemplate',
            params={'input': input},
            response_cls=GetTemplatesResponse,
        )
