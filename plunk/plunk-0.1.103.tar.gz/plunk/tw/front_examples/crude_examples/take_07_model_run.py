"""
Same as take_06_model_run, with additionally:
- dispatching learn_model
- introducing iterable_to_enum, inject_enum_annotations (from from front.util)

"""

import os

from crude.extrude_crude.extrude_crude_util import apply_model, learn_model
from crude.extrude_crude.extrude_crude_util import mall_with_learners as mall_contents

from dol.filesys import mk_tmp_dol_dir
from front.crude import KT, StoreName, Mall, mk_mall_of_dill_stores

# def mk_mall(rootdir=None, mall_contents=mall_contents) -> Mall:
#     rootdir = rootdir or mk_tmp_quick_store_dirpath("crude_takes")
#     print(rootdir)
#     mall = dict()
#     for k, store_contents in mall_contents.items():
#         mall[k] = QuickStore(os.path.join(rootdir, k))
#         mall[k].update(store_contents)
#     return mall


# class ReadOnlyDict(dict):
#     def __setitem__(self, k):
#         if k in self:

# mall = mk_mall()
from collections import ChainMap

this_filename, *_ = os.path.splitext(__file__)
this_filename = os.path.basename(this_filename)
print(this_filename)
rootdir = mk_tmp_dol_dir(this_filename)
print(f'\n****************************************************')
print(f'The data will be saved here: {rootdir}')
print(f'****************************************************')

# Here we want to use the RAM mall_contents for fvs and fitted_models, but
# a dill mall (persisted) for model_results
# ram_stores = mall_contents
persisting_stores = mk_mall_of_dill_stores('model_results', rootdir=rootdir)
mall = dict(mall_contents, **persisting_stores)

# ---------------------------------------------------------------------------------------
# dispatchable function:
from front.crude import prepare_for_crude_dispatch

w_apply_model = prepare_for_crude_dispatch(
    apply_model,
    param_to_mall_map=['fvs', 'fitted_model'],
    mall=mall,
    include_stores_attribute=True,
)
assert (
    w_apply_model('fitted_model_1', 'test_fvs')
    == [[0.0], [1.0], [0.5], [2.25], [-1.5]]
    == apply_model(
        fitted_model=w_apply_model.store_for_param['fitted_model']['fitted_model_1'],
        fvs=w_apply_model.store_for_param['fvs']['test_fvs'],
    )
)


if __name__ == '__main__':

    from functools import partial
    from streamlitfront.base import dispatch_funcs
    from front.crude import simple_mall_dispatch_core_func
    from front.util import iterable_to_enum, inject_enum_annotations

    # TODO: the function doesn't see updates made to mall. Fix.
    # Just the partial (with mall set), but without mall arg visible (or will be
    # dispatched)
    def explore_mall(
        key: KT,
        action: str,  # iterable_to_enum(["list", "get"], "MallActions"),
        store_name: StoreName,
    ):
        return simple_mall_dispatch_core_func(key, action, store_name, mall=mall)

    dispatchable_apply_model = prepare_for_crude_dispatch(
        apply_model,
        param_to_mall_map=['fvs', 'fitted_model'],
        mall=mall,
        output_store='model_results',
    )
    # extra, to get some defaults in:
    dispatchable_apply_model = partial(
        dispatchable_apply_model, fitted_model='fitted_model_1', fvs='test_fvs',
    )

    dispatchable_learn_model = prepare_for_crude_dispatch(
        learn_model,
        param_to_mall_map={'learner': 'learner_store', 'fvs': 'fvs'},
        mall=mall,
        output_store='fitted_model',
    )

    # inject an Enum (fed by mall['learners']) in learners arg
    dispatchable_learn_model = inject_enum_annotations(
        dispatchable_learn_model, learner=list(mall['learner_store'])
    )

    # # extra, to get some defaults in:
    # dispatchable_learn_model = partial(
    #     dispatchable_learn_model,
    #     fitted_model="fitted_model_1",
    #     fvs="test_fvs",
    # )

    from streamlitfront.page_funcs import SimplePageFuncPydanticWrite

    configs = {'page_factory': SimplePageFuncPydanticWrite}
    app = dispatch_funcs(
        [dispatchable_apply_model, explore_mall, dispatchable_learn_model],
        configs=configs,
    )
    print(app)
    app()
