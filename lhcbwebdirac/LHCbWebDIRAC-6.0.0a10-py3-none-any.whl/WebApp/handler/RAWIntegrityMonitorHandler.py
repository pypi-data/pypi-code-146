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
from datetime import datetime, timedelta
from time import time

from DIRAC import gLogger
from DIRAC.Core.Utilities.Graphs.Palette import Palette
from DIRAC.Core.DISET.RPCClient import RPCClient

from WebAppDIRAC.Lib.WebHandler import WebHandler


class RAWIntegrityMonitorHandler(WebHandler):

    AUTH_PROPS = "authenticated"

    numberOfFiles = 25
    pageNumber = 0
    globalSort = [["SubmitTime", "DESC"]]

    def index(self):
        pass

    def web_getSelectionData(self):
        callback = {}
        now = datetime.today()
        mon = timedelta(days=30)
        sd = now - mon
        tmp = {}
        ttt = str(sd.isoformat())
        gLogger.info(" - T I M E - ", ttt)
        tmp["startDate"] = sd.isoformat()
        tmp["startTime"] = sd.isoformat()
        callback["extra"] = tmp
        if len(self.request.arguments) > 0:
            tmp = {}
            for i in self.request.arguments:
                tmp[i] = self.get_arguments(i)
            callback["extra"] = tmp
        #####################################################################
        # This is the part that obtains the selections from the integrity db.
        RPC = RPCClient("DataManagement/RAWIntegrity")

        result = RPC.getFileSelections()

        if result["OK"]:
            if len(result["Value"]) > 0:
                result = result["Value"]
                for key, value in result.items():
                    if len(value) > 3:
                        value = ["All"] + value
                    key = key.lower()
                    value = map(lambda x: [x], value)
                    callback[key] = value
        else:
            callback = {"success": "false", "error": result["Message"]}
        gLogger.info(" - callback - ", callback)
        return callback

    def __request(self):
        req = {}
        lfns = list(json.loads(self.get_argument("lfn", "[]")))
        if lfns:
            req["lfn"] = lfns

        self.numberOfFiles = int(self.get_argument("limit", "25"))
        self.pageNumber = int(self.get_argument("start", "0"))

        #######################################################################
        # For the selection boxes only
        if "status" in self.request.arguments:
            req["Status"] = list(json.loads(self.get_argument("status")))

        if "storageelement" in self.request.arguments:
            if str(self.request.params["storageelement"]) != "All":
                req["StorageElement"] = list(json.loads(self.get_argument("storageelement")))
        #######################################################################
        # For the start time selection
        if "startDate" in self.request.arguments and len(self.get_argument("startDate")) > 0:
            if "startTime" in self.request.arguments and len(self.get_argument("startTime")) > 0:
                req["FromDate"] = str(self.get_argument("startDate") + " " + self.get_argument("startTime"))
            else:
                req["FromDate"] = self.get_argument("startDate")

        if "endDate" in self.request.arguments and len(self.get_argument("endDate")) > 0:
            if "endTime" in self.request.arguments and len(self.get_argument("endTime")) > 0:
                req["ToDate"] = str(self.get_argument("endDate") + " " + self.get_argument("endTime"))
            else:
                req["ToDate"] = self.get_argument("endDate")

        #######################################################################
        # The global sort of the data
        if "sort" in self.request.arguments:
            sort = json.loads(self.get_argument("sort"))
            if len(sort) > 0:
                self.globalSort = []
                for i in sort:
                    self.globalSort += [[i["property"], i["direction"]]]
        else:
            self.globalSort = [["SubmitTime", "DESC"]]

        gLogger.info("REQUEST:", req)
        return req

    def web_getloggingInfo(self):
        req = self.__request()
        gLogger.debug("getloggingInfo" + str(req))

        RPC = RPCClient("DataManagement/DataLogging")
        result = RPC.getFileLoggingInfo(str(req["lfn"][0]))

        if not result["OK"]:
            return {"success": "false", "error": result["Message"]}
        result = result["Value"]
        if not result:
            return {"success": "false", "result": "", "error": "No logging information found for LFN"}
        callback = []
        for i in result:
            callback.append([i[0], i[1], i[2], i[3]])
        return {"success": "true", "result": callback}

    def web_getStatisticsData(self):
        paletteColor = Palette()
        gLogger.debug("Params:" + str(self.request.arguments))

        req = self.__request()
        selector = self.get_argument("statsField")

        if selector == "Status":
            selector = "status"
        if selector == "Storage Element":
            selector = "storageelement"

        RPC = RPCClient("DataManagement/RAWIntegrity")

        result = RPC.getStatistics(selector, req)
        gLogger.info(" - result - :", result)
        callback = {}

        if result["OK"]:
            callback = []
            result = result["Value"]
            keylist = sorted(result.keys())

            for key in keylist:
                callback.append({"key": key, "value": result[key], "code": "", "color": paletteColor.getColor(key)})
            callback = {"success": "true", "result": callback}
        else:
            callback = {"success": "false", "error": result["Message"]}

        gLogger.debug("retValue" + str(callback))
        return callback

    #####################################################################
    #
    # Handles displaying results
    #
    def web_getRawIntegrityData(self):
        gLogger.info(" -- SUBMIT --")
        pagestart = time()
        RPC = RPCClient("DataManagement/RAWIntegrity")
        result = self.__request()
        result = RPC.getFilesSummaryWeb(result, self.globalSort, self.pageNumber, self.numberOfFiles)
        if result["OK"]:
            result = result["Value"]

            if "TotalRecords" in result:
                if result["TotalRecords"] > 0:
                    if "ParameterNames" in result and "Records" in result:
                        if len(result["ParameterNames"]) > 0:
                            if len(result["Records"]) > 0:
                                callback = []
                                jobs = result["Records"]
                                head = result["ParameterNames"]
                                headLength = len(head)
                                for i in jobs:
                                    tmp = {}
                                    for j in range(0, headLength):
                                        tmp[head[j]] = i[j]
                                    callback.append(tmp)
                                total = result["TotalRecords"]
                                if "Extras" in result:
                                    extra = result["Extras"]
                                    callback = {"success": "true", "result": callback, "total": total, "extra": extra}
                                else:
                                    callback = {"success": "true", "result": callback, "total": total}
                                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]")
                                callback["date"] = timestamp
                            else:
                                callback = {"success": "false", "result": "", "error": "There are no data to display"}
                        else:
                            callback = {"success": "false", "result": "", "error": "ParameterNames field is missing"}
                    else:
                        callback = {"success": "false", "result": "", "error": "Data structure is corrupted"}
                else:
                    callback = {"success": "false", "result": "", "error": "There were no data matching your selection"}
            else:
                callback = {"success": "false", "result": "", "error": "Data structure is corrupted"}
        else:
            callback = {"success": "false", "error": result["Message"]}
        gLogger.info("\033[0;31mJOB SUBMIT REQUEST:\033[0m %s" % (time() - pagestart))
        return callback
