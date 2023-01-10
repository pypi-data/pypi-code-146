from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportTemplateInput(TcBaseObj):
    """
    The ExportTemplateInput structure contains the flags that are required to filter the different type of export
    templates such as SpecTemplate, ObjectTemplate and ExcelTemplate from the database.
    
    :var getSpecTemplates: If set to true then it will query for SpecTemplates in database.
    :var getObjectTemplates: If set to true then it will query for ObjectTemplates in database.
    :var getExcelTemplates: If set to true then it will query for ExcelTemplates in database.
    :var getConfiguredSpecTemplate: This element is not used.
    :var getConfiguredObjectTemplate: This element is not used.
    """
    getSpecTemplates: bool = False
    getObjectTemplates: bool = False
    getExcelTemplates: bool = False
    getConfiguredSpecTemplate: bool = False
    getConfiguredObjectTemplate: bool = False


@dataclass
class ExportToApplicationInputData1(TcBaseObj):
    """
    The ExportToApplicationInputData1 structure represents all of the data necessary to export selected Teamcenter
    objects to MSWord/Excel.
    
    :var objectsToExport: The list of Teamcenter business objects to export.
    :var attributesToExport: The list of attributes to export.
    :var applicationFormat: The application format such as "'MSWordXML'", "'MSExcel'", "'MSExcelLive'",
    "'MSExcelReimport'", "'MSWordXMLLive'", "'MSExcelLiveBulkMode'".
    
    Supported application format for this operation
    
    - MSWordXML     This format is used for exporting Workspace objects to static MSWord application.
    - MSExcel    This format is used for exporting Teamcenter objects to static MSExcel  application.
    - MSExcelLive    This format is used for exporting Teamcenter objects to Live MSExcel  application.
    - MSExcelReimport    This format is used for exporting Teamcenter objects to MSExcel 
    
    
    application for reimport purpose.
    - MSExcelLiveBulkMode    This format is used for exporting Teamcenter objects to MSExcel  application for Bulk Live
    mode so that user can make all the property changes and save all the changes to Teamcenter on click of "Save to
    Teamcenter"button.
    - MSWordXMLLive    This format is used for exporting Workspace objects to Live MSWord application.
    
    
    :var templateId: The name of the Word/Excel template
    :var templateType: The type of the export template.
    :var objectTemplateOverride: The runtime object template override which is association of objectTemplate for a
    Business object type for a  chosen SpecTemplate.
    """
    objectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateId: str = ''
    templateType: str = ''
    objectTemplateOverride: List[TemplateOverride] = ()


@dataclass
class GetExportTemplateResponse(TcBaseObj):
    """
    The GetExportTemplateResponse Return represents the output of getExportTemplates operation which contains the
    information about the objects of type SpecTemplate, ObjectTemplate and ExcelTemplate that are queried from the
    database. Example- If the input filter flag (getSpecTemplates) is set to true in ExportTemplateInput structure,
    then the GetExportTemplateResponse structure will contain the all the objects of type SpecTemplate
    
    :var specTemplates: The list of objects of type SpecTemplate
    :var objectTemplats: The list of objects of type ObjectTemplate
    :var excelTemplates: The list of objects of type ExcelTemplate
    :var configuredSpecTemplates: This is not used
    :var configuredObjectTemplates: This is not used
    :var serviceData: The Service Data
    """
    specTemplates: List[str] = ()
    objectTemplats: List[str] = ()
    excelTemplates: List[str] = ()
    configuredSpecTemplates: List[ConfiguredTemplate] = ()
    configuredObjectTemplates: List[ConfiguredTemplate] = ()
    serviceData: ServiceData = None


@dataclass
class ImportFromApplicationInputData1(TcBaseObj):
    """
    The ImportFromApplicationInputData1 structure represents all of the data necessary to import a specification into
    Teamcenter or import templates to Teamcenter.
    
    :var transientFileWriteTicket: The file ticket of the. docx file to be imported into Teamcenter.
    :var applicationFormat: The application format suchas "'MSWordXML'", "'MSWordXMLLive'",
    "'MSWordXMLOverWriteCheck'", "'MSWordSpecTemplate'","'MSWordObjTemplate'","'MSExcelTemplate'" and
    "'MSWordSetContent'"
    
    Supported application formats for this operation
    
    - MSWordXML     This format is used for importing a MSWord document to Teamcenter.
    - MSWordXMLLive    This format is used for importing a Live MSWord document to Teamcenter.
    - MSWordXMLOverwriteCheck    This format is used for importing a  Live MSWord document to Teamcenter and check for
    overwrite condition on the object during setting of properties in database.
    - MSWordSetContent    This format is used for importing a  Live MSWord document to 
    
    
    Teamcenter. This format is used by the embedded viewer to set the rich text of SpecElement and to set the
    properties on the SpecElement.
    - MSWordSpecTemplate    This format is used for importing a SpecificationTemplate to 
    
    
    Teamcenter.
    - MSWordObjectTemplate    This format is used for importing a ObjectTemplate to Teamcenter.
    - MSWordExcelTemplate    This format is used for importing a ExcelTemplate to Teamcenter.
    
    
    :var createSpecElementType: The subtype of SpecElement to be created.
    :var specificationType: The subtype of Specification to be created.
    :var isLive: If the flag is set to true then it indicates "live" option.
    If the flag is set to false then it indicates "static" option.
    """
    transientFileWriteTicket: str = ''
    applicationFormat: str = ''
    createSpecElementType: str = ''
    specificationType: str = ''
    isLive: bool = False


@dataclass
class TemplateOverride(TcBaseObj):
    """
    The structure represents all of the data necessary to override object templates.
    
    :var businessObjectType: The type of business object.
    :var templateId: The name of object template.
    :var templateType: The type of object template.
    """
    businessObjectType: str = ''
    templateId: str = ''
    templateType: str = ''


@dataclass
class ConfiguredTemplate(TcBaseObj):
    """
    The 'ConfiguredTemplate' structure contains the information required to get IRDC configured export templates. BMIDE
    enables the user to configure templates based on the object type using the IRDC configuration.
    
    :var businessObjectType: Type name of business object.
    :var templateName: The name of the configured template on business object type.
    :var templateType: The type name of configured template.
    """
    businessObjectType: str = ''
    templateName: str = ''
    templateType: str = ''
