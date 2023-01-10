#!/usr/bin/env python
# coding: utf-8

# Copyright (c) seerai.
# Distributed under the terms of the Modified BSD License.

"""
UI widget for interacting with the Entanglement knowledge graph through Jupyter
"""

from geodesic.account import get_projects, get_active_project
from geodesic.entanglement.object import Object, get_objects
from geodesic.entanglement.graph import Graph
from geodesic.utils import DeferredImport

from ._frontend import module_name, module_version

ipywidgets = DeferredImport('ipywidgets')
traitlets = DeferredImport('traitlets')

class EntanglementWidget(ipywidgets.DOMWidget):
    _model_name = traitlets.Unicode('EntanglementModel').tag(sync=True)
    _model_module = traitlets.Unicode(module_name).tag(sync=True)
    _model_module_version = traitlets.Unicode(module_version).tag(sync=True)
    _view_name = traitlets.Unicode('EntanglementView').tag(sync=True)
    _view_module = traitlets.Unicode(module_name).tag(sync=True)
    _view_module_version = traitlets.Unicode(module_version).tag(sync=True)
    object_value = traitlets.Dict({}).tag(sync=True)
    projects = traitlets.List().tag(sync=True)
    search_term = traitlets.Unicode('').tag(sync=True)
    search_project = traitlets.Unicode().tag(sync=True)
    search_results = traitlets.Dict({}).tag(sync=True)
    connections_node = traitlets.Unicode('').tag(sync=True)
    connections_results = traitlets.Dict({}).tag(sync=True)

    def __init__(self, obj={}, **kwargs):
        super().__init__(**kwargs)
        self.projects = [p.name for p in get_projects()]
        self.observe(self.graph_search, names='search_term')
        self.observe(self.get_connections, names='connections_node')

    def graph_search(self, change):
        """
        When the search_term is updated, this searches the Entanglement graph for the term
        and updates the search_results accordingly. It passes the search_project as the
        project parameter, which defaults to the active project if not set by the user.
        """
        search_term = change['new']
        if search_term == '':
            return
        project = get_active_project().name if self.search_project == "" else self.search_project
        filtered_nodes = get_objects(search=search_term, project=project)
        graph = get_objects(project=project, as_graph=True)
        self.search_results = structure_graph_data(graph, filtered_nodes)

    def get_connections(self, change):
        """
        When the connections_node is changed, this calls get_connections_data to retrieve
        all the nodes and connections associated with the specified node, which it uses to
        update connections_results.
        """
        uid = change['new']
        self.connections_results = get_connections_data(uid)


def structure_graph_data(graph: Graph, filtered_nodes=None) -> dict:
    """
    Converts an Entanglement graph into the JSON format required for the Entanglement Widget

    Args:
        graph: the Graph to be displayed in the widget.
        filtered_nodes: list of only nodes needed when searching, as using get_project with
        a search parameter specified returns no edges. This means the filtered list of nodes
        must be sourced separately. When initially rendering the widget, or in any other
        situation where the graph contains the proper edges, it is unneeded.

    Returns:
        A dict of the data of the graph converted to the required JSON schema.
        The format is as follows:
        {
            'objects': [
                { // JSON of node's data },
                ...
            ],
            'connections': [
                {
                    'subject': { // JSON of subject node's data },
                    'predicate': { 'name': 'name-of-connection' },
                    'object: { // JSON of object node's data }
                },
                ...
            ]
        }
    """
    if filtered_nodes is None:
        filtered_nodes = graph.nodes
    graph_data = {}
    graph_data['objects'] = list(map(dict, filtered_nodes))
    graph_data['connections'] = []
    for edge in graph.edges:
        if edge[0] in filtered_nodes and edge[1] in filtered_nodes:
            connection = {}
            edge_data = graph.get_edge_data(edge[0], edge[1])
            connection['subject'] = dict(edge[0])
            connection['object'] = dict(edge[1])
            connection['predicate'] = {'name': edge_data['name']}
            graph_data['connections'].append(connection)
    return graph_data

def get_connections_data(uid: str) -> dict:
    """
    Gets all the connections involving a particular node in the graph and adds them to
    the representation.

    Args:
        uid: the uid of the node whose full list of connections the user wants added
        to the graph

    Returns:
        A dict of the data of all connections involving the node, formatted in the
        required schema (as described in structure_graph_data)
    """
    source_node = Object().load(uid)
    connection_list = source_node.connections()
    graph_data = {}
    graph_data['connections'] = connection_list
    graph_data['objects'] = []
    for connection in connection_list:
        if connection.subject.uid == uid:
            object_node = Object().load(connection.object.uid)
            graph_data['objects'].append(object_node)
        elif connection.object.uid == uid:
            subject_node = Object().load(connection.subject.uid)
            graph_data['objects'].append(subject_node)
    return graph_data
