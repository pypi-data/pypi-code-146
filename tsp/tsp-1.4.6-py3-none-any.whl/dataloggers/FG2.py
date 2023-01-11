import pandas as pd
import re
import warnings

from .AbstractReader import AbstractReader


class FG2(AbstractReader):
    DATEFMT = "%d.%m.%Y %H:%M:%S"
    DELIMITER = ","
    HK = re.compile("^HK")

    def __init__(self):
        """File reader for FG2
        
        FG2 is the newer software for GeoPrecision instruments
        
        Examples
        --------
        .. code-block:: python

            from teaspoon.dataloggers import FG2
            from pkg_resources import resource_filename
            fg2_file = resource_filename("teaspoon", "dataloggers/test_files/FG2_399.csv")

            # Read an FG2 file
            FG2().read(fg2_file)
        """
        pass

    def read(self, file: str) -> "pd.DataFrame":
        """Read a FG2 geoprecision file

        Parameters
        ----------
        file : str
            Path to an FG2 Geoprecision datalogger export

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
                    delimiters = line.count(self.DELIMITER)
                    columns = line.strip().split(self.DELIMITER)

                elif self._is_observation(line):
                    line = line.strip()
                    line += self.DELIMITER * (delimiters - line.count(self.DELIMITER))
                    data.append(line.split(self.DELIMITER))

                else:
                    self.META['raw'].append(line)

        self.DATA = pd.DataFrame(data, columns=columns)
        
        for col in self.DATA.columns:
            if col == "TIME":
                continue
            
            try:
                self.DATA[col] = pd.to_numeric(self.DATA[col], errors='raise')
            except ValueError:
                warnings.warn("Could not successfully convert all data to numeric. Some data may be missing")
                self.DATA[col] = pd.to_numeric(self.DATA[col], errors='coerce')

        self.DATA["TIME"] = pd.to_datetime(self.DATA["TIME"], format=self.DATEFMT)
        self.DATA = self.DATA.drop(["NO"], axis=1)
        self.DATA = self.drop_hk(self.DATA)

        return self.DATA

    def _is_metadata(self, line) -> bool:
        match = re.search("^<.*>$", line)
        return bool(match)

    def _is_observation(self, line: str) -> bool:
        match = re.search(fr"^\d*{self.DELIMITER}\d\d.\d\d", line)
        return bool(match) 

    def __is_header(self, line: str) -> bool:
        match = re.search(f"NO{self.DELIMITER}TIME", line)
        return bool(match)

    def _is_hk(self, name: str) -> bool:
        if self.HK.match(name):
            return True
        return False

    def drop_hk(self, df: "pd.DataFrame") -> "pd.DataFrame":
        return df.drop([c for c in df if self._is_hk(c)], axis=1)
