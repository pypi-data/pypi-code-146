from os.path import join
from pathlib import Path

from cryptography.fernet import Fernet

BIN_FILE = join(str(Path.home()), 'mysql_bytes.bin')


class Decrypt:

    @classmethod
    def initialize(cls, key):
        cipher_suite = Fernet(key)
        with open(BIN_FILE, 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = (cipher_suite.decrypt(encryptedpwd))
        plain_text_encryptedpassword = bytes(uncipher_text).decode("utf-8")  # convert to string
        return plain_text_encryptedpassword
