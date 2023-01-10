import streamlit as st
from front.crude import Crudifier
from typing import Any
from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
import streamlit as st


from streamlitfront import mk_app, binder as b
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront.elements import SelectBox

from front.crude import Crudifier


from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep5 import (
    DFLT_CHUNKER_MAKER,
    DFLT_FEATURIZER_MAKER,
)

# ============ MALL ===============
if not b.mall():
    b.mall = dict(factory_store={}, factory_objects_store={})

mall = b.mall()


mall['factory_store'] = [
    'FixedSizeChunkerMaker',
    'FeaturizerMaker',
]

metadata = {
    'FixedSizeChunkerMaker': {'func': DFLT_CHUNKER_MAKER, 'out': 'chunker'},
    'FeaturizerMaker': {'func': DFLT_FEATURIZER_MAKER, 'out': 'featurizer'},
}

# ============ DFLT FACTORIES =====

# select_factories = Crudifier(output_store="factories", mall=mall)(select_factories)


@Crudifier(output_store='factory_objects_store', mall=mall)
def select_factory(factory):
    return metadata[factory]


# ============ BACKEND ============
def make_functions():
    pass


# ============ END BACKEND ============


# ============ FRONT END   ============


config_ = {
    APP_KEY: {'title': 'Data Prepper'},
    RENDERING_KEY: {
        'select_factory': {
            NAME_KEY: 'Select factories',
            # "description": {"content": get_data_description},
            'execution': {
                'inputs': {
                    'factory': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['factory_store'],
                    },
                },
            },
        },
    },
}
# ============ END FRONTEND ============

if __name__ == '__main__':
    app = mk_app([select_factory], config=config_)
    app()
    st.write(mall)
