from __future__ import annotations

from tcsoa.gen.Core._2007_06.LOV import AttachedLOVsResponse, LOVInfo
from tcsoa.gen.Core._2007_06.PropDescriptor import PropDescInfo, AttachedPropDescsResponse
from tcsoa.gen.Core._2007_06.DataManagement import WhereReferencedByRelationNameResponse, ExpandGRMRelationsResponse, DatasetTypeInfoResponse, SetOrRemoveImmunityInfo, ExpandGRMRelationsPref, ValidateIdsInfo, PurgeSequencesInfo, GetAvailableTypesResponse, BaseClassInput, ValidateItemIdsAndRevIdsResponse, WhereReferencedByRelationNameInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def purgeSequences(cls, objects: List[PurgeSequencesInfo]) -> ServiceData:
        """
        Given a list of ItemRevision sequences, this opertion is used ot perform per the following criteria: 
        - If the input object is the latest sequence of an ItemRevision, all previous sequences will be purged. 
        - If the input object is not the latest sequence of the ItemRevision and the 'validateLatestFlag' is false, the
        input object will be purged.
        - If the input object is not the latest sequence of the ItemRevision and the 'validateLatestFlag' is true, the
        'ServiceData' will be updated with an error.
        
        """
        return cls.execute_soa_method(
            method_name='purgeSequences',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def setOrRemoveImmunity(cls, objects: List[SetOrRemoveImmunityInfo]) -> ServiceData:
        """
        This operation is used to add or remove immunity for each object in the input list according to the value of
        the associated 'setOrRemoveFlag'.  A value of true indicates to apply immunity to the object.  A value of false
        indicates that immunity should be removed from the object.
        """
        return cls.execute_soa_method(
            method_name='setOrRemoveImmunity',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def validateItemIdsAndRevIds(cls, infos: List[ValidateIdsInfo]) -> ValidateItemIdsAndRevIdsResponse:
        """
        Validates the item ID and revision ID based on the naming rules and user exit callbacks.
        """
        return cls.execute_soa_method(
            method_name='validateItemIdsAndRevIds',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'infos': infos},
            response_cls=ValidateItemIdsAndRevIdsResponse,
        )

    @classmethod
    def whereReferencedByRelationName(cls, inputs: List[WhereReferencedByRelationNameInfo], numLevels: int) -> WhereReferencedByRelationNameResponse:
        """
        Finds the objects that reference a given object by a specific relation. The input object will be the secondary
        object for that relation.  It does not return relations where the given input object is the primary object for
        the relation.  The Datamanagement service operation expandGRMRelationsForPrimary can be used to return the
        relations where the input object is the primary object and the objects which are the secondary object for the
        relation
        
        Use cases:
        Use case 1: Use this operation to find the objects referencing the input object by a specific relation.
        Use case 2: Use this operation to find objects of a specific type that reference the input object by a specific
        relation.
        Use case 3: Use this operation to find objects of a specific type referencing the input object.
        """
        return cls.execute_soa_method(
            method_name='whereReferencedByRelationName',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'inputs': inputs, 'numLevels': numLevels},
            response_cls=WhereReferencedByRelationNameResponse,
        )

    @classmethod
    def expandGRMRelationsForPrimary(cls, primaryObjects: List[BusinessObject], pref: ExpandGRMRelationsPref) -> ExpandGRMRelationsResponse:
        """
        Returns the secondary objects related to the input object for the given list of properties / relations and
        other side object types.  If no properties/relations or other side objects types are input, then all related
        objects will be returned.  In addition, for performance, if an Item is the output of the expansion, then its
        associated Item Revisions and the Datasets for those Item Revisions will be returned.  Similarly, if an Item
        Revision is the output of the expansion, then its associated Datasets will be returned.
        """
        return cls.execute_soa_method(
            method_name='expandGRMRelationsForPrimary',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'primaryObjects': primaryObjects, 'pref': pref},
            response_cls=ExpandGRMRelationsResponse,
        )

    @classmethod
    def expandGRMRelationsForSecondary(cls, secondaryObjects: List[BusinessObject], pref: ExpandGRMRelationsPref) -> ExpandGRMRelationsResponse:
        """
        Returns the primary objects related to the input object for the given list of properties / relations and other
        side object types.  If no properties/relations or other side objects types are input, then all related objects
        will be returned.  In addition, for performance, if an Item is the output of the expansion, then its associated
        Item Revisions and the Datasets for those Item Revisions will be returned.  Similarly, if an Item Revision is
        the output of the expansion, then its associated Datasets will be returned.
        """
        return cls.execute_soa_method(
            method_name='expandGRMRelationsForSecondary',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'secondaryObjects': secondaryObjects, 'pref': pref},
            response_cls=ExpandGRMRelationsResponse,
        )

    @classmethod
    def getAvailableTypes(cls, classes: List[BaseClassInput]) -> GetAvailableTypesResponse:
        """
        This will return type names implemented by the given classes. This is lightweight way to get all displayable
        types by name rather than model object.
        """
        return cls.execute_soa_method(
            method_name='getAvailableTypes',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'classes': classes},
            response_cls=GetAvailableTypesResponse,
        )

    @classmethod
    def getDatasetTypeInfo(cls, datasetTypeNames: List[str]) -> DatasetTypeInfoResponse:
        """
        This operation returns the named reference information for a set of dataset types.  Named references are
        Teamcenter objects that relate to a specific data file.
        
        Any failure that occurs during this operation is returned in the 'ServiceData' list of partial errors with the
        dataset type name string mapped to error message.
        
        
        Use cases:
        User wants to see which file type is allowed for attaching to a dataset.
        
        For this operation, the dataset type name is passed in the 'datasetTypeNames' input and the named reference
        information is returned.  The file extension, 'fileExtension', is returned in 'ReferenceInfo' and can be used
        to determine the supported file type for the dataset.
        """
        return cls.execute_soa_method(
            method_name='getDatasetTypeInfo',
            library='Core',
            service_date='2007_06',
            service_name='DataManagement',
            params={'datasetTypeNames': datasetTypeNames},
            response_cls=DatasetTypeInfoResponse,
        )


