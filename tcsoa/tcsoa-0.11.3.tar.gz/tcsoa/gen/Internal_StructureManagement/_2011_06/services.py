from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2011_06.IncrementalChange import AttributeChangeResponse, StructureChangeResponse, PredecessorChangeResponse, AttachmentChangeResponse, ParentAndChildComponentsResponse
from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, MECfgLine, ItemRevision
from tcsoa.gen.Internal.StructureManagement._2011_06.VariantManagement import ModularOptionsInput, BOMVariantConfigOptionResponse, ModularOptionsForBomResponse
from tcsoa.gen.Internal.StructureManagement._2011_06.Structure import CreateOrSaveAsPSBOMViewRevisionInput, CreateOrSaveAsPSBOMViewRevisionResponse, GetAllAvailableViewTypesInput, GetAvailableViewTypesResponse
from typing import List
from tcsoa.base import TcService


class IncrementalChangeService(TcService):

    @classmethod
    def getStructureChanges(cls, bomlines: List[BOMLine], fRefresh: bool) -> StructureChangeResponse:
        """
        Gets the changes on the occurrence for the given list of BOMLine objects captured in incremental change (IC)
        context.  All changes are returned not just those from the configured window.
        
        Use cases:
        User needs to find the changes done on the occurrence in incremental change (IC) context, for a given set of
        BOMLine objects.  The input to the operation is a list of BOMLine objects.  The output is list of
        IncrementalChangeElement (ICE) objects.
        """
        return cls.execute_soa_method(
            method_name='getStructureChanges',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='IncrementalChange',
            params={'bomlines': bomlines, 'fRefresh': fRefresh},
            response_cls=StructureChangeResponse,
        )

    @classmethod
    def getAttachmentChanges(cls, attachmentlines: List[MECfgLine], fRefresh: bool) -> AttachmentChangeResponse:
        """
        This operation gets changes on datasets, forms and relations under incrementalchange (IC) context.  All changes
        and not just the ones configured in the window are returned.
        
        Use cases:
        The user needs to get attachment data changes on datasets, forms, and/or relations under incremental change
        context. The input to this operation is a list of attachment lines.  The output is a list of attachment change
        information like the type of IncrementalChangeElement, and in which incremental change revision context.
        """
        return cls.execute_soa_method(
            method_name='getAttachmentChanges',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='IncrementalChange',
            params={'attachmentlines': attachmentlines, 'fRefresh': fRefresh},
            response_cls=AttachmentChangeResponse,
        )

    @classmethod
    def getAttributeChanges(cls, attributeOccLines: List[BOMLine], fRefresh: bool) -> AttributeChangeResponse:
        """
        This operation gets the changes on the occurrence attribute (notes, conditions) tracked under incremental
        change context.
        
        Use cases:
        The user needs to get the attribute changes on the occurrence under incremental change (IC) context for one or
        many BOMLine objects.  The user calls the operation 'getAttributeChanges' with a list of input BOMLine objects.
         The output returned is a list of attribute information for each BOMLine object.
        """
        return cls.execute_soa_method(
            method_name='getAttributeChanges',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='IncrementalChange',
            params={'attributeOccLines': attributeOccLines, 'fRefresh': fRefresh},
            response_cls=AttributeChangeResponse,
        )

    @classmethod
    def getParentAndChildComponents(cls, icRevision: ItemRevision) -> ParentAndChildComponentsResponse:
        """
        Gets the parent and child components for the changes on occurrences, occurrence attributes, datasets and/or
        forms under an incremental change context.
        
        Use cases:
        The user wants to get the parent and child object for all the changes made in the context of a given
        incremental change revision.  The input to this operation is the incremental change revision.  The output is a
        list of structures containing parent and child objects for each IncrementalChangeElement object.
        """
        return cls.execute_soa_method(
            method_name='getParentAndChildComponents',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='IncrementalChange',
            params={'icRevision': icRevision},
            response_cls=ParentAndChildComponentsResponse,
        )

    @classmethod
    def getPredecessorChanges(cls, predecessorLines: List[BOMLine], fRefresh: bool) -> PredecessorChangeResponse:
        """
        For a given set of BOMLine objects, 'getPredecessorChanges' returns predecessor changes captured in incremental
        change (IC) context.  All changes and not just the ones configured in the window are returned.
        are returned.
        Note:
        A predecessor represents a sequence relationship between two processes or operations. An occurrence, which
        represents a process or operation, has an attribute predList to store a list of predecessors for it.  When a
        new predecessor is added for a process or operation, it appends an occurrence to the predList. Similarly when a
        predecessor is removed for a process or operation, it removes the occurrence from the predList. To manage
        changes to predecessors of a process or operation, an IncrementalChangeElement (ICE) object will be created
        whenever a predecessor has been added or removed in the context of incremental change (IC).
        
        
        Use cases:
        The user wants to get the predecessor changes tracked by incremental change (IC) context.  A BOMLine could have
        multiple predecessor changes.  A list of BOMLine objects is input to this operation and a list of predecessor
        IncrementalChangeElement (ICE) object(s) are returned.
        """
        return cls.execute_soa_method(
            method_name='getPredecessorChanges',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='IncrementalChange',
            params={'predecessorLines': predecessorLines, 'fRefresh': fRefresh},
            response_cls=PredecessorChangeResponse,
        )


