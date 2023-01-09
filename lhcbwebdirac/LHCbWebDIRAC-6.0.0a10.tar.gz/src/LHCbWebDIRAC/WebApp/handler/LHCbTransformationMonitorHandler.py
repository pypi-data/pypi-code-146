###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
from datetime import datetime

from DIRAC import gLogger

from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

from WebAppDIRAC.WebApp.handler.TransformationMonitorHandler import TransformationMonitorHandler
from WebAppDIRAC.Lib.WebHandler import WErr
from WebAppDIRAC.Lib.SessionData import SessionData


class LHCbTransformationMonitorHandler(TransformationMonitorHandler):

    AUTH_PROPS = "authenticated"

    def index(self):
        pass

    def web_standalone(self):
        self.render(
            "TransformationMonitorHandler/standalone.tpl", config_data=json.dumps(SessionData(None, None).getData())
        )

    ################################################################################
    def _TransformationMonitorHandler__dataQuery(self, prodid):
        callback = {}

        tsClient = TransformationClient()
        res = tsClient.getBookkeepingQuery(prodid)
        gLogger.info("-= #######", res)
        if not res["OK"]:
            callback = {"success": "false", "error": res["Message"]}
        else:
            result = res["Value"]
            back = []
            for i in sorted(result.keys(), reverse=False):
                back.append([i, result[i]])
            callback = {"success": "true", "result": back}
        return callback

    ################################################################################
    def web_showRunStatus(self):
        callback = {}
        start = int(self.get_argument("start"))
        limit = int(self.get_argument("limit"))

        try:
            id = int(self.get_argument("TransformationId"))
        except KeyError as excp:
            raise WErr(400, "Missing %s" % excp)

        tsClient = TransformationClient()
        result = tsClient.getTransformationRunsSummaryWeb(
            {"TransformationID": id}, [["RunNumber", "DESC"]], start, limit
        )

        if not result["OK"]:
            callback = {"success": "false", "error": result["Message"]}
        else:
            result = result["Value"]
            if "TotalRecords" in result and result["TotalRecords"] > 0:
                total = result["TotalRecords"]
                if "Extras" in result:
                    extra = result["Extras"]
                if "ParameterNames" in result and "Records" in result:
                    head = result["ParameterNames"]
                    if len(head) > 0:
                        headLength = len(head)
                        if len(result["Records"]) > 0:
                            callback = []
                            jobs = result["Records"]
                            for i in jobs:
                                if len(i) != headLength:
                                    gLogger.info("Faulty record: %s" % i)
                                    callback = {
                                        "success": "false",
                                        "result": callback,
                                        "total": total,
                                        "error": "One of the records in service response is corrupted",
                                    }
                                    return callback
                                tmp = {}
                                for j in range(0, headLength):
                                    tmp[head[j]] = i[j]
                                callback.append(tmp)
                            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]")
                            if extra:
                                callback = {
                                    "success": "true",
                                    "result": callback,
                                    "total": total,
                                    "extra": extra,
                                    "date": timestamp,
                                }
                            else:
                                callback = {"success": "true", "result": callback, "total": total, "date": timestamp}
                        else:
                            callback = {"success": "false", "result": "", "error": "There are no data to display"}
                    else:
                        callback = {"success": "false", "result": "", "error": "ParameterNames field is undefined"}
                else:
                    callback = {"success": "false", "result": "", "error": "Data structure is corrupted"}
            else:
                callback = {"success": "false", "result": "", "error": "There were no data matching your selection"}
        return callback

    ################################################################################
    def web_setRunStatus(self):
        callback = {}
        transID = int(self.get_argument("TransformationId"))
        runID = int(self.get_argument("RunNumber"))
        status = self.get_argument("Status")

        gLogger.info(f"\033[0;31m setTransformationRunStatus({transID}, {runID}, {status}) \033[0m")
        tsClient = TransformationClient()
        result = result = tsClient.setTransformationRunStatus(transID, runID, status)
        if result["OK"]:
            callback = {"success": True, "result": True}
        else:
            callback = {"success": "false", "error": result["Message"]}
        return callback

    def _prepareSearchParameters(self, *args, **kwargs):
        req = super()._prepareSearchParameters(*args, **kwargs)
        hotFlag = json.loads(self.get_argument("Hot", "[false]"))[-1]
        if hotFlag:
            req["Hot"] = hotFlag

        return req

    def web_changeHotFlag(self):
        data = self.getSessionData()
        isAuth = False
        if "JobAdministrator" in data.get("user", {}).get("properties", {}):
            isAuth = True
        if not isAuth:
            raise WErr(500, "You are not authorized to change the hot flag (only lhcb_prmgr can change it)!!")

        hotFlag = json.loads(self.get_argument("Hot"))
        prod = int(self.get_argument("Production"))

        tsClient = TransformationClient()

        retVal = tsClient.setHotFlag(prod, hotFlag)
        if not retVal["OK"]:
            raise WErr.fromSERROR(retVal)
        return {"success": True, "result": prod}
