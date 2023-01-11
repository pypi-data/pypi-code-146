from typing import Mapping

import numpy as np
import pandas as pd

# pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import Segment as SegmentProto
from truera.protobuf.public.data.segment_pb2 import \
    Segmentation as SegmentationProto
# pylint: enable=no-name-in-module
from truera.utils.filter_utils import FilterProcessor


class Segment:
    name: str
    project_id: str
    _segment_proto: SegmentProto

    def __init__(self, name: str, project_id: str, segment_proto: SegmentProto):
        self.name = name
        self.project_id = project_id
        self._segment_proto = segment_proto

    def _validate_apply(self, data: pd.DataFrame):
        filter_requirements = FilterProcessor.get_filter_requirements(
            self._segment_proto.filter_expression
        )
        if filter_requirements.requires_ground_truth:
            raise ValueError("Cannot apply filter on ground truth data!")
        if filter_requirements.requires_index:
            raise ValueError("Cannot apply filter on indices!")
        if filter_requirements.model_ids_to_score_type:
            raise ValueError("Cannot apply filter on model outputs!")
        if filter_requirements.segmentation_ids:
            raise ValueError("Cannot apply filter on segment IDs!")
        cols = filter_requirements.column_names
        for col in cols:
            if not col in data:
                raise ValueError(
                    f"Cannot apply filter on non-existent column \"{col}\"!"
                )

    def apply(self, data: pd.DataFrame) -> np.ndarray:
        """Applies the filter associated with this segment to the provided data.

        Args:
            data: Data to apply segment on.

        Returns:
            np.ndarray: Boolean array of same length of `data`, indicating whether each row meets the filter requirements
        """
        self._validate_apply(data)
        return FilterProcessor.filter(
            data, self._segment_proto.filter_expression
        )

    def pretty_print(self):
        """Print out the filter associated with this segment.
        """
        print(self)

    def ingestable_definition(self) -> str:
        return FilterProcessor.stringify_filter(
            self._segment_proto.filter_expression, ingestable=True
        )

    @property
    def is_protected(self) -> bool:
        return self._segment_proto.is_protected

    def __str__(self) -> str:
        rep = f"Segment {self.name}\n\t"
        rep += FilterProcessor.stringify_filter(
            self._segment_proto.filter_expression
        ).replace("\n", "\n\t")
        return rep


class SegmentGroup:
    name: str
    id: str
    segments: Mapping[str, Segment]
    _segmentation_proto: SegmentationProto

    def __init__(
        self, name: str, id: str, segments: Mapping[str, Segment],
        segmentation_proto: SegmentationProto
    ):
        self.name = name
        self.id = id
        self.segments = segments
        self._segmentation_proto = segmentation_proto

    def get_segments(self) -> Mapping[str, Segment]:
        """Returns all segments present in the given segment group. 

        Returns:
            Mapping[str, Segment]: Map from each segment name to its corresponding Segment object. 
        """
        return self.segments

    def pretty_print(self):
        """Print out this segmentation and its associated segments.
        """
        print(self)

    def __str__(self) -> str:
        rep = f"Segment group {self.name}"
        for segment in self.segments:
            rep += f"\n--Segment {segment}"
        return rep
