# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from abc import abstractmethod
from typing import List, Union
from .utils.utils import ApiInputs
import uuid
from switch_api.pipeline.pipeline import Task

from .models.api import SwitchGuideExecuteApiInput, SwitchGuideApiResponse, SwitchGuideFetchApiInput, SwitchGuideFetchApiResponse, SwitchGuideStepApiResponse
from .models.guide import SwitchGuide, SwitchGuideInstance, SwitchGuideDefinition, SwitchGuideStatus, SwitchGuideSummaryStepConfig
from .models.step import SwitchGuideStep, SwitchGuideStepDefinition, SwitchGuideStepOverrides, SwitchGuideStepStatus


class SwitchGuideTask(Task):
    """Switch Guide Task

    This class is used to run Switch Guide within the Switch Automation Platform.

    """

    DEFAULT_INDEX: int = -1

    def _find_step_in_journeyDef(self, definition: SwitchGuideDefinition, stepId: str):
        index = -1
        for step in definition.steps:
            index = index + 1
            if (uuid.UUID(step.stepId, version=4) == uuid.UUID(stepId, version=4)):
                return (step, index)

        return (None, self.DEFAULT_INDEX)

    def _find_step_def(self, steps: List[SwitchGuideStepDefinition], stepId: str):
        index = self.DEFAULT_INDEX
        for step in steps:
            index = index + 1
            if (uuid.UUID(step.stepId, version=4) == uuid.UUID(stepId, version=4)):
                return (step, index)

        return (None, self.DEFAULT_INDEX)

    def _find_step_in_journey(self, stepId: str, journeyInstance: SwitchGuideInstance):
        index = self.DEFAULT_INDEX
        steps: List[SwitchGuideStepOverrides] = journeyInstance.steps
        for step in steps:
            index = index + 1
            if (step.stepId == stepId):
                return (step, index)

        return (None, self.DEFAULT_INDEX)

    def build_journey_instance(self, definition: SwitchGuideDefinition, journeyInstanceId: str, journeyStepDefinitions: List[SwitchGuideStepDefinition]):
        journeySteps = []

        for s in definition.steps:
            (stepDefinition, _) = self._find_step_def(
                journeyStepDefinitions, s.stepId)

            if (stepDefinition == None):
                continue

            journeySteps.append(SwitchGuideStepOverrides(
                stepId=s.stepId,

                status=SwitchGuideStepStatus(
                    type=stepDefinition.status.type,
                    progress=stepDefinition.status.progress,
                    state=stepDefinition.status.state,
                    uiState=stepDefinition.status.uiState
                )
            ))

        journeyInstance = SwitchGuideInstance(
            # This should come from request and should not be definitionId as it's for an instance of definition
            id=journeyInstanceId,
            status=SwitchGuideStatus(
                # TODO: Check based on current state of steps
                percentageCompleted=0,
                # TODO: Check based on current state of steps or current step fails with ActionRequired or Failed
                state='Pending'
            ),
            steps=journeySteps
        )

        return journeyInstance

    def execute(self, api_inputs: ApiInputs, journey_input: SwitchGuideExecuteApiInput) -> SwitchGuideApiResponse:
        """ DEPRECATED: Method is called by the Journey framework to execute a specific step

        Args:
            api_inputs (ApiInputs): ApiInputs for calling SwitchApi methods
            journey_input (JourneyInput): Input for running Journey step

        Raises:
            Exception: thrown when step response is unexpected 

        Returns:
            JourneyResponse: response associated with the exceution of a step
        """

        currentStepId = journey_input.stepId

        # Future: Retrieved from the Database. Should be passed in from SwitchGuideExecuteApiInput.
        definition = journey_input.journeyDefinition

        stepDefinitions = journey_input.journeyStepDefinitions

        journeyInstance = journey_input.journeyInstance
        if (journeyInstance == None):
            journeyInstance = self.build_journey_instance(
                definition=definition, journeyInstanceId=journey_input.journeyInstanceId, journeyStepDefinitions=stepDefinitions)

        # Future: Retrieved from the Database when Step Definitions are stored there.
        (currentStepDef, index) = self._find_step_def(
            stepDefinitions, currentStepId)

        if (index == self.DEFAULT_INDEX):
            return SwitchGuideApiResponse(success=False, errorMessage="Step Definition could not be found")

        (journeyInstanceStep, _) = self._find_step_in_journey(
            currentStepId, journeyInstance)

        # Future: CurrentStepDef needs to be updated with values from JourneyStepOverrides so latest is available for step.
        result = self.handle_step(
            api_inputs=api_inputs, stepDef=currentStepDef)

        if (type(result) is not SwitchGuideStepApiResponse):
            raise Exception(
                f'Expected SwitchGuideStepApiResponse but got {type(result)}')

        journeySteps = self._build_journey_steps(
            definition=definition, journeyInstance=journeyInstance)

        # Update Journey Steps with changes made during handle_step
        for s in journeySteps:
            if (s.stepId != currentStepId):
                continue

            # TODO: update on journeyStep and journeyInstanceStep are duplicated

            journeyInstanceStep.status.state = result.status.state
            s.status.state = result.status.state

            journeyInstanceStep.status.progress = result.status.progress
            s.status.progress = result.status.progress

            if (result.status.messages):
                journeyInstanceStep.status.messages = result.status.messages
                s.status.messages = result.status.messages

            if (result.uiAssets):
                # TODO: This should be a little smarter and only override values in uiAssets that have changed.
                journeyInstanceStep.uiAssets = result.uiAssets
                s.uiAssets = result.uiAssets

        # Build finalized model of the Journey
        (journey, journeyInstance) = self._build_journey(
            definition=definition, journeyInstance=journeyInstance, journeySteps=journeySteps)

        return SwitchGuideApiResponse(journey=journey, journeyInstance=journeyInstance)

    def get_journey(self, journeyInput: SwitchGuideFetchApiInput) -> SwitchGuideApiResponse:
        definition = journeyInput.journeyDefinition

        journeyInstance = journeyInput.journeyInstance

        steps = journeyInput.journeyStepDefinitions

        journeySteps = self._build_journey_steps(
            definition=definition, journeyInstance=journeyInstance, journeyStepDefinitions=steps)

        (journey, journeyInstance) = self._build_journey(definition=definition,
                                                         journeyInstance=journeyInstance, journeySteps=journeySteps)

        return SwitchGuideFetchApiResponse(journey=journey, journeyInstance=journeyInstance)

    def _build_journey_steps(self, definition: SwitchGuideDefinition,
                             journeyInstance: SwitchGuideInstance, journeyStepDefinitions: List[SwitchGuideStepDefinition]) -> List[SwitchGuideStep]:

        journeySteps: List[SwitchGuideStep] = []

        # Build Journey Steps
        for step in definition.steps:
            (stepDefinition, index) = self._find_step_def(
                journeyStepDefinitions, step.stepId)

            if (index == self.DEFAULT_INDEX):
                continue

            (journeyDefinitionStep, _) = self._find_step_in_journeyDef(
                definition, step.stepId)

            (journeyInstanceStep, _) = self._find_step_in_journey(
                step.stepId, journeyInstance)

            if (journeyInstanceStep == None):
                # Step doesn't exist in Journey Instance.
                # Might happen when a step is added to Journey Definition
                #   after creation of Journey Instance
                journeyInstanceStep = SwitchGuideStepOverrides(
                    stepId=step.stepId,
                    status=SwitchGuideStepStatus(
                        type=stepDefinition.status.type,
                        progress=stepDefinition.status.progress,
                        state=stepDefinition.status.state
                    )
                )

                journeyInstance.steps.append(journeyInstanceStep)
            else:
                # Ensure Status Type is set according to Step Definition
                journeyInstanceStep.status.type = stepDefinition.status.type

                # Override progress component of the Step definition with one from Journey Instance Step
                stepDefinition.status.progress = journeyInstanceStep.status.progress
                stepDefinition.status.state = journeyInstanceStep.status.state
                stepDefinition.status.uiState = journeyInstanceStep.status.uiState

                if (journeyInstanceStep.uiAssets):
                    stepDefinition.uiAssets = journeyInstanceStep.uiAssets

            journeySteps.append(SwitchGuideStep(
                stepId=stepDefinition.stepId,
                callToAction=stepDefinition.callToAction,
                component=stepDefinition.component,
                description=stepDefinition.description,
                icon=stepDefinition.icon,
                isEnabled=stepDefinition.isEnabled,
                isHidden=stepDefinition.isHidden,
                name=stepDefinition.name,
                uiAssets=stepDefinition.uiAssets,
                status=stepDefinition.status,
                dependsOn=journeyDefinitionStep.dependsOn,
                order=journeyDefinitionStep.order,
                events=journeyDefinitionStep.events,
                isBackgroundStep=journeyDefinitionStep.isBackgroundStep
            ))

        return journeySteps

    def _build_journey(self, definition: SwitchGuideDefinition, journeyInstance: SwitchGuideInstance, journeySteps: List[SwitchGuideStep]) -> Union[SwitchGuide, SwitchGuideInstance]:
        # Update Journey Steps with overrides from JourneyInstance
        for s in journeySteps:
            (journeyInstanceStep, _) = self._find_step_in_journey(
                s.stepId, journeyInstance)

            s.status.state = journeyInstanceStep.status.state
            s.status.progress = journeyInstanceStep.status.progress
            s.status.uiState = journeyInstanceStep.status.uiState

            if (journeyInstanceStep.status.messages):
                s.status.messages = journeyInstanceStep.status.messages

            if(journeyInstanceStep.uiAssets):
                s.uiAssets = journeyInstanceStep.uiAssets

            if(journeyInstanceStep.component):
                s.component = journeyInstanceStep.component
            
            if(journeyInstanceStep.data):
                s.data = journeyInstanceStep.data

        journeyInstance = self.update_journey_instance_status(journeyInstance, journeySteps)

        # Represents the entire Journey combining Definition and Instance views
        # Future: Construction of SwitchGuide model should be done on the AF so we can fetch latest model from SQL before updating it.
        #   We could only update the specific step status rather than upserting the entire SwitchGuideInstance json document.
        #   In other words, we need to handle multiple accessing different steps at the same time.
        #   We could consider preventing updates to the journey if the user is working off an outdated state.
        #   We can provide an option for the user to refresh the journey when this happens.
        journey = SwitchGuide(
            id=journeyInstance.id,
            name=definition.name,
            description=definition.description,
            instructions=definition.instructions,
            status=journeyInstance.status,
            steps=journeySteps,  # Combine JourneyDef + JourneyInstance Steps
            summaryStep=self._get_summary_step(journey_definition=definition, journey_instance=journeyInstance)
        )

        return (journey, journeyInstance)

    def _get_summary_step(self, journey_definition: SwitchGuideDefinition, journey_instance: SwitchGuideInstance):
        if journey_instance.status.state != 'Completed':
            return None
        
        if not journey_definition.summaryStep or not journey_definition.summaryStep.events.componentOnCompletion:
            return None
        
        return SwitchGuideSummaryStepConfig(
            component=journey_definition.summaryStep.events.componentOnCompletion
        )

    def update_journey_instance_status(self, journeyInstance: SwitchGuideInstance, journeySteps: List[SwitchGuideStep]):
        # Update Journey Status
        completedSteps = [
            s for s in journeySteps if s.status.state == 'Completed']
        
        stepContributionRatio = 1 / len(journeySteps)

        if (len(completedSteps) == len(journeySteps)):
            journeyInstance.status.state = 'Completed'
            journeyInstance.status.percentageCompleted = 100
        else:
            journeyInstance.status.state = 'Pending'
            journeyInstance.status.percentageCompleted = int(
                len(completedSteps) / len(journeySteps) * 100)
            
        for s in journeySteps:
            if s.status.state == 'Completed':
                continue
            
            if s.status.type == 'Percentage':
                journeyInstance.status.percentageCompleted += int(stepContributionRatio * s.status.progress.completionPercentage)
            elif s.status.type == 'Fraction' and s.status.progress.denominator > 0:
                journeyInstance.status.percentageCompleted += int(stepContributionRatio * (s.status.progress.numerator / s.status.progress.denominator * 100))
                
        if (journeyInstance.status.percentageCompleted > 100):
            journeyInstance.status.percentageCompleted = 100
            
        return journeyInstance

    @abstractmethod
    def handle_step(self, api_inputs: ApiInputs, stepDef: SwitchGuideStepDefinition) -> SwitchGuideStepApiResponse:
        """Method to be implemented to process Guides Journey steps

        The method should contain all code used to execute steps associated specified within JourneyInput

        Parameters
        ----------
        api_inputs: ApiInputs
            object returned by call to initialize()
        journey_input : JourneyInput
            Any settings required to be passed to run Switch Guide steps. Step to process, query keys etc.
        """
        return SwitchGuideStepApiResponse()
