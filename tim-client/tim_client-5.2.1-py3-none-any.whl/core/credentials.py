from typing import Optional
from .server import server as default_server

class Credentials:
  __email: Optional[str] = None
  __password: Optional[str] = None
  __token: Optional[str] = None
  __token_expiration: str = ""
  __server: Optional[str] = None
  __client_name: Optional[str] = None

  def __init__(
      self,
      email: str,
      password: str,
      server: str = default_server,
      client_name: str = "Python Client",
  ):
    self.__email = email
    self.__password = password
    self.__server = server
    self.__client_name = client_name

  @property
  def email(self):
    return self.__email

  @property
  def token(self):
    return self.__token

  @property
  def password(self):
    return self.__password

  @property
  def server(self):
    return self.__server

  @property
  def client_name(self):
    return self.__client_name

  @property
  def token_expiration(self):
    return self.__token_expiration

  @token.setter
  def token(self, token: str):
    self.__token = token

  @token_expiration.setter
  def token_expiration(self, token_expiration: str):
    self.__token_expiration = token_expiration