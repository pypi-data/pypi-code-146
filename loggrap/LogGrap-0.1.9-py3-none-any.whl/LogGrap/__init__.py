"""
LogGrap :
A logging package for your python project

developed by ssomgrap
"""

from datetime import datetime
from os import path

TYPE_NEUTRAL = "neutral"
TYPE_INFO = "info"
TYPE_WARN = "warn"
TYPE_ERROR = "error"
TYPE_CRITICAL = "critical"


class Logger:

    def __init__(self, name, directory="./"):
        """
        :param name: The name of your Logger (will be present in all messages formats).
        :param directory: The directory where the logs files will be create.
        :return: A Logger object and create a logs file when initialized.
        """
        self.name = name
        self.directory = directory.replace("\\", "/")
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.logsDict = {
            f"{TYPE_NEUTRAL}": {"doTerminalOutput": True, "doFileOutput": True},
            f"{TYPE_INFO}": {"format": "[%name] [%time] [Info] ", "doTerminalOutput": True, "doFileOutput": True},
            f"{TYPE_WARN}": {"format": "[%name] [%time] [Warning] ", "doTerminalOutput": True, "doFileOutput": True},
            f"{TYPE_ERROR}": {"format": "[%name] [%time] [Error] ", "doTerminalOutput": True, "doFileOutput": True},
            f"{TYPE_CRITICAL}": {"format": "[%name] [%time] [Critical] ", "doTerminalOutput": True, "doFileOutput": True}
        }
        self.logFile = f"{self.directory}/{self.name}_{self.date}.log"

    def getFormat(self, logType=""):
        """
        :param logType: TYPE_INFO, TYPE_WARN, TYPE_ERROR, TYPE_CRITICAL. If the logType is not specify, return all logs types formats.
        :return: List of logs format
        """
        if logType == "":
            result = []
            for logTyp in self.logsDict.items():
                result.append(self.logsDict[logTyp[0]]["format"])
        else:
            result = [self.logsDict[logType[0]]["format"]]
        return result

    def setFormat(self, logFormat, logType=""):
        """
        %name : Name of your Logger
        %hour : Time of the event
        %date : Date of the event
        :param logType: TYPE_INFO, TYPE_WARN, TYPE_ERROR, TYPE_CRITICAL. If the logType is not specify, define the format for all logs types.
        :param logFormat: Write here the new format you need, 
        """
        if logType == "":
            for logTyp in self.logsDict.items():
                self.logsDict[logTyp[0]]["format"] = str(logFormat)
        else:
            self.logsDict[logType]["format"] = str(logFormat)

    def setTerminalOutput(self, boolean, logType=""):
        """
        True by default
        :param logType: TYPE_INFO, TYPE_WARN, TYPE_ERROR, TYPE_CRITICAL. If the logType is not specify, define the terminalOutput for all logs types.
        :param boolean: True or False
        """
        if logType == "":
            for logTyp in self.logsDict.items():
                self.logsDict[logTyp[0]]["doTerminalOutput"] = bool(boolean)
        else:
            self.logsDict[logType]["doTerminalOutput"] = bool(boolean)

    def setFileOutput(self, boolean, logType=""):
        """
        It's true for all logs by default
        :param logType: TYPE_INFO, TYPE_WARN, TYPE_ERROR, TYPE_CRITICAL. If the logType is not specify, define the fileOutput for all logs types.
        :param boolean: True or False
        """
        if logType == "":
            for logTyp in self.logsDict.items():
                self.logsDict[logTyp[0]]["doFileOutput"] = bool(boolean)
        else:
            self.logsDict[logType]["doFileOutput"] = bool(boolean)

    def neutral(self, text):
        """
        This log has no format
        :param text:
        :return: The Log without format
        """
        if self.logsDict["neutral"]["doTerminalOutput"]:
            print(text)
        if self.logsDict["neutral"]["doFileOutput"]:
            if not path.exists(self.logFile):
                file = open(self.logFile, "x")
                file.close()
            with open(self.logFile, "a") as logFile:
                logFile.write(text + "\n")
        return text

    def loggerPrint(self, logType, text):
        """
        :param logType:
        :param text:
        """
        text = str(self.logsDict[logType]["format"] + text).replace("%name", self.name).replace("%time", datetime.now().strftime("%H:%M:%S")).replace("%date", self.date)
        if self.logsDict[logType]["doTerminalOutput"]:
            print(text)
        if self.logsDict[logType]["doFileOutput"]:
            if not path.exists(self.logFile):
                file = open(self.logFile, "x")
                file.close()
            with open(self.logFile, "a") as logFile:
                logFile.write(text + "\n")
        return text

    def info(self, text):
        """
        :param text:
        :return:
        """
        return self.loggerPrint(TYPE_INFO, text)

    def warn(self, text):
        """
        :param text:
        :return:
        """
        return self.loggerPrint(TYPE_WARN, text)

    def error(self, text):
        """
        :param text:
        :return:
        """
        return self.loggerPrint(TYPE_ERROR, text)

    def critical(self, text):
        """
        :param text:
        :return:
        """
        return self.loggerPrint(TYPE_CRITICAL, text)
