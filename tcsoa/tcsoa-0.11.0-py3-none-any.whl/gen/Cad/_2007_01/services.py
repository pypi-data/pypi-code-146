from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow, BusinessObject, ItemRevision, Folder
from tcsoa.gen.Cad._2007_01.StructureManagement import CreateOrUpdateRelativeStructureResponse, DeleteAssemblyArrangementsResponse, ExpandPSAllLevelsPref, GetVariantRulesResponse, CreateOrUpdateAbsoluteStructurePref, CreateBOMWindowsResponse, CreateOrUpdateRelativeStructurePref, CreateBOMWindowsInfo, CreateOrUpdateAbsoluteStructureResponse, ExpandPSOneLevelPref, DeleteRelativeStructureInfo, CreateOrUpdateAbsoluteStructureInfo, DeleteRelativeStructurePref, DeleteRelativeStructureResponse, ExpandPSAllLevelsResponse, ExpandPSOneLevelResponse, ExpandPSOneLevelInfo, CreateOrUpdateRelativeStructureInfo, DeleteAssemblyArrangementsInfo, ExpandPSAllLevelsInfo, CloseBOMWindowsResponse, GetRevisionRulesResponse
from tcsoa.gen.Cad._2007_01.DataManagement import ExpandFolderForCADPref, CreateOrUpdateRelationsInfo, GetAttrMappingsForDatasetTypeCriteria, CreateOrUpdateRelationsResponse, GenerateAlternateIdsProperties, CreateOrUpdatePartsResponse, ExpandGRMRelationsPref, ResolveAttrMappingsForDatasetResponse, GetAttrMappingsForDatasetTypeResponse, ExpandFoldersForCADResponse, PartInfo, GetAvailableTypesResponse, ExpandGRMRelationsResponse, ResolveAttrMappingsForDatasetInfo, GetAllAttrMappingsResponse, GenerateAlternateIdsResponse, ExpandPrimaryObjectsPref, CreateOrUpdateRelationsPref, ExpandPrimaryObjectsResponse
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getRevisionRules(cls) -> GetRevisionRulesResponse:
        """
        The GetRevisionRules service gets all the persistent revision rules in the database. It along with the revision
        rules returns its runtime configuration properties status of being fixed or not.
        
        Exceptions:
        >ServiceException Thrown if the system fails retreiving the list of revision rules.
        """
        return cls.execute_soa_method(
            method_name='getRevisionRules',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={},
            response_cls=GetRevisionRulesResponse,
        )

    @classmethod
    def getVariantRules(cls, itemRevs: List[ItemRevision]) -> GetVariantRulesResponse:
        """
        The GetVariantRules service gets all the variant rules in the database for the given Item Revision. To get
        Product Configurator authored variant rules, value of preference PSM_default_configurator_context must be true.
        
        Exceptions:
        >ServiceException Thrown if the there are no ItemRevision objects input.
        """
        return cls.execute_soa_method(
            method_name='getVariantRules',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'itemRevs': itemRevs},
            response_cls=GetVariantRulesResponse,
        )

    @classmethod
    def closeBOMWindows(cls, bomWindows: List[BOMWindow]) -> CloseBOMWindowsResponse:
        """
        Closes a BOMWindow.  Must be used to close the BOMWindow created during Create BOM Window after calls to Expand
        Product Structure services are complete.
        """
        return cls.execute_soa_method(
            method_name='closeBOMWindows',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'bomWindows': bomWindows},
            response_cls=CloseBOMWindowsResponse,
        )

    @classmethod
    def createBOMWindows(cls, info: List[CreateBOMWindowsInfo]) -> CreateBOMWindowsResponse:
        """
        Creates a BOMWindow and sets the input Item Revision as the top line.  Can be used to create the BOMLine for
        input to Expand Product Structure services.  All BOMLines under this window are unpacked.  To use the
        Teamcenter default unitNo or use your input RevisionRule with no changes, you must set unitNo to -1 in
        RevisionRuleEntryProps::unitNo.  If it is not specified, your input rule will function as a modified/transient
        revision rule with a unitNo of 0.
        """
        return cls.execute_soa_method(
            method_name='createBOMWindows',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateBOMWindowsResponse,
        )

    @classmethod
    def createOrUpdateAbsoluteStructure(cls, info: List[CreateOrUpdateAbsoluteStructureInfo], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateAbsoluteStructurePref) -> CreateOrUpdateAbsoluteStructureResponse:
        """
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
            service_date='2007_01',
            service_name='StructureManagement',
            params={'info': info, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateAbsoluteStructureResponse,
        )

    @classmethod
    def createOrUpdateRelativeStructure(cls, inputs: List[CreateOrUpdateRelativeStructureInfo], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateRelativeStructurePref) -> CreateOrUpdateRelativeStructureResponse:
        """
        Create or update the relative structure objects and relations for the input model.
        The service first attempts to check for the presence of duplicate context objects and then validate the
        existence of the structure to be created.
        If any of the objects exist but the input attribute values that differ from those already set, an attempt is
        made to update the values if possible.
        This service assumes the input is in a bottom-up format such that if any failures occur, the structure that is
        created will be consistent.
        No attempt is made in the service to rearrange the input and process it in the correct order.
        As we process one parent context object at one time, it is assumed that all edits for a given parent context
        come in as one set of input.
        
        Exceptions:
        >Service exceptions are thrown for the following error situations:
        
        215005: The BOM view revision (BVR) is not checked out by the current user.
        215006: The BOM view revision is checked out by another user.
        215009: The object type name specified in the input preference does not exist.
        215010: The input CAD occurrence identifier does not correspond to a valid BOM line. This is an error when the
        complete input is false.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelativeStructure',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateRelativeStructureResponse,
        )

    @classmethod
    def deleteAssemblyArrangements(cls, info: List[DeleteAssemblyArrangementsInfo], bomViewTypeName: str) -> DeleteAssemblyArrangementsResponse:
        """
        Deletes assembly arrangements and all the absolute occurrence data associated with the assembly arrangements,
        it also delete the relation between assembly arrangements and bvr.
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in bomViewTypeName. 
        """
        return cls.execute_soa_method(
            method_name='deleteAssemblyArrangements',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'info': info, 'bomViewTypeName': bomViewTypeName},
            response_cls=DeleteAssemblyArrangementsResponse,
        )

    @classmethod
    def deleteRelativeStructure(cls, inputs: List[DeleteRelativeStructureInfo], bomViewTypeName: str, pref: DeleteRelativeStructurePref) -> DeleteRelativeStructureResponse:
        """
        Deletes one or more first level children of a parent assembly.
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in bomViewTypeName. 
        """
        return cls.execute_soa_method(
            method_name='deleteRelativeStructure',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'pref': pref},
            response_cls=DeleteRelativeStructureResponse,
        )

    @classmethod
    def expandPSAllLevels(cls, input: ExpandPSAllLevelsInfo, pref: ExpandPSAllLevelsPref) -> ExpandPSAllLevelsResponse:
        """
        Finds the chilren at all levels given parent bomlines. Also if required gets the objects of given type and
        relation that are attached to the parent and children
        """
        return cls.execute_soa_method(
            method_name='expandPSAllLevels',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'input': input, 'pref': pref},
            response_cls=ExpandPSAllLevelsResponse,
        )

    @classmethod
    def expandPSOneLevel(cls, input: ExpandPSOneLevelInfo, pref: ExpandPSOneLevelPref) -> ExpandPSOneLevelResponse:
        """
        Finds the first level chilren of given parent bomlines. Also if required gets the objects of given type and
        relation that are attached to the parent and children
        """
        return cls.execute_soa_method(
            method_name='expandPSOneLevel',
            library='Cad',
            service_date='2007_01',
            service_name='StructureManagement',
            params={'input': input, 'pref': pref},
            response_cls=ExpandPSOneLevelResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def resolveAttrMappingsForDataset(cls, info: List[ResolveAttrMappingsForDatasetInfo]) -> ResolveAttrMappingsForDatasetResponse:
        """
        Retrieves CAD attribute mapped properties for one or more datasets.
        
        Use cases:
        User does a FileOpen of Teamcenter Item or Dataset (CAD Part).  CAD properties mapped to Teamcenter attribute
        values are shown in the Part attribute display.
        """
        return cls.execute_soa_method(
            method_name='resolveAttrMappingsForDataset',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ResolveAttrMappingsForDatasetResponse,
        )

    @classmethod
    def createOrUpdateParts(cls, info: List[PartInfo]) -> CreateOrUpdatePartsResponse:
        """
        CreateOrUpdateParts allows the user to create or update a set of parts using Items, Item Revisions, Datasets
        and ExtraObjects.
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
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info},
            response_cls=CreateOrUpdatePartsResponse,
        )

    @classmethod
    def createOrUpdateRelations(cls, info: List[CreateOrUpdateRelationsInfo], complete: bool, pref: CreateOrUpdateRelationsPref) -> CreateOrUpdateRelationsResponse:
        """
        'createOrUpdateRelations' creates or updates GRM relations between existing objects in Teamcenter. If the
        'complete' flag is set and a filter is supplied, then any relation types that exist for primary objects in the
        info that are listed in the filter, but the relations are not sent in the input, those relations will be
        deleted.
        
        Use cases:
        The user wishes to relate two objects in Teamcenter. The user specifies the primary and secondary objects, the
        type of relation to be created and any optional data the user wants added to the relation.
        The user wishes to modify the user data on the relationship between two objects. The user specifies the primary
        and secondary objects and the existing relationship. The user also specifies the new user data to be placed on
        the relationship.
        The user wishes to relate two objects in Teamcenter and remove any existing relationships between the objects.
        The user specifies the primary and secondary objects, the type of relation to be created and any optional data
        the user wants added to the relation. The user also sets the 'complete' option to true to delete the existing
        relationships that pass the supplied filter, but does not send those existing relationships in the input.  For
        example, there is an item revision and a dataset related with an IMAN_specification relationship in Teamcenter
        and the user wants to change this to an IMAN_Rendering relationship. The user can specify the item revision and
        the dataset, specify the new relationship is IMAN_Rendering and set the 'complete' flag. With the filter
        specifying the relation type of IMAN_specification and the object type as dataset. This will delete the current
        relationship and create the new one.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelations',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateRelationsResponse,
        )

    @classmethod
    def expandFoldersForCAD(cls, folders: List[Folder], pref: ExpandFolderForCADPref) -> ExpandFoldersForCADResponse:
        """
        The purpose of this service is to provide the contents of a folder that a CAD integration typically needs in
        one service call as opposed to multiple expand calls.
        This service is specifically for Folder expansion and will only return Items, Item Revisions and Folders that
        are contained in the input Folder.
        Other types of objects (Forms, Datasets, etc...) that are contained directly under the input folder will not be
        returned.
        The service will also return the Item Revisions and Datasets for the Items found in the folder and Datasets
        found for the Item Revisions found directly under the folder.
        The Item Revisions returned, are controlled thru an input latestNRevs specifying how many latest revisions
        should be sent to output.
        The Items, Item Revisions and Datasets returned can be filtered thru an input preference of a list of relation
        names and dataset types filter.
        """
        return cls.execute_soa_method(
            method_name='expandFoldersForCAD',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'folders': folders, 'pref': pref},
            response_cls=ExpandFoldersForCADResponse,
        )

    @classmethod
    def expandGRMRelations(cls, objects: List[BusinessObject], pref: ExpandGRMRelationsPref) -> ExpandGRMRelationsResponse:
        """
        Returns the secondary objects related to the input object for the given list of relation names and other side
        object types filter.
        If no relation names or other side objects types are provided in the input, then all related objects will be
        returned.
        In addition, for performance, if an Item is the output of the expansion, then its associated Item Revisions and
        the Datasets for those Item Revisions will be returned.
        Similarly, if an Item Revision is the output of the expansion, then its associated Datasets will be returned.
        However this additional expansion is controlled through the expItemRev flag.
        """
        return cls.execute_soa_method(
            method_name='expandGRMRelations',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects, 'pref': pref},
            response_cls=ExpandGRMRelationsResponse,
        )

    @classmethod
    def expandPrimaryObjects(cls, objects: List[BusinessObject], pref: ExpandPrimaryObjectsPref) -> ExpandPrimaryObjectsResponse:
        """
        Returns the secondary objects related to the input object for the given list of relation names and other side
        object types filter.
        If no relation names or other side objects types are provided in the input, then all related objects will be
        returned.
        In addition, for performance, if an Item is the output of the expansion, then its associated Item Revisions and
        the Datasets for those Item Revisions will be returned.
        Similarly, if an Item Revision is the output of the expansion, then its associated Datasets will be returned.
        However this additional expansion is controlled through the expItemRev flag.
        """
        return cls.execute_soa_method(
            method_name='expandPrimaryObjects',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects, 'pref': pref},
            response_cls=ExpandPrimaryObjectsResponse,
        )

    @classmethod
    def generateAlternateIds(cls, input: List[GenerateAlternateIdsProperties]) -> GenerateAlternateIdsResponse:
        """
        Generate a list of alternate ids. An alternate id is a displayable id for an Item or ItemRevision that is
        controlled by the user via display rules. The client creates Identifiers that contain the various alternate ids
        to be displayed. Each Identifier is controlled by a display rule. When a display rule is active then the
        appropriate alternate id is displayed.
        
        Use cases:
        The client defines several alternate ids for a part. One alternate id is for the manufacturer of the part( this
        would be their part number ), another would be for a customer ( their part number ) and maybe one for a second
        customer ( again, another part number ). This service allows the client to invoke the user exit
        USER_new_alt_id. This exit will be called once for each count specified in the input using the data passed in
        as parameters.
        """
        return cls.execute_soa_method(
            method_name='generateAlternateIds',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GenerateAlternateIdsResponse,
        )

    @classmethod
    def getAllAttrMappings(cls) -> GetAllAttrMappingsResponse:
        """
        Retrieves all CAD attribute mapping definitions. Additionally, if a CadAttributeMappingDefinition object has a
        path that includes a GRM or NR part, the associated PropertyDescriptor and any attached ListOfValues objects
        will be returned.
        
        Exceptions:
        >Service Exception    Thrown if any Teamcenter subsystem errors occur during the retrieval of all attribute
        mappings, finding the dataset type or finding the attribute mapping type.
        """
        return cls.execute_soa_method(
            method_name='getAllAttrMappings',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={},
            response_cls=GetAllAttrMappingsResponse,
        )

    @classmethod
    def getAttrMappingsForDatasetType(cls, info: List[GetAttrMappingsForDatasetTypeCriteria]) -> GetAttrMappingsForDatasetTypeResponse:
        """
        This operation retrieves the CAD attribute mapping definitions for one or more dataset type and item type
        combinations.  If a 'CadAttributeMappingDefinition' object has a path that includes a Generic Relationship
        Manager (GRM) or named reference part, the associated property descriptor and any attached 'ListOfValues' (LOV)
        objects will be returned.
        
        Since this operation returns existing Teamcenter attribute mappings, please reference the Teamcenter help
        section on creating attribute mappings.
        
        
        Use cases:
        User needs to have attribute mappings defined in Teamcenter.
        
        For this operation, the dataset object type is passed as input. The client application uses the list of
        returned attribute mapping definitions to present the CAD attributes to the user that correspond to the correct
        Teamcenter attributes.
        
        
        Exceptions:
        >Service Exception    Thrown if any Teamcenter subsystem errors occur during the retrieval of all attribute
        mappings.
        """
        return cls.execute_soa_method(
            method_name='getAttrMappingsForDatasetType',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info},
            response_cls=GetAttrMappingsForDatasetTypeResponse,
        )

    @classmethod
    def getAvailableTypes(cls, classes: List[str]) -> GetAvailableTypesResponse:
        """
        Finds types implemented by the given input class name.
        
        Use cases:
        User selects File New Item and is presented with a list of creatable item types.
        """
        return cls.execute_soa_method(
            method_name='getAvailableTypes',
            library='Cad',
            service_date='2007_01',
            service_name='DataManagement',
            params={'classes': classes},
            response_cls=GetAvailableTypesResponse,
        )
