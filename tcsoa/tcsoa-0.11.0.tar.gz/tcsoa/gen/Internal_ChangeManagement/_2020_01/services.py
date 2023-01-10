from __future__ import annotations

from tcsoa.gen.Internal.ChangeManagement._2020_01.MassUpdate import SaveImpactedAssembliesIn, HasActiveMarkupAssociatedOut
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class MassUpdateService(TcService):

    @classmethod
    def hasActiveMarkupAssociated(cls, changeObject: ItemRevision) -> HasActiveMarkupAssociatedOut:
        """
        This operation checks if there are active Mass Update Fnd0Markup objects associated with the PSBOMViewRevision
        of impacted ItemRevision objects related to the input change object ItemRevision.
        
        Use cases:
        When you remove the problem object ItemRevision from the change object ItemRevision of a Mass Update, any
        associated Fnd0Markup objects will be removed. Before the removal of the Fnd0Markup objects, this operation
        will check for the existence of associated Fnd0Markup objects and a confirmation message will be displayed.
        """
        return cls.execute_soa_method(
            method_name='hasActiveMarkupAssociated',
            library='Internal-ChangeManagement',
            service_date='2020_01',
            service_name='MassUpdate',
            params={'changeObject': changeObject},
            response_cls=HasActiveMarkupAssociatedOut,
        )

    @classmethod
    def saveImpactedAssemblies(cls, changeObject: ItemRevision, impactedObjectsInfo: List[SaveImpactedAssembliesIn]) -> ServiceData:
        """
        This operation saves proposed changes as Fnd0MarkupChange objects for an Fnd0Markup related to the
        PSBOMViewRevision of an impacted ItemRevision. Based on the modified properties specified on
        Fnd0MUImpactedParents, the operation will add, update or delete markup changes.
        
        Use cases:
        When you attach a problem ItemRevision to the ChangeItemRevision, corresponding impacted assembly parents of
        the problem object are listed for the Mass Update.
        You can select an action (Add Part, Replace Part, Remove Part, Remove Part as Substitute, and Add Part as
        Substitute) and choose a corresponding proposed solution object. When you save the action including its
        solution object, this operation stores it as Fnd0MarkupChange objects within the Fnd0Markup object related to
        the PSBOMViewRevision of the impacted ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='saveImpactedAssemblies',
            library='Internal-ChangeManagement',
            service_date='2020_01',
            service_name='MassUpdate',
            params={'changeObject': changeObject, 'impactedObjectsInfo': impactedObjectsInfo},
            response_cls=ServiceData,
        )
