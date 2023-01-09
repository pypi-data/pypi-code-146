# streamlit run pydantic_streamlit_input.py

import streamlit as st
from pydantic import BaseModel
from typing import List, Dict
import streamlit_pydantic as sp
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class SelectionValue(str, Enum):
    FOO = 'foo'
    BAR = 'bar'


class NestedData(BaseModel):
    text: str
    integerchoice: List[int]


class ExampleModel(BaseModel):
    some_text: str
    some_number: int
    some_boolean: bool
    some_list: List[int]
    some_dict: Dict[str, int]
    integer_in_range: int = Field(
        20,
        ge=10,
        lt=30,
        multiple_of=2,
        description='Number property with a limited range.',
    )
    single_selection: SelectionValue = Field(
        ..., description='Only select a single item from a set.'
    )
    nested_choice: NestedData = Field(
        ..., description='Another object embedded into this model.',
    )


st.title('Use of pydantic for complex inputs')
data = sp.pydantic_input(key='my_form', model=ExampleModel)

if data:
    st.write(data)
