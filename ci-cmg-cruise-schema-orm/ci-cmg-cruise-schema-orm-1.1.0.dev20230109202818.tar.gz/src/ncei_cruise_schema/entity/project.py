from ..orm.entity import Entity, Column

class Project(Entity):

  @staticmethod
  def _table():
    return "projects"
  
  def __init__(self, id=None, name=None):
    self.__id = id
    self.__name = name

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, value):
    self.__name = value

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @classmethod
  def _columns(cls):
    return (
      Column("project_id", cls.id, id=True, sequence="projects_seq"),
      Column("project_name", cls.name)
    )
