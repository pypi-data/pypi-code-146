from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    from jija_orm import models
    from jija_orm.executors.operators import Operator
    from jija_orm.executors.processors import Processor

import asyncio
from jija_orm import config, fields

MODEL = typing.TypeVar('MODEL')


class Executor(typing.Generic[MODEL]):
    from jija_orm.executors.operators import Operator
    from jija_orm.executors.processors import Processor

    __ITEMS_MARK = {
        'operators': Operator,
        'processors': Processor
    }

    def __init__(
            self,
            model: typing.Union[typing.Type[MODEL], str],
            *items: typing.Union[Operator, Processor],
            use_model: bool = True
    ):
        from jija_orm import models
        if isinstance(model, type) and issubclass(model, models.Model) and use_model is False:
            self.__model = model.get_name()
        else:
            self.__model = model

        marked_items = self.mark_items(items)
        self.extend_items(marked_items)

        self.__operators = self.sort_operators(marked_items['operators'])
        self.__processors = marked_items['processors']

        self.__operators_query = self.prepare()
        self.__query = self.__generate_query()
        self.__params = self.get_params()

    @classmethod
    def mark_items(cls, items: typing.Iterable[typing.Union[Operator, Processor]]) -> typing.Dict[str, typing.List]:
        marked_items = dict((name, []) for name in cls.__ITEMS_MARK)

        for item in items:
            marked = False
            for marked_name in cls.__ITEMS_MARK:
                if isinstance(item, cls.__ITEMS_MARK[marked_name]):
                    marked_items[marked_name].append(item)
                    marked = True
                    break

            if not marked:
                raise TypeError(f'Invalid type {type(item)}')

        return marked_items

    @classmethod
    def extend_items(cls, items):
        extra = []

        for marked_name in items:
            for item in items[marked_name]:
                extra.extend(item.EXTRA)

        marked_extra = cls.mark_items(extra)
        for marked_name in marked_extra:
            items[marked_name].extend(marked_extra[marked_name])

        return items

    @staticmethod
    def sort_operators(operators: typing.Iterable[Operator]) -> typing.List[Operator]:
        return sorted(operators, key=lambda arg: arg.PRIORITY)

    def prepare(self) -> typing.Dict[str, str]:
        result = {}

        for operator in self.operators:
            operator.prepare(self.model)

            result[operator.get_name()] = operator.calculate()

        return result

    def __generate_query(self) -> str:
        return "\n".join(self.operators_query.values())

    def get_params(self) -> typing.Set[str]:
        params = set()
        for operator in self.__operators:
            params.update(operator.get_params())

        return params

    @property
    def model(self) -> typing.Union[typing.Type[models.Model], str]:
        return self.__model

    @property
    def operators(self) -> typing.List[Operator]:
        return self.__operators

    @property
    def operators_query(self) -> typing.Dict[str, str]:
        return self.__operators_query

    @property
    def params(self) -> typing.Set[str]:
        return self.__params

    @property
    def query(self) -> str:
        return self.__query

    def sync_execute(self, **kwargs: str) -> typing.List[models.Model]:
        result = asyncio.run(self.execute(**kwargs))
        return result

    async def execute(self, **kwargs: str) -> typing.Union[typing.List[MODEL][MODEL], typing.Dict]:
        if self.__params != set(kwargs.keys()):
            raise ValueError('Invalid params')

        connection = await self.get_connection()

        for key in kwargs.keys():
            kwargs[key] = fields.get_validator(kwargs[key]).to_sql(kwargs[key])

        query = self.__query.format(**kwargs)
        query = query.format(**kwargs)
        return self.__serialize(await connection.fetch(query))

    @staticmethod
    async def get_connection():
        return await config.JijaORM.get_connection()

    def __serialize(self, query_set):
        if isinstance(self.model, str):
            return query_set

        result = list(map(lambda record: self.model(**record), query_set))
        for processor in self.__processors:
            result = processor.process_response(result)

        return result
