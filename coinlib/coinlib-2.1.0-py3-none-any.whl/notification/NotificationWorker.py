import asyncio
import inspect
import threading

import simplejson as json
from coinlib.Registrar import Registrar
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib.WorkerJobProcess import WorkerJobProcess


class NotificationWorker(WorkerJobProcess):


    def __init__(self, workerJob, factory):
        self.notificationWorkerConfig = None
        self.notificationProcessInfo = None
        self.notificationRegistrationInfo = None
        super(NotificationWorker, self).__init__(workerJob, factory)

    def getNotificationCallerType(self):
        if self.notificationWorkerConfigGlobal.HasField("sendMessageConfig"):
            return "sendNotification"
        return "extractMessageCallback"

    def initialize(self):
        self.registrar = Registrar()
        self.notificationWorkerInterface = stats.NotificationWorkerStub(self.getChannel())
        if self.notificationWorkerConfig is None:
            notificationWorkerConfigGlobal = self.notificationWorkerInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
            self.notificationWorkerConfigGlobal = notificationWorkerConfigGlobal
            if notificationWorkerConfigGlobal.HasField("sendMessageConfig"):
                self.notificationWorkerConfig = notificationWorkerConfigGlobal.sendMessageConfig
            if notificationWorkerConfigGlobal.HasField("extractDataConfig"):
                self.notificationWorkerConfig = notificationWorkerConfigGlobal.extractDataConfig

            self.notificationRegistrationInfo = self.registrar.notificationCallbacks["method_"+self.notificationWorkerConfig.notificationIdentifier]
            self.notificationProcessInfo = self.notificationRegistrationInfo["process"]
            self.notificationProcessExtractorInfo = self.notificationRegistrationInfo["process_extractCallback"]
        pass

    def onErrorHappened(self, message):

        indicatorError = statsModel.NotificationError()
        indicatorError.error.message = str(message)
        indicatorError.worker.CopyFrom(self.workerJob)

        self.logger().error("Error in Notiification Worker - "+str(message))

        self.notificationWorkerInterface.OnNotificationErrorOccured(indicatorError, metadata=self.registrar.getAuthMetadata())

    def error(self, message):
        self.onErrorHappened(message)
        return False

    def setConfig(self, configuration):
        self.notificationWorkerConfig = configuration
        pass

    def getRunnerProcess(self):
        return self.notificationProcessInfo

    def getExtractorRunnerProcess(self):
        return self.notificationProcessExtractorInfo

    def extractCallbackNotification(self):
        try:
            process = self.getExtractorRunnerProcess()
            inputs = self.getInputs()

            inputs["data"] = json.loads(self.notificationWorkerConfig.data)

            if (inspect.iscoroutinefunction(process)):
                async def runandwait():
                    try:
                        task = asyncio.ensure_future(process(inputs, self))
                        result = await task
                    except Exception as e2:
                        raise e2
                    return result

                loop = asyncio.new_event_loop()
                ret = loop.run_until_complete(runandwait())
            else:
                ret = process(inputs, self)

            data = statsModel.NotificationCallbackExtract()
            data.data = json.dumps(ret["data"])
            data.button_id = ret["button_id"]
            data.worker.CopyFrom(self.workerJob)

            self.notificationWorkerInterface.OnCallbackDataExtracted(data, metadata=self.registrar.getAuthMetadata())

        except Exception as e:
            return self.onErrorHappened(str(e))

        return ret

    def runNotification(self):


        try:

            process = self.getRunnerProcess()

            inputs = self.getInputs()

            inputs["channels"] = json.loads(self.notificationWorkerConfig.channels)
            inputs["message"] = self.notificationWorkerConfig.message
            inputs["callback_id"] = self.notificationWorkerConfig.callback_id
            inputs["callback_url"] = self.notificationWorkerConfig.callback_url
            try:
                inputs["buttons"] = json.loads(self.notificationWorkerConfig.buttons)
            except Exception as e:
                inputs["buttons"] = None
            try:
                inputs["images"] = json.loads(self.notificationWorkerConfig.images)
            except Exception as e:
                inputs["images"] = None

            if (inspect.iscoroutinefunction(process)):
                async def runandwait():
                    try:
                        task = asyncio.ensure_future(process(inputs, self))
                        result = await task
                    except Exception as e2:
                        raise e2

                loop = asyncio.new_event_loop()
                ret = loop.run_until_complete(runandwait())
            else:
                ret = process(inputs, self)

        except Exception as e:
            return self.onErrorHappened(str(e))

        return ret

    def getInputs(self):
        return json.loads(self.notificationWorkerConfig.options)

    def run(self):

        if self.getNotificationCallerType() == "sendNotification":
            t = threading.Thread(target=self.runNotification, args=[], daemon=True)
        else:
            t = threading.Thread(target=self.extractCallbackNotification, args=[], daemon=True)

        t.start()

        try:
           t.join()
        except Exception as e:
           self.onErrorHappened(e.message)
           pass

        return True


