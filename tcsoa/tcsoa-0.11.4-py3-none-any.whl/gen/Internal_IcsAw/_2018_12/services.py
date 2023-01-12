from __future__ import annotations

from tcsoa.gen.Internal.IcsAw._2018_12.Classification import ClassificationObjectInfo2, FindClassificationInfo2Response, SaveClassificationObjects2Response
from typing import List
from tcsoa.gen.Internal.IcsAw._2018_05.Classification import SearchCriteria
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class ClassificationService(TcService):

    @classmethod
    def findClassificationInfo2(cls, workspaceObjects: List[WorkspaceObject], searchCriterias: List[SearchCriteria], classificationDataOptions: int) -> FindClassificationInfo2Response:
        """
        Finds classification information based on the input criteria.
        
        A populated list If a list of WorkspaceObject objects are provided  ; then this operation finds all the
        classification objects for the given WorkspaceObject.
        In caseIf a given WorkspaceObject is not classified this operation finds and returns standalone classification
        object; which could then be linked to given WorkspaceObject.
        If a given workspace object is not classified and also the system does not contain standalone classification
        object which could be linked to the WorkspaceObject then this operation will return classification hierarchy
        which could be used for browsing and classifying an object in a classification class of interest. (For
        traditional classification system, children of "Classification Root" (ICM) are returned. For next generation
        Classification Standard Taxonomy (CST) system, children of the Default Hierarchy are returned).
        Empty list of  WorkspaceObject would be passed in if user wants to search for a class in classification
        hierarchy using search criteria.
        This operations takes care of returning classification node information from next generation classification
        system including, containing cardinal and polymorphic blocks.
        
        If a search criteria is provided; then this operation searches for classification classes in classification
        hierarchy and returns their metadata information like class ID, name, class parents etc. If both
        searchCriterias and workspaceObjects are provided, workspaceObjects list is ignored and search criteria is used.
        
        Use cases:
        This operation could be used when user needs to find classification objects, for both traditional and
        Classification Standard Taxonomy (CST), based on workspace objects. Each time a WorkspaceObject is classified
        in a classification class a classification object is created. After searching for all the classification
        objects corresponding to a WorkspaceObject, user can find more information about the classification(s) of a
        WorkspaceObject. 
        The operation findClassificationInfo2 can be used to get detailed information about the classification objects,
        classification classes where these classification objects belong. After getting information about
        classification objects the user can choose to modify or delete the objects by using operation:
        saveClassificationObjects2 or deleteClassificationObjects, both of which support traditional and Classification
        Standard Taxonomy (CST) classes.
        
        The operation findClassificationInfo2 can also be used when a user wants to search for classes in
        classification hierarchy by using any of class' properties. After searching for classification classes; the
        user can use that information to browse through a subset of classification hierarchy and classify a
        classifiable workspace object in a classification class of interest.
        """
        return cls.execute_soa_method(
            method_name='findClassificationInfo2',
            library='Internal-IcsAw',
            service_date='2018_12',
            service_name='Classification',
            params={'workspaceObjects': workspaceObjects, 'searchCriterias': searchCriterias, 'classificationDataOptions': classificationDataOptions},
            response_cls=FindClassificationInfo2Response,
        )

    @classmethod
    def saveClassificationObjects2(cls, classificationObjects: List[ClassificationObjectInfo2]) -> SaveClassificationObjects2Response:
        """
        Creates or updates one or more classification objects and (optionally) attach them to a WorkspaceObject object,
        thus classifying it. When the Classification objects are not associated with any WorkspaceObject they act as
        standalone classification objects. A classification object is also called an ICO object. This supports
        traditional icm0, next generation Cls0Object, and Classification Standard Taxonomy (CST) Cls0CstObject.
        This operation can also be used to create or update classification objects in next generation classification
        hierarchy containing cardinal and polymorphic blocks.
        
        Use cases:
        User wants to classify a WorkspaceObject or create a standalone classification object (ICO) or update an
        existing classification object in Active Workspace, in either a traditional or Classification Standard Taxonomy
        (CST) class. Additionally, the user could be performing a delta update on a CST Property Record. This operation
        can be combined with other operations like createItems() to create workspace object and then associate the
        workspace object to the classification object. Before creating a classification object, a classification class
        hierarchy should already be created by the classification admin user in Teamcenter. This hierarchy should
        include a storage class (a class that allows instances to be created and associated to it) for which the
        classification objects need to be created. Values of any attributes associated with classification objects can
        also be populated.
        """
        return cls.execute_soa_method(
            method_name='saveClassificationObjects2',
            library='Internal-IcsAw',
            service_date='2018_12',
            service_name='Classification',
            params={'classificationObjects': classificationObjects},
            response_cls=SaveClassificationObjects2Response,
        )
