"""A simple app to demo the use of Mappings to handle complex type"""
from typing import Mapping, Callable, Any
from enum import Enum
from streamlitfront.page_funcs import (
    BasePageFunc,
    func_to_pyd_input_model_cls,
    name_of_obj,
)
import streamlit_pydantic as sp
import streamlit as st

# from front.py2pydantic import func_to_pyd_model_specs
from i2 import Sig, empty_param_attr
from pydantic import create_model, Field

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


class SimplePageFuncPydanticWrite(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        mymodel = func_to_pyd_input_model_cls(self.func)
        name = name_of_obj(self.func)
        data = sp.pydantic_form(key=f'my_form_{name}', model=mymodel)
        # data = sp.pydantic_input(key=f"my_form_{name}", model=mymodel)

        if data:
            st.write(self.func(**dict(data)))


def func_to_pyd_input_model_cls(func: Callable, dflt_type=Any, name=None):
    """Get a pydantic model of the arguments of a python function"""
    name = name or name_of_obj(func)
    return create_model(name, **dict(func_to_pyd_model_specs(func, dflt_type)))


def func_to_pyd_model_specs_with_tooltips(func: Callable, dflt_type=Any):
    """Helper function to get field info from python signature parameters"""
    text_info = func.__doc__
    for p in Sig(func).params:
        if p.annotation is not empty_param_attr:
            if p.default is not empty_param_attr:
                p.default = Field(p.default, description=text_info)
                yield p.name, (p.annotation, p.default)
            else:
                p.default = Field(..., description=text_info)
                yield p.name, (p.annotation, p.default)
        else:  # no annotations
            if p.default is not empty_param_attr:
                yield p.name, Field(p.default, description=text_info)
            else:
                yield p.name, Field(dflt_type, ..., description=text_info)


def func_to_pyd_model_specs(func: Callable, dflt_type=Any):
    """Helper function to get field info from python signature parameters"""
    text_info = func.__doc__

    for p in Sig(func).params:
        if p.annotation is not empty_param_attr:
            if p.default is not empty_param_attr:
                yield p.name, (p.annotation, Field(p.default))
            else:
                yield p.name, (p.annotation, Field(...))
        else:  # no annotations
            if p.default is not empty_param_attr:
                yield p.name, Field(p.default)
            else:
                yield p.name, (dflt_type, Field(...))


if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from pydantic import BaseModel, Field, ValidationError, parse_obj_as

    # from streamlitfront.page_funcs import SimplePageFuncPydanticWrite

    # class ChoiceModel(BaseModel):
    #    single_selection: mk_choices_from_store(salary_store) = Field(
    #        ..., description="Only select a single item from a set."
    #    )

    configs = {'page_factory': SimplePageFuncPydanticWrite}

    app = dispatch_funcs([func], configs=configs)
    app()
