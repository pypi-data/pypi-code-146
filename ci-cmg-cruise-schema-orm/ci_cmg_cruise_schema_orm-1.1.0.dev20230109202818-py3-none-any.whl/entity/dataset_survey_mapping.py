from ..orm.entity import Entity, Column

class DatasetSurveyMapping(Entity):

  @staticmethod
  def _table():
    return "dataset_surveys"

  def __init__(self, dataset_id=None, survey_id=None):
    self.__dataset_id = dataset_id
    self.__survey_id = survey_id

  @property
  def dataset_id(self):
    return self.__dataset_id

  @dataset_id.setter
  def dataset_id(self, value):
    self.__dataset_id = value

  @property
  def survey_id(self):
    return self.__survey_id

  @survey_id.setter
  def survey_id(self, value):
    self.__survey_id = value

  @classmethod
  def _columns(cls):
    return (
      Column("dataset_id", cls.dataset_id, id=True),
      Column("survey_id", cls.survey_id, id=True)
    )



