from __future__ import annotations

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init

try:
    import imblearn.over_sampling as imb_over_sampling
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class SMOTENC(DataSpecWrapper[imb_over_sampling.SMOTENC]):
    @sarus_init("imblearn.IMB_SMOTENC")
    def __init__(
        categorical_features,
        *,
        sampling_strategy="auto",
        random_state=None,
        k_neighbors=5,
        n_jobs=None,
    ):
        ...


register_ops()
