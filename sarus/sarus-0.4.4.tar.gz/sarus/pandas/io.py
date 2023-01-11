import pandas as pd

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops


class PrettyDict(DataSpecWrapper[pd.io.formats.printing.PrettyDict]):
    ...


register_ops()
