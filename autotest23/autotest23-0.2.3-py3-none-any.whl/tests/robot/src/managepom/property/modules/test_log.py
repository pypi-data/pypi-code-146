"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""

import os
import logging
import datetime as dt

class TestLog:
    """
    Levels:
        * DEBUG
        * INFO
        * ERROR
        * WARNING
        * CRITICAL 
    """
    
    def __init__(self):
        self.logger = None
        self.file_handler = None
        
    # https://docs.python.org/3/library/logging.html#logging.Formatter
    def log(self, file_directory: str):
        # Setting up basic logger configuration.
        logging.basicConfig(level= logging.DEBUG)
        # Creating Log File
        file_path = self.__create_log_file(file_directory)
        # Making Log file writable with updated log data.
        self.__file_handler(file_path)
        self.logger = logging.getLogger("AUTOMATION-QA_LOG")
        # All the new logs will append in the Log file 
        self.logger.addHandler(self.file_handler)
        
    def __create_log_file(self, file_directory: str = None) -> str:
        # Getting current date and time
        current_date = dt.datetime.today()
        # File naming format according to current date in log extention.
        file_name = f"{current_date.day:02d}-{current_date.month:02d}-{current_date.year}.log"
        # Create file path for Log file.
        file_path = str(os.path.join(file_directory, file_name))
        return file_path
    
    def __file_handler(self, file_path):
        # If the Log file does not exist in the file path, new Log file will be created.
        self.file_handler = logging.FileHandler(file_path)
        # Setting Level into Debug
        self.file_handler.setLevel(logging.DEBUG)
        # Data Writing Format.
        formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
        # Setting the Data writing format in the Log file.
        self.file_handler.setFormatter(formatter)