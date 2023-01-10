import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from classiq.interface.analyzer.result import GraphResult

from classiq.exceptions import ClassiqAnalyzerError


def _create_heatmap_graph(result: GraphResult, num_qubits: int) -> go.Figure:
    if result is None:
        raise ClassiqAnalyzerError("heatmap failed to create`")
    return (
        px.imshow(
            pd.read_json(result.details),
            labels=dict(
                x="cycles",
                y="qubit",
                color="connectivity strength",
            ),
            color_continuous_scale="sunset",
        )
        .update_xaxes(showticklabels=False)
        .update_yaxes(tickvals=list(range(num_qubits)))
    )


def _create_gate_histogram(result: GraphResult, num_qubits: int) -> go.Figure:
    if result is None:
        raise ClassiqAnalyzerError("gate histogram failed to create`")
    return (
        px.bar(
            pd.read_json(result.details),
            labels=dict(x="Qubit ID"),
            color_discrete_map={
                "1": "rgb(201,203,192)",  # gray
                "2": "rgb(17,157,164)",  # turquoise
                "3": "rgb(215,247,91)",  # yellow
                "multiple": "rgb(244,55,100)",
            },
        )
        .update_layout(
            xaxis_title="Qubit ID",
            yaxis_title="Number of gates",
            legend_title="Filter by # qubits",
        )
        .update_yaxes(tick0=0, dtick=1)
        .update_xaxes(tickvals=list(range(num_qubits)))
    )
