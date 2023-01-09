from ..orm.entity import Entity, Column
from ..orm.column_consts import DATE_PLACEHOLDER, date_select_name

class ParameterDetail(Entity):

  @staticmethod
  def _table():
    return "parameter_details"

  def __init__(self,
    id=None,
    parameter=None,
    description=None,
    last_update_date=None,
    last_updated_by=None
  ):
    self.__id = id
    self.__parameter = parameter
    self.__description = description
    self.__last_update_date = last_update_date
    self.__last_updated_by = last_updated_by


  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def parameter(self):
    return self.__parameter

  @parameter.setter
  def parameter(self, value):
    self.__parameter = value

  @property
  def description(self):
    return self.__description

  @description.setter
  def description(self, value):
    self.__description = value

  @property
  def last_update_date(self):
    return self.__last_update_date

  @last_update_date.setter
  def last_update_date(self, value):
    self.__last_update_date = value

  @property
  def last_updated_by(self):
    return self.__last_updated_by

  @last_updated_by.setter
  def last_updated_by(self, value):
    self.__last_updated_by = value


  @classmethod
  def _columns(cls):
    return (
      Column("parameter_id", cls.id, id=True, sequence="parameter_details_seq"),
      Column("parameter", cls.parameter),
      Column("description", cls.description),
      Column("last_update_date", cls.last_update_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
      Column("last_updated_by", cls.last_updated_by)
    )



