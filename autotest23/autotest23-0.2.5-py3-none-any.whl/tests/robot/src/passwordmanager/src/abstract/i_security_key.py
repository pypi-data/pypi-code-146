from abc import ABC, abstractmethod 


class ISecurityKey(ABC):
    """
    This is an abstract class which is a skeleton for dealing with Encryption key
    functionality. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    # Output Messages
    NEW_NEY_SUCCESS:str = None
    """This constant value holds the success message which can be returned or printed in the methods. © BS23"""
    KEY_NOT_FOUND:str = None
    """This constant value holds the error message which can be returned or printed in the methods. © BS23"""
    
    @abstractmethod
    def __init__(self) -> None:
        pass    
    
    @abstractmethod
    def key_generator(self, key_path: str, user_credentials_path: str = None):
        """This method can take two parameters. One is for key file path and another one is user credentials file path.
        Both file path should be extention included (key & pickle). This can Create or Update security key. If user_credentials_path 
        is not None, this method will also auto update all the existing user credentials. © BRAIN STATION 23"""
        
    @abstractmethod
    def get_key(self, key_path):
        """ This method will take parameter of key path (including extention) and return security key as string. © BRAIN STATION 23"""