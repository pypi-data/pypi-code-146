import functools
import logging
import json
import datetime
import time
import os
import base64

from typing import Mapping, List, Tuple, Dict, Any



from .expression_evaluator import ExpressionEvaluator

# Google workflow Intrinsic functions, only relevant for local execution
class GoogleWorkflowExpressionEvaluator(ExpressionEvaluator):


    def evaluate(self, expression:str, flow_context: Dict[str,Any]) -> Any:

        # invoke eval here, with the flow context
        step_outputs = flow_context["step_outputs"]
        step_inputs = flow_context["step_inputs"]
        step_input = flow_context["step_input"]
        flow_input = flow_context["flow_input"]


        # expression functions as supported by google workflow
        sys_object = type('obj', (), {
          'get_env': os.getenv,
          'now': time.time_ns
          })()

        math_object = type('obj', (), {
          'abs' : abs,
          'max': max,
          'min': min
          })()

        # add json
        json_object = type('obj', (), {
          'encode': lambda x: json.dumps(x).encode("utf-8"),
          'decode': lambda x: json.loads(x)
          })()

        # add base64
        base64_object = type('obj', (), {
          'encode': lambda x, pad=True: base64.b64encode(x).decode("utf-8"),
          'decode': lambda x, pad=True: base64.b64decode(x.encode("utf-8"))
          })()


        # add to copy of list/append
        list_object = type('obj', (), {
          'concat': lambda ls, el: ls + [el],
          'prepend': lambda ls, el: [el] + ls
          })()


        try:

            return eval(expression, {
              "sys": sys_object,
              "math": math_object,
              "json": json_object,
              "base64": base64_object,
              "if": lambda c, x, y: x if c else y,
              "default": lambda x, y: x if x else y,
              "keys": lambda m: m.keys(),
              "len": len,
              "list": list_object,
            }, {
              "step_outputs": step_outputs,
              "step_inputs": step_inputs,
              "step_input": step_input,
              "flow_input": flow_input
            })

        except Exception as e:
            print(f"Error on expression evaluation of: \"{expression}\" - only Google Workflow instrinsics allowed")
            raise e
