from ..orm.entity import Entity, Column

class DatasetProjectMapping(Entity):

  @staticmethod
  def _table():
    return "dataset_projects"

  def __init__(self, dataset_id=None, project_id=None):
    self.__dataset_id = dataset_id
    self.__project_id = project_id

  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def project_id(self):
    return self.__project_id

  @project_id.setter
  def project_id(self, value):
    self.__project_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("project_id", cls.project_id, id=True)
    )

