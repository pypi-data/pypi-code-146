from typing import Tuple

from sourcery.analysis.clone_detection import Clones
from sourcery.analysis.control_flow_next_node import ControlFlowNextNode
from sourcery.analysis.near_clone_detection import NearClones, PartialBlockNearClones
from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.analysis.node_paths import PathNodes
from sourcery.analysis.node_statements import NodeStatements
from sourcery.analysis.node_var_ranges import StatementMemoryVars
from sourcery.analysis.nodes_in_loops import NodesInLoops
from sourcery.analysis.variable_usage import VariableUsage, VariableUsageAnalyzer
from sourcery.ast import AST, Block, Module
from sourcery.clones.extract_checker import ExtractChecker
from sourcery.clones.extract_method import MethodExtractor
from sourcery.engine.proposal import Proposer
from sourcery.rules.private.refactorings.descriptions import EXTRACT_METHOD_CLASS
from sourcery.rules.private.refactorings.visitor.extract_function_proposals import (
    BaseExtractMethodProposal,
    suitable_function,
)


class ClassExtractMethodProposer(Proposer):
    """Extract functions at class level."""

    clones: Clones
    near_clones: NearClones
    partial_clones: PartialBlockNearClones

    suitable_clones: Tuple[Tuple[Block, ...], ...]

    node_statements: NodeStatements
    variable_usages: VariableUsage
    next_nodes: ControlFlowNextNode
    nodes_in_loops: NodesInLoops
    node_paths: PathNodes

    statement_vars: StatementMemoryVars

    node_dependencies: NodeDependencies
    current_function_size: int
    extract_checker: ExtractChecker

    def reset(self, ast: AST):
        super().reset(ast)

        for clones in self.partial_clones:
            for clone in clones:
                usages = clone.run(VariableUsageAnalyzer())
                var_usages = usages[clone[0].parent]
                self.variable_usages[clone] = var_usages

        self.extract_checker = ExtractChecker(
            self.node_dependencies,
            self.variable_usages,
            self.nodes_in_loops,
            self.statement_vars,
            self.next_nodes,
        )

        self.suitable_clones = self.extract_checker.suitable_clones(self.partial_clones)

    def leave_module(self, _node: Module):
        if not self.suitable_clones:
            return
        clone_to_use = max(self.suitable_clones, key=lambda x: sum(len(y) for y in x))

        # Check all of the clones belong to normal functions
        parent_nodes = []
        for clone in clone_to_use:
            parent = clone[0].scope()
            if not suitable_function(parent):
                return
            parent_nodes.append(parent)

        extractor = MethodExtractor(self.extract_checker)
        if extracted_method := extractor.extract_method(parent_nodes[-1], clone_to_use):
            self.propose(
                ClassExtractMethodProposal(self.ast, parent_nodes[-1], extracted_method)
            )


class ClassExtractMethodProposal(BaseExtractMethodProposal):
    def description(self):
        return EXTRACT_METHOD_CLASS
