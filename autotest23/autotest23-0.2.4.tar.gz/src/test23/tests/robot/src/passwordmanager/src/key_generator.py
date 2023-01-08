import os.path
from cryptography.fernet import Fernet
from .abstract.i_security_key import ISecurityKey
from .abstract.i_user_credentials import IUserCredentials
from ... import IoC_Container

class KeyManager(ISecurityKey):
    """
    This Module is responsible for generating new key and its destrivution.
    Note: If a new key is created, it will automatically update the encryption 
    of the existing passwords with the new key. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self):
        self.key = None
        self.ioc_container = IoC_Container.CONTAINER
        self.NEW_NEY_SUCCESS = "New key has been generated! 🗝"
        self.KEY_NOT_FOUND = "No key generated! Please, create a key first."
        
    def key_generator(self, key_path: str, user_credentials_path: str = None):
        # Generating a new Key
        new_key = Fernet.generate_key()     
        # Cheking if this Key generating process is first time of not.
        if os.path.exists(key_path): 
            # If this key generating process is not first time 
            # then this will go to check if there is any existing 
            # user credentials or not
            user_credentials_obj = self.ioc_container.resolve(IUserCredentials)
            #UserCredentials(user_credentials_path, key_path, self)
            # If any user credentials are found this method will 
            # update those encryption with the newly generated key.
            user_credentials_obj.update_encryption_new_key(new_key)
        with open(key_path, 'wb') as file:  #wb stands for Writing Bytes.
            file.write(new_key)
        self.key = new_key
        return self.NEW_NEY_SUCCESS
        
    def get_key(self, key_path):
        if os.path.exists(key_path):
            # rb stands for Read Bytes.
            with open(key_path, 'rb') as file:
                self.key = file.read()
            return str(self.key, 'utf-8')
        else:
            return self.KEY_NOT_FOUND
      