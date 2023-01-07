import os
import ast
import pickle
from ... import IoC_Container
from cryptography.fernet import Fernet
from .abstract.i_security_key import ISecurityKey
from .abstract.i_user_credentials import IUserCredentials


class UserCredentials(IUserCredentials):
    """
    Dependency Injection Design Pattern implemented. Constructor of this class 
    requires three parameters. One is user credentials, key file path and another 
    one is KeyManager class object, which is in ISecurityKey data type..  
    This Module is responsible for encrypting, decrypting, adding single or 
    multiple user credentials, finding those user credentials by User ID, 
    getting full list of credentials and most importantly if the Key gets 
    updated this will auto update all the excrypted information existing 
    user credentials with the new Key.
    Note: All the user credentials are stored in computer memory in binary
    fromet (pickle file). That is not human readable. This module also holds 
    a method which can convert this pickle file data into python dictionary.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self, user_credentials_file: str = None, key_path: str = None, key_obj: ISecurityKey = None):
        self.ioc_container = IoC_Container.CONTAINER
        self.file_path = user_credentials_file
        key_obj = self.ioc_container.resolve(ISecurityKey)
        self.key = key_obj.get_key(key_path)
        self.user_credentials_cache: dict = {}
    
    def add_multiple_credentials(self, user_credentials_dict: dict):
        if user_credentials_dict is not None:
            for user_id, password in user_credentials_dict.items():
                self.add_user_credentials(user_id, password)
            return self.ALL_INSERT_SUCCESS
        else:
            return self.FAIL_INSERT
    
    def add_user_credentials(self, user_id: str, password: str, updated_key: str = None):
        current_data: str = ""
        # Only if this method get any new key as argument that updated_key will be used for encryption.
        # If the this method dont get any value as argument for updated_key this method will.... 
        # update existing key as updated_key value.
        if updated_key is None:
            updated_key = self.key
        # If file is not created yet, here that file will be created first.
        if os.path.exists(self.file_path) is not True:
            # wb stands for Writing Bytes.
            with open(self.file_path, 'wb') as jar:
                pickle.dump("", jar)
            jar.close()
        else:
            # rb stands for Read Bytes.
            with open(self.file_path, 'rb') as jar:     # If file already exist, read operation will be conducted.
                current_data = pickle.load(jar)     # Collecting all the current data from the existing file. 
            jar.close()
        encrypted_data = Fernet(updated_key).encrypt(password.encode())     # Encrypting the plain text password
        # As currently existing credentials are stored at current_data variable,
        # Here current_data and new credentials are concatenating as updated_data
        # to append the new information.
        updated_data = current_data + '"' + user_id + '"' + ':' + '"' + encrypted_data.decode() + '",' + '\n'
        # wb stands for Writing Bytes.
        with open(self.file_path, 'wb') as jar:
            pickle.dump(updated_data, jar)  # Here updated_data is getting stored at computer memory.
        jar.close()
        return self.SUCCESS_INSERT
    

    def __encrypted_or_plain(self, encr_pwd, is_encrypted):
        # Get password encrypted or plaintext based on `is_encrypted`
        return  encr_pwd if is_encrypted else str(Fernet(self.key).decrypt(encr_pwd.encode()), 'utf-8')
    
    def get_all_users(self, is_encrypted=False):
        user_credentials_dict = {
            
        }
        if os.path.exists(self.file_path) and os.stat(self.file_path).st_size > 0:
            # Here r stands for Read mode  only
            with open(self.file_path, 'rb') as jar:
                file = str(pickle.load(jar))
                # As all the passwords are encrypted, this loop will traverse each credentials and decrypt
                for line in file.splitlines():
                    user_id, encr_pwd = line.split(":")
                    # For returning all the decrypted credentials this temporary Dictionary will be used.
                    user_credentials_dict[user_id] = self.__encrypted_or_plain(encr_pwd, is_encrypted)
                jar.close()
            return user_credentials_dict
        else:
            return self.EMPTY_RECORD

    def get_user_credentials_by_name(self, user_id: str):
            # As all data will be collected from the user_credentials_cache,
            # that must get updated from the actual user credential file.
            self.__update_user_credentials_cache()
            encr_pwd = self.user_credentials_cache[user_id]
            print("User ID Found!")
            if encr_pwd is not None:
                return str(Fernet(self.key).decrypt(encr_pwd.encode()), 'utf-8')
            else:
                return self.UNKNOWN_USER
    
    def update_encryption_new_key(self, new_key: str):
        if os.path.exists(self.file_path):
            try:
                current_user_credentials = self.__bytes_to_dict_converter() # Taking backup of existing credentials
                os.remove(self.file_path) # Removing pickle file (Existing user credentials)
                for user_id, encr_pwd in current_user_credentials.items():
                    pwd = str(Fernet(self.key).decrypt(encr_pwd.encode()), 'utf-8')
                    self.add_user_credentials(user_id, pwd, new_key) # Pickle file will be created again from this method.
                return self.NEW_KEY_ENCR_PWD
            except Exception as e:
                print(self.BUG_HEADER + "\n" + e)
                return e
        else:
            return self.EMPTY_RECORD
            
    def __update_user_credentials_cache(self):
        self.user_credentials_cache = self.__bytes_to_dict_converter()
        return self.CACHE_UPDATED
        
    def __bytes_to_dict_converter(self, path: str = None):
        # If this method is called without passing any argument for path 
        # path value will get updated as static path.
        if path is None:
            path = self.file_path
        temp_str: str
        if os.path.exists(path):
            # Checking do the file has anyting to convert or not.
            if os.stat(path).st_size > 0:
                # rb stands for Read Bytes.
                with open(self.file_path, 'rb') as jar:
                    temp_str = "{" + pickle.load(jar) + "}"
                    #- https://docs.python.org/3/library/ast.html
                    temp_str = ast.literal_eval(temp_str)   # Converting string to python dictionary.
                jar.close()
                return temp_str
            else:
                return self.EMPTY_RECORD
        else:
            return self.DB_NOT_FOUND
            
            
