import io
import logging
import os

from datetime import datetime, timedelta
import json

import ujson
import yaml
import requests
import ujson as json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger, RequestsHTTPTransport
import pandas as pd

requests_logger.setLevel(logging.WARNING)


class GSDBS:
    def __init__(self, creadPath, configstr=""):
        self.version = "0.2.6-27"
        self._logger = logging.getLogger(__name__)
        self.credentials = None
        self.accessToken = None
        self.dtablename = None
        self.superdtablename = None
        self.sriBuildInfo = list()
        self.data = pd.DataFrame()
        self.statement = None
        self.creadPath = creadPath
        self.configstr = configstr
        self.readCredentials()
        self.cookiejar = {}
        self.getTokenFromApi()
        self.CGSResponseCode = {}
        self.setupCGSResponseCodes()
        self.debugModus = False
        self.querybuffer = ''
        return

    def setDebugModus(self, debugModus):
        self.debugModus = debugModus

    def readCredentials(self):
        try:
            self._logger.info(f'GS-DBMS Python client version: {self.version}')

            if self.configstr == "":
                f = open(self.creadPath + "/gscred.yml", "r")
                cred = f.read()
                f.close()
                self.credentials = yaml.safe_load(cred)['cred']
            else:
                self.credentials = yaml.safe_load(self.configstr)['cred']

            if (('graphqlapiurl' not in self.credentials.keys())
                    or ('token' not in self.credentials.keys())):
                raise ValueError('error: credentials')
            return
        except Exception as e:
            self._logger.exception(e)
        return

    def getAccessToken(self):
        return self.accessToken["access_token"]

    def getTokenFromApi(self):
        try:
            data = {'username': self.credentials['cnode'],
                    'password': self.credentials['token']}
            self.getAccessTokenFromApi(data)
        except Exception as e:
            self._logger.exception(e)
            os._exit(0)
        return

    def getAccessTokenFromApi(self, data):
        session = requests.session()
        refresh_token_response = session.post(
            self.credentials['baseurl'] + self.credentials['login'],
            json=data,
            headers={'Content-Type': 'application/json'})
        self.accessToken = refresh_token_response.text
        if refresh_token_response.status_code > 299:
            self._logger.warn("Error: Login failed with " + str(refresh_token_response.status_code))
            os._exit(0)

        self.cookiejar = session.cookies
        session.close()

        if 'error' in self.accessToken:
            self._logger.exception("could not authenticate")

    def setupCGSResponseCodes(self):
        self.CGSResponseCode['0'] = 'SUCCESS'
        self.CGSResponseCode['-1'] = 'MISSING (SUPER) DTABLE NAME'
        self.CGSResponseCode['-2'] = 'MISSING DATA LINK LIST'
        self.CGSResponseCode['-3'] = 'MISSING SRI BUILD INFO'
        self.CGSResponseCode['-4'] = 'MISSING DATA'
        self.CGSResponseCode['-5'] = 'MISSING DATALINK FOR SRI BUILD INFO in DATAFRAME'
        self.CGSResponseCode['-6'] = 'QUERY RESULT IS NULL'
        self.CGSResponseCode['-7'] = 'DATAFRAME DATATYPE DOESN\'T MATCHES DTABEL DATATYPE'
        self.CGSResponseCode['-8'] = 'EXECUTION FAILED'
        self.CGSResponseCode['-9'] = 'MISSING STATEMENT TO EXECUTE'
        self.CGSResponseCode['-10'] = 'STATEMENT ERROR'
        self.CGSResponseCode['-11'] = 'ERROR IN DATASCHEMA'
        self.CGSResponseCode['-12'] = 'TYPE ERROR'
        self.CGSResponseCode['-13'] = 'Missing DTABLE'
        self.CGSResponseCode['-14'] = 'Missing DTABLE SCHEMA'
        self.CGSResponseCode['-15'] = 'Missing QUERY'

    def setDTableName(self, dTableName, superDTableName="DTABLE"):
        if dTableName is None or superDTableName is None:
            self.dtablename = None
            self.superdtablename = None
            return -1;
        if (not (isinstance(dTableName, str) and isinstance(superDTableName, str))):
            self.dtablename = None
            self.superdtablename = None
            return -1;
        self.dtablename = dTableName
        self.superdtablename = superDTableName
        return 0

    def clearDTableName(self):
        self.dtablename = None
        self.superdtablename = None
        return 0

    def checkDTableName(self):
        if self.dtablename is None or self.superdtablename is None:
            return -1
        return 0

    def setSriBuildInfo(self, dataLinkList):
        if (dataLinkList is None):
            self.sriBuildInfo = None
            return -2;
        if not isinstance(dataLinkList, list):
            self.sriBuildInfo = None
            return -2
        if (len(dataLinkList) == 0):
            self.sriBuildInfo = None
            return -2
        self.sriBuildInfo = dataLinkList
        return 0

    def getSriBuildInfo(self):
        buidInfo = str()
        for dl in self.sriBuildInfo:
            if len(buidInfo) == 0:
                buidInfo += f'${{{dl}}}'
            else:
                buidInfo += f'-${{{dl}}}'
        return buidInfo

    def clearSriBuildInfo(self):
        self.sriBuildInfo = None
        return 0

    def checkSriBuildInfo(self):
        if (self.sriBuildInfo is None):
            return -3
        if (self.data is None):
            return -4
        for dl in self.sriBuildInfo:
            if dl not in self.data.columns:
                return -5
        return 0

    def setData(self, data):
        if data is None:
            self.data = None
            return -4
        if not isinstance(data, pd.DataFrame):
            self.data == None
            return -4
        if len(data.index) == 0:
            self.data = None
            return -4
        self.data = data
        return 0

    def getGSDBSType(self, pyType):
        if pyType == "object":
            return "STRING"
        elif pyType == "str":
            return "STRING"
        elif pyType == "int":
            return "INTEGER"
        elif pyType == "integer":
            return "INTEGER"
        elif pyType == "int32":
            return "INTEGER"
        elif pyType == "int64":
            return "LONG"
        elif pyType == "float":
            return "FLOAT"
        elif pyType == "float32":
            return "FLOAT"
        elif pyType == "float64":
            return "DOUBLE"
        elif pyType == "bool":
            return "BOOLEAN"
        elif pyType == "datetime":
            return "DATETIME"
        elif pyType == "datetime64":
            return "DATETIME"
        elif pyType == "datetime64[ns]":
            return "DATETIME"
        else:
            return None

    def getDataSchema(self):
        s = str()
        for col in self.data:
            gsDbsType = self.getGSDBSType(str(self.data.dtypes[col]))
            if gsDbsType == None:
                return f"""type error: column {gsDbsType} """
            s += f"""\t\t\t{{alias: "{col}", locale: DE, superPropertyURI: DYNAMIC_DATALINK, DataType: {gsDbsType}}},\n"""
        if len(s) > 0:
            s = s[:-2]
        return s

    def getData(self):
        datalist = list()
        self.data = self.data.astype(str)
        datalist = [self.data.columns.tolist()] + self.flatten(self.data.values.tolist())
        return json.dumps(datalist)

    # s = str()
    # s += f"\t\t\t["
    # for col in self.data:
    #     s += f""""{col}", """
    # s = s[:-2]
    # if len(self.data) > 0:
    #     s += "], \n"
    # else:
    #     s += "]\n"
    #
    # for i in range(len(self.data)):
    #     s += f"\t\t\t["
    #     for col in self.data:
    #
    #         s = str(self.data.loc[i, col])
    #         if s is not None:
    #             if "\"" in s:
    #                 s = s.replace("\"", "'")
    #         s += f""""{s}", """
    #
    #     s = s[:-2]
    #     if i < (len(self.data) - 1):
    #         s += "], \n"
    #     else:
    #         s += "]\n"
    # return s

    def flatten(self, t):
        return [item for item in t]

    def clearData(self):
        self.data = None
        return 0

    def checkData(self):
        if (self.data is None):
            return -4
        for col in self.data:
            gsDbsType = self.getGSDBSType(str(self.data.dtypes[col]))
            if gsDbsType == None:
                return f"""type error: column{gsDbsType} """
        return 0

    def generateMutationStatement(self):
        buildInfo = self.getSriBuildInfo()
        if buildInfo == None:
            return
        dataSchema = self.getDataSchema()
        if dataSchema == None:
            return
        self.statement = \
            f"""mutation {{\n\taddDTable(dtablename: "{self.dtablename}", \n\t\tsuperDTable: [{self.superdtablename}], \n\t\tsriBuildInfo: "{buildInfo}", \n\t\tdataLinks: [\n{dataSchema}\n\t\t], \n\t\tdata: \n{self.getData()}\t\t\n\t)\n}}"""
        return

    async def asyncSchemaCheck(self):
        # check mutation content
        rc = self.checkDTableName()
        if rc != 0: return rc
        rc = self.checkData()
        if rc != 0: return rc
        rc = self.checkSriBuildInfo()
        if rc != 0: return rc

        iQuery = await self.asyncSchemaQuery(self.dtablename)
        if iQuery == None: return -6

        if iQuery['__type'] == None: return 0  # dtable doesn't exist, do what you want
        rc = self.schemaLinkCheck(iQuery)
        return rc

    def schemaCheck(self):
        # check mutation content
        rc = self.checkDTableName()
        if rc != 0: return rc
        rc = self.checkData()
        if rc != 0: return rc
        rc = self.checkSriBuildInfo()
        if rc != 0: return rc

        iQuery = self.schemaQuery(self.dtablename)
        if iQuery == None: return -6

        if iQuery['__type'] == None: return 0  # dtable doesn't exist, do what you want
        rc = self.schemaLinkCheck(iQuery)
        return rc

    def schemaLinkCheck(self, iQuery):
        schema = dict(iQuery['__type'])
        schemaName = schema["name"]
        schemaLinks = schema["fields"]

        for col in self.data:
            dfType = self.getGSDBSType(str(self.data.dtypes[col]))
            linkType = self.getLinkType(schemaLinks, col)
            if dfType.upper() != linkType.upper():
                self._logger.error('ERROR: dataframe datatype ', dfType, ' doesnt\' matches dTable datatype', linkType)
                return -7
        return 0

    def getLinkType(self, schemaLinks, linkName):
        if linkName == None:
            return -1
        for link in schemaLinks:
            if link['name'] == linkName:
                return link['type']['name']
        return None

    async def asyncAddDObject(self, dtablename, sribuildinfo, dataframe, superdtablename="DTABLE", schemaCheck=True):
        self.superdtablename = superdtablename
        rc = self.setDTableName(dtablename)
        if rc != 0: return rc
        rc = self.setSriBuildInfo(sribuildinfo)
        if rc != 0: return rc
        rc = self.setData(dataframe)
        if rc != 0: return rc
        if schemaCheck == True:
            rc = await self.asyncSchemaCheck()
            if rc != 0: return rc
        self.generateMutationStatement()
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = await self.asyncExecuteStatement()
        except Exception as e:
            self._logger.exception(e)
            return e
        return rc

    def addDObject(self, dtablename, sribuildinfo, dataframe, superdtablename="DTABLE", schemaCheck=True):
        self.superdtablename = superdtablename
        rc = self.setDTableName(dtablename)
        if rc != 0: return rc
        rc = self.setSriBuildInfo(sribuildinfo)
        if rc != 0: return rc
        rc = self.setData(dataframe)
        if rc != 0: return rc
        if schemaCheck == True:
            rc = self.schemaCheck()
            if rc != 0: return rc
        self.generateMutationStatement()
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = self.executeStatement()
        except Exception as e:
            self._logger.exception(e)
            return e
        return rc

    def addDObjectXSV(self, data):
        self.statement = self.generateStatement(data)
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = self.executeStatement()
        except Exception as e:
            self._logger.exception(e)
            return e

    def addDObjectv2XSV(self, data):
        self.statement = self.generateV2Statement(data)
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = self.executeStatement()
        except Exception as e:
            self._logger.exception(e)
            return e

    def updateDObjectXSV(self, data):
        self.statement = self.generateXsvUpdateStatement(data)
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = self.executeStatement()
        except Exception as e:
            self._logger.exception(e)
            return e

    def deleteDDatalinkXSV(self, data):
        self.statement = self.generateXsvDeleteStatement(data)
        if self.debugModus:
            self._logger.debug(self.statement)
        try:
            rc = self.executeStatement()
        except Exception as e:
            self._logger.exception(e)
            return e

    async def asyncSchemaQuery(self, dtablename):
        statement = "{ __type(name: \"" + dtablename + "\") {name fields { name type { name kind } } } }"

        try:
            result = await self.asyncExecuteStatement(statement)
        except Exception as e:
            self._logger.exception(e)
            return e

        return result

    def schemaQuery(self, dtablename):
        statement = "{ __type(name: \"" + dtablename + "\") {name fields { name type { name kind } } } }"

        try:
            result = self.executeStatement(statement)
        except Exception as e:
            self._logger.exception(e)
            return e

        return result

    async def asyncExecuteStatement(self, statement=None):
        if statement == None:
            if self.statement == None: return -9
            query = gql(self.statement)
        else:
            query = gql(statement)

        try:
            result = await self.prepareClient().execute_async(query)

        except Exception as e:
            os._exit(0)
            if "invalid_token" in str(e):
                self.refreshToken()
                result = await self.asyncExecuteStatement(statement)
            else:
                return e

    def executeStatement(self, statement=None):
        if statement == None:
            if self.statement == None: return -9
            query = gql(self.statement)
        else:
            query = gql(statement)
        try:
            return self.prepareClient().execute(query)
        except Exception as e:
            logging.exception(e)
            os._exit(0)

    def executeStatementSync(self, statement=None):
        if statement == None:
            if self.statement == None: return -9
            query = gql(self.statement)
        else:
            query = gql(statement)
        try:
            return self.prepareClientSync().execute(query)
        except Exception as e:
            logging.exception(e)
            os._exit(0)

    def prepareClient(self):
        return Client(
            transport=AIOHTTPTransport(url=self.credentials["baseurl"] + self.credentials['graphqlapiurl'],
                                       cookies=self.cookiejar), execute_timeout=40)

    def prepareClientSync(self):
        return Client(
            transport=RequestsHTTPTransport(url=self.credentials["baseurl"] + self.credentials['graphqlapiurl'],
                                            cookies=self.cookiejar), execute_timeout=40)

    async def asyncDropDTable(self, dtablename):
        statement = f"""mutation {{\n\tdropDTable(dtablename: {dtablename})\n}}"""
        result = await self.asyncExecuteStatement(statement)
        return result

    def dropDTable(self, dtablename):
        statement = f"""mutation {{\n\tdropDTable(dtablename: {dtablename})\n}}"""
        result = self.executeStatement(statement)
        return result

    def getDTableFullQuery(self, dtablename):
        try:
            self.querybuffer = 'query {\n'
            self.querybuffer += dtablename + '\n'
            self.getDTableQuery(dtablename)
            self.querybuffer += '}'
        except Exception as e:
            return e
        return self.querybuffer

    def getDTableQuery(self, dtablename):
        statement = f"""{{
              __type(name: \"{dtablename}\") {{
                name
                fields {{
                  name
                  type {{
                    name
                    kind
                    ofType {{
                      name
                      kind
                    }}
                  }}
                }}
              }}
            }}"""
        result = self.executeStatement(statement)
        if result == None:
            raise ValueError('MISSING DTABLE')

        schema = dict(result['__type'])
        if schema == None:
            raise ValueError('MISSING DTABLE SCHEMA')

        schemaName = schema["name"]

        self.querybuffer += '{\n'
        for field in schema["fields"]:
            if field['name'] == 'episodes':
                continue
            if field['name'] == 'dynamic_snapshot_timestamp':
                continue
            if field['name'] == 'totalrowcount':
                continue
            self.querybuffer += field['name'] + "\n"
            if field['type'] != None:
                if field['type']['ofType'] != None:
                    self.getDTableQuery(field['type']['ofType']['name'])
        self.querybuffer += '}\n'
        return 0

    def getForeignDTableName(self, dtablename, foreignLinkName):
        statement = f"""{{
              __type(name: \"{dtablename}\") {{
                name
                fields {{
                  name
                  type {{
                    name
                    kind
                    ofType {{
                      name
                      kind
                    }}
                  }}
                }}
              }}
            }}"""
        result = self.executeStatement(statement)
        if result == None:
            raise ValueError('MISSING DTABLE')
        schema = dict(result['__type'])
        if schema == None:
            raise ValueError('MISSING DTABLE SCHEMA')
        schemaName = schema["name"]

        for field in schema["fields"]:
            if field['name'] == foreignLinkName:
                if field['type'] != None:
                    if field['type']['ofType'] != None:
                        return field['type']['ofType']['name']
        return None

    def getFileFromCloud(self, filename):
        filename = filename.replace("/", "$")
        storageURL = self.credentials["baseurl"] + self.credentials['storageurl'] + "/file/" + filename
        # headers = {'Authorization': 'Bearer ' + self.accessToken['access_token']}
        resp = requests.get(storageURL, cookies=self.cookiejar)
        buf = io.BytesIO(resp.content)
        return buf

    def saveFileInCloud(self, filenamewithpath, fileasbytesio, fileformat):
        storageURL = self.credentials["baseurl"] + self.credentials['storageurl'] + "/file"
        # headers = {'Authorization': 'Bearer ' + self.accessToken['access_token']}
        files = [
            ('filePart', (filenamewithpath, fileasbytesio.getvalue(), fileformat)),
        ]
        res = requests.post(storageURL, cookies=self.cookiejar, files=files)

    def generateStatement(self, data):
        nl = '"'
        return f"""mutation 
        {{  addDTable(
                dtablename: "{data["dtablename"]}",
                superDTable: [{data["superdtable"].upper()}],
                sriBuildInfo: "{"-".join(map(lambda x: f"${{{x}}}", data["sribuildinfo"]))}",
                dataLinks: [{",".join(
            map(lambda x:
                f'{{alias:"{x["name"]}", locale: DE, superPropertyURI: DYNAMIC_DATALINK, DataType: {x["type"].upper()}}}'
                , data["header"]))}],
                data:
                [ [{",".join(map(lambda x: f'"{x["name"]}"', data["header"]))}]
                  {",".join(
            map(
                lambda row: f'[{",".join(map(lambda col: f"{nl}{col}{nl}", row))}]', data["rowdata"]))}
                ]
                )}}"""

    def generateV2Statement(self, data):
        nl = '"'
        empty = ""
        ignore = "IGNORE"
        dontignore = "DONTIGNORE"

        for idx, rowdata in enumerate(data["rowdata"]):
            for idx2, coldata in enumerate(rowdata):
                if isinstance(coldata, str):
                    data["rowdata"][idx][idx2] = ujson.dumps(coldata)
                else:
                    data["rowdata"][idx][idx2] = f'"{coldata}"'

        return f"""mutation 
        {{  addDTablev2(
                dtablename: "{data["dtablename"]}",
                superDTable: [{data["superdtable"].upper()}],
                sriBuildInfo: "{"-".join(map(lambda x: f"${{{x}}}", data["sribuildinfo"]))}",
                dataLinks: [{",".join(
            map(lambda x:
                f'{{alias:"{x["name"]}", locale: DE, superPropertyURI: DYNAMIC_DATALINK, DataType: {x["type"].upper()}}}'
                , data["header"]))}],
                data:
                [ [{",".join(map(lambda x: f'{{value:{nl}{x["name"]}{nl}}}', data["header"]))}]
                  {",".join(
            map(
                lambda row: f'[{",".join(map(lambda col: f"{{value:{empty if col is None else col},state:{ignore if col is None else dontignore}}}", row))}]', data["rowdata"]))}
                ]
                )}}"""

    def generateXsvUpdateStatement(self, data):
        stmnt = f'mutation{{' \
                f'updateDTable(dtablename:{data["dtablename"]}' \
                f' where: ['
        for e in data['where']:
            connective = e['connective']
            column = e['column']
            operator = e['operator']
            value = e['value']
            stmnt += f'{{connective: {connective}, column: {column}, operator: {operator}, value: "{value}"}}'
        stmnt += f']' \
                 f' updatelist: ['
        for key, value in data['update'].items():
            stmnt += f'{{datalink: {key}, value: "{value}"}}'
        stmnt += f'])}}'
        return stmnt

    def generateXsvDeleteStatement(self, data):
        stmnt = f'mutation{{' \
                f'deleteDDatalink(dtablename:{data["dtablename"]}' \
                f' where: ['
        for e in data['where']:
            connective = e['connective']
            column = e['column']
            operator = e['operator']
            value = e['value']
            stmnt += f'{{connective: {connective}, column: {column}, operator: {operator}, value: "{value}"}}'
        stmnt += f']' \
                 f' updatelist: ['
        for key, value in data['update'].items():
            stmnt += f'{{datalink: {key}}}'
        stmnt += f'])}}'
        return stmnt

    def saveVod(self,gsdbs, target, vodpath, datetime):
        vodFileName = vodpath.rsplit("\\", 1)[1]

        storageURL = self.credentials["baseurl"] + self.credentials['storageurl'] + f"/vod/{target}"
        with open(vodpath, 'rb') as fh:
            buf = io.BytesIO(fh.read())
            files = [
                ('filePart', (f"{vodFileName}", buf.getvalue(), "application/octet-stream")),
            ]
            res = requests.post(storageURL, cookies=gsdbs.cookiejar, files=files)

        self.executeStatement(f"""
                mutation{{
                addDTable(
                    dtablename:"gsvod",
                    superDTable:[DTABLE],
                    sriBuildInfo:"${{streamkey}}-${{fragmentid}}",
                    dataLinks:[{{ alias:"streamkey",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                    {{ alias:"fragmentid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                    {{ alias:"starttime",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:DATETIME}},
                    {{ alias:"segmentlength",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}],
                    data:[["streamkey","fragmentid","starttime","segmentlength"],
                          ["{target}","{vodFileName}","{datetime}","60"]
                          ])
            }}
            """)
        self._logger.debug("saved vod:" + vodpath)