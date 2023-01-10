import streamlit as st
from front import APP_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY, RENDERING_KEY
from front.crude import Crudifier, prepare_for_crude_dispatch
from streamlitfront import mk_app
from streamlitfront.elements import SelectBox
from streamlitfront import binder as b

DFLT_INPUT = 'my text'


def do_something(wf_src):
    return wf_src


# if "mall" not in st.session_state:
#     st.session_state["mall"] = dict(
#         wfsource={"wfsrc": DFLT_INPUT},
#     )

if not b.mall():
    b.mall = dict(wfsource={'wfsrc': DFLT_INPUT},)

mall = b.mall()

# mall = st.session_state["mall"]


# @Crudifier(mall=mall, param_to_mall_map={"wf_src": "wfsource"})
def example(wf_src):
    result = do_something(wf_src)  # better tuple wfs_train, wfs_test
    return result  # put a return, different from the code_to_dag example


example = prepare_for_crude_dispatch(
    example, mall=mall, param_to_mall_map={'wf_src': 'wfsource'}
)

config_ = {
    APP_KEY: {'title': 'Crudified learner'},
    RENDERING_KEY: {
        'example': {
            'execution': {
                'inputs': {
                    'wf_src': {ELEMENT_KEY: SelectBox, 'options': mall['wfsource'],},
                },
            }
        },
    },
}

app = mk_app([example], config=config_,)
app()
# st.write(locals())
