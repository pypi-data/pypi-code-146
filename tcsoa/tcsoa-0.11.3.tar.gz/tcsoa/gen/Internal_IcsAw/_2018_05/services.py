from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from tcsoa.gen.Internal.IcsAw._2018_05.Classification import SaveClassificationObjectsResponse, SearchCriteria, FindClassificationInfoResponse, ClassificationInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def deleteClassificationObjects(cls, classificationObjects: List[BusinessObject]) -> ServiceData:
        """
        Deletes one or more traditional or Classification Standard Taxonomy (CST) classification objects permanently.
        The classified workspace object associated with the classification object will not be deleted. When deleting a
        classification object, additional structures related to this classification object are deleted as well. These
        are the icm0 and Cst0PropertyRecord objects, Cls0ClassifiedBy object, and Ptn0Membership object.
        """
        return cls.execute_soa_method(
            method_name='deleteClassificationObjects',
            library='Internal-IcsAw',
            service_date='2018_05',
            service_name='Classification',
            params={'classificationObjects': classificationObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def findClassificationInfo(cls, workspaceObjects: List[WorkspaceObject], searchCriteria: List[SearchCriteria], classificationDataOptions: int) -> FindClassificationInfoResponse:
        """
        Finds traditional and Classification Standard Taxonomy (CST) classification information based on the input
        criteria.
        
        If a list of WorkspaceObject objects are provided; then this operation finds all the classification objects for
        the given WorkspaceObject.
        If a given WorkspaceObject is not classified this operation finds and returns standalone classification object;
        which could then be linked to given WorkspaceObject.
        If a given workspace object is not classified and also system does not contain standalone classification object
        which could be linked to the WorkspaceObject then this operation will return classification class hierarchy
        (For traditional classification, children of "Classification Root" (ICM). For CST classification, children of
        the Default Hierarchy View) which could be used for browsing and classifying an object in a classification
        class of interest.
        
        If a search criteria is provided; then this operation searches for classification classes in classification
        hierarchy and returns their metadata information like class ID, name, class parents etc. If both
        'searchCriterias' and 'workspaceObjects' are provided, 'workspaceObjects' list is ignored and search criteria
        is used.
        
        Use cases:
        This operation could be used when user needs to find classification objects, for both traditional and
        Classification Standard Taxonomy (CST), based on workspace objects. Each time a WorkspaceObject is classified
        in a classification class a classification object is created. After searching for all the classification
        objects corresponding to a WorkspaceObject, user can find more information about the classification(s) of a
        WorkspaceObject. 
        The operation 'findClassificationInfo' can be used to get detailed information about the classification
        objects, classification classes where these classification objects belong. After getting information about
        classification objects the user can choose to modify or delete the objects by using operation:
        'saveClassificationObjects' or 'deleteClassificationObjects', both of which support traditional and
        Classification Standard Taxonomy (CST) classes.
        
        The operation 'findClassificationInfo' can also be used when a user wants to search for classes in
        classification hierarchy by using any of class' properties. After searching for classification classes; the
        user can use that information to browse through a subset of classification hierarchy and classify a
        classifiable workspace object in a classification class of interest.
        """
        return cls.execute_soa_method(
            method_name='findClassificationInfo',
            library='Internal-IcsAw',
            service_date='2018_05',
            service_name='Classification',
            params={'workspaceObjects': workspaceObjects, 'searchCriteria': searchCriteria, 'classificationDataOptions': classificationDataOptions},
            response_cls=FindClassificationInfoResponse,
        )

    @classmethod
    def saveClassificationObjects(cls, classificationObjects: List[ClassificationInfo], deltaUpdateFlag: int) -> SaveClassificationObjectsResponse:
        """
        Creates or updates one or more classification objects and (optionally) attach them to a WorkspaceObject object,
        thus classifying it. When the Classification objects are not associated with any WorkspaceObject they act as
        standalone classification objects. A classification object is also called an ICO object. This supports
        traditional ICO, next generation Cls0Object, and Classification Standard Taxonomy (CST) Cls0CstObject.
        Additionally, this operation can perform a delta update for Cls0CstObject object.
        
        Use cases:
        User wants to classify a workspace object or create a standalone classification object (ICO) or update an
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
            method_name='saveClassificationObjects',
            library='Internal-IcsAw',
            service_date='2018_05',
            service_name='Classification',
            params={'classificationObjects': classificationObjects, 'deltaUpdateFlag': deltaUpdateFlag},
            response_cls=SaveClassificationObjectsResponse,
        )
