import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import request
from flask import Response

import jumonc.models.cache.helper as cache
from jumonc import settings
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers.base import api_version_path
from jumonc.handlers.base import check_version
from jumonc.handlers.base import generate_cache_id
from jumonc.handlers.base import get_prefer_id_description
from jumonc.handlers.base import RESTAPI
from jumonc.models import pluginInformation
from jumonc.tasks import LinuxNetwork
from jumonc.tasks import taskPool


logger = logging.getLogger(__name__)

links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
status_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

network_path = "/network"

@RESTAPI.route(api_version_path + network_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnNetworkLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/network/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + network_path + "/status", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnNetworkStatusLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/network/status", version)
    return make_response(jsonify(sorted(status_links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    links.append(registerStatusLinks(version))
    return {
        "link": "/v" + str(version) + network_path,
        "isOptional": False,
        "description": "Gather information concerning the network",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }

def registerStatusLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.pluginIsWorking("jumonc_LinuxNetworkPlugin") is True:
        types = LinuxNetwork.plugin.getAvaiableDataTypes()
        descriptions = LinuxNetwork.plugin.getAvaiableDataTypesDescriptions()
        types.append("All")
        descriptions.append("get all network status information")
        
        parameters = [{ "name": "duration",
                        "description": "When this parameter is not present the raw data value(s) will be provided, otherwise the average value per second"},
                        {"name": "interface",
                        "description": ("When this parameter is not present, information for all network " +
                                        "interfaces are collected, otherwise only for the specified " + 
                            "interface. Avaiable interfaces: " + str(LinuxNetwork.plugin.getAvaiableInterfaces()))},
                        {"name": "humanReadable",
                        "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                            "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                        {"name": "node",
                        "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                        {"name": "token",
                        "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
        parameters.append(get_prefer_id_description())
            
        
        for i, typeStr in enumerate(types):
            status_links.append({
            "link": "/v" + str(version) + network_path + "/status/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": parameters})
        
        @RESTAPI.route(api_version_path + network_path + "/status/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        @generate_cache_id
        def returnLinuxNetworkStatus(version: int, datatype:str, cache_id: int) -> Response:
            interface = request.args.get('interface', default = "all", type = str)
            duration = request.args.get('duration', default = -1.0, type = float)
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/network/status/%s", version, datatype)
            datatype = datatype.lower().capitalize()
            dataTypes = LinuxNetwork.plugin.getAvaiableDataTypes()
            dataTypes.append("All")
            if datatype in dataTypes:
                #cache_id = cache.add_cache_entry("/v" + str(version) + "/network/status/" + datatype)
                if duration > 0:
                    cache.addParameter(cache_id, "duration", str(duration))
                cache.addParameter(cache_id, "interface", interface)
                # cache.commit()
                
                data = networkStatusTask(cache_id = cache_id,
                                         duration = duration,
                                         datatype = datatype,
                                         interface = interface,
                                         humanReadable = humanReadable)
                if data is None:
                    return make_response(jsonify({"link": "/v" + str(version) + "/cache/id/?id=" + str(cache_id)}), 200)
                return make_response(jsonify(data, 200))
            return make_response("Invalid data type choosen",404)
        
    return {
        "link": "/v" + str(version) + network_path + "/status",
        "isOptional": False,
        "description": "Gather information concerning the network status",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}
        ]
    }


@taskPool.executeAsTask
def networkStatusTask(cache_id: int, duration: float, datatype: str, interface: str, humanReadable:bool
                     ) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str, List[int], List[float], List[str]]]]]]:
    data = LinuxNetwork.plugin.getData(dataType = datatype,
                                            duration = duration,
                                            interface = interface,
                                            overrideHumanReadableWithValue = humanReadable)
    for data_element in data:
        interface_str:Union[str, Dict[str, Union[int, float, str, List[int], List[float], List[str]]]] = data_element["interface"]  # type: ignore
        if not isinstance(interface_str, str):
            logger.warning("Unexpected datatype in passing networkdata into cache")
            continue
        for result_part_name, part in data_element.items():
            if result_part_name == "interface":
                continue
            if isinstance(part, dict):
                for result_name, result in part.items():
                    cache.addResult(cache_id, interface_str + "_" + result_part_name + "_" + result_name, result)
    cache.commit()
    return data
