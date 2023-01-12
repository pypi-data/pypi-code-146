from __future__ import annotations

from tcsoa.gen.Core._2018_06.DataManagement import CreateIn3
from tcsoa.gen.Core._2008_06.DataManagement import CreateResponse
from tcsoa.gen.Core._2018_06.LogicalObject import GetLogicalObjectInput2, GetLogicalObjectResponse2
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createObjectsInBulkAndRelate(cls, createInputs: List[CreateIn3]) -> CreateResponse:
        """
        (1)    This is a generic operation for creation of business objects in bulk (i.e. in a set&ndash;based manner).
        All business objects will be created or none, a failure for a single object will result in no business objects
        being created.
        This operation will also create any secondary objects compounded with the main object being created. For
        example, please refer to the Create Item (a compound object) use case.
        (2)    The other task this operation will perform is to relate the created business object to the input target
        object.
        
        Use cases:
        This operation is typically preceded by a call to
        Teamcenter::Soa::Core::_2008_06::PropDescriptor::getCreateDesc or to the Client Meta Model layer to retrieve
        Create Descriptor(s) for business objects to be created.
        The CreateInput2 object is used to hold the Create Descriptor info.
        (1)      Create Item (a compound object)
        Item is a compound object. Item creation in turn creates Item Master and ItemRevision. ItemRevision creation in
        turn creates ItemRevision Master.
        This means the CreateInput2 object for the Item will in turn hold two CreateInput2 objects (in the
        CreateInputMap2 one each for "IMAN_master_form" and "revision" respectively), for Item Master and ItemRevision.
        Also, the CreateInput2 object for the ItemRevision will in turn hold CreateInput2 object (in the
        CreateInputMap2 for "IMAN_master_form_rev") for ItemRevision Master.
        (2)      Relate the created object to the input target object
        A created object is linked to the input target object (targetObject) for the input property (pasteProp). In
        case, the targetObject is empty, it would default to the Newstuff Folder or Home Folder for the session User
        depending on the value for the preference, WsoInsertNoSelectionsPref. In case, the pasteProp is empty,
        following sequence is used to come up with a preferred property name,
        (a)     If created object is of type, WolfObject and the targetObject is a Folder, pasteProp will be set to
        "TC_external_object_link".
        (b)     The format, <targetObjectTypeName>_<createdObjectTypeName>_default_relation will be used to search for
        a preference. The whole parent Type hierarchy for both, the targetObject and the createdObject will be
        searched. In case, such a preference is present, pasteProp will be set to that preference value.
        (c)     The format, <targetObjectTypeName>_default_relation will be used to search for a preference. The whole
        parent Type hierarchy for the targetObject will be searched. In case, such a preference is present, pasteProp
        will be set to that preference value.
        (d)     In case, the targetObject is a Folder, pasteProp will be set to "contents".
        (e)     Else, an error will be reported in the response.
        
        Exceptions:
        >214200 &ndash; Unable to create business objects.
        """
        return cls.execute_soa_method(
            method_name='createObjectsInBulkAndRelate',
            library='Core',
            service_date='2018_06',
            service_name='DataManagement',
            params={'createInputs': createInputs},
            response_cls=CreateResponse,
        )


