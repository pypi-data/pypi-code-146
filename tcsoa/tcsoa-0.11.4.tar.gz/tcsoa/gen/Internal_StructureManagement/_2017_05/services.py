from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2017_05.StructureVerification import AttachmentComparisonDetailsResponse
from tcsoa.gen.Internal.StructureManagement._2017_05.StructureExpansionLite import Controls2, Controls3, ExpansionResponse3
from tcsoa.gen.Internal.StructureManagement._2017_05.StructureLiteConversion import ConversionResponse
from tcsoa.gen.StructureManagement._2012_02.StructureVerification import EquivalentLines
from typing import List
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject
from tcsoa.gen.StructureManagement._2012_10.StructureVerification import StringToPartialMatchCriteria
from tcsoa.base import TcService


class StructureExpansionLiteService(TcService):

    @classmethod
    def getUndelivered3(cls, undeliveredLineUids: List[str], controls: Controls3) -> ExpansionResponse3:
        """
        This operation returns Fnd0BomLineLite as objects for input UIDs of Fnd0BomLineLite. 
        It may be required to invoke this operation more than once as the number of Fnd0BomLineLite returned depends on
        outputPageSize specified in 'Controls'. The 'RelationAndTypesCriteria' of 'Controls' is used to retrieve
        Dataset, named references objects with FMS tickets when named reference object is file.
        
        Use cases:
        This operation helps while working with large structure. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes expandNext3 operation with top BOMLine to get next set of configured children as
        Fnd0BomLineLite objects.
        4. Client checks if there are any undelivered Fnd0BomLineLite objects in ExpansionResponse.
        5. Client invokes getUndelivered3 operation to get next set of undelivered Fnd0BomLineLites along with Dataset.
        6. Client uses response from expandNext3 operation to create a configured structure including Dataset
        information on client and Dataset to render the product.
        7. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='getUndelivered3',
            library='Internal-StructureManagement',
            service_date='2017_05',
            service_name='StructureExpansionLite',
            params={'undeliveredLineUids': undeliveredLineUids, 'controls': controls},
            response_cls=ExpansionResponse3,
        )

    @classmethod
    def expandNext3(cls, linesToExpand: List[RuntimeBusinessObject], controls: Controls2) -> ExpansionResponse3:
        """
        The operation performs top down expansion for the given parent Fnd0BOMLineLite or BOMLine. The level of
        expansion is based upon input 'Controls' such as maxLevel. The 'RelationAndTypesCriteria' of 'Controls' is used
        to retrieve Dataset, named references objects with FMS tickets when named reference object is file.
        Note that partial expansion for ImanItemBOPLine is not supported.
        
        Use cases:
        This operation is suited to get configured structure and related Dataset for read-only scenarios, e.g.
        Visualization, NX. 
        
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes expandNext3 operation with top BOMLine to get next set of configured children as
        Fnd0BOMLineLite objects.
        4. Client invokes expandNext3 recursively until till the structure is fully completely expanded.
        5. Client uses response from expandNext3 operation to create a configured structure including Dataset
        information on client and Dataset to render the product.
        6. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='expandNext3',
            library='Internal-StructureManagement',
            service_date='2017_05',
            service_name='StructureExpansionLite',
            params={'linesToExpand': linesToExpand, 'controls': controls},
            response_cls=ExpansionResponse3,
        )


class StructureLiteConversionService(TcService):

    @classmethod
    def liteBOMLinesToBOMLines(cls, linesToConvert: List[RuntimeBusinessObject]) -> ConversionResponse:
        """
        The operation converts the given list of Fnd0BOMLineLite to list of BOMLine. It also converts all the
        Fnd0BOMLineLite parents of the input Fnd0BOMLineLite till until it finds the BOMLine parent in the same
        hierarchy. No Fnd0BOMLineLite objects from same parent hierarchy are expected.
        
        Use cases:
        1. Client creates BOMWindow with RevisionRule and sets top BOMLine.
        2. Client optionally sets Variant Rule on BOMWindow.
        3. Client invokes 'expandNext3' with top BOMLine to get next set of configured children as Fnd0BOMLineLite
        objects.
        4. Client optionally invokes 'expandNext3' recursively till structure is fully expanded.
        5. Client uses 'liteBOMLinesToBOMLines' operation to convert a Fnd0BOMLineLite line to BOMLine. This line can
        be from any level of assembly but single Fnd0BOMLineLite line should be passed from the same parent hierarchy.
        6. Client closes the BOMWindow to release resources.
        """
        return cls.execute_soa_method(
            method_name='liteBOMLinesToBOMLines',
            library='Internal-StructureManagement',
            service_date='2017_05',
            service_name='StructureLiteConversion',
            params={'linesToConvert': linesToConvert},
            response_cls=ConversionResponse,
        )


class StructureVerificationService(TcService):

    @classmethod
    def getAttachmentComparisonDetails(cls, equivalentObjects: List[EquivalentLines], partialMatchCriteria: List[StringToPartialMatchCriteria]) -> AttachmentComparisonDetailsResponse:
        """
        This operation returns the details of any differences between attachments for the supplied source and target
        BOMLine objects. Attachments can be Dataset or Form objects. The operation takes the source and target BOMLine
        objects and compares their attachments according to their types &ndash; Dataset are compared with Dataset and
        Form with Form. The supported attachment relation types to compare are governed by
        MEAccountabilityCheckIncludedAttachmentRelations site preference such as the relation type Cps0LBRel for the
        dataset ProcessSimulatePLCLB etc. The source and target attachments are returned by this operation in the form
        of a table that is created by the output structures.
        
        Use cases:
        A user wants to perform comparison of Attachments within a particular scope.
        """
        return cls.execute_soa_method(
            method_name='getAttachmentComparisonDetails',
            library='Internal-StructureManagement',
            service_date='2017_05',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'partialMatchCriteria': partialMatchCriteria},
            response_cls=AttachmentComparisonDetailsResponse,
        )
