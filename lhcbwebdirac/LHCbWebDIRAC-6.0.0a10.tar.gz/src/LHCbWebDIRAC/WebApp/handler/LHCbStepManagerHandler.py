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

import six

from DIRAC import S_OK, S_ERROR, gConfig, gLogger
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.ConfigurationSystem.Client import PathFinder
from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr

from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

# TODO: Replace with
# from LHCbDIRAC.ConfigurationSystem.Client.Helpers.Resources import DEFAULT_CACHEPATH
DEFAULT_CACHEPATH = "/cvmfs/lhcb.cern.ch/lib/var/lib/softmetadata/project-platforms.json"


def getSoftVersions(name, web_names="", add=""):
    """Return list of all downloadable versions
    of specified software package.
    web_name is default to name_name
    add specify verbatim version to add to the list
    Note: It was in ProductionLib
    """

    if web_names == "":
        web_names = name

    try:
        with open(DEFAULT_CACHEPATH) as fp:
            projectMetadata = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        gLogger.exception("Failed to load projects from", DEFAULT_CACHEPATH)
        return S_ERROR("Failed to load projects from %s" % DEFAULT_CACHEPATH)

    vers = set()
    for web_name in web_names.split(","):
        platforms = projectMetadata.get(web_name.upper())
        if not platforms:
            return S_ERROR("%s is not in the list of known platforms" % web_name)
        vers |= set(platforms)

    # Remove duplicates
    allversions = tuple(vers)
    if add:
        allversions += tuple(add.split(","))

    # Sort the result, newer version will be first
    allversions = list(sorted(allversions, reverse=True))
    gLogger.debug("Application versions", allversions)
    return S_OK(allversions)


