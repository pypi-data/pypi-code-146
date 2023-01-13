#!/bin/python3
from base64 import urlsafe_b64encode
import hashlib as hashlib
from cryptography.fernet import Fernet

"""
The cryptogram class enscapulates methods used for keeping
secrets in both one-way and two-way forms.

SHA-256 is delivered in a much simpler syntax than the default method
utilized by hashlib; the CryptographyMethods.SHA256 object merely
requires a secret to be hashed and delivers the hexdigest of the
resulting byte object.

For two-way secret keeping CryptographyMethods.Encryption and
CryptographyMethods.Decryption are offered; both of which utilize the
CryptographyMethods.BuildKey function for locking and unlocking secrets,
respectively.
"""

def SHA256(secret="test"):
  """
  Create a SHA-256 hash of whatever value is given as 'secret' and
  return the the hexdigest of the bytes-encoded secret.
  """
  return hashlib.sha256(secret.encode()).hexdigest()


def BuildKey(key="test"):
  """
  Create a two-way encryption token using the first 32
  digits of the hash of a given string named 'key'.

  The results are then encoded in urlsafe-base64 bytes
  and returned to the caller.
  """
  basecode = SHA256(str(key))[:32]
  return urlsafe_b64encode(basecode.encode())


def Encryption(phrase=BuildKey(), secret="test"):
  """
  Encrypt a secret string using a byte 'phrase' provided by
  CryptographyMethods.BuildKey as an encryption token.
  """
  intelligence = Fernet(phrase)
  return intelligence.encrypt(bytes(secret, 'utf-8'))


def Decryption(phrase=BuildKey(), secret="test"):
  """
  Decrypt a secret string using a byte 'phrase' provided by
  CryptographyMethods.BuildKey as an encryption token.
  """
  intelligence = Fernet(phrase)
  return intelligence.decrypt(secret)
