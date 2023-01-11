from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2013_05.StructureExpansionLite import PartialExpansionControls, LineAndPaths, Controls
from tcsoa.gen.Internal.StructureManagement._2013_12.StructureExpansionLite import ExpansionResponse2
from typing import List
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureExpansionLiteService(TcService):

    @classmethod
    def getUndelivered2(cls, undeliveredLineUids: List[str], controls: Controls) -> ExpansionResponse2:
        """
        This operation returns Fnd0BOMLineLite as objects for input UIDs of Fnd0BOMLineLite. 
        It may be required to invoke this operation more than once as the number of Fnd0BOMLineLite returned depends on
        'outputPageSize' specified in 'Controls'. The 'RelationAndTypesCriteria' of 'Controls' is used to retrieve
        Dataset, named references objects with FMS tickets when named reference object is file.
        
        
        Use cases:
        This operation helps while working with large structure. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets VariantRule on BOMWindow.
        3. Client invokes 'expandNext2' with top BOMLine to get next set of configured children as Fnd0BOMLineLite
        objects.
        4. Client checks if there are any undelivered Fnd0BOMLineLite objects in 'ExpansionResponse2'
        5. Client invokes 'getUndelivered2' operation to get next set of undelivered Fnd0BOMLineLite(s) along with
        Dataset.
        6. Client uses configured structure and Dataset to render the product.
        7. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='getUndelivered2',
            library='Internal-StructureManagement',
            service_date='2013_12',
            service_name='StructureExpansionLite',
            params={'undeliveredLineUids': undeliveredLineUids, 'controls': controls},
            response_cls=ExpansionResponse2,
        )

    @classmethod
    def unloadBelow2(cls, lines: List[RuntimeBusinessObject]) -> ServiceData:
        """
        This operation destroys Fnd0BOMLineLite children lines of input Fnd0BOMLineLite or BOMLine parent lines from
        Teamcenter server.
        
        Use cases:
        This operation is useful to release resources after rendering product.
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets VariantRule on BOMWindow.
        3. Client invokes 'expandNext2' with top BOMLine to get next set of configured children as Fnd0BOMLineLite
        objects.
        4. Client performs expansion.
        5. Client uses configured structure and Dataset to render the product.
        6. Client releases resource on Teamcenter server by calling unload operation.
        """
        return cls.execute_soa_method(
            method_name='unloadBelow2',
            library='Internal-StructureManagement',
            service_date='2013_12',
            service_name='StructureExpansionLite',
            params={'lines': lines},
            response_cls=ServiceData,
        )

    @classmethod
    def expandBasedOnOccurrenceList2(cls, linePaths: List[LineAndPaths], controls: PartialExpansionControls) -> ExpansionResponse2:
        """
        The operation performs partial expansion for the given 'LineAndPaths'. This operation returns Dataset(s), named
        reference objects with FMS tickets which are requested through 'RelationAndTypesCriteria' in
        'PartialExpansionControls' for the partially expanded child Fnd0BOMLineLite(s).
        Note that partial expansion for ImanItemBOPLine is not supported.
        
        
        Use cases:
        This operation is suited to get partially expanded configured structure and related Dataset for read-only
        scenarios, e.g. Visualization. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets VariantRule on BOMWindow.
        3. Client pulls the 'occurrence_list' from the VisStructureContext object.
        3. Client invokes 'expandBasedOnOccurrenceList2' to get partially expanded configured structure.
        4. Client uses configured structure and Dataset to render the product.
        5. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='expandBasedOnOccurrenceList2',
            library='Internal-StructureManagement',
            service_date='2013_12',
            service_name='StructureExpansionLite',
            params={'linePaths': linePaths, 'controls': controls},
            response_cls=ExpansionResponse2,
        )

    @classmethod
    def expandNext2(cls, linesToExpand: List[RuntimeBusinessObject], controls: Controls) -> ExpansionResponse2:
        """
        The operation performs top down expansion for the given parent Fnd0BOMLineLite or BOMLine. The level of
        expansion is based upon input 'Controls' such as maxLevel. The 'RelationAndTypesCriteria' of 'Controls' is used
        to retrieve Dataset, named references objects with FMS tickets when named reference object is file.
        
        Use cases:
        This operation is suited to get configured structure and related Dataset for read-only scenarios, e.g.
        Visualization. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes 'expandNext2' with top BOMLine to get next set of configured children as Fnd0BOMLineLite
        objects.
        4. Client invokes 'expandNext2' recursively till structure is fully expanded.
        5. Client uses configured structure and Dataset to render the product.
        6. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='expandNext2',
            library='Internal-StructureManagement',
            service_date='2013_12',
            service_name='StructureExpansionLite',
            params={'linesToExpand': linesToExpand, 'controls': controls},
            response_cls=ExpansionResponse2,
        )
