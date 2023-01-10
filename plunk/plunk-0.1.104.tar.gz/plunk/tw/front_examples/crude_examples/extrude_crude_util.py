"""Utils for buildup"""
import os
from typing import Any
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from dol.filesys import mk_tmp_dol_dir

# Being lazy with the definition of these:
FVs = Any
FittedModel = Any
Learner = Any


def get_a_root_directory_for_module_and_mk_tmp_dir_for_it(module_path, verbose=True):
    # if not (isinstance(module_path, str) and os.path.isdir(module_path)):
    #     module_path = module_path.__file__  # assuming it's an object with a __file__

    this_filename, *_ = os.path.splitext(module_path)
    this_filename = os.path.basename(this_filename)
    rootdir = mk_tmp_dol_dir(this_filename)
    if verbose:
        print(f'\n****************************************************')
        print(f'A temp directory was made for {this_filename}')
        print(f'The data will be saved here: {rootdir}')
        print(f'****************************************************')
    return rootdir


# ---------------------------------------------------------------------------------------
# The function(ality) we want to dispatch:
# Note: apply_model and learn_model both have the same structure, just different
#  parameters (names, annotations, defaults).
# TODO: apply_model and learn_model both have the same structure, just different
#  parameters (names, annotations, defaults), so...
#  Could make them from i2.wrapper tools. Should is a different question though.


def learn_model(learner: Learner, fvs: FVs, method='fit'):
    method_func = getattr(learner, method)
    return method_func(list(fvs))


def apply_model(fitted_model: FittedModel, fvs: FVs, method='transform'):
    method_func = getattr(fitted_model, method)
    # TODO: Should remove .tolist() (and possibly the list of list(fvs)).
    #  Not concern here.
    return method_func(list(fvs)).tolist()


# TODO: Make a sklearn-free and numpy-free version?
# class MinMaxScaler:
#     def fit(self, X):
#         self.min_ = min(X)

# ---------------------------------------------------------------------------------------
# The stores that will be used -- here, all stores are just dictionaries, but the
# contract is with the typing.Mapping (read-only here) interface.
# As we grow up, we'll use other mappings, such as:
# - server side RAM (as done here, simply)
# - server side persistence (files or any DB or file system thanks to the dol package)
# - computation (when you want the request for a key to actually launch a process that
#   will generate the value for you (some say you should be obvious to that detail))
# - client side RAM (when we figure that out)

# really, should be a str from a list of options, given by list(fvs_store)
FVsKey = str
# really, should be a str from a list of options, given by list(fitted_model_store)
FittedModelKey = str
Result = Any
ResultKey = str

mall = dict(
    fvs=dict(  # Mapping[FVsKey, FVs]
        train_fvs_1=np.array([[1], [2], [3], [5], [4], [2], [1], [4], [3]]),
        train_fvs_2=np.array([[1], [10], [5], [3], [4]]),
        test_fvs=np.array([[1], [5], [3], [10], [-5]]),
    ),
    fitted_model=dict(  # Mapping[FittedModelKey, FittedModel]
        fitted_model_1=MinMaxScaler().fit(
            [[1], [2], [3], [5], [4], [2], [1], [4], [3]]
        ),
        fitted_model_2=MinMaxScaler().fit([[1], [10], [5], [3], [4]]),
    ),
    model_results=dict(),  # Mapping[ResultKey, Result]
)

mall_with_learners = dict(
    mall,
    **dict(
        learner_store=dict(
            MinMaxScaler=MinMaxScaler(), StandardScaler=StandardScaler(), PCA=PCA(),
        )
    ),
)


def test_dispatch(dispatcher):
    w_apply_model = dispatcher(
        apply_model,
        param_to_mall_map=['fvs', 'fitted_model'],
        mall=mall,
        include_stores_attribute=True,
    )
    assert (
        w_apply_model('fitted_model_1', 'test_fvs')
        == [[0.0], [1.0], [0.5], [2.25], [-1.5]]
        == apply_model(
            fitted_model=w_apply_model.store_for_param['fitted_model'][
                'fitted_model_1'
            ],
            fvs=w_apply_model.store_for_param['fvs']['test_fvs'],
        )
    )
