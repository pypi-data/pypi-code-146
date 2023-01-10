from lib.consts import DocLinks
from sourcery.analysis.node_scope import NodeScopes
from sourcery.ast import AST, FunctionDef
from sourcery.conditions.metric_conditions import MetricConditions
from sourcery.config.main import SourceryConfig
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType
from sourcery.metrics import Metric
from sourcery.metrics.cognitive_complexity import CognitiveComplexityMetric
from sourcery.metrics.peak_working_memory import PeakWorkingMemoryMetric
from sourcery.metrics.simple_metrics import ExternalNodeSizeMetric


class FunctionQualityProposer(Proposer, MetricConditions):
    config: SourceryConfig
    node_scopes: NodeScopes

    def enter_functiondef(self, node: FunctionDef) -> None:
        self.propose(
            FunctionQualityProposal(
                self.ast,
                node,
                self.cognitive_complexity_metric(node),
                self.node_size_metric(node),
                self.working_memory_metric(node),
                self.quality_score_metric(node),
            )
        )

    def kind(self) -> RuleType:
        return RuleType.HOVER


class FunctionQualityProposal(Proposal):
    def __init__(
        self,
        ast: AST,
        node: FunctionDef,
        complexity: float,
        node_size: float,
        working_memory: float,
        score: float,
    ) -> None:
        self.ast = ast
        self.node = node
        self.complexity = complexity
        self.node_size = node_size
        self.working_memory = working_memory
        self.score = score

    def description(self) -> str:  # pragma: no cover
        return ""

    def explanation(self) -> str:
        quality_exp = Metric.emoji_for_value((100 - self.score) / 10, is_markdown=True)
        link = DocLinks.METRICS

        return f"""
            | [**Sourcery Code Metrics**]({link}) |  |  |  |
            | --- | --- | --- | --- |
            | Complexity | {self.complexity} | {CognitiveComplexityMetric.explanation(self.complexity, is_markdown=True)} | {CognitiveComplexityMetric.suggestion(self.complexity)} |
            | Size | {self.node_size} | {ExternalNodeSizeMetric.explanation(self.node_size, is_markdown=True)} | {ExternalNodeSizeMetric.suggestion(self.node_size)} |
            | Working memory | {self.working_memory} | {PeakWorkingMemoryMetric.explanation(self.working_memory, is_markdown=True)} | {PeakWorkingMemoryMetric.suggestion(self.working_memory)} |
            | **Quality Score** | **{self.score:.0f}%** | {quality_exp} | |
        """

    def html_explanation(self) -> str:
        quality_exp = Metric.emoji_for_value((100 - self.score) / 10, is_markdown=False)
        link = DocLinks.METRICS
        return f"""
            <b><a href="{link}">Sourcery Code Metrics</a></b>
            <table>
                <tr><td>Complexity&nbsp</td><td>{self.complexity}&nbsp</td><td>{CognitiveComplexityMetric.explanation(self.complexity, is_markdown=False)}&nbsp&nbsp</td><td>{CognitiveComplexityMetric.suggestion(self.complexity)}</td></tr>
                <tr><td>Size</td><td>{self.node_size}&nbsp</td><td>{ExternalNodeSizeMetric.explanation(self.node_size, is_markdown=False)}&nbsp&nbsp</td><td>{ExternalNodeSizeMetric.suggestion(self.node_size)}</td></tr>
                <tr><td>Working Memory</td><td>{self.working_memory}&nbsp</td><td>{PeakWorkingMemoryMetric.explanation(self.working_memory, is_markdown=False)}&nbsp&nbsp</td><td>{PeakWorkingMemoryMetric.suggestion(self.working_memory)}</td></tr>
                <tr><td><b>Quality Score</b> </td><td><b>{self.score:.0f}%</b> </td><td><b>{quality_exp}</b></td></tr>
            </table>
        """

    def execute(self) -> None:  # pragma: no cover
        pass

    def kind(self) -> RuleType:
        return RuleType.HOVER
