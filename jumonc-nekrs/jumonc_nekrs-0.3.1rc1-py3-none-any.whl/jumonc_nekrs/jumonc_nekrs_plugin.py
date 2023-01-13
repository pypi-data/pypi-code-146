import logging
import os
import argparse

import pluggy


logger = logging.getLogger(__name__)

hookimpl = pluggy.HookimplMarker("jumonc")


links = []

nekrs_logfile = "nekrs.log"


@hookimpl
def needed_REST_paths():
    from jumonc.handlers.base import api_version_path
    return [api_version_path + "/nekRS",]


@hookimpl
def register_REST_path(requested_path, approved_path):
    from flask import jsonify, make_response
    
    from jumonc.handlers.base import check_version, RESTAPI, return_schema, get_return_schema_description
    from jumonc.authentication import scopes
    from jumonc.authentication.check import check_auth
    
    import jumonc.handlers.versionTree as tree
    
    tree.links["v1"].append({
                "link": "/v1/nekRS",
                "isOptional": True,
                "description": "Following this links leads to the nekRS jumonc plugin ",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    
    
    links.append({
                "link": "/v1/nekRS/config",
                "isOptional": True,
                "description": "Following this links leads to the nekRS config information ",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    parameters = [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
    parameters.append(get_return_schema_description())
    links.append({
                "link": "/v1/nekRS/status",
                "isOptional": True,
                "description": "Following this links leads to the nekRS status information ",
                "parameters": parameters 
            })
    
    
    @RESTAPI.route(approved_path, methods=["GET"])
    @check_version
    @check_auth(scopes["see_links"])
    def nekrs_links(version):
        logger.debug("Accessed /v%i/nekRS/", version)
        return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)
    
    
    @RESTAPI.route(approved_path + "/status", methods=["GET"])
    @check_version
    @check_auth(scopes["compute_data"])
    @return_schema("nekrs_status_schema.json")
    def nekrs_status(version):
        try:
            file = open(nekrs_logfile, "rb")
        
            end = file.seek(0, os.SEEK_END)
            if end > 3000:
                start = -3000
            else:
                start = -end    
            file.seek(-3000, os.SEEK_END)

            log = file.read().decode()

            if log.find(">>> runtime statistics") != -1:
                last_step = log.split("step= ")[-2]
            else:
                last_step = log.split("step= ")[-1]

            split = last_step.split() 

            step = int(split[0])
            time = float(split[2])
            dt = float(split[3].replace("dt=", ""))
            CFL = float(split[5])
        
            return make_response(jsonify({"step": step,
                                      "time": time,
                                      "dt":   dt,
                                      "CFL":  CFL}), 200)
        except:
            return make_response(jsonify("internal error"), 500)
    
    
    @RESTAPI.route(approved_path + "/config", methods=["GET"])
    @check_version
    @check_auth(scopes["compute_data"])
    def nekrs_config(version):
        try:
            file = open(nekrs_logfile, "rb")
        
            file.seek(210)
            version_string = str(file.readline().decode())
            nekrs_version = version_string.split(" ")[0]
            nekrs_short_hash =  version_string.split(" ")[1].replace("(", "").replace(")\n", "")
         
            return make_response(jsonify({"nekrs version": nekrs_version,
                                      "nekrs short hash": nekrs_short_hash}), 200)
        except:
            return make_response(jsonify("internal error"), 500)


@hookimpl
def startup_parameter_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=("jumonc nekrs plugin"))
    
    parser.add_argument("--nekrs-log-path" ,
                       dest="NEKRS_LOG_PATH",
                       help=("Path and filename to the nekRS logfile to use in the plugin"),
                       default="nekrs.log",
                       type=str)

    return parser
    

@hookimpl
def evaluate_startup_parameter(parsed:argparse.Namespace) -> None:
    global nekrs_logfile
    
    nekrs_logfile = parsed.NEKRS_LOG_PATH
    

@hookimpl
def register_MPI(MPI_ID_min, MPI_ID_max):
    pass


@hookimpl
def selfcheck_is_working():
    return True