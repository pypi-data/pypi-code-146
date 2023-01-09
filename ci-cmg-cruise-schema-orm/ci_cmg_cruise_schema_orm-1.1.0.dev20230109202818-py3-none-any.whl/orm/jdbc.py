import jaydebeapi
from past.types import long

from .persistence import PersistenceEngine

class JdbcPersistenceEngine(PersistenceEngine):
  def __init__(
      self,
      url,
      driver_properties=None,
      driver_path=None,
      driver="oracle.jdbc.driver.OracleDriver",
      schema="cruise",
      debug_query=False,
      debug_params=False
  ):
    self.__driver = driver
    self.__url = url
    self.__driver_properties = driver_properties
    self.__driver_path = driver_path
    self.__debug_query = debug_query
    self.__debug_params = debug_params
    if schema:
      self.__schema = schema + "."
    else:
      self.__schema = ""

  def _debug_query(self):
    return self.__debug_query

  def _debug_params(self):
    return self.__debug_params

  def _schema(self):
    return self.__schema

  def _placeholder_func(self, name):
    return "?"

  def _set_clob(self, value):
    if value and "oracle.sql.CLOB" in type(value).__name__:
      return value.getSubString(long(1), int(value.length()))
    return value

  def _get_connection(self):
    connection = jaydebeapi.connect(
      self.__driver,
      self.__url,
      self.__driver_properties,
      self.__driver_path)
    connection.jconn.setAutoCommit(False)
    return connection