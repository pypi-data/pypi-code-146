"""
https://peps.python.org/pep-0591/#id2 [for future scope]

© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from abc import ABC, abstractmethod

class IDriver(ABC):
    
    driver = ""

    @abstractmethod
    def get_browser(self):
        """This method will install and open / run and open the 
        Web Driver and return the object id © BRAIN STATION 23"""
        pass
    
    