from ..orm.entity import Entity, Column

class FileShapeMapping(Entity):

  @staticmethod
  def _table():
    return "file_shapes"

  def __init__(self, file_id=None, shape_id=None):
    self.__file_id = file_id
    self.__shape_id = shape_id

  @property
  def shape_id(self):
    return self.__shape_id

  @shape_id.setter
  def shape_id(self, value):
    self.__shape_id = value

  @property
  def file_id(self):
    return self.__file_id

  @file_id.setter
  def file_id(self, value):
    self.__file_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("file_id", cls.file_id, id=True),
      Column("shape_id", cls.shape_id, id=True)
    )
