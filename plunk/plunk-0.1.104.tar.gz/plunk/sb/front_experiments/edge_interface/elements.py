import streamlit as st
from meshed import DAG
from front.types import FrontElementName
from front.elements import FrontComponentBase, TextInputBase
from typing import List, Any

WaveForm = List[int]


class SimpleList(FrontComponentBase):
    def __init__(
        self,
        arr: WaveForm,
        name: FrontElementName = None,
        use_container_width: bool = False,
    ):
        super().__init__(arr=arr, name=name)
        self.use_container_width = use_container_width

    def render(self):
        with st.expander(self.name, True):
            arr: WaveForm = self.arr
            st.write(arr.len)


class SimpleText(TextInputBase):
    def __init__(
        self,
        obj: str,
        name: FrontElementName = None,
        use_container_width: bool = False,
        input_key: str = None,
        init_value=None,
    ):
        super().__init__(obj=obj, name=name, input_key=input_key)
        self.use_container_width = use_container_width

    def render(self):
        # with st.expander(self.name, True): No nesting of expanders
        input_key: str = self.input_key
        st.write(f'length of text entered= {len(input_key)}')


class SimpleDataframe(FrontComponentBase):
    def __init__(
        self,
        obj: str,
        name: FrontElementName = None,
        use_container_width: bool = False,
        input_key: str = None,
        init_value=None,
    ):
        super().__init__(obj=obj, name=name, input_key=input_key)
        self.use_container_width = use_container_width

    def render(self):
        # with st.expander(self.name, True): No nesting of expanders
        input_key: str = self.input_key
        st.write(f'length of text entered= {len(input_key)}')
