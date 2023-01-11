from typing import List

from truera.client.private.metarepo import DataSplit
from truera.protobuf.public.metadata_message_types_pb2 import \
    SplitStatus  # pylint: disable=no-name-in-module


def _filter_to_active_splits(splits_list: List[DataSplit]) -> List[DataSplit]:
    accept_statuses = [
        SplitStatus.SPLIT_STATUS_INVALID, SplitStatus.SPLIT_STATUS_ACTIVE
    ]
    return [s for s in splits_list if s.status in accept_statuses]
