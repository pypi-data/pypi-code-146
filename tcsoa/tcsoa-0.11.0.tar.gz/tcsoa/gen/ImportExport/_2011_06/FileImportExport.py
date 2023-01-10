from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanRelation, WorkspaceObject, Dataset
from tcsoa.gen.ImportExport._2008_06.FileImportExport import TemplateOverride, ConfiguredTemplate
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportToApplicationInputData2(TcBaseObj):
    """
    The ExportToApplicationInputData2 structure represents all of the data necessary to export selected objects to
    specific application like MSWord and MSExcel.
    
    :var objectsToExport: lThe list of Teamcenter business objects to export.
    :var attributesToExport: The list of attributes to export.
    :var applicationFormat: The application format such as "'MSWordXML'", "'MSWordXMLLive'","'MSExcel'" and
    "'MSExcelLive'","'MSExcelReimport'","'StructureOnly'","'StructureWithContents'","'MSWordXMLLiveMarkupFN'",
    "'MSWordXMLFN'","'MSWordXMLLiveFN'"
    
    Supported application format for this operation
    
    - MSWordXML     This format is used for exporting Workspace objects to static MSWord application.
    - MSExcel    This format is used for exporting Teamcenter objects to static MSExcel  application.
    - CSV    This format is used for exporting Teamcenter objects in a comma separated file format used for audit
    purpose.
    - MSExcelLive    This format is used for exporting Teamcenter objects to Live MSExcel  application.
    - MSExcelReimport    This format is used for exporting Teamcenter objects to MSExcel  application for reimport
    purpose.
    - MSExcelLiveBulkMode    This format is used for exporting Teamcenter objects to MSExcel  application for Bulk Live
    mode so that user can make all the property changes and save all the changes to Teamcenter on click of "Save to
    Teamcenter" button.
    - MSWordXMLLive    This format is used for exporting objects of type WorkspaceObject to Live  MSWord application.
    - StructureOnly    This format is used for exporting Workspace objects to MSWord without its  contents.(only
    object_name property value exported to MSWord)
    - StructureWithContents    This format is used for exporting WorkspaceObject to MSWord Live and so that user can
    modify its contents and save them back to Teamcenter.
    - MSWordXMLLiveMarkupFN    This format is used for exporting Markups to MSWord Live using FindNo as sorting key.
    - MSWordXMLLiveMarkup    This format is used for exporting Markups to MSWord Live.
    - MSWordXMLFN    This format is used for exporting WorkspaceObject to static MSWord using FindNo as sorting key.
    - MSWordXMLLiveFN    This format is used for exporting WorkspaceObject to Live MSWord application using FindNo as
    sorting key.
    
    
    :var templateId: The name of the MSWord/MSExcel template
    :var templateType: Type of export template.
    :var objectTemplateOverride: The runtime object template override which is association of objectTemplate for a
    Business object type for a chosen SpecTemplate.
    :var exportOptions: The options to be considered during the export process like "CheckOutObjects"
    """
    objectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateId: str = ''
    templateType: str = ''
    objectTemplateOverride: List[TemplateOverride] = ()
    exportOptions: List[ImportExportOptions] = ()


@dataclass
class ExportToApplicationResponse1(TcBaseObj):
    """
    ExportToApplicationResponse structure represents the output of export to application operation.  It has information
    about file ticket for the exported file generated at the server and the single markup file sent to the client.
    
    :var transientFileReadTickets: The transient file read tickets for the exported file.
    :var markupXMLReadTickets: The transient file read tickets for the generated markup file during Export to Word and
    when the application format is "MSWordXMLLiveMarkup" or "MSWordXMLLiveMarkupFN"
    
    :var serviceData: The Service Data
    """
    transientFileReadTickets: List[str] = ()
    markupXMLReadTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class FileMetaData(TcBaseObj):
    """
    This structure contains the information about file path, The key will contain "FilePath" and data will contain the
    physical file path of the file to be used for the purpose of import/export.
    
    
    :var key: Placeholder for a string called "FilePath".
    :var data: Physical file path of the file for import/export to Teamcenter.
    """
    key: str = ''
    data: str = ''


@dataclass
class GetExportTemplateResponse1(TcBaseObj):
    """
    This structure contains the information about the export templates that are queried from database. If there is any
    error during the querying of export templates from the database or if there is any error during the operation, then
    it is added as part of ServiceData.
    
    :var serviceData: The Service Data
    :var outputTmplNames: The object type of template as key and a vector of template names as the value.
    
    :var configuredSpecTemplates: This parameter is not being used.
    :var configuredObjectTemplates: This parameter is not being used.
    """
    serviceData: ServiceData = None
    outputTmplNames: TemplateTypeVsTemplates = None
    configuredSpecTemplates: List[ConfiguredTemplate] = ()
    configuredObjectTemplates: List[ConfiguredTemplate] = ()


