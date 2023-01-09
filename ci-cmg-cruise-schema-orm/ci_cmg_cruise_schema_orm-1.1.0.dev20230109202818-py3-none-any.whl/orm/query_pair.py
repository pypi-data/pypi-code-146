class QueryPair(object):
  def __init__(self, query, params):
    self.__query = query
    self.__params = params

  @property
  def query(self):
    return self.__query

  @property
  def params(self):
    return self.__params