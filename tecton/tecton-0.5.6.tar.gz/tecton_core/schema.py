from typing import Dict
from typing import List
from typing import Tuple

from tecton_core.data_types import data_type_from_proto
from tecton_core.data_types import DataType


class Schema:
    def __init__(self, proto):
        self._proto = proto

    def to_proto(self):
        return self._proto

    def _column(self, column_name):
        cs = [c for c in self._proto.columns if c.name == column_name]
        if not cs:
            raise ValueError(f"Unknown column: {column_name}. Schema is: {self._proto}")
        return cs[0]

    def column_names(self):
        return [c.name for c in self._proto.columns]

    def column_name_and_data_types(self) -> List[Tuple[str, DataType]]:
        return [(c.name, data_type_from_proto(c.offline_data_type)) for c in self._proto.columns]

    def to_dict(self) -> Dict[str, DataType]:
        return dict(self.column_name_and_data_types())
