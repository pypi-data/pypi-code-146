# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import Optional, Union
from typing import List
from pydantic import BaseModel
from .literals import STATUS_STATE, STATUS_TYPE


class SwitchGuideStepComponent(BaseModel):
    type: str
    id: str
    attributes: dict


class SwitchGuideStepCallToAction(BaseModel):
    path: str
    step: Optional[str] = ''
    description: Optional[str] = ''
    autoRedirectOnStepCompletion: Optional[bool] = False


class SwitchGuideStepStatusProgress(BaseModel):
    """Contains properties that help build the full picture of the status of a step. Not all properties might be relevant for each step.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """
    count: int = 0
    completionPercentage: int = 0
    numerator: int = 0
    denominator: int = 0


class SwitchGuideStepData(dict):
    pass


class SwitchGuideStepStatusUiState(BaseModel):
    """Keep the step locked on the UI when True; otherwise unlock it.
    Attribute relevant for UI
    """

    lockStep: bool = False
    """Keep the step locked on the UI when True; otherwise unlock it."""

    returnToSummary: bool = False
    """Indicates that we should return user to Summary step on Step Execution.
    Note: This will take the user to the even if next step is available.
    Note 2: Supersedes the 'continueToNextStep' property.
    """

    continueToNextStep: bool = False
    """Indicates that we should continue to next step on Step Execution.
    Note: This will take the user to the next step even when next step is already completed.
    Note 2: This property is ignored if the 'returnToSummary' property is set to True.
    """

    continueToNextStepWhenAvailable: bool = False
    """Indicates that we should continue to next step on Step Execution when next is available.
    Note: This will take the user to the next available incomplete step otherwise it will take the user to summary step.
    Note 2: This property is ignored if the 'returnToSummary' property is set to True.
    Note 3: This property is ignored if the 'continueToNextStep' property is set to True.
    """

class SwitchGuideStepStatus(BaseModel):
    """Status of the Journey Step
    """

    type: STATUS_TYPE = 'Percentage'
    """Type of status this is. Based on the type different property values would be relevant

    Available types and their relevant properties:

    Percentage
        - progress.percentageCompleted    [int]
        - messages.default                [str]

    StateBased
        - messages.completed      [str]   (when state == Completed)
        - messages.pending        [str]   (when state == Pending)
        - messages.actionRequired [str]   (when state == ActionRequired)
        - messages.failed         [str]   (when state == Failed)

    Count
        - progress.count [int]
        - messages.count [str]  (replaces occurrences of {{count}} in the message with the value of progress.count)

    Fraction
        - progress.numerator   [int]
        - progress.denominator [int]
        - messages.default     [str] (replaces occurrences of {{numerator}} and {{denominator}} in the message with the values of progress.numerator and progress.denominator respectively)

    Simple
        - messages.default     [str]

    """

    state: STATUS_STATE = 'Queued'
    """State of the step"""

    messages: dict = {}
    """Messages associated with the step. Contains at least 'default' message"""

    progress: SwitchGuideStepStatusProgress = SwitchGuideStepStatusProgress()
    """Progress data"""

    uiState: SwitchGuideStepStatusUiState = SwitchGuideStepStatusUiState()
    """UI State
    Dynamically control UI state of the step.
    """

class SwitchGuideStepDefinitionUiAssets(BaseModel):
    """Dynamically adjustable config to change UI look and feel. 
    """
    
    stepContinueButtonText: str = 'Get Started'
    """Step continue button text
    """

    progressCtaDescription: Optional[str] = None
    """Call To Action description to associate with the path.
    """

    progressCtaPath: Optional[str] = None
    """Call To Action path. Expected to be an internal route in the Platform App for now.
    """

    progressCtaText: Optional[str] = 'Click here'
    """Call To Action text. By default it will be "Click here".
    """

    stepBannerText: Optional[str] = None
    """Text contained in the banner.
    """

    stepBannerType: Optional[str] = None
    """Type of the banner. By default it will be of Type 'Note'.
    In the future it could also be warnings and errors.
    """

    isPromotional: Optional[bool] = False
    """Treat step as a promotional step with limited function.
    Purely for cosmetic purposes. Specific limitations should be handled by other means.
    """

    enableUpgrade: Optional[bool] = False
    """Controls whether to display Upgrade request button across the Guide.
    """

class SwitchGuideStepDefinition(BaseModel):
    """Shape of the a Step. This defines what a step is and the data is shared by instances of the step.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """
    
    stepId: str = ''
    """Id of the Step - same as the Step Definition driver id."""

    name: str
    """Name of the step visible to the user on the Guides UI"""
    
    description: str
    """Description visible to the user on the Guides UI"""

    status: SwitchGuideStepStatus = SwitchGuideStepStatus()
    """Status associated with the Step"""
    
    icon: str
    """Icon associated with the step"""

    isEnabled: bool = True
    """Indicates whether the step is enabled or not. If not enabled, the step will not be visible to the user."""

    isHidden: bool = False
    """When True, hides the step on the left tracker of the Guides UI. 
    And displays in the summary page when (if any) onDepends conditions are met.
    When False, step will always be visible on the left tracker and summary page of the Guides UI.
    """

    callToAction: Union[SwitchGuideStepCallToAction, None] = None
    
    component: Union[SwitchGuideStepComponent, None] = None
    """Custom component to display on the Guides UI
    """

    uiAssets: SwitchGuideStepDefinitionUiAssets = SwitchGuideStepDefinitionUiAssets()
    """Configuration to customize certain elements of the Guides UI
    """


class SwitchGuideStepDependencyEvents(BaseModel):
    checkStatusOnJourneyCreation: bool = True
    """Check status of the step on Journey creation"""

    triggerProcessOnStepCompletion: List[str] = []
    """List of step ids that should be processed when this step is completed"""

    preventStatusCheckBeforeDependsOn: bool = False
    """When true, status check will not be called for this step until dependent steps are completed"""


class SwitchGuideStepDependency(BaseModel):
    """Represents the instance of a step where the state might not be the same as other instances of the same step
    """

    stepId: str
    """Id of the step instance"""

    order: Optional[int]
    """Order to appear on the Frontend UIs.
        Optional when when Step is marked as a Background Step
    """
    
    dependsOn: List[str] = []
    """When a step depends on another step, the step is only unlocked on UI when the other step is completed.
    """
    
    events: SwitchGuideStepDependencyEvents = SwitchGuideStepDependencyEvents()
    """Events associated with the step in relation to the journey or other steps within the journey.
    """

    isBackgroundStep: bool = False
    """When True, step is expected to run on event trigger and will not be returned to the frontend.
    """

    options: Optional[dict] = {}
    """Options to be passed to the step driver. Options are unique to each step so consult the Step documentation."""

class SwitchGuideStepOverrides(BaseModel):
    """Represents the simplest view of a step. Useful for maintain overrides for the step without duplicating the data.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """

    stepId: str
    status: SwitchGuideStepStatus
    component: Union[SwitchGuideStepComponent, None] = None
    uiAssets: Optional[SwitchGuideStepDefinitionUiAssets]
    data: Optional[SwitchGuideStepData] = {}


class SwitchGuideStep(SwitchGuideStepDefinition, SwitchGuideStepDependency):
    """Full Journey Step Model

    Args:
        SwitchGuideStepDefinition (_type_): Represents the step shape
        SwitchGuideStepDependency (_type_): Represents the shape of a step within a Journey dependency
    """
    stepId: str
    data: Optional[SwitchGuideStepData] = {}
