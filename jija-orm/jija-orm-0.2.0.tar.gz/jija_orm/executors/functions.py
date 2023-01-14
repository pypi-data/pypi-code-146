from jija_orm.executors import sql_object


class Function(sql_object.TemplateSqlObject):
    pass


class Max(Function):
    TEMPLATE = 'max({field})'

    def __init__(self, field: str):
        super().__init__([sql_object.Field(field)])

    def get_template_params(self):
        return {'field': self.objects[0].query}

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.objects[0].raw_name}>'


class Alias(sql_object.TemplateSqlObject):
    TEMPLATE = '{field} as {alias}'

    def __init__(self, field, alias):
        self.__alias = self.correct_name(alias)
        super().__init__([field if isinstance(field, sql_object.SimpleSQLObject) else sql_object.Field(field)])

    @property
    def alias(self):
        return self.__alias

    def get_template_params(self):
        return {
            'field': self.objects[0].query,
            'alias': self.__alias
        }

    def __eq__(self, other):
        return super().__eq__(other) and self.__alias == other.alias

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.alias}>'
        # return ''
