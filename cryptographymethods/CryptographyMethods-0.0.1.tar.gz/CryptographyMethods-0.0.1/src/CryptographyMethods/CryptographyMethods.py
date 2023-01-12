#!/bin/python3
""" Lab-93's implementation of Python's cryptographic capabilities.  Here are metho
"""
from base64 import urlsafe_b64encode
import hashlib as hashlib
from cryptography.fernet import Fernet

class CryptographyMethods():
  """ A collection of tools specifically dealing with the security
  of certain given credentials.

  One-Way SHA-256 hashes are implemented through self.SHA256()
  Two-Way Fernet encryption is implemented through self.Encryption()
    -- Custom keys are created with self.BuildKey(), which allows
       for the use of an 'imaginary' encr
  """

  def __init__(self):
    self = self 

  def SHA256(self, secret: str):
    """ Create a SHA-256 hash of whatever value is given. """
    return hashlib.sha256(secret.encode()).hexdigest()


  def BuildKey(self, key: str):
    """ Create a two-way encryption key using the first 32
    digits of the hash of a username and password strings.

        The results are then encoded in urlsafe-base64 bytes
    and returned to the caller. """
    basecode = self.SHA256(str(key))[:32]
    key = urlsafe_b64encode(basecode.encode())
    return key


  def Encryption(self, phrase: bytes, target: str):
    intelligence = Fernet(phrase)
    return intelligence.encrypt(bytes(target, 'utf-8'))
  

  def Decryption(self, phrase: bytes, target: str):
    intelligence = Fernet(phrase)
    return intelligence.decrypt(target)

