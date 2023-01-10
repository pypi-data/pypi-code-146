# launch as : opyrator launch-ui opyrator_front_dispatch:wrapped_func
# launch as : opyrator launch-api opyrator_front_dispatch:wrapped_func


import streamlit as st
import streamlit_pydantic as sp
from streamlitfront.base import dispatch_funcs, BasePageFunc
from opyratorfront.py2pydantic import func_to_pyd_input_model_cls
from pydantic import BaseModel, Field
from i2 import name_of_obj
from opyrator import Opyrator


# class Input(BaseModel):
#    inp: int


class Output(BaseModel):
    res: str


def func(x: str) -> str:
    result = x * 2
    return result


Input = func_to_pyd_input_model_cls(func, name='Input')
print('issubclass', issubclass(Input, BaseModel))
name = name_of_obj(func)


def wrapped_func(input: Input) -> Output:
    return Output(res=func(input.x))


# op = Opyrator(wrapped_func)