class LHCbStepManagerHandler(WebHandler):

    AUTH_PROPS = "authenticated"

    def __getArgument(self, argName, argDefValue):
        return self.get_argument(argName, None) or argDefValue

    def __getJsonArgument(self, argName, argDefValue):
        x = self.get_argument(argName, None)
        return json.loads(x) if x else argDefValue

    def __getApplications(self):
        applications = []
        csS = PathFinder.getServiceSection("ProductionManagement/ProductionRequest")
        if csS:
            applications = gConfig.getValue("%s/Applications" % csS, "")
        if not applications:
            applications = ["Gauss", "Boole", "Brunel", "DaVinci", "Moore", "LHCb"]
        else:
            applications = applications.split(", ")
        return applications

    def web_getApplications(self):
        applications = self.__getApplications()

        self.write({"success": "true", "total": len(applications), "result": [{"v": x} for x in applications]})

    def web_getAppVersions(self):
        app = self.__getArgument("app", "")
        if not app:
            return {"success": "true", "result": [], "total": 0}

        result = getSoftVersions(app)
        if not result["OK"]:
            return {"success": "false", "result": [], "total": 0, "error": result["Message"]}

        versions = result["Value"]
        return {"success": "true", "total": len(versions), "result": [{"v": x} for x in versions]}

    def web_getAppOptionsFormats(self):
        app = self.__getArgument("app", "")
        if not app:
            self.write({"success": "true", "result": [], "total": 0})
            return

        formats = Operations().getValue("Productions/StepOptionsFormat/%s" % app)
        formats = formats.split(", ") if formats is not None else []
        return {"success": "true", "total": len(formats), "result": [{"v": x} for x in formats]}

    def web_getSelectionData(self):
        callback = {
            "ApplicationName": [[x] for x in self.__getApplications()],
            "Visible": [["Yes"], ["No"]],
            "Usable": [["Yes"], ["Not ready"], ["Obsolete"]],
        }
        self.write(callback)

    def __getFilter(self):
        visibleMap = {"Yes": "Y", "No": "N"}
        sfilter = {}

        # Selector
        try:

            for selFieldName in [
                "ApplicationName",
                "ApplicationVersion",
                "Visible",
                "Usable",
                "ProcessingPass",
                "StartDate",
                "StartDate",
                "InputFileTypes",
                "OutputFileTypes",
                "Equal",
                "StepId",
            ]:
                field = self.__getJsonArgument(selFieldName, [])
                if field:
                    if selFieldName == "Equal":
                        sfilter[selFieldName] = str(field[-1])
                    elif selFieldName == "StartDate":
                        sfilter[selFieldName] = str(field[0])
                    elif selFieldName == "Visible":
                        sfilter[selFieldName] = [visibleMap.get(str(x), "Y") for x in field]
                    else:
                        sfilter[selFieldName] = [str(x) for x in field]
                        gLogger.info(f"{selFieldName} = {str(sfilter[selFieldName])}")
        except Exception as e:
            gLogger.info("__getFilter: Wrong selection: %s" % str(e))

        # Grid ordering and sorting
        sort = {"Items": "StepId", "Order": "Desc"}
        try:
            start = int(self.__getArgument("start", 0))
            limit = int(self.__getArgument("limit", 0))
            sortlist = self.__getJsonArgument("sort", [])
            if sortlist:
                sort = {"Items": str(sortlist[-1]["property"]), "Order": str(sortlist[-1]["direction"])}
        except Exception:  # fallback to defaults instead of error
            start = 0
            limit = 25
        if limit > 0:
            sfilter["StartItem"] = start
            sfilter["MaxItem"] = start + limit
        sfilter["Sort"] = sort
        gLogger.info(str(sfilter))
        return sfilter

    def __runtimeProjectsConvert(self, step):
        projects = step.get("RuntimeProjects", [])
        if projects:
            fieldNames = projects["ParameterNames"]
            projects = [dict(zip(fieldNames, y)) for y in projects["Records"]]
        step["RuntimeProjects"] = projects
        step["textRuntimeProjects"] = ",".join([f"{x.get('StepName', '')}({x.get('StepId', '')})" for x in projects])

    def __nullConvert(self, oneDict):
        for x in oneDict:
            if oneDict[x] is None:
                oneDict[x] = ""

    def web_getSteps(self):
        sfilter = self.__getFilter()

        result = BookkeepingClient().getAvailableSteps(sfilter)

        if not result["OK"]:
            return {"success": "false", "result": [], "total": 0, "error": result["Message"]}
            return

        result = result["Value"]

        if "TotalRecords" in result:
            if not (result["TotalRecords"] > 0):
                raise WErr(500, "There were no data matching your selection")
        else:
            raise WErr(500, "There were no data matching your selection")

        fields = result["ParameterNames"]
        steps = [dict(zip(fields, x)) for x in result["Records"]]
        for step in steps:
            self.__runtimeProjectsConvert(step)

        return {"success": "true", "result": steps, "total": result["TotalRecords"], "date": None}

    def web_getStep(self):
        bk = BookkeepingClient()

        StepId = 0
        try:
            StepId = int(self.__getArgument("StepId", 0))
        except Exception:
            pass  # ignore errors

        # Get Step Body
        result = bk.getAvailableSteps({"StepId": StepId})
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
            return
        result = result["Value"]
        fields = result["ParameterNames"]
        steps = [dict(zip(fields, x)) for x in result["Records"]]
        if len(steps) != 1:
            return {"success": "false", "result": [], "error": "Requested Step is not found"}
            return
        step = steps[0]

        # Get Input Files for the step
        result = bk.getStepInputFiles(StepId)
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
            return
        result = result["Value"]
        fields = ["FileType"]  # TODO: replace with result['ParameterNames']
        ift = [dict(zip(fields, x)) for x in result["Records"]]

        # Get Output Files for the step
        result = bk.getStepOutputFiles(StepId)
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
            return
        result = result["Value"]
        fields = ["FileType"]  # TODO: replace with result['ParameterNames']
        oft = [dict(zip(fields, x)) for x in result["Records"]]

        # Put everything together
        step["InputFileTypes"] = ift
        step["OutputFileTypes"] = oft
        try:
            step["textInputFileTypes"] = ",".join(["%s" % x["FileType"] for x in ift])
            step["textOutputFileTypes"] = ",".join(["%s" % x["FileType"] for x in oft])
        except Exception as e:
            return {"success": "false", "result": [], "error": "Can not convert File Types: %s" % str(e)}
        self.__runtimeProjectsConvert(step)
        self.__nullConvert(step)

        return {"success": "true", "result": step}

    def web_getRuntimeProjects(self):

        result = BookkeepingClient().getAvailableSteps({})
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
            return

        fields = result["Value"]["ParameterNames"]
        rows = [dict(zip(fields, x)) for x in result["Value"]["Records"]]
        rows = [{"id": r["StepId"], "text": f"{r['StepName']}({r['StepId']})"} for r in rows if r["Usable"] == "Yes"]
        rows.sort(key=lambda x: x["id"], reverse=True)
        return {"success": "true", "result": rows, "total": len(rows)}

    def web_getBKTags(self):
        tag = self.__getArgument("tag", "")
        if not tag:
            return {"success": "true", "result": [], "total": 0}
            return

        result = BookkeepingClient().getAvailableTagsFromSteps()
        if not result["OK"]:
            return {"success": "false", "result": [], "total": 0, "error": result["Message"]}
            return

        rows = [{"v": x[1]} for x in result["Value"]["Records"] if x[0] == tag]
        rows.sort(key=lambda x: x["v"])

        if "ONLINE" not in [list(tag.values())[0] for tag in rows]:
            rows.append({"v": "ONLINE"})
        if "fromPreviousStep" not in [list(tag.values())[0] for tag in rows]:
            rows.append({"v": "fromPreviousStep"})
        return {"success": "true", "total": len(rows), "result": rows}

    def web_getFileTypes(self):
        result = BookkeepingClient().getAvailableFileTypes()
        if not result["OK"]:
            return {"success": "false", "result": [], "total": 0, "error": result["Message"]}
            return
        rows = [dict(zip(["Name", "Description"], x)) for x in result["Value"]["Records"]]
        rows.sort(key=lambda x: x["Name"])
        return {"success": "true", "total": len(rows), "result": rows}

    def web_addFileType(self):
        name = self.__getArgument("Name", "")
        description = self.__getArgument("Description", "")
        if not name or not description:
            return {"success": "false", "result": [], "error": "File type specification is incomplete"}
            return
        result = BookkeepingClient().insertFileTypes(str(name), str(description), "ROOT")
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
        else:
            return {"success": "true", "result": []}

    __stepOrdinaryFields = [
        "StepId",
        "StepName",
        "ApplicationName",
        "ApplicationVersion",
        "SystemConfig",
        "mcTCK",
        "OptionFiles",
        "OptionsFormat",
        "DDDB",
        "CONDDB",
        "DQTag",
        "ExtraPackages",
        "Visible",
        "Usable",
        "ProcessingPass",
        "isMulticore",
    ]

    def __decodeFileTypes(self, s):
        r = []
        try:
            ftl = json.loads(s)
            for x in ftl:
                d = {}
                for y in x:
                    d[str(y)] = str(x[y])
                r.append(d)
        except Exception as e:
            gLogger.error("Cound not covert 's': %s" % str(e))
        return r

    def web_saveStep(self):
        params = {}
        for name in self.request.arguments:
            value = self.get_argument(name)
            if name in self.__stepOrdinaryFields:
                if six.PY2 and isinstance(value, unicode):  # pylint: disable=undefined-variable
                    value = str(value)
                params[name] = value
            elif name in ["InputFileTypes", "OutputFileTypes"]:
                params[name] = self.__decodeFileTypes(value)
            elif name in ["RuntimeProjectStepId"]:
                if value:
                    params["RuntimeProjects"] = [{"StepId": int(value)}]
        if "RuntimeProjects" not in params:
            params["RuntimeProjects"] = []

        if "StepId" not in params:
            params["StepId"] = "0"

        bk = BookkeepingClient()
        if params["StepId"] == "0":
            for name in ["StepId", "InputFileTypes", "OutputFileTypes", "RuntimeProjects"]:
                if name in params and not params[name]:
                    del params[name]
            params = {"Step": params}
            for name in ["InputFileTypes", "OutputFileTypes"]:
                if name in params["Step"]:
                    params[name] = params["Step"][name]
                    del params["Step"][name]
            result = bk.insertStep(params)
        else:
            result = bk.updateStep(params)
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
        else:
            return {"success": "true", "result": []}

    def web_deleteStep(self):
        StepId = 0
        try:
            StepId = int(self.__getArgument("StepId", 0))
        except Exception:
            pass
        if not StepId:
            return {"success": "false", "result": [], "error": "StepId is not correctly specified"}
            return
        result = BookkeepingClient().deleteStep(StepId)
        if not result["OK"]:
            return {"success": "false", "result": [], "error": result["Message"]}
        else:
            return {"success": "true", "result": []}
