from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from tcsoa.gen.Manufacturing._2012_02.DataManagement import GeneralInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetConnectorResponse(TcBaseObj):
    """
    Response for getConnectorInfo operation.
    
    :var connectorInfo: List of structures containing connector information for given ItemRevision objects.
    :var serviceData: Partial errors as part of the serviceData.
    """
    connectorInfo: List[ConnectorTableInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetPhysicalAttachmentsInput(TcBaseObj):
    """
    Input structure containing context and scope information for which the attachments need to be retrieved.
    
    :var context: A root Mfg0BvrWorkarea object in Bill of Equipment structure. The operation processes scope within
    context.
    :var scope: A Mfg0BvrWorkarea object under context for which attachment need to be queried
    """
    context: BOMLine = None
    scope: BOMLine = None


@dataclass
class GetPhysicalAttachmentsResponse(TcBaseObj):
    """
    Response for getPhysicalAttachmentsInScope operation.
    
    :var attachmentsInfo: List of structures containing information about the physical attachment relation
    Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot between AbsOccurrence of BOMLine objects under the given scope
    Mfg0BvrWorkarea.
    :var serviceData: Partial errors as part of the serviceData.
    """
    attachmentsInfo: List[PhysicalAttachmentInfo] = ()
    serviceData: ServiceData = None


@dataclass
class PhysicalAttachmentInfo(TcBaseObj):
    """
    The structure containing source and target BOMLine and the Mfg0MEPhysicalAttachment relation information.
    
    :var context: A root Mfg0BvrWorkarea object in Bill of Equipment structure.
    :var scope: A Mfg0BvrWorkarea object under context
    :var source: A BOMLine node of the AbsOccurrence represeting primary  in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    :var target: A BOMLine node of the AbsOccurrence represeting secondary  in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    :var relationName: Name of relation by which  AbsOccurence of source BOMLine and target BOMLine are related.
    Possible values are Mfg0MEPhysicalAttachment or its subtype Mfg0MEMountToolToRobot.
    :var relationInfo: Structure containing Mfg0MEPhysicalAttachment or its subtype Mfg0MEMountToolToRobot relation
    properties.
    Teamcenter::Soa::Manufacturing::_2012_02::GeneralInfo is an existing Data Structure that holds map for different
    properties. 
    The relationInfo contains information about following
    - String type relation properties of Mfg0MEPhysicalAttachment. stringProps element holds these proerties as key.
    Below is the list of String type relation properties of Mfg0MEPhysicalAttachment
    - mfg0SourceID as key. Value can be  "Connect Point1".
    - mfg0SourceIDFormatType as key. Possible values are Kinematics (KIN), Connector Table (CTB), PRT, JT.
    - mfg0TargetID as key. Value can be "Mount Point1".
    - mfg0TargetIDFormatType as key. Possible values are Kinematics (KIN), Connector Table (CTB), PRT, JT.
    - Boolean type mfg0BiDirectional relation property of Mfg0MEPhysicalAttachment. boolProps element of GeneralInfo
    contains mfg0BiDirectional as key and value is true or false.
    - Double type mfg0RelTransform relation property of Mfg0MEPhysicalAttachment. doubleProps element of GeneralInfo
    contains mfg0RelTransform as key and value is double e.g. 100.00.
    - Double type mfg0TCPFPosition relation property of Mfg0MEMountToolToRobot. doubleProps element of GeneralInfo
    contains mfg0TCPFPosition as key and value is double e.g. 100.00. This is specified only if the relation type is
    Mfg0MEMountToolToRobot.
    
    """
    context: BOMLine = None
    scope: BOMLine = None
    source: BOMLine = None
    target: BOMLine = None
    relationName: str = ''
    relationInfo: GeneralInfo = None


@dataclass
class RemovePhysicalAttachmentRelInput(TcBaseObj):
    """
    Input structure containing context, scope, source, and target information.
    
    :var context: A root Mfg0BvrWorkarea object in Bill of Equipement structure. The operation deletes relations of
    type Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot created in this context.
    :var scope: A Mfg0BvrWorkarea object under context.  The operation travereses the scope, finds the source and
    target BOMLine,gets  AbsOccurrence for source and target BOMLine and collects Mfg0MEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation to be deleted.
    :var source: A BOMLine node of the AbsOccurrence represeting primary  in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    :var target: A BOMLine node of the AbsOccurrence represeting secondary in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    """
    context: BOMLine = None
    scope: BOMLine = None
    source: BOMLine = None
    target: BOMLine = None


@dataclass
class SetConnectorInput(TcBaseObj):
    """
    Input structure containing ItemRevision and connectorInformation
    
    :var itemRev: ItemRevision for which connector details are to be updated.
    :var connectorInformation: List of structures containing properties of connectors to be added or updated in
    Mfg0MEConnectorTableRow on Mfg0MEConnectorTable. 
    Teamcenter::Soa::Manufacturing::_2012_02::GeneralInfo is an existing Data Structure that holds map for different
    properties. 
    The connectorsInfo contains information about following
    - String type relation properties of Mfg0MEConnectorTableRow. stringProps element holds these proerties as key.
    Below is the list of String type relation properties of Mfg0MEConnectorTableRow
    - mfg0ConnectorType as key. Value can be  Tool Frame Connector, Base frame connector, Riser frame connector.
    - mfg0ConnectorID as key. Value can be "Mount Point1". 
    - mfg0ConnectorName as key. Value can be "Base Frame".
    - Double type mfg0RelToOrigin property of Mfg0MEConnectorTableRow. doubleProps element of GeneralInfo contains
    mfg0RelToOrigin as key and value is double e.g. 100.00.
    
    """
    itemRev: BusinessObject = None
    connectorInformation: List[GeneralInfo] = ()


@dataclass
class SetPhysicalAttachmentsInput(TcBaseObj):
    """
    Input structure containing context, scope, source, target, relation name, and relation properties information.
    
    :var context: A root Mfg0BvrWorkarea object in Bill of Equipment structure. In context of this root, AbsOccurrence
    is created for source BOMLine and target BOMLine.
    :var scope: A Mfg0BvrWorkarea object under context.
    :var source: A BOMLine node of the AbsOccurrence representing primary  in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    :var target: A BOMLine node of the AbsOccurrence representing secondary in MfgMEPhysicalAttachment or
    Mfg0MEMountToolToRobot relation.
    :var relationName: Name of relation by which AbsOccurence of source BOMLine and target BOMLine are related.
    Possible values are  Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot.
    :var relationInfo: Structure containing Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot relation properties.
    Teamcenter::Soa::Manufacturing::_2012_02::GeneralInfo is an existing Data Structure that holds map for different
    properties.
    The relationInfo contains information about following
    - String type relation properties of Mfg0MEPhysicalAttachment. stringProps element holds these proerties as key.
    Below is the list of String type relation properties of Mfg0MEPhysicalAttachment
    - mfg0SourceID as key. Value can be  "Connect Point1"
    - mfg0SourceIDFormatType as key. Possible values are Kinematics (KIN), Connector Table (CTB), PRT, JT
    - mfg0TargetID as key. Value can be "Mount Point1"
    - mfg0TargetIDFormatType as key. Possible values are Kinematics (KIN), Connector Table (CTB), PRT, JT
    - Boolean type mfg0BiDirectional relation property of Mfg0MEPhysicalAttachment. boolProps element of GeneralInfo
    contains mfg0BiDirectional as key and value is true or false.
    - Double type mfg0RelTransform relation property of Mfg0MEPhysicalAttachment. doubleProps element of GeneralInfo
    contains mfg0RelTransform as key and value is double e.g. 100.00.
    - Double type mfg0TCPFPosition relation property of Mfg0MEMountToolToRobot. doubleProps element of GeneralInfo
    contains mfg0TCPFPosition as key and value is double e.g. 100.00. This is specified only if the relation type is
    Mfg0MEMountToolToRobot.
    
    """
    context: BOMLine = None
    scope: BOMLine = None
    source: BOMLine = None
    target: BOMLine = None
    relationName: str = ''
    relationInfo: GeneralInfo = None


@dataclass
class ConnectorTableInfo(TcBaseObj):
    """
    The structure containing ItemRevision and its connector details.
    
    :var itemRev: ItemRevision for which connector details are to be retrieved.
    :var connectorProperties: List of structure containing Mfg0MEConnectorTableRow properties.
    Teamcenter::Soa::Manufacturing::_2012_02::GeneralInfo is an existing Data Structure that holds map for different
    properties. 
    The connectorsInfo contains information about following
    - String type relation properties of Mfg0MEConnectorTableRow. stringProps element holds these proerties as key.
    Below is the list of String type relation properties of Mfg0MEConnectorTableRow
    - mfg0ConnectorType as key. Value can be  Tool Frame Connector, Base frame connector, Riser frame connector.
    - mfg0ConnectorID as key. Value can be "Mount Point1". 
    - mfg0ConnectorName as key. Value can be "Base Frame"
    - Double type mfg0RelToOrigin property of Mfg0MEConnectorTableRow. doubleProps element of GeneralInfo contains
    mfg0RelToOrigin as key and value is double e.g. 100.00.
    
    """
    itemRev: BusinessObject = None
    connectorProperties: List[GeneralInfo] = ()
