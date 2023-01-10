from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from collections.abc import Callable

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SelectBox
from typing import Any
from streamlitfront.elements import MultiSourceInput
import streamlit as st
from front.elements import InputBase
from i2 import Sig
from dataclasses import dataclass
from streamlitfront.elements import TextInput, SelectBox, ExecSection, TextOutput
from functools import partial
from front.crude import Crudifier
from streamlitfront.data_binding import BoundData


# # ============ MALL ===============
# if not b.mall():
#     b.mall = dict(func_store={})

# mall = b.mall()


def foo(x: str, y: str, z: int):
    return x + y * z


def bar(msg: str):
    return msg


# Choice #1: Simple ####################
# data = ['foo', 'bar']
# metadata = {'foo': foo, 'bar': bar}

# Choice #2: Involving a local file store ####################
from dol import Files

data = Files('~', max_levels=0)
metadata = {k: [foo, bar][len(k) % 2] for k in data}

# print(metadata)

# @Crudifier(output_store="func_store", mall=mall)
def my_map(func, kwargs):
    f = metadata[func]
    return partial(f, **kwargs)
    # return f, kwargs


def expand_names(names):
    return {name: {ELEMENT_KEY: TextInput} for name in names}


def populate_kwargs():
    value = b.selected_func()
    list_names = list(Sig(metadata[value]).names)
    b.names_for_kwargs = expand_names(list_names)
    st.write(b.names_for_kwargs())


if not b.selected_func():
    b.selected_func = next(iter(data))


def get_kwargs(**kwargs):
    return kwargs


@dataclass
class KwargsInput(InputBase):
    func_sig: Sig = None

    def __post_init__(self):
        super().__post_init__()
        self.get_kwargs = self.func_sig(get_kwargs)
        self.inputs = self._build_inputs_from_sig()

    def render(self):
        exec_section = ExecSection(
            obj=self.get_kwargs,
            inputs=self.inputs,
            output={ELEMENT_KEY: TextOutput},
            auto_submit=True,
            on_submit=self._return_kwargs,
            use_expander=False,
        )
        exec_section()
        return self.value()

    def _build_inputs_from_sig(self):
        return {
            name: {ELEMENT_KEY: TextInput, 'bound_data_factory': BoundData}
            for name in self.func_sig
        }

    def _return_kwargs(self, output):
        self.value.set(output)


if __name__ == '__main__':
    app = mk_app(
        [my_map],
        config={
            APP_KEY: {'title': 'Rendering map'},
            RENDERING_KEY: {
                'my_map': {
                    'execution': {
                        'inputs': {
                            'func': {
                                ELEMENT_KEY: SelectBox,
                                'options': data,
                                'value': b.selected_func,
                                'on_value_change': populate_kwargs,
                            },
                            'kwargs': {
                                ELEMENT_KEY: KwargsInput,
                                'func_sig': Sig(metadata[b.selected_func()]),
                            },
                        }
                    }
                },
            },
        },
    )
    app()
