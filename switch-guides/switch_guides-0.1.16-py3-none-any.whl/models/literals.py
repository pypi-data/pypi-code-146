from typing import Dict, Literal


STATUS_STATE = Literal['Queued', 'Pending', 'Completed', 'ActionRequired', 'Failed']

STATUS_TYPE = Literal['Percentage',
                      'StateBased', 'Count', 'Fraction', 'Simple']

STEP_EVENTS = Literal['CheckStatusOnJourneyCreation',
                      'TriggerProcessOnStepCompletion']

SIGNALR_HUBNAMES = Literal['Journeys']
SIGNALR_TARGET_METHODS = Literal['journey-full']

JOURNEY_NOTIFICATION_FEATURE_NAME = 'platform-journeys'

JOURNEY_EVENT_DEFINITION_IDS = Literal['journey-completed',
                                        'journey-failed', 'journey-required']

JOURNEY_STEP_EVENT_DEFINITION_IDS = Literal['journey-step-completed',
                                            'journey-step-failed', 'journey-step-action-required']

JOURNEY_EVENT_DEFINITION_MAP: Dict[STATUS_STATE, JOURNEY_EVENT_DEFINITION_IDS] = {
    'Completed': 'journey-completed',
    'ActionRequired': 'journey-action-required',
    'Failed': 'journey-failed'
}

JOURNEY_STEP_EVENT_DEFINITIONS_MAP: Dict[STATUS_STATE, JOURNEY_STEP_EVENT_DEFINITION_IDS] = {
    'Completed': 'journey-step-completed',
    'ActionRequired': 'journey-step-action-required',
    'Failed': 'journey-step-failed'
}

NOTIFICATION_FIELD_PORTFOLIO_NAME = 'PortfolioName'
