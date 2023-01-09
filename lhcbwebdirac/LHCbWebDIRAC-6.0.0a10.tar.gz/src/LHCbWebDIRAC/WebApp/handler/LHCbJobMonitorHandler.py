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

from WebAppDIRAC.WebApp.handler.JobMonitorHandler import JobMonitorHandler
from WebAppDIRAC.Lib.SessionData import SessionData


class LHCbJobMonitorHandler(JobMonitorHandler):

    AUTH_PROPS = "authenticated"

    def index(self):
        pass

    def web_standalone(self):
        self.render("JobMonitor/standalone.tpl", config_data=json.dumps(SessionData(None, None).getData()))

    def _request(self):
        req = super()._request()
        runs = list(json.loads(self.get_argument("RunNumbers", "[]")))
        if runs:
            req["runNumber"] = runs
        return req
