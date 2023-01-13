import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import request
from flask import Response
from sqlalchemy import desc

import jumonc.models.cache.dbmodel as cache_model
import jumonc.models.cache.helper as cache_helper
from jumonc import settings
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers.base import api_version_path
from jumonc.handlers.base import check_version
from jumonc.handlers.base import RESTAPI
from jumonc.models import pluginInformation


logger = logging.getLogger(__name__)

links:List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

cache_path = "/cache"

@RESTAPI.route(api_version_path + cache_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnCacheLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/cache/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if pluginInformation.flask_path_reg is False:
        links.append(registerCacheList(version))
        links.append(registerCacheID(version))
    pluginInformation.flask_path_reg = True
    return {
        "link": "/v" + str(version) + cache_path,
        "isOptional": False,
        "description": "Retrieve old results",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerCacheList(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
        
    @RESTAPI.route(api_version_path + cache_path + "/list", methods=["GET"])
    @check_version
    @check_auth(scopes["retrieve_simulation_data"])
    def returnCacheList(version: int) -> Response:
        entries = request.args.get('entries', default = settings.CACHE_DEFAULT_ENTRIES_PER_PAGE, type = int)
        page = request.args.get('page', default = 1, type = int)
        path = request.args.get('path', default = None, type = str)
        logger.debug("Accessed /v%i/cache/list/", version)

        if page < 1:
            return make_response("Pages start with 1, you set page number to: " + str(page), 422)

        
        query = cache_model.CacheEntry.query
        
        # replace standart expandable characters to sqlalchemy versions
        if path is not None:
            path_replaced = path.replace('_', '__')\
                       .replace('*', '%')\
                       .replace('?', '_')
            path_replaced = f"%{path_replaced}%"
            query = query.filter(cache_model.CacheEntry.API_path.ilike(path_replaced))
        
        
        
        query = query.order_by(desc(cache_model.CacheEntry.cache_id))
        
        start = (page-1)*entries
        lastpage = round(query.count()/entries+0.5)
        cache_data = query.offset(start).limit(entries)
        
        data:List[Dict[str, Union[int, float,str]]] = []
        index:Dict[str, Union[int, float,str]] = {"page": page,
                     "description": "Showing cache elements for " +
                     str(start) + " to " + str(start+entries) +
                     ", most recent results first",
                     "total entries": query.count(),
                     "last page": lastpage
                    }
        
        previous_page = "/v" + str(version) + "cache/list/?"
        next_page = "/v" + str(version) + "/cache/list/?"
            
        if entries != settings.CACHE_DEFAULT_ENTRIES_PER_PAGE:
            previous_page = previous_page + "&entries=" + str(entries)
            next_page = next_page + "&entries=" + str(entries)
        
        index["path filter"] = ""
        if path is not None:
            index["path filter"] = path
            previous_page = previous_page + "&path=" + str(path)
            next_page = next_page + "&path=" + str(path)
        
        if page > 1:
            previous_page = previous_page + "&page=" + str(page-1)
            index["previous page"] = previous_page.replace("?&", "?")
        if lastpage > page:
            next_page = next_page + "&page=" + str(page+1)
            index["next page"] = next_page.replace("?&", "?")
        
        data.append(index)
            
        for element in cache_data:
            data.append({"ID": element.cache_id,
                         "time": element.time.strftime(settings.DATETIME_FORMAT),
                         "link": "/v" + str(version) + "/cache/id/?id=" + str(element.cache_id),
                         "API_path": element.API_path})
        
        return make_response(jsonify(data), 200)
        
    return {
        "link": "/v" + str(version) + cache_path + "/list",
        "isOptional": False,
        "description": "List old results that can be retrieved, if to many results are avaiable, it will be split into pages",
        "parameters": [
            {"name": "page",
             "description": "Which page will be used"},
            {"name": "entries",
             "description": "How many entries are per page"},
            {"name": "path",
             "description": "Filter to only contain results containing this path, allows the use of wildcards"},
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
        


def registerCacheID(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    @RESTAPI.route(api_version_path + cache_path + "/id", methods=["GET"])
    @check_version
    @check_auth(scopes["retrieve_simulation_data"])
    def returnCacheID(version: int) -> Response:
        c_id = request.args.get('id', type = int)
        logger.debug("Accessed /v%i/cache/id/", version)
        
        if c_id is None:
            return make_response("Missing an id argument, can not retrieve the cache result like this", 400)
        try :
            return cache_helper.get_response_for_cache_id(c_id)
        except ValueError as error:
            message = str(error.args[0]) + " You can use/v" + str(version) + "/cache/list to see all available entries"
            response = make_response(message, 400)
            print(str(response))
            return response
        
    return {
        "link": "/v" + str(version) + cache_path + "/id",
        "isOptional": False,
        "description": "Retrieve complete cache entry by ID",
        "parameters": [
            {"name": "id",
             "description": "ID of the cahce entry that shall be retrieved"},
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
