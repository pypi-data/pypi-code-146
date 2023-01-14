import datetime
import decimal

from jija_orm import utils


class Field:
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(*args, **kwargs)

    PYTHON_TYPE = NotImplemented
    SQL_TYPE = NotImplemented
    EQUAL_PARAMS = ('default', 'null')

    def __init__(self, *, pk=False, default=utils.NotSet, null=False):
        self.pk = pk
        self.null = null
        self.default = default

    # @classmethod
    # def to_python(cls, value):
    #     raise NotImplementedError()

    @classmethod
    def __validate_type(cls, value):
        if type(value) is not cls.PYTHON_TYPE:
            raise TypeError(f'Excepted {cls.PYTHON_TYPE.__name__}, got {type(value).__name__}')

    @classmethod
    def to_sql(cls, value):
        cls.__validate_type(value)
        return cls._to_sql(value)

    @classmethod
    def _to_sql(cls, value):
        return value

    def get_type(self):
        return self.SQL_TYPE

    @property
    def data(self):
        return {
            'type': self.get_type(),
            'null': self.null,
            'default': self.default,
            'pk': self.pk,
        }


class BooleanField(Field):
    PYTHON_TYPE = bool
    SQL_TYPE = 'bool'

    @classmethod
    def _to_sql(cls, value):
        return 'true' if value else 'false'


class TextField(Field):
    PYTHON_TYPE = str
    SQL_TYPE = 'text'

    @classmethod
    def _to_sql(cls, value):
        return f"'{value}'"


class CharField(TextField):
    PYTHON_TYPE = str
    EQUAL_PARAMS = (*Field.EQUAL_PARAMS, 'max_length')

    def __init__(self, *, max_length, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def get_type(self):
        return f'{self.SQL_TYPE}({self.max_length})'


class IntegerField(Field):
    PYTHON_TYPE = int
    SQL_TYPE = 'int4'


class BigIntegerField(Field):
    PYTHON_TYPE = int
    SQL_TYPE = 'int8'


class FloatField(Field):
    PYTHON_TYPE = float
    SQL_TYPE = 'float8'


class DecimalField(Field):
    PYTHON_TYPE = decimal.Decimal
    SQL_TYPE = 'numeric'


class DateField(Field):
    PYTHON_TYPE = datetime.date
    SQL_TYPE = 'date'

    @classmethod
    def _to_sql(cls, value: datetime.date) -> str:
        return f"'{value.isoformat()}'"


class DatetimeField(Field):
    PYTHON_TYPE = datetime.datetime
    SQL_TYPE = 'timestamp'

    @classmethod
    def _to_sql(cls, value: datetime.datetime) -> str:
        return f"'{value.isoformat(' ')}'"


class RelatedField:
    def __init__(self, *, relation_to, on_delete, null=False):
        from jija_orm import models
        from jija_orm import config

        if isinstance(relation_to, type) and issubclass(relation_to, models.Model):
            self.__relation_to_class = relation_to
            self.__relation_to = relation_to.get_name()

        elif isinstance(relation_to, str):
            self.__relation_to_class = config.JijaORM.get_model(relation_to)
            self.__relation_to = self.__relation_to_class.get_name()

        else:
            raise ValueError('relation_to must be a model or string')

        self.__on_delete = on_delete
        self.__null = null

    @property
    def relation_to(self):
        return self.__relation_to

    @property
    def relation_to_class(self):
        return self.__relation_to_class

    @property
    def on_delete(self):
        return self.__on_delete

    @property
    def null(self):
        return self.__null


class ForeignKey(RelatedField):
    @classmethod
    def to_sql(cls, value):
        from jija_orm import models
        if isinstance(value, models.Model):
            return value.id

        if isinstance(value, int):
            return value

        if isinstance(value, str) and value.isnumeric():
            return int(value)

        raise TypeError('Unsupported type {type(value)}')


class OnDelete:
    CASCADE = 'cascade'
    SET_NULL = 'set null'
    SET_DEFAULT = 'set default'


def get_validator(value):
    if isinstance(value, bool):
        return BooleanField

    elif isinstance(value, str):
        return CharField

    elif isinstance(value, int):
        return IntegerField

    elif isinstance(value, datetime.date):
        return DateField

    elif isinstance(value, datetime.datetime):
        return DatetimeField

    raise TypeError(type(value))


SQL_TYPE_DICT = {
    BooleanField.SQL_TYPE: BooleanField,

    CharField.SQL_TYPE: CharField,
    TextField.SQL_TYPE: TextField,

    IntegerField.SQL_TYPE: IntegerField,
    FloatField.SQL_TYPE: FloatField,
    DecimalField.SQL_TYPE: DecimalField,

    DateField.SQL_TYPE: DateField,
    DatetimeField.SQL_TYPE: DatetimeField,
}
