import json
import logging


from typing import Mapping, List, Tuple, Dict, Any
from ..flows import BaseGraph


class InternalJSONFlowCompiler():

    def __init__(self, flow: BaseGraph):

        self.flow = flow


    def compile(self) -> str:
        return json.dumps(self.flow._graph_steps)
