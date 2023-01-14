import abc
import re
import typing

from jija_orm import exceptions


def calculated_decorator(func):
    def wrapper(self, *args, **kwargs):
        if not self.calculated:
            raise ValueError('SQL object not calculated')

        return func(self, *args, **kwargs)

    return wrapper


def validated_decorator(func):
    def wrapper(self, *args, **kwargs):
        if not self.validated:
            raise ValueError('SQL object not validated')

        return func(self, *args, **kwargs)

    return wrapper


class SqlObjectInterface(abc.ABC):
    @abc.abstractmethod
    def prepare(self, model):
        pass

    @abc.abstractmethod
    def get_query(self):
        pass


class SimpleSQLObject(SqlObjectInterface, abc.ABC):
    def __init__(self):
        self.__model = None

        self.__query = None
        self.__calculated = False

        self.__self_params = set()

    @property
    def model(self):
        return self.__model

    @property
    def calculated(self):
        return self.__calculated

    @property
    def self_params(self):
        return self.__self_params

    def add_param(self, param: 'Param'):
        self.__self_params.add(param.name)

    def get_params(self):
        return self.__self_params

    @property
    @calculated_decorator
    def query(self):
        return self.__query

    def prepare(self, model):
        self.__model = model

    def calculate(self):
        self.__query = self.get_query()
        self.__calculated = True
        return self.__query

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @staticmethod
    def correct_name(name):
        check = name.split('.')
        for index in range(len(check)):
            if not re.match(r'"\w*"', check[index]):
                check[index] = f'"{check[index]}"'

        return '.'.join(check)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.model == other.model and
                self.calculated == other.calculated and
                self.__calculated_eq(other)
        )

    def __calculated_eq(self, other):
        if self.calculated:
            return self.query == other.query

        return True


class ValidationSQLObject(SimpleSQLObject):
    def __init__(self):
        super().__init__()
        self.__validated = False

    @property
    def validated(self):
        return self.__validated

    def prepare(self, model):
        super().prepare(model)

        self.validate()
        self.__validated = True

    @abc.abstractmethod
    def validate(self):
        pass


class SQLObject(SimpleSQLObject):
    def __init__(self, objects: typing.Union[typing.List[SimpleSQLObject] or typing.Dict[SimpleSQLObject]]):
        super().__init__()

        self.__objects = objects
        self.__objects_query = objects.__class__()

    @property
    def objects(self):
        return self.__objects

    @property
    def objects_query(self):
        return self.__objects_query

    def get_params(self):
        params = set()
        if isinstance(self.__objects, dict):
            for obj in self.__objects.values():
                params.update(obj.get_params())

        elif isinstance(self.__objects, list):
            for obj in self.__objects:
                params.update(obj.get_params())

        else:
            raise TypeError()

        return params

    def prepare(self, model):
        super().prepare(model)

        if isinstance(self.__objects, dict):
            for obj in self.__objects.values():
                obj.prepare(model)

        elif isinstance(self.__objects, list):
            for obj in self.__objects:
                obj.prepare(model)

        else:
            raise TypeError()

    def get_query(self):
        return None

    def calculate(self):
        if isinstance(self.__objects, dict):
            for name, obj in self.__objects.items():
                self.__objects_query[name] = obj.calculate()

        elif isinstance(self.__objects, list):
            for obj in self.__objects:
                self.__objects_query.append(obj.calculate())

        else:
            raise TypeError()

        return super().calculate()

    def __eq__(self, other):
        return super().__eq__(other) and self.objects == other.objects and self.objects_query == other.objects_query


class TemplateSqlObject(SQLObject):
    TEMPLATE: str = NotImplemented

    def __init__(self, objects):
        super().__init__(objects)
        self.__template_params = None

    @property
    @calculated_decorator
    def template_params(self):
        return self.__template_params

    def get_template_params(self):
        raise NotImplementedError()

    def get_query(self):
        self.__template_params = self.get_template_params()
        return self.TEMPLATE.format(**self.__template_params)


class Value(ValidationSQLObject):
    def __init__(self, value, field=None):
        super().__init__()

        self.__field = field

        self.__raw_value = value
        self.__value = None

    @property
    def field(self):
        return self.__field

    @property
    def raw_value(self):
        return self.__raw_value

    @property
    @validated_decorator
    def value(self):
        return self.__value

    def validate(self):
        if isinstance(self.__raw_value, Param):
            self.__value = self.raw_value.calculate()
            self.add_param(self.raw_value)
            return

        if self.__raw_value is None:
            self.__value = 'null'
            return

        validator = self.get_validator()
        self.__value = validator.to_sql(self.__raw_value)

    def get_validator(self):
        from jija_orm import fields
        from jija_orm import models

        if isinstance(self.model, str):
            return fields.get_validator(self.raw_value)

        if issubclass(self.model, models.Model):
            if self.field:
                if not hasattr(self.model, self.field):
                    raise exceptions.TemplateAttributeError(self.model, self.field)

                return getattr(self.model, self.field)

        return fields.get_validator(self.raw_value)

    def get_query(self):
        return self.__value

    def __eq__(self, other):
        base_eq = super().__eq__(other) and self.raw_value == other.raw_value and self.field == other.field

        if not base_eq:
            return base_eq

        if self.validated:
            base_eq = base_eq and self.value == other.value

        return base_eq

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.raw_value} {f" for field {self.field}" if self.field else ""}>'


class Field(ValidationSQLObject):
    def __init__(self, name):
        super().__init__()

        self.__raw_name = name
        self.__name = None

    @property
    def raw_name(self):
        return self.__raw_name

    @property
    @validated_decorator
    def name(self):
        return self.__name

    def validate(self):
        from jija_orm import models
        from jija_orm import fields

        if isinstance(self.model, str):
            name = self.__raw_name

        elif issubclass(self.model, models.Model):
            if not hasattr(self.model, self.__raw_name):
                raise exceptions.TemplateAttributeError(self.model, self.__raw_name)

            field_obj = getattr(self.model, self.__raw_name)
            if isinstance(field_obj, fields.RelatedField):
                name = f'{self.__raw_name}_id'

            else:
                name = self.__raw_name
        else:
            name = self.__raw_name

        self.__name = self.correct_name(name)

    def get_query(self):
        return self.__name

    def __eq__(self, other):
        base_eq = super().__eq__(other) and self.raw_name == other.raw_name

        if not base_eq:
            return base_eq

        if self.validated:
            base_eq = base_eq and self.name == other.name

        return base_eq

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.raw_name}>'


class Param:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def calculate(self):
        return '{' + self.__name + '}'
