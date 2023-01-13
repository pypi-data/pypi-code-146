from dataclasses import dataclass
from typing import List
import zipfile
import glob
import os
import shutil
import pandas as pd


@dataclass
class TextractZipToDataFrame:
    """
    Class that take as input AWS textract manual zip output
    Unzip the file and concat all the table found in the pdf
    Only valid on pdf from Credit Agricole Alsace
    """

    # init method or constructor
    def __init__(self, directory_to_extract_to):
        self.directory_to_extract_to = directory_to_extract_to

    def unzip_textract_zip_file(self, path_to_zip_file) -> List[str]:
        """
        Process and tranform data in Zip to pd.DataFrame
        Zip file is obtained from a manual process of using AWS textract services
        This class worked only for a specifc type of docuements from a specific bank
        """

        with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
            zip_ref.extractall(self.directory_to_extract_to)

        list_unzipped_files = os.listdir(self.directory_to_extract_to)

        return list_unzipped_files

    def get_csv_table_from_unzipped_file(self) -> pd.DataFrame:
        """
        Process and only keep the table.csv files needed
        Delete all non csv file from the unzipped folder
        """

        # Read all the file containing table into one unique table and return the table
        unifed_table = pd.concat(
            map(
                pd.read_csv,
                glob.glob(os.path.join(self.directory_to_extract_to, "table-*.csv")),
            )
        )

        if unifed_table.shape[0] == 0:
            unifed_table = pd.DataFrame()

        # Deleting an non-empty folder if it exists
        if os.path.exists(self.directory_to_extract_to + "/__MACOSX/") is True:
            shutil.rmtree(
                self.directory_to_extract_to + "/__MACOSX/", ignore_errors=True
            )
            print("Deleted __MACOSX directory successfully")

        # Delete all the file in folder
        for file in os.listdir(self.directory_to_extract_to):
            os.remove(os.path.join(self.directory_to_extract_to, file))

        return unifed_table
