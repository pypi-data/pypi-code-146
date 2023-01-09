from ..orm.entity import Entity, Column
from ..orm.column_consts import WKT_PLACEHOLDER, wkt_select_name

class Shape(Entity):

  @staticmethod
  def _table():
    return "shapes"

  def __init__(self, id=None, shape=None, geom_type=None, shape_type=None, link_id=None):
    self.__id = id
    self.__shape = shape
    self.__geom_type = geom_type
    self.__shape_type = shape_type
    self.__link_id = link_id

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def shape(self):
    return self.__shape

  @shape.setter
  def shape(self, value):
    self.__shape = value

  @property
  def geom_type(self):
    return self.__geom_type

  @geom_type.setter
  def geom_type(self, value):
    self.__geom_type = value

  @property
  def shape_type(self):
    return self.__shape_type

  @shape_type.setter
  def shape_type(self, value):
    self.__shape_type = value

  @property
  def link_id(self):
    return self.__link_id

  @link_id.setter
  def link_id(self, value):
    self.__link_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("shape_id", cls.id, id=True, sequence="shapes_seq"),
      Column("shape_type", cls.shape_type),
      Column("geom_type", cls.geom_type),
      Column("shape", cls.shape, placeholder=WKT_PLACEHOLDER, select_name_func=wkt_select_name, use_null=True, clob=True),
      Column("link_id", cls.link_id),
    )

