from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import FloatSliderInput, FloatInput
from streamlitfront.base import mk_app
from front.crude import prepare_for_crude_dispatch
import streamlit as st


if 'mall' not in st.session_state:
    st.session_state['mall'] = {'train_test_proportion': {'train_test_proportion': 0.8}}

mall = st.session_state['mall']


def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting):
    """bar greets its input"""
    return f'{greeting} {x}'


def set_train_test_proportion(train_proportion):
    mall['train_test_proportion'] = train_proportion
    return train_proportion


app = mk_app(
    [foo, bar, set_train_test_proportion],
    config={
        APP_KEY: {'title': 'My app'},
        RENDERING_KEY: {
            'set_train_test_proportion': {
                'execution': {
                    'inputs': {'train_proportion': {ELEMENT_KEY: FloatSliderInput,},}
                },
            },
        },
    },
)
app()
st.write(mall)
