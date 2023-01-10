from __future__ import annotations

from tcsoa.gen.RelationshipViewer._2012_10.NetworkEngine import GraphTypeListResponse, GraphStyleDefResponse, GraphParamMap, CreateRelationsResponse, QueryNetworkInputs, NetworkResponse, CreateRelationInput
from typing import List
from tcsoa.base import TcService


class NetworkEngineService(TcService):

    @classmethod
    def createRelations(cls, inputs: List[CreateRelationInput]) -> CreateRelationsResponse:
        """
        The operation will create the specified relation between the input objects (primary and secondary objects) for
        each input structure.
        
        Use cases:
        You can create relations that can be represented as edges in network graph. Such as GRM (General Relation
        Management) relation, BOM structure and PS Connection.
        """
        return cls.execute_soa_method(
            method_name='createRelations',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={'inputs': inputs},
            response_cls=CreateRelationsResponse,
        )

    @classmethod
    def getGraphStyleDef(cls) -> GraphStyleDefResponse:
        """
        Provides a style definition which can be used for client to render graph data. For example, it returns style
        definition of node shape and color,edge type and color.
        """
        return cls.execute_soa_method(
            method_name='getGraphStyleDef',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={},
            response_cls=GraphStyleDefResponse,
        )

    @classmethod
    def getViews(cls) -> GraphTypeListResponse:
        """
        The RelationShipViewer library provides graph (nodes connected via edges) views of data elements. Each graph
        has a defined view type. The view type is a container for the rules that determine what should be included in a
        graph and how it should be represented. The choice of graph view is determined based on business need. 
        
        This API provides a list of the available graph view types. A graph view is a set of configuration that can be
        used for network expansion. For example: view name, graph parameters, inquires, graph presentation rules. The
        view list is role based, different role may get different view list.
        """
        return cls.execute_soa_method(
            method_name='getViews',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={},
            response_cls=GraphTypeListResponse,
        )

    @classmethod
    def getViews2(cls, key: str) -> GraphTypeListResponse:
        """
        This operation provides a list of the available graph view types identified by the input key. A graph view is a
        set of configuration that can be used for network expansion. For example: view name, graph parameters,
        inquires, graph presentation rules. The view list is role based, different role may get different view list.
        
        The RelationShipViewer library provides graph (nodes connected via edges) views of data elements. Each graph
        has a defined view type. The view type is a container for the rules that determine what should be included in a
        graph and how it should be represented. The choice of graph view is determined based on business need.
        """
        return cls.execute_soa_method(
            method_name='getViews2',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={'key': key},
            response_cls=GraphTypeListResponse,
        )

    @classmethod
    def queryNetwork(cls, rootIds: List[str], viewName: str, graphParamMap: GraphParamMap, inquiries: List[str]) -> NetworkResponse:
        """
        This API produces a graph of data corresponding to the input parameters. For Teamcenter data source, the graph
        nodes are Teamcenter business objects, the relation between the returns objects and the input root objects may
        be Teamcenter Relation class (GRM) relationships, TraceLink and its sub types, Where used, where referenced,
        BOM relation and Tag reference.
        """
        return cls.execute_soa_method(
            method_name='queryNetwork',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={'rootIds': rootIds, 'viewName': viewName, 'graphParamMap': graphParamMap, 'inquiries': inquiries},
            response_cls=NetworkResponse,
        )

    @classmethod
    def queryNetwork2(cls, input: QueryNetworkInputs) -> NetworkResponse:
        """
        This operation produces a graph of data corresponding to the input parameters. The graph nodes are Teamcenter
        business objects, the relation between the returned objects and the input root objects may be Teamcenter
        Relation class (GRM) relationships, TraceLink and its sub types, Where used, where referenced, BOM relation and
        Tag reference.
        You can query relations supported in Teamcenter for the input root Business Objects, such as GRM (General
        Relationship Management) relation, BOM structure, Connectility, etc.
        """
        return cls.execute_soa_method(
            method_name='queryNetwork2',
            library='RelationshipViewer',
            service_date='2012_10',
            service_name='NetworkEngine',
            params={'input': input},
            response_cls=NetworkResponse,
        )
