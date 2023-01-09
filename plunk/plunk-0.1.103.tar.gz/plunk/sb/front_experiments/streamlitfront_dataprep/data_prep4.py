from meshed import FuncNode, DAG
import streamlit as st
from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep2 import (
    data_from_wav_folder,
    data_from_csv,
    store_to_key_fvs,
    key_fvs_to_tag_fvs,
    mk_Xy,
)
from odat.mdat.vacuum import (
    DFLT_ANNOTS_COLS,
    DFLT_CHUNKER,
    DFLT_FEATURIZER,
)
from streamlitfront.examples.util import Graph
from streamlitfront.elements import TextInput, SelectBox, FloatSliderInput

from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from streamlitfront.base import mk_app

DFLT_CHUNKER_MAKER = lambda: DFLT_CHUNKER
DFLT_FEATURIZER_MAKER = lambda: DFLT_FEATURIZER

FixedSizeChunker = DFLT_CHUNKER
Featurizer = DFLT_FEATURIZER

if 'mall' not in st.session_state:
    st.session_state['mall'] = dict(
        # train_audio={},
        # tag={},
        # unused_store={"to": "illustrate"},
        global_input={}
    )

mall = st.session_state['mall']
mall['global_input'] = ['a name', 3]


def funcnode_maker(name):
    kwargs = metadata[name]
    return FuncNode(**kwargs)


def dag_maker(funcnames_list):
    func_nodes = list(map(funcnode_maker, funcnames_list))
    return DAG(func_nodes)


def f(msg):
    return msg + 'bob'


def g(x):
    return int(x) + 1


def mul(msg_out, multiplier):
    return msg_out * multiplier


metadata = {
    'f': {'func': f, 'out': 'msg_out'},
    'g': {'func': g, 'out': 'multiplier'},
    'mul': {'func': mul, 'out': 'result'},
}

# Make a dag from only typing info
# my_chunker: Chunker    -->
funcnames_list = ['f', 'g', 'mul']


def delegate_input(input_nodes):
    dflt_val = {
        ELEMENT_KEY: SelectBox,
        'options': mall['global_input'],
    }

    return {k: dflt_val for k in input_nodes}


if __name__ == '__main__':

    dag = dag_maker(funcnames_list)
    var_nodes = dag.var_nodes
    print(var_nodes)
    nodes_list = ['x', 'msg']
    print(dag.synopsis_string())

    config_ = {
        APP_KEY: {'title': 'Simple Load and Display'},
        RENDERING_KEY: {
            DAG: {
                'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},
                'execution': {'inputs': delegate_input(nodes_list),},
            },
        },
    }

    app = mk_app([dag], config=config_)
    app()
