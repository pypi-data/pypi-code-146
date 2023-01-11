from typing import Dict
from typing import List
from typing import Tuple

import attrs

from tecton_core.data_types import data_type_from_proto
from tecton_core.data_types import DataType
from tecton_proto.common import schema_pb2


@attrs.frozen
class Schema:
    proto: schema_pb2.Schema

    # TODO(jake): Remove this method. Just access proto attr directly.
    def to_proto(self):
        return self.proto

    def column_names(self):
        return [c.name for c in self.proto.columns]

    def column_name_and_data_types(self) -> List[Tuple[str, DataType]]:
        return [(c.name, data_type_from_proto(c.offline_data_type)) for c in self.proto.columns]

    def to_dict(self) -> Dict[str, DataType]:
        return dict(self.column_name_and_data_types())
