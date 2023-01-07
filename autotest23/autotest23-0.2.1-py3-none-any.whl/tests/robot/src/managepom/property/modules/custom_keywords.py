from src.test23.tests.resources.test_log import TestLog
from src.test23.tests.resources.json_report import ReportInJSON

class CustomKeywords(TestLog, ReportInJSON):
    """
    CustomKeyword is a colloection of commonly used methods. 
    these methods can exist inside the CustomKeyword itself 
    or can be inherited from other classes. This CustomKeyword
    class is inherited by DriverController. So DriverController 
    can get all the needed keywords/methods from CustomKeyword easily.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    pass
