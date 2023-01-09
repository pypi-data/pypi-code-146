from advancedLogger.contract import IIndexFormatter, ITimeFormatter


class IndexFormatter(IIndexFormatter):
    def __init__(self, indicator: str, timeFormatter: ITimeFormatter):
        self.__timeFormatter: ITimeFormatter = timeFormatter
        self.__indicator = indicator

    def getIndex(self) -> str:

        return self.__indicator + '-' + self.__timeFormatter.get()
