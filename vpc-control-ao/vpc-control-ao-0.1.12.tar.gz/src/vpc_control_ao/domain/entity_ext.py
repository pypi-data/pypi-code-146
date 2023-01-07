from ddd_objects.domain.entity import Entity
from typing import Optional, Any, Callable
from .value_obj_ext import PipelineContext, PipelineIndicator
from .value_obj import Name

class _PipelineStage(Entity):
    def __init__(
        self,
        stage_name: str,
        action: Callable,
        allow_failure: bool=False
    ) -> None:
        self.stage_name = stage_name
        self.action = action
        self.allow_failure = allow_failure

class PipelineActionOutput(Entity):
    def __init__(
        self,
        context: PipelineContext,
        indicator: PipelineIndicator=PipelineIndicator(),
        jump_stage: Optional[Name] = None,
        output: Optional[Any]=None
    ) -> None:
        self.context = context
        self.indicator = indicator
        self.jump_stage = jump_stage
        self.output = output
