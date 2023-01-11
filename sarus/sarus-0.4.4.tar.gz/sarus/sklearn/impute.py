from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import sklearn.impute as sk_impute
    from sklearn.impute import *
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class SimpleImputer(DataSpecWrapper[sk_impute.SimpleImputer]):
    @sarus_init("sklearn.SK_SIMPLE_IMPUTER")
    def __init__(self, steps, *, memory=None, verbose=False):
        ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y=None):
        ...


register_ops()
