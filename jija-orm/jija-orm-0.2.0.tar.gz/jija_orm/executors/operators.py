from abc import ABC
from jija_orm.executors import sql_object, functions, comparators, processors


class Operator(sql_object.TemplateSqlObject, ABC):
    PRIORITY = NotImplemented
    COMPARABLE = False
    EXTRA = []

    def get_table_name(self):
        from jija_orm import models
        if isinstance(self.model, str):
            return self.correct_name(self.model)

        if issubclass(self.model, models.Model):
            return self.correct_name(self.model.get_name())

        raise TypeError(f'Invalid type of model: {type(self.model)}')


class Select(Operator):
    PRIORITY = 0
    TEMPLATE = 'select {distinct}{fields} from {table_name}'

    def __init__(self, *fields, distinct=False, **alias):
        objects = []
        for field in fields:
            objects.append(field if isinstance(field, sql_object.SimpleSQLObject) else sql_object.Field(field))

        for field, name in alias.items():
            objects.append(functions.Alias(name, field))

        self.__distinct = distinct
        super().__init__(objects)

    def get_template_params(self):
        return {
            'fields': ', '.join(self.objects_query) if self.objects_query else '*',
            'distinct': 'distinct ' if self.__distinct else '',
            'table_name': self.get_table_name()
        }


class Insert(Operator):
    PRIORITY = 0
    TEMPLATE = 'insert into {table_name} ({fields}) values ({values}) returning *'
    EXTRA = [processors.Single()]

    def __init__(self, **kwargs):
        fields = []
        values = {}

        for field, value in kwargs.items():
            fields.append(field if isinstance(field, sql_object.SimpleSQLObject) else sql_object.Field(field))
            values[field] = value if isinstance(value, sql_object.SimpleSQLObject) else sql_object.Value(value, field)

        super().__init__({
            'fields': sql_object.SQLObject(fields),
            'values': sql_object.SQLObject(values)
        })

    def get_template_params(self):
        return {
            'fields': ', '.join(self.objects['fields'].objects_query),  # TODO ???
            'values': ', '.join(map(str, self.objects['values'].objects_query.values())),
            'table_name': self.get_table_name()
        }


class InsertRow(Operator):
    TEMPLATE = '({values})'

    def __init__(self, fields, values):
        objects = []

        for field in fields:
            value = values.get(field)
            objects.append(value if isinstance(value, sql_object.SimpleSQLObject) else sql_object.Value(value, field))

        super().__init__([sql_object.SQLObject(objects)])

    def get_template_params(self):
        return {'values': ', '.join(map(str, self.objects[0].objects_query))}


class MultipleInsert(Operator):
    PRIORITY = 0
    TEMPLATE = 'insert into {table_name} ({fields}) values {rows} returning *'

    def __init__(self, rows):
        rows_fields = self.get_fields(rows)

        fields = []
        for field in rows_fields:
            fields.append(sql_object.Field(field))

        values = []
        for index in range(len(rows)):
            values.append(InsertRow(rows_fields, rows[index]))

        super().__init__({
            'fields': sql_object.SQLObject(fields),
            'rows': sql_object.SQLObject(values)
        })

    @staticmethod
    def get_fields(rows):
        model_fields = set()
        for row in rows:
            model_fields.update(row.keys())

        return sorted(list(model_fields))

    def get_template_params(self):
        return {
            'fields': ', '.join(self.objects['fields'].objects_query),
            'rows': ', '.join(self.objects['rows'].objects_query),
            'table_name': self.get_table_name()
        }


class UpdateUnit(Operator):
    TEMPLATE = '{field} = {value}'

    def __init__(self, field, value):
        super().__init__({
            'field': field if isinstance(field, sql_object.SimpleSQLObject) else sql_object.Field(field),
            'value': value if isinstance(value, sql_object.SimpleSQLObject) else sql_object.Value(value, field)
        })

    def get_template_params(self):
        return {
            'field': self.objects_query['field'],
            'value': self.objects_query['value']
        }


class Update(Operator):
    PRIORITY = 0
    NAME = 'update'
    TEMPLATE = 'update {table_name} set {params}'

    def __init__(self, **params):
        objects = []

        for field, value in params.items():
            objects.append(UpdateUnit(field, value))

        super().__init__(objects)

    def get_template_params(self):
        return {
            'params': ', '.join(self.objects_query),
            'table_name': self.get_table_name()
        }


class Delete(Operator):
    PRIORITY = 0
    TEMPLATE = 'delete from {table_name}'

    def __init__(self):
        super().__init__([])

    def get_template_params(self):
        return {'table_name': self.get_table_name()}


class WhereAddParam:
    AND = 'and'
    OR = 'or'


class Where(Operator):
    PRIORITY = 1
    TEMPLATE = 'where {expressions}'

    def __init__(self, *args, add_param=WhereAddParam.AND, **kwargs):
        self.__add_param = add_param

        expressions = []
        for arg in args:
            if isinstance(arg, comparators.Comparator):
                expressions.append(arg)
            else:
                raise TypeError()

        for field, expression in kwargs.items():
            expressions.append(comparators.Equal(field, expression))

        super().__init__(expressions)

    def get_template_params(self):
        return {'expressions': f' {self.__add_param} '.join(self.objects_query)}
