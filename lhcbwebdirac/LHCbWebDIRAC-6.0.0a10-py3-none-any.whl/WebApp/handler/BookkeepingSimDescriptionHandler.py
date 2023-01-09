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

import six

from DIRAC import gLogger
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from WebAppDIRAC.Lib.WebHandler import WebHandler


class BookkeepingSimDescriptionHandler(WebHandler):

    AUTH_PROPS = "authenticated"

    def index(self):
        pass

    def web_getSelectionData(self):
        data = {"Visible": ["Y", "N"]}
        return data

    def web_getData(self):

        filter = {}
        limit = 0
        dir = "DESC"
        sort = "SimId"
        data = None

        try:
            for f in ["SimId", "SimDescription", "Visible"]:
                jsvalue = json.loads(self.get_argument(f, "[]"))
                v = str(jsvalue[0]) if len(jsvalue) > 0 else ""
                if v != "":
                    filter[f] = v

            start = int(self.get_argument("start", "0"))
            limit = int(self.get_argument("limit", "0"))
            if "sort" in self.request.arguments:
                data = json.loads(self.get_argument("sort"))
                sort = str(data[-1]["property"])
                dir = str(data[-1]["direction"])

        except Exception as e:
            data = {"success": "false", "error": str(e)}

        if limit > 0:
            filter["StartItem"] = start
            filter["MaxItem"] = start + limit

        if dir == "ASC":
            filter["Sort"] = {"Items": sort, "Order": "Asc"}
        else:
            filter["Sort"] = {"Items": sort, "Order": "Desc"}

        gLogger.debug("getSimulatuionConditions", str(filter))

        retVal = BookkeepingClient().getSimulationConditions(filter)

        if not retVal["OK"]:
            data = {"success": "false", "error": retVal["Message"]}
        else:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]")

            fields = retVal["Value"]["ParameterNames"]
            totalRecords = retVal["Value"]["TotalRecords"]
            rows = [dict(zip(fields, i)) for i in retVal["Value"]["Records"]]
            data = {"success": "true", "result": rows, "total": totalRecords, "date": timestamp}
        return data

    def web_editSimulation(self):
        try:
            simId = int(self.get_argument("SimId"))
        except ValueError:
            return "SimId is not a number"

        result = BookkeepingClient().getSimulationConditions({"SimId": simId})
        if not result["OK"]:
            return {"success": "false", "error": result["Message"]}
        fields = result["Value"]["ParameterNames"]
        row = [dict(zip(fields, x)) for x in result["Value"]["Records"]][0]
        return {"success": "true", "data": row}

    def web_simulationinsert(self):
        simdict = {k: self.get_argument(k) for k in self.request.arguments}
        if "SimId" in simdict:
            del simdict["SimId"]
        for i, value in simdict.items():
            if six.PY2 and isinstance(value, unicode):  # pylint: disable=undefined-variable
                simdict[i] = str(simdict[i])
            else:
                simdict[i] = simdict[i]
        gLogger.debug("Insert:", str(simdict))

        retVal = BookkeepingClient().insertSimConditions(simdict)
        result = None
        if retVal["OK"]:
            result = {"success": "true", "result": "It is registered to the database!"}
        else:
            result = {"success": "false", "error": retVal["Message"]}

        return result

    def web_simulationupdate(self):
        simdict = {k: self.get_argument(k) for k in self.request.arguments}
        for i, value in simdict.items():
            if six.PY2 and isinstance(value, unicode):  # pylint: disable=undefined-variable
                simdict[i] = str(simdict[i])
            else:
                simdict[i] = simdict[i]
        gLogger.debug("Insert:", str(simdict))
        retVal = BookkeepingClient().updateSimulationConditions(simdict)
        result = None
        if retVal["OK"]:
            result = {"success": "true", "result": "It has successfully updated!"}
        else:
            result = {"success": "false", "error": retVal["Message"]}

        return result

    def web_simulationdelete(self):
        try:
            simId = int(self.get_argument("SimId"))
        except ValueError as e:
            return {"success": "false", "error": str(e)}
        gLogger.debug("SimId:", id)
        retVal = BookkeepingClient().deleteSimulationConditions(simId)
        result = None
        if retVal["OK"]:
            result = {"success": "true", "result": "It has successfully deleted!"}
        else:
            result = {"success": "false", "error": retVal["Message"]}

        return result
