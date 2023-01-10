from typing import Union

from ..extensions import UnknownType
from ..models.analysis_step_update_with_message import AnalysisStepUpdateWithMessage
from ..models.analysis_step_update_without_message import AnalysisStepUpdateWithoutMessage

AnalysisStepUpdate = Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType]
