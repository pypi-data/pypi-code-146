from meshed import code_to_dag
from plunk.sb.front_experiments.data_visualizer.utils.tools import (
    store_to_key_fvs,
    key_fvs_to_tag_fvs,
    mk_Xy,
)

d_input = {
    'store_to_key_fvs': store_to_key_fvs,
    'key_fvs_to_tag_fvs': key_fvs_to_tag_fvs,
    'mk_Xy': mk_Xy,
}


@code_to_dag(func_src=d_input)
def load_dataset():
    key_fvs = store_to_key_fvs(wf_store)
    tag_fv_iterator = key_fvs_to_tag_fvs(key_fvs, annots_df=annots_df)
    X, y = mk_Xy(tag_fv_iterator)
