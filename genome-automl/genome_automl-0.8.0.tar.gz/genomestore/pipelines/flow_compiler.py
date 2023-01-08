import json
import logging


from typing import Mapping, List, Tuple, Dict, Any

from .flows import BaseGraph

from .flow_compilers.internal_json_compiler import InternalJSONFlowCompiler
from .flow_compilers.genome_compiler import GenomeFlowCompiler

class FlowCompilerFactory():

    @staticmethod
    def get_compiler(flow: BaseGraph, target="json"):

        """
        compiles into some fancy graph execution engine with high availability and scale
        """

        if target == "json":
            # raw json internal representation
            return InternalJSONFlowCompiler(flow)

        elif target == "genome":
            # genome sequencer format
            return GenomeFlowCompiler(flow)
        else:
            #dunno anything else
            pass
