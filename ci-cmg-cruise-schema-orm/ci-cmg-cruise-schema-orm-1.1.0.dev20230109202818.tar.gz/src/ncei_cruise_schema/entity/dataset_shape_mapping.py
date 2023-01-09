from ..orm.entity import Entity, Column

class DatasetShapeMapping(Entity):

  @staticmethod
  def _table():
    return "dataset_shapes"

  def __init__(self, dataset_id=None, shape_id=None):
    self.__dataset_id = dataset_id
    self.__shape_id = shape_id

  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def shape_id(self):
    return self.__shape_id

  @shape_id.setter
  def shape_id(self, value):
    self.__shape_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("shape_id", cls.shape_id, id=True)
    )

