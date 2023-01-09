"""A simple app to demo the use of Mappings to handle complex type"""
from typing import Mapping
from enum import Enum


ComplexType = float  # just pretend it's complex!


def func(salary: ComplexType, n_months: int = 12) -> float:
    return salary * n_months


SalaryKey = str  # or some type that will resolve in store-fed key selector
SalaryMapping = Mapping[SalaryKey, ComplexType]

salary_store: SalaryMapping
salary_store = {'sylvain': 10000, 'christian': 2000, 'thor': 50000}


def mk_choices_from_store(store):
    choices = Enum('Choices', {key: key for key in store.keys()})
    return choices


if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from pydantic import BaseModel, Field, ValidationError, parse_obj_as
    from streamlitfront.page_funcs import SimplePageFuncPydanticWrite

    class ChoiceModel(BaseModel):
        single_selection: mk_choices_from_store(salary_store) = Field(
            ..., description='Only select a single item from a set.'
        )

    configs = {'page_factory': SimplePageFuncPydanticWrite}

    def wrapped_func(selection: ChoiceModel, n_months: int):
        # print(f"{type(selection)=}, {selection=}")
        selection = selection.single_selection.value
        salary_val = salary_store[selection]

        return func(salary_val, n_months)

    app = dispatch_funcs([func, wrapped_func], configs=configs)
    app()
