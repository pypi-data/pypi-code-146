import functools
import logging
import json
import datetime
import time
import os

from typing import Mapping, List, Tuple, Dict, Any

from .step_input import StepInput

from ..base import ArtifactMeta, BaseRef, TransformExecution

from .expression_evaluators.expression_evaluator import ExpressionEvaluator
from .expression_evaluators.expression_evaluator import GOOGLE_WORKFLOW_EXPRESSION_TYPE, STEP_FUNCTION_EXPRESSION_TYPE
from .expression_evaluators.google_workflow_evaluator import GoogleWorkflowExpressionEvaluator
from .expression_evaluators.step_function_evaluator import StepFunctionExpressionEvaluator


class InputConverter():
    def __init__(self, converter_input:StepInput, flow_context:Dict[str,Any]):
        self.converter_input = converter_input
        self.flow_context = flow_context


    def convert(self):
        # this is a dict with potential expressions embedded in it
        converter_input = self.converter_input.get_meta()
        converted = self._convert_expressions(converter_input)

        return StepInput.from_meta(converted)



    def _convert_expressions(self, input_entry):

        entry = input_entry if isinstance(input_entry, Dict) else input_entry.__dict__

        # check if we are dealing with an input expression
        if ("expression_type" in entry) and ("expression" in entry):

            # return the result of the evaluation
            evaluation_factory = ExpressionEvaluatorFactory.get_evaluator(expression_type = entry["expression_type"])
            evaluation_result = evaluation_factory.evaluate(entry["expression"], self.flow_context)

            if isinstance(evaluation_result, (ArtifactMeta, StepInput)):
                return evaluation_result.get_meta()
            else:
                return evaluation_result



        # now iterate over dictionary items
        for k, v in entry.items():

            if isinstance(v, str):
                pass
            elif isinstance(v, int):
                pass
            elif isinstance(v, float):
                pass
            elif isinstance(v, bool):
                pass

            elif isinstance(v, (Dict, ArtifactMeta, BaseRef, TransformExecution)):

                entry[k] = self._convert_expressions(v)


            elif isinstance(v, List):

                entry[k] = [
                  self._convert_expressions(m)
                  if isinstance(v, (Dict, ArtifactMeta, BaseRef, TransformExecution)) else m
                  for m in v
                ]


        return input_entry





class ExpressionEvaluatorFactory():

    @staticmethod
    def get_evaluator(expression_type:str = STEP_FUNCTION_EXPRESSION_TYPE) -> ExpressionEvaluator:
        if expression_type == GOOGLE_WORKFLOW_EXPRESSION_TYPE:
            return GoogleWorkflowExpressionEvaluator()

        elif expression_type == STEP_FUNCTION_EXPRESSION_TYPE:
            return StepFunctionExpressionEvaluator()


        return GoogleWorkflowExpressionEvaluator()
