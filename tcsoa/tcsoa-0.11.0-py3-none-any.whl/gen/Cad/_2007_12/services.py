from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from tcsoa.gen.Cad._2007_12.StructureManagement import DeleteRelativeStructurePref2, CreateOrUpdateAbsoluteStructureInfo2, DeleteRelativeStructureInfo2, CreateOrUpdateRelativeStructureInfo2, CreateOrUpdateRelativeStructurePref2, ClassicOptionsResponse, VariantConditionResponse, CreateOrUpdateAbsoluteStructurePref2, DeleteAssemblyArrangementsInfo2, DeleteAssemblyArrangementsPref
from tcsoa.gen.Cad._2007_01.StructureManagement import DeleteRelativeStructureResponse, CreateOrUpdateRelativeStructureResponse, CreateOrUpdateAbsoluteStructureResponse, DeleteAssemblyArrangementsResponse
from tcsoa.gen.Cad._2007_12.DataManagement import PartInfo2, CreateOrUpdatePartsPref
from tcsoa.gen.Cad._2007_01.DataManagement import CreateOrUpdatePartsResponse
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def queryClassicOptions(cls, inputRevisions: List[ItemRevision]) -> ClassicOptionsResponse:
        """
        This operation is to find classic variant options defined on an ItemRevision object(s).
        
        Use cases:
        The user can use this operation to find all the classic variant options defined on given ItemRevision object.
        The option and values can be used for configuration or creating other related objects like variant conditions,
        constraint (defaults, derived defaults and rule checks) rules or VariantRule objects.
        """
        return cls.execute_soa_method(
            method_name='queryClassicOptions',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'inputRevisions': inputRevisions},
            response_cls=ClassicOptionsResponse,
        )

    @classmethod
    def queryVariantConditions(cls, inputBomLines: List[BOMLine]) -> VariantConditionResponse:
        """
        This operation is to find a variant condition value ( load if - this is a type of variant expression represents
        variant condition) for a BOMLine object.
        
        Use cases:
        The user needs variant condition defined on the BOMLine object, for display or editing purpose.
        """
        return cls.execute_soa_method(
            method_name='queryVariantConditions',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'inputBomLines': inputBomLines},
            response_cls=VariantConditionResponse,
        )

    @classmethod
    def createOrUpdateAbsoluteStructure(cls, info: List[CreateOrUpdateAbsoluteStructureInfo2], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateAbsoluteStructurePref2) -> CreateOrUpdateAbsoluteStructureResponse:
        """
        This is the overloaded function of Cad::_2007_01::StructureManagement::createOrUpdateAbsoluteStructure.
        It takes an additional variable into the CreateOrUpdateAbsoluteStructurePref2 structure to hold the last
        modified date of the BVR with an extra preference value to check it with server modifed date to make a decision
        whether we want to make modification on BVR.
        CreateOrUpdateAbsoluteStucture allows the user to find or create the absolute structure network of objects and
        relations for the input model.
        The service first attempts to check for the presence of duplicate context objects and then validate the
        existence of the structure to be created.
        If any of the objects exist and the input attribute values differ from those already set, an attempt is made to
        update the values.
        Note: The following AbsOccData attributes are not supported for arrangement qualified overrides.
        These attributes can only be overridden at the bvr level (which applies to all arrangements).
        If these attributes are overridden in the AssemblyArrangementInfo, they will be ignored.
        1.child item
        2.GDE object
        3.instance number
        4.occurrence name
        5.note
        6.occurrence type
        7.Variant instance
        As we process one contextItemRev object at one time, it is assumed that all edits for a given contextItemRev
        come in as one set of input.
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in bomViewTypeName. 
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateAbsoluteStructure',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'info': info, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateAbsoluteStructureResponse,
        )

    @classmethod
    def createOrUpdateRelativeStructure(cls, inputs: List[CreateOrUpdateRelativeStructureInfo2], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateRelativeStructurePref2) -> CreateOrUpdateRelativeStructureResponse:
        """
        This is the overloaded function of Cad::_2007_01::StructureManagement::createOrUpdateRelativeStructure.
        It takes an additional variable into the CreateOrUpdateRelativeStructureInfo2 structure to hold the last
        modified date of the BVR with an extra preference value to check it with server modifed date to make a decision
        whether we want to make modification on BVR.
        Create or update the relative structure objects and relations for the input model.
        The service first attempts to check for the presence of duplicate context objects and then validate the
        existence of the structure to be created.
        If any of the objects exist but the input attribute values that differ from those already set, an attempt is
        made to update the values if possible.
        This service assumes the input is in a bottom-up format such that if any failures occur, the structure that is
        created will be consistent.
        No attempt is made in the service to rearrange the input and process it in the correct order.
        As we process one parent context Object at one time, it is assumed that all edits for a given parent context
        come in as one set of input.
        
        Exceptions:
        >Service exceptions are thrown for the following error situations:
        
        215005: The BOM view revision (BVR) is not checked out by the current user.
        215006: The BOM view revision is checked out by another user.
        215009: The object type name specified in the input preference does not exist.
        215010: The input CAD occurrence identifier does not correspond to a valid BOM line. This is an error when the
        complete input is false.
        215033: The input last modified date differs from actual.
        215034: The dataset or BVR was modified even when the input last modified dates was different than the current
        last modified data. 
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelativeStructure',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateRelativeStructureResponse,
        )

    @classmethod
    def deleteAssemblyArrangements(cls, info: List[DeleteAssemblyArrangementsInfo2], bomViewTypeName: str, pref: DeleteAssemblyArrangementsPref) -> DeleteAssemblyArrangementsResponse:
        """
        This operation deletes assembly arrangements and all the absolute occurrence data associated with the assembly
        arrangements.  It also deletes the relation between assembly arrangements and the BOM view revision object. The
        last modified date of the BVR can be specified for comparison against the last modified date in Teamcenter to
        ensure the BVR that contains the arrangement has not changed outside of this client context.
        
        Use cases:
        User deletes an existing assembly arrangement from an existing assembly.
        
        For this operation, the assembly is passed in as the 'itemRev' and the assembly arrangement is passed in
        through 'arrangements'.  The assembly arrangement is removed from the assembly, as well as the relation between
        the arrangement and the BVR, and the UID of the deleted arrangement is added to the ServiceData list of deleted
        objects.
        
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in 'bomViewTypeName'.
        """
        return cls.execute_soa_method(
            method_name='deleteAssemblyArrangements',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'info': info, 'bomViewTypeName': bomViewTypeName, 'pref': pref},
            response_cls=DeleteAssemblyArrangementsResponse,
        )

    @classmethod
    def deleteRelativeStructure(cls, inputs: List[DeleteRelativeStructureInfo2], bomViewTypeName: str, pref: DeleteRelativeStructurePref2) -> DeleteRelativeStructureResponse:
        """
        Deletes one or more first level children of a parent assembly.  This is the overloaded function of
        Cad::_2007_01::StructureManagement::deleteRelativeStructure.
        It takes an additional variable into the DeleteRelativeStructureInfo2 structure to hold the last modified date
        of the BVR with an extra preference value to check it with server modifed date to make a decision whether we
        want to make modification on BVR.
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in bomViewTypeName. 
        """
        return cls.execute_soa_method(
            method_name='deleteRelativeStructure',
            library='Cad',
            service_date='2007_12',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'pref': pref},
            response_cls=DeleteRelativeStructureResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateParts(cls, info: List[PartInfo2], pref: CreateOrUpdatePartsPref) -> CreateOrUpdatePartsResponse:
        """
        CreateOrUpdateParts allows the user to create or update a set of parts using Items, Item Revisions, Datasets
        and ExtraObjects and also changes the ownership of the newly created object to the user/group supplied.
        If the user supplies a valid Item object reference without specifying a valid item revision object reference or
        id, then only the item will be updated.
        If the user specifies a valid item object reference with a null item revision object reference and a non-null
        revision id, then a new item revision will be created and attached to the item with no relations from the new
        item revision to the previous item revision.
        If the user specifies a valid item object reference and a valid item revision object reference, then the item
        and item revision and related objects will be updated.
        If no item object reference or item revision object references are specified then a new item and item revision
        and related objects will be created.
        All objects created and updated will be returned in the ServiceData.
        All partial errors will contain the clientIDs for all items related to the error message, i.e. if a dataset
        encounters an error, then the ID for that erro will be the item client ID concantentated with the item revision
        id contantenated with the dataset client ID, all separated by semi-colons ( ; ).
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateParts',
            library='Cad',
            service_date='2007_12',
            service_name='DataManagement',
            params={'info': info, 'pref': pref},
            response_cls=CreateOrUpdatePartsResponse,
        )
