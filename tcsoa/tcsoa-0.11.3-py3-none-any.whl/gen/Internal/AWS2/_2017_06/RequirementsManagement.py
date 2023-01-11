from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_12.RequirementsManagement import ImportExportOptions
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BaselineInputData(TcBaseObj):
    """
    The structure BaselineInputData represents the input data required to baseline selected object.
    
    :var objectToBaseline: A business object (ItemRevision or Awb0Element) to be baselined.
    :var baselineRevisionId: The required revision ID of new Baseline Revision which would be created after baseline
    completes. This is an optional parameter and can be empty.
    :var baselineDescription: Description for the new Baseline Revision to be created. This is an optional parameter
    and can be empty.
    :var baselineReleaseProcedureName: Name of the Release Procedure through which the Baseline Revision should
    undergo. The possible release procedure name is governed by preference Baseline_release_procedures.
    :var baselineJobName: Name of the Job for new Baseline Revision to be created. This is an optional parameter and
    can be empty.
    :var baselineLabelName:   Name of the Snapshot folder . Snapshot folder name  is required for imprecise
    baselining.This field is optional and can be blank.
    :var baselineJobDescription: Description of the Job. This is an optional parameter and can be empty.
    :var isDryRun: This option indicates whether dry run creation is to be performed. This is an  optional parameter
    and can be empty. The current value is defaulted to false. This parameter is for future use.
    :var isPreciseBaseline: This option indicates whether the created structure would be a precise or imprecise.  Value
    true denotes precise structure and false denotes imprecise structure. The default value is true.
    """
    objectToBaseline: BusinessObject = None
    baselineRevisionId: str = ''
    baselineDescription: str = ''
    baselineReleaseProcedureName: str = ''
    baselineJobName: str = ''
    baselineLabelName: str = ''
    baselineJobDescription: str = ''
    isDryRun: bool = False
    isPreciseBaseline: bool = False


@dataclass
class BaselineInputDataAsync(TcBaseObj):
    """
    This is required as an input for operation createBaselineAsync
    
    :var baselineInputDataSync: Sync Baseline Input Data.
    :var recipeObject: The recipe of selected BOMLine object which contains information to reconstruct it back and
    create baseline.
    """
    baselineInputDataSync: BaselineInputData = None
    recipeObject: str = ''


@dataclass
class ObjectTemplateInputs(TcBaseObj):
    """
    This structure contains additional options required to be passed when object template is applied during export.
    
    :var boType: Type of object. The supported types are ItemRevision and its sub-types.
    :var objectTemplateName: Name of the object template to be applied during export.
    """
    boType: str = ''
    objectTemplateName: str = ''


@dataclass
class ExportToApplicationInputData4(TcBaseObj):
    """
    The ExportToApplicationInput4 represents the data required to export selected objects to MSWord or MSExcel.
    
    :var objectsToExport: A list of Teamcenter business objects to be exported.
    :var targetObjectsToExport: The list of Teamcenter business objects to be exported which acts as target objects
    used for comparing the contents. An optional parameter and can be empty.
    :var recipeSourceObjects: The recipe of selected BOMLine objects which contains information to reconstruct them
    back and export. This is an optional parameter and can be empty.
    :var recipeTargetObjects: The recipe of target BOMLine objects which contains information to reconstruct them back
    and export. This is an optional parameter used for compare scenarios and can be empty.
    :var attributesToExport: A list of attributes that are visible in Active Workspace for export. An optional
    parameter which can be empty. (For future use.)
    :var applicationFormat: The application formats supported are:  "MSExcel", "MSWordXMLLive", "MExcelLive",
    "MSExcelReimport", "MSWordCompare", "HTML".
    :var templateName: The name of the MSWord or MSExcel template.
    :var exportOptions: List of options for export. Supported options are: 
    "CheckOutObjects" - the selected object and its hierarchy is checked out during export.
    "RunInbackground" - the export operation will be executed in background and a notification is sent when export is
    completed.
    :var objectTemplateInputs: Inputs for applying object template during export.
    :var includeAttachments: If true, the attachments are to be included while exporting.
    """
    objectsToExport: List[BusinessObject] = ()
    targetObjectsToExport: List[BusinessObject] = ()
    recipeSourceObjects: List[str] = ()
    recipeTargetObjects: List[str] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateName: str = ''
    exportOptions: List[ImportExportOptions] = ()
    objectTemplateInputs: List[ObjectTemplateInputs] = ()
    includeAttachments: bool = False
