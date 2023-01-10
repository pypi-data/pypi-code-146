# streamlit run pydantic_streamlit_front.py

import streamlit as st
import streamlit_pydantic as sp
from streamlitfront.base import dispatch_funcs, BasePageFunc
from opyratorfront.py2pydantic import func_to_pyd_input_model_cls
from pydantic import BaseModel, Field
from i2 import name_of_obj


def foo(word: str, multiplier: int) -> str:
    return word * multiplier


class SimplePageFuncPydanticWrite(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        mymodel = func_to_pyd_input_model_cls(self.func)
        name = name_of_obj(self.func)

        # data = sp.pydantic_form(key=f"my_form_{name}", model=mymodel)
        data = sp.pydantic_input(key=f'my_form_{name}', model=mymodel)

        if data:
            st.write(self.func(**data))
            # st.write(self.func(**dict(data)))
            # st.json(data.json())


configs = {'page_factory': SimplePageFuncPydanticWrite}
app = dispatch_funcs([foo], configs=configs)
app()
