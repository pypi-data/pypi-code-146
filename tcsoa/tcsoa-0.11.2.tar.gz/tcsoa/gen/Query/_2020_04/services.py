from __future__ import annotations

from tcsoa.gen.Query._2020_04.SavedQuery import BusinessObjectQueryInput4
from typing import List
from tcsoa.gen.Query._2007_09.SavedQuery import SavedQueriesResponse
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def executeBOQueriesWithSortAndContext(cls, inputs: List[BusinessObjectQueryInput4]) -> SavedQueriesResponse:
        """
        Execute business object searches (Simple Search) and return sorted search results. 
        This operation is invoked to query business object instances including Logical Object instances. The input
        structure identifies the type, clauses, sorting options, and max number to return for the search. Additionally,
        a map of of property name and ConfigurationContext pairs are input to support configuration context as a filter
        for the search.
        
        Use cases:
        This operation is invoked to query business object instances including Logical Object instances.
        
        The Logical Object query use cases are described below: The properties used in search clauses and sort options
        are presented properties of  Logical Object.
        
        Logical Object Query Use Case Data:
        
        1.    Logical object definition 1
            Name                                            :     "LogicalItemRevision"
            Root business object                :      ItemRevision
            Included logical object ID1        :    "LogicalItemRevisionDomainA"
        
        2.    Logical object definition 2
            Name                                            :     "LogicalItemRevisionDomainA"
            Root business object                    :      ItemRevision
        
        
        
         Use Case 1: 
         
        BusinessObjectQueryInput4 [0] = { 
            typeName                       =      "LogicalItemRevision", 
            clauses [0]= 
                { 
                    propName = "object_name",
                    propValue = "design1",
                    mathOperator = "=",
                    logicOperator = "AND"
                  }
            sortOptions [0]= 
                { 
                    sortAttribute = "item_revision_id",
                    sortOrder = "AscendingOrder"
                }
            maxNumToReturn         =     30,
            requestId             =     1,
            clientId             =     1,
        }
        
        This operation will return instances of "LogicalItemRevision", object_name of root "Item Revision" is
        "design1". Since no configuration context is provided for "Included logical object ID1", all the instances of 
        "LogicalItemRevisionDomainA" will be returned.
        
        The input sort options will return instances of "LogicalItemRevision", sorted by item_revision_id in ascending
        order.
        
        The presented properties on the instances of "LogicalItemRevision" and its included logical object:
        "LogicalItemRevisionDomainA" will be returned through Service Data.  
        
        Use Case 2:
        
        BusinessObjectQueryInput4 [0] = { 
            typeName                       =      "LogicalItemRevision", 
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
        
        This operation will return instances of "LogicalItemRevision", object_name of root "Item Revision" is
        "design1". Since the configuration context is provided for "Included logical object ID1", one instance of 
        "LogicalItemRevisionDomainA" will be returned for the root Item Revision which satifies the input configuration
        context criteria.
        
        The presented properties on the instances of "LogicalItemRevision" and its included logical object:
        "LogicalItemRevisionDomainA" will be returned through Service Data.
        """
        return cls.execute_soa_method(
            method_name='executeBOQueriesWithSortAndContext',
            library='Query',
            service_date='2020_04',
            service_name='SavedQuery',
            params={'inputs': inputs},
            response_cls=SavedQueriesResponse,
        )
