from typing import Union

from ..extensions import UnknownType
from ..models.analysis_dataset_ids import AnalysisDatasetIds
from ..models.file_ids import FileIds

AnalysisStepDataUpdate = Union[FileIds, AnalysisDatasetIds, UnknownType]
