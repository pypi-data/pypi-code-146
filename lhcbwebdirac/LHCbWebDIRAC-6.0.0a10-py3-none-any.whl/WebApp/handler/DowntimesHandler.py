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
""" WebApp handler for Downtimes WebApp
"""

import json
from datetime import datetime

import tornado
from DIRAC import gLogger
from DIRAC.ResourceStatusSystem.Client.PublisherClient import PublisherClient
from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr


class DowntimesHandler(WebHandler):

    AUTH_PROPS = "authenticated"

    def web_getSelectionData(self):
        callback = {"name": set(), "severity": set(), "sites": set()}

        gLogger.info("Arguments to web_getSelectionData", repr(self.request.arguments))

        downtimes = PublisherClient().getCachedDowntimes(None, None, None, None)

        if downtimes["OK"]:

            dtList = [dict(zip(downtimes["Columns"], dt)) for dt in downtimes["Value"]]

            for dt in dtList:

                callback["name"].add(dt["Name"])
                callback["severity"].add(dt["Severity"])

        sites = PublisherClient().getSites()
        if sites["OK"]:

            callback["site"] = sites["Value"]

        for key, value in callback.items():

            callback[key] = [[item] for item in list(value)]
            # callback[key].sort()
            callback[key] = [["All"]] + callback[key]

        callback["view"] = [["tabular"], ["availability"]]

        return callback

    def web_getDowntimesData(self):
        requestParams = self.__requestParams()
        gLogger.info(requestParams)

        retVal = PublisherClient().getSitesResources(list(requestParams["site"]))

        sitesResources = ""
        if not retVal["OK"]:
            raise WErr.fromSERROR(retVal)
        else:
            sitesResources = retVal["Value"]

        names = []
        if requestParams["site"]:

            if names is None:
                names = []

            for _site, resources in sitesResources.items():

                names += resources["ces"]
                names += resources["ses"]

        downtimes = PublisherClient().getCachedDowntimes(None, None, names, list(requestParams["severity"]))
        if not downtimes["OK"]:
            raise WErr.fromSERROR(downtimes)

        dtList = [dict(zip(downtimes["Columns"], dt)) for dt in downtimes["Value"]]

        for dt in dtList:

            dt["Site"] = "Unknown"

            for site, resources in sitesResources.items():
                if dt["Name"] in resources["ces"] + resources["ses"]:
                    dt["Site"] = site
                    break

            dt["StartDate"] = str(dt["StartDate"])
            dt["EndDate"] = str(dt["EndDate"])

        return {"success": "true", "result": dtList, "total": len(dtList)}

    def __requestParams(self):
        """
        We receive the request and we parse it, in this case, we are doing nothing,
        but it can be certainly more complex.
        """
        gLogger.always("!!!  PARAMS: ", repr(self.request.arguments))

        responseParams = {}

        for key in ("name", "severity", "site"):
            value = self.get_argument(key, None)
            if value:
                responseParams[key] = list(json.loads(value))
            else:
                responseParams[key] = []

        try:
            startDate = f"{self.get_argument('startDate')} {self.get_argument('startTime')}"
            startDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M")
        except (tornado.web.MissingArgumentError, ValueError):
            startDate = datetime.utcnow()
        responseParams["startDate"] = startDate

        try:
            endDate = f"{self.get_argument('endDate')} {self.get_argument('endTime')}"
            endDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M")
        except (tornado.web.MissingArgumentError, ValueError):
            endDate = datetime.utcnow()
        responseParams["endDate"] = datetime.utcnow()

        return responseParams
