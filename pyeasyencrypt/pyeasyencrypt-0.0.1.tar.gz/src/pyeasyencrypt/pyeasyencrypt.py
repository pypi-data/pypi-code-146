# Generated using pyarchetype template
# pip install pyarchetype
# git clone https://github.com/redcorjo/pyarchetype.git
import logging, os
import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

class EasyEncrypt:
    KDF_ALGORITHM = hashes.SHA256()
    KDF_LENGTH = 32
    KDF_ITERATIONS = 120000

    def __init__(self, KDF_LENGTH=32, KDF_ITERATIONS=120000):
        self.KDF_LENGTH=KDF_LENGTH
        self.KDF_ITERATIONS=KDF_ITERATIONS

    def __fernet_key(self, password):
        key = base64.b64encode(f"{password:<32}".encode("utf-8"))
        my_fernet = Fernet(key=key)
        return my_fernet

    def encrypt_string(self, clear_string: str, password: str) -> (str):
        my_fernet = self.__fernet_key(password)
        cipher_bytes = my_fernet.encrypt(clear_string.encode("utf-8"))
        cipher_string = cipher_bytes.decode("utf-8")
        return cipher_string

    def decrypt_string(self, encrypted_string: str, password: str) -> str:
        my_fernet = self.__fernet_key(password)
        plaintext = my_fernet.decrypt(encrypted_string)
        clear_string = plaintext.decode("utf-8")
        return clear_string

def encrypt_string(clear_string, password):
    easyEncrypt = EasyEncrypt()
    encrypted_string = easyEncrypt.encrypt_string(clear_string, password)
    return encrypted_string

def decrypt_string(encrypted_string, password):
    easyEncrypt = EasyEncrypt()
    decrypted_string = easyEncrypt.decrypt_string(encrypted_string, password)
    return decrypted_string

def main():
    logger.debug("Main")
    clear_string = "hello world"
    password = "my password"
    easyEncrypt = EasyEncrypt()
    encrypted_string = easyEncrypt.encrypt_string(clear_string, password)
    decrypted_string = easyEncrypt.decrypt_string(encrypted_string, password)
    logger.info(f"clear_string={clear_string} decrypted_string={decrypt_string} password={password} encrypted_string={encrypted_string}")
    logger.debug("Done")

if __name__ == "__main__":
    main()
