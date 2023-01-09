from typing import Iterable
from streamlitfront.elements import TextInput, SelectBox, ExecSection, TextOutput
from dataclasses import dataclass
from streamlitfront import mk_app, binder as b
from front.elements import InputBase
from i2 import Sig
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
import streamlit as st


def add_nums(nums_to_add: Iterable[float] = 12):
    # return sum([int(nums_to_add)])
    return nums_to_add


if not b.mall():
    b.mall = {
        'result': {},
    }

mall = b.mall()


@dataclass
class ArgsInput(InputBase):
    # func_sig: Sig = None

    def __post_init__(self):
        super().__post_init__()
        self.get_args = []
        self.inputs = []

    def render(self):
        exec_section = ExecSection(
            obj=self.get_args,
            inputs=self.inputs,
            output={ELEMENT_KEY: TextOutput},
            auto_submit=True,
            on_submit=self.populate_input,
            use_expander=False,
        )
        exec_section()
        st.write(f'inputs={self.inputs}, args={self.output}')
        return self.value()

    def populate_input(self, output):
        st.write(f'inputs={self.inputs}, args={self.output}')
        self.value.set(output)
        # self.inputs.append(item)


if not b.list_args():
    b.list_args = []


def populate_list():
    value = b.result()
    b.list_args().append(value)


if __name__ == '__main__':
    app = mk_app(
        [add_nums],
        config={
            APP_KEY: {'title': 'Rendering map'},
            RENDERING_KEY: {
                'add_nums': {
                    'execution': {
                        'inputs': {
                            'nums_to_add': {
                                ELEMENT_KEY: TextInput,
                                'value': b.result,
                                'on_value_change': populate_list
                                # "func_sig": Sig(add_nums),
                            },
                        },
                        # "on_submit": lambda x: print("done!"),
                    }
                },
            },
        },
    )
    app()
    st.write(mall)
