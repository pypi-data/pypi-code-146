from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Iterable, Union
from dol import Files
from meshed import code_to_dag, DAG
from odat.mdat.vacuum import (
    DFLT_ANNOTS_COLS,
    DFLT_CHUNKER,
    DFLT_FEATURIZER,
)
from creek.tools import apply_func_to_index, fanout_and_flatten
import os
import numpy as np
from dol.appendable import appendable
import matplotlib.pyplot as plt

from streamlitfront import mk_app, binder as b

import streamlit as st

import soundfile as sf
import pandas as pd
import zipfile
from io import BytesIO
from pathlib import Path

from dol.appendable import add_append_functionality_to_store_cls
from dol import Store
from dol import FilesOfZip, wrap_kvs, filt_iter

from hear import WavLocalFileStore


DFLT_WF_PATH = '/Users/sylvain/Dropbox/Otosense/VacuumEdgeImpulse/'
DFLT_ANNOT_PATH = '/Users/sylvain/Dropbox/sipyb/Testing/data/annots_vacuum.csv'


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
    return store_factory(filepath, data_reader=data_from_wav_folder, prefix='wf_store')


def annot_store_factory(filepath):
    return store_factory(filepath, data_reader=data_from_csv, prefix='annot_store')


def data_from_wav_folder(filepath):
    if is_dir(filepath):
        data = WavLocalFileStore(filepath)

    elif is_zip_file(filepath):
        data = WfZipStore(filepath)

    else:
        raise ('Data not supported')
    return data


def data_from_csv(filepath):
    return pd.read_csv(filepath)


def annot_store_factory(filepath):
    key = key_maker(name=filepath, prefix='annot_store')
    tag = 'annot_store'


def store_factory(filepath, data_reader=data_from_csv, prefix='annot_store'):
    key = key_maker(name=filepath, prefix=prefix)
    tag = prefix

    data = data_reader(filepath)

    return mk_store_item(key, tag, data)


def mk_store_item(key, tag, data):
    return dict(key=key, tag=tag, data=data)


def store_to_key_fvs(wf_store, chunker=DFLT_CHUNKER, featurizer=DFLT_FEATURIZER):
    wf_items = wf_store.items()
    key_chk_tuples = fanout_and_flatten(wf_items, chunker, 1)
    featurizer_iter = partial(apply_func_to_index, apply_to_idx=1, func=featurizer)
    yield from map(featurizer_iter, key_chk_tuples)


def key_fvs_to_tag_fvs(key_fvs, annots_df):
    func = partial(key_to_tag_from_annots, annots_df=annots_df)
    tagger = partial(apply_func_to_index, apply_to_idx=0, func=func)

    yield from map(tagger, key_fvs)


def key_to_tag_from_annots(key, annots_df):
    tag = annots_df['tag'][annots_df['key'] == key].values[0]
    return tag


def mk_Xy(tag_fv_iterator):
    y, X = zip(*list(tag_fv_iterator))
    return np.array(X), y


if __name__ == '__main__':
    pass
