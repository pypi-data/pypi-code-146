from sourcery.analysis.node_scope import NodeScope, NodeScopes
from sourcery.ast import AST, FunctionDef
from sourcery.code.code_location import qualified_function_name
from sourcery.conditions.metric_conditions import MetricConditions
from sourcery.config.main import SourceryConfig
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType


class LowCodeQualityProposer(Proposer, MetricConditions):
    config: SourceryConfig
    node_scopes: NodeScopes

    def enter_functiondef(self, node: FunctionDef) -> None:
        score = self.quality_score_metric(node)
        if score < self.config.metrics.quality_threshold:
            self.propose(
                LowCodeQualityProposal(
                    self.ast,
                    node,
                    score,
                    self.config.metrics.quality_threshold,
                    self.node_scopes[node.body],
                )
            )

    def kind(self) -> RuleType:
        return RuleType.COMMENT


class LowCodeQualityProposal(Proposal):
    def __init__(
        self,
        ast: AST,
        node: FunctionDef,
        score: float,
        quality_threshold: float,
        scopes: NodeScope,
    ) -> None:
        self.ast = ast
        self.node = node
        self.score = score
        self.quality_threshold = quality_threshold
        self.scopes = scopes

    def description(self):
        # pylint: disable=line-too-long
        return f"Low code quality found in {qualified_function_name(self.scopes)} - {self.score:.0f}%"

    def explanation(self):
        return f"""
            The quality score for this function is below the quality threshold of {self.quality_threshold:.0f}%.
            This score is a combination of the method length, cognitive complexity and working memory.

            How can you solve this?

            It might be worth refactoring this function to make it shorter and more readable.

            - Reduce the function length by extracting pieces of functionality out into
              their own functions. This is the most important thing you can do - ideally a
              function should be less than 10 lines.
            - Reduce nesting, perhaps by introducing guard clauses to return early.
            - Ensure that variables are tightly scoped, so that code using related concepts
              sits together within the function rather than being scattered.
        """

    def execute(self) -> None:  # pragma: no cover
        pass

    def kind(self) -> RuleType:
        return RuleType.COMMENT
