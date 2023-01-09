from ..orm.entity import Entity, Column

class DatasetPlatformMapping(Entity):

  @staticmethod
  def _table():
    return "dataset_platforms"

  def __init__(self, dataset_id=None, platform_id=None):
    self.__dataset_id = dataset_id
    self.__platform_id = platform_id

  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def platform_id(self):
    return self.__platform_id

  @platform_id.setter
  def platform_id(self, value):
    self.__platform_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("platform_id", cls.platform_id, id=True)
    )



