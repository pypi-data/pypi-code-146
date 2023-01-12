from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DerivativeRuleResponse(TcBaseObj):
    """
    DerivativeRuleResponse represents the output of the published execute Derive CAE Structure operation.
    
    The root of the output structure is returned as a part of created object in the Service Data. A log is also
    returned with the results of the derivative rule applied to the input structure and the output item created. Any
    failures in creation of the output item or relationships are also returned as a part of the activity log.
    
    The following partial errors may be returned:
    
    - 206845 - Error occurred during Derive operation.
    - 206845 - Derive  Engine unable to load/read/parse XMLRendering.
    - 206643 - CAE_dataMapping_file preference not defined.
    - 206647 - Item creation failed, operation aborted.
    - 206648 - Occurrence creation failed, operation aborted.
    - 206649 - Unknown attribute found.
    - 206650 - Object not modifiable, set attribute operation failed.
    - 206651 - Form creation failed.
    - 206652 - BOMView creation failed.
    - 206653 - Unable to save the Item in the Newstuff folder.
    - 206664 - Error in relationship creation.
    - 206665 - Item node line definition missing in Data Map.
    
    
    
    :var serviceData: The root of the output structure is returned as a part of Created Object in the Service Data.
    :var activityLog: The text of activityLog contains the Item ID and revision of the root of created output structure
    . In case of failure of derive operation, the text will report failure. This text is used for intermediate
    reporting when executeDeriveCAEStructure is called in a loop for multiple structure creation from rich client. User
    is  informed of the status of ongoing operation by displaying this text in a string viewer. If failure is reported,
    user can choose to terminate the entire operation from rich client. The details of failure can be then retrieved
    from ServiceData.
    """
    serviceData: ServiceData = None
    activityLog: str = ''
