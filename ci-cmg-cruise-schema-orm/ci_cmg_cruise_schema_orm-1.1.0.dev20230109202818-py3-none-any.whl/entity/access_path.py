from ..orm.entity import Entity, Column

class AccessPath(Entity):

  @staticmethod
  def _table():
    return "access_paths"

  def __init__(self, id=None, path=None, path_type=None):
    self.__id = id
    self.__path = path
    self.__path_type = path_type

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def path(self):
    return self.__path

  @path.setter
  def path(self, value):
    self.__path = value

  @property
  def path_type(self):
    return self.__path_type

  @path_type.setter
  def path_type(self, value):
    self.__path_type = value

  @classmethod
  def _columns(cls):
    return (
      Column("path_id", cls.id, id=True, sequence="access_paths_seq"),
      Column("path", cls.path),
      Column("path_type", cls.path_type)
    )

