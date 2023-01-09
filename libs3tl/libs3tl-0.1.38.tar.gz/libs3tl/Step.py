from datetime import datetime
import inspect
import json
import redis
from jproperties import Properties
import logging
import time
import os
import sys
import traceback
import requests
import platform


class Step:

    # initializing with defaults
    def __init__(self):
        self.setStartTime()
        self.step = "St"
        self.paramsFile = 'Step.properties'
        self.logger = 'logStep'
        self.logFile = self.getRelativeFile('../logs/Step.log')

    # Needed for relative paths
    def getRelativeFile(self, filename):
        # dirname = os.path.dirname(__file__) ## python directory should not be fetched  using __file__
        dirname = sys.path[0] + '/'
        filename = os.path.join(dirname, filename)
        return filename

    # Tasks to be done at the start of the script
    def startup(self):
        self.setTaskID()
        self.setUUID()
        self.params = self.trimPropertiesConfig(self.loadParams(self.paramsFile))
        self.params = self.loadParams(self.paramsFile)
        self.nextStep = None
        if self.params["nextStep"]:
            self.nextStep = self.params["nextStep"].data
        self.setTaskExecutionID()
        self.setLogger(self.logger, self.logFile, logging.INFO)
        self.startRedisConn()
        self.consensusID = self.taskID
        self.consensusExecutionID = self.taskExecutionID
        if ("consensusID" in self.params):
            self.consensusID = self.params["consensusID"].data
            self.consensusExecutionID = self.consensusID + "_" + self.startTime

    # setter for Start Time
    def setStartTime(self):
        now = datetime.utcnow()
        self.startTime = now.strftime("%Y%m%d%H%M%S")

    # setter for task Execution ID
    def setTaskExecutionID(self):
        self.taskExecutionID = self.taskID + "_" + self.startTime

    # Get the NodeId of the System. Similar to uname -n
    def getNodeId(self):
        return platform.node()

    # Create  Redis connection
    def startRedisConn(self):
        self.rC = self.makeRedisConn()

    # Load parameters from file
    def loadParams(self, filename):
        configs = Properties()
        filename = self.getRelativeFile('../params/' + filename)
        with open(filename, 'rb') as config_file:
            configs.load(config_file)
            config_file.close()
        return configs

     # Trim keys and values in properties
    def trimPropertiesConfig(self, config: Properties) -> Properties:
        trimmedPropertiesFile = Properties()
        for properties in config:
            trimmedPropertiesFile[properties.strip()] = config[properties].data.strip()
        return trimmedPropertiesFile

    # declaring Redis connection parameters
    def makeRedisConn(self):
        try:
            connection = redis.StrictRedis(host=self.params["redisHost"].data,
                                           port=self.params["redisPort"].data,
                                           password=self.params["redisPassword"].data,
                                           decode_responses=True)
            response = connection.ping()
            return connection
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            self.logError(self.step, 'Error in redis connection setup')

    # This method has to be used by the relevant class - Transform, ML, Load to listen to their queue.
    def startSubscriber(self):
        self.subscriber = self.rC.pubsub()
        self.subscriber.subscribe(self.taskID + "_" + self.step)


    # Extracting UUID from path of current working directory
    def setUUID(self):
        path = os.getcwd().replace("\\", "/").split("/")
        self.taskUUID = path[-2]

    # Reading taskID from text file
    def setTaskID(self):
        with open(self.getRelativeFile('../params/Identifier.txt')) as f:
            lines = f.readlines()
        self.taskID = lines[0]
        f.close()

    # Storing the datahandoff in a dataframe and the converting  DF to json and printing it
    # def handOff(self, rC, taskID, step, datatohandoff):
    def handOff(self, dataToHandoff):
        try:
            self.logInfo("Handoff",self.taskID)
            self.rC.publish(self.taskID + "_" + self.nextStep, dataToHandoff)
        except(ConnectionError) as cE:
            self.logError(self.nextStep, str(cE))

    # setter function to configure Logger
    def setLogger(self, logger_name, log_file, level=logging.INFO):
        self.mylogger = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        self.mylogger.setLevel(level)
        self.mylogger.addHandler(fileHandler)
        logging.Formatter.datefmt = '%Y-%m-%d %H:%M:%S'
        logging.Formatter.converter = time.gmtime

    # getter function to get logger
    def getLogger(self):
        return self.mylogger

    def logMessageFormat(self, step, method, message):
        try:
            if message == None or step == None or method == None:
                logdata = ' : ' + 'None'
                return logdata
            else:
                logdata = ' : ' + self.taskExecutionID + ' : ' + step + ' : ' + method + ' : ' + message
                return logdata
        except:
            print('logMessageFormat')
            return 'settaskExecutionId OR set step  went wrong , kindly recheck.'

    def exceptionTraceback(self):
        try:
            # Get current system exception
            # sys.exc_info() returns list of size 3 automatic assignments to variables
            ex_type, ex_value, ex_traceback = sys.exc_info()
            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)
            # Format stacktrace
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Message : %s" % (trace[0], trace[1], trace[3]))
            # self.getLogger().error(self.logMessageFormat(self.step, inspect.stack()[0][3], str(str(ex_traceback) + ' ' + str(stack_trace))))
            return str(str(ex_traceback) + ' ' + str(stack_trace))
        except Exception as error:
            print('#######exceptionTraceback#### ' + str(error))

    def connectToAPIForKey(self, url, headers, successResponse, key):
        try:
            response = self.createAndGetResponseFromURL(url, headers, successResponse)
            if response == None:
                return None
            responseData = json.loads(response.text)
            if key in responseData:
                return responseData[key]
            else:
                self.logError(self.step, 'Key not found' + key)
                print('Key not found' + key)
                return None
        except(BaseException) as e:
            self.logError(self.step, str(e))
            print(self.exceptionTraceback())
            return None

    def createAndGetResponseFromURL(self, url, headers, successResponse):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == successResponse:
                return response
            else:
                self.logError(self.step, 'response.status_code from createAndGetResponseFromURL ' + str(response.status_code))
                return None
        except(BaseException) as e:
            self.logError(self.step, str(e))
            print(self.exceptionTraceback())
            return None


    def logInfo(self, step, message):
        currentframe = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentframe, 2)
        self.getLogger().info(self.logMessageFormat(step, outerFrames[1][3], message))


    def logWarn(self, step, message):
        currentframe = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentframe, 2)
        self.getLogger().warn(self.logMessageFormat(step, outerFrames[1][3], message))


    def logError(self, step, message):
        currentframe = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentframe, 2)
        self.getLogger().error(self.logMessageFormat(step, outerFrames[1][3], message))


    def logDebug(self, step, message):
        currentframe = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentframe, 2)
        self.getLogger().debug(self.logMessageFormat(step, outerFrames[1][3], message))


    def logFatal(self, step, message):
        currentframe = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentframe, 2)
        self.getLogger().fatal(self.logMessageFormat(step, outerFrames, message))
