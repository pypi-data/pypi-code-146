from __future__ import annotations

from tcsoa.gen.Requirementsmanagement._2007_01.RequirementsManagement import CreateOrUpdateResponse, ImportFromApplicationInputData, ExportToApplicationInputData, ExportToApplicationResponse, PartInfo, GetContentInput, SetContentInput, ImportFromApplicationResponse, SetRichContentResponse, GetRichContentResponse
from typing import List
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def getRichContent(cls, inputs: List[GetContentInput]) -> GetRichContentResponse:
        """
        getRichContent operation is used to retrieve rich text contents of SpecElement type of objects which is a
        subclass of WorkspaceObject.  A .docm file is generated as a result of getRichContent operation which can be
        opened in MSWord.
        
        Use cases:
        User can open content (body text) in word for view and edit purpose.
        
        Exceptions:
        >If there is any error during generating transient file read ticket due to a configuration issue at the server,
        then the operation throws a service exception. Example- If the transient volume directory is not configured at
        the server then the FMS fails to generate a file at the server and subsequent file download operation fails. In
        such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='getRichContent',
            library='Requirementsmanagement',
            service_date='2007_01',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=GetRichContentResponse,
        )

    @classmethod
    def importFromApplication(cls, inputs: List[ImportFromApplicationInputData]) -> ImportFromApplicationResponse:
        """
        This operation is used for importing the contents of the given MSWord document  to create objects of type
        SpecElement.  The MSWord document to be imported to Teamcenter should have .docx file format. If the
        application format is MSWordXML then the operation parses the given MSWord document to creates a structure of
        chosen subtype of SpecElement.
        
        Objects of type Requirement/Paragraph are created at the server after importing the document.  When this
        operation is called from Teamcenter rich client, a structure is created and is opened in the
        'RequirementsManagement' application.  The structure and indentation of the child Requirement is driven by the
        MSWord outline level in the document.  Each Paragraph that is formatted in an outline level style produces a
        separate Requirement. This file may be located in a local file system folder or a network folder.  This
        operation supports MSWord documents in MS Office Open XML format (.docx format) only.
        
        Use cases:
        User can create an MSWord document and import it using this operation to create a structure. Each Paragraph in
        MSWord document represents a Requirement/Paragraph in the structure.
        
        Exceptions:
        >If there is any error during generating transient file ticket due to a configuration issue at the server, then
        the operation throws a service exception. For example If the transient volume directory is not configured at
        the server then the FMS fails to import the document and subsequent file upload operation fails. In such
        situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='importFromApplication',
            library='Requirementsmanagement',
            service_date='2007_01',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse,
        )

    @classmethod
    def setRichContent(cls, inputs: List[SetContentInput]) -> SetRichContentResponse:
        """
        The SOA operation is responsible for setting rich text contents from Word document to a Fulltext object of
        requirement. This SOA operation will be called when; User modified rich content of requirements through word
        document. This operation will basically accept Fulltext object to process in "objectToProcess" variable. Along
        with Fulltext object, this operation will accept transient file tickets for MSWord Document which is modified
        by user. All exceptions are added to service data, if occurred.
        
        Use cases:
        User can set rich text contents of SpecElement object by using setRichContent SOA.
        
        Exceptions:
        >If there is any error while downloading file then the operation throws a service exception. Example- The
        transient volume directory is not configured at the server then the FMS fails to generate a file at the server
        and subsequent file download operation fails. In such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='setRichContent',
            library='Requirementsmanagement',
            service_date='2007_01',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=SetRichContentResponse,
        )

    @classmethod
    def createOrUpdate(cls, info: List[PartInfo]) -> CreateOrUpdateResponse:
        """
        This operation creates objects of type Item .  The related objects such as ItemRevision, Dataset and Forms are
        also created during this operation.  This operation checks for the existence of the Item, ItemRevision, and
        Dataset.  If the Item and ItemRevision already exists, but the Dataset does not exist, then the Dataset is
        created.  If the Dataset exists, a new version will be added to the existing version.  If any of the objects
        exists, but the input attribute values that differ from those already set, attempts are made to update the
        values. There is no attempt to query and update an existing object without a reference to that object. This
        operation has the additional behavior to create and update the Dataset along with the creation of Item.
        
        Use cases:
        User can create objects of type Item using this operation.
        User can create or update objects of type Dataset using this operation.
        
        Exceptions:
        >None.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdate',
            library='Requirementsmanagement',
            service_date='2007_01',
            service_name='RequirementsManagement',
            params={'info': info},
            response_cls=CreateOrUpdateResponse,
        )

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData]) -> ExportToApplicationResponse:
        """
        This operation is used for exporting Teamcenter objects (WorkspaceObject) to applications like MSWord and
        MSExcel.  Teamcenter business objects should already be created so that the objects can be exported to MSWord
        and MSExcel using the service operation.
        
        An Excel (.mhtml) or a Word (.docx) file is generated at the server as a result of this operation.  The
        generated file will contain Teamcenter objects and their properties. Depending upon the application format that
        is being passed as input parameter, the generated file can be opened in MSWord or MSExcel.  If the application
        format is MSWordXML then the generated document is a Word document.  If the application format is MSExcel then
        the generated sheet is a static Excel spreadsheet.  If the application format is MSExcelLive then the generated
        sheet is a Live Excel spreadsheet. "Live" sheet means that modifications can be done to the data in MSExcel
        which will reflect to Teamcenter. 
        
        
        Use cases:
        User can create Teamcenter objects in RAC and then export those objects and their properties to MSWord or
        MSExcel. If "Live" option is selected then User can create "Live" spreadsheet after export to MSExcel.
        
        Following usecases are supported in this operation
        
        - Export of Workspace objects to MSWord (static)
        - Export of Teamcenter objects to MSExcel(static)
        - Export of Teamcenter objects to MSExcel(Live) and edit the properties from Excel Live sheet.
        
        
        
        Exceptions:
        >If there is any error during generating transient file read ticket due to a configuration issue at the server,
        then the operation throws a service exception. Example- If the transient volume directory is not configured at
        the server then the FMS fails to generate a file at the server and subsequent file download operation fails. In
        such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='Requirementsmanagement',
            service_date='2007_01',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse,
        )
