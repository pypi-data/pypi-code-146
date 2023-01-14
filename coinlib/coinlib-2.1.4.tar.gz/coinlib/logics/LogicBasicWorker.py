import asyncio

import numpy as np
from chipmunkdb.ChipmunkDb import ChipmunkDb

from coinlib import Registrar
from coinlib.event.EventConsumer import EventConsumer
import inspect
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess


class LogicBasicWorker(WorkerJobProcess):

    def initialize(self):
        self.eventConsumer = EventConsumer(self)
        self.registrar = Registrar()
        self.chipmunkDb = None
        self.logicComponentsWithInfo = []

    def onBeforeWorkerStarts(self):
        self.createAllEventListeners()

        pass

    def generateLocalJob(self):
        pass
    def isOfflineWorker(self):
        return False

    def createAllEventListeners(self):
        for l in self.logicComponentsWithInfo:
            if "monitoredEvents" in l.details:
                for e in l.details["monitoredEvents"]:
                    self.eventConsumer.consume(e["realEventName"])


    def fireEventCallback(self, method, routing_key, message):
        try:
            logicJob = self.generateLocalJob()
            self.runLogicProcess(method, message, logicJob)
        except Exception as e:
            pass

    def getLogicMethodConfiguration(self, element):
        return json.loads(str(element.indicatorConfig, 'ascii'))

    def getLogicMethod(self, indicator):
        found_method = None
        registeredFunctions = self.registrar.logicCallbacks

        logic_component_id  = indicator.type+"_"+indicator.logicComponentId
        logic_component_id_without_cofix = logic_component_id
        if "-" in indicator.logicComponentId:
            logic_component_id_without_cofix = indicator.type+"_"+indicator.logicComponentId.rsplit('-', 1)[0]

        if logic_component_id in registeredFunctions:
            found_method = registeredFunctions[logic_component_id]
        elif logic_component_id_without_cofix in registeredFunctions:
            found_method = registeredFunctions[logic_component_id_without_cofix]

        return found_method

    def runLogicProcess(self, targetProcess, inputs, logicJob):
        ret_data_process = None

        if inspect.iscoroutinefunction(targetProcess):
            async def runandwait():
                try:
                    task = asyncio.ensure_future(targetProcess(inputs, logicJob))
                    result = await task
                except Exception as e2:
                    raise e2

            loop = asyncio.new_event_loop()
            ret_data_process = loop.run_until_complete(runandwait())
        else:
            ret_data_process = targetProcess(inputs, logicJob)

        return ret_data_process

    def setConfig(self, configuration):
        self.logicConfig = configuration
        pass

    def generateJob(self, table, logicComponentInfo, logic, inputs, fakeManager):
        return None

    def generateLogicComponentsInfo(self):

        class Object(object):
            pass
        self.logicComponentsWithInfo = []
        for logic in self.logicConfig.logicComponents:
            info = self.getLogicMethod(logic)
            if info is not None:
                s = Object()
                s.info = info
                s.logic = logic
                s.details = json.loads(logic.logicDetails)
                self.logicComponentsWithInfo.append(s)
            else:
                raise Exception("Your Logic Method " + logic.logicComponentId + " was not found")

        return self.logicComponentsWithInfo

    def getDataFrameLogicsActivityName(self):
        return self.chartConfigData.workspace_id + "_" + self.chartConfigData.activity_id

    def onLogicRunningFinished(self):

        self.saveLogicStorageToDataFrame()

        return True

    def extractLogicInfosFromManagerData(self, externalInfoBlock):
        try:
            infoBlock = externalInfoBlock
            allColumns = {}

            for key in infoBlock:
                row = infoBlock[key]
                for key_col in row:
                    if key_col not in allColumns:
                        allColumns[key_col] = []


            for col in allColumns:
                allColumns[col] = [None for i in range(len(infoBlock))]

            # save Datablock
            for key in infoBlock:
                row = infoBlock[key]
                for key_col in row:
                    v = row[key_col]
                    if v is not None:
                        try:
                            if type(v) == int or type(v) == float:
                                v = row[key_col]
                            else:
                                is_json = False
                                if ":" in row[key_col]:
                                    try:
                                        json.loads(v)
                                        is_json = True
                                    except Exception as e:
                                        is_json = False
                                        pass
                                if not is_json:
                                    v = json.dumps(row[key_col])
                        except Exception as e2:
                            pass
                    allColumns[key_col][key] = v

            for col in allColumns:
                arr = allColumns[col]
                fillpadSize = self.dataFrame.shape[0] - len(arr)
                arr = np.pad(arr, (0, fillpadSize), 'constant',
                                                       constant_values=(None))
                self.dataFrame["logics."+col] = arr
        except Exception as e:
            self.logger().error("Error in extractLogicInfosFromManagerData "+str(e))
            raise Exception("Error in extractLogicInfosFromManagerData "+str(e))

        return True

    def saveLogicStorageToDataFrame(self):

        filter_col = [col for col in self.dataFrame if col.startswith('logics')]
        # returnRows
        # save the returnRows to chipmunk as a storage database

        workspace = self.logicConfig.chartData.workspace_id


        if self.chipmunkDb is None:
            self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(self.logicConfig.chartData.chipmunkdbHost))

        try:
            self.chipmunkDb.save_as_pandas(self.dataFrame[filter_col], self.getDataFrameLogicsActivityName(),
                                           mode="append",
                                           domain="result")
        except Exception as e:
            self.logger().warn("Error on saving logics data", e)

        return True

    def runLogicComponents(self, table, fakeManager):

        try:

            for logicWithInfo in self.logicComponentsWithInfo:
                try:
                    logic = logicWithInfo.logic
                    logicComponentInfo = logicWithInfo.info

                    if logic.enabled:
                        inputs = {}
                        #if "inputs" in logicComponentInfo:
                        #    inputs = self.extractInputsFromDataFrameAndInsertInDataFrame(logicComponentInfo["inputs"])

                        logicJob = None
                        logicJob = self.generateJob(table, logicComponentInfo, logic, inputs, fakeManager)
                        logicJob.setParameterTable(self.parameterTable)

                        self.runLogicProcess(logicComponentInfo["process"], inputs, logicJob)


                except Exception as ie:
                    raise ie


        except Exception as e:
            self.registrar.logger.exception("Error on Logic Method Running")
            self.registrar.logger.error(e)
            raise e

        return True