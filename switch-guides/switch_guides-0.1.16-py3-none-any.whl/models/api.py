# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import List, Optional, Union
import uuid
from pydantic import BaseModel
from .guide import SwitchGuide, SwitchGuideDefinition, SwitchGuideInstance
from .step import SwitchGuideStepComponent, SwitchGuideStepDefinition, SwitchGuideStepDefinitionUiAssets, SwitchGuideStepData, SwitchGuideStepStatus, SwitchGuideStepStatusUiState


class SwitchGuideExecuteApiInput(BaseModel):
    journeyInstanceId: str
    journeyInstance: SwitchGuideInstance = None
    journeyDefinition: SwitchGuideDefinition = None
    journeyStepDefinitions: List[SwitchGuideStepDefinition] = []
    stepId: str = ''
    data: dict = ''


class SwitchGuideStepApiResponse(BaseModel):
    component: Union[SwitchGuideStepComponent, None] = None
    """Component to be displayed on the UI temporarily.
    Useful to display component to the user that's only relevant after a step is immediately executed.
    Example: Step execution fails and so we would like to display a error component temporarily with additional information.
    Note: This is not persisted in the database. Will be overwritten when check_ui_component is called.
    Ensure that check_ui_component is updated to match the component to display during a given state.
    """

    uiState: SwitchGuideStepStatusUiState = SwitchGuideStepStatusUiState()
    """Dynamically control UI state of the step.
    Maybe overwritten by check_status() function. Ensure they are in sync if experiencing issues.
    """

    data: dict = None
    """[Deprecated]
    Values set on this property are ignored. Will be removed in future versions.
    """

    errorMessage: str = ''
    """[Deprecated]
    Values set on this property are ignored. Will be removed in future versions.
    """

    status: SwitchGuideStepStatus = None
    """[Deprecated]
    Values set on this property are ignored. Will be removed in future versions.
    """

    uiAssets: SwitchGuideStepDefinitionUiAssets = None
    """[Deprecated]
    Values set on this property are ignored. Will be removed in future versions.
    """


class SwitchGuideApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: SwitchGuide = None
    journeyInstance: SwitchGuideInstance = None


class SwitchGuideFetchApiInput(BaseModel):
    journeyInstance: SwitchGuideInstance = None
    journeyDefinition: SwitchGuideDefinition = None
    journeyStepDefinitions: List[SwitchGuideStepDefinition] = []


class SwitchGuideFetchApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: SwitchGuide = None
    journeyInstance: SwitchGuideInstance = None


class SwitchGuideStepProcessInput(BaseModel):
    journey_id: uuid.UUID
    """[Deprecated] Prefer to use guide_id property as this will be removed in future versions."""

    guide_id: Optional[uuid.UUID]
    """Unique identifier for the Guide"""

    stepData: Optional[SwitchGuideStepData] = {}
    """Data associated with the step"""
