from __future__ import annotations

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import imblearn.pipeline as imb_pipeline
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class Pipeline(DataSpecWrapper[imb_pipeline.Pipeline]):
    @sarus_init("imblearn.IMB_PIPELINE")
    def __init__(steps, *, memory=None, verbose=False):
        ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y=None):
        ...


register_ops()