@dataclass
class GetTemplateInput(TcBaseObj):
    """
    This structure contains information about the templates to be queried from Teamcenter database. It will contain
    additional information in the form of name-value pair to store the information about the application domain.
    
    :var templateType: The type of template like "SpecTemplate", "ObjectTemplate" and "ExcelTemplate"
    
    :var nameValueMap: The name value pair to store information about the application domain.
    """
    templateType: str = ''
    nameValueMap: NameValueMap = None


@dataclass
class ImportExportOptions(TcBaseObj):
    """
    This structure contains additional options required to pass during the Import\Export operations. importOptions:
    This structure is used for providing the import or export options depending on the mode of operation. This is
    key/value pair.  
    Following are the available options used during importing data to Teamcenter
    - UnCheckOutObjects - Performs uncheckout operation
    - SyncTeamcenter - Synchronize Teamcenter data with document
    - FeedbackRequired - Runs SOA in "feedback" mode, so check conflicting objects
    - SyncDocument - Synchronize document with Teamcenter
    - ReviseAllObjects - Revise option (not used)
    - ReviseOverwriteObjects - Revise option for "modified" objects after export
    - IgnoreCheckoutObjects - Ignore checked out objects and save remaining objects.
    - CheckInObjects - Check in objects
    - UnCheckOutObjects - UnCheckout objects
    
    
    Following are the available options used during exporting data to Teamcenter
    - ShowTransferModeWarning - to show warning if secondary objects are exported to Word Live with structure editing.
    - CheckOutObjects - Checkout objects.
    
    
    
    :var option: The option name can be as below
    - UnCheckOutObjects
    - SyncTeamcenter
    - FeedbackRequired
    - SyncDocument
    - ReviseAllObjects
    - ReviseOverwriteObjects
    - IgnoreCheckoutObjects
    - CheckInObjects
    
    
    :var value: The option's value can be as below
    - UnCheckOutObjects
    - SyncTeamcenter
    - FeedbackRequired
    - SyncDocument
    - ReviseAllObjects
    - ReviseOverwriteObjects
    - IgnoreCheckoutObjects
    - CheckInObjects
    
    """
    option: str = ''
    value: str = ''


@dataclass
class ImportFromApplicationInputData2(TcBaseObj):
    """
    The ImportFromApplicationInputData2 structure represents all of the data necessary to import a specification into
    Teamcenter or import templates to Teamcenter.
    
    :var transientFileWriteTicket: The file ticket of the. docx file to be imported into Teamcenter.
    :var applicationFormat: The application format such as "'MSWordXML'","MSWordXMLLive", "MSWordXMLOverWriteCheck",
    "MSWordSpecTemplate", "MSWordObjTemplate", "MSExcelTemplate" and "MSWordSetContent"
    
    Supported application formats for this operation
    
    - MSWordXML     This format is used for importing a MSWord document to Teamcenter.
    - MSWordXMLLive    This format is used for importing a Live MSWord document to 
    
    
                                        Teamcenter.
    - MSWordXMLExisting    This format is used for importing a  MSWord document and 
    
    
                                                create a Specification within an existing chosen Specification.
    - MSWordSetContent    This format is used for importing a  Live MSWord document to  
    
    
                                            Teamcenter. This format is used by the embedded viewer to  
                                            set the rich text of SpecElement and to set the properties on the  
                                            SpecElement.
    - MSWordSpecTemplate    This format is used for importing a Specification template to  
    
    
                                                Teamcenter.
    - MSWordObjectTemplate    This format is used for importing a ObjectTemplate to 
    
    
                                                    Teamcenter.
    - MSWordExcelTemplate    This format is used for importing a ExcelTemplate to 
    
    
                                                    Teamcenter.
    :var createSpecElementType: The subtype of SpecElement to be created.
    :var specificationType: The subtype of Specification to be created.
    :var isLive: Flag to determine static or live option. Default value is non live.
    :var selectedBomLine: The top BOMLine under which new structure gets imported.
    :var fileMetaDatalist: The list of structures that contains information about the physical file path of the file.
    :var importOptions: The additional options that user can pass for import purpose.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with the input structure.
    """
    transientFileWriteTicket: str = ''
    applicationFormat: str = ''
    createSpecElementType: str = ''
    specificationType: str = ''
    isLive: bool = False
    selectedBomLine: BusinessObject = None
    fileMetaDatalist: List[FileMetaData] = ()
    importOptions: List[ImportExportOptions] = ()
    clientId: str = ''


