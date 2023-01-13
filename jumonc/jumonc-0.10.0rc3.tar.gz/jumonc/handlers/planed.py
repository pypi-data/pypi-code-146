import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import request
from flask import Response

import jumonc.models.cache.helper as cache_helper
from jumonc import settings
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers.base import api_version_path
from jumonc.handlers.base import check_version
from jumonc.handlers.base import RESTAPI
from jumonc.models import planed_tasks


logger = logging.getLogger(__name__)

links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

scheduled_path = "/scheduled"

@RESTAPI.route(api_version_path + scheduled_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnPlanningLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/scheduled/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    if settings.SCHEDULED_TASKS_ENABLED:
        links.append(registerScheduledList(version))
        links.append(registerScheduledSchedule(version))
        links.append(registerScheduledCancel(version))
        links.append(registerScheduledLastResult(version))
        return {
            "link": "/v" + str(version) + scheduled_path,
            "isOptional": False,
            "description": "See and plan task that are executed regularily",
            "parameters": [
                {"name": "token",
                "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}
            ]
        }
           
    return {
        "link": "/v" + str(version) + scheduled_path,
        "isOptional": False,
        "description": "Scheduling functionality was disabled on startup, therefore it will not be avaiable",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }




def registerScheduledList(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    @RESTAPI.route(api_version_path + scheduled_path + "/list", methods=["GET"])
    @check_version
    @check_auth(scopes["see_links"])
    def schedulingList(version: int) -> Response:
        logger.debug("Accessed /v%i/%s/list", version, scheduled_path)
        
        return make_response(planed_tasks.get_tasks_as_flask_json(), 200)
    
    return {
        "link": "/v" + str(version) + scheduled_path + "/list",
        "isOptional": False,
        "description": "List information about all scheduled tasks",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}
        ]
    }


def registerScheduledSchedule(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    @RESTAPI.route(api_version_path + scheduled_path + "/schedule", methods=["GET"])
    @check_version
    @check_auth(scopes["full"])
    def schedulingschedule(version: int) -> Response:
        interval = request.args.get('interval', type = int)
        if interval is None:
            return make_response(jsonify("interval argument missing"), 400)
        task = request.args.get('task', type = str)
        if task is None:
            return make_response(jsonify("task argument missing"), 400)
        logger.debug("Accessed /v%i/%s/schedule with interval=%i and task \"%s\"", version, scheduled_path, interval, task)
        
        ID = planed_tasks.addScheduledTask(task, interval)
        return make_response(jsonify("Scheduled task with ID " + str(ID)), 200)
    
    return {
        "link": "/v" + str(version) + scheduled_path + "/schedule",
        "isOptional": False,
        "description": "Schedule a new task to be regularily executed",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"},
            {"name": "interval",
             "description": "Specify a time duration, specifying the waiting time between each execution in ms"},
            {"name": "task",
             "description": "Supply the string, that you could use to access this function using the REST-API. Example:" + 
                 "\"/v1/cpu/status/freq?humanReadable=False&token=12345678\",\n please include the token that denotes " +
                 "the access level needed to access this function."},
            
        ]
    }


def registerScheduledCancel(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    @RESTAPI.route(api_version_path + scheduled_path + "/cancel", methods=["GET"])
    @check_version
    @check_auth(scopes["full"])
    def schedulingCancel(version: int) -> Response:
        ID = request.args.get('id', type = int)
        if ID is None:
            ID = request.args.get('ID', type = int)
            if ID is None:
                return make_response(jsonify("ID argument missing"), 400)
        logger.debug("Accessed /v%i/%s/cancel with id=%i", version, scheduled_path, ID)
        
        if planed_tasks.cancel(ID) is False:
            return make_response(jsonify("id argument is wrong, see \" /v" + str(version) + scheduled_path + "/list\" for valid IDs"), 400)        
        return make_response(jsonify("Scheduled task with id " + str(ID) + " was canceled"), 200)
    
    return {
        "link": "/v" + str(version) + scheduled_path + "/cancel",
        "isOptional": False,
        "description": "Cancel a scheduled tasks, to stop it from being executed in the future",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"},
            {"name": "id",
             "description": "The id of the scheduled task, that you want to cancel. Can be obtained using \" /v" + str(version) + scheduled_path + "/list\""}
        ]
    }


def registerScheduledLastResult(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    
    @RESTAPI.route(api_version_path + scheduled_path + "/result", methods=["GET"])
    @check_version
    @check_auth(scopes["retrieve_simulation_data"])
    def schedulingLastResult(version: int) -> Response:
        ID = request.args.get('id', type = int)
        if ID is None:
            ID = request.args.get('ID', type = int)
            if ID is None:
                return make_response(jsonify("ID argument missing"), 400)
        logger.debug("Accessed /v%i/%s/result with id=%i", version, scheduled_path, ID)
        
        try:
            result_id = planed_tasks.task_last_result_id(ID)
            if result_id == -1:
                return make_response(jsonify("no result avaiable for this task yet. See the status using \" /v" + str(version) + scheduled_path + "/list\""),
                                             425)
            try:
                return cache_helper.get_response_for_cache_id(result_id)
            except ValueError as error:
                logger.error((error.args[0],
                               " This should not happen, because the used id was set internaly. ",
                               "For the task scheduled with schedule_id: ", str(ID)))
                return make_response("For the task scheduled with schedule_id \"" + str(ID) + "\" there was an internal error", 500)
        except ValueError as error:
            return make_response(jsonify(error.args[0]), 400)
    
    return {
        "link": "/v" + str(version) + scheduled_path + "/result",
        "isOptional": False,
        "description": "Retrieve the last result of this scheduled job",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"},
            {"name": "id",
             "description": "The id of the scheduled task. Can be obtained using \" /v" + str(version) + scheduled_path + "/list\""}
        ]
    }
