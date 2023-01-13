"""
Functionality related to encryption of files in qalx
"""

import os

import appdirs
from cryptography.fernet import Fernet

from ..core.utils import APPNAME, APPAUTHOR


class QalxEncrypt:
    """
    Provides functionality to encrypt and decrypt files
    """

    DEFAULT_KEY_PATH = os.path.join(
        appdirs.user_data_dir(APPNAME, APPAUTHOR), "qalx.key"
    )
    encryption_class = Fernet

    def __init__(self, key_file):
        self.key_file = key_file

    def load(self):
        """Read key_file in"""
        with open(self.key_file, "rb") as key_file:
            return self.encryption_class(key_file.read())

    def encrypt(self, file_bytes):
        """
        Encrypt file data.
        :param file_bytes:  The bytes to encrypt
        :return The encrypted bytes
        """
        return self.load().encrypt(file_bytes)

    def decrypt(self, file_bytes):
        """
        Decrypt file data.
        :param file_bytes:  The bytes to decrypt
        :return The decrypted bytes
        """
        return self.load().decrypt(file_bytes)

    @staticmethod
    def generate_key():
        """Return an encryption key"""
        return Fernet.generate_key()

    @classmethod
    def save_key(cls, key_path=None):
        """
        Saves a new encryption key to the provided file location

        :param key_path:    The path to the file where the new key will be saved
                            If None is provided, it defaults to DEFAULT_KEY_PATH
        """
        if key_path is None:
            key_path = cls.DEFAULT_KEY_PATH
        key = cls.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
