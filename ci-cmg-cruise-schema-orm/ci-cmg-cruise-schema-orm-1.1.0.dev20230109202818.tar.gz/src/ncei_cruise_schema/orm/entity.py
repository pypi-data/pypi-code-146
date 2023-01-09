from .query import QueryRunner, Where, And
from .query_pair import QueryPair
NULL = 'NULL'

class Column(object):
  def __init__(
      self,
      name,
      field,
      id = False,
      placeholder = "?",
      select_name_func=None,
      sequence="",
      use_null=False,
      clob = False
  ):
    self.__name = name
    self.__placeholder = placeholder
    if select_name_func:
      self.__select_name_func = select_name_func
    else:
      self.__select_name_func = lambda name: name
    self.__field = field
    self.__id = id
    self.__sequence = sequence
    self.__use_null = use_null
    self.__clob = clob

  @property
  def name(self):
    return self.__name

  @property
  def placeholder(self):
    return self.__placeholder

  @property
  def select_name_func(self):
    return self.__select_name_func

  @property
  def field(self):
    return self.__field

  @property
  def id(self):
    return self.__id

  @property
  def sequence(self):
    return self.__sequence

  @property
  def use_null(self):
    return self.__use_null

  @property
  def clob(self):
    return self.__clob



class _ColumnProcessor(object):
  def __init__(self, column_name, placeholder, value, id, sequence, field, select_name_func, use_null):
    self.__column_name= column_name
    self.__placeholder = placeholder
    self.__value = value
    self.__id = id
    self.__sequence = sequence
    self.__field = field
    self.__select_name_func = select_name_func
    self.__use_null = use_null

  @property
  def column_name(self):
    return self.__column_name

  @property
  def placeholder(self):
    return self.__placeholder

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self, val):
    self.__value = val

  @property
  def id(self):
    return self.__id

  @property
  def sequence(self):
    return self.__sequence

  @property
  def field(self):
    return self.__field

  @property
  def select_name_func(self):
    return self.__select_name_func

  @property
  def use_null(self):
    return self.__use_null

