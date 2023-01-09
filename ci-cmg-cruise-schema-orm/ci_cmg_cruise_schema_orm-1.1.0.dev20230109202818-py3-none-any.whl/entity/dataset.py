from ..orm.entity import Entity, Column
from ..orm.column_consts import DATE_PLACEHOLDER, date_select_name, WKT_PLACEHOLDER, wkt_select_name

class Dataset(Entity):

  @staticmethod
  def _table():
    return "datasets"

  def __init__(
      self,
      id=None,
      other_id=None,
      name=None,
      dataset_type_name=None,
      dataset_type_id=None,
      instruments=None,
      platforms=None,
      doi=None,
      shape=None,
      archive_date=None,
      last_update=None,
      surveys=None,
      projects=None
  ):
    self.__id = id
    self.__other_id = other_id
    self.__name = name
    self.__dataset_type_name = dataset_type_name
    self.__dataset_type_id = dataset_type_id
    self.__instruments = instruments
    self.__platforms = platforms
    self.__doi = doi
    self.__shape = shape
    self.__archive_date = archive_date
    self.__last_update = last_update
    self.__surveys = surveys
    self.__projects = projects


  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def other_id(self):
    return self.__other_id

  @other_id.setter
  def other_id(self, value):
    self.__other_id = value

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, value):
    self.__name = value

  @property
  def dataset_type_name(self):
    return self.__dataset_type_name

  @dataset_type_name.setter
  def dataset_type_name(self, value):
    self.__dataset_type_name = value

  @property
  def dataset_type_id(self):
    return self.__dataset_type_id

  @dataset_type_id.setter
  def dataset_type_id(self, value):
    self.__dataset_type_id = value

  @property
  def instruments(self):
    return self.__instruments

  @instruments.setter
  def instruments(self, value):
    self.__instruments = value

  @property
  def platforms(self):
    return self.__platforms

  @platforms.setter
  def platforms(self, value):
    self.__platforms = value

  @property
  def doi(self):
    return self.__doi

  @doi.setter
  def doi(self, value):
    self.__doi = value

  @property
  def shape(self):
    return self.__shape

  @shape.setter
  def shape(self, value):
    self.__shape = value

  @property
  def archive_date(self):
    return self.__archive_date

  @archive_date.setter
  def archive_date(self, value):
    self.__archive_date = value

  @property
  def last_update(self):
    return self.__last_update

  @last_update.setter
  def last_update(self, value):
    self.__last_update = value

  @property
  def surveys(self):
    return self.__surveys

  @surveys.setter
  def surveys(self, value):
    self.__surveys = value

  @property
  def projects(self):
    return self.__projects

  @projects.setter
  def projects(self, value):
    self.__projects = value

  @classmethod
  def _columns(cls):
    return (
       Column("dataset_id", cls.id, id=True, sequence="datasets_seq"),
       Column("other_id", cls.other_id),
       Column("dataset_name", cls.name),
       Column("dataset_type_name", cls.dataset_type_name),
       Column("dataset_type_id", cls.dataset_type_id),
       Column("instruments", cls.instruments),
       Column("platforms", cls.platforms),
       Column("doi", cls.doi),
       Column("shape", cls.shape, placeholder=WKT_PLACEHOLDER, select_name_func=wkt_select_name, use_null=True, clob=True),
       Column("archive_date", cls.archive_date, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
       Column("last_update", cls.last_update, placeholder=DATE_PLACEHOLDER, select_name_func=date_select_name),
       Column("surveys", cls.surveys),
       Column("projects", cls.projects)
    )