"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
import re
from abc import ABC
class CommonConstants(ABC):
    """
     This abstract class holds all the constant variables which can be commonly used 
     in this automation application.                                  
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    BASE_URL: str = None #http://127.0.0.1:8000/ #https://digital.kortfilmfestivalen.no/en/
    """The default value of BASE_URL is None. If the value is None then this automation app 
    will open the WebApp at Localhost automatically. And if there is a valid URL (string) 
    assigned in the BASE_URL the automation app will open then URL for testing. © BS23"""
    URL_VALIDATOR_CHAR = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    """This is a constant for checking string to identify valid URL. © BS23"""
    PROJECT_DIRECTORY_LOCATION: str = str(os.path.realpath(''))
    """This will indicate at the root directory of the project . © BS23"""
    LOG_FILE_PATH_LOCATION: str = str(os.path.join(os.path.realpath(''), "tests", "log"))
    """This is a constant variable which holds the location of log directory. © BS23"""
    GENERATE_JSON_REPORT = False
    JSON_REPORT_FILE_PATH: str = str(os.path.join(os.path.realpath(''), "tests", "report", "report.json"))
    TARGET_TEST_AREA_LOCATION: str = str(os.path.join(os.path.realpath(''), "tests", "testcases", ""))
    HEADLESS_MODE: bool = True
    """Headless test mode will be always True. If the Tester want to see Visual Test in 
    the Automation Browser the HEADLESS_MODE must set False. © BS23"""
    PARALLEL_MODE: bool = False    # More R&D Needed! > PARALLEL_MODE = True < is not fit for Production
    """Parellel or Concurrent testing mode will be always Flase. If the Tester have requirement 
    of Parellel/Concurrent test the PARALLEL_MODE value must get updated as True. © BS23"""
    DEFAULT_BROWSER_OPTION: int = 5
    """
        [1] Chrome
        [2] Chromium (Ignore)
        [3] Brave (Ignore)
        [4] Firefox
        [5] Edge
        [6] Opera (Ignore)
        © BS23
    """
    WORKBOOK_FILE_PATH = str(os.path.join(os.path.realpath(''), "tests", "testdata", "resources",
                                          "AutomationScriptTest.xlsx"))
    