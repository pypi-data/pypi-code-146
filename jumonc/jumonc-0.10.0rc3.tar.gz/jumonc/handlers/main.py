import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import Response

from jumonc.handlers import auth
from jumonc.handlers import base
from jumonc.handlers import versionTree


logger = logging.getLogger(__name__)

links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []




@base.RESTAPI.route("/", methods=["GET"])
def returnRootLinks() -> Response:
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)


def registerRestApiPaths() -> None:
    for i in range(base.start_version, base.end_version + 1):
        links.append(versionTree.registerRestApiPaths(i))
        
    links.append(auth.registerLogin())
    links.append(auth.registerLogout())
    links.append(auth.registerScope())

    links.append({
        "link": "/version",
        "isOptional": False,
        "description": "Get current version of jumonc",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    })
    links.append({
        "link": "/ping",
        "isOptional": False,
        "description": "Test link to test avaibility of jumonc REST API",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    })
    links.append({
        "link": "/stop",
        "isOptional": False,
        "description": "Calling this link stops jumonc",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    })
