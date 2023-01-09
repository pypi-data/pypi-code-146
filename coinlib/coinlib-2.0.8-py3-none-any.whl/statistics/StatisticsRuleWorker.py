from chipmunkdb.ChipmunkDb import ChipmunkDb

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from google.protobuf.json_format import MessageToJson
import inspect
import numpy as np
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.statistics.StatisticRuleJob import StatisticRuleJob

class StatisticsRuleWorker(WorkerJobProcess):

    def initialize(self):
        self.registrar = Registrar()
        self.statisticInterface = stats.StatisticsMethodWorkerStub(self.getChannel())

        if self.statisticConfig is None:
            self.statisticConfig = self.statisticInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
        self.chartConfigData = self.statisticConfig.chartData
        pass

    def setConfig(self, configuration):
        self.statisticConfig = configuration
        pass

    def getIndicatorMethod(self, indicator):
        found_method = None
        registeredFunctions = self.registrar.statisticsCallbacks

        if "rule_." + indicator.statisticFunction in registeredFunctions:
            found_method = registeredFunctions["rule_." + indicator.statisticFunction]
        else:
            if "rule_" + indicator.statisticFunction in registeredFunctions is not None:
                found_method = registeredFunctions["rule_"+indicator.statisticFunction]

        return found_method

    def onStatisticFunctionError(self, statisticJob, error):

        statsError = statsModel.StatisticRuleFunctionError()
        statsError.error.message = str(error)
        statsError.worker.CopyFrom(self.workerJob)
        statsError.statisticFunction.CopyFrom(statisticJob)

        self.statisticInterface.OnStatisticFunctionErrorOccured(statsError, metadata=self.registrar.getAuthMetadata())

        return False

    def calculateStatisticFunction(self, statisticRule):

        try:
            targetMethod = self.getIndicatorMethod(statisticRule)

            message_as_json = json.loads(MessageToJson(statisticRule))
            self.logger().info(message_as_json)
            inputs = message_as_json["inputs"]

            raw_inputs = self.extractInputsFromDataFrameAndInsertInDataFrame(inputs)
            inputs_with_raw_values = {}
            for k in inputs:
                inputs_with_raw_values[k] = inputs[k]["value"]
            statisticJob = StatisticRuleJob(self.getDf(), inputs_with_raw_values, statisticRule.id, self)

            if (inspect.iscoroutinefunction(targetMethod["process"])):
                async def runandwait():
                    try:
                        task = asyncio.ensure_future(targetMethod["process"](raw_inputs, statisticJob))
                        result = await task
                    except Exception as e2:
                        raise e2

                loop = asyncio.new_event_loop()
                process = loop.run_until_complete(runandwait())
            else:
                process = targetMethod["process"](raw_inputs, statisticJob)
        except Exception as e:
            self.logger().info("Error on Statistic")
            self.logger().error(e)
            self.onStatisticFunctionError(statisticRule, e)
            return None

        return statisticJob.getResultColumns()

    def calculateRulesGroup(self, ruleGroup):

        if ruleGroup.enabled == False:
            return False

        allResults = []
        for r in ruleGroup.rules:
            try:
                if r.type == "group":
                    groupResults = self.calculateRulesGroup(r)
                    allResults.append(groupResults)
                else:
                    ruleResults = self.calculateStatisticFunction(r)
                    if ruleResults is not None:
                        allResults.append(ruleResults)
            except Exception as e:
                self.logger().error("Problem mit Indicator", str(e))
                pass

        combinator = ruleGroup.combinator

        allResults = [[np.int(i if not np.isnan(i) else 0) for i in arr] for arr in allResults]

        try:
            if combinator == "and":
                resultColumn = np.logical_and.reduce(allResults)
            elif combinator == "or":
                resultColumn = np.logical_or.reduce(allResults)

            if ruleGroup.combinator_not == True:
                resultColumn = np.logical_not.reduce(resultColumn)
        except Exception:
            print(e)
            pass

        self.getDf()["r_"+ruleGroup.id] = resultColumn

        return resultColumn
        
    def run(self):

        returnRow = False
        # lets fill teh dataframe with previous value because of the different merged timeframes
        self.dataFrame = self.dataFrame.fillna(method='ffill')
        try:

            returnRow = self.calculateRulesGroup(self.statisticConfig)
        except Exception as e:
            self.logger().error("Problem mit Indicator", str(e))
            pass

        if not isinstance(returnRow, list) and not isinstance(returnRow, np.ndarray):
            returnRow = False

        self.getDf()["r_master"] = returnRow

        self.getDf()["r_master"] = self.getDf()["r_master"].astype(int)

        ##try:
        ##   print(self.getDf().query('r_master > 0')["r_master"].to_json())
        ##except Exception as e:
        ##   pass

        self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(self.chartConfigData.chipmunkdbHost))
        self.chipmunkDb.save_as_pandas(self.getDf().query("r_master > 0")[["r_master"]], self.chartConfigData.workspace_id,
                                  mode="dropbefore",
                                  domain="stats")

        partiallyData = statsModel.StatisticBulkedPartiallyData()
        resultData = statsModel.StatisticRulePartiallyData()
        resultData.resultName = "master"
        resultData.collectionid = ""
        resultData.worker.CopyFrom(self.workerJob)
        partiallyData.ruleData.CopyFrom(resultData)

        self.statisticInterface.OnStatisticPartiallyData(partiallyData, metadata=self.registrar.getAuthMetadata())


        