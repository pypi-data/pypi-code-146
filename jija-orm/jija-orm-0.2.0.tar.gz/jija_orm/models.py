import typing

from jija_orm import executors
from jija_orm.executors import query, operators


MODEL = typing.TypeVar('MODEL')


class Model(typing.Generic[MODEL]):
    from jija_orm import fields

    id = fields.IntegerField(pk=True)
    manager: query.QueryManager[typing.Type[MODEL]] = query.QueryManager

    def __init__(self: MODEL, *, from_query=False, **kwargs):
        self.__from_query = from_query
        self.__state = {}

        for field in self.get_fields():
            value = kwargs.get(field)
            self.__state[field] = value
            setattr(self, field, value)

        for constraint in self.get_constraints():
            value = kwargs.get(constraint) or kwargs.get(f'{constraint}_id')
            self.__state[constraint] = value
            setattr(self, constraint, value)

        if 'id' in kwargs:
            for name, related_manager in self.get_related_managers().items():
                setattr(self, name, related_manager.get_manager(self.__class__, self.id))


    @classmethod
    def init_managers(cls, real_class: typing.Type[MODEL] = None):
        for name, attr in cls.__dict__.items():
            if isinstance(attr, type) and issubclass(attr, query.QueryManager):
                setattr(real_class, name, attr(real_class or cls))

        if hasattr(cls.__base__, 'init_managers'):
            cls.__base__.init_managers(cls)

    @classmethod
    def get_fields(cls):
        model_fields = {}

        for name, attr in cls.__dict__.items():
            from jija_orm import fields
            if isinstance(attr, fields.Field):
                model_fields[name] = attr

        if hasattr(cls.__base__, 'get_fields'):
            model_fields.update(cls.__base__.get_fields())

        return model_fields

    @classmethod
    def get_constraints(cls) -> typing.Dict[str, 'fields.RelatedField']:
        model_fields = {}

        for name, attr in cls.__dict__.items():
            from jija_orm import fields
            if isinstance(attr, fields.RelatedField):
                model_fields[name] = attr

        if hasattr(cls.__base__, 'get_constraints'):
            model_fields.update(cls.__base__.get_constraints())

        return model_fields

    @classmethod
    def get_related_managers(cls) -> typing.Dict[str, query.RelatedManager]:
        related_managers = {}

        for name, attr in cls.__dict__.items():
            if isinstance(attr, query.RelatedManager):
                related_managers[name] = attr

        if hasattr(cls.__base__, 'get_constraints'):
            related_managers.update(cls.__base__.get_constraints())

        return related_managers

    async def save(self):
        to_update = {}
        for arg in self.__state:
            real_arg = getattr(self, arg)
            if self.__state[arg] != real_arg:
                to_update[arg] = real_arg

        if not to_update:
            return

        executor = executors.Executor(
            self.__class__,
            operators.Update(**to_update),
            operators.Where(id=self.id)
        )

        return await executor.execute()

    async def delete(self):
        executor = executors.Executor(
            self.__class__,
            operators.Delete(),
            operators.Where(id=self.id)
        )

        return await executor.execute()

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def select(cls: typing.Type[MODEL], *args, **kwargs) -> query.QueryManager[MODEL]:
        return cls.manager.select(*args, **kwargs)

    @classmethod
    def update(cls: typing.Type[MODEL], **kwargs) -> query.QueryManager[MODEL]:
        return cls.manager.update(**kwargs)

    @classmethod
    def where(cls: typing.Type[MODEL], *args, **kwargs) -> query.QueryManager[MODEL]:
        return cls.manager.where(*args, **kwargs)

    @classmethod
    def multiple_create(cls: typing.Type[MODEL], rows) -> query.QueryManager[MODEL]:
        return cls.manager.multiple_insert(rows)

    @classmethod
    def insert(cls: typing.Type[MODEL], **kwargs) -> query.QueryManager[MODEL]:
        return cls.manager.insert(**kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def __eq__(self, other: 'Model'):
        if type(self) != type(other):
            raise TypeError(f'Cant compare different types {type(self)} and {type(other)}')

        for item in self.__state:
            if getattr(other, item, None) != self.__state[item]:
                return False

        return True
