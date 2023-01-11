from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from tcsoa.gen.Classification._2007_01.Classification import SearchByInstanceIdResponse, GetChildrenResponse, SearchForClassesCriteria, GetClassificationObjectsResponse, GetParentsResponse, SearchForClassesResponse, FindClassifiedObjectsResponse, GetKeyLOVsResponse, CreateClassificationObjectsResponse, GetClassDescriptionsResponse, GetPartFamilyTemplatesResponse, FindClassificationObjectsResponse, ClassificationObject, GetAttributesForClassesResponse, UpdateClassificationObjectsResponse, SearchResponse, GetFileIdCriteria, GetFileIdsResponse, SearchClassAttributes
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def search(cls, searchCriteria: List[SearchClassAttributes]) -> SearchResponse:
        """
        Finds all the classification objects based on classification class IDs, classification attribute ID and an
        expression for classification attribute value. A classification object is also called an ICO.
        
        Use cases:
        User needs to search for classification objects based on the class where they are classified and the value of
        classification attributes.Another related operation for searching classification objects is
        'searchByInstanceID'(), that can search for classification objects based on their IDs
        
        Exceptions:
        >The operation throws a 'ServiceException' in case of an error condition. Clients should  then retrieve the
        errors from the 'ServiceData' list of partial errors in the returned 'SearchResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='search',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'searchCriteria': searchCriteria},
            response_cls=SearchResponse,
        )

    @classmethod
    def searchByInstanceId(cls, instanceIdQueries: List[str]) -> SearchByInstanceIdResponse:
        """
        Finds all the classification objects based on their IDs. A classification object is also called an ICO. If the
        ICO classifies a workspace object, then ICO ID would be same as the workspace object ID
        
        Use cases:
        User wants to search for classification objects based on their IDs. The returned objects can then be used as
        input for operations like 'findClassifiedObjects'(), which is used to search workspace objects associated with
        the ICOs.
        Another related operation for searching classification objects is 'search'(), that can search for
        classification objects based on class ID and attribute values
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='searchByInstanceId',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'instanceIdQueries': instanceIdQueries},
            response_cls=SearchByInstanceIdResponse,
        )

    @classmethod
    def searchForClasses(cls, criteria: List[SearchForClassesCriteria]) -> SearchForClassesResponse:
        """
        Finds the classification classes based on provided search criteria and provides detailed information about
        those classes.  The user can search using a search expression on attributes of the class (Class ID, Name, Type
        etc.)  . For example, the user shall be able to search all the classes whose name begins with a particular set
        of characters and where the class ID matches certain pattern. The order of search results can also be sorted on
        various criteria.
        
        Use cases:
        The user needs to search for classification classes using a search criterion based on various attributes of a
        class. The search criterion can be based on one or more attributes
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='searchForClasses',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'criteria': criteria},
            response_cls=SearchForClassesResponse,
        )

    @classmethod
    def updateClassificationObjects(cls, clsObjs: List[ClassificationObject]) -> UpdateClassificationObjectsResponse:
        """
        Updates existing classification objects. A classification object is also called ICO. Values of various ICO
        attributes can be modified
        
        Use cases:
        User wants to update values of the attributes for an existing classification object in Teamcenter. E.g. user
        wants to modify an integer value of a class attribute ("Length") for an existing ICO. This operation is
        typically used after creating the classification objects using 'createClassificationObjects'().
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='updateClassificationObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'clsObjs': clsObjs},
            response_cls=UpdateClassificationObjectsResponse,
        )

    @classmethod
    def createClassificationObjects(cls, clsObjs: List[ClassificationObject]) -> CreateClassificationObjectsResponse:
        """
        Creates one or more classification objects and (optionally) attach them to a workspace object, thus classifying
        it. When the Classification objects are not associated with any workspace object, they would act as standalone
        Classification objects. A classification object is also called ICO
        
        Use cases:
        User wants to classify a workspace object or create a standalone classification object (ICO) in Teamcenter.
        This operation can be combined with other operations like createItems() to create workspace object and then
        associate the workspace object to the classification object. Before creating a classification object, a
        classification class hierarchy should already be created by the classification admin user in Teamcenter. This
        hierarchy should include a storage class (a class that allows instances to be created and associated to it) for
        which the classification objects need to be created. Values of any attributes associated with classification
        objects can also be populated.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Classification object ID mapped to the error message in the 'ServiceData'
        list of partial errors in the returned 'CreateClassificationObjectsResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='createClassificationObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'clsObjs': clsObjs},
            response_cls=CreateClassificationObjectsResponse,
        )

    @classmethod
    def deleteClassificationObjects(cls, clsObjTags: List[BusinessObject]) -> ServiceData:
        """
        Deletes one or more classification objects permanently. A classification object is also called ICO. The
        classified workspace object associated with the ICO will not be deleted
        
        Use cases:
        User needs to delete classification objects. It is typically called when after creating or searching the
        classification objects, user decides that the returned objects are not needed anymore
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Classification object ID mapped to the error message in the 'ServiceData'
        list of partial errors in the returned 'DeletedClassificationObjectsResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='deleteClassificationObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'clsObjTags': clsObjTags},
            response_cls=ServiceData,
        )

    @classmethod
    def findClassificationObjects(cls, wsoIds: List[WorkspaceObject]) -> FindClassificationObjectsResponse:
        """
        Finds the classification objects associated with input workspace objects (WSO). A classification object is also
        called ICO. Each workspace object can have one or more ICOs associated with it.
        
        Use cases:
        When user need to find classification objects (ICO) based on workspace objects. Each time a workspace object is
        classified in a classification class a classification object (ICO) object is created.  After searching for all
        the classification objects corresponding to a workspace object, user can find more information about the
        classification(s) of a workspace object. The operation 'getClassificationObjects()'' 'can be used to get
        detailed information about the classification objects. After getting information on classification objects,
        user can also choose to modify or delete those using operation 'updateClassificationObjects()' or
        'deleteClassificationObjects()'
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Classification object ID mapped to the error message in the 'ServiceData'
        list of partial errors in the returned 'CreateClassificationObjectsResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='findClassificationObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'wsoIds': wsoIds},
            response_cls=FindClassificationObjectsResponse,
        )

    @classmethod
    def findClassifiedObjects(cls, icoTags: List[BusinessObject]) -> FindClassifiedObjectsResponse:
        """
        Finds the workspace objects (WSO) associated with input Teamcenter classification objects. A classification
        object is also called ICO. Each ICO can have only one workspace object associated with it.
        
        Use cases:
        When user need to find workspace objects based on classification objects (ICO) that were created when workspace
        objects were classified.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Classification object ID mapped to the error message in the 'ServiceData'
        list of partial errors in the returned 'FindClassifiedObjectsResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='findClassifiedObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'icoTags': icoTags},
            response_cls=FindClassifiedObjectsResponse,
        )

    @classmethod
    def getAttributesForClasses(cls, classIds: List[str]) -> GetAttributesForClassesResponse:
        """
        Provides information on class attributes for the classification classes based on input classification class
        ids. Detailed information about class attributes is provided & includes class attribute name, description,
        format, unit system, minimum/maximum value & configuration set
        
        Use cases:
        When user wants to view details of all class attributes associated with a classification class. This operation
        is similar to getAttributesForClasses2(), but provides information in a slightly different format. Typically,
        the information about class attributes is used to determine which classification class a workspace object shall
        be classified into
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.
        In all other cases failures will be returned with the Class ID mapped to the error message in the 'ServiceData'
        list of partial errors of the returned 'GetAttributesForClassesResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='getAttributesForClasses',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'classIds': classIds},
            response_cls=GetAttributesForClassesResponse,
        )

    @classmethod
    def getChildren(cls, groupOrClassIds: List[str]) -> GetChildrenResponse:
        """
        Gets the information about immediate children in classification hierarchy for given group or class
        identifier(s).
        Returns a 'GetChildrenResponse' structure containing:
        - Retrieved child classes in the 'ServiceData' list of plain objects
        - Any failures with Class ID mapped to the error message in the 'ServiceData' list of partial errors.
        
        
        
        Use cases:
        User wants to get details of all groups or classes that lie under a particular group or class in a
        classification class hierarchy.
        
        Returns a 'GetChildrenResponse' structure containing:
        - Retrieved child classes in the 'ServiceData' list of plain objects
        - Any failures with Class ID mapped to the error message in the 'ServiceData' list of partial errors.
        
        
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.
        In all other cases failures will be returned with the Class ID mapped to the error message in the 'ServiceData'
        list of partial errors of the returned 'GetChildrenResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='getChildren',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'groupOrClassIds': groupOrClassIds},
            response_cls=GetChildrenResponse,
        )

    @classmethod
    def getClassDescriptions(cls, classIds: List[str]) -> GetClassDescriptionsResponse:
        """
        Gets detailed information about a classification class based on classification class ID. This information
        includes class type, parent, name, description, unit system and user data associated with the class.  It also
        includes a count of children, number of classification views & number of instances of classification objects
        associated with the classification class. Information can also be obtained on any documents such as images &
        icons attached to the classification class.
        
        Use cases:
        When user need details of classification classes. These details can help user decide whether to classify a
        workspace object in particular classification classes.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getClassDescriptions',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'classIds': classIds},
            response_cls=GetClassDescriptionsResponse,
        )

    @classmethod
    def getClassificationObjects(cls, clsObjTags: List[BusinessObject]) -> GetClassificationObjectsResponse:
        """
        Looks for specified classification objects. If they are found, then detailed information about those objects is
        provided. A classification object is also called ICO
        
        Use cases:
        When user need to find an existing classification object to either view or update its details. It can be
        followed by operations like 'updateClassificationObjects()' or 'deleteClassificationObjects()' to update or
        delete the classification objects. 
        The operation 'findClassificationObjects()' can be used to get the list of classification objects, associated
        with workspace objects. Then, this operation 'getClassificationObjects()' is used to get the detailed
        information on the classification objects.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Classification object ID mapped to the error message in the 'ServiceData'
        list of partial errors in the returned 'GetClassificationObjectsResponse' structure.
        """
        return cls.execute_soa_method(
            method_name='getClassificationObjects',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'clsObjTags': clsObjTags},
            response_cls=GetClassificationObjectsResponse,
        )

    @classmethod
    def getFileIds(cls, criteria: List[GetFileIdCriteria]) -> GetFileIdsResponse:
        """
        Gets the file information from any dataset that is associated with workspace object(s). The dataset type can be
        specified along with the relation used when it is attached to a workspace object. Information corresponding to
        a particular file inside a dataset can be retrieved.
        
        Use cases:
        User wants to get information about files inside a dataset that is associated with workspace objects (WSO).
        Typically it will be used to get and view the  image or icon files associated with datasets attached to
        workspace objects.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getFileIds',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'criteria': criteria},
            response_cls=GetFileIdsResponse,
        )

    @classmethod
    def getKeyLOVs(cls, keyLOVIds: List[str]) -> GetKeyLOVsResponse:
        """
        Gets the information for classification key-LOVs  based on given ID(s). Information such as key-LOV's name,
        display options, and key and value entries can be obtained. A key-LOV is a list of values used in
        classification. The key-LOVs are used to define one or more values that can be set for classification
        dictionary attributes
        
        Typical format of a key-LOV -
        
            <key-LOV ID>:<key-LOV Name>
            <Key10>:<Value10>
            <Key20>:<Value20>
        
        Example of a key-LOV
        
        - 33381:Design Categories
            Des1:Bearing
            Des2:Bracket
            Des3:Frame
            Des4:LeadBox
        
        
        Use cases:
        User wants to retrieve the information for an existing key-LOV using the key-LOV's unique identifier. The
        operation is similar to 'getKeyLOVs2'(). But 'getKeyLOVs2'()provides more detailed information about any
        key-LOVs .
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception. In all other cases
        failures will be returned with the Key-LOV ID mapped to the error message in the 'ServiceData' list of partial
        errors of the 'GetKeyLOVsResponse' return structure.
        """
        return cls.execute_soa_method(
            method_name='getKeyLOVs',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'keyLOVIds': keyLOVIds},
            response_cls=GetKeyLOVsResponse,
        )

    @classmethod
    def getParents(cls, childIds: List[str]) -> GetParentsResponse:
        """
        Gets the classification class ID(s) of all parent classes in a hierarchy, based on given classification class
        ID. The parent class IDs are sorted as immediate parent first, toplevel parent last.
        
        Use cases:
        User needs to determine all the parent classes for any given class in a classification hierarchy.  If user
        needs to get the children of the given class ID, then 'getChildren'() operation shall be used.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.
        In all other cases failures will be returned with the Class ID mapped to the error message in the 'ServiceData'
        list of partial errors of 'GetParentsResponse' return structure.
        """
        return cls.execute_soa_method(
            method_name='getParents',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'childIds': childIds},
            response_cls=GetParentsResponse,
        )

    @classmethod
    def getPartFamilyTemplates(cls, clsClassIds: List[str]) -> GetPartFamilyTemplatesResponse:
        """
        Finds the information for part family templates (PFT) based on the classification class IDs. Part family
        templates can be used to define geometry and certain properties of the geometry as variable properties. They
        can be attached to a classification class. For any classification class, user can find out the associated part
        family templates and their information.
        
        Use cases:
        While using graphics builder, users often require information about the part family template attached to the
        classification classes.  Graphics builder is a program used by classification administration that communicates
        with the Teamcenter server to generate graphics. The graphics builder uses NX libraries.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getPartFamilyTemplates',
            library='Classification',
            service_date='2007_01',
            service_name='Classification',
            params={'clsClassIds': clsClassIds},
            response_cls=GetPartFamilyTemplatesResponse,
        )
