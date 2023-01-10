from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExecuteRuleResponse(TcBaseObj):
    """
    ExecuteRuleResponse represents the outputs of the internal execute StructureMap and execute Data Map operations.
    
    :var serviceData: If the root of the output structure has a BOMView Revision, PSBOMViewRevision of the root of the
    output structure is returned as a part of Created Object in the Service Data, else the ItemRevision of the root is
    returned as a part of the Created Object in the Service Data.
    :var activityLog: A log containing the results of the Data Map and StructureMap rules applied to the input
    structure and the output items created. The details include what Data Map and StructureMap rules were applied, type
    of the output item created, the Item ID of the output item, the relationships created between the input and the
    output ItemRevision. Any failures in creation of the output item or relationships are also returned as a part of
    the activity log.
    
    Following are some possible errors returned in ServiceData:
    - 206622 Structure Engine unable to load/read/parse Data Map.
    - 206642 XML Libraries for StructureMap Engine not available.
    - 206643 CAE_dataMapping_file preference not defined.
    - 206647 Item creation failed, operation aborted.
    - 206648 Occurrence creation failed, operation aborted.
    - 206649 Unknown attribute found.
    - 206650 Object not modifiable, set attribute operation failed.
    - 206651 Form creation failed.
    - 206652 BOMView creation failed.
    - 206653 Unable to save the Item in the Newstuff folder.
    - 206658 Existing Relationship found, relationship not being created.
    - 206662 Error encountered in Variant Condition creation.
    - 206664 Error in relationship creation.
    - 206665 Item node line definition missing in Data Map.
    - 206666 StructureMap domain not found for StructureMapRevision.
    - 206672 Rules with different domains found in the same StructureMap/Data Map.
    - 206673 Rules with no domain defined found in StructureMap/Data Map.
    - 206677 Multiple variant clauses found in the variant condition. Variant Condition creation failed.
    - 206678 Invalid or missing variant clause expression. Variant Condition creation failed.
    - 206679 Mapped BOMView Type does not exist, creating default view type.
    
    """
    serviceData: ServiceData = None
    activityLog: str = ''