class SessionService(TcService):

    @classmethod
    def refreshPOMCachePerRequest(cls, refresh: bool) -> bool:
        """
        By Default the service operations will retrieve property value data straight from the POM. When 'refresh' is
        set to true, a refresh will be done on business objects before getting any property data. This will update the
        POM with fresh data from the database. The refresh is only applied to business objects that are actually being
        returned by a service operation. This applies only to database objects, and is not applied to runtime objects. 
        This is applied to all subsequent service requests from the same client. If multiple clients are sharing the
        same Teamcenter server session the refresh POM state is applied per client. Setting this to true will have a
        performance impact but will grantee all property values returned are up-to-date.
        """
        return cls.execute_soa_method(
            method_name='refreshPOMCachePerRequest',
            library='Core',
            service_date='2007_06',
            service_name='Session',
            params={'refresh': refresh},
            response_cls=bool,
        )


class LOVService(TcService):

    @classmethod
    def getAttachedLOVs(cls, inputs: List[LOVInfo]) -> AttachedLOVsResponse:
        """
        Get attached LOV based on input type name and property names structure. The LOV Tag is returned in the response
        and service data.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='getAttachedLOVs',
            library='Core',
            service_date='2007_06',
            service_name='LOV',
            params={'inputs': inputs},
            response_cls=AttachedLOVsResponse,
        )


class PropDescriptorService(TcService):

    @classmethod
    def getAttachedPropDescs(cls, inputs: List[PropDescInfo]) -> AttachedPropDescsResponse:
        """
        Get the attached property descriptor based on input type name and property names structure.
        """
        return cls.execute_soa_method(
            method_name='getAttachedPropDescs',
            library='Core',
            service_date='2007_06',
            service_name='PropDescriptor',
            params={'inputs': inputs},
            response_cls=AttachedPropDescsResponse,
        )
