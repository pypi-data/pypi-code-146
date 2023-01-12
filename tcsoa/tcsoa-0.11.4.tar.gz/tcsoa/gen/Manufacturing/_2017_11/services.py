from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2017_11.DataManagement import GetPhysicalAttachmentsResponse, RemovePhysicalAttachmentRelInput, SetConnectorInput, GetConnectorResponse, SetPhysicalAttachmentsInput, GetPhysicalAttachmentsInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def removePhysicalAttachementRelation(cls, input: List[RemovePhysicalAttachmentRelInput]) -> ServiceData:
        """
        This operation deletes Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot relation between the AbsOccurrence of
        given source BOMLine and target BOMLine objects for given scope Mfg0BvrWorkarea and context Mfg0BvrWorkarea
        acting as a root of the structure.
        
        Use cases:
        Line Designer user wants to disconnect two connected resource object (for e.g. Mfg0MEFactoryTool from the
        Mfg0MERobot ) which are connected with Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot relation in a given
        scope Mfg0BvrWorkarea and context Mfg0BvrWorkarea acting as a root of the structure.
        """
        return cls.execute_soa_method(
            method_name='removePhysicalAttachementRelation',
            library='Manufacturing',
            service_date='2017_11',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def setConnectorInfo(cls, input: List[SetConnectorInput]) -> ServiceData:
        """
        Connector is Product and Manufacturing Information (PMI) object created by NX which is used to define the
        connection between two components used on shop floor. This operation sets the connector information stored as
        Mfg0MEConnectorTableRow in Mfg0MEConnectorTable. The Mfg0MEConnectorTableForm is attached to the ItemRevision. 
        If the Mfg0MEConnectorTableForm is not related to the ItemRevision the operation first creates
        Mfg0MEConnectorTableForm and attaches it to the given ItemRevision with a relation Mfg0MEConnectorTblFormRel.
        If given input connector id is not present in Mfg0MEConnectorTableRow, then a Mfg0MEConnectorTableRow is added
        in Mfg0MEConnectorTable with information connector type, connector name, connector ID and transformation. 
        If given input connector id is present in Mfg0MEConnectorTableRow,the row is updated with latest information. 
        All the Mfg0MEConnectorTableRow for which information is not given are removed from Mfg0MEConnectorTable.
        
        Use cases:
        Line Designer user wants to add, remove or update the connector information for ItemRevision
        """
        return cls.execute_soa_method(
            method_name='setConnectorInfo',
            library='Manufacturing',
            service_date='2017_11',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def setPhysicalAttachementsInScope(cls, input: List[SetPhysicalAttachmentsInput]) -> ServiceData:
        """
        This operation creates physical attachment Mfg0MEPhysicalAttachment or  Mfg0MEMountToolToRobot relation between
        the AbsOccurrence of given source BOMLine and target BOMLine objects for given scope Mfg0BvrWorkarea and
        context Mfg0BvrWorkarea acting as a root of the structure.
        
        Use cases:
        Line Designer user wants to set mount and attach information for BOMLine (e.g. Mfg0MEFactoryTool and
        Mfg0MERobot) using  Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot relation in a given scope
        Mfg0BvrWorkarea and context Mfg0BvrWorkarea acting as a root of the structure.
        """
        return cls.execute_soa_method(
            method_name='setPhysicalAttachementsInScope',
            library='Manufacturing',
            service_date='2017_11',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getConnectorInfo(cls, itemRevs: List[BusinessObject]) -> GetConnectorResponse:
        """
        Connector is Product and Manufacturing Information (PMI) object created by NX which is used to define the
        connection between two components used on shop floor. This operation retrieves the information of connectors
        represented as a Mfg0MEConnectorTableRow in Mfg0MEConnectorTable. 
        Mfg0MEConnectorTableRow has information about connector type, connector name, connector ID and transformation.
        The Mfg0MEConnectorTableForm holds Mfg0MEConnectorTable and is related to ItemRevision through the relation
        Mfg0MEConnectorTblFormRel.
        
        Use cases:
        Connector is Product and Manufacturing Information (PMI) object created by NX which is used to define the
        connection between two components used on shop floor. E.g. Mfg0Conveyor and Mfg0Conveyor or Mfg0Conveyor and
        Mfg0MERobot. Line Designer user wants to retrieve connector information for ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='getConnectorInfo',
            library='Manufacturing',
            service_date='2017_11',
            service_name='DataManagement',
            params={'itemRevs': itemRevs},
            response_cls=GetConnectorResponse,
        )

    @classmethod
    def getPhysicalAttachmentsInScope(cls, input: List[GetPhysicalAttachmentsInput]) -> GetPhysicalAttachmentsResponse:
        """
        This operation retrievs all physical attachments (Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot) relations
        defined between two BOMLine objects that are children of the given scope Mfg0BvrWorkarea and context
        Mfg0BvrWorkarea acting as a root of the structure.
        This operation
        - Processes the input scope Mfg0BvrWorkarea under root context Mfg0BvrWorkarea in Bill of Equipment structure.
        - Traverses   the scope, finds the AbsOccurrence under the scope related with Mfg0MEPhysicalAttachment or
        Mfg0MEMountToolToRobot relation. From primary AbsOccurrence of relation Mfg0MEPhysicalAttachment or
        Mfg0MEMountToolToRobot it collects source BOMLine and from secondary AbsOccurrence it collects target BOMLine
        along with the relation properties on Mfg0MEPhysicalAttachment or Mfg0MEMountToolToRobot.
        
        
        
        Use cases:
        Line Designer user wants to retrieve mount and attachment information for the BOMLine connections with
        Mfg0MEPhysicalAttachment relation in a given scope of Mfg0BvrWorkarea and Mfg0BvrWorkarea acting as a root of
        the structure.
        """
        return cls.execute_soa_method(
            method_name='getPhysicalAttachmentsInScope',
            library='Manufacturing',
            service_date='2017_11',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetPhysicalAttachmentsResponse,
        )
