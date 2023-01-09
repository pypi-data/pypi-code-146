from ..orm.entity import Entity, Column

class DatasetSourceMapping(Entity):

  @staticmethod
  def _table():
    return "sources"

  def __init__(
      self,
      dataset_id=None,
      contact_id=None,
      group=None,
  ):
    self.__dataset_id = dataset_id
    self.__contact_id = contact_id
    self.__group = group


  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def contact_id(self):
    return self.__contact_id

  @contact_id.setter
  def contact_id(self, value):
    self.__contact_id = value

  @property
  def group(self):
    return self.__group

  @group.setter
  def group(self, value):
    self.__group = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("contact_id", cls.contact_id, id=True),
      Column("source_group", cls.group)
    )

