
import functools
import logging
import json
import datetime
import time
import os
import base64
import random
import uuid
import hashlib

from typing import Mapping, List, Tuple, Dict, Union, Any



from .expression_evaluator import ExpressionEvaluator

# AWS Step Function Intrinsics, only relevant for local execution
class StepFunctionExpressionEvaluator(ExpressionEvaluator):

    def evaluate(self, expression:Union[str, Dict[str, str]], flow_context: Dict[str,Any]) -> Any:

        # invoke eval here, with the flow context
        step_outputs = flow_context["step_outputs"]
        step_inputs = flow_context["step_inputs"]
        step_input = flow_context["step_input"]
        flow_input = flow_context["flow_input"]



        # expression (intrinsic) functions as supported by AWS Step Functions Intrinsics
        states_object = type('obj', (), {
          'Array': lambda *args: list(args)[1:],
          'ArrayLength': len,
          'ArrayRange': lambda start, end, step: [a for a in range(start, end + step, step)],
          'ArrayPartition': lambda input_list, n: [input_list[i:i + n] for i in range(0, len(input_list), n)],
          'ArrayContains': lambda l, a: a in l,
          'ArrayGetItem': lambda l, a: l[a],
          'ArrayUnique': lambda l: list(set(l)),


          'MathAdd': lambda x, y: x + y,
          'MathRandom': lambda x, y, seed: random.randrange(x, y, 1),

          'UUID': lambda : str(uuid.uuid4()),
          'Hash': lambda input, algo: ({
                                     'MD5': lambda x: hashlib.md5(x.encode("utf-8")).hexdigest(),
                                     'SHA-1': lambda x: hashlib.sha1(x.encode("utf-8")).hexdigest(),
                                     'SHA-256': lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest(),
                                     'SHA-384': lambda x: hashlib.sha384(x.encode("utf-8")).hexdigest(),
                                     'SHA-512': lambda x: hashlib.sha512(x.encode("utf-8")).hexdigest()
                                     }[algo](input)),

          'StringSplit': lambda v, s: v.split(s),

          'Base64Encode': lambda x, pad=True: base64.b64encode(x.encode("utf-8")).decode("utf-8"),
          'Base64Decode': lambda x, pad=True: base64.b64decode(x.encode("utf-8")).decode("utf-8"),


          'JsonMerge': lambda ls, ls_to_merge: ls.update(ls_to_merge) or ls,
          'JsonToString': lambda x: json.dumps(x).encode("utf-8"),
          'StringToJson': lambda x: json.loads(x)
          })()


        try:
            # when dealing with AWS condition/choice expressions
            if isinstance(expression, Dict):
                literal_str_comps = [
                  "StringEquals",  "StringGreaterThan", "StringLessThan",
                ]

                comp_key = [k for k in filter(lambda x: x!='Variable', [a for a in expression.keys()])][0]
                comp_val = f"'{expression[comp_key]}'" if comp_key in literal_str_comps else expression[comp_key]
                expr_flattend = f"{comp_key}({expression['Variable']}, {comp_val})"

                return eval(expr_flattend, {
                  "States": states_object,

                  "StringEquals": lambda a,b: a == b,
                  "StringEqualsPath": lambda a,b: a == b,
                  "StringGreaterThan": lambda a,b: a > b,
                  "StringGreaterThanEquals": lambda a,b: a >= b,
                  "StringGreaterThanEqualsPath": lambda a,b: a >= b,
                  "StringLessThan": lambda a,b: a < b,
                  "StringLessThanEqual": lambda a,b: a <= b,
                  "StringLessThanEqualPath": lambda a,b: a <= b,

                  "NumericEquals": lambda a,b: a == b,
                  "NumericEqualsPath": lambda a,b: a == b,
                  "NumericGreaterThan": lambda a,b: a > b,
                  "NumericGreaterThanPath": lambda a,b: a > b,
                  "NumericGreaterThanEquals": lambda a,b: a >= b,
                  "NumericGreaterThanEqualsPath": lambda a,b: a >= b,
                  "NumericLessThan": lambda a,b: a < b,
                  "NumericLessThanPath": lambda a,b: a < b,
                  "NumericLessThanEquals": lambda a,b: a <= b,
                  "NumericLessThanEqualsPath": lambda a,b: a <= b,

                  "BooleanEquals": lambda a,b: a == b,
                  "BooleanEqualsPath": lambda a,b: a == b,

                  "IsNull": lambda a,b: isinstance(a, type(None)) == b,
                  "IsBoolean": lambda a,b: isinstance(a, bool) == b,
                  "IsNumeric": lambda a,b: isinstance(a, (int, float)) == b,
                  "IsString": lambda a,b: isinstance(a, str) == b
                }, {
                  "step_outputs": step_outputs,
                  "step_inputs": step_inputs,
                  "step_input": step_input,
                  "flow_input": flow_input
                })

            else:
                # when dealing with normal string expressions
                return eval(expression, {
                  "States": states_object,
                }, {
                  "step_outputs": step_outputs,
                  "step_inputs": step_inputs,
                  "step_input": step_input,
                  "flow_input": flow_input
                })


        except Exception as e:
            print(f"Error on expression evaluation of: {expression} - only AWS step function instrinsics, or choice expressions allowed")
            raise e
