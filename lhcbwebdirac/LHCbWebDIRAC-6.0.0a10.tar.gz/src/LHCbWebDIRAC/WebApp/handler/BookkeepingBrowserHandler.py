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
import tornado
import sys
import datetime
import tempfile
import tarfile
import os
import shutil

from DIRAC import gLogger
from DIRAC.FrameworkSystem.Client.UserProfileClient import UserProfileClient
from DIRAC.DataManagementSystem.Utilities.DMSHelpers import DMSHelpers
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from DIRAC.FrameworkSystem.Client.ProxyManagerClient import gProxyManager

from LHCbDIRAC.BookkeepingSystem.Client.LHCB_BKKDBClient import LHCB_BKKDBClient
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr


class BookkeepingBrowserHandler(WebHandler):

    AUTH_PROPS = "authenticated"

    numberOfJobs = None
    pageNumber = None

    def index(self):
        pass

    def web_getNodes(self):

        _, querytype, tree, dataQuality = self.__parseRequest()
        node = self.get_argument("node", "")

        bk = LHCB_BKKDBClient()

        bk.setFileTypes([])

        bk.setAdvancedQueries(querytype)
        bk.setParameter(tree)
        bk.setDataQualities(dataQuality)

        retVal = bk.list(node)

        nodes = []
        if len(retVal) > 0:
            for i in retVal:
                node = {}
                node["text"] = i["name"]
                node["fullpath"] = i["fullpath"]
                node["id"] = i["fullpath"]
                node["selection"] = i["selection"] if "selection" in i else ""
                node["method"] = i["method"] if "method" in i else ""
                node["cls"] = "folder" if i["expandable"] else "file"
                if "level" in i and i["level"] == "Event types":
                    if "Description" in i:
                        node["text"] = f"{i['name']} ({i['Description']})"
                    else:
                        node["text"] = i["name"]
                if "level" in i and i["level"] == "FileTypes":
                    node["leaf"] = True
                else:
                    node["leaf"] = False if i["expandable"] else True
                if "level" in i:
                    node["level"] = i["level"]
                    node["qtip"] = i["name"]
                nodes += [node]

        return tornado.escape.json_encode(nodes)

    def web_getdataquality(self):
        bk = LHCB_BKKDBClient()
        result = bk.getAvailableDataQuality()
        if result["OK"]:
            ret = []
            for i in result["Value"]:
                checked = True if i == "OK" else False
                ret += [{"name": i, "value": checked}]
            return {"success": "true", "result": ret}
        else:
            return {"result": [], "error": result["Message"]}

    def web_getFiles(self):

        path, querytype, tree, dataQuality = self.__parseRequest()

        bk = LHCB_BKKDBClient()

        bk.setAdvancedQueries(querytype)
        bk.setParameter(tree)
        bk.setDataQualities(dataQuality)

        retVal = bk.getLimitedFiles(
            {"fullpath": path}, {"total": "0"}, self.pageNumber, self.numberOfJobs + self.pageNumber
        )

        if not retVal["OK"]:
            raise WErr.fromSERROR(retVal)
        nbrecords = retVal["Value"]["TotalRecords"]
        if nbrecords > 0:
            params = retVal["Value"]["ParameterNames"]
            records = []
            for i in retVal["Value"]["Records"]:
                k = [j if j and j != "None" else "-" for j in i]
                records += [dict(zip(params, k))]
            extras = {}
            if "Extras" in retVal["Value"]:
                extras = retVal["Value"]["Extras"]
                extras["GlobalStatistics"]["Number of Files"] = nbrecords
                size = self.__bytestr(extras["GlobalStatistics"]["Files Size"])
                extras["GlobalStatistics"]["Files Size"] = size

            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]")
            data = {
                "success": "true",
                "result": records,
                "date": timestamp,
                "total": nbrecords,
                "ExtraParameters": extras,
            }
        else:
            data = {"success": "false", "result": [], "error": "Nothing to display!"}

        return data

    ################################################################################
    @staticmethod
    def __bytestr(size, precision=1):
        """Return a string representing the greek/metric suffix of a size"""
        abbrevs = [
            (1 << 50, " PB"),
            (1 << 40, " TB"),
            (1 << 30, " GB"),
            (1 << 20, " MB"),
            (1 << 10, " kB"),
            (1, " bytes"),
        ]
        if size is None:
            return "0 bytes"
        if size == 1:
            return "1 byte"
        factor = None
        suffix = None
        for factor, suffix in abbrevs:
            if size >= factor:
                break
        float_string_split = repr(size / float(factor)).split(".")
        integer_part = float_string_split[0]
        decimal_part = float_string_split[1]
        if int(decimal_part[0:precision]):
            float_string = ".".join([integer_part, decimal_part[0:precision]])
        else:
            float_string = integer_part
        return float_string + suffix

    def __parseRequest(self):
        path = self.get_argument("fullpath", "")
        querytype = self.get_argument("type", "") == "adv"
        tree = self.get_argument("tree", "Configuration")

        dataQuality = None
        if "dataQuality" in self.request.arguments:
            dataQuality = dict(json.loads(self.get_argument("dataQuality")))
            if not dataQuality:
                dataQuality = {"OK": True}

        self.numberOfJobs = int(self.get_argument("limit", "25"))
        self.pageNumber = int(self.get_argument("start", "0"))

        return path, querytype, tree, dataQuality

    def web_getStatistics(self):

        path, querytype, tree, dataQuality = self.__parseRequest()

        bk = LHCB_BKKDBClient()

        bk.setAdvancedQueries(querytype)
        bk.setParameter(tree)
        bk.setDataQualities(dataQuality)

        retVal = bk.getLimitedInformations(self.pageNumber, self.numberOfJobs + self.pageNumber, path)
        if retVal["OK"]:
            value = {}
            value["nbfiles"] = retVal["Value"]["Number of files"]
            value["nbevents"] = self.__niceNumbers(retVal["Value"]["Number of Events"])
            value["fsize"] = self.__bytestr(retVal["Value"]["Files Size"])
            data = {"success": "true", "result": value}
        else:
            data = {"success": "false", "result": [], "error": retVal["Message"]}
        # data = {"success":"true","result":{'nbfiles':0,'nbevents':0,'fsize':0}}
        return data

    @staticmethod
    def __niceNumbers(number):
        strList = list(str(number))
        newList = [strList[max(0, i - 3) : i] for i in range(len(strList), 0, -3)]
        newList.reverse()
        finalList = []
        for i in newList:
            finalList.append(str("".join(i)))
        finalList = " ".join(map(str, finalList))
        return finalList

    def web_saveDataSet(self):

        path, querytype, tree, dataQuality = self.__parseRequest()

        bk = LHCB_BKKDBClient()

        bk.setAdvancedQueries(querytype)
        bk.setParameter(tree)
        bk.setDataQualities(dataQuality)

        fileformat = self.get_argument("format", None)
        fileName = self.get_argument("fileName", "bookkeeping_files")
        if not fileName.lower().endswith("." + fileformat.lower()):
            fileName += "." + fileformat.lower()

        if fileformat in ("py", "txt"):
            try:
                data = bk.writePythonOrJobOptions(
                    self.pageNumber, self.numberOfJobs + self.pageNumber, path, fileformat
                )
            except Exception:
                data = {"success": "false", "error": str(sys.exc_info()[1])}
        elif "bkQuery" in self.request.arguments:
            bkQuery = dict(json.loads(self.get_argument("bkQuery")))
            retVal = bk.getFilesWithMetadata(bkQuery)
            if not retVal["OK"]:
                data = {"success": "false", "error": retVal["Message"]}
            else:
                fileContent = [",".join(retVal["Value"]["ParameterNames"])]
                for record in retVal["Value"]["Records"][self.pageNumber : self.numberOfJobs + self.pageNumber]:
                    fileContent += [",".join(str(metadata) for metadata in record)]
                data = "\n".join(fileContent)
        else:
            return {"success": "false", "error": "Please provide fileName and format!"}

        self.set_header("Content-type", "text/plain")
        self.set_header("Content-Disposition", 'attachment; filename="%s' % fileName)
        self.set_header("Content-Length", len(data))
        self.set_header("Content-Transfer-Encoding", "Binary")
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.set_header("Pragma", "no-cache")
        self.set_header(
            "Expires", (datetime.datetime.utcnow() - datetime.timedelta(minutes=-10)).strftime("%d %b %Y %H:%M:%S GMT")
        )
        return data

    def web_getBookmarks(self):
        upc = UserProfileClient("Bookkeeping")
        result = upc.retrieveVar("Bookmarks")
        if result["OK"]:
            data = []
            for i in result["Value"]:
                data += [{"name": i, "value": result["Value"][i]}]
            result = {"success": "true", "result": data}
        else:
            if result["Message"].find("No data for") != -1:
                result = {"success": "true", "result": {}}
            else:
                result = {"success": "false", "error": result["Message"]}
        return result

    def web_addBookmark(self):
        title = self.get_argument("title", "")
        path = self.get_argument("path", "")

        upc = UserProfileClient("Bookkeeping")
        result = upc.retrieveVar("Bookmarks")
        data = result["Value"] if result["OK"] else {}
        if title in data:
            result = {"success": "false", "error": 'The bookmark with the title "' + title + '" is already exists'}
        else:
            data[title] = path
        result = upc.storeVar("Bookmarks", data, {"ReadAccess": "ALL"})
        if result["OK"]:
            result = {"success": "true", "result": "It successfully added to the bookmark!"}
        else:
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_deleteBookmark(self):
        title = self.get_argument("title", "")

        upc = UserProfileClient("Bookkeeping")
        result = upc.retrieveVar("Bookmarks")

        data = result["Value"] if result["OK"] else {}
        if title in data:
            del data[title]
        else:
            result = {"success": "false", "error": "Can't delete not existing bookmark: \"" + title + '"'}

        result = upc.storeVar("Bookmarks", data, {"ReadAccess": "ALL"})
        if result["OK"]:
            result = {"success": "true", "result": "It successfully deleted to the bookmark!"}
        else:
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_jobinfo(self):
        """
        For retrieving the job information for a given lfn
        """
        lfn = self.get_argument("lfn", None)

        bk = LHCB_BKKDBClient()
        result = bk.getJobInfo(lfn)

        if result is None:
            result = {"success": "false", "error": "Can not retrive job information"}
        else:
            jobinfos = [[key, value] for key, value in result.items()]
            result = {"success": "true", "result": jobinfos}
        return result

    def web_ancestors(self):
        """
        For retrieving the ancestors for a given lfn
        """
        lfn = self.get_argument("lfn", None)

        bk = LHCB_BKKDBClient()
        result = bk.getFileHistory(lfn)
        if result["OK"]:
            files = []
            nbrecords = result["Value"]["TotalRecords"]
            if nbrecords > 0:
                params = result["Value"]["ParameterNames"]
                for i in result["Value"]["Records"]:
                    k = [str(j) if j and j != "None" else "-" for j in i]
                    files += [dict(zip(params, k))]
                result = {"success": "true", "result": files}
            else:
                result = {"success": "false", "error": "No ancestors found!"}
        else:
            WErr.fromSERROR(result)
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_processingpass(self):
        """
        Retrieve the processing pass for a given dataset.
        """
        stepname = self.get_argument("stepName", None)

        bk = LHCB_BKKDBClient()

        result = bk.getProcessingPassSteps({"StepName": stepname})
        if result["OK"]:
            # convert the data to the correct format
            records = result["Value"]["Records"]
            steps = [dict([step for step in records[record]]) for record in records]
            result = {"success": "true", "result": steps}
        else:
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_stepmetadata(self):
        """
        Retrieve the processing pass for a given dataset.
        """
        bkQuery = self.get_argument("bkQuery", None)
        if bkQuery is not None:
            bkQuery = dict(json.loads(bkQuery))

        bk = LHCB_BKKDBClient()

        result = bk.getStepsMetadata(bkQuery)

        if result["OK"]:
            # convert the data to the correct format
            records = result["Value"]["Records"]
            steps = [dict([step for step in records[record]]) for record in records]
            result = {"success": "true", "result": steps}
        else:
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_conditions(self):
        """
        Retrieve the simulation or data taking conditions
        """
        bkQuery = self.get_argument("bkQuery", None)
        if bkQuery is not None:
            bkQuery = dict(json.loads(bkQuery))

        result = BookkeepingClient().getConditions(bkQuery)

        if result["OK"]:
            # convert the data to the correct format
            records = result["Value"]
            conditions = []
            if records[0]["TotalRecords"] > 0:
                paramNames = records[0]["ParameterNames"]
                for rec in records[0]["Records"]:
                    conditions = dict(zip(paramNames, rec))
                    if bkQuery["ConditionDescription"] in conditions.values():
                        condType = "sim"
                        break
            else:
                paramNames = records[1]["ParameterNames"]
                for rec in records[1]["Records"]:
                    conditions = dict(zip(paramNames, rec))
                    if bkQuery["ConditionDescription"] in conditions.values():
                        condType = "daq"
                        break
            result = {"success": "true", "result": conditions, "CondType": condType}
        else:
            result = {"success": "false", "error": result["Message"]}
        return result

    def web_runs(self):
        """
        For retrieving list of runs
        """

        bk = LHCB_BKKDBClient()
        bk.setParameter("Runlookup")

        retVal = bk.list()

        data = []
        if len(retVal) > 0:
            for i in retVal:
                data.append({"data": i["name"]})
            result = {"success": "true", "result": sorted(data, key=lambda x: x["data"])}
        else:
            result = {"success": "false", "error": "no data found"}

        return result

    def web_productions(self):
        """
        For retrieving list of runs
        """

        bk = LHCB_BKKDBClient()
        bk.setParameter("Productions")

        retVal = bk.list()

        data = []
        if len(retVal) > 0:
            for i in retVal:
                data.append({"data": i["name"]})
            result = {"success": "true", "result": sorted(data, key=lambda x: x["data"])}
        else:
            result = {"success": "false", "error": "no data found"}

        return result

    def web_t1sites(self):
        """
        Retrive the list of Tier1 sites
        """

        try:
            shortSiteNames = DMSHelpers().getShortSiteNames(withStorage=False, tier=(0, 1))
        except AttributeError:
            shortSiteNames = {
                "CERN": "LCG.CERN.cern",
                "RAL": "LCG.RAL.uk",
                "IN2P3": "LCG.IN2P3.fr",
                "GRIDKA": "LCG.GRIDKA.de",
                "NIKHEF": "LCG.NIKHEF.nl",
                "CNAF": "LCG.CNAF.it",
                "RRCKI": "LCG.RRCKI.ru",
                "PIC": "LCG.PIC.es",
            }
            # no we have to convert to the proper format
        data = []
        for shortSiteName, siteName in shortSiteNames.items():
            data.append({"Name": shortSiteName, "Value": siteName})

        return {"success": "true", "result": sorted(data, key=lambda x: x["Name"])}

    def web_createCatalog(self):
        """It is used for create pool xml catalog"""

        _, querytype, tree, dataQuality = self.__parseRequest()

        bk = LHCB_BKKDBClient()
        bk.setAdvancedQueries(querytype)
        bk.setParameter(tree)
        bk.setDataQualities(dataQuality)

        siteName = self.get_argument("SiteName")
        formatType = self.get_argument("formatType")
        fileName = self.get_argument("fileName")
        bkQuery = dict(json.loads(self.get_argument("bkQuery")))

        userName = self.getUserName()
        result = gProxyManager.downloadVOMSProxyToFile(
            self.getUserDN(), self.getUserGroup(), limited=True, requiredTimeLeft=86400, cacheTime=86400
        )

        if not result["OK"]:
            gLogger.error("Failed to set shifter proxy", result["Message"])
            return {
                "success": "false",
                "error": "Can not retrieve proxy used to generate the xml catalog! "
                "Please upload your proxy to LHCbDIRAC!",
            }

        proxyFile = result["Value"]
        os.environ["X509_USER_PROXY"] = proxyFile

        retVal = bk.getFilesWithMetadata(bkQuery)
        if not retVal["OK"]:
            return {"success": "false", "error": retVal["Message"]}

        lfns = {}
        for record in retVal["Value"]["Records"][self.pageNumber : self.numberOfJobs + self.pageNumber]:
            fileMetaDict = dict(zip(retVal["Value"]["ParameterNames"], record))
            lfns[fileMetaDict["FileName"]] = fileMetaDict
        if not lfns:
            return {"success": "false", "error": "No files found"}

        tmpdir = tempfile.mkdtemp(prefix=userName)
        catalog = f"{tmpdir}/{fileName}.xml"
        retVal = DiracLHCb().getInputDataCatalog(list(lfns), siteName, catalog, True)
        if not retVal["OK"]:
            raise WErr.fromSERROR(retVal)

        slist = retVal["Value"].get("Successful", {})
        exists = {}
        for lfn in slist.keys():
            exists[lfn] = lfns[lfn]

        if not fileName.endswith(".py"):
            fileName = f"{tmpdir}/{fileName}.py"

        kwargs = dict(catalog=catalog, dataset=bkQuery)
        if formatType.lower() == "pfn":
            kwargs = dict(savedType=None, savePfn=slist)
        elif formatType.lower() != "lfn":
            raise NotImplementedError(formatType)
        bk.writeJobOptions(exists, fileName, **kwargs)

        tarFile = "%s.tar.gz" % tmpdir
        with tarfile.open(tarFile, "w:gz") as tar:
            tar.add(tmpdir, arcname=userName)

        with open(tarFile, "rb") as tar:
            data = tar.read()
        shutil.rmtree(tmpdir)
        shutil.os.remove(tarFile)
        del os.environ["X509_USER_PROXY"]
        shutil.os.remove(proxyFile)

        self.set_header("Content-type", "application/gzip")
        self.set_header("Content-Disposition", 'attachment; filename="%s"' % tarFile)
        self.set_header("Content-Length", len(data))
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.set_header("Pragma", "no-cache")
        return data
