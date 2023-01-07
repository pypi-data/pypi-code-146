from abc import ABC, abstractmethod
from .i_security_key import ISecurityKey


class IUserCredentials(ABC):
    """
    This is an abstract class which is a skeleton for dealing with User Credentials
    with the Dependency Injection from ISecurityKey abstract class. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    # Output Messages
    UNKNOWN_USER = "User ID unknown."
    ALL_INSERT_SUCCESS = "All credentials inserted successfully."
    SUCCESS_INSERT = "New User Credentials has been inserted!"
    FAIL_INSERT = "Someting went wrong! Credentials are not inserted."
    EMPTY_RECORD = "Empty record!"
    CACHE_UPDATED = "User Credentials cache memory updated......."
    DB_NOT_FOUND = "Database not found!"
    NEW_KEY_ENCR_PWD = "Data encrypted with new Key successfully!"
    BUG_HEADER = "***ERROR******ERROR******ERROR******ERROR******ERROR******ERROR***"

    user_credentials_cache = {}
    """All user credentials with encrypted passwords will be stored here for fast access and operations. © BS23"""
    
    @abstractmethod
    def __init__(self, user_credentials_file: str = None, key_path: str = None, key_obj: ISecurityKey = None):
        """Constructor with Dependency Injection of ISecurityKey Abstract Method. © BS23"""
    
    @abstractmethod
    def add_multiple_credentials(self, user_credentials_dict: dict):
        """This method will be used when the requirement is to add multiple credentials at once. © BS23  """
        
    @abstractmethod
    def add_user_credentials(self, user_id: str, password: str, updated_key: str = None):
        """This method will add user details (encrypted) directly at pickle file. If the parameter 
        updated_key is None/Null this will encrypt the user credentials with the existing key assigned 
        at the constructor. And if an argument is passed as a parameter of this method's updated_key value
        all the existing user credentials will also get updated with the new encryption key. © BS23"""
        
    @abstractmethod
    def get_all_users(self):
        """This method will get data directly from the pickle and decrypt all the user password.
        Then retuen it in Python Dictionary format. © BS23"""
        
    @abstractmethod
    def get_user_credentials_by_name(self, user_id: str):
        """This method will take user id/name as parameter and will get user data from updated 
        cache (dict). Then decrypt user password and return it as string. © BS23"""
        
    @abstractmethod
    def update_encryption_new_key(self, new_key: str):
        """
        This method is only used when Key gets re-generated or updated. This method traverse each and 
        every user credential and re-encrypt those with updated Key. © BS23        
        """