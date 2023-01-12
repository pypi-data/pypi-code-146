import logging
from getpass import getpass
from os.path import join
from pathlib import Path

from cryptography.fernet import Fernet

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BIN_FILE = join(str(Path.home()), 'mysql_bytes.bin')


class Encrypt:

    @classmethod
    def initialize(cls):
        password = getpass()
        password = password.encode()
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(password)  # Password required in bytes
        with open(BIN_FILE, 'wb') as file_object:
            file_object.write(ciphered_text)
        logging.info(f'Key: {key}')
