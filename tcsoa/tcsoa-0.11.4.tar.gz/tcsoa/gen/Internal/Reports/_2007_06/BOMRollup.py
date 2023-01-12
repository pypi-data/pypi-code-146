from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, Folder, Dataset
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetRollupTemplateInput(TcBaseObj):
    """
    The input structure which contains data used to find RollupTemplates.
    
    :var clientId: A unique string used to identify the caller. It is simply returned on success, or used to label any
    errors.
    :var mode: The search mode string:
    "Mode=ALL"
    "Mode=USER_PREFERENCE"
    or
    "Mode=SPECIFIC:name:scope_context"
    """
    clientId: str = ''
    mode: str = ''


@dataclass
class ReviseRollupReportInput(TcBaseObj):
    """
    Input structure which defines data needed to revise rollup report.
    
    :var clientId: A unique string used to identify the caller.
    :var bomline: The root BOM line the report is based on.
    :var dataset: The existing rollup report you want to revise.
    :var rollupTemplate: The RollupTemplate on which to base the revised rollup report.
    """
    clientId: str = ''
    bomline: BOMLine = None
    dataset: Dataset = None
    rollupTemplate: BusinessObject = None


@dataclass
class RollupReportOutput(TcBaseObj):
    """
    A structure used by 'generateRollupReports' to return rollup reports.
    
    :var clientId: A unique string used to identify the caller.
    :var dataset: The generated rollup report Dataset tag.
    """
    clientId: str = ''
    dataset: Dataset = None


@dataclass
class RollupReportResponse(TcBaseObj):
    """
    Response from 'generateRollupReports' and 'reviseRollupReports' operations.
    
    :var output: A list of 'RollupReportOutput', which is a list of rollup report Dataset tags.
    :var serviceData: Status of the operation.
    """
    output: List[RollupReportOutput] = ()
    serviceData: ServiceData = None


@dataclass
class RollupTemplateCalculation(TcBaseObj):
    """
    A structure used by the 'getRollupTemplateCalculations' operation to return rollup calculation templates.
    
    :var type: The rollup calculation template type: 'ROLLUPCalcSum', 'ROLLUPCalcCofm', 'ROLLUPCalcInertia', or
    'ROLLUPCalcRef'.
    :var calcTemplates: A list of rollup calculation templates of type "type".
    """
    type: ROLLUPCalculationType = None
    calcTemplates: List[BusinessObject] = ()


@dataclass
class RollupTemplateCalculationOutput(TcBaseObj):
    """
    A structure used by 'getRollupTemplateCalculations' to return RollupTemplates and their rollup calculation
    templates.
    
    :var rollupTemplate: A RollupTemplate tag.
    :var rollupCalcTemplates: The RollupTemplate's rollup calculation templates.
    """
    rollupTemplate: BusinessObject = None
    rollupCalcTemplates: List[RollupTemplateCalculation] = ()


@dataclass
class RollupTemplateCalculationResponse(TcBaseObj):
    """
    The returned structure from 'getRollupTemplateCalculations'.
    
    :var output: A list of 'RollupTemplateCalculationOutput', which is a list of rollup calculation template tags.
    :var serviceData: Status of the operation.
    """
    output: List[RollupTemplateCalculationOutput] = ()
    serviceData: ServiceData = None


@dataclass
class RollupTemplateInput(TcBaseObj):
    """
    - Input structure which contains data needed to get calculation templates from RollupTemplates.
    - Input structure used to clone RollupTemplates.
    
    
    
    :var clientId: A unique string which identifies the caller. It is simply returned on success, or used to label any
    errors.
    :var rollupTemplate: The tag of a RollupTemplate.
    """
    clientId: str = ''
    rollupTemplate: BusinessObject = None


@dataclass
class RollupTemplateOutput(TcBaseObj):
    """
    Structure used by 'createRollupTemplates' to return created RollupTemplates.
    
    :var clientId: A unique string used to identify the caller. It is simply returned on success, or attached to any
    errors.
    :var rollupTemplates: A list of RollupTemplate tags.
    """
    clientId: str = ''
    rollupTemplates: List[BusinessObject] = ()


