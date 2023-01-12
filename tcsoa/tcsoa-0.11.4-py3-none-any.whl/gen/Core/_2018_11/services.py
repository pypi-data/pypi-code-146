from __future__ import annotations

from tcsoa.gen.Core._2018_11.ProjectLevelSecurity import ChangeOwningProgramInput2, UserGroupRoleInfo, UserProjectsResponse
from tcsoa.gen.Core._2018_11.LogicalObject import GetLogicalObjectResponse3, GetLogicalObjectInput3
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getUserProjects2(cls, userInfoList: List[UserGroupRoleInfo], activeProjectsOnly: bool, visibleProjectsOnly: bool, privilegedProjectsOnly: bool, programsOnly: bool, programsAndTheChildProjects: bool) -> UserProjectsResponse:
        """
        This operation returns the list of TC_Project objects for the user, group, and role based on the additional
        criteria like active projects only, user privileged projects only and programs only.
        
        Use cases:
        Use Case 1: Changing group/role selection in the user setting dialog. The available projects needs to be
        populated.
        Use Case 2: Assigning workspace objects to project, the assignable projects needs to be populated. If the "show
        all user projects" checkbox is checked, then the group/role of the user session should not be considered.
        """
        return cls.execute_soa_method(
            method_name='getUserProjects2',
            library='Core',
            service_date='2018_11',
            service_name='ProjectLevelSecurity',
            params={'userInfoList': userInfoList, 'activeProjectsOnly': activeProjectsOnly, 'visibleProjectsOnly': visibleProjectsOnly, 'privilegedProjectsOnly': privilegedProjectsOnly, 'programsOnly': programsOnly, 'programsAndTheChildProjects': programsAndTheChildProjects},
            response_cls=UserProjectsResponse,
        )

    @classmethod
    def changeOwningProgram(cls, chgOwnProgramInput: List[ChangeOwningProgramInput2]) -> ServiceData:
        """
        This operation changes the owning program of the given set of objects. Owning Program (owning_project attribute
        ) is changed to the new value passed in.
        """
        return cls.execute_soa_method(
            method_name='changeOwningProgram',
            library='Core',
            service_date='2018_11',
            service_name='ProjectLevelSecurity',
            params={'chgOwnProgramInput': chgOwnProgramInput},
            response_cls=ServiceData,
        )


