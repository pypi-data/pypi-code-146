from __future__ import annotations

from tcsoa.gen.BusinessObjects import ChangeItemRevision, WorkspaceObject, ImanRelation
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateChangeLineageInputData(TcBaseObj):
    """
    Input data for creation of lineage.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var solutionItems: List of WorkspaceObject which are referred as Solution Items for the ChangeNoticeRevision. All
    the solution items must belong to same ChangeNoticeRevision.
    :var impactedItems: List of WorkspaceObject which are referred as Impacted Items for the ChangeNoticeRevision. All
    the impacted items must belong to same ChangeNoticeRevision.
    """
    clientId: str = ''
    solutionItems: List[WorkspaceObject] = ()
    impactedItems: List[WorkspaceObject] = ()


@dataclass
class CreateChangeLineageOutput(TcBaseObj):
    """
    Change Lineage output.
    
    :var clientId: The unmodified value from the CreateChangeLineageInputData.clientId. This can be used by the caller
    to identify this data structure with the source input data.
    :var relations: A list of created relations.
    """
    clientId: str = ''
    relations: List[ImanRelation] = ()


@dataclass
class CreateChangeLineageResponse(TcBaseObj):
    """
    Change Lineage creation response.
    
    :var serviceData: Service data.
    :var output: Change Lineage output.
    """
    serviceData: ServiceData = None
    output: List[CreateChangeLineageOutput] = ()


@dataclass
class DeleteChangeLineageInputData(TcBaseObj):
    """
    DeleteChangeLineageInputData structure contains clientId to uniquely identify the input, an object reference that
    can be used to point to the ChangeNoticeRevision and list to hold any number of business objects for which change
    lineage has to be deleted.
    
    :var clientId: Input string to uniquely identify the input.
    :var changeNoticeRev: The ChangeNoticeRevision associated with the lineage to be deleted.
    :var objects: A list of objects for which the related lineage will be deleted.
    """
    clientId: str = ''
    changeNoticeRev: ChangeItemRevision = None
    objects: List[WorkspaceObject] = ()
