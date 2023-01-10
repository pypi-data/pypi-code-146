from __future__ import annotations

from tcsoa.gen.ImportExport._2011_06.FileImportExport import GetExportTemplateResponse1, MarkupReqResponse, MarkupReqUpdateInput, MarkupReqInput, GetTemplateInput, ImportFromApplicationInputData2, ExportToApplicationInputData2, ExportToApplicationResponse1, MarkupReqUpdateResponse, ImportFromApplicationResponse1
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importFromApplication(cls, inputs: List[ImportFromApplicationInputData2]) -> ImportFromApplicationResponse1:
        """
        This operation is used for importing the contents of the given MSWord  document (.docx) to create objects of
        type SpecElement.  Based on the application format, this operation can also be used for importing SpecTemplate,
        ObjectTemplate and ExcelTemplate in database. 
        If the application format is "MSWordXML" then the operation parses the given MS Word document to creates a
        structure of type SpecElement.
         If the application format is "MSWordSpecTemplate" or "MSWordObjTemplate" or "MSExcelTemplate" then the chosen
        template can be imported into Teamcenter. 
        If the application format is "MSWordXMLLive" then a "Live" document can be imported to Teamcenter.  To use this
        application format, a "Live" document should be generated from Teamcenter.
        If the application format is "MSWordSetContent" then it can set the rich text of the SpecElement  by applying
        the templates at the server.
        If the application format is "MSWordXMLExisting" then the given MSWord document is imported to Teamcenter to
        create a Specification within an existing chosen Specification.
        If the application format is "MSWordImportUsingKW" then the given MSWord document is imported to Teamcenter if
        user chooses keywords supplied by user. The keywords are parsed at the server to create the appropriate
        SpecElement type when the keyword is found.
        If the application format is "StructureOnly" then the given MSWord Live document is imported to Teamcenter
        without its  contents.(only object_name property value)
        If the application format is "StructureWithContents" then the given MSWord Live document is imported to
        Teamcenter along with its rich text contents.
        If the application format is "MSWordXWithFulltext" then this operation can be used to create new FullText with
        provided rich text in given MSWord document and this FullText needs to be attached to selected ItemRevision.
        Currently this gets called from Rich client in case of editing rich text for only Systems Engineering revision
        objects,if there is no FullText dataset associated.to selected ItemRevision.
        If the application format is "MSWordXWithFulltext"then this operation can be used to create FullText object
        with input rich text in given document. The created FullText object will be attached to selected object
        revision. Currently this format is called from Rich client in case of editing rich text for only Systems
        Engineering revision objects and if there is no FullText dataset associated.to selected revision.
        When Objects objects of type Requirement/Paragraph are created at the server after importing the document. 
        When this operation is called from Teamcenter rich client, a structure is created and is opened in the
        RequirementsManagement application.  The structure and indentation of the child Requirement is driven by the
        outline levels in the document.  Each Paragraph that is formatted in an outline level style produces a separate
        Requirement. This file may be located in a local file system folder or a network folder.  Import of document to
        Teamcenter supports Word documents in MSOffice Open XML format (.docx format) only. Import of templates to
        Teamcenter supports Word documents in MSOffice Open XML format. (.docx and .docm format)
        
        Supported application formats for this operation
        
        - StructureOnly    This format is used for importing MSWord document to Teamcenter without its  contents.(only
        object_name property value).
        - StructureWithContents This format is used for importing WorkspaceObject to MSWord Live and so that user can
        modify its contents and save them back to Teamcenter.
        - MSWordImportUsingKW    This format is used for importing a MSWord document to Teamcenter using keywords
        supplied by user.
        - MSWordImportExistingUsingKW This format is used for importing a MSWord document to create a Specification in
        Teamcenter into an existing Specification when keywords are supplied by user.
        - MSWordXWithFulltext    This format is used for importing a MSWord document when user wanted to create new
        FullText with provided rich text in given document and this FullText needs to be attached to selected
        ItemRevision. Currently this gets called from Rich client in case of editing rich text for only ItemRevision
        objects, if there is no FullText dataset associated to selected ItemRevision.
        - MSWordXMLPreview This format is used for importing a MSWord document to create a Specification from a
        document previewed by Office client.
        
        
        
        Use cases:
        User can create an MSWord document and import it using this operation to create a structure. Each paragraph in
        Word document represents a Requirement/Paragraph in the structure. User can import templates (SpecTemplate,
        ObjectTemplate and ExcelTemplate) to Teamcenter. User can import a "Live" document generated in Teamcenter and
        set the properties of Workspace objects. User can set the rich text of the SpecElement using the embedded
        MSWord from RAC. User can prevent overwrite of objects which are edited by others.
        """
        return cls.execute_soa_method(
            method_name='importFromApplication',
            library='ImportExport',
            service_date='2011_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse1,
        )

    @classmethod
    def updateReqMarkup(cls, inputs: List[MarkupReqUpdateInput]) -> MarkupReqUpdateResponse:
        """
        This operation creates new markups and updates existing markups in rich text content of SpecElement objects
        that are exported to MSWord using markup option. 
        This operation will take information about markups in the form of mrk file. User needs to have Office Client
        installed to create and update the markups in Word document.
        
        Use cases:
        User can install Office Client and export SpecElement to MSWord using the markup option. Office Client provides
        a mechainsm to create or update markups in a Word document.
        """
        return cls.execute_soa_method(
            method_name='updateReqMarkup',
            library='ImportExport',
            service_date='2011_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=MarkupReqUpdateResponse,
        )

    @classmethod
    def createReqMarkup(cls, inputs: List[MarkupReqInput]) -> MarkupReqResponse:
        """
        This operation will take info for markup datasets to be created for the requirement objects and create a markup
        dataset for each markup data requirement object
        """
        return cls.execute_soa_method(
            method_name='createReqMarkup',
            library='ImportExport',
            service_date='2011_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=MarkupReqResponse,
        )

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData2]) -> ExportToApplicationResponse1:
        """
        This operation is used for exporting Teamcenter objects (WorkspaceObject) to applications like MSWord and
        MSExcel. Teamcenter business objects should already be created so that the objects can be exported to Word and
        Excel using the service operation.
        An MSExcel (.xlsm) or a MSWord (.docx) file or a comma separated file (.csv) file is generated at the server as
        a result of this operation.  The generated file will contain Teamcenter objects and their properties. Depending
        upon the application format that is being passed as input parameter, the generated file can be opened in MSWord
        or MSExcel.  If the application format is "'CSV'" then a comma separated file is generated at the server.  If
        the application format is "'MSWordXML'" then the generated document is a Word document.  It traverses the
        structure for the given SpecElement deep and exports all its children to MSWord document. If the application
        format is "'MSExcel'" then the generated sheet is a static Excel spreadsheet.  If the application format is
        "'MSExcelLive'" then the generated sheet is a Live Excel spreadsheet. "Live" sheet means that modifications can
        be done to the data will reflect to Teamcenter.  If the application format is "'MSWordXMLLive'" then the
        generated document is a Live Word document.  This mode provides the capability of Live editing the SpecElement
        in the word document.  A "Live" Word document means that the any modifications done in the document like
        changing the rich text or editing of properties will be saved to Teamcenter on click of "Save"button in MSWord.
        If the application format is "'MSExcelReimport'" then the generated sheet can be reimported back to Teamcenter.
        If the application format is "'MSExcelLiveBulkMode'" then the sheet is generated in "Bulk Live" mode. This mode
        enables the user to make all the changes to the properties of objectsfrom Excel and then commit the changes to
        Teamcenter on click of "Save to Teamcenter" button in Excel.  If the application format is "'StructureOnly'"
        then the structure can be exported to Word without the contents having only "object_name" property in the
        exported document.  If the application format is "'StructureWithContents'" then the structure is exported to
        MSWord along with the contents (rich text) of each element in the structure.  This mode provides the ability of
        live editing and structure editing of SpecElements in the MSWord document. User can edit the contents or can
        make structural changes to the exported document.  If the application format is "'MSWordXMLLiveMarkupFN'" then
        Markups will be exported to MSWord using FindNo as sorting key.  If the application format is "'MSWordXMLFN'"
        then a static structure can be exported to MSWord using FindNo as sorting key.  If the application format is
        "'MSWordXMLLiveFN'" then a "Live" structure can be exported to MSWord using FindNo as sorting key.  If the
        export Option is "CheckOutObjects" then the objects can be checked out before exporting to MSWord/Excel.
        
        Use cases:
        User can create Teamcenter objects in RAC and then export those objects and their properties to Word or Excel.
        If "Live" option is selected then user can create "Live" documents after export to Word/Excel.  During the
        export to Word/Excel, Teamcenter objects are exported to Word/Excel by applying the appropriate templates. User
        can export Teamcenter objects to Excel which can be imported back to Teamcenter. User can create excel sheet in
        a "Bulk Live" mode so that bulk changes can be committed to Teamcenter.  User can export the objects and
        properties to a comma separated file. User can create SpecTemplate, ObjectTemplate and ExcelTemplate in
        Teamcenter and customize these templates as per User need such as adding more properties or adding formatting
        information to the templates.  User can associate different objectTemplate for every Business object type at
        runtime and specify this configuration when using this operation. User can export a structure to MSWord without
        exporting the rich text of each SpecElement. User can export a structure for "Live" edit and structure edit to
        MSWord.  User can export a static or a "Live" structure along with the Markups. Users can checkout objects
        during Export to MSWord/MSExcel.
        
        Exceptions:
        >Service Exception If there is any error during generating transient file read ticket due to a configuration
        issue at the server, then the operation throws a service exception. Example- If the transient volume directory
        is not configured at the server then the FMS fails to generate a file at the server and subsequent file
        download operation fails. In such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='ImportExport',
            service_date='2011_06',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse1,
        )

    @classmethod
    def getExportTemplates(cls, filter: List[GetTemplateInput]) -> GetExportTemplateResponse1:
        """
        'getExportTemplates' is responsible for getting various export templates from database based on input filter.
        Export templates can be of type SpecTemplate, ObjectTemplate or ExcelTemplate. Depending upon the input filter,
        the templates of type SpecTemplate or ObjectTemplate or ExcelTemplate are retrieved from the database. These
        templates can be used by the application for export purpose.
        
        Use cases:
        User can create Items of type SpecTemplate or ObjectTemplate or ExcelTemplate in Teamcenter and use this
        operation to get the desired template types.
        """
        return cls.execute_soa_method(
            method_name='getExportTemplates',
            library='ImportExport',
            service_date='2011_06',
            service_name='FileImportExport',
            params={'filter': filter},
            response_cls=GetExportTemplateResponse1,
        )
