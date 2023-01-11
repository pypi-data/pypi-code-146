from abc import ABCMeta, abstractmethod
import pandas as pd

class AbstractReader(object):
    __metaclass__ = ABCMeta

    DATA = pd.DataFrame()
    META = dict()
    
    def __init__(self, datefmt=None):
        """
        The generic class used to read logger data. Subclasses must be defined depending on what kind of instrument the data comes from. However, each reader behaves the same way. They all have the `.read()` method that takes the file name as an argument. You can create a reader first and then call the `.read()` method, or just run everything on one line. 

        Attributes
        ----------
        DATA : pd.DataFrame
            Reader objects should store csv data in a pandas dataframe in the `DATA` attribute.  Column titles should mostly be left unchanged with the exception of the datetime column which is renamed to `TIME`. TIME should always the first column in the dataframe.
        META : dict
            Where possible, any metadata that is found in the file is stored in a `META` attribute.

        Notes
        -----
        Datalogger metadata will differ between instruments. However, there are many commonalities. The following is an alphabetical list of metadata that should use common terminology and formatting in the `META` dictionary for each datalogger type. 
        
        .. code-block:: python

            latitude : (CF) latitude where data was collected
            longitude : (CF) longitude where data was collected


            Abbrevations:
            CF - Climate and Forecast Conventions

        """
        if datefmt:
            self.DATEFMT = datefmt

    @abstractmethod
    def read(self, file) -> "pd.DataFrame":
        """read data from a file"""

    def get_data(self):
        return self.DATA
