
from typing import Mapping, List, Tuple, Dict, Any

GOOGLE_WORKFLOW_EXPRESSION_TYPE = "google_workflows"
STEP_FUNCTION_EXPRESSION_TYPE = "step_function"


class Expression():

    def __init__(self, expression:str, expression_type:str = GOOGLE_WORKFLOW_EXPRESSION_TYPE):
        self.expression = expression
        self.expression_type = expression_type # only google_workflow and step_function supported


    def get_meta(self):
        return {
          "expression_type": self.expression_type,
          "expression": self.expression
        }


    # equality
    def __eq__(self, other) -> bool:

        if not isinstance(other, Expression):
            return False

        return (self.expression_type, self.expression) == (other.expression_type, other.expression)




class ExpressionEvaluator():

    def evaluate(self, expression:str, flow_context: Dict[str,Any]) -> Any:
        pass
