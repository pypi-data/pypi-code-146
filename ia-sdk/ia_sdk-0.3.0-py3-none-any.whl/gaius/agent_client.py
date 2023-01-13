"""Implements the "Agent" interface."""
import functools
import io
import json
import uuid
from typing import Dict, List, Any, Tuple, Union
from os.path import join
from datetime import datetime
from copy import deepcopy
import requests

from ia.gaius.genome_info import Genome


class AgentQueryError(BaseException):
    """Raised if any query to any node returns an error."""
    pass


class AgentConnectionError(BaseException):
    """Raised if connecting to any node returns an error."""
    pass


def _ensure_connected(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        if not self._connected:
            raise AgentConnectionError(
                'Not connected to a agent. You must call `connect()` on a AgentClient instance before making queries'
            )
        return f(self, *args, **kwargs)

    return inner


def _remove_unique_id(response: dict) -> dict:
    """Return *response* with the key 'unique_id' removed regardless of nesting."""
    if isinstance(response, dict):
        if 'unique_id' in response:
            del response['unique_id']
        for value in response.values():
            if isinstance(value, dict):
                _remove_unique_id(value)
    return response


class AgentClient:
    """Interface for interacting with agents."""

    def __init__(self, bottle_info: dict, verify=True):
        """
        Provide agent information in a dictionary.

        Example:
            .. code-block:: python
            
                from ia.gaius.agent_client import AgentClient

                agent_info = {'api_key': 'ABCD-1234',
                            'name': 'gaius-agent',
                            'domain': 'intelligent-artifacts.com',
                            'secure': False}

                agent = AgentClient(agent_info)
                agent.connect()

                agent.set_ingress_nodes(['P1'])
                agent.set_query_nodes(['P1'])

        """
        self.session = requests.Session()
        self.genome = None
        self._bottle_info = bottle_info
        self.name = bottle_info['name']
        self._domain = bottle_info['domain']
        self._api_key = bottle_info['api_key']
        self.ingress_nodes = []
        self.query_nodes = []
        self._headers = {'X-API-KEY': self._api_key}
        self.all_nodes = []
        self._connected = False
        self.genome = None
        self.gaius_agent = None
        self.send_unique_ids = True
        self.summarize_for_single_node = True
        self._verify = verify
        if 'secure' not in self._bottle_info or self._bottle_info['secure']:
            self._secure = True
            if not self.name:
                self._url = 'https://{domain}/'.format(**self._bottle_info)
            else:
                self._url = 'https://{name}.{domain}/'.format(**self._bottle_info)
        else:
            self._secure = False
            if not self.name:
                self._url = 'http://{domain}/'.format(**self._bottle_info)
            else:
                self._url = 'http://{name}.{domain}/'.format(**self._bottle_info)

    def __repr__(self) -> str:
        return (
            '<{name}.{domain}| secure: %r, connected: %s, gaius_agent: %s, \
                  ingress_nodes: %i, query_nodes: %i>'.format(
                **self._bottle_info
            )
            % (
                self._secure,
                self._connected,
                self.gaius_agent,
                len(self.ingress_nodes),
                len(self.query_nodes),
            )
        )

    def receive_unique_ids(self, should_set: bool = True) -> bool:
        self.send_unique_ids = should_set
        return self.send_unique_ids

    def connect(self) -> Dict:
        """Establishes initial connection to GAIuS agent and grabs the agent's genome for node definitions.

            Example:
                    .. code-block:: python

                        agent_info = {...}
                        agent = AgentClient(agent_info)
                        agent.connect()
        """
        response_data = self.session.get(self._url + 'connect', verify=self._verify, headers=self._headers).json()
        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise AgentConnectionError("Connection failed!", response_data)

        self.genome = Genome(response_data['genome'])
        self.gaius_agent = response_data['genome']['agent']
        self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        if response_data['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': response_data['connection'], 'agent': response_data['genie']}

    def set_ingress_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define where data will be sent.
        
            Example:
                .. code-block:: python
                
                    # when observing data, it will be sent to only P1 by default
                    agent.set_ingress_nodes(nodes=["P1"])
        """
        if nodes is None:
            nodes = []
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.ingress_nodes

    def set_query_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define which nodes should return answers.
        
            Example:
                .. code-block:: python
                
                    agent.set_query_nodes(nodes=["P1"])
        """
        if nodes is None:
            nodes = []
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.query_nodes

    def _query(
        self, query_method: Any, path: str, data: Union[dict, str] = None, nodes: List = None, unique_id: str = None
    ) -> Union[dict, Tuple[dict, str]]:
        """Internal helper function to make a REST API call with the given *query* and *data*."""
        if not self._connected:
            raise AgentConnectionError(
                'Not connected to a agent. You must call `connect()` on a AgentClient instance before making queries'
            )
        result = {}
        if unique_id is not None:
            if data:
                data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}
                
        data = json.loads(json.dumps(data))
        
        if isinstance(nodes[0], str):
            nodes = [{'name': name, 'id': self.genome.primitive_map[name]} for name in nodes]
        for node in nodes:
            full_path = f'{self._url}{node["id"]}/{path}'
            try:
                if data is not None:
                    response = query_method(full_path, verify=self._verify, headers=self._headers, json={'data': data})
                else:
                    response = query_method(full_path, verify=self._verify, headers=self._headers)
                response.raise_for_status()
                response = response.json()
                if response['status'] != 'okay':
                    raise AgentQueryError(response['message'])
                if not self.send_unique_ids:
                    response = _remove_unique_id(response['message'])
                else:
                    response = response['message']
                if len(nodes) == 1 and self.summarize_for_single_node:
                    result = response
                else:
                    result[node['name']] = response
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None
        if unique_id is not None:
            return result, unique_id
        return result

    def set_summarize_for_single_node(self, value: bool):
        """When True, queries against a single node return responses directly instead of in a dict key.
        
            Example:
                .. code-block:: python
                
                    # set summarize_for_single_node to True
                    >>> agent.set_summarize_for_single_node(value=True)
                    >>> gdf = {'strings':['hello'], 'vectors': [], 'emotives':{}}
                    >>> agent.observe(gdf)
                    'observed'
                    
                    # set summarize_for_single_node to False
                    >>> agent.set_summarize_for_single_node(value=False)
                    >>> agent.observe(gdf)
                    {'P1': 'observed'}
        
        """
        self.summarize_for_single_node = value

    def observe(self, data: Dict, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Exclusively uses the 'observe' call.
            Will observe on nodes specified by set_ingress_nodes() unless nodes explicitly provided

            Args:
                data (dict): the GDF data to be observed
                nodes (list, optional): Nodes to observe data on, defaults to ingress nodes
            
            Example:
                .. code-block:: python
                
                    gdf = {"strings":["hello"], "vectors": [], "emotives":{}, "metadata":{}}
                    agent.observe(data=gdf, nodes=["P1"])
        """
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(self.session.post, 'observe', data=data, nodes=nodes)

    def _observe_event(self, data: Dict, unique_id: str = None) -> Tuple[dict, str]:
        """Exclusively uses the 'observe' call."""
        results = {}
        uid = None
        if unique_id is None:
            unique_id = str(uuid.uuid4())
        for node, node_data in data.items():
            response, uid = self._query(self.session.post, 'observe', data=node_data, nodes=[node], unique_id=unique_id)
            results[node] = response
        return results, uid

    @_ensure_connected
    def observe_classification(self, data=None, nodes: List = None):
        """Send a classification to all nodes as a singular symbol in the last event.

        Sending the classification as a single symbol in the last event is the canonical way to classify a sequence.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(self.session.post, 'observe', data=data, nodes=nodes)

    def show_status(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return the current status of the agent.
        
        Example:
            .. code-block:: python
            
                >>> agent.show_status(nodes=['P1'])
                {'PREDICT': True,
                'SLEEPING': False,
                'emotives': {},
                'last_learned_model_name': '',
                'models_kb': '{KB| objects: 0}',
                'name': 'P1',
                'size_WM': 0,
                'target': '',
                'time': 0,
                'vectors_kb': '{KB| objects: 0}'}
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.get, 'status', nodes=nodes)

    def learn(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return the learn results."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'learn', nodes=nodes)

    def get_wm(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return information about Working Memory.
        
        Example:
            .. code-block:: python

                >>> gdf = {'strings':['hello'], 'vectors': [], 'emotives':{}}
                >>> agent.observe(gdf, nodes=['P1'])
                >>> agent.get_wm(nodes=['P1'])
                [['hello']]
                
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.get, 'working-memory', nodes=nodes)

    def get_predictions(self, unique_id: str = None, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return prediction result data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(self.session.post, 'predictions', nodes=nodes, unique_id=unique_id)

    def clear_wm(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clear the Working Memory of the Agent.
        Will not delete any persisted memory from the KnowledgeBase
        
        Example:
            .. code-block:: python
            
                >>> agent.clear_wm(nodes=['P1'])
                'wm-cleared'
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'working-memory/clear', nodes=nodes)

    def clear_all_memory(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clear both the Working Memory and persisted memory.
        Equivalent to re-initializing the nodes specified
        
        Example:
            .. code-block:: python
            
                agent.clear_all_memory(nodes=["P1"])
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'clear-all-memory', nodes=nodes)

    def get_percept_data(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return percept data."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.get, 'percept-data', nodes=nodes)

    def get_cognition_data(self, unique_id: str = None, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return cognition data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(self.session.get, 'cognition-data', nodes=nodes, unique_id=unique_id)

    @_ensure_connected
    def change_genes(self, gene_data: Dict, nodes: List = None) -> Union[dict, Any]:
        """Change the genes in *gene_data* to their associated values.

        This will do live updates to an existing agent, rather than stopping an agent and starting a new one, as
        per 'injectGenome'.
        gene_data of form:

            {gene: value}

        Example:
            .. code-block:: python

                agent.change_genes(gene_data={"recall_threshold" : 0.15})
                    
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]

        result = {}
        for node in nodes:
            response = self.session.post(
                f"{self._url}{node['id']}/genes/change",
                verify=self._verify,
                headers=self._headers,
                json={'data': gene_data},
            ).json()
            if 'error' in response or response['status'] == 'failed':
                if len(nodes) == 1 and self.summarize_for_single_node:
                    raise AgentQueryError(response)
            self.genome.change_genes(node['id'], gene_data)
            if len(nodes) == 1 and self.summarize_for_single_node:
                return response['message']
            result[node['name']] = response['message']
        return result

    @_ensure_connected
    def get_gene(self, gene: str, nodes: List = None) -> Union[dict, Dict[Any, Dict[str, Any]]]:
        """Return the value for the gene *gene* on *nodes*.
        
        Example:
                .. code-block:: python

                    agent.get_gene(gene="recall_threshold")
        
        
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.get(
                    f"{self._url}{node['id']}/gene/{gene}", verify=self._verify, headers=self._headers
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {gene: response['message']}
                result[node['name']] = {gene: response['message']}
            except BaseException as exception:
                raise AgentQueryError(exception) from None

        return result

    @_ensure_connected
    def get_model(self, model_name: str, nodes: List = None) -> Union[dict, Any]:
        """Returns model with name *model_name*.

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found.
        
        Example:
                .. code-block:: python

                    agent.get_model("MODEL|d85f28ebda228064299035bf2dbf58f5c6484108")
        
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.get(
                    f"{self._url}{node['id']}/model/{model_name}", headers=self._headers, verify=self._verify
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result
    
    @_ensure_connected
    def delete_model(self, model_name: str, nodes: List = None) -> Union[dict, Any]:
        """Deletes model with name *model_name*.

        Model name is unique, so it should not matter that we query all nodes, 
        all its duplicates everywhere will be deleted.
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.delete(
                    f"{self._url}{node['id']}/model/{model_name}", headers=self._headers, verify=self._verify
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result
    
    @_ensure_connected
    def update_model(self, model_name: str, model: Dict, nodes: List = None) -> Union[dict, Any]:
        """Update the model  **model_name** with the data in **model** on nodes **nodes**
        
        
        .. note:: 

            This function is only capable of updating the emotives corresponding to a model. In order to update the sequence corresponding to a model,
            delete this model and reobserve the updated sequence
            
        Example:
            .. code-block:: python

                # retrieve a model already learned on an agent
                model_name = 'MODEL|d85f28ebda228064299035bf2dbf58f5c6484108'
                model = agent.get_model(model_name=model_name, nodes=['P1'])
                
                # update the emotives in the model
                model["emotives"] = [{'utility': 500}]
                agent.update_model(model_name=model_name, model=model, nodes=['P1'])
                
            
            
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.put(
                    f"{self._url}{node['id']}/model/{model_name}", headers=self._headers, verify=self._verify,
                    json={'model': model}
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result

    @_ensure_connected
    def resolve_model(self, model_name: str, nodes: List = None) -> Union[dict, Any]:
        """Returns model with name *model_name*.

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found.
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.get(
                    f"{self._url}{node['id']}/model/{model_name}", headers=self._headers, verify=self._verify
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result    

    def get_name(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return name of *nodes*.
        
            Example:
                .. code-block:: python
                
                    agent.get_name(nodes=["P1", "P2"])
        
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.get, 'name', nodes=nodes)

    def get_time(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return time on *nodes*.
        
            Example:
                .. code-block:: python
                
                    >>> agent.get_time(nodes=['P1'])
                    '1'
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.get, 'time', nodes=nodes)

    @_ensure_connected
    def get_vector(self, vector_name: str, nodes: List = None) -> Union[dict, Dict[Any, Dict[str, Any]]]:
        """Return the vector with *vector_name* on *nodes* (it will be present on at most one).
        
            Example:
                .. code-block:: python

                    agent.get_vector(vector_name="VECTOR|0b7f2aac43ae8a0d94c58be08a5b8b0ab28079de")
        
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.get(
                    f"{self._url}{node['id']}/vector", headers=self._headers, verify=self._verify, json={'data': vector_name}
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result

    @_ensure_connected
    def increment_recall_threshold(self, increment: float, nodes: List = None) -> Dict[Any, Dict[str, Any]]:
        """Increment recall threshold by *increment* on *nodes*.
        
            Args:
                increment (float): value by which to increment the recall threshold by

            Example:
                .. code-block:: python

                    agent.increment_recall_threshold(increment=0.05, nodes=["P1"])

            .. note:: 

                This command with only update the recall threshold by a specified value. 
                In order to set the recall threshold to a specific value, 
                use :func:`change_genes` instead.
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = self.session.post(
                    f"{self._url}{node['id']}/gene/increment-recall-threshold",
                    verify=self._verify,
                    headers=self._headers,
                    json={'increment': increment},
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise AgentQueryError(response)
                else:
                    self.genome.primitives[node['id']]['recall_threshold'] += increment
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {"recall_threshold": response['message']}
                result[node['name']] = {"recall_threshold": response['message']}
            except Exception as exception:
                raise AgentQueryError(str(exception)) from None

        return result

    def start_sleeping(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to start sleeping.
        
            Example:
                    .. code-block:: python

                        # will disable observing new data on node P1
                        agent.start_sleeping(nodes=["P1"])
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'sleeping/start', nodes=nodes)

    def stop_sleeping(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Wakes up sleeping *nodes*.

            Example:
                .. code-block:: python

                    # will enable observing new data on node P1
                    agent.stop_sleeping(nodes=["P1"])
        
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'sleeping/stop', nodes=nodes)

    def start_predicting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to start predicting.

            Example:
                .. code-block:: python

                    # will enable prediction generation on node P1
                    agent.start_predicting(nodes=["P1"])
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'predicting/start', nodes=nodes)

    def stop_predicting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to stop predicting.

        Useful for faster training, but abstracted nodes will not learn.
        
        Example:
            .. code-block:: python

                # will disable prediction generation on node P1
                agent.stop_predicting(nodes=["P1"])
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(self.session.post, 'predicting/stop', nodes=nodes)

    @_ensure_connected
    def ping(self, nodes: List = None) -> Union[dict, Any]:
        """Ping a node to ensure it's up.
        
            Example:
            
                .. code-block:: python
                                    
                    agent.ping(nodes=["P1"])
        """
        if nodes is None:
            return self.session.get(f'{self._url}gaius-api/ping', headers=self._headers).json()
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
            results = {}
            for node in nodes:
                response = self.session.get(f"{self._url}{node['id']}/ping", verify=self._verify, headers=self._headers).json()
                if 'error' in response or response["status"] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    print("Failure:", {node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                results[node['name']] = response["message"]
            return results
    
    @_ensure_connected
    def get_kbs(self, directory='./'):
        """Returns the KBs for the agent.
        This is a mongo-db and can be used to store or analyze locally.
        Choose the directory to save in with the directory keyword. Default is in './'.
        
        .. warning::

            .. deprecated:: 12.0 (Kehl)
            
            Use :func:`get_kbs_as_json` instead.
        
        """
        _headers = self._headers
        _headers['Content-Encoding'] = 'gzip'
        archive = self.session.get(
                    f"{self._url}database", 
                    headers=_headers,
                    json={},
                    verify=self._verify
                )
        archive_file = join(directory, f'{self.gaius_agent}-{self.name}-{datetime.now()}-kb.archive.gz')
        with open(archive_file, 'wb') as f:
            f.write(archive.content)
        return f"Saved as {archive_file}"
    
    @_ensure_connected
    def get_kbs_as_json(self, nodes: List = None, directory='./', filename=None, separated=False, ids=True, obj=False) -> Union[List[str], dict]:
        """Returns KBs of specified nodes as JSON Objects

        Args:
            nodes (list, optional): Defaults to None.
            directory (str, optional): Defaults to './'.
            separated (bool, optional): store each KB separately. Defaults to False
            ids (bool, optional): use primitive_ids as keys for knowledgebase instead of node numbers. Defaults to True
            obj (bool, optional): whether to save the kbs to a filepath or a python object
        Returns:
            Union[List(str), Dict]: List of files where KB is stored if obj = False, or big dictionary where KB is to be stored if obj = True
            

        Example:
            .. code-block:: python
            
                # save the KBs in a specified directory, without using node IDs
                # will use node names instead (e.g. P1, P2, P3)
                kb_path = "../path/to/save/dir/"
                agent.get_kbs_from_json(directory=kb_path, separated=False, ids=False)
                
                #save the KBs to the active directory, using node IDs (e.g. p46514fa2, etc.)
                agent.get_kbs_from_json(ids=True)
                
                #save the KBs to a dictionary object, using node names
                agent.get_kbs_from_json(ids=False, obj=True)
                
        """
        
        if obj == True and separated == True:
            print("obj == True and separated == True is not yet supported")
            return None
        
        if nodes is None:
            nodes = self.all_nodes
        prev_summarize_state = self.summarize_for_single_node
        try:
            self.set_summarize_for_single_node(False)
            output = self._query(requests.get, 'get_kb', nodes=nodes)
        except Exception as e:
            print(f'failed to get kb: {e}')
            raise e
        finally:
            self.set_summarize_for_single_node(prev_summarize_state)
        
        filenames = []
        if isinstance(output, dict):
            altered_output = {}
            if ids == True and "metadata" not in output:
                for key in output.keys():
                    node_id = [node["id"] for node in self.all_nodes if node['name'] == key][0]
                    altered_output[node_id] = output[key]
            else:
                altered_output = output
            if separated:
                for key, value in altered_output.items():
                    archive_file = join(directory, f'{self.gaius_agent}-{self.name}-{key}-{datetime.now()}-kb.json')
                    filenames.append(archive_file)
                    with open(archive_file, 'w') as f:
                        f.write(json.dumps({key: altered_output[key]}))
            else:
                archive_file = join(directory, f'{self.gaius_agent}-{self.name}-{datetime.now()}-kb.json')
                if filename:
                    archive_file = filename
                    
                filenames.append(archive_file)
                
                # return kb as json object
                if obj == True:
                    return altered_output
                # otherwise write json file
                with open(archive_file, 'w') as f:
                    f.write(json.dumps(altered_output))
                
        return filenames
    
    @_ensure_connected
    def load_kbs_from_json(self, path=None, obj=None):        
        """Load KBs from a JSON file

        Args:
            path (str, optional): path to JSON file where KBs are stored.
            obj  (dict, optional): object to load KnowledgeBase from

        Returns:
            str: 'success' or 'failed'
            
        Example:
            .. code-block:: python
            
                kb_path = "../path/to/kb.json"
                agent.load_kbs_from_json(path=kb_path)
        
        """
        
        node_dict = {}
        for item in self.all_nodes:
            node_dict[item['name']] = item['id']
            node_dict[item['id']] = item['id']
        
        kb = None
        if path is not None:
            with open(path, 'r') as f:
                kb = json.load(f)
        elif obj is not None:
            kb = obj
        else:
            raise Exception("Must specify path or obj argument")
        
        # check if the kb is only for a single node (simple-topology edge case)
        if 'metadata' in kb.keys():
            kb = {'P1' : kb}

        for key, value in kb.items():
            prim_id = key
            if prim_id in node_dict:
                prim_id = node_dict[prim_id]
            else:
                print(f'Warning, node {prim_id} not found in topology, skipping')
                continue
            print(f'loading node {prim_id} from kb for {key}')
            response = self.session.post(f'{self._url}{prim_id}/load_kb', headers={'X-API-KEY' : self._api_key}, json={'data': value})
            if response.status_code != 200:
                print(f'error loading kb for node {prim_id}: {response.text}')
                return 'failed', response.status_code
            print(f'loading node {prim_id} succeeded')
        
        return 'success'
    
    @_ensure_connected
    def put_kbs(self, archive_file):
        """Uploads KBs from local archive_file file.
        
        .. warning:: 
        
            .. deprecated:: 12.0 (Kehl)
            
            Use :func:`load_kbs_from_json` instead.
        
        """
        _headers = self._headers
        _headers['Content-Encoding'] = 'gzip'
        _headers['Content-type'] = 'application/octet-stream'
        with open(archive_file, 'rb') as f:
            data = f.read()
            response = self.session.put(f'{self._url}database', 
                        headers=_headers,
                        verify=self._verify,
                        data=data)
        return response.json()

    def set_target_class(self, target_class: str, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Provide a target_class symbol for the searcher to look for.

        The searcher will ignore all other classes. This is a symbol that is in the last event of a classification
        sequence.
        
        Example:
                .. code-block:: python

                    agent.set_target_class(target_class="apple", nodes=["P1"])
                    
        .. note::

            This will result in the nodes specified only predicting on models that include the target class
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(self.session.post, 'set-target-class', nodes=nodes, data=target_class)

    def clear_target_class(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clears target selection.
        
            Example:
                .. code-block:: python

                    agent.clear_target_class(nodes=["P1"])
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(self.session.post, 'clear-target-class', nodes=nodes)

    @_ensure_connected
    def tf_attach(self, name, config):
        return self.session.post(f'{self._url}/thinkflux/{name}/attach', data={'config' : config})
        
    @_ensure_connected
    def investigate_record(self, node, record):
        data = {}
        try: 
            if isinstance(node, list):
                node = node[0]
            try:
                # if the node passed is a primitive_id, get the name (P1, P2, etc.) of the node
                node = self.genome.primitives[node]['name']
            except:
                pass
            # print(f"investigating record {record}")
            return self.__get_model_details(model=record, node=[node], topLevel=True)

        except Exception as e:
            print(str(e))
        return data

    @_ensure_connected
    def __get_model_details(self, model, node, topLevel=False):
        """Recursive function to get details about a specific model on a specific node

        Args:
            model (str): the model hash to look for
            node (list(str)): The node to look for the model on (provided as a list with a single element)
            topLevel (bool, optional): flag used to show that the function is at the top level (no recursing). Defaults to False.

        Returns:
            dict: recursive structure representing the data from the topLevel model
        """
        if model == None:
            return None
        p_id = self.genome.get_primitive_map()[node[0]]
        if topLevel is True:
            # top level request
            record_data = {'record' : f"{model}",
                        'subitems':[],
                        'model': self.get_model(model, nodes=node),
                        'node': p_id,
                        'topLevel' : topLevel,
                        'bottomLevel' : False,
            }
        else:            
            record_data = {'record' : f"PRIMITIVE|{p_id}|{model['name']}",
                        'subitems':[],
                        'model': model,
                        'node': p_id,
                        'topLevel' : topLevel,
                        'bottomLevel' : False
            }
        for event_list in record_data['model']['sequence']:
            event = []
            for item in event_list:
                symbol = {}
                split_model = item.split('|')
                if split_model[0] == 'PRIMITIVE':
                    node_id = split_model[1]
                    try:
                        node_name = self.genome.primitives[node_id]['name']
                    except:
                        # node name already provided
                        node_name = node_id
                        pass
                    sub_model = self.get_model(split_model[2], nodes=[node_name])
                    symbol = self.__get_model_details(model=sub_model, node=[node_name])
                elif split_model[0] == 'VECTOR':
                    symbol = {'record': item,
                                'data'  : self.get_vector(item, nodes=node),
                                'subitems': None,
                                'bottomLevel': True,
                                'topLevel' : False,
                                'node':node[0]}
                else:
                    # print(f'reached symbol: {item}')
                    if 'VECTOR' in item:
                        symbol = {'record': item,
                                    'data'  : self.get_vector(item, nodes=node),
                                    'subitems': None,
                                    'bottomLevel': True,
                                    'topLevel' : False,
                                    'node' : node[0]}
                    else:
                        symbol = item
                event.append(deepcopy(symbol))
            record_data["subitems"].append(event)
        if tuple(record_data["subitems"]) == tuple(record_data["model"]["sequence"]):
            del record_data["subitems"]
            record_data['bottomLevel'] == True
        else:
            pass
        if not topLevel:
            if 'subitems' in record_data:
                record_data["subitems"] = tuple(record_data["subitems"])
            else:
                record_data["subitems"] = None
                record_data['bottomLevel'] = True
        return record_data
    
__all__ = ("AgentConnectionError", "AgentClient", "AgentQueryError")