@dataclass
class ImportFromApplicationOutputData(TcBaseObj):
    """
    The structure contains the information about the data that is passed back to the client after the result of
    importFromApplication SOA operation. It contains the UID of the BOMWindow after the document is imported to
    Teamcenter.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var transientFileTickets: The file ticket of the transient file to be imported.
    :var resultObjects: The objects like the BOMWindow tag if the import is successful.
    """
    clientId: str = ''
    transientFileTickets: List[str] = ()
    resultObjects: List[BusinessObject] = ()


@dataclass
class ImportFromApplicationResponse1(TcBaseObj):
    """
    ImportFromApplicationResponse1 structure represents the output of import from application operation. It contains
    UID of the BOMWindow created after the document is imported.  In case of import of templates, it contains the
    business object of the tenplate after the import operation.
    
    :var serviceData: The Service Data. It holds the error stack which contains information about any errors that are
    generated during importFromApplication operation.
    
    :var output: The list of structure containing the resultant objects which contains the UID of the BOMWindow created
    after the document is imported.  In case of importing templates, it contains the business object of the template.
    It also contains the file ticket of the xml file containing the details about the generated errors at the server
    during importFromApplication operation.
    """
    serviceData: ServiceData = None
    output: List[ImportFromApplicationOutputData] = ()


@dataclass
class MarkupReqInput(TcBaseObj):
    """
    Input structure containing the Single Markup XML info and Markup dataset info to be created
    
    :var clientId: This is not used.
    :var markupDataset: This is not used.
    :var reqObj: This is not used.
    :var isLiveMarkup: This should be always false as we do not support markup in live mode.
    
    :var transientFileWriteTickets: FMS ticket of "mrk" file.
    """
    clientId: str = ''
    markupDataset: DatasetInfo = None
    reqObj: WorkspaceObject = None
    isLiveMarkup: bool = False
    transientFileWriteTickets: List[str] = ()


@dataclass
class MarkupReqOutput(TcBaseObj):
    """
    This structure containing the information about the created markup Dataset and the GRM relation on the created
    markup Dataset to the FullText.
    
    :var markupDatset: The created markup Dataset.
    :var relation: The GRM relation on the created Dataset to the FullText.
    """
    markupDatset: Dataset = None
    relation: ImanRelation = None


@dataclass
class MarkupReqResponse(TcBaseObj):
    """
    Structure containing markup output with created markup Dataset information and ServiceData.
    
    :var markupInfo: This is not used.
    :var serviceData: Updated markup Dataset are added to updated object list of ServiceData.
    """
    markupInfo: MarkupReqOutputMap = None
    serviceData: ServiceData = None


@dataclass
class MarkupReqUpdateInput(TcBaseObj):
    """
    Markup dataset sent by the client that needs to be updated
    
    :var markupDataset: Markup dataset sent by the client that needs to be updated
    :var reqObj: Requirement object ID which has the markups that need an update
    :var isLiveMarkup: Flag indicating whether markup is on live or non live document
    :var transientFileWriteTickets: Contains an FMS ticket of the single XML file uploaded
    """
    markupDataset: Dataset = None
    reqObj: WorkspaceObject = None
    isLiveMarkup: bool = False
    transientFileWriteTickets: List[str] = ()


@dataclass
class MarkupReqUpdateResponse(TcBaseObj):
    """
    Structure containing markup dataset update response
    
    :var serviceData: Updated markup dataset will be returned in the ServiceData. Any failure will be returned with
    error message in the ServiceData list of partial errors.
    """
    serviceData: ServiceData = None


@dataclass
class DatasetInfo(TcBaseObj):
    """
    This structure contains the markup dataset information like name, type, tool information specified by client.
    
    :var tool: The tool used to open the created Dataset.
    :var datasetType: The type of the Dataset to be created.
    :var datasetName: The name of the markup Dataset to be created.
    :var datasetDesc: The description of the markup Dataset to be created.
    """
    tool: str = ''
    datasetType: str = ''
    datasetName: str = ''
    datasetDesc: str = ''


"""
This map contains the key as clientId to the 'MarkupReqOutput' structure. The 'MarkupReqOutput' structure contains the created Markup Datatset and the GRM relation on the created markup Dataset and the FullText.
"""
MarkupReqOutputMap = Dict[str, MarkupReqOutput]


"""
This map will hold the name value pair of input. The map stores the "ApplicationDomain" as key and value of the key specific to the domain.
"""
NameValueMap = Dict[str, str]


"""
This map contains information about the template type and the name of the templates. Template type can be SpecTemplate and ObjectTemplate. For each template type the name of the templates in the database is queried and returned to the user.
"""
TemplateTypeVsTemplates = Dict[str, List[str]]