class LogicalObjectService(TcService):

    @classmethod
    def getLogicalObjectsWithContext(cls, loInputs: List[GetLogicalObjectInput3]) -> GetLogicalObjectResponse3:
        """
        This operation returns the logical object instances for the input list of client id and root object instance
        pairs, logical object type names and a map containing the included logical object ID, or member ID and
        configuration context UID. This operation can also return classification objects [A classification object is
        also called an ICO], if the root object or a member object or an included logical object on the logical object
        type is configured for retrieving classification data. For such use cases it also returns ICO property data in
        an ICO specific property structure. This operation can also return the presented properties of logical object
        instances and  configured included logical object instances. An included logical object is a logical object
        that has been added to the other logical object defintion.
        
        This operation will have a one-to-one mapping between the input list  and output list.  The order in the input
        list is also matched to the order in the output list. In an error scenario, an empty entry in the output list
        will be returned.
        
        Use cases:
        This operation is invoked to retrieve logical object instances by the client by passing a list of input
        structures each containing:
        1.    A list of client id and root object instance pairs.
        2.    A logical object type name.
        3.    A map containing the included logical object ID, or member ID and configuration context UID.
        
        For example, consider the below use case data for the use case(s) specified: 
        
        Use Case Data:
        
        1.    Logical Object definition 1
        Name                                        :     "LogicalObject1"
        Root business object                :       Item
        Included logical object    ID1    :    "LogicalObjectDomainA"
         
        2.    Logical Object definition 2
        Name                                        :     "LogicalObject2"
        Root business object                :       ItemRevision
        Included logical object ID2    :     "LogicalObjectDomainB"
        Included logical object ID3    :     "LogicalObjectDomainC"
        
        3.    Logical Object definition 3
        Name                                        :     "LogicalObject3"
        Root business object                :       Item
        
        4.    Logical Object definition 4
        Name                                        :     "LogicalObject4"
        Root business object                :      ItemRevision
        Retrieve classification data    :      True
        Included logical object ID4    :    "LogicalObjectDomainD"
         
        5.    Logical Object definition 5
        Name                                        :     "LogicalObjectDomainA"
        Root business object                :      ItemRevision
        
        6.    Logical Object definition 6
        Name                                        :     "LogicalObjectDomainB"
        Root business object                :      ItemRevision
        
        7.    Logical Object definition 7
        Name                                        :     "LogicalObjectDomainC"
        Root business object                :      ItemRevision
        
        8.    Logical Object definition 8
        Name                                        :     "LogicalObjectDomainD"
        Root business object                :      ItemRevision
        Retrieve classification data    :      True
        
         9.    Logical object definition 9
        Name            :     "LogicalObject9"
        Root business object    :      Item
        Member ID            :      "Member Revision"
        
        Use Case 1:
         
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {    
                rootObject         =    [Item],
                clientID            =     ["0"]
            }
        loTypeName                     =         "LogicalObject1",   
        loQueryNameValues          =           [<"Included logical object ID1", "ccUid1">]
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs list of size = 1
        and element = 1 contains 1 instance(s) of "LogicalObject1". 
        
        One instance of the included logical object: "LogicalObjectDomainA" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid1".
        
        The presented properties on the instances of "LogicalObject1" and its included logical object:
        "LogicalObjectDomainA" will be returned through Service Data.
        
        Use Case 2:
        
        GetLogicalObjectInput3[0] = {
            RootObject[0]= { 
                rootObject         =     [Item] , 
                clientID            =     ["0"]
            }
        loTypeName                   =             "LogicalObject2",
        loQueryNameValues    =           [<"Included logical object ID2", "ccUid2">]
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs list of size = 1
        and element = 1 contains 0 instance(s).
        
        Error 39040 - "TYPE_lo_instance_not_found" is stored in the partial error list of service data with "Logical
        Object type name +  root object client id" as the key which helps the caller identify the logical object type
        and root combination for which the logical object instance is not found.
        
        Use Case 3:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {    
                rootObject         =     [ItemRevision] , 
                clientID        =     ["0"]
            }
        loTypeName                             =        "LogicalObject2",
        loQueryNameValues                  =           [<"Included logical object ID2", "ccUid1">, 
                                                                     <"Included logical object ID3", "ccUid2">]
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs list of size = 1
        and element = 1 contains 1 instance(s) of "LogicalObject2". 
        
        One instance of the included logical object: "LogicalObjectDomainB" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid1".
        
        One instance of the included logical object: "LogicalObjectDomainC" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid2".
        
        The presented properties on the instances of "LogicalObject2" and its included logical objects:
        "LogicalObjectDomainB" and "LogicalObjectDomainC" will be returned through Service Data. 
        
        Error 39040 - "TYPE_lo_instance_not_found" is stored in the partial error list of service data with "Logical
        Object type name +  root object client id" as the key which helps the caller identify the logical object type
        and root combination for which the logical object instance is not found.
        
        Use Case 4:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {    
                rootObject         =     [Item], 
                clientID            =     ["0"]
            }
        
            RootObject[1]= {    
                  rootObject             =     [Item], 
                clientID                =     ["1"]
            }
        loTypeName                      =      "LogicalObject1"   
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 1
        and element = 1 contains 2 instance(s) of "LogicalObject1" and "LogicalObject1". 
        
        The instance(s) of the included logical object: "LogicalObjectDomainA" per main logical object instance will be
        returned for all the  root ItemRevision object(s) which are reached through Included Logical Object Navigation
        Path.
        
        The presented properties on the instances of  "LogicalObject1" and its included logical object:
        "LogicalObjectDomainA" will be returned through Service Data.
        
        Use Case 5:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {
                 rootObject         =     [Item], 
                clientID                =     ["0"]
            }
        
            RootObject[1]= { 
                rootObject         =     [ItemRevision], 
                clientID                =     ["1"]
            }
            loTypeName                     =      "LogicalObject1"
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 1
        and element = 1 contains 1 instance(s) of "LogicalObject1". 
        
        The instance(s) of the included logical object: "LogicalObjectDomainA" for the main logical object instance
        will be returned for all the  root ItemRevision object(s) which are reached through Included Logical Object
        Navigation Path.
        
        The presented properties on the instances of  "LogicalObject1" and its included logical object:
        "LogicalObjectDomainA" will be returned through Service Data. 
        
        Error 39040 - is stored in the partial error list of service data with "Logical Object type name +  root object
        client id" as the key which helps the caller identify the logical object type and root combination for which
        the logical object instance is not found.
        
        Use Case 6:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {
                rootObject             =     [Item] ,  
                clientID                =     ["0"],
            }
        loTypeName                           =             "Logical Object 1" 
        loQueryNameValues                  =           [<"Included logical object ID1", "ccUid1">]
        }
        
        GetLogicalObjectInput3[1] = { 
            RootObject[1]= {
                rootObject             =     [ItemRevision],
                clientID                =     ["0"],
            }
        loTypeName                         =         "LogicalObject2",
        loQueryNameValues             =           [ <"Included logical object ID2", "ccUid2">]   
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 2
        and element = 1 returns 1 instance(s) of "LogicalObject1". 
        
        One instance of the included logical object: "LogicalObjectDomainA" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid1".
        
        The presented properties on the instances of "LogicalObject1" and its included logical object:
        "LogicalObjectDomainA" will be returned through Service Data. 
        
        and element = 2 returns 1 instance(s) of "LogicalObject2". 
        
        One instance of the included logical object: "LogicalObjectDomainB" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid2".
        
        The instance(s) of the included logical object: "LogicalObjectDomainC" for the main logical object instance
        will be returned for all the  root ItemRevision object(s) which are reached through Included Logical Object
        Navigation Path.
        
        The presented properties on the instances of "LogicalObject2" and its included logical objects:
        "LogicalObjectDomainB" and "LogicalObjectDomainC" will be returned through Service Data. 
        
        Use Case 7:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {
                rootObject         =    [Item] , 
                clientID        =     ["0"]
            }
        loTypeName                      =      "Logical Object 1"
        }
        
        GetLogicalObjectInput3[1] = { 
            RootObject[0]= {
                rootObject         =     [Item] , 
            clientID                    =     ["0"]
            }
        loTypeName                      =      "LogicalObject2"   
        }
        
        GetLogicalObjectInput3[2] = { 
            RootObject[0]= {
                rootObject         =     [Item] , 
                clientID                =     ["0"]
            }
        loTypeName                      =      "LogicalObject3"}
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 3
        and element = 1 returns 1 instance(s) of "LogicalObject1". 
        
        The instance(s) of the included logical object: "LogicalObjectDomainA" for the main logical object instance
        will be returned for all the  root ItemRevision object(s) which are reached through Included Logical Object
        Navigation Path.
        
        The presented properties on the instances of "LogicalObject1" and its included logical object:
        "LogicalObjectDomainA" will be returned through Service Data. 
        
        and element = 2 contains 0 instance(s)
        
        and element = 3 contains 1 instance(s) of "LogicalObject3". 
        
        The presented properties on  the instance of  "LogicalObject3" will be returned through Service Data.
        
        Error 39040 - "TYPE_lo_instance_not_found" is stored in the partial error list of service data with "Logical
        Object type name +  root object client id" as the key which helps the caller identify the logical object type
        and root combination for which the logical object instance is not found.
        
        Use Case 8:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {
                rootObject         =     [ItemRevision] , 
                clientID                =     ["0"]
                }
        loTypeName                       =      "Logical Object 4"   
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 1
        and element = 1 returns 1 instance(s) of "Logical Object 4".
        
        The instance(s) of the included logical object: "LogicalObjectDomainD" for the main logical object instance
        will be returned for all the  root ItemRevision object(s) which are reached through Included Logical Object
        Navigation Path.
        The ICO data for the root ItemRevision object of "LogicalObject4" and the ICO data for the root ItemRevision
        object of the included logical object: "LogicalObjectDomainD" will be also returned.
        The presented properties on the instances of  "LogicalObject4" and its included logical object:
        "LogicalObjectDomainD"  will be returned through Service Data. 
        
        Use Case 9:
        
        GetLogicalObjectInput3[0] = { 
            RootObject[0]= {
                rootObject         =     [ItemRevision] , 
                clientID                =     ["0"],
            }
        loTypeName                         =             "Logical Object 4",
        loQueryNameValues                  =           [<"Included logical object ID4", "ccUid1">]
        }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs listof size = 1
        and element = 1 returns 1 instance(s) of "Logical Object 4".
        
        One instance of the included logical object: "LogicalObjectDomainD" will be returned if the root ItemRevision
        object of the included logical object satisfies the configuration context specified by "ccUid1".
        The ICO data for the root ItemRevision object of "LogicalObject4" and the ICO data for the root ItemRevision
        object of the included logical object: "LogicalObjectDomainD" will be also returned.
        The presented properties on the instances of "LogicalObject4" and its included logical object:
        "LogicalObjectDomainD" will be returned through Service Data.
        
        Use Case 10:
        
        GetLogicalObjectInput3[0] = { 
        RootObject[0]= {    
        rootObject         =    [Item],
        clientID        =     ["0"]
        }
        loTypeName         =      "LogicalObject9",   
        loQueryNameValues      =           [<"Member ID1", "ccUid1">]
         }
        
        then GetLogicalObjectResponse3 structure would contain loOutputs list of size = 1
        and element = 1 contains 1 instance(s) of "LogicalObject9". 
        One instance of the logical object: "LogicalObject9" will be returned if the Member Revision satisfies the
        configuration context specified by "ccUid1".
        The presented properties on the instances of "LogicalObject9" will be returned through Service Data.
        """
        return cls.execute_soa_method(
            method_name='getLogicalObjectsWithContext',
            library='Core',
            service_date='2018_11',
            service_name='LogicalObject',
            params={'loInputs': loInputs},
            response_cls=GetLogicalObjectResponse3,
        )
