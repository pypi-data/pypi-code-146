from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_02.StructureVerification import EquivalentLines
from tcsoa.gen.Internal.StructureManagement._2018_11.MassUpdate import SaveImpactedAssembliesIn, HasActiveMarkupAssociatedOut
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.gen.Internal.StructureManagement._2018_11.StructureVerification import MountAttachComparisonsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.StructureManagement._2012_10.StructureVerification import StringToPartialMatchCriteria
from tcsoa.base import TcService


class MassUpdateService(TcService):

    @classmethod
    def hasActiveMarkupAssociated(cls, changeObject: ItemRevision) -> HasActiveMarkupAssociatedOut:
        """
        This operation checks if there are active Mass Update markups associated with the impacted items attached to
        the change object.
        
        Use cases:
        User tries to remove problem object from the change object from Mass Update, this will remove all the
        associated markups, if exists. Before removing, the existence of associated markups will be checked and
        confirmation message will be shown to the user.
        """
        return cls.execute_soa_method(
            method_name='hasActiveMarkupAssociated',
            library='Internal-StructureManagement',
            service_date='2018_11',
            service_name='MassUpdate',
            params={'changeObject': changeObject},
            response_cls=HasActiveMarkupAssociatedOut,
        )

    @classmethod
    def saveImpactedAssemblies(cls, changeObject: ItemRevision, impactedObjectsInfo: List[SaveImpactedAssembliesIn]) -> ServiceData:
        """
        This operation saves the proposed changes in the form of markup and markup change on parents BOM View Revision,
        based on the modified properties on Fnd0MUImpactedParents will add, update or delete markup changes and add
        parent BOM View revision.
        
        Use cases:
        Once user attached Problem Object to ChangeItemRevision, impacted assemblies listed on Mass Update.
        User can select Action (Add Part,Replace part, Remove Part and Substitutes &amp; Add Part as substitute) &amp; 
        its corresponding Proposed Solution Object, this operation saves action and proposed object as Fnd0Markup
        objects.
        """
        return cls.execute_soa_method(
            method_name='saveImpactedAssemblies',
            library='Internal-StructureManagement',
            service_date='2018_11',
            service_name='MassUpdate',
            params={'changeObject': changeObject, 'impactedObjectsInfo': impactedObjectsInfo},
            response_cls=ServiceData,
        )


class StructureVerificationService(TcService):

    @classmethod
    def getMountAttachComparisonDetails(cls, equivalentObjects: List[EquivalentLines], partialMatchCriteria: List[StringToPartialMatchCriteria]) -> MountAttachComparisonsResponse:
        """
        This operation returns the details of any differences between physical attachments including their relation
        properties for the supplied source and target BOMLine objects. 
        
        Physical attachments are secondary resources like tool or weld gun objects connected using
        Mfg0MEPhysicalAttachment and Mfg0MEMountToolToRobot relations. The operation takes the source and target
        BOMLine objects and compares their physical connection according to their types.
        
        For the equivalent primary object, the secondary should be equivalent, for example - tools are compared with
        tools and weld guns with weld guns. Also it compares the properties defined on the relation between physical
        attachments of source and target BOMLine objects. 
        
        The supported physical attachment relation types to compare are Mfg0MEPhysicalAttachment and
        Mfg0MEMountToolToRobot. 
        
        The secondary resources with their physical attachment relation from source and target objects are returned by
        this operation in the form of a table that is created by the output structures.
        
        Use cases:
        User creates an Alternative Collaboration Context (CC) structure from a Plant structure and Bill Of Equipment
        (BOE) structure. In the BOE structure, the resources have one or more physical attachments between them
        connected using Mfg0MEPhysicalAttachment and Mfg0MEMountToolToRobot relation. The mount and attach properties
        of the resources are defined on these relations.
        
        User sends such Alternative CC to Line Designer or Process Simulate application and manipulates mount or attach
        properties of these resources by performing actions.
        
        Now, the user wants to perform comparison of resources (attached or mounted as tools or weld guns) including
        properties defined on the relations between them within a particular scope in Teamcenter.
        """
        return cls.execute_soa_method(
            method_name='getMountAttachComparisonDetails',
            library='Internal-StructureManagement',
            service_date='2018_11',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'partialMatchCriteria': partialMatchCriteria},
            response_cls=MountAttachComparisonsResponse,
        )
