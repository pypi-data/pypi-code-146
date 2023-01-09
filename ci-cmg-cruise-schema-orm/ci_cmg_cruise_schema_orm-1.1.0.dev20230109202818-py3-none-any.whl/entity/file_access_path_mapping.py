from ..orm.entity import Entity, Column

class FileAccessPathMapping(Entity):

  @staticmethod
  def _table():
    return "file_access_paths"

  def __init__(self, file_id=None, access_path_id=None):
    self.__file_id = file_id
    self.__access_path_id = access_path_id

  @property
  def file_id(self):
    return self.__file_id

  @file_id.setter
  def file_id(self, value):
    self.__file_id = value

  @property
  def access_path_id(self):
    return self.__access_path_id

  @access_path_id.setter
  def access_path_id(self, value):
    self.__access_path_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("file_id", cls.file_id, id=True),
      Column("path_id", cls.access_path_id, id=True)
    )



