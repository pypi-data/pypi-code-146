from abc import abstractmethod
from pathlib import Path

from pyPhases.Data import Data

from ..util.Optionizable import Optionizable


class DataExporter(Optionizable):
    """
    Data exporter is an abstract class that should be used to define new data exporters.
    A data exporter can handle data from a specific type and read or write it to self definded
    storage.

    The data exporter should handle all ingoing and outgoing data for the project.
    """
    recreate: bool = True
    currentDataObj: Data = None


    def initialOptions(self, defaultOptions=None):
        return {
            "basePath": "./data"
        }

    @abstractmethod
    def checkType(self, type) -> bool:
        """this method needs to be overwritten and checks if the exporter is compatible to a given type

        Returns:
            bool: returns True if the exporter can handle the given type.
        """
        return False

    def stream(self, dataId, options={}):
        """a stream exporter can be used to pass the streaming handle within the project.

        Args:
            dataId ([type]): the full data id (with all config values) is passed to the stream
            options (dict, optional): options passed to the stream exporter
        """
        raise Exception("The exporter has no stream method implemented")

    def finishStream(self, dataId):
        """this method can be called if the streaming process finished (for example the writing process)

        dataId ([type]): the full data id (with all config values) is passed to the stream
        """
        pass

    def reinit(self):
        """recreate the current datatype if the exporter needs to be recreated with every exported/imported type.
        """
        if not self.recreate:
            return self
        return type(self)(self.options)

    def exists(self, path):
        """checks if there is data to a given path

        Args:
            path (str): path to identify the data
        """
        return Path(self.getPath(path)).exists()

    @abstractmethod
    def read(self, path, options={}):
        """read data and raises an exception (DataNotFound) if the data was not found

        Args:
            path (str): path to identify the data
        """
        pass

    @abstractmethod
    def write(self, path, data, options={}):
        """writes data

        Args:
            path (str): path to identify the data
            data (): the data object
        """
        pass

    def getPath(self, path):
        basePath = self.getOption("basePath")
        return Path(basePath, path).as_posix()

    def delete(self, path):
        return Path(self.getPath(path)).unlink()
