from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from tcsoa.gen.Core._2007_01.ManagedRelations import TraceabilityInfoInput, TraceabilityReportOutput, ManagedRelationResponse, ModifyManagedRelationInput, CreateManagedRelationInput
from tcsoa.gen.Core._2007_01.DataManagement import CreateOrUpdateFormsResponse, GetItemFromIdInfo, WhereUsedResponse, GetItemCreationRelatedInfoResponse, FormInfo, GetItemFromIdResponse, MoveToNewFolderResponse, GenerateUIDResponse, NameValueMap, WhereReferencedResponse, SaveAsNewItemInfo, MoveToNewFolderInfo, SaveAsNewItemResponse, GetDatasetCreationRelatedInfoResponse, GetItemFromIdPref
from tcsoa.gen.Core._2007_01.Session import GetTCSessionInfoResponse, ScopedPreferenceNames, MultiPreferencesResponse
from tcsoa.gen.Core._2007_01.FileManagement import TransientFileInfo, GetTransientFileTicketsResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def getTCSessionInfo(cls) -> GetTCSessionInfoResponse:
        """
        This operation gets information about the current user's Teamcenter session. This will return more detail
        session information than the login service operation including User, Group, Role, Site, Volume, Project, and
        WorkContext.
        """
        return cls.execute_soa_method(
            method_name='getTCSessionInfo',
            library='Core',
            service_date='2007_01',
            service_name='Session',
            params={},
            response_cls=GetTCSessionInfoResponse,
        )

    @classmethod
    def setObjectPropertyPolicy(cls, policyName: str) -> bool:
        """
        Sets the current object property policy. The business logic of a service operation determines what business
        objects are returned, while the object property policy determines which properties are returned on each
        business object instance. This allows the client application to determine how much or how little data is
        returned based on how the client application uses those returned business objects. The policy is applied
        uniformly to all service operations. 
        By default, all applications use the Default object property policy, defined on the Teamcenter server
        '$TC_DATA/soa/policies/default.xml. 'It is this policy that is applied to all service operation responses until
        the client application changes the policy. Siemens PLM Software strongly recommends that all applications
        change the policy to one applicable to the client early in the session.
        The object property policy is set to the policy named in the file '$TC_DATA/soa/policies/<policyName>.xml 'The
        reserved policy name "Empty", will enforce a policy that only returns minimum data required for each object
        (UID and type name).The object property policy will stay in affect for this session until changed by another
        call to 'setObjectPRopertyPolicy'.
        
        
        Like any other service operation, this operation cannot be called before establishing a session with the
        'login' serivce operation, so if you need a policy other than the Default policy for the business objects
        returned by the 'login' operation, use the _2011_06 version of the 'login/loginSso' operation to authenticate
        and establish a session without returning business objects. The 'setObjectPropertyPolicy' operation can then be
        called to establish the policy for the session.
        
        Exceptions:
        >If the named policy does not exist or there are errors parsing the XML file (error code 214104).
        """
        return cls.execute_soa_method(
            method_name='setObjectPropertyPolicy',
            library='Core',
            service_date='2007_01',
            service_name='Session',
            params={'policyName': policyName},
            response_cls=bool,
        )

    @classmethod
    def getPreferences(cls, requestedPrefs: List[ScopedPreferenceNames]) -> MultiPreferencesResponse:
        """
        Get preference values
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='getPreferences',
            library='Core',
            service_date='2007_01',
            service_name='Session',
            params={'requestedPrefs': requestedPrefs},
            response_cls=MultiPreferencesResponse,
        )


class ManagedRelationsService(TcService):

    @classmethod
    def getTraceReport(cls, input: TraceabilityInfoInput) -> TraceabilityReportOutput:
        """
        This operation will create traceability report for the selected TC object.
        """
        return cls.execute_soa_method(
            method_name='getTraceReport',
            library='Core',
            service_date='2007_01',
            service_name='ManagedRelations',
            params={'input': input},
            response_cls=TraceabilityReportOutput,
        )

    @classmethod
    def modifyRelation(cls, newInput: List[ModifyManagedRelationInput]) -> ManagedRelationResponse:
        """
        This operation will Edit the managed relation
        """
        return cls.execute_soa_method(
            method_name='modifyRelation',
            library='Core',
            service_date='2007_01',
            service_name='ManagedRelations',
            params={'newInput': newInput},
            response_cls=ManagedRelationResponse,
        )

    @classmethod
    def createRelation(cls, relationinfo: List[CreateManagedRelationInput]) -> ManagedRelationResponse:
        """
        This operation will create new managed relation
        """
        return cls.execute_soa_method(
            method_name='createRelation',
            library='Core',
            service_date='2007_01',
            service_name='ManagedRelations',
            params={'relationinfo': relationinfo},
            response_cls=ManagedRelationResponse,
        )


class FileManagementService(TcService):

    @classmethod
    def getTransientFileTicketsForUpload(cls, transientFileInfos: List[TransientFileInfo]) -> GetTransientFileTicketsResponse:
        """
        This operation gets the tickets for the desired files to be uploaded to the transient volume. These tickets can
        be used to upload corresponding files via 'FileManagementUtility::putFileViaTicket'. The 'TransientFileInfo'
        contains the basic information for a file to be uploaded such as file name, file type and whether the file
        should be deleted after reading.
        
        Use cases:
        This operation supports the uploading of files into the FMS transient volume.
        """
        return cls.execute_soa_method(
            method_name='getTransientFileTicketsForUpload',
            library='Core',
            service_date='2007_01',
            service_name='FileManagement',
            params={'transientFileInfos': transientFileInfos},
            response_cls=GetTransientFileTicketsResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def moveToNewFolder(cls, moveToNewFolderInfos: List[MoveToNewFolderInfo]) -> MoveToNewFolderResponse:
        """
        The 'moveToNewFolder' operation moves a set of objects from one folder to another. This operation allows for
        moving multiple sets of objects to and from different folders. If no old folder is specified, this operation
        adds the objects to the new folder.
        
        
        Use cases:
        - The user selects an object or group of objects and specifies the folder for the objects to be copied into.
        - The user selects an object or group of objects, removes them from a specified folder and specifies the folder
        for the objects to be copied into.
        
        """
        return cls.execute_soa_method(
            method_name='moveToNewFolder',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'moveToNewFolderInfos': moveToNewFolderInfos},
            response_cls=MoveToNewFolderResponse,
        )

    @classmethod
    def refreshObjects(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation is used to reload the in-memory representation of the objects from the database. Any references
        to the object will still be valid. Any in-memory changes to the original object will be lost. If the object has
        been changed in the database since it was last loaded, then those changes will not be present in memory. The
        operation updates the in memory representation to reflect database changes and does not obtain write lock on
        any objects.
        
        Use cases:
        Use this operation to reload the in-memory representation of one or more objects from the Teamcenter database.
        """
        return cls.execute_soa_method(
            method_name='refreshObjects',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def saveAsNewItem(cls, info: List[SaveAsNewItemInfo]) -> SaveAsNewItemResponse:
        """
        This operation creates a new Item object and ItemRevision object from an existing ItemRevision object.  The
        master form properties may be supplied for the new ItemRevision and item master form objects.  If master form
        data is not supplied the master forms will be initialized from the master forms attached to the existing
        ItemRevision.  Deep Copy rules may also be supplied to override the default Deep Copy rules.
        """
        return cls.execute_soa_method(
            method_name='saveAsNewItem',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info},
            response_cls=SaveAsNewItemResponse,
        )

    @classmethod
    def setProperties(cls, objects: List[BusinessObject], attributes: NameValueMap) -> ServiceData:
        """
        This operation is to support updating list of objects with the given property names and values. All the objects
        updated with same set of property and values data.  Also see  Teamcenter::Soa::Core::2010_09::setProperties
        operation.
        Note: Objects are saved as a part of this operation itself.
        """
        return cls.execute_soa_method(
            method_name='setProperties',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects, 'attributes': attributes},
            response_cls=ServiceData,
        )

    @classmethod
    def whereReferenced(cls, objects: List[WorkspaceObject], numLevels: int) -> WhereReferencedResponse:
        """
        This operation finds the objects and relations that reference a given object.  It returns objects where the
        input object is specified in a Reference property on that object.  It also returns relations where the input
        object is listed as the secondary object for that relation.  It does not return relations where the input
        object is the primary object for that relation. The Datamanagement service operation
        expandGRMRelationsForPrimary can be used to return the relations where the input object is the primary object
        and the objects which are the secondary object for the relation.
        
        Use cases:
        User selects an object, specifies the number of levels (or all) of referencers to return and executes a where
        referenced query.
        
        For example, the user selects a Dataset which has a specification relation to an Item and is contained in the
        users Home folder. The Item is contained in the user Newstuff folder and in the view folder of another Item
        Revision. If the user selects level 2, the Item and Home folder would be returned at level 1 and the Newstuff
        folder and view folder of the other ItemRevision would be returned at level 2.
        """
        return cls.execute_soa_method(
            method_name='whereReferenced',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects, 'numLevels': numLevels},
            response_cls=WhereReferencedResponse,
        )

    @classmethod
    def whereUsed(cls, objects: List[BusinessObject], numLevels: int, whereUsedPrecise: bool, rule: BusinessObject) -> WhereUsedResponse:
        """
        The 'whereUsed' service identifies all the parent Item and ItemRevision objects in the structure where the
        input Item or ItemRevision is used. User can provide RevisionRule to search for specific ItemRevision. By
        default all ItemRevision objects are returned. The number of levels of 'whereUsed' search indicates, whether to
        return one or top or all levels of assemblies. It supports search on Item, ItemRevision  and Dataset.
        
        Use cases:
        A user performs 'whereUsed' search to find all the assemblies that contain a particular Item or ItemRevision.
        User inputs Item or ItemRevision and the search can be made with following options:
        - RevisionRule This can be set to All, displaying all ItemRevision objects  that have an occurrence of target
        ItemRevision. If a specific RevisionRule is selected only the ItemRevision objects  configured by the rule are
        returned in the search.
        - Depth up to which numbers of levels are to be returned.
        
        
        
        The output contains list of  each parent level search result in the structure.
        """
        return cls.execute_soa_method(
            method_name='whereUsed',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'objects': objects, 'numLevels': numLevels, 'whereUsedPrecise': whereUsedPrecise, 'rule': rule},
            response_cls=WhereUsedResponse,
        )

    @classmethod
    def createOrUpdateForms(cls, info: List[FormInfo]) -> CreateOrUpdateFormsResponse:
        """
        This operation creates Form objects or update existing Form objects using the info provided. A new Form will be
        associated to the container object with specified relation type. The properties of the existing Form will be
        updated.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateForms',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'info': info},
            response_cls=CreateOrUpdateFormsResponse,
        )

    @classmethod
    def generateUID(cls, nUID: int) -> GenerateUIDResponse:
        """
        This function returns a number of Teamcenter UIDs generated from the Teamcenter server. This operation can be
        used for assigning unique identifiers to objects that will not be stored in Teamcenter or for objects which
        have yet to be created in Teamcenter.
        
        The 'createObjects' and 'createOrUpdateParts' operations will support input of a preallocated UID for use
        during creation. Please see those operation descriptions for further details.
        
        
        Use cases:
        The integration create workflow requires data to be precreated and stored outside of Teamcenter and then used
        during the Teamcenter create process. For example, generating a UID for an ItemRevision object and then storing
        that UID in the CAD integration data file. The UID is then used as input to the create SOA operation and that
        UID is assigned to the created object.
        """
        return cls.execute_soa_method(
            method_name='generateUID',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'nUID': nUID},
            response_cls=GenerateUIDResponse,
        )

    @classmethod
    def getDatasetCreationRelatedInfo(cls, typeName: str, parentObject: BusinessObject) -> GetDatasetCreationRelatedInfoResponse:
        """
        This operation pre-populates Dataset creation information, default new Dataset name and Tool names, for a
        specified Dataset type.  This operation is used to get all the information associates with the specified
        Dataset prior to the creation operation. The returned default new Dataset name may be determined by the parent
        container object.
        """
        return cls.execute_soa_method(
            method_name='getDatasetCreationRelatedInfo',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'typeName': typeName, 'parentObject': parentObject},
            response_cls=GetDatasetCreationRelatedInfoResponse,
        )

    @classmethod
    def getItemCreationRelatedInfo(cls, typeName: str, parentObject: BusinessObject) -> GetItemCreationRelatedInfoResponse:
        """
        This operation will return naming rules, property rule, form property descriptor, unit of measurement and
        ItemRevision type name based on Item type selected by user during Item creation.
        """
        return cls.execute_soa_method(
            method_name='getItemCreationRelatedInfo',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'typeName': typeName, 'parentObject': parentObject},
            response_cls=GetItemCreationRelatedInfoResponse,
        )

    @classmethod
    def getItemFromId(cls, infos: List[GetItemFromIdInfo], nRev: int, pref: GetItemFromIdPref) -> GetItemFromIdResponse:
        """
        This operation returns Items, Item Revisions, and Dataset based on the input item id. Input is a list of
        GetItemFromIdInfo structures each of which contain an item id (GetItemFromIdInfo.itemId) and optionally a list
        of revision ids (GetItemFromIdInfo.revIds) which specify which Item Revisions to retrieve.  Also input is and
        integer value (nRev) which can also be used to help specify which Item Revisions to return with the Item.  The
        final input is a GetItemFromIdPref structure which contains a list of RelationFilter structures
        (GetItemFromIdPref.prefs) each of which contain a relation type name (RelationFilter.relationTypeName) and a
        list of object type names (RelationFilter.objectTypeNames). This filter can be used to specify which Datasets
        are returned.  The relation type name specifies the relation that relates the Item Revision to the Dataset. 
        The object type name is the type of Dataset to return.  For example, if relationTypeName is "IMAN_reference"
        and the object type name is "Text" then only those Datasets of type "Text" that are related to candidate Item
        Revisions with the "IMAN_reference" relation will be returned.  Supplying no value or an empty value for the
        rev id list and 0 for nRevs will signify the return of no Item Revisions, and thus no Datasets will be returned
        either.  Supplying no value or an empty value for the rev id list and a negative value for nRevs will signify
        the return of all Item Revisions.   Supplying no value or an empty value for the rev id list and a positive
        value for nRev will signify the return of the latest number of Item Revisions specified by the integer--if the
        number of actual revisions found is greater than the input nRev, all revisions for the found Item will be
        returned. Supplying a rev id list will only return those revisions, and the nRev value will not be processed.
        For example, if the input rev Id is "A" and the nRev value is 0, only revision "A" will be returned. If the rev
        id list is empty and nRevs = 5, then the 5 latest Item Revisions will be returned. If no preference filter is
        specified, all Datasets will be returned.  The return is a GetItemFromIdResponse which contains a list of
        GetItemFromIdItemOutput (GetItemFromIdResponse.output and a ServiceData (GetItemFromIdResponse.serviceData). 
        Each GetItemFromIdItemOutput contains an Item (GetItemFromIdItemOutput.item) and a list of
        GetItemFromIdItemRevOutput structures (GetItemFromIdItemOutput.itemRevOutput).  Each GetItemFromIdItemRevOutput
        structure contains an Item Revision (GetItemFromIdItemRevOutput.itemRevision) and a list of found Datasets
        (GetItemFromIdItemRevOutput.datasets).
        """
        return cls.execute_soa_method(
            method_name='getItemFromId',
            library='Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'infos': infos, 'nRev': nRev, 'pref': pref},
            response_cls=GetItemFromIdResponse,
        )
