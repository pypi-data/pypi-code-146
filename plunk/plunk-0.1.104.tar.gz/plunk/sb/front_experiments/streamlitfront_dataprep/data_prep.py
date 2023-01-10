from dataclasses import dataclass
from functools import partial
from io import BytesIO
import os
from pathlib import Path
import time
from typing import Any, Iterable, Union
from dol import Files
from front.elements import DEFAULT_INPUT_KEY, OutputBase
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from collections.abc import Callable
from front.crude import Crudifier, prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox
from dol.appendable import appendable
import soundfile as sf
import matplotlib.pyplot as plt
from streamlit.uploaded_file_manager import UploadedFile

from streamlitfront import mk_app, binder as b
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st

import os
import soundfile as sf
import pandas as pd
import zipfile
from io import BytesIO
from pathlib import Path

from dol.appendable import add_append_functionality_to_store_cls
from dol import Store
from dol import FilesOfZip, wrap_kvs, filt_iter

from py2store import FilesOfZip
from hear import WavLocalFileStore
from dol import FuncReader


# ============ BACKEND ============
WaveForm = Any
DFLT_WF_PATH = '/Users/sylvain/Dropbox/Otosense/VacuumEdgeImpulse/'
DFLT_ANNOT_PATH = '/Users/sylvain/Dropbox/sipyb/Testing/data/annots_vacuum.csv'


from hear import WavLocalFileStore
from dol import FuncReader


def my_obj_of_data(b):
    return sf.read(BytesIO(b), dtype='float32')[0]


@wrap_kvs(obj_of_data=my_obj_of_data)
@filt_iter(filt=lambda x: not x.startswith('__MACOSX') and x.endswith('.wav'))
class WfZipStore(FilesOfZip):
    """Waveform access. Keys are .wav filenames and values are numpy arrays of int16 waveform."""

    pass


def key_to_ext(k):
    _, ext = os.path.splitext(k)
    if ext.startswith('.'):
        ext = ext[1:]
    return ext


def processor_from_ext(ext):
    if ext.startswith('.'):
        ext = ext[1:]
    if ext in {'zip'}:
        pass
    elif ext in {'wav'}:
        pass


def is_zip_file(filepath):
    return zipfile.is_zipfile(filepath)


def is_dir(filepath):
    return os.path.isdir(filepath)


def key_maker(name, prefix):
    return f'{prefix}_{name}'


def wf_store_factory(filepath):
    key = key_maker(name=filepath, prefix='wf_store')
    tag = 'wf_store'

    if is_dir(filepath):
        data = WavLocalFileStore(filepath)

    elif is_zip_file(filepath):
        data = WfZipStore(filepath)

    return mk_store_item(key, tag, data)


def annot_store_factory(filepath):
    key = key_maker(name=filepath, prefix='annot_store')
    tag = 'annot_store'

    data = pd.read_csv(filepath)

    return mk_store_item(key, tag, data)


def mk_store_item(key, tag, data):
    return dict(key=key, tag=tag, data=data)


# tagged_wf_store = appendable(Files, item2kv=tagged_timestamped_kv)
if not b.mall():
    b.mall = dict(
        wf_store_factory={'wf_factory': wf_store_factory},
        wf_store_path={'wf_path': DFLT_WF_PATH},
        annot_store_path={'annot_path': DFLT_ANNOT_PATH},
        # wf_store_factory=dict(one=1, two=2),
        annot_store_factory={'annot_factory': annot_store_factory},
        data_store=dict(),
        dummy_store=dict(),
    )
mall = b.mall()
crudifier = partial(Crudifier, mall=mall)


def auto_namer(*, arguments):
    return '_'.join(map(str, arguments.values()))


# @crudifier(output_store="wf_store", auto_namer=auto_namer)
@crudifier(
    param_to_mall_map=dict(factory='wf_store_factory', path='wf_store_path'),
    output_store='data_store',
)
def mk_wf_store(factory: Any, path: str):
    result = factory(path)
    st.write(result)
    return factory(path)


@crudifier(
    param_to_mall_map=dict(factory='annot_store_factory', path='annot_store_path')
)
def mk_annot_store(factory: Any, path: str):
    result = factory(path)
    st.write(result)
    return factory(path)


# ============ END BACKEND ============


# ============ FRONTEND ============


@dataclass
class SuccessNotification(OutputBase):
    message: str = 'Success!'

    def render(self):
        return st.success(self.message)


get_wfstore_description = '''
Make a store containing wav files.
'''

config_ = {
    APP_KEY: {'title': 'Data Prep App'},
    RENDERING_KEY: {
        'mk_wf_store': {
            NAME_KEY: 'Make Wf Store',
            'description': {'content': get_wfstore_description},
            'execution': {
                'inputs': {
                    'factory': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['wf_store_factory'],
                        # "options": dict(a="a_choice"),
                        # "display_label": False,
                    },
                    'path': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['wf_store_path'],
                        # "options": dict(a="a_choice"),
                        # "display_label": False,
                    },
                },
                'output': {
                    ELEMENT_KEY: SuccessNotification,
                    'message': 'The wave store has been made successfully.',
                },
            },
        },
        'mk_annot_store': {
            NAME_KEY: 'Make annot Store',
            # "description": {"content": get_wfstore_description},
            'execution': {
                'inputs': {
                    'factory': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['annot_store_factory'],
                        # "options": dict(a="a_choice"),
                        # "display_label": False,
                    },
                    'path': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['annot_store_path'],
                        # "options": dict(a="a_choice"),
                        # "display_label": False,
                    },
                },
                'output': {
                    ELEMENT_KEY: SuccessNotification,
                    'message': 'The wave store has been made successfully.',
                },
            },
        },
        DAG: {'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',}},
        Callable: {
            'execution': {
                'inputs': {
                    'save_name': {ELEMENT_KEY: TextInput, NAME_KEY: 'Save output as',}
                }
            }
        },
    },
}
# ============ END FRONTEND ============

if __name__ == '__main__':
    app = mk_app([mk_wf_store, mk_annot_store], config=config_)
    app()