class Entity(object):

  @classmethod
  def _columns(cls):
    pass

  @staticmethod
  def _table():
    pass

  def __execute(self, cursor, query, params, persistence_context):
    if persistence_context.debug_query:
      print(query)
    if persistence_context.debug_params:
      print(params)
    cursor.execute(query, params)

  def __resolve_placeholder(self, placeholder, column_name, persistence_context):
    return placeholder.replace("?", persistence_context.placeholder_func(column_name))

  def __checkExists(self, ids, processors, schema, persistence_context):
    table = self.__class__._table()
    cursor = persistence_context.cursor
    where_ids = []
    id = None
    for processor in processors:
      if processor.id:
        id = processor.column_name
        where_ids.append("{idColumnName}={idPlaceholder}"
                         .format(idColumnName=processor.column_name, idPlaceholder=processor.placeholder))
    query = ("SELECT COUNT({id}) FROM {schema}{table} WHERE {where_ids}"
      .format(id=id, schema=schema, table=table, where_ids=" AND ".join(where_ids)))
    params = ids
    self.__execute(cursor, query, params, persistence_context)
    result = cursor.fetchone()
    if result[0]:
      return True
    return False

  def __isInsert(self, processors, schema, persistence_context):
    ids = []
    for processor in processors:
      if processor.id:
        ids.append(processor.value)

    if not ids:
      return True
    for id in ids:
      if not id:
        return True
    for processor in processors:
      if processor.sequence:
        return False
    return not self.__checkExists(ids, processors, schema, persistence_context)

  def __insert(self, processors, persistence_context):
    schema = persistence_context.schema
    table = self.__class__._table()
    cursor = persistence_context.cursor

    column_names = []
    placeholders = []
    params = []

    for processor in processors:
      placeholder = processor.placeholder
      column_names.append(processor.column_name)
      placeholders.append(placeholder)
      if processor.id:
        sequence = processor.sequence
        if sequence:
          cursor.execute("SELECT {schema}{sequence}.nextval FROM dual".format(schema=schema, sequence=sequence))
          processor.value = cursor.fetchone()[0]
      if placeholder != NULL:
        params.append(processor.value)

    query = ("INSERT INTO {schema}{table} ({columns}) VALUES ({placeholders})"
             .format(schema=schema, table=table, columns=", ".join(column_names), placeholders=", ".join(placeholders)))

    return QueryPair(query, params)

  def __update(self, processors, persistence_context):
    schema = persistence_context.schema
    table = self.__class__._table()
    where_ids = []
    where_params = []
    set_statements = []
    set_params = []
    for processor in processors:
      column_name = processor.column_name
      placeholder = processor.placeholder
      value = processor.value
      name_placeholder = "{column_name}={placeholder}".format(column_name=column_name, placeholder=placeholder)
      if processor.id:
        where_ids.append(name_placeholder)
        where_params.append(value)
      else:
        set_statements.append(name_placeholder)
        if placeholder != NULL:
          set_params.append(value)

    query = ("UPDATE {schema}{table} SET {set_statements} WHERE {where_ids}"
             .format(schema=schema, table=table, set_statements=", ".join(set_statements), where_ids=" AND ".join(where_ids)))
    params = set_params + where_params

    return QueryPair(query, params)


  def __getColumnProcessors(self, persistence_context):
    columns = self.__class__._columns()
    processors = []
    for column in columns:
      field = column.field
      value = field.fget(self)
      placeholder = None
      if column.use_null and value == None:
        placeholder = NULL
      if placeholder != NULL:
        placeholder = self.__resolve_placeholder(column.placeholder, column.name, persistence_context)
      sequence = ""
      if column.id:
        sequence = column.sequence
      processors.append(_ColumnProcessor(column.name, placeholder, value, column.id, sequence, field, column.select_name_func, column.use_null))
    return  processors

  def save(self, persistence_context):
    cursor = persistence_context.cursor
    schema = persistence_context.schema
    table = self.__class__._table()

    processors = self.__getColumnProcessors(persistence_context)

    pair = None

    if self.__isInsert(processors, schema, persistence_context):
      pair = self.__insert(processors, persistence_context)
    else:
      pair = self.__update(processors, persistence_context)

    self.__execute(cursor, pair.query, pair.params, persistence_context)

    id = {}

    for processor in processors:
      if processor.id:
        id[processor.field] = processor.value

    loaded = self._load(id, persistence_context)
    if not loaded:
      raise RuntimeError("{table} row with ID {id} does not exist ".format(table=table,id=id))
    return self

  def _load(self, id, persistence_context):
    if not id:
      raise RuntimeError("ID is required")
    cursor = persistence_context.cursor
    where_ids = []
    wheres = []
    processors = self.__getColumnProcessors(persistence_context)
    for processor in processors:
      if processor.id:
        where_ids.append("{column_name}={placeholder}"
                         .format(column_name=processor.column_name, placeholder=processor.placeholder))
        if isinstance(id, dict):
          key = processor.field
          id_value = id.get(key)
          if not id_value:
            raise RuntimeError("Missing ID key")
          wheres.append(Where(cls=self.__class__, field=key, op="=", value=id_value))
        else:
          wheres.append(Where(cls=self.__class__, field=processor.field, op="=", value=id))

    where = wheres[0]
    if len(wheres):
      where = And(wheres)

    runner = QueryRunner()
    qp = runner.run(cls=self.__class__, where=where, persistence_context=persistence_context)
    query = qp.query
    params= qp.params

    self.__execute(cursor, query, params, persistence_context)
    result = cursor.fetchone()

    if not result:
      return False

    self._from_row(result, persistence_context)
    return True

  def delete(self, persistence_context):
    cursor = persistence_context.cursor
    schema = persistence_context.schema
    table = self.__class__._table()
    columns = self.__class__._columns()
    idColumnName = None
    idPlaceholder = None
    idGetter = None
    for column in columns:
      if column.id:
        idGetter = column.field
        idColumnName = column.select_name_func(column.name)
        idPlaceholder = self.__resolve_placeholder(column.placeholder, column.name, persistence_context)
        break
    id = None
    if idGetter:
      id = idGetter.fget(self)
    if id:
      query = ("DELETE FROM {schema}{table} WHERE {idColumnName}={idPlaceholder}"
               .format(schema=schema, table=table,
                       idColumnName=idColumnName, idPlaceholder=idPlaceholder))
      params = (id,)
      self.__execute(cursor, query, params, persistence_context)
    return self

  def _from_row(self, row, persistence_context):
    columns = self.__class__._columns()
    for i in range(len(columns)):
      column = columns[i]
      if column.clob:
        column.field.fset(self, persistence_context.set_clob_func(row[i]))
      else:
        column.field.fset(self, row[i])

  @classmethod
  def from_row(cls, row, persistence_context):
    inst = cls()
    inst._from_row(row, persistence_context)
    return inst

  @classmethod
  def load(cls, id, persistenceContext):
    inst = cls()
    loaded = inst._load(id, persistenceContext)
    if not loaded:
      return None
    return inst

