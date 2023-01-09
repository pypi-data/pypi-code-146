from .query_pair import QueryPair


class _ConditionCriterion(object):
  def __init__(self, criteria, op):
    self.criteria = criteria
    self.op = op

  def get(self, get_alias, persistence_context):
    c = []
    params = []
    for criterion in self.criteria:
      qp = criterion.get(get_alias, persistence_context)
      c.append(qp.query)
      for p in qp.params:
        params.append(p)
    query = "( {c} )".format(c=" {op} ".format(op=self.op).join(c))
    return QueryPair(query, params)


class Or(_ConditionCriterion):
  def __init__(self, criteria):
    super(Or, self).__init__(criteria, "OR")


class And(_ConditionCriterion):
  def __init__(self, criteria):
    super(And, self).__init__(criteria, "AND")

class Not(object):
  def __init__(self, where):
    self.where = where

  def get(self, get_alias, persistence_context):
    qp = self.where.get(get_alias, persistence_context)
    query = "NOT ( {c} )".format(c=qp.query)
    return QueryPair(query, qp.params)

class Order(object):
  def __init__(self, cls, field, direction="ASC"):
    self.cls = cls
    self.field = field
    self.direction = direction

  def __resolve_column(self):
    columns = self.cls._columns()
    for column in columns:
      if column.field == self.field:
        return column.name

  def get(self, get_alias):
    alias = get_alias(self.cls)
    column = self.__resolve_column()
    return "{alias}.{column} {direction}".format(alias=alias, column=column, direction=self.direction)


class Where(object):
  def __init__(self, cls, field, op=None, value=None, is_null=False):
    self.cls = cls
    self.field = field
    self.op = op
    self.value = value
    self.is_null = is_null

  def __resolve_placeholder(self, column, persistence_context):
    placeholder = column.placeholder
    return placeholder.replace("?", persistence_context.placeholder_func(column.name))

  def __resolve_column(self):
    columns = self.cls._columns()
    for column in columns:
      if column.field == self.field:
        return column

  def get(self, get_alias, persistence_context):
    alias = get_alias(self.cls)
    column = self.__resolve_column()
    params = []
    if self.is_null:
      query = "{alias}.{column} IS NULL".format(alias=alias, column=column.name)
    else:
      placeholder = self.__resolve_placeholder(column, persistence_context)
      query = "{alias}.{column} {op} {placeholder}".format(alias=alias, column=column.name, op=self.op, placeholder=placeholder)
      params.append(self.value)
    return QueryPair(query, params)


class Join(object):
  def __init__(self, left_cls, left_field, op, right_cls, right_field,
      type="INNER"):
    self.left_cls = left_cls
    self.left_field = left_field
    self.op = op
    self.right_cls = right_cls
    self.right_field = right_field
    self.type = type

  def __resolveColumn(self, cls, field):
    columns = cls._columns()
    for column in columns:
      if column.field == field:
        return column.name

  def get(self, schema, get_alias):
    right_table = self.right_cls._table()
    left_alias = get_alias(self.left_cls)
    right_alias = get_alias(self.right_cls)
    left_column = self.__resolveColumn(self.left_cls, self.left_field)
    right_column = self.__resolveColumn(self.right_cls, self.right_field)
    query = (
    "{type} JOIN {schema}{right_table} {right_alias} ON {left_alias}.{left_column} {op} {right_alias}.{right_column}"
      .format(
      type=self.type,
      schema=schema,
      right_table=right_table,
      right_alias=right_alias,
      left_alias=left_alias,
      op=self.op,
      left_column=left_column,
      right_column=right_column)
    )
    return query


class QueryRunner(object):

  def __getColumns(self, cls, alias):
    columns = cls._columns()
    column_names = []
    for column in columns:
      column_names.append(column.select_name_func("{alias}.{name}".format(alias=alias, name=column.name)))
    return ", ".join(column_names)

  def run(self, cls, persistence_context, where=None, joins=None, frm=None, distinct=False, orders=None):
    schema = persistence_context.schema

    params = []
    table_alias = {}

    def get_alias(table_cls):
      alias = table_alias.get(table_cls)
      if not alias:
        alias = "t{i}".format(i=len(table_alias))
        table_alias[table_cls] = alias
      return alias

    cls_alias = get_alias(cls)
    columns = self.__getColumns(cls, cls_alias)

    if frm:
      left_alias = get_alias(frm)
      left_table = frm._table()
    else:
      left_alias = get_alias(cls)
      left_table = cls._table()

    distinct_t = ""
    if distinct:
      distinct_t = "DISTINCT "


    select = "SELECT {distinct}{columns}".format(columns=columns, distinct=distinct_t)
    frm = "FROM {schema}{left_table} {left_alias}".format(schema=schema, left_table=left_table, left_alias=left_alias)
    join_queries = []
    if joins:
      for join in joins:
        join_queries.append(join.get(schema, get_alias))
    where_q = ""
    if where:
      qp = where.get(get_alias, persistence_context)
      where_q = "WHERE {where}".format(where=qp.query)
      for p in qp.params:
        params.append(p)

    order = ""
    if orders:
      order_strs = []
      for o in orders:
        order_strs.append(o.get(get_alias))
      order = "ORDER BY {orders}".format(orders=", ".join(order_strs))

    query = ("{select} {frm} {joins} {where} {order}"
             .format(select=select,
                     frm=frm,
                     joins=" ".join(join_queries),
                     where=where_q,
                     order=order
                     ))

    return QueryPair(query, params)
