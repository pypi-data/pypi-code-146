"""Provides utilities for higher level operations on KnowledgeBases"""
from ia.gaius.agent_client import AgentClient
import traceback

def list_models(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: model_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (_type_, optional): nodes to list models on

    Returns:
        dict: {node_name: model_list} for each node specified in nodes
        
    Example:
        .. code-block:: python

            agent = AgentClient(agent_info)
            
            #get list of models found on node P1
            models = list_models(agent, nodes=['P1'])
    
    """
    if not agent._connected:
        agent.connect()
    
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        models_dict = {k : list(v['models_kb'].keys()) for k,v in kb.items()}

    except Exception as e:
        print(f'Error in list_models: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return models_dict

def list_symbols(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: symbol_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (_type_, optional): nodes to list symbols on

    Returns:
        dict: {node_name: symbol_list} for each node specified in nodes
        
    Example:
        .. code-block:: python

            agent = AgentClient(agent_info)
            
            #get list of symbols found on node P1
            symbols = list_symbols(agent, nodes=['P1'])
            
                
    """
    if not agent._connected:
        agent.connect()
    
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        models_dict = {k : list(v['symbols_kb'].keys()) for k,v in kb.items()}
    except Exception as e:
        print(f'Error in list_symbols: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return models_dict