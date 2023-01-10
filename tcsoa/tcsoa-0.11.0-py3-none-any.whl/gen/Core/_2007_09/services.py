from __future__ import annotations

from tcsoa.gen.Core._2007_09.ProjectLevelSecurity import AssignedOrRemovedObjects
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2007_09.DataManagement import ExpandGRMRelationsPref2, RemoveNamedReferenceFromDatasetInfo, ExpandGRMRelationsResponse2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def loadObjects(cls, uids: List[str]) -> ServiceData:
        """
        Load business objects into the client data model for each of the UIDs supplied. The business objects are loaded
        from the Teamcenter server's in memory cache of business objects or from the database. UIDs of runtime business
        objects (BOMLines) that are not currently loaded in the Teamcenter server's memory will result in a partial
        error being returned.
        """
        return cls.execute_soa_method(
            method_name='loadObjects',
            library='Core',
            service_date='2007_09',
            service_name='DataManagement',
            params={'uids': uids},
            response_cls=ServiceData,
        )

    @classmethod
    def removeNamedReferenceFromDataset(cls, inputs: List[RemoveNamedReferenceFromDatasetInfo]) -> ServiceData:
        """
        This operation removes the specified named references from a dataset.
        
        If the 'NamedReferenceInfo.targetObject' input is not specified then all named references of the type specified
        are removed from the dataset.  If the 'NamedReferenceInfo.targetObject' input is specified then only that named
        reference is removed from the dataset.  If the 'NamedReferenceInfo.deleteTarget' input is true then the
        'NamedReferenceInfo.targetObject' will be deleted if it is no longer referenced.
        
        
        Use cases:
        User deletes a single named reference from a dataset that has multiple named references of the same type.
        
        For this operation, the dataset is passed in along with the named reference type and object reference for the
        specific named reference to be removed from the dataset.  The specific named reference is removed from the
        dataset and the dataset is added to the 'ServiceData' list of updated objects.
        """
        return cls.execute_soa_method(
            method_name='removeNamedReferenceFromDataset',
            library='Core',
            service_date='2007_09',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def expandGRMRelationsForPrimary(cls, primaryObjects: List[BusinessObject], pref: ExpandGRMRelationsPref2) -> ExpandGRMRelationsResponse2:
        """
        This operation returns the secondary objects that are related to the input primary objects.  Relation type
        names and secondary object types can be input as a filter to reduce the set of returned secondary objects.  In
        the context of expanding primary objects, secondary objects may be referred to as side objects. If no relation
        type names or secondary object types are input, then all related objects will be returned.
        
        For improved performance, if an item is the output of the expansion, then its associated item revisions and the
        datasets for those item revisions will be returned.  Similarly, if an item revision is the output of the
        expansion, then its associated datasets will be returned.
        
        
        Use cases:
        User wants to see all the secondary objects related to the input primary item object.
        
        For this operation, the item object is input in 'primaryObjects' and the filter preference 'info'
        'relationTypeName' and 'otherSideObjectTypes' parameters are set to be empty.  All secondary objects that have
        a relation to the item are returned in 'ExpandGRMRelationsOutput2'  'relationshipData'.  The primary object,
        secondary objects and relation objects are returned as plain objects in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='expandGRMRelationsForPrimary',
            library='Core',
            service_date='2007_09',
            service_name='DataManagement',
            params={'primaryObjects': primaryObjects, 'pref': pref},
            response_cls=ExpandGRMRelationsResponse2,
        )

    @classmethod
    def expandGRMRelationsForSecondary(cls, secondaryObjects: List[BusinessObject], pref: ExpandGRMRelationsPref2) -> ExpandGRMRelationsResponse2:
        """
        This operation returns the primary objects that are related to the input secondary objects.  Relation type
        names and secondary object types can be input as a filter to reduce the set of returned primary objects.  In
        the context of expanding secondary objects, primary objects may be referred to as side objects.  If no relation
        type names or secondary object types are input, then all related objects will be returned.
        
        For improved performance, if an item is the output of the expansion, then its associated item revisions and the
        datasets for those item revisions will be returned.  Similarly, if an item revision is the output of the
        expansion, then its associated datasets will be returned.
        
        
        Use cases:
        User wants to see all the primary objects related to the input secondary dataset object.
        
        For this operation, the dataset object is input in 'secondaryObjects' and the filter preference info
        'relationTypeName' and 'otherSideObjectTypes' parameters are set to be empty.  All primary objects that have a
        relation to the dataset are returned in 'ExpandGRMRelationsOutput2'  'relationshipData'.  The secondary object,
        primary objects and relation objects are returned as plain objects in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='expandGRMRelationsForSecondary',
            library='Core',
            service_date='2007_09',
            service_name='DataManagement',
            params={'secondaryObjects': secondaryObjects, 'pref': pref},
            response_cls=ExpandGRMRelationsResponse2,
        )


class ProjectLevelSecurityService(TcService):

    @classmethod
    def assignOrRemoveObjects(cls, assignedOrRemovedobjects: List[AssignedOrRemovedObjects]) -> ServiceData:
        """
        This operation assigns the given set of workspace objects to the given projects. Similarly, it removes an
        additional set of given workspace objects from the same set of given projects. If user is not privileged to
        assign objects to any of the given projects then this operation will return the error 101014 : You have
        insufficient privilege to assign object to a project. Similarly, if user is not privileged to remove objects
        from any of the given projects then this operation will return error 101015: You have insufficient privilege to
        remove object from a project.  These errors will not terminate processing of rest of the objects.
        """
        return cls.execute_soa_method(
            method_name='assignOrRemoveObjects',
            library='Core',
            service_date='2007_09',
            service_name='ProjectLevelSecurity',
            params={'assignedOrRemovedobjects': assignedOrRemovedobjects},
            response_cls=ServiceData,
        )
