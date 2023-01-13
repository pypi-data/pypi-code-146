"""
The handlers package of jumonc provides the handlers to interact with jumonc using the REST-API.

The REST API is documented with openapi, and rendered well by gitlab on:
https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/blob/CI_fixes/doc/REST_API/openapi.yaml
"""
import logging
import subprocess # nosec B404
import time

from flask import jsonify
from flask import make_response
from flask import Response

from jumonc import settings
from jumonc._version import __version__
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers.base import RESTAPI
from jumonc.models.cache import helper as db_helper
from jumonc.tasks import mpi_helper
from jumonc.tasks import mpibase
from jumonc.tasks import mpiroot


logger = logging.getLogger(__name__)


@RESTAPI.route("/ping", methods=["GET"])
def ping() -> str:
    return "PONG.\n"



@RESTAPI.route("/stop")
@check_auth(scopes["full"])
def stopjumonc() -> Response:
    logger.info("Stopping jumonc")
    db_helper.stop()
    
    logger.debug("Finalizing MPI")
    mpiroot.sendCommand(mpi_helper.build_mpi_command(mpi_id = mpibase.stop_handlers_id, 
                                                     resultids = [], 
                                                     kwargs = {}))
    
    logger.debug("stopping flask")
    
    time.sleep(1)
    with subprocess.Popen("netstat -tulnp | grep LISTEN | grep " + str(settings.REST_API_PORT) + " 2>/dev/null",
                          stdout=subprocess.PIPE,
                          shell=True) as p: # nosec B602
        pid = str(p.communicate()[0]).split("/", maxsplit=1)[0][-5:]
        with subprocess.Popen("kill -9 " + pid + " 2>/dev/null", stdout=subprocess.PIPE, shell=True) as p: # nosec B602
            pass
    

    #func = request.environ.get('werkzeug.server.shutdown')
    #if func is not None:
    #    func()

    return make_response(jsonify("Stopping server and shutting down jumonc\n"), 200)


@RESTAPI.route("/version", methods=["GET"])
def version() -> Response:
    response_body = {"jumonc_version": __version__}
    return make_response(jsonify(response_body), 200)


@RESTAPI.route("/all_links", methods=["GET"])
@check_auth(scopes["full"])
def allLinks() -> Response:
    return make_response(jsonify(RESTAPI.url_map), 200)