class StructureService(TcService):

    @classmethod
    def createOrSavePSBOMViewRevision(cls, createOrSavePSBOMViewRevisionInputs: List[CreateOrSaveAsPSBOMViewRevisionInput]) -> CreateOrSaveAsPSBOMViewRevisionResponse:
        """
        This operation is to create a new PSBOMViewRevision object or perform a Save As based on existing
        PSBOMViewRevision object.
        
        Use cases:
        The user wants to create a new PSBOMViewRevision object or want to perform Save As based on existing
        PSBOMViewRevision object.
        """
        return cls.execute_soa_method(
            method_name='createOrSavePSBOMViewRevision',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'createOrSavePSBOMViewRevisionInputs': createOrSavePSBOMViewRevisionInputs},
            response_cls=CreateOrSaveAsPSBOMViewRevisionResponse,
        )

    @classmethod
    def getAvailableViewTypes(cls, getAvailableViewTypesInputs: List[GetAllAvailableViewTypesInput]) -> GetAvailableViewTypesResponse:
        """
        This operation is to query the available PSBOMView types objects for the given ItemRevision object. The output
        available list will exclude the PSBOMView types which are already created on given ItemRevision object.
        
        Use cases:
        This operation is called when user wants to know all the available PSBOMView type objects for a given
        ItemRevision object which are not yet used.
        """
        return cls.execute_soa_method(
            method_name='getAvailableViewTypes',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'getAvailableViewTypesInputs': getAvailableViewTypesInputs},
            response_cls=GetAvailableViewTypesResponse,
        )


class VariantManagementService(TcService):

    @classmethod
    def getBOMVariantConfigOptions(cls, bomWindow: BOMWindow, bomLine: BOMLine) -> BOMVariantConfigOptionResponse:
        """
        This operation will provide currently applied variant configuration for a given BOMLine object in its
        respective BOMWindow object. This will output variant configuration information for both modular variants as
        well as legacy variants. Output Variant configuration consists of variant option name, item id, type of variant
        option (classic or modular), currently set value, currently value how-set and option description.
        
        Use cases:
        This operation should be used when user wants to know currently applied variant configuration on a BOMLine in a
        BOMWindow.
        """
        return cls.execute_soa_method(
            method_name='getBOMVariantConfigOptions',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='VariantManagement',
            params={'bomWindow': bomWindow, 'bomLine': bomLine},
            response_cls=BOMVariantConfigOptionResponse,
        )

    @classmethod
    def getModularOptionsForBom(cls, modules: List[ModularOptionsInput]) -> ModularOptionsForBomResponse:
        """
        This operation will provide all modular variant options defined or available on given BOMLine (also called as
        Module). Multiple BOMLine objects can be given as input, and operation will return modular variant options
        defined for each input BOMLine object.
        
        Use cases:
        It should be used when user wants to get all defined or available Modular Variant Option information for one or
        some set of BOMLine object(s).
        """
        return cls.execute_soa_method(
            method_name='getModularOptionsForBom',
            library='Internal-StructureManagement',
            service_date='2011_06',
            service_name='VariantManagement',
            params={'modules': modules},
            response_cls=ModularOptionsForBomResponse,
        )
