from __future__ import annotations

from tcsoa.gen.Cad._2008_06.StructureManagement import AbsOccDataPref, CreateOrUpdateAbsoluteStructurePref3, CreateOrUpdateAbsoluteStructureInfo3, AbsOccQualifierInfo, ExpandPSAllLevelsResponse2, ReconfigureBOMWindowsInfo, ExpandPSAllLevelsPref, CreateVariantRulesInfo, CreateOrUpdateAbsoluteStructureResponse2, CreateVariantRulesResponse, ExpandPSOneLevelPref, ExpandPSOneLevelResponse2, DeleteRelativeStructureInfo3, ReconfigureBOMWindowsResponse, SaveBOMWindowsResponse, CreateOrUpdateRelativeStructureInfo3, ExpandPSOneLevelInfo, ExpandPSAllLevelsInfo, GetAbsoluteStructureDataResponse, CreateOrUpdateRelativeStructurePref3
from tcsoa.gen.BusinessObjects import BOMWindow, Folder
from tcsoa.gen.Cad._2007_12.DataManagement import CreateOrUpdatePartsPref
from tcsoa.gen.Cad._2008_06.DataManagement import CreateOrUpdatePartsResponse, PartInfo, ExpandFoldersForCADResponse2, ExpandFolderForCADPref2
from tcsoa.gen.Cad._2007_01.StructureManagement import CreateOrUpdateRelativeStructureResponse, DeleteRelativeStructureResponse
from tcsoa.gen.Cad._2007_12.StructureManagement import DeleteRelativeStructurePref2
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def reconfigureBOMWindows(cls, info: List[ReconfigureBOMWindowsInfo]) -> ReconfigureBOMWindowsResponse:
        """
        This operation takes a list of BOMWindow objects and updates the contents of the windows (i.e. configuration)
        by applying the supplied RevisionRule and variant configuration information.  If the
        'RevisionRuleEntryProps'::'unitNo' is set to -1 then it considers default unitNo or use the input RevisionRule
        object with no changes. If no value specified for 'RevisionRuleEntryProps'::'unitNo', then the input
        RevisionRule object used as modified/transient rule with unitNo as 0. If the value of preference
        PSM_enable_product_configurator is set to true, then Product Configurator variant rule will be honored.
        
        Use cases:
        This operation is used to reconfigure the BOMWindow with new or modified RevisionRule and VariantRule
        information.
        """
        return cls.execute_soa_method(
            method_name='reconfigureBOMWindows',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=ReconfigureBOMWindowsResponse,
        )

    @classmethod
    def saveBOMWindows(cls, bomWindows: List[BOMWindow]) -> SaveBOMWindowsResponse:
        """
        This operation can be used by a client developer to save any modifications made to a Teamcenter product
        structure through its runtime artifacts. A Teamcenter product structure is a persistent parent child
        composition and clients often deal with runtime artifacts of this persistent model. The runtime artifacts are
        primarily represented by BOMLine business objects and BOMWindow business objects along with the BOMLine
        properties. Modifications to the product structure are typically bulked up on the client and tracked through
        the BOMWindow. Once it is established that changes to a product structure can be saved this operation can be
        called passing in a handle to the BOMWindows that need to be saved.
        
        Use cases:
        In a typical usage of the saveBOMWindows operation, a client developer already has a Teamcenter product
        structure loaded with the runtime artifacts created. This means that the client developer has/creates handles
        to a BOMWindow, and BOMLine business objects that are part of that BOMWindow. Given this pre disposition,
        typical interaction with the client may involve addition of a new BOMLine or removal of a BOMLine,
        creation/removal of In Structure associations etc. In such cases, the changes to the product structure are
        tracked on the BOMWindow and when the changes are ready to be persisted, the client developer calls the
        saveBOMWindows operation.
        """
        return cls.execute_soa_method(
            method_name='saveBOMWindows',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'bomWindows': bomWindows},
            response_cls=SaveBOMWindowsResponse,
        )

    @classmethod
    def createOrUpdateAbsoluteStructure(cls, absOccInfos: List[CreateOrUpdateAbsoluteStructureInfo3], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateAbsoluteStructurePref3) -> CreateOrUpdateAbsoluteStructureResponse2:
        """
        This operation creates or updates absolute occurrences on an existing relative structure.  The structure will
        be configured with revision rule set in the preference TC_config_rule_name before any configuration changes are
        applied. The objects created or updated can include an absolute occurrence, assembly arrangement and datasets
        and are added to the ServiceData as created or updated objects.  Created forms are added as plain objects and
        updated forms are added as updated objects.
        
        Before creating the absolute occurrence or assembly arrangement, this operation will check whether either
        already exists.  If the occurrence or arrangement exists but the input attribute values differ from those
        already set, an attempt is made to update the values.
        This operation assumes the input is in a bottom up format such that if any failures occur, the structure that
        is updated will still be consumable.  For example:
        
        Parent assembly A and occurrence C are input into this operation along with subassembly B and occurrence D.  If
        occurrence D is updated successfully on subassembly B but an error occurs during the update of occurrence C on
        assembly A, the client can still access subassembly B.
        
        For objects of type dataset and form, this operation can create or update a new object instance and attach it
        as an override on the absolute occurrence.  For all object types, existing objects can be attached or removed
        as an override on the absolute occurrence.
        
        To help reduce the client overhead of sending all override information during a complete synchronization and
        avoid accidental removal of overrides coming from other clients, this operation allows the client to provide
        only the attributes it is interested in syncing when the complete flag is set to true.  For more information on
        complete synchronization, see the description for the complete input parameter.
        
        One parent context object is processed at a time and it is assumed that all edits for a given parent context
        come in as one set of input.
        
        Use cases:
        Use case 1:
        
        User adds an override to an existing assembly to create an absolute occurrence.
        
        For this operation, the assembly is passed in as the 'contextItemRev' and the override, such as new
        transformation data to position a component in an assembly, is passed in as the absolute occurrence.  The
        absolute occurrence is created and a map of the input 'clientID' to AbsOccurrence is returned in 'absOccOutput'
        and the occurrence is returned as created objects in 'ServiceData'.
        
        Use case 2:
        
        User adds an override with a new dataset to an existing assembly to create an absolute occurrence with an
        attached dataset.
        
        For this operation, the assembly is passed in as the 'contextItemRev' and the override with information for the
        new dataset is passed in as the absolute occurrence information.  The absolute occurrence and new dataset are
        created and a map of the input 'clientID' to AbsOccurrence is returned in 'absOccOutput' and the created
        dataset is returned in 'datasetOutput'.  The occurrence and dataset are returned as created objects in
        'ServiceData'.
        
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in 'bomViewTypeName'.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateAbsoluteStructure',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'absOccInfos': absOccInfos, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateAbsoluteStructureResponse2,
        )

    @classmethod
    def createOrUpdateRelativeStructure(cls, inputs: List[CreateOrUpdateRelativeStructureInfo3], bomViewTypeName: str, complete: bool, pref: CreateOrUpdateRelativeStructurePref3) -> CreateOrUpdateRelativeStructureResponse:
        """
        This is the overloaded function for Cad::_2007_12::StructureManagement::createOrUpdateRelativeStructure.
        It differs by allowing the parent member of the structure CreateOrUpdateRelativeStructureInfo to be a
        ModelObject instead of a strongly typed Item Revision object and makes the child member of the
        RelativeStructureChildInfo to a ModelObject instead of strongly typed Item Revision.
        This is to allow structures with GDE elements to be edited with this service.
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
        215033: The input last modified date differs from actual.
        215034: The dataset or BVR was modified even when the input last modified dates was different than the current
        last modified data. 
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelativeStructure',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'complete': complete, 'pref': pref},
            response_cls=CreateOrUpdateRelativeStructureResponse,
        )

    @classmethod
    def createVariantRules(cls, input: List[CreateVariantRulesInfo]) -> CreateVariantRulesResponse:
        """
        This operation creates the saved VariantRule objects for classic variant options.
        
        Use cases:
        This operation is used to create VariantRule object and save them, which can be used later for BOM variant
        configuration.
        """
        return cls.execute_soa_method(
            method_name='createVariantRules',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=CreateVariantRulesResponse,
        )

    @classmethod
    def deleteRelativeStructure(cls, inputs: List[DeleteRelativeStructureInfo3], bomViewTypeName: str, pref: DeleteRelativeStructurePref2) -> DeleteRelativeStructureResponse:
        """
        This operation deletes one or more first level children of a parent assembly.  The children, or occurrences, to
        be deleted are specified by the CAD occurrence ID or PSOccurrenceThread UID.  The last modified date of the BOM
        view revision (BVR) can also be specified for comparison against the last modified date in Teamcenter to ensure
        the occurrence has not changed outside of this client context and control if the BVR is actually modified and
        the occurrence deleted by this operation.
        
        Use cases:
        User deletes an existing relative occurrence from an existing assembly.
        
        For this operation, the assembly is passed in as the parent and the occurrence ID is passed in as the child
        information.  The relative occurrence is removed from the parent assembly and the ID of the deleted occurrence
        is added to the ServiceData list of deleted objects.
        
        Exceptions:
        >Service Exception    Thrown if an invalid BOM view type is specified in 'bomViewTypeName'.
        """
        return cls.execute_soa_method(
            method_name='deleteRelativeStructure',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs, 'bomViewTypeName': bomViewTypeName, 'pref': pref},
            response_cls=DeleteRelativeStructureResponse,
        )

    @classmethod
    def expandPSAllLevels(cls, info: ExpandPSAllLevelsInfo, pref: ExpandPSAllLevelsPref) -> ExpandPSAllLevelsResponse2:
        """
        This is the overloaded function for Cad::_2007_01::StructureManagement::expandPSAllLevels.
        The member itemRevOfBOMLine of ExpandPSData and ExpandPSParentData is renamed as objectOfBOMLine and its type
        is changed from Item Revision to ModelObject.
        Also the datasets and parentDatasets member of ExpandPSData and ExpandPSParentData structures respectively are
        renamed to relatedObjects and type changed to ModelObject instead of Dataset.
        This is to support structures with GDE elements to be returned from the expansion.
        Finds the children at all levels given parent BOMLines.
        Also if required gets the objects of given type and relation that are attached to the parent and children.
        In addition to the above, the expansion of the Product Structure can be filtered for a given occurrence type/s
        which can be included and/or excluded from the expansion.
        In addition to the above the following additional functionality has been added:
        1.  The operation is not limited to return related objects of dataset type only.  Expansion of attached objects
        to the BOM line object is determined by a filtering mechanism where the criteria is set by: relation name,
        related object type, and named references.
        2.  This operation allows for expansion to reference object associated to a named reference.  Typically this is
        a file.  An FMS ticket will be returned to provide access to this file.
        3.  Where a named reference points to a file, this operation allows for specific logic in choosing which files
        are returned.  This is determined by the input parameter NamedRefHandler (included in the info object).
        """
        return cls.execute_soa_method(
            method_name='expandPSAllLevels',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info, 'pref': pref},
            response_cls=ExpandPSAllLevelsResponse2,
        )

    @classmethod
    def expandPSOneLevel(cls, info: ExpandPSOneLevelInfo, pref: ExpandPSOneLevelPref) -> ExpandPSOneLevelResponse2:
        """
        This operation will expand one level of a product structure and return the resulting BOM lines.
        If required, it will return objects of a given relation and type that are attached to the parent and child BOM
        lines.
        Additionally, if specified in the preference, this will return only BOM Lines of a given particular occurrence
        type and exclude occurrence types of a given type.
        This operation differs from the operation Teamcenter.Soa.Cad._2007_01.StructureManagement.expandPSOneLevel in
        the following ways:
        1.  The operation is not limited to return related objects of dataset type only.  Expansion of attached objects
        to the BOM line object is determined by a filtering mechanism where the criteria is set by: relation name,
        related object type, and named references.
        2.  This operation allows for expansion to reference object associated to a named reference.  Typically this is
        a file.  An FMS ticket will be returned to provide access to this file.
        3.  Where a named reference points to a file, this operation allows for specific logic in choosing which files
        are returned.  This is determined by the input parameter NamedRefHandler (included in the info object).
        4.  The resulting Product Structure expansion can be limited to a certain Occurrence Types.
        """
        return cls.execute_soa_method(
            method_name='expandPSOneLevel',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info, 'pref': pref},
            response_cls=ExpandPSOneLevelResponse2,
        )

    @classmethod
    def getAbsoluteStructureData(cls, absOccDataQualInfos: List[AbsOccQualifierInfo], absOccDataPref: AbsOccDataPref) -> GetAbsoluteStructureDataResponse:
        """
        This operation retrieves the absolute occurrence override information for the given qualifier.
        The input accepts the relation override that needs to be expanded.
        In case of finding the overrides based on the used arrangement within the structure, the client is expected to
        provide bvr of sub assembly in the input.
        ParentBVR |--(Arr1) |--(Arr2) | |________childBVR1 |           |-----(Arr3) |           |-----(Arr4) |         
         |_____________childBVR2 |                                    |----(Arr5) |                                   
        |----(Arr6) |_____ childBVR2 |----(Arr5) |----(Arr6)
        If Arr1 uses Arr3 which in turn uses Arr5, to determine the overrides by Arr3 and Arr5 qualifier the client is
        expected to send childbvr1 and childbvr2 as inputs along with the parentBVR.
        """
        return cls.execute_soa_method(
            method_name='getAbsoluteStructureData',
            library='Cad',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'absOccDataQualInfos': absOccDataQualInfos, 'absOccDataPref': absOccDataPref},
            response_cls=GetAbsoluteStructureDataResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateParts(cls, partInput: List[PartInfo], pref: CreateOrUpdatePartsPref) -> CreateOrUpdatePartsResponse:
        """
        CreateOrUpdateParts allows the user to update or create a set of parts using Items, Item Revisions, and
        Datasets and save the boudingbox information related to these objects.
        The service first attempts to validate the existence of the Item, Item Revision, and Dataset.
        If the Item and Item Revision already exist, but the Dataset does not, then only the Dataset is created.
        If the Dataset exists, a new version will be added to the existing series.
        If any of the objects exist but the input attribute values that differ from those already set, attempts are
        made to update the values if possible.
        If the boundingbox information exists it saves that information on that particular dataset else it willnot save
        the boudingbox information.
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
            service_date='2008_06',
            service_name='DataManagement',
            params={'partInput': partInput, 'pref': pref},
            response_cls=CreateOrUpdatePartsResponse,
        )

    @classmethod
    def expandFoldersForCAD(cls, folders: List[Folder], pref: ExpandFolderForCADPref2) -> ExpandFoldersForCADResponse2:
        """
        The purpose of this service is to provide the contents of a folder that a CAD integration typically needs in
        one service call as opposed to multiple expand calls. This service is specifically for folder expansion and
        will only return items, item revisions and folders that are contained in the input folder. Other types of
        objects ( forms, datasets, etc.. ) that are contained directly under the input folder can be returned if their
        type is specified in the preference. The service will also return the item revisions and datasets for the items
        found in the folder and datasets found for the item revisions found directly under the folder. The item
        revisions returned, are controlled thru an input 'latestNRevs' specifying how many latest revisions should be
        sent to output. The items, item revisions and datasets returned can be filtered thru an input preference of a
        list of relation names and dataset types filter.
        
        Use cases:
        A CAD application needs to know what objects in the database are relative to the cad application. The CAD
        application can get the contents of the home folder and display to the user. If the user then selects a
        subfolder of home then the application can expand that folder to get to the desired data. This service will
        return objects that the cad application understands such as subfolders, items, item revisions and datasets and
        other objects of the type the application specifies in the input filter.
        """
        return cls.execute_soa_method(
            method_name='expandFoldersForCAD',
            library='Cad',
            service_date='2008_06',
            service_name='DataManagement',
            params={'folders': folders, 'pref': pref},
            response_cls=ExpandFoldersForCADResponse2,
        )
