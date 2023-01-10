from functools import partial
import streamlit as st

from front.crude import prepare_for_crude_dispatch

# ============ BACKEND ============

import numpy as np


def apply_func_to_wf(wf, func):
    print(f'{wf=}, {func=}')
    return func(wf)


mall = dict(func=dict(volume=np.std, bull=np.mean,),)
# crudify = Crudifier(mall)

import front as f
import streamlitfront.elements as sf

from i2 import wrap, Pipe
from recode import decode_wav_bytes


class MyFileUploader(sf.FileUploader):
    def render(self):
        print('... in render with {self=} and {uploaded_file=}')
        uploaded_file = super().render()
        if uploaded_file is not None:
            b = decode_wav_bytes(uploaded_file.read())
            print(f'{len(b)=}, {type(b)=}')
            return decode_wav_bytes(uploaded_file.read())


from front.crude import prepare_for_crude_dispatch

apply_func_to_wf = prepare_for_crude_dispatch(
    apply_func_to_wf, param_to_mall_map={'func': 'func'}, mall=mall
)

# my_file_uploader = wrap(sf.FileUploader, egress=)

config_ = {
    # f.APP_KEY: {'title': 'apply_func_to_wf'},
    f.RENDERING_KEY: {
        'apply_func_to_wf': {
            'execution': {
                'inputs': {
                    'wf': {f.ELEMENT_KEY: MyFileUploader, 'type': 'wav',},
                    'func': {f.ELEMENT_KEY: sf.SelectBox, 'options': mall['func'],},
                },
            }
        },
    }
}


from streamlitfront import mk_app

app = mk_app([apply_func_to_wf], config=config_)
app()

# families = {'whalen': ['cora', 'thor', 'ness'], 'feron': ['valentin', 'maya', 'haydeé']}


# if 'mall' not in st.session_state:
#     st.session_state['mall'] = {
#         'family_name': dict(zip(families, families)),
#         'first_name': dict(),
#     }
#
# mall = st.session_state['mall']
# crudify = partial(prepare_for_crude_dispatch, mall=mall)

# locals = st.session_state['locals']


# stores = {
#     'fruit': {'apple': [1, 2, 3], 'banana': 'abc'},
#     'numbers': {'one': 1, 'two': 2},
# }

from dataclasses import dataclass
from typing import Any


# class Get:
#     key: str
#
#
# Nest = partial
#
#
# first_name_element = Nest(
#     st.selectbox,
#     options=Nest(families, Get('family_name'))
# )
#
# def get_value_from_store(family_name, first_name):
#     return f'{first_name} {family_name}'
#
#
# first_name_element.options = F(foo, family_name.value)


# ============ END BACKEND ============


# ============ FRONTEND ============


import os
