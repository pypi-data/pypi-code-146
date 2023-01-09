from ..orm.entity import Entity, Column

class FileFormat(Entity):

  @staticmethod
  def _table():
    return "file_formats"

  def __init__(
      self,
      id=None,
      name=None,
      description=None
  ):
    self.__id = id
    self.__name = name
    self.__description = description

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, value):
    self.__name = value

  @property
  def description(self):
    return self.__description

  @description.setter
  def description(self, value):
    self.__description = value

  @classmethod
  def _columns(cls):
    return (
        Column("format_id", cls.id, id=True, sequence="file_formats_seq"),
        Column("format_name", cls.name),
        Column("format_description", cls.description)
    )

