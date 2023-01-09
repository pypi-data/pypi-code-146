from ..orm.entity import Entity, Column

class DatasetType(Entity):

  @staticmethod
  def _table():
    return "dataset_types"

  def __init__(self, id=None, name=None, description=None):
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
      Column("type_id", cls.id, id=True, sequence="dataset_types_seq"),
      Column("type_name", cls.name),
      Column("type_description", cls.description)
    )
