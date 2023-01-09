"""
Same as take_06_model_run, with additionally:
- dispatching learn_model
- introducing iterable_to_enum, inject_enum_annotations (from from front.util)

"""

import os

from crude.extrude_crude.extrude_crude_util import (
    apply_model,
    learn_model,
    test_dispatch,
    mall_with_learners as mall_contents,
    get_a_root_directory_for_module_and_mk_tmp_dir_for_it,
)

from front.crude import KT, StoreName, Mall, mk_mall_of_dill_stores

rootdir = get_a_root_directory_for_module_and_mk_tmp_dir_for_it(__file__)

# Here we want to use the RAM mall_contents for fvs and fitted_models, but
# a dill mall (persisted) for model_results
# ram_stores = mall_contents
persisting_stores = mk_mall_of_dill_stores('model_results', rootdir=rootdir)
mall = dict(mall_contents, **persisting_stores)

# ---------------------------------------------------------------------------------------
# dispatchable function:
from front.crude import prepare_for_crude_dispatch
from front.crude import simple_mall_dispatch_core_func
from front.util import inject_enum_annotations
from front.base import prepare_for_dispatch


@inject_enum_annotations(action=['list', 'get'], store_name=mall)
def explore_mall(
    store_name: StoreName, key: KT, action: str,
):
    return simple_mall_dispatch_core_func(key, action, store_name, mall=mall)


dispatchable_learn_model = prepare_for_dispatch(
    learn_model,
    param_to_mall_map={'learner': 'learner_store', 'fvs': 'fvs'},
    mall=mall,
    output_store='fitted_model',
    defaults=dict(learner='StandardScaler', fvs='train_fvs_1',),
)

dispatchable_apply_model = prepare_for_dispatch(
    apply_model,
    param_to_mall_map=['fvs', 'fitted_model'],
    mall=mall,
    output_store='model_results',
    defaults=dict(fitted_model='fitted_model_1', fvs='test_fvs',),
)


if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from streamlitfront.page_funcs import SimplePageFuncPydanticWrite

    configs = {'page_factory': SimplePageFuncPydanticWrite}

    app = dispatch_funcs(
        [dispatchable_learn_model, dispatchable_apply_model] + [explore_mall],
        configs=configs,
    )
    # print(app)
    print(app)
    print(__file__)
    app()
