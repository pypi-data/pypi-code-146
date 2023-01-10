from typing import Union

from ..extensions import UnknownType
from ..models.analysis_step_dataset_data import AnalysisStepDatasetData
from ..models.analysis_step_file_data import AnalysisStepFileData

AnalysisStepData = Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]
