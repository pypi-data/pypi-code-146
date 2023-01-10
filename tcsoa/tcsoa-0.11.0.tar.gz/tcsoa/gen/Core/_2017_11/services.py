from __future__ import annotations

from tcsoa.gen.Core._2017_11.LogicalObject import GetLogicalObjectInput, GetLogicalObjectResponse
from typing import List
from tcsoa.base import TcService


class LogicalObjectService(TcService):

    @classmethod
    def getLogicalObjects(cls, loInputs: List[GetLogicalObjectInput]) -> GetLogicalObjectResponse:
        """
        This operation returns the logical object instances for the input list of root object instances and logical
        object type names. This operation can also return classification objects [ A classification object is also
        called an ICO], if the root obejct or a member object is configured on the logical object type for retieving
        classification data. For such usecases it also returns ICO property data in an ICO specific property structure.
        
        This operation returns all properties for given logical object type when property policy is not found.
        
        This operation will have a one-to-one mapping between the input vector and output vector.  The order in the
        input vector is also matched to the order in the output vector. In an error scenario, an empty entry in the
        output vector  will be returned.
        
        Use cases:
        This operation is invoked to retrieve logical object instances by the client by passing a list of root object
        instances and logical object type names.
        
        For example, consider the below use case data for the use case(s) specified:
        
        Use Case Data:
        
        1.  Logical object definition 1
        Name                           :   "Logical Object 1"
        Root business object           :   Item
        
        2.  Logical object definition 2
        Name                           :   "Logical Object 2"
        Root business object           :   ItemRevision
        
        3.  Logical object definition 3
        Name                           :   "Logical Object 3"
        Root business object           :   Item
        
        4.  Logical object definition 4
        Name                           :   "Logical Object 4"
        Root business object           :    ItemRevision
        Retrieve classification data   :    True
        
        Note: The presented property fnd0Root_ICO is automatically generated when "Retrieve classification data" is
        checked for the root business object. The same is applied for a member.
        
        
        Use Case 1:
        
        GetLogicalObjectInput[0] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 1"
         }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 1
        and element = 1 contains 1 instance(s) of "Logical Object 1"
        
        Use Case 2:
        
        GetLogicalObjectInput[0] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 2"
         }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 1
        and element = 1 contains 0 instance(s)
        
        
        Use Case 3:
        
        GetLogicalObjectInput[0] = {
        rootObjects   =   [Item, Item] ,
        loTypeName    =   "Logical Object 1"
         }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 1
        and element = 1 contains 2 instance(s) of "Logical Object 1" and "Logical Object 1"
        
        Use Case 4:
        
        GetLogicalObjectInput[0] = {
        rootObjects   =   [Item, ItemRevision] ,
        loTypeName    =    "Logical Object 1"
         }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 1
        and element = 1 contains 1 instance(s) of "Logical Object 1"
        
        
        Use Case 5:
        
        GetLogicalObjectInput [0] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 1"
        }
        GetLogicalObjectInput [1] = {
        rootObjects   =   [ItemRevision] ,
        loTypeName    =   "Logical Object 2"
        }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 2
        and element = 1 returns 1 instance(s) of "Logical Object 1"
        and element = 2 returns 1 instance(s) of "Logical Object 2"
        
        
        Use Case 6:
        
        GetLogicalObjectInput [0] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 1"
        }
        GetLogicalObjectInput [1] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 2"
        }
        GetLogicalObjectInput [2] = {
        rootObjects   =   [Item] ,
        loTypeName    =   "Logical Object 3"
        }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 3
        and element = 1 returns 1 instance(s) of "Logical Object 1"
        and element = 2 contains 0 instance(s)
        and element = 3 contains 1 instance(s) of "Logical Object 3"
        
        
        Use Case 7:
        GetLogicalObjectInput [0] = {
        rootObjects         =   [ItemRevision] ,
        loTypeName          =   "Logical Object 4"
         }
        
        then GetLogicalObjectResponse structure would contain loOutputs vector of size = 1
        and element = 1 returns 1 instance(s) of "Logical Object 4"and
        GetLogicalObjectOutput structure would contain ClassificationObjectInfoMap map and provide details for the ICO
        objects assocaiated with ItemRevison
        and ClassificationAttributeDescMap map
        would provide details for the classification class of the ICO objects assocaiated with ItemRevison.
        """
        return cls.execute_soa_method(
            method_name='getLogicalObjects',
            library='Core',
            service_date='2017_11',
            service_name='LogicalObject',
            params={'loInputs': loInputs},
            response_cls=GetLogicalObjectResponse,
        )
