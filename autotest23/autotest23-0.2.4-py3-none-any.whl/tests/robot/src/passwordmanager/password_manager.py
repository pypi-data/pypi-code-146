"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from .constants import *
from ..abstract.menu import Menu
from .src.abstract.i_security_key import ISecurityKey
from .src.abstract.i_user_credentials import IUserCredentials
from .. import ObjMapper
from .. import IoC_Container


class PasswordManager(Menu):
    """
    PasswordManager is a special service because, as this micro-framework
    willbe included in the back-end application and automation test engineer
    may need to design test plans with data driven testing. Then this service 
    will keep the important data secure (encrypted). So when the Data is needed
    this service can just decrypt the data to use it in the data driven testing.
    Note: This PasswordManager can also generate encryption/decryption keys. And 
    if the key gets updated all the encrypted value will auto update its encryption 
    with the newly generatged key.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    banner = '''
    ------------------------------------------------------------------------
    ----------------------------Password Manager----------------------------
    ------------------------------------------------------------------------ 
    '''
     
    option_menu = '''
    [1] Generate a new Key
    [2] Load Current Key
    [3] Create new Username & Password
    [4] Make a random Username & Password
    [5] Load existing User Credentials
    [6] Get Credentials by User ID
    [7] Automation
    [0] Exit
    '''
    
    def __init__(self):
        self.ioc_container = IoC_Container.CONTAINER
        self.key_path =  KEY_FILE_PATH
        self.user_credentials_file = USER_CREDENTIALS_FILE_PATH
        self.key_generator_obj: ISecurityKey = self.ioc_container.resolve(ISecurityKey)

    def get_indexed(self):
        ObjMapper.OBJ_MAP['password_manager'] = ObjMapper.remember(self) 
        
    def display(self):
        print(self.banner)
        print(self.option_menu)       
        
    def get_input(self):
        return super().get_input()
    
    def switch_options(self, choice: int):
        user_cred_obj: IUserCredentials = self.ioc_container.resolve(IUserCredentials)
        # This switch case is addad from python 3.10 version.
        # So if anyone using python version below 3.10, please replace switch case with if-else.  
        # https://docs.python.org/3.10/whatsnew/3.10.html#pep-634-structural-pattern-matching
        match choice:
            case 1:
                 print(self.key_generator_obj.key_generator(self.key_path, self.user_credentials_file))
            case 2:
                 print(self.key_generator_obj.get_key(self.key_path))
            case 3:
                #  Dependency Injection Design Pattern
                user_cred_obj = user_cred_obj
                user_id = input("Enter username:")
                password = input("Enter password/token:")
                print(user_cred_obj.add_user_credentials(user_id, password))
            case 5:
                user_cred_obj = user_cred_obj
                print(user_cred_obj.get_all_users())
            case 6:
                if os.path.exists(self.user_credentials_file):
                    user_cred_obj = user_cred_obj
                    user_id = input("Please provide an user name:")
                    print(user_cred_obj.get_user_credentials_by_name(user_id))
                else:
                    print("Empty record! Please, add some user credentials first.")
            case 0:
                id = ObjMapper.OBJ_MAP['robo_manager']
                route = ObjMapper.id2obj(id)
                route.menu()
                return None
            case _:
                raise ValueError("Not an option")
        # After a Successful operation getting back to current Menu for further actions
        self.menu()
        
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)
