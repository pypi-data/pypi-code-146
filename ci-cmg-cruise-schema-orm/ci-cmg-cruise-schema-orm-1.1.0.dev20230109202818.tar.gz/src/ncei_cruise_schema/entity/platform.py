from ..orm.entity import Entity, Column


class Platform(Entity):

  @staticmethod
  def _table():
    return "platforms"

  def __init__(
      self,
      id=None,
      name=None,
      internal_name=None,
      long_name=None,
      type=None,
      docucomp_uuid=None,
      designator=None
  ):
    self.__id = id
    self.__name = name
    self.__internal_name = internal_name
    self.__long_name = long_name
    self.__type = type
    self.__docucomp_uuid = docucomp_uuid
    self.__designator = designator

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
  def long_name(self):
    return self.__long_name

  @long_name.setter
  def long_name(self, value):
    self.__long_name = value

  @property
  def internal_name(self):
    return self.__internal_name

  @internal_name.setter
  def internal_name(self, value):
    self.__internal_name = value

  @property
  def type(self):
    return self.__type

  @type.setter
  def type(self, value):
    self.__type = value

  @property
  def designator(self):
    return self.__designator

  @designator.setter
  def designator(self, value):
    self.__designator = value

  @property
  def docucomp_uuid(self):
    if self.__docucomp_uuid:
      return self.__docucomp_uuid.lower()
    return self.__docucomp_uuid

  @docucomp_uuid.setter
  def docucomp_uuid(self, value):
    self.__docucomp_uuid = value

  @classmethod
  def _columns(cls):
    return (
      Column("platform_id", cls.id, id=True, sequence="platforms_seq"),
      Column("platform_name", cls.name),
      Column("long_name", cls.long_name),
      Column("internal_name", cls.internal_name),
      Column("platform_type", cls.type),
      Column("docucomp_uuid", cls.docucomp_uuid),
      Column("designator", cls.designator)
    )
