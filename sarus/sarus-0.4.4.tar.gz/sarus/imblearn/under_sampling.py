from __future__ import annotations

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init

try:
    import imblearn.under_sampling as imb_under_sampling
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class RandomUnderSampler(
    DataSpecWrapper[imb_under_sampling.RandomUnderSampler]
):
    @sarus_init("imblearn.IMB_RANDOM_UNDER_SAMPLER")
    def __init__(
        self, *, sampling_strategy="auto", random_state=None, replacement=False
    ):
        ...


register_ops()
