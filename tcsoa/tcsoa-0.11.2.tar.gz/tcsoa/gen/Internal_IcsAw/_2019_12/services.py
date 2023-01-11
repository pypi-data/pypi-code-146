from __future__ import annotations

from tcsoa.gen.Internal.IcsAw._2019_12.Classification import FindClassificationInfo3Response
from typing import List
from tcsoa.gen.Internal.IcsAw._2018_05.Classification import SearchCriteria
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class ClassificationService(TcService):

    @classmethod
    def findClassificationInfo3(cls, workspaceObjects: List[WorkspaceObject], searchCriterias: List[SearchCriteria], classificationDataOptions: int) -> FindClassificationInfo3Response:
        """
        Finds classification information based on the input criteria.
        
        A populated list If a list of WorkspaceObject objects are provided ; then this operation finds all the
        classification objects for the given WorkspaceObject.
        In caseIf a given WorkspaceObject is not classified this operation finds and returns standalone classification
        object; which could then be linked to given WorkspaceObject.
        If a given workspace object is not classified and also the system does not contain standalone classification
        object which could be linked to the WorkspaceObject then this operation will return classification hierarchy
        which could be used for browsing and classifying an object in a classification class of interest. (For
        traditional classification system, children of "Classification Root" (ICM) are returned. For next generation
        Classification Standard Taxonomy (CST) system, children of the Default Hierarchy are returned).
        Empty list of WorkspaceObject would be passed in if user wants to search for a class in classification
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
            method_name='findClassificationInfo3',
            library='Internal-IcsAw',
            service_date='2019_12',
            service_name='Classification',
            params={'workspaceObjects': workspaceObjects, 'searchCriterias': searchCriterias, 'classificationDataOptions': classificationDataOptions},
            response_cls=FindClassificationInfo3Response,
        )
