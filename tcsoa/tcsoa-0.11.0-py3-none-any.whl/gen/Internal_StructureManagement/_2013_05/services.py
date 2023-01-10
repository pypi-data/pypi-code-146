from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2013_05.StructureExpansionLite import PartialExpansionControls, ExpansionResponse, LineAndPaths, Controls
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject, Fnd0BOMLineLite
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureExpansionLiteService(TcService):

    @classmethod
    def getUndelivered(cls, undeliveredLineUids: List[str], controls: Controls) -> ExpansionResponse:
        """
        This operation returns Fnd0BomLineLite as objects for input UIDs of Fnd0BomLineLite. 
        It may be required to invoke this operation more than once as the number of Fnd0BomLineLite returned depends on
        outputPageSize specified in 'Controls'. The 'RelationAndTypesCriteria' of 'Controls' is used to retrieve
        Dataset, named references objects with FMS tickets when named reference object is file.
        
        
        Use cases:
        This operation helps while working with large structure. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes expandNext with top BOMLine to get next set of configured children as Fnd0BomLineLite objects
        4. Client checks if there are any undelivered Fnd0BomLineLite objects in 'ExpansionResponse'
        5. Client invokes getUndelivered operation to get next set of undelivered Fnd0BomLineLites along with Dataset
        6. Client uses configured structure and Dataset to render the product
        7. Client closes the BOMWindow to release resources
        """
        return cls.execute_soa_method(
            method_name='getUndelivered',
            library='Internal-StructureManagement',
            service_date='2013_05',
            service_name='StructureExpansionLite',
            params={'undeliveredLineUids': undeliveredLineUids, 'controls': controls},
            response_cls=ExpansionResponse,
        )

    @classmethod
    def unloadBelow(cls, lines: List[Fnd0BOMLineLite]) -> ServiceData:
        """
        This operation destroys children of input Fnd0BomLineLite from Teamcenter server. 
        
        
        
        Use cases:
        This operation is useful to release resources after rendering product.
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes expandNext with top BOMLine to get next set of configured children as Fnd0BomLineLite objects
        4. Client invokes expandNext recursively till structure is fully expanded
        5. Client uses configured structure and Dataset to render the product
        6. Client releases resource on Teamcenter server by calling unload operation
        """
        return cls.execute_soa_method(
            method_name='unloadBelow',
            library='Internal-StructureManagement',
            service_date='2013_05',
            service_name='StructureExpansionLite',
            params={'lines': lines},
            response_cls=ServiceData,
        )

    @classmethod
    def expandBasedOnOccurrenceList(cls, linePaths: List[LineAndPaths], controls: PartialExpansionControls) -> ExpansionResponse:
        """
        The operation performs partial expansion for the given 'LineAndPaths'. This operation also returns Dataset(s),
        named reference objects with FMS tickets which are requested through 'RelationAndTypesCriteria' in
        'PartialExpansionControls' for the paritally expanded child Fnd0BOMLineLite(s).
        
        
        
        
        Use cases:
        This operation is suited to get partially expanded configured structure and related Dataset for read-only
        scenarios, e.g. Visualization. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine
        2. Client optionally sets Variant Rule on BOMWindow
        3. Client pulls the occurrence_list from the VisStructureContext object
        3. Client invokes expandBasedOnOccurrenceList to get partially expanded configured structure
        4. Client uses configured structure and Dataset to render the product
        5. Client closes the BOMWindow to release resources
         
        """
        return cls.execute_soa_method(
            method_name='expandBasedOnOccurrenceList',
            library='Internal-StructureManagement',
            service_date='2013_05',
            service_name='StructureExpansionLite',
            params={'linePaths': linePaths, 'controls': controls},
            response_cls=ExpansionResponse,
        )

    @classmethod
    def expandNext(cls, linesToExpand: List[RuntimeBusinessObject], controls: Controls) -> ExpansionResponse:
        """
        The operation performs top down expansion for the given parent Fnd0BomLineLite or BOMLine. The level of
        expansion is based upon input 'Controls' such as maxLevel. The 'RelationAndTypesCriteria' of 'Controls' is used
        to retrieve Dataset, named references objects with FMS tickets when named reference object is file.
        
        
        
        
        
        
        Use cases:
        This operation is suited to get configured structure and related Dataset for read-only scenarios, e.g.
        Visualization. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes expandNext with top BOMLine to get next set of configured children as Fnd0BomLineLite objects
        4. Client invokes expandNext recursively till structure is fully expanded
        5. Client uses configured structure and Dataset to render the product
        6. Client closes the BOMWindow to release resources
        """
        return cls.execute_soa_method(
            method_name='expandNext',
            library='Internal-StructureManagement',
            service_date='2013_05',
            service_name='StructureExpansionLite',
            params={'linesToExpand': linesToExpand, 'controls': controls},
            response_cls=ExpansionResponse,
        )
