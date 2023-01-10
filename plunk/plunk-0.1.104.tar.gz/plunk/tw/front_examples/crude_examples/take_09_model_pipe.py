"""
Same as take_06_model_run, with additionally:
- dispatching learn_model
- introducing iterable_to_enum, inject_enum_annotations (from from front.util)

"""

from functools import partial

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
persisting_stores = mk_mall_of_dill_stores(
    ['model_results', 'learner_store', 'chunkers'], rootdir=rootdir
)
mall = dict(mall_contents, **persisting_stores)

# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# dispatchable function:
from front.crude import prepare_for_crude_dispatch
from front.crude import simple_mall_dispatch_core_func
from front.util import inject_enum_annotations
from front.base import prepare_for_dispatch

from i2 import Pipe
from i2.wrapper import rm_params

from front.util import annotate_func_arguments, iterable_to_enum
from pydantic import confloat
from typing import Optional


annotator = partial(
    annotate_func_arguments,
    annot_for_argname={
        'n_components': Optional[int],  # TODO: Default should be None
        'feature_range': confloat(),
        'iterated_power': int,  # really Union[int, 'auto']
        'random_state': Optional[int],  # TODO: Default should be None
        # TODO: Had iterable_to_enum(["auto", "full", "arpack", "randomized"], "SvdSolverChoices"),
        #  in the following, but led to `Can't pickle <enum 'SvdSolverChoices'>: it's not found as front.util.SvdSolverChoices`
        #  problem. need to use inject_enum_annotations tech somehow
        'svd_solver': str,
        'chk_size': int,
        'chk_step': Optional[int],
    },
    annot_for_dflt_type={bool: bool, int: int, float: float, str: str},
)

# TODO: Conditional Enums: Selection list of one field based on selection of previous
# TODO: Deal with long Enums (paging? filtering?)
# TODO: Enhanced Enum; Give more info to user to be able to choose

# TODO: Better dispatching of mall explorer (needs conditional Enums)
@inject_enum_annotations(action=['list', 'get'], store_name=mall)
def explore_mall(
    store_name: StoreName, key: KT, action: str,
):
    return simple_mall_dispatch_core_func(key, action, store_name, mall=mall)


from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA

# TODO: Again, need for conditional fields
# TODO: Auto-suggestions and/or resolution of arg problems
# TODO: Find more systematic and automatic way to deal with arg names conflicting with
#  Pydantic


# TODO: Make it easier to dispatch "function makers" like make_chunker and make_ffter
# chunker ----------------------------------------------------------------------

from slang.chunkers import fixed_step_chunker


def make_chunker(chk_size: int, chk_step: Optional[int] = None):
    return partial(fixed_step_chunker, chk_size=chk_size, chk_step=chk_step)


chunker = prepare_for_dispatch(make_chunker, output_store=mall['chunkers'],)


# learners ----------------------------------------------------------------------

MinMaxScaler, StandardScaler, PCA = map(
    Pipe(
        rm_params(params_to_remove=['copy']),
        annotator,
        partial(prepare_for_dispatch, output_store=mall['learner_store']),
    ),
    [MinMaxScaler, StandardScaler, PCA],
)


# learn model ----------------------------------------------------------------------

# TODO: param_to_mall_map maker (from list of strings or pairs thereof)
# TODO: automatic mall store enhancer
# TODO: Automatic output_store maker from DAG
# TODO: Automatic defaults from Enum (do the defaults even interact well with Enums?)
dispatchable_learn_model = prepare_for_dispatch(
    learn_model,
    param_to_mall_map={'learner': 'learner_store', 'fvs': 'fvs'},
    mall=mall,
    output_store='fitted_model',
    defaults=dict(learner='StandardScaler', fvs='train_fvs_1',),
)

# apply model ----------------------------------------------------------------------

dispatchable_apply_model = prepare_for_dispatch(
    apply_model,
    param_to_mall_map=['fvs', 'fitted_model'],
    mall=mall,
    output_store='model_results',
    defaults=dict(fitted_model='fitted_model_1', fvs='test_fvs',),
)


if __name__ == '__main__':

    from streamlitfront.page_funcs import SimplePageFuncPydanticWrite

    configs = {'page_factory': SimplePageFuncPydanticWrite}

    from streamlitfront.base import dispatch_funcs

    app = dispatch_funcs(
        [
            chunker,
            MinMaxScaler,
            StandardScaler,
            PCA,
            dispatchable_learn_model,
            dispatchable_apply_model,
            explore_mall,
        ],
        configs=configs,
    )

    # from streamlitfront.base import mk_app
    #
    # app = mk_app(
    #     [
    #         chunker,
    #         MinMaxScaler,
    #         StandardScaler,
    #         PCA,
    #         dispatchable_learn_model,
    #         dispatchable_apply_model,
    #         explore_mall,
    #     ],
    #     config=configs,
    # )
    #

    # print(app)
    print(app)
    print(__file__)
    app()
