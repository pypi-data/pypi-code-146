import logging
from typing import Dict
from typing import List
from typing import Union

from flask import abort
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
from jumonc.tasks import CPU

logger = logging.getLogger(__name__)

links:        List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
status_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
config_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

cpu_path = "/cpu"

@RESTAPI.route(api_version_path + cpu_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnCPULinks(version: int) -> Response:
    logger.debug("Accessed /v%i/cpu/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + cpu_path + "/status", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnCPUStatusLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/cpu/status", version)
    return make_response(jsonify(sorted(status_links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + cpu_path + "/config", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnCPUConfigLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/cpu/config", version)
    return make_response(jsonify(sorted(config_links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.pluginIsWorking("jumonc_CPUPlugin") is True:
        links.append(registerStatusLinks(version))
        links.append(registerConfigLinks(version))
    return {
        "link": "/v" + str(version) + cpu_path,
        "isOptional": False,
        "description": "Gather information concerning the CPU",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerStatusLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    types: List[str] = ["load",
                        "percent",
                        "frequency"]
    descriptions: List[str] = ["Get the system load, duration can be 1,5 or 15 min",
                               "Get the CPU utilization in percent",
                               "Get the CPU frequency in MHz"]
    if pluginInformation.pluginIsWorking("jumonc_CPUPlugin") is True:
        parameters = [  {"name": "node",
                        "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                        {"name": "token",
                        "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
        parameters.append(get_prefer_id_description())
        
        for i, typeStr in enumerate(types):
            status_links.append({
            "link": "/v" + str(version) + cpu_path + "/status/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": parameters
            })
        
        @RESTAPI.route(api_version_path + cpu_path + "/status/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        @generate_cache_id
        def returnCPUStatus(version: int, datatype:str, cache_id: int) -> Response:
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/cpu/status/%s", version, datatype)
            
            
            data = CPU.plugin.getStatusData(dataType = datatype,
                                            overrideHumanReadableWithValue = humanReadable)
            if len(data) > 0:
                for data_element in data:
                    logger.debug(str(data_element))
                    for result_name, result in data_element.items():
                        cache.addResult(cache_id, result_name, result)
                cache.commit()
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/cpu/status/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + cpu_path + "/status",
        "isOptional": False,
        "description": "Gather information concerning the cpu status",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerConfigLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    types : List[str] = []
    descriptions : List[str] = []
    if pluginInformation.pluginIsWorking("jumonc_CPUPlugin") is True:
        for i, typeStr in enumerate(types):
            config_links.append({
            "link": "/v" + str(version) + cpu_path + "/config/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": [
                {"name": "duration",
                "description": "When this parameter is not present the raw data value(s) will be provided, otherwise the average value per second"},
                {"name": "humanReadable",
                "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                {"name": "node",
                "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                {"name": "token",
                "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
            })
        
        @RESTAPI.route(api_version_path + cpu_path + "/config/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        def returnCPUConfig(version: int, datatype:str) -> Response:
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/cpu/config/%s", version, datatype)
            data = CPU.plugin.getConfigData(dataType = datatype, overrideHumanReadableWithValue = humanReadable)
            
            
            
            if len(data) > 0:
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/cpu/config/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + cpu_path + "/config",
        "isOptional": False,
        "description": "Gather information concerning the cpu config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
