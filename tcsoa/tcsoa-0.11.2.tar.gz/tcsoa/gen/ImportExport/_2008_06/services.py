from __future__ import annotations

from tcsoa.gen.ImportExport._2008_06.FileImportExport import ImportFromApplicationInputData1, ExportTemplateInput, GetExportTemplateResponse, ExportToApplicationInputData1
from tcsoa.gen.ImportExport._2007_06.FileImportExport import ImportFromApplicationResponse, ExportToApplicationResponse
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importFromApplication(cls, inputs: List[ImportFromApplicationInputData1]) -> ImportFromApplicationResponse:
        """
        This operation is used for importing the contents of the given MSWord document (.docx) to create objects of
        type SpecElement.  Based on the application format, this operation can also be used to import objects of type
        SpecTemplate,ObjectTemplate and ExcelTemplate in database. If the application format is "'MSWordXML'"then the
        operation parses the given MS Word document to creates a structure of type SpecElement.  If the application
        format is "'MSWordSpecTemplate'" or "'MSWordObjTemplate'"or "'MSExcelTemplate'" then the chosen template can be
        imported into Teamcenter.  If the application format is "'MSWordXMLLive'" then a "Live" document can be
        imported to Teamcenter.  To use this application format, a "Live" document should be generated from Teamcenter.
        If the application format is "'MSWordSetContent'" then it can set the rich text of the SpecElement  and the
        properties on the SpecElement by using the SpecficationTemplate and ObjectTemplate at the server. If the
        application format is "'MSWordXMLOverWriteCheck'" then the Teamcenter objects will be checked for overwrite
        condition at the server.
        The objects of type Requirement/Paragraph are created at the server after import of the document.  If this
        operation is called from Teamcenter rich client, a structure is created and is opened in the
        RequirementsManagement application.  The structure and indentation of the child Requirement is driven by the
        outline levels in the document.  Each Paragraph that is formatted in an outline level style produces a separate
        Requirement. This file may be located in a local file system folder or a network folder.  Import of document to
        Teamcenter supports Word documents in MS Office Open XML format (.docx format) only. Import of templates to
        Teamcenter supports MSWord documents in MS Office Open XML format. (.docx and .docm format)
        
        Use cases:
        User can create an MSWord document and import it using this operation to create a structure. Each paragraph in
        MSWord document represents a Requirement/Paragraph in the structure. User can import templates (SpecTemplate,
        ObjectTemplate and ExcelTemplate) to Teamcenter. User can import a "Live" document generated in Teamcenter and
        set the properties of Workspace objects. User can set the rich text of the SpecElement using the embedded Word
        from RAC. User can prevent overwrite of objects which are edited by others.
        
        Exceptions:
        >Service Exception If there is any error during generating transient file ticket due to a configuration issue
        at the server, then the operation throws a service exception. Example - If there is any exception due FMS not
        configured then the file upload to server will fail and a service exception will occur.
        """
        return cls.execute_soa_method(
            method_name='importFromApplication',
            library='ImportExport',
            service_date='2008_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse,
        )

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData1]) -> ExportToApplicationResponse:
        """
        This operation is used for exporting Teamcenter objects (WorkspaceObject) to applications like MSWord and
        MSExcel. Teamcenter business objects should already be created so that the objects can be exported to MSWord
        and MSExcel using the service operation.
        An Excel (.mhtml) or a Word (.docx) file or a comma separated file (.csv) file is generated at the server as a
        result of this operation.  The generated file will contain Teamcenter objects and their properties. Depending
        upon the application format that is being passed as input parameter, the generated file can be opened in MSWord
        or MXExcel.  If the application format is "MSWordXML" then the generated document is a Word document.  It
        traverses the structure for the given SpecElement deep and exports all its children to MSWord document. If the
        application format is "MSExcel" then the generated sheet is a static Excel spreadsheet.  If the application
        format is "MSExcelLive" then the generated sheet is a Live Excel spreadsheet. "Live" sheet means that
        modifications can be done to the data will reflect to Teamcenter.  If the application format is "MSWordXMLLive"
        then the generated document is a Live Word document.  A "Live" Word diocument means that the any modifications
        done in the document like changing the rich text or editing of properties will be saved to Teamcenter on click
        of "Save" button in MSWord. If the application format is "MSExcelReimport" then the generated sheet can be
        reimported back to Teamcenter. If the application format is "MSExcelLiveBulkMode"then the sheet is generated in
        "Bulk Live" mode. This mode enables the user to make all the changes to the properties of objectsfrom Excel and
        then commit the changes to Teamcenter on click of "Save to Teamcenter" button in Excel.
        
        
        Use cases:
        User can create Teamcenter objects in RAC and then export those objects and their properties to Word or Excel.
        If "Live" option is selected then User can create "Live" documents after export to Word/Excel.  During the
        export to Word/Excel, Teamcenter objects are exported to Word/Excel by applying the appropriate templates. User
        can export Teamcenter objects to Excel which can be imported back to Teamcenter. User can create excel sheet in
        a "Bulk Live" mode so that bulk changes can be committed to Teamcenter.  User can export the objects and
        properties to a comma separated file. User can create SpecTemplate, ObjectTemplate and ExcelTemplate in
        Teamcenter and customize these templates as per User need such as adding more properties or adding formatting
        information to the templates.  User can associate different objectTemplate for every Business object type at
        runtime and specify this configuration when using this operation.
        
        Exceptions:
        >Service Exception  If there is any error during generating transient file read ticket due to a configuration
        issue at the server, then the operation throws a service exception. Example-  If the transient volume directory
        is not configured at the server then the FMS fails to generate a file at the server and subsequent file
        download operation fails. In such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='ImportExport',
            service_date='2008_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse,
        )

    @classmethod
    def getExportTemplates(cls, filter: ExportTemplateInput) -> GetExportTemplateResponse:
        """
        This operation is used for retrieving all the MSWord and MSExcel templates from database. An input filter can
        be applied to get the desired template type from database. All the Word and Excel templates are of 'Item' type.
        Depending on the input filter, the Item of type SpecTemplate or ObjectTemplate or ExcelTemplate are retrieved
        from the database. These templates are used by the application for export purpose. If the chosen filter is of
        type SpecTemplate or ObjectTemplate then the document to be imported is in .docx or .docm file format.  If the
        chosen filter is of type ExcelTemplate then the spreadsheet to be imported is in .xlsx or .xlsm file format.
        
        Use cases:
        User can import MSWord and MSExcel templates to Teamcenter and use these templates for export purpose. During
        this operation, items of type SpecTemplate or ObjectTemplate or ExcelTemplate is created after the import
        operation in Teamcenter.
        """
        return cls.execute_soa_method(
            method_name='getExportTemplates',
            library='ImportExport',
            service_date='2008_06',
            service_name='FileImportExport',
            params={'filter': filter},
            response_cls=GetExportTemplateResponse,
        )
