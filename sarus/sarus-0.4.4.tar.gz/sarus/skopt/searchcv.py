from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import skopt.searchcv as skopt_searchcv
    from skopt.searchcv import *
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class BayesSearchCV(DataSpecWrapper[skopt_searchcv.BayesSearchCV]):
    @sarus_init("skopt.SKOPT_BAYES_SEARCH_CV")
    def __init__(
        self,
        estimator,
        search_spaces,
        optimizer_kwargs=None,
        n_iter=50,
        scoring=None,
        fit_params=None,
        n_jobs=1,
        n_points=1,
        iid=True,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch='2*n_jobs',
        random_state=None,
        error_score='raise',
        return_train_score=False,
    ):
        ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y=None):
        ...


register_ops()
