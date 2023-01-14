from __future__ import annotations

from jija_orm import executors
from jija_orm.executors import operators, comparators

import typing
if typing.TYPE_CHECKING:
    from jija_orm.models import Model

QUERY_MODEL = typing.TypeVar('QUERY_MODEL')


class QueryManager(typing.Generic[QUERY_MODEL]):
    def __init__(self, model_class: QUERY_MODEL, class_operators=None):
        self.__model_class = model_class
        self.__operators = self.fix_operators(class_operators)
        # self.__processors =

    def __add_templates(self, *new_templates) -> 'QueryManager':
        class_operators = self.__operators.copy()
        class_operators.extend(new_templates)
        return self.__class__(self.__model_class, class_operators)

    @staticmethod
    def fix_operators(class_templates):
        if not class_templates:
            return []

        templates_dict = {}
        for template in class_templates:
            if templates_dict.get(template.PRIORITY):
                if template.COMPARABLE is False:
                    templates_dict[template.PRIORITY] = template
                else:
                    raise NotImplementedError()

            else:
                templates_dict[template.PRIORITY] = template

        return list(templates_dict.values())

    @property
    def model(self) -> QUERY_MODEL:
        return self.__model_class

    @property
    def operators(self):
        return self.__operators

    def select(self, *args, **kwargs) -> 'QueryManager[QUERY_MODEL]':
        return self.__add_templates(operators.Select(*args, **kwargs))

    def update(self, **kwargs) -> 'QueryManager[QUERY_MODEL]':
        return self.__add_templates(operators.Update(**kwargs))

    def insert(self, **kwargs) -> 'QueryManager[QUERY_MODEL]':
        return self.__add_templates(operators.Insert(**kwargs))

    def multiple_insert(self, rows) -> 'QueryManager[QUERY_MODEL]':
        return self.__add_templates(operators.MultipleInsert(rows))

    def delete(self) -> 'QueryManager[QUERY_MODEL]':
        return self.__add_templates(operators.Delete())

    def where(self, *args, **kwargs) -> 'QueryManager[QUERY_MODEL]':
        if self.__operators:
            new_operators = []
        else:
            new_operators = [operators.Select()]

        new_operators.append(operators.Where(*args, **kwargs))
        return self.__add_templates(*new_operators)

    def __await__(self) -> typing.Generator[typing.Any, None, typing.List[QUERY_MODEL]]:
        executor = executors.Executor(self.__model_class, *self.__operators)
        return executor.execute().__await__()


class RelatedManager(typing.Generic[QUERY_MODEL]):
    def __init__(self, to: typing.Union[str, QUERY_MODEL], field: typing.Optional[str] = None):
        self.__to = to
        self.__field = field

    def get_model(self) -> QUERY_MODEL:
        from jija_orm import config
        from jija_orm import models

        if isinstance(self.__to, type):
            if not issubclass(self.__to, models.Model):
                raise TypeError('to must be str or model')

            return self.__to

        elif isinstance(self.__to, str):
            return config.JijaORM.get_model(self.__to)

        else:
            raise TypeError('to must be str or model')

    def get_field(self, self_model: typing.Type[Model], model: QUERY_MODEL) -> str:
        if self.__field:
            return self.__field

        to_return = None
        for name, constraint in model.get_constraints().items():
            if constraint.relation_to_class == self_model:
                if to_return:
                    raise ValueError(
                        'Looks like your model has two relations, pleas set field param in related manager')

                to_return = name

        if not to_return:
            raise ValueError(f'{model} does`t have relation to {self_model}')

        return to_return

    def get_manager(self, self_model: typing.Type[Model], object_id: int) -> QueryManager[QUERY_MODEL]:
        model = self.get_model()
        field = self.get_field(self_model, model)

        return QueryManager(model).where(comparators.Equal(field, object_id))
