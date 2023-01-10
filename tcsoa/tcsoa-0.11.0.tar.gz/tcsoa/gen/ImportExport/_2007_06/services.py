from __future__ import annotations

from tcsoa.gen.ImportExport._2007_06.FileImportExport import ImportFromApplicationResponse, ImportFromApplicationInputData, ExportToApplicationInputData, ExportToApplicationResponse
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importFromApplication(cls, inputs: List[ImportFromApplicationInputData]) -> ImportFromApplicationResponse:
        """
        This operation imports the contents of the given MSWord document to create objects of type SpecElement.  The
        MSWord document to be imported to Teamcenter should have .docx file format. If the application format is
        MSWordXML then the operation parses the given MSWord document to creates a structure of chosen subtype of
        SpecElement.  The parsing of dcoument involves parsing of individual paragraphs in the document. Each paragraph
        in the document with a Heading becomes a SpecElement. After the BOM structure is created at the server, a
        BOMWIndow is constructed at the server and returned returned to the caller. Objects of type
        Requirement/Paragraph are created at the server after importing the document.  This operation supports Word
        documents in MSOffice Open XML format (.docx format) only. If the application format is not set then the
        operation does not do anything.
        
        Use cases:
        User can create an MSWord document and import it using this operation to create a structure. Each paragraph in
        MSWord document represents a Requirement/Paragraph in the structure. When this operation is called from
        Teamcenter rich client, a structure is created and is opened in the Requirements Management application.  The
        structure and indentation of the child Requirements is driven by the MSWord outline level in the document. 
        Each Paragraph that is formatted in an outline level style produces a separate Requirement. This file may be
        located in a local file system folder or a network folder.
        
        Exceptions:
        >Service Exception    This occurs due to an error during generating transient file ticket due to a
        configuration issue at the server. For example, if the transient volume directory is not configured at the
        server then the FMS fails to import the document and subsequent file upload operation fails. In such situation
        a 'ServiceException' is thrown.
        """
        return cls.execute_soa_method(
            method_name='importFromApplication',
            library='ImportExport',
            service_date='2007_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse,
        )

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData]) -> ExportToApplicationResponse:
        """
        This operation is used for exporting Teamcenter objects (WorkspaceObject) to applications like MSWord and
        MSExcel. Teamcenter business objects should already be created so that the objects can be exported to Word and
        Excel using the service operation.
        An MSExcel (.mhtml) or a MSWord (.docx) file is generated at the server as a result of this operation.  The
        generated file will contain Teamcenter objects and their properties. Depending upon the application format that
        is being passed as input parameter, the generated file can be opened in Word or Excel.  If the application
        format is "'MSWordXML'" then the generated document is a Word document.  If the application format is
        "'MSExcel'" then the generated sheet is a static Excel spreadsheet.  If the application format is
        "'MSExcelLive'" then the generated sheet is a Live Excel spreadsheet. "Live" sheet means that modifications can
        be done to the data in Excel which will reflect to Teamcenter.
        
        
        
        Use cases:
        User can create Teamcenter objects in RAC and then export those objects and their properties to Word or Excel.
        If "Live" option is selected then User can create "Live" spreadsheet after export to Excel.
        
        Following usecases are supported in this operation
        
        - Export of Workspace objects to MSWord (static)
        - Export of Teamcenter objects to MSExcel(static)
        - Export of Teamcenter objects to MSExcel(Live) and edit the properties from Excel Live sheet.
        
        
        
        Exceptions:
        >Service Exception If there is any error during generating transient file read ticket due to a configuration
        issue at the server, then the operation throws a service exception. Example- If the transient volume directory
        is not configured at the server then the FMS fails to generate a file at the server and subsequent file
        download operation fails. In such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='ImportExport',
            service_date='2007_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse,
        )
