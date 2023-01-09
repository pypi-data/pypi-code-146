from meshed import FuncNode, DAG
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

from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from streamlitfront.base import mk_app

DFLT_CHUNKER_MAKER = lambda: DFLT_CHUNKER
DFLT_FEATURIZER_MAKER = lambda: DFLT_FEATURIZER

FixedSizeChunker = DFLT_CHUNKER
Featurizer = DFLT_FEATURIZER


def funcnode_maker(name):
    kwargs = metadata[name]
    return FuncNode(**kwargs)


def dag_maker(funcnames_list):
    func_nodes = list(map(funcnode_maker, funcnames_list))
    return DAG(func_nodes)


metadata = {
    'FixedSizeChunker': {'func': FixedSizeChunker, 'out': 'chks'},
    'FixedSizeChunker100': {'out': 'chks'},
    'ThresholdChunker': {'out': 'chks'},
    'FixedSizeChunkerMaker': {'func': DFLT_CHUNKER_MAKER, 'out': 'chunker'},
    'FeaturizerMaker': {'func': DFLT_FEATURIZER_MAKER, 'out': 'featurizer'},
    'key_fvs_to_tag_fvs': {'func': key_fvs_to_tag_fvs},
    'Featurizer': {'func': DFLT_FEATURIZER, 'out': 'fvs'},
    'store_to_key_fvs': {'func': store_to_key_fvs, 'out': 'key_fvs'},
    'key_fvs_to_tag_fvs': {'func': key_fvs_to_tag_fvs, 'out': 'tag_fv_iterator'},
    'WfStoreMaker': {
        'func': data_from_wav_folder,
        'out': 'wf_store',
        'bind': {'filepath': 'wf_filepath'},
    },
    'AnnotsStoreMaker': {'func': data_from_csv, 'out': 'annots_df'},
    'mk_Xy': {'func': mk_Xy},
}

# Make a dag from only typing info
# my_chunker: Chunker    -->


if __name__ == '__main__':
    # example
    # pyckup
    wf_filepath = '/Users/sylvain/Dropbox/Otosense/VacuumEdgeImpulse/'
    annots_filepath = '/Users/sylvain/Dropbox/sipyb/Testing/data/annots_vacuum.csv'

    funcnames_list = [
        'FixedSizeChunkerMaker',
        'FeaturizerMaker',
        'WfStoreMaker',
        'AnnotsStoreMaker',
        'key_fvs_to_tag_fvs',
        'store_to_key_fvs',
        'key_fvs_to_tag_fvs',
        'mk_Xy',
    ]
    # do a multiselect to do the selection
    # validation, errors to be checked
    dag = dag_maker(funcnames_list)
    print(dag.synopsis_string())

    config_ = {
        APP_KEY: {'title': 'Simple Load and Display'},
        RENDERING_KEY: {DAG: {'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},},},
    }

    app = mk_app([dag], config=config_)
    app()
