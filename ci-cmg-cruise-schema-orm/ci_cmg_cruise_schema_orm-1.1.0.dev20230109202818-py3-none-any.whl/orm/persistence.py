from .query import QueryRunner

class PersistenceContext:
  def __init__(
      self,
      cursor,
      placeholder_func,
      set_clob_func,
      schema ="",
      debug_query=False,
      debug_params=False):
    self.__cursor = cursor
    self.__placeholder_func = placeholder_func
    self.__schema = schema
    self.__debug_query = debug_query
    self.__debug_params = debug_params
    self.__set_clob_func = set_clob_func

  @property
  def cursor(self):
    return self.__cursor

  @property
  def placeholder_func(self):
    return self.__placeholder_func

  @property
  def schema(self):
    return self.__schema

  @property
  def debug_query(self):
    return self.__debug_query

  @property
  def debug_params(self):
    return self.__debug_params

  @property
  def set_clob_func(self):
    return self.__set_clob_func

class PersistenceEngine(object):

  def _debug_query(self):
    return False

  def _debug_params(self):
    return False

  def _create_cursor(self, connection):
    return connection.cursor()

  def _schema(self):
    return ""

  def _placeholder_func(self, i):
    pass

  def _get_connection(self):
    pass

  def _set_clob(self, value):
    return value

  def _create_context(self, cursor):
    return PersistenceContext(
      cursor=cursor,
      placeholder_func=self._placeholder_func,
      set_clob_func=self._set_clob,
      schema=self._schema(),
      debug_query=self._debug_query(),
      debug_params=self._debug_params()
    )

  def save(self, entity):
    connection = self._get_connection()
    try:
      with self._create_cursor(connection) as cursor:
        context = self._create_context(cursor)
        r = entity.save(context)
        connection.commit()
        return r
    except:
      connection.rollback()
      raise
    finally:
      connection.close()

  def load(self, id, cls):
    connection = self._get_connection()
    try:
      with self._create_cursor(connection) as cursor:
        context = self._create_context(cursor)
        m = getattr(cls, "load")
        r = m(id, context)
        connection.commit()
        return r
    except:
      connection.rollback()
      raise
    finally:
      connection.close()

  def delete(self, entity):
    connection = self._get_connection()
    try:
      with self._create_cursor(connection) as cursor:
        context = self._create_context(cursor)
        r = entity.delete(context)
        connection.commit()
        return r
    except:
      connection.rollback()
      raise
    finally:
      connection.close()

  def __get_setters(self, cls):
    columns = cls._columns()
    setters = []
    for column in columns:
      setters.append(column.field)
    return setters

  def find(self, cls, joins=None, where=None, frm=None, distinct=False, orders=None):
    connection = self._get_connection()
    try:
      with self._create_cursor(connection) as cursor:
        context = self._create_context(cursor)
        runner = QueryRunner()
        qp = runner.run(cls=cls, joins=joins, where=where, frm=frm, persistence_context=context, distinct=distinct, orders=orders)
        query = qp.query
        params= qp.params
        if context.debug_query:
          print(query)
        if context.debug_params:
          print(params)
        cursor.execute(query, params)
        r = cursor.fetchall()
        entities = []
        for row in r:
          entities.append(cls.from_row(row, context))
        connection.commit()
        return entities
    except:
      connection.rollback()
      raise
    finally:
      connection.close()



  def query(self, query, params=(), size=None):
    connection = self._get_connection()
    try:
      with self._create_cursor(connection) as cursor:
        context = self._create_context(cursor)
        if context.debug_query:
          print(query)
        if context.debug_params:
          print(params)
        cursor.execute(query, params)
        r = tuple()
        try:
          if size:
            r = cursor.fetchmany(size)
          else:
           r = cursor.fetchall()
        except:
          pass
        connection.commit()
        return r
    except:
      connection.rollback()
      raise
    finally:
      connection.close()
