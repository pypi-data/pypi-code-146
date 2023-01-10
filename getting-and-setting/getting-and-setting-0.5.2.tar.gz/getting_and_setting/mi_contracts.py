from typing import Protocol
from typing import NoReturn
from typing import List
from typing import Tuple
from typing import Dict
from typing import Iterator


class MiApiContract(Protocol):
    def __init__(self, host: str, port: str, pwd: str):
        """ Initialize a new MiApi contract, using
        
        As an alternative the 'from_env' and 'save_env' methods
        can be used to save and load connections and passwords,
        instead of using the __init__ directly. """

    def execute(self, prog: str, trans: str, **kwargs) -> bytes:
        """ Executes a requeset and returns the result as an
        XML bytes object that can be further parsed. """
        
    @staticmethod
    def load(name: str) -> 'MiApiContract':
        """ Creates a new MiApi object using an environment name to
        look-up connection details. """
        
    @staticmethod
    def save(name: str, host: str, port: str, pwd: str) -> NoReturn:
        """ Saves environment details for use later """
        
    @staticmethod
    def environments() -> List[Dict]:
        """ Returns all stored envoironments as a list containing a dict
        with the connection details, including password. """
        

class MiBaseContract(Protocol):
    ...
    
class MiDataContract(MiBaseContract):
    def __init__(self, api: MiApiContract):
        ...
        
    def __iter__(self) -> Iterator[Dict]:
        ...
        
    def __repr__(self) -> str:
        ...
        
    def __str__(self) -> str:
        ...
    
    
    