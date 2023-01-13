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
from jumonc.tasks import Nvidia


logger = logging.getLogger(__name__)

links:        List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
status_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
config_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

gpu_path = "/gpu"

@RESTAPI.route(api_version_path + gpu_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnGPULinks(version: int) -> Response:
    logger.debug("Accessed /v%i/gpu/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + gpu_path + "/status", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnGPUStatusLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/gpu/status", version)
    return make_response(jsonify(sorted(status_links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + gpu_path + "/config", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnGPUConfigLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/gpu/config", version)
    return make_response(jsonify(sorted(config_links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    links.append(registerStatusLinks(version))
    links.append(registerConfigLinks(version))
    return {
        "link": "/v" + str(version) + gpu_path,
        "isOptional": False,
        "description": "Gather information about the GPU",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerStatusLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.pluginIsWorking("jumonc_NvidiaPlugin") is True:
        parameters = [  {"name": "humanReadable",
                        "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                            "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                        {"name": "node",
                        "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                        {"name": "token",
                        "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
        parameters.append(get_prefer_id_description())
        
        types = Nvidia.plugin.getStatusList()
        for typeStr in types:
            status_links.append({
            "link": "/v" + str(version) + gpu_path + "/status/" + typeStr,
            "isOptional": True,
            "description": "Nvidia SMI status data, for detailed description see: nvidia-smi --help-query-gpu",
            "parameters": parameters
            })
        
        @RESTAPI.route(api_version_path + gpu_path + "/status/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        @generate_cache_id
        def returnGPUStatus(version: int, datatype:str, cache_id:int) -> Response:
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/gpu/status/%s with humanReadable=%s", version, datatype, humanReadable)
            
            
            data = Nvidia.plugin.getStatusData(dataType = datatype)
            if len(data) > 0:
                cache.addResult(cache_id, datatype, str(data))
                cache.commit()
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/gpu/status/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + gpu_path + "/status",
        "isOptional": False,
        "description": "Gather information concerning the gpu status",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerConfigLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.pluginIsWorking("jumonc_NvidiaPlugin") is True:
        types = Nvidia.plugin.getStatusList()
        for typeStr in types:
            config_links.append({
            "link": "/v" + str(version) + gpu_path + "/status/" + typeStr,
            "isOptional": True,
            "description": "Nvidia SMI status data, for detailed description see: nvidia-smi --help-query-gpu",
            "parameters": [
                {"name": "humanReadable",
                "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                 "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                {"name": "node",
                "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                {"name": "token",
                "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
            })
        
        @RESTAPI.route(api_version_path + gpu_path + "/config/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        def returnGPUConfig(version: int, datatype:str) -> Response:
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/gpu/config/%s with humanReadable=%s", version, datatype, humanReadable)
            
            cache_id = cache.add_cache_entry("/v" + str(version) + "/gpu/status/" + datatype)
            
            data = Nvidia.plugin.getStatusData(dataType = datatype)
            if len(data) > 0:
                cache.addResult(cache_id, datatype, str(data))
                cache.commit()
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/gpu/status/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + gpu_path + "/config",
        "isOptional": False,
        "description": "Gather information concerning the GPU config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