class LogicalObjectService(TcService):

    @classmethod
    def getLogicalObjects2(cls, loInputs: List[GetLogicalObjectInput2]) -> GetLogicalObjectResponse2:
        """
        This operation returns the logical object instances for the input list of root object instances and logical
        object type names. This operation can also return classification objects (A classification object is also
        called an ICO), if the root obejct or a member object is configured on the logical object type for retieving
        classification data. For such use cases it also returns ICO property data in an ICO specific property structure.
        
        This operation will have a one-to-one mapping between the input list   and output list.  The order in the input
        list is also matched to the order in the output list. In an error scenario, an empty entry in the output list 
        will be returned.
        
        Use cases:
        This operation is invoked to retrieve logical object instances by the client by passing a list of root object
        instances and logical object type names.
        
        For example, consider the below use case data for the use case(s) specified:
        Use Case Data:
        
        1. Logical object definition 1
        Name:  "Logical Object 1"
        Root business object: Item
        
        2. Logical object definition 2
        Name: "Logical Object 2"
        Root business object : ItemRevision 
        
        3. Logical object definition 3
        Name : "Logical Object 3"
        Root business object: Item
        
        4. Logical object definition 4
        Name : "Logical Object 4"
        Root business object : ItemRevision
        Retrieve classification data : True
        
        Use Case 1:
        
        GetLogicalObjectInput[0] =
        { 
           {   rootObject = Item,
                clientID = "UniqueID-1"
           } 
           loTypeName = "Logical Object 1"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 1
        and element = 1 contains 1 instance(s) of "Logical Object 1"
        
        Use Case 2:
        
        GetLogicalObjectInput[0] = 
        { 
           {   rootObjects = Item,
                  clientID = "UniqueID-2"
             } 
             loTypeName = "Logical Object 2"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 1
        and element = 1 contains 0 instance(s)
        
        Error 39040 - Is stored in the partial error list of service data with "Logical Object type name +  root object
        client id" as the key which helps the caller identify for which logical object type and root combination, the
        logical object instance is not created.
        Since Root business object for "Logical Object 2" is ItemRevision, system can&rsquo;t create a Logical Object
        instance with Item instance as root object input.
        
        Use Case 3:
        GetLogicalObjectInput[0] =
        { 
             {  rootObjects = Item
                  clientID = "UniqueID-3"
             } 
             {  rootObjects = Item
                  clientID = "UniqueID-4"
             } 
             loTypeName = "Logical Object 1"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 1
        and element = 1 contains 2 instance(s) of "Logical Object 1" and "Logical Object 1"
        
        Use Case 4:
        
        GetLogicalObjectInput[0] = 
        { 
             {  rootObjects = Item
                  clientID = "UniqueID-4"
             } 
             {  rootObjects = ItemRevision
                  clientID = "UniqueID-5"
             }
             loTypeName = "Logical Object 1"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 1
        and element = 1 contains 1 instance(s) of "Logical Object 1"
        
        Error 39040 - Is stored in the partial error list of service data with "Logical Object type name +  root object
        client id" as the key which helps the caller identify for which logical object type and root combination, the
        logical object instance is not created.
        Since Root business object for "Logical Object 1" is Item, system can&rsquo;t create a Logical Object instance
        with ItemRevision instance as root object input.
        
        Use Case 5:
        
        GetLogicalObjectInput[0] = 
        {
           {  rootObjects = Item
                clientID = "UniqueID-6"
           }
           loTypeName = "Logical Object 1"
        }
        GetLogicalObjectInput[1] = 
        { 
           {  rootObjects = ItemRevision
                clientID = "UniqueID-7"
           }
           loTypeName = "Logical Object 2"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 2
        and element = 1 returns 1 instance(s) of "Logical Object 1"
        and element = 2 returns 1 instance(s) of "Logical Object 2"
        
        Use Case 6:
        
        GetLogicalObjectInput[0] =
        { 
           {  rootObjects = Item
                clientID = "UniqueID-8"
           }
           loTypeName = "Logical Object 1"
        }
        GetLogicalObjectInput[1] =
        { 
           {  rootObjects = Item
                clientID = "UniqueID-9"
           }
           loTypeName = "Logical Object 2"
        }
        GetLogicalObjectInput[2] =
        { 
           {  rootObjects = Item
                clientID = "UniqueID-10"
           }
           loTypeName = "Logical Object 3"
        }
        
        then GetLogicalObjectResponse2 structure would contain loOutputs list of size = 3
        and element = 1 returns 1 instance(s) of "Logical Object 1"
        and element = 2 contains 0 instance(s)
        and element = 3 contains 1 instance(s) of "Logical Object 3"
        
        Error 39040 - Is stored in the partial error list of service data with "Logical Object type name +  root object
        client id" as the key which helps the caller identify for which logical object type and root combination, the
        logical object instance is not created.
        Since Root business object for "Logical Object 2" is ItemRevision, system can&rsquo;t create a Logical Object
        instance with Item instance as root object input.
        
        Use Case 7:
        GetLogicalObjectInput[0] = 
        { 
           {  rootObjects = ItemRevision
                clientID = "UniqueID-11"
           }
           loTypeName = "Logical Object 4"
        }
        
        then GetLogicalObjectResponse2 structure would contain 
        loOutputs list of size = 1 
        and element = 1 returns 1 instance(s) of "Logical Object 4"
        GetLogicalObjectOutput2 structure would contain LogicalObjectOutput2 and then LogicalObject will provide
        details for the ICO objects assocaiated with ItemRevison and ClassificationAttributeDescMap2 map would provide
        details for the classification objects assocaiated with ItemRevison.
        """
        return cls.execute_soa_method(
            method_name='getLogicalObjects2',
            library='Core',
            service_date='2018_06',
            service_name='LogicalObject',
            params={'loInputs': loInputs},
            response_cls=GetLogicalObjectResponse2,
        )
