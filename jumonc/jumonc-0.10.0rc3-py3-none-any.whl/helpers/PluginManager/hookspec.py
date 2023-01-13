import argparse
from typing import Dict
from typing import List
from typing import Union

import pluggy

hookspec = pluggy.HookspecMarker("jumonc")


# Defining empty functions for plugins, therefore parameters will not be used here
#pylint: disable=unused-argument


    
@hookspec
def needed_REST_paths() -> List[str]:
    """
    Return a list of paths that this plugin wants to add to the REST-API.
    
    :return: a list of REST API paths
    """


@hookspec
def register_REST_path(requested_path: str, approved_path:str) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    """
    Register the requested path with the REST-API.

    :param requested_path: the path that was requested
    :param approved_path: the path that that was approved
    :return: if the approved path was added, return a dictonary, explaining the path,
    as a dictonary with entries for the link, a description and parameters. 
    
    note::
    A dictonary for the link description could look like this:
    {
        "link": "/v" + str(version) + gpu_path + "/config",
        "isOptional": True,
        "description": "Gather information concerning the memory config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
    
    """


@hookspec
def startup_parameter_parser() -> argparse.ArgumentParser:
    """
    Register the wanted startup parameter for this plugin.

    :return: an argparser for this plugin
    """


@hookspec
def evaluate_startup_parameter(parsed:argparse.Namespace) -> None:
    """
    Use the user supplied values for start parameters.

    :param parsed: argparse namespace
    """


@hookspec
def register_MPI(MPI_ID_min:int, MPI_ID_max:int) -> None:
    """
    Let the plugin handle all necessary steps for it's MPI communication.
    
    Let the plugin register callback options for MPI_IDs used in jumonc's communication.
    This plugin can use all MPI_IDs between min and max for all it's internal needs.
    """



@hookspec
def selfcheck_is_working() -> bool:
    """
    Let the plugin check, if everything it needs to work is avaiable.
    
    This function will be called on startup on all nodes, so that each plugin can check if all imports
    and needed system functionality is avaiable. In case one node flags the plugin as not working, 
    it will be disabled everywhere to prevent issues.
    """



#pylint: enable=unused-argument
