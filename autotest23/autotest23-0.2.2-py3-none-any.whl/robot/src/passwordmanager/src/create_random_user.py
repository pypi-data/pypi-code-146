"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from .abstract.i_security_key import SecurityKey

class KeyTester(SecurityKey):
    
    def demo(self):
        print("Hello World!!!")
        
    def key_generator(self, key_path: str, user_credentials_path: str = None):
        print("Hello World Trial!!!")
    
    def get_key(self, key_path):
        print("Hello World Trial1111!!!")