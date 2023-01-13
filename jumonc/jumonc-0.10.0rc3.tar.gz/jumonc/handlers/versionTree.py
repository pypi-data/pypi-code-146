import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import Response

from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers import cache
from jumonc.handlers import cpu
from jumonc.handlers import gpu
from jumonc.handlers import io
from jumonc.handlers import job
from jumonc.handlers import main_memory
from jumonc.handlers import network
from jumonc.handlers import planed
from jumonc.handlers.base import api_version_path
from jumonc.handlers.base import check_version
from jumonc.handlers.base import RESTAPI


logger = logging.getLogger(__name__)

links: Dict[str, List[Dict[str, Union[bool, str, List[Dict[str, str]]]]]] = {}


@RESTAPI.route(api_version_path)
@check_version
@check_auth(scopes["see_links"])
def returnVersionLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/", version)
    return make_response(jsonify(sorted(links["v" + str(version)], key=lambda dic: dic['link'])), 200)


def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    links_this_version: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
    
    links_this_version.append(cache.registerRestApiPaths(version))
    links_this_version.append(cpu.registerRestApiPaths(version))
    links_this_version.append(gpu.registerRestApiPaths(version))
    links_this_version.append(io.registerRestApiPaths(version))
    links_this_version.append(job.registerRestApiPaths(version))
    links_this_version.append(main_memory.registerRestApiPaths(version))
    links_this_version.append(network.registerRestApiPaths(version))
    links_this_version.append(planed.registerRestApiPaths(version))
    
    links["v" + str(version)] = links_this_version
    
    
    
    return {
        "link": "/v" + str(version),
        "isOptional": False,
        "description": "Following this links leads to API version " + str(version),
        "parameters": [
             {"name": "token",
              "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
        ]
    }
