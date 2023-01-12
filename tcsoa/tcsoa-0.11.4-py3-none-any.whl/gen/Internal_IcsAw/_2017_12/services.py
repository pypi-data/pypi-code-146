from __future__ import annotations

from tcsoa.gen.Internal.IcsAw._2017_12.Author import ClassSearchCriteria, FindClassificationsResponse
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class AuthorService(TcService):

    @classmethod
    def findClassifications(cls, workspaceObjects: List[WorkspaceObject], searchCriterias: List[ClassSearchCriteria], classificationDataOptions: int) -> FindClassificationsResponse:
        """
        Finds classification information based on the input criteria.
        
        If a list of workspace objects are provided; then this operation finds out all the classification objects for
        the given workspace object.
        If a given workspace object is not classified; this operation finds and returns standalone classification
        object; which could then be linked to given workspace object.
        If a given workspace object is not classified and also system does not contain standalone classification object
        which could be linked to the workspace object; then this operation will return classification class hierarchy
        (children of "Classification Root" (ICM)) which could be used for browsing and classifying an object in a
        classification class of interest.
        
        If a search criteria is provided; then this operation searches for classification classes in classification
        hierarchy and returns their metadata information like class ID, name, class parents etc. 
        
        Note that this operation returns only the information that is asked through "classificationDataOptions"
        parameter.
        
        Use cases:
        This operation could be used when user needs to find classification objects (ICO) based on workspace objects.
        Each time a workspace object is classified in a classification class a classification object (ICO) object is
        created. After searching for all the classification objects corresponding to a workspace object, user can find
        more information about the classification(s) of a workspace object. The operation findClassification() can be
        used to get detailed information about the classification objects, classification classes where these
        classification objects belong. After getting information about classification objects, the user can also choose
        to modify or delete the object found by this operation using operation createOrUpdateClassificationObjects() or
        deleteClassificationObjects().
        
        The operation findClassification() can be used when user wants to search for classes in classification
        hierarchy by using any of class' properties. After searching for classification classes; the user can use that
        information to browse through a subset of classification hierarchy and classify a classifiable workspace object
        in a classification class of interest.
        """
        return cls.execute_soa_method(
            method_name='findClassifications',
            library='Internal-IcsAw',
            service_date='2017_12',
            service_name='Author',
            params={'workspaceObjects': workspaceObjects, 'searchCriterias': searchCriterias, 'classificationDataOptions': classificationDataOptions},
            response_cls=FindClassificationsResponse,
        )
