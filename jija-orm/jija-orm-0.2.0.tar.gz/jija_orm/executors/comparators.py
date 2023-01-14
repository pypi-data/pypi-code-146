from jija_orm.executors import sql_object


class Comparator(sql_object.TemplateSqlObject):
    TEMPLATE = '{field} {operator} {value}'
    OPERATOR = NotImplemented
    BOOL_OPERATOR = NotImplemented

    def __init__(self, field, value, **kwargs):
        super().__init__({
            'field': sql_object.Field(field),
            'value': value if isinstance(value, sql_object.SimpleSQLObject) else sql_object.Value(value, field),
            **kwargs
        })

    def get_template_params(self):
        return {
            'field': self.objects_query['field'],
            'value': self.objects_query['value'],
            'operator': self.BOOL_OPERATOR if self.bool_protect(self.objects['value']) else self.OPERATOR,
        }

    @staticmethod
    def bool_protect(value):
        if isinstance(value, sql_object.Value) and isinstance(value.raw_value, bool):
            return True

        return False


class NumericComparator(Comparator):
    OPERATOR = NotImplemented
    TEMPLATE = '{field} {operator}{equal} {value}'

    def __init__(self, *args, equal=False, **kwargs):
        self.__equal = equal
        super().__init__(*args, **kwargs)

    def get_template_params(self):
        template_params = super().get_template_params()
        return {
            **template_params,
            'equal': '=' if self.__equal else ''
        }


class Grater(NumericComparator):
    OPERATOR = '>'


class Lower(NumericComparator):
    OPERATOR = '<'


class Not(Comparator):
    OPERATOR = '!='
    BOOL_OPERATOR = 'is not'


class Equal(Comparator):
    OPERATOR = '='
    BOOL_OPERATOR = 'is'


class Like(Comparator):
    OPERATOR = 'like'
