from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from collections.abc import Callable
from front.crude import Crudifier

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
from i2.deco import FuncFactory
from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep2 import (
    # DFLT_WF_PATH,
    # DFLT_ANNOT_PATH,
    data_from_wav_folder,
    data_from_csv,
    store_to_key_fvs,
    key_fvs_to_tag_fvs,
    mk_Xy,
)
from odat.mdat.vacuum import DFLT_CHUNKER, DFLT_FEATURIZER
from typing import Optional
from slang.chunkers import fixed_step_chunker
from front.base import prepare_for_dispatch
from front.crude import simple_mall_dispatch_core_func
from front.util import inject_enum_annotations
from front.base import prepare_for_dispatch
from front.crude import KT, StoreName


# # ============ MALL ===============
def make_chunker(chk_size: int, chk_step: Optional[int] = None):
    return partial(fixed_step_chunker, chk_size=chk_size, chk_step=chk_step)


if not b.mall():
    b.mall = {
        'func_store': {},
        'featurizer': {},
        'featurizer_cls': {},
        'chunker': {},
        'factories': {'chunker': make_chunker},
        'wf_store': {},
        'wf_store_cls': {'data_from_wav_folder': data_from_wav_folder},
        'annots_loader': {},
        'annots_loader_cls': {'data_from_csv': data_from_csv},
    }

mall = b.mall()
chunker = prepare_for_dispatch(make_chunker, output_store=mall['chunker'],)


DFLT_CHUNKER_MAKER = lambda: DFLT_CHUNKER
DFLT_FEATURIZER_MAKER = lambda: DFLT_FEATURIZER
DFLT_WF_PATH = '/Users/sylvain/Dropbox/Otosense/VacuumEdgeImpulse/'
DFLT_ANNOT_PATH = '/Users/sylvain/Dropbox/sipyb/Testing/data/annots_vacuum.csv'


FixedSizeChunker = DFLT_CHUNKER
featurizer = DFLT_FEATURIZER

# def data_loader(**kwargs):
#     return data_from_wav_folder(filepath)

# DFLT_CHUNKER_MAKER = lambda: DFLT_CHUNKER
# DFLT_FEATURIZER_MAKER = lambda: DFLT_FEATURIZER
# DFLT_WF_PATH = "/Users/sylvain/Dropbox/Otosense/VacuumEdgeImpulse/"
# DFLT_ANNOT_PATH = "/Users/sylvain/Dropbox/sipyb/Testing/data/annots_vacuum.csv"

# metadata = {
#     "FixedSizeChunker": {"func": DFLT_CHUNKER, "out": "chks"},
#     # 'FixedSizeChunker100': {'out': 'chks'},
#     # 'ThresholdChunker': {'out': 'chks'},
#     "FixedSizeChunkerMaker": {"func": DFLT_CHUNKER_MAKER, "out": "chunker"},
#     "FeaturizerMaker": {"func": DFLT_FEATURIZER_MAKER, "out": "featurizer"},
#     # 'key_fvs_to_tag_fvs': {'func': key_fvs_to_tag_fvs},
#     # 'Featurizer': {'func': DFLT_FEATURIZER, 'out': 'fvs'},
#     "store_to_key_fvs": {"func": store_to_key_fvs, "out": "key_fvs"},
#     "key_fvs_to_tag_fvs": {"func": key_fvs_to_tag_fvs, "out": "tag_fv_iterator"},
#     "WfStoreMaker": {
#         "func": data_from_wav_folder,
#         "out": "wf_store",
#         "bind": {"filepath": "wf_filepath"},
#     },
#     "AnnotsStoreMaker": {"func": data_from_csv, "out": "annots_df"},
#     "mk_Xy": {"func": mk_Xy},
# }

from meshed import DAG
from sklearn.preprocessing import MinMaxScaler


from streamlitfront.elements import SelectBox


from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from streamlitfront.base import mk_app


# crudifier_output = Crudifier(output_store='func_store', mall=mall)

# @Crudifier(output_store='func_store', mall = mall)


def dag_from_mall():
    pass


def select_func(func, store_name, kwargs):
    f = metadata[func]
    result_func = partial(f, **kwargs)
    mall[store_name][func] = result_func
    sig = Sig(result_func)
    st.write(f'added function with sig={sig}')
    return result_func


# @inject_enum_annotations(action=["list", "get"], store_name=mall)


def convert(arg):
    return None


# @inject_enum_annotations(action=["list", "get"], store_name=mall)
def explore_mall(
    store_name: StoreName, key: KT, action: str,
):
    args = [key, action, store_name]
    [key, action, store_name] = list(map(convert, args))

    return simple_mall_dispatch_core_func(key, action, store_name, mall=mall)


def get_kwargs(**kwargs):
    return kwargs


def populate_list_funcs():
    value = b.selected_func()
    b.list_funcs().append(metadata[value])


if not b.selected_func():
    b.selected_func = 'chunker'

if not b.list_funcs():
    b.list_funcs = [select_func]

data = ['chunker', 'featurizer', 'data_loader']
metadata = {
    'chunker': chunker,
    'featurizer': featurizer,
    'data_loader': data_from_wav_folder,
    'csv_loader': data_from_csv,
}


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


def send_message(output):
    b.update_store()


from typing import Tuple


def dummy(t: Tuple[int, int]):
    return t


if __name__ == '__main__':
    app = mk_app(
        [select_func, explore_mall],
        config={
            APP_KEY: {'title': 'Rendering map'},
            RENDERING_KEY: {
                'select_func': {
                    'execution': {
                        'inputs': {
                            'func': {
                                ELEMENT_KEY: SelectBox,
                                'options': data,
                                'value': b.selected_func,
                                # "on_value_change": populate_list_funcs,
                            },
                            'store_name': {
                                ELEMENT_KEY: SelectBox,
                                'options': ['func_store'],
                                # "value": b.selected_func,
                                # "on_value_change": populate_list_funcs,
                            },
                            'kwargs': {
                                ELEMENT_KEY: KwargsInput,
                                'func_sig': Sig(metadata[b.selected_func()]),
                            },
                        },
                        'on_submit': send_message,
                    }
                },
            },
        },
    )
    app()
    st.write(mall)