@dataclass
class RollupTemplateResponse(TcBaseObj):
    """
    The structure returned from 'createRollupTemplates' and 'getRollupTemplates'.
    
    :var output: A list of RollupTemplate tags.
    :var serviceData: Status of the operation.
    """
    output: List[RollupTemplateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateRollupCalculationInputArgument(TcBaseObj):
    """
    Input structure used by 'createRollupCalculationTemplates'.
    
    :var name: "Value" or "Asserted" depending on whether you are setting the property to use for the calculation or
    the property to use for asserted (use the value calculated by your CAD tool).
    :var input: The name of the property you want to use for the calculation.
    :var output: The label you want to use for the column in the rollup report. (Does not apply to Asserted, so use "".)
    """
    name: str = ''
    input: str = ''
    output: str = ''


@dataclass
class CreateRollupCalculationTemplateInput(TcBaseObj):
    """
    The input structure which defines data needed to create rollup calculation templates.
    
    :var clientId: A unique string used to identify the caller. It is simply returned on success, or used to ID any
    errors.
    :var type: An enumeration specifying the type of rollup calculation template to create: 'ROLLUPCalcSum',
    'ROLLUPCalcCofm', 'ROLLUPCalcInertia', or 'ROLLUPCalcRef'.
    :var parent: The tag of the RollupTemplate to attach the new rollup calculation template to.
    :var arguments: A vector of structures consisting of three strings - name, input, output.
    - Name is "Value" or "Asserted" depending on whether you are setting the property to use for the calculation or the
    property to use for asserted (use the value calculated by NX).
    - Input is the name of the property you want to use for the calculation.
    - Output is the label you want to use for the column in the rollup report. (Does not apply to Asserted, so use "".)
    
    """
    clientId: str = ''
    type: ROLLUPCalculationType = None
    parent: BusinessObject = None
    arguments: List[CreateRollupCalculationInputArgument] = ()


@dataclass
class CreateRollupCalculationTemplateOutput(TcBaseObj):
    """
    Output structure used by 'createRollupCalculationTemplates' to return created rollup calculation templates.
    
    :var clientId: A unique string used to identify the caller.
    :var type: The type of rollup calculation templates.
    :var calcTemplate: The created rollup calculation template.
    """
    clientId: str = ''
    type: ROLLUPCalculationType = None
    calcTemplate: BusinessObject = None


@dataclass
class CreateRollupCalculationTemplateResponse(TcBaseObj):
    """
    The returned structure from 'createRollupCalculationTemplates'.
    
    :var output: A list of 'CreateRollupCalculationTemplateOutput', which constists of:
    - The client ID string that was passed in.
    - The rollup calculation template type that was passed in.
    - The tag of the created rollup calculation template.
    
    
    :var serviceData: Status of the operation.
    """
    output: List[CreateRollupCalculationTemplateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateRollupReportInput(TcBaseObj):
    """
    Input structure which defines data needed to create a rollup report.
    
    :var clientId: A string which identifies the caller. Can be any unique string since it is simply returned on
    success.
    :var name: A string used to name the rollup report Dataset. If null, the ItemRevision name will be used.
    :var description: An optional string to describe the rollup report.
    :var bomline: The tag of the root BOM line on which to generate the rollup report.
    :var folder: Optional Teamcenter folder in which to put the rollup report. If null, the report will be attached to
    the ItemRevision corresponding to the specified root BOM line, otherwise on error it will be placed in the Newstuff
    folder.
    :var rollupTemplate: The RollupTemplate you want to use to generate the rollup report.
    """
    clientId: str = ''
    name: str = ''
    description: str = ''
    bomline: BOMLine = None
    folder: Folder = None
    rollupTemplate: BusinessObject = None


@dataclass
class CreateRollupTemplateInput(TcBaseObj):
    """
    Input structure which defines data needed to create RollupTemplates.
    
    :var clientId: A string which identifies the caller. The string can be anything since it is simply returned in
    'RollupTemplateOutput'.
    :var name: A string which will be used to name the RollupTemplate.
    :var desc: A description for the RollupTemplate.
    :var delimiter: The delimiter which will be used to separate columns in the rollup reports generated using this
    template.
    :var scopeContext: A string which gives context to the scope. For site scope - the site ID, for group scope - the
    group name, for user scope - the user name.
    :var scope: One of the following: 'ROLLUPScopeSite', 'ROLLUPScopeUser', 'ROLLUPScopeGroup'
    """
    clientId: str = ''
    name: str = ''
    desc: str = ''
    delimiter: str = ''
    scopeContext: str = ''
    scope: ROLLUPScopeType = None


class ROLLUPCalculationType(Enum):
    """
    Enumerator used to distinguish between different rollup calculation template types.
    """
    ROLLUPCalcInvalid = 'ROLLUPCalcInvalid'
    ROLLUPCalcSum = 'ROLLUPCalcSum'
    ROLLUPCalcCofm = 'ROLLUPCalcCofm'
    ROLLUPCalcInertia = 'ROLLUPCalcInertia'
    ROLLUPCalcRef = 'ROLLUPCalcRef'


class ROLLUPScopeType(Enum):
    """
    Enumerator used to distinguish between different rollup template scopes.
    """
    ROLLUPScopeInvalid = 'ROLLUPScopeInvalid'
    ROLLUPScopeSite = 'ROLLUPScopeSite'
    ROLLUPScopeUser = 'ROLLUPScopeUser'
    ROLLUPScopeGroup = 'ROLLUPScopeGroup'
