from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import sklearn.compose as sk_compose
    from sklearn.compose import *
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class ColumnTransformer(DataSpecWrapper[sk_compose.ColumnTransformer]):
    @sarus_init("sklearn.SK_COLUMN_TRANSFORMER")
    def __init__(
        self,
        transformers,
        *,
        remainder='drop',
        sparse_threshold=0.3,
        n_jobs=None,
        transformer_weights=None,
        verbose=False,
        verbose_feature_names_out=True,
    ):
        ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y=None):
        ...


register_ops()
