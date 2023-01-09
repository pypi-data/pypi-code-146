from ..orm.entity import Entity, Column

class DatasetInstrumentMapping(Entity):

  @staticmethod
  def _table():
    return "dataset_instruments"

  def __init__(self, dataset_id=None, instrument_id=None):
    self.__dataset_id = dataset_id
    self.__instrument_id = instrument_id

  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def instrument_id(self):
    return self.__instrument_id

  @instrument_id.setter
  def instrument_id(self, value):
    self.__instrument_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("instrument_id", cls.instrument_id, id=True)
    )



