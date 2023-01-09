from ..orm.entity import Entity, Column
from ..orm.column_consts import DATE_PLACEHOLDER, date_select_name

class Survey(Entity):

  @staticmethod
  def _table():
    return "surveys"

  def __init__(
      self,
      id=None,
      name=None,
      parent=None,
      platform_name=None,
      start_date=None,
      end_date=None,
      departure_port=None,
      arrival_port=None,
      last_update=None,
      creation_date=None
  ):
    self.__id = id
    self.__name = name
    self.__parent = parent
    self.__platform_name = platform_name
    self.__start_date = start_date
    self.__end_date = end_date
    self.__departure_port = departure_port
    self.__arrival_port = arrival_port
    self.__last_update = last_update
    self.__creation_date = creation_date

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
  def parent(self):
    return self.__parent

  @parent.setter
  def parent(self, value):
    self.__parent = value

  @property
  def platform_name(self):
    return self.__platform_name

  @platform_name.setter
  def platform_name(self, value):
    self.__platform_name = value

  @property
  def start_date(self):
    return self.__start_date

  @start_date.setter
  def start_date(self, value):
    self.__start_date = value

  @property
  def end_date(self):
    return self.__end_date

  @end_date.setter
  def end_date(self, value):
    self.__end_date = value

  @property
  def departure_port(self):
    return self.__departure_port

  @departure_port.setter
  def departure_port(self, value):
    self.__departure_port = value

  @property
  def arrival_port(self):
    return self.__arrival_port

  @arrival_port.setter
  def arrival_port(self, value):
    self.__arrival_port = value

  @property
  def last_update(self):
    return self.__last_update

  @last_update.setter
  def last_update(self, value):
    self.__last_update = value

  @property
  def creation_date(self):
    return self.__creation_date

  @creation_date.setter
  def creation_date(self, value):
    self.__creation_date = value

  @classmethod
  def _columns(cls):
    return (
      Column("survey_id", cls.id, id=True, sequence="surveys_seq"),
      Column("survey_name", cls.name),
      Column("parent", cls.parent),
      Column("platform_name", cls.platform_name),
      Column("start_date", cls.start_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
      Column("end_date", cls.end_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
      Column("departure_port", cls.departure_port),
      Column("arrival_port", cls.arrival_port),
      Column("last_update", cls.last_update, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
      Column("creation_date", cls.creation_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name)
    )