
import pandas as pd
import re
import warnings

from .AbstractReader import AbstractReader


class GP5W(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"
    HK = re.compile("^#HK")

    def __init__(self):
        """File reader for GP5W 

        GP5W is the older software for GeoPrecision instruments

        Examples
        --------

        .. code-block:: python

            from teaspoon.dataloggers import GP5W
            from pkg_resources import resource_filename
            gp5w_file = resource_filename("teaspoon", "dataloggers/test_files/GP5W_260.csv")

            # To read a file, you might first create a reader object 
            reader = GP5W()
            reader.read(gp5w_file)

            # Or instead, read the data in one line
            data = GP5W().read(gp5w_file)
        """
        super().__init__()

    def read(self, file: str) -> "pd.DataFrame":
        """Read a GP5W geoprecision file

        Parameters
        ----------
        file : str
            Path to an GP5W Geoprecision datalogger export

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the data

        """
        self.META['raw'] = list()

        data = list()
        
        with open(file, "r") as f:
            for line in f:
                if self.__is_header(line):
                    delimiters = line.count(",")
                    columns = line.strip().split(",")

                elif self._is_observation(line):
                    line = line.strip()
                    line += "," * (delimiters - line.count(","))
                    data.append(line.split(","))

                else:
                    self.META['raw'].append(line)

        self.DATA = pd.DataFrame(data, columns=columns)
        
        for col in self.DATA.columns:
            if col == "Time":
                continue
            
            try:
                self.DATA[col] = pd.to_numeric(self.DATA[col], errors='raise')
            except ValueError:
                warnings.warn("Could not successfully convert all data to numeric. Some data may be missing")
                self.DATA[col] = pd.to_numeric(self.DATA[col], errors='coerce')

        self.DATA["Time"] = pd.to_datetime(self.DATA["Time"], format=self.DATEFMT)
        self.DATA.rename(columns={"Time":"TIME"}, inplace=True)

        self.DATA = self.DATA.drop(["No"], axis=1)
        self.DATA = self.drop_hk(self.DATA)

        return self.DATA

    def _is_observation(self, line: str) -> bool:
        match = re.search(r"\d*,\d{2}\.\d{2}\.\d{4}", line)
        return bool(match)

    def __is_header(self, line: str) -> bool:
        match = re.search("No,Time", line)
        return bool(match)

    def _is_hk(self, name: str) -> bool:
        if self.HK.match(name):
            return True
        return False

    def drop_hk(self, df: "pd.DataFrame") -> "pd.DataFrame":
        return df.drop([c for c in df if self._is_hk(c)], axis=1)