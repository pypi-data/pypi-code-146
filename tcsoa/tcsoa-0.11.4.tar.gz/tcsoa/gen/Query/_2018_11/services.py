from __future__ import annotations

from tcsoa.gen.Query._2018_11.SavedQuery import BusinessObjectQueryInput2
from typing import List
from tcsoa.gen.Query._2007_09.SavedQuery import SavedQueriesResponse
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def executeBOQueriesWithContext(cls, inputs: List[BusinessObjectQueryInput2]) -> SavedQueriesResponse:
        """
        Execute business object searches (Simple Search) and return search results. 
        
        This operation is invoked to query business object instances including Logical Object instances. The input
        structure identifies the type, clauses, and max number to return for the search. Additionally, a map of of
        property name and ConfigurationContext pairs are input to support configuration context as a filter for the
        search.
        
        Use cases:
        This operation is invoked to query business object instances including Logical Object instances.
        
        The Logical Object query use cases are described below: 
        
        Logical Object Query Use Case Data:
        
        1.    Logical object definition 1
            Name                                            :     "LogicalItem"
            Root business object                :      Item
            memberID1                                :     ItemRevision
            Included logical object ID1        :    "LogicalItemRevisionDomainA"
        
        2.    Logical object definition 2
            Name                                            :     "LogicalItemRevisionDomainA"
            Root business object                    :      ItemRevision
        
        
        
         Use Case 1: 
         
        BusinessObjectQueryInput2 [0] = { 
            typeName                       =      "LogicalItem", 
            clauses [0]= 
                { 
                    propName = "object_name",
                    propValue = "design1",
                    mathOperator = "=",
                    logicOperator = "AND"
                  }
            maxNumToReturn         =     30,
            requestId             =     1,
            clientId             =     1,
        }
        
        This operation will return instances of "LogicalItem", object_name of root "Item" is "design1". Since no
        configuration context is provided for "Included logical object ID1", all the instances of 
        "LogicalItemRevisionDomainA" will be returned.
        
        The presented properties on the instances of "LogicalItem" and its included logical object:
        "LogicalItemRevisionDomainA" will be returned through Service Data. 
        
        Use Case 2:
        
        BusinessObjectQueryInput2 [0] = { 
            typeName                       =      "LogicalItem", 
            clauses [0]= 
            { 
                    propName = "object_name",
                propValue = "design1",
                mathOperator = "=",
                logicOperator = "AND"
              }
            maxNumToReturn         =     30,
            requestId             =     1,
            clientId             =     1,
            configurationContextMap =           [<"Included logical object ID1", "ConfigContextUid1">]
        }
        
        This operation will return instances of "Logical Object 1", object_name of root "Item" is "design1". Since the
        configuration context is provided for "Included logical object ID1", one instance of 
        "LogicalItemRevisionDomainA" will be returned for the root Item Revision which satisfies the input
        configuration context criteria.
        
        The presented properties on the instances of "LogicalItem" and its included logical object:
        "LogicalItemRevisionDomainA" will be returned through Service Data.
        
        Use Case 3:
        
        BusinessObjectQueryInput2 [0] = { 
            typeName                       =      "LogicalItem", 
            clauses [0]= 
            { 
                    propName = "object_name",
                propValue = "design1",
                mathOperator = "=",
                logicOperator = "AND"
              }
            maxNumToReturn         =     30,
            requestId             =     1,
            clientId             =     1,
            configurationContextMap =           [<"memberID1", "ConfigContextUid2">]
        }
        
        This operation will return instances of "Logical Object 1", object_name of root "Item" is "design1". Since the
        configuration context is provided for "memberID1", one instance of "ItemRevision" will be returned for the root
        Item which satisfies the input configuration context criteria.
        
        The presented properties on the instances of "LogicalItem" and its included logical object:
        "LogicalItemDomainA" will be returned through Service Data.
        """
        return cls.execute_soa_method(
            method_name='executeBOQueriesWithContext',
            library='Query',
            service_date='2018_11',
            service_name='SavedQuery',
            params={'inputs': inputs},
            response_cls=SavedQueriesResponse,
        )
