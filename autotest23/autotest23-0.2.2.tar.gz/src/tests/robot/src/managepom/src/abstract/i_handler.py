from ...constants import Constants
from abc import ABC, abstractmethod


class IHandler(Constants, ABC):
    """
    This is an abstract class which is acts like a data type 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    #Output Message
    POM_GENERATE_SUCCESS_MESSAGE: str = "\n=======>Page Object Model (POM) Design Pattern Implemented<=======\n"
    POM_PLACEMENT_SUCCESS_MESSAGE: str = "\n=======>Scripts & Module placement operations at POM Pattern complete.<=======\n"
    PAGE_OBJECT_GENERATE_SUCCESS_MESSAGE: str = "\n=======>New Page Object and Locator created successfully.<=======\n"
    TEST_SCENARIO_GENERATE_SUCCESS_MESSAGE: str = "\n=======>New Test Scenerio created successfully<=======\n"
    ERROR_UNKNOWN_MESSAGE: str = "\n!!! Someting went wrong !!!\n"
    
    @abstractmethod
    def operation(self, option_number: int = 0):
        """Data Type Abstract Class © BS23"""