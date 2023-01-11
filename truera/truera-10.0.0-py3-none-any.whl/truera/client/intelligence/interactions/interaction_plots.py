from __future__ import annotations

from collections import OrderedDict
import itertools
from typing import (
    Callable, Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING
)

from IPython.display import clear_output
from IPython.display import display
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import truera.client.intelligence.visualizations.colors as Colors
from truera.client.intelligence.visualizations.plots import Plots
from truera.rnn.general.aiq.clustering import FEATURE_KEY
from truera.rnn.general.aiq.clustering import PARENT_ID_KEY
from truera.rnn.general.aiq.clustering import X_KEY
from truera.rnn.general.aiq.clustering import Y_KEY

if TYPE_CHECKING:
    from truera.nlp.general.aiq.aiq import SentenceInfo


class InteractionPlots(Plots):
    """
    A Visualization Class for interaction workflows.
    """

    @staticmethod
    def gradient_landscape_graph(
        *,
        record_info: Tuple[pd.DataFrame, Sequence[str]],
        record_idx: Sequence[int],
        corrs: Dict[int, np.ndarray] = None,
        corr_idx_mapping: Dict[int, int] = None,
        init_word_idx: int = None,
        figsize: Optional[Tuple[int, int]] = (800, 600)
    ) -> go.Figure:
        """
        Visualize the gradient paths by feature.

        Args:
            record_info (tuple[pd.DataFrame, list[str]]): Supplementary information about the record. 
                The dataframe will contain gradient path info. The list[str] are the corresponding feature names
            record_idx (int): The record to show gradient paths for.
            corrs (Dict[int, np.ndarray]): correlation matrix. If provided, used to determine which tokens to display
            corr_idx_mapping (Dict[int, np.ndarray]): correlation matrix. If provided, used to determine which tokens to display
            init_word_idx (Dict[int, np.ndarray]): Index of selected token. If provided, will display token at this index and most correlated tokens. Expects to be supplied with corrs and corr_idx_maps 
            figsize: Size for plot in pixels. Defaults to (800, 400).
        Returns:
            go.Figure: the visualization
        """
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            yaxis=dict(fixedrange=True),
            xaxis=dict(fixedrange=True),
            width=figsize[0],
            height=figsize[1],
            showlegend=False,
            uniformtext_minsize=20,
            title={
                "text": "Gradient Landscape from Baseline",
                "x": 0.5,
                "xanchor": "center"
            }
        )

        landscape_df, tokens = record_info[record_idx]
        n_rows = min(5, len(landscape_df.columns))

        if corrs is not None:
            # Maps from correlation_matrix_idx to token Idx
            reverse_corr_idx_map = {
                corr_idx_mapping[i]: i for i in range(len(corr_idx_mapping))
            }

            correlations = corrs[reverse_corr_idx_map[init_word_idx]]
            plot_idxs = [
                corr_idx_mapping[i]
                for i in correlations.argsort()[-n_rows:][::-1]
            ]
            # Sanity check: selected token should be displayed
            assert init_word_idx in plot_idxs
        else:
            plot_idxs = list(range(n_rows))

        display_to_col = OrderedDict()
        for idx in plot_idxs:
            if init_word_idx and idx == init_word_idx:
                disp_key = f"<b>{tokens[idx]}</b>"
            else:
                disp_key = tokens[idx]
            if tokens[idx] in landscape_df.columns:
                col_name = tokens[idx]
            else:
                col_name = f"{idx}: {tokens[idx]}"
            display_to_col[disp_key] = col_name

        fig = go.FigureWidget(
            make_subplots(
                rows=n_rows,
                cols=1,
                subplot_titles=list(display_to_col.keys()),
                x_title="Integrated Gradients Resolution",
                y_title="Gradient Magnitude",
                figure=go.Figure(layout=layout),
                shared_xaxes=True,
                shared_yaxes=True
            )
        )

        for i, (feature_name, col_name) in enumerate(display_to_col.items()):
            landscape_scatter = go.Scatter(
                y=landscape_df[col_name], mode="lines", name=feature_name
            )
            fig.add_trace(landscape_scatter, row=i + 1, col=1)

        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_annotations(
            align='right',
            xanchor='left',
            x=0,
            yanchor='middle',
            yshift=0,
            selector=lambda x: x['text'] in display_to_col
        )
        return fig

    @staticmethod
    def feature_interaction_dendrogram(
        record_info: Tuple[pd.DataFrame, Sequence[str]],
        record_idx: Sequence[int],
        figsize: Optional[Tuple[int, int]] = (800, 800)
    ) -> go.Figure:
        """
        Visualize the feature interaction via dendrogram of similar features

        Args:
            record_info (tuple[pd.DataFrame, list[str]]): Supplementary information about the record. 
                The dataframe will contain gradient path info. The list[str] are the corresponding feature names
            record_idx (int): The record to show gradient paths for.
            figsize: Size for plot in pixels. Defaults to (800, 800).
        Returns:
            go.Figure: the visualization
        """
        landscape_df, _ = record_info[record_idx]
        f_df = landscape_df[landscape_df[FEATURE_KEY].notnull()]
        has_parent_df = landscape_df[landscape_df[PARENT_ID_KEY].notnull()]

        hide_axis = dict(
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        )
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            showlegend=False,
            width=figsize[0],
            height=figsize[1],
            uniformtext_minsize=20,
            xaxis=hide_axis,
            yaxis=hide_axis,
            title={
                "text": f"Interaction Dendrogram",
                "x": 0.5,
                "xanchor": "center"
            }
        )
        fig = go.FigureWidget(layout=layout)

        edge_xs = has_parent_df.apply(
            lambda row: [landscape_df.loc[int(row.parent_id)].x, row.x, None],
            axis=1
        )
        edge_ys = has_parent_df.apply(
            lambda row: [landscape_df.loc[int(row.parent_id)].y, row.y, None],
            axis=1
        )
        edge_scatter = go.Scatter(
            x=list(itertools.chain.from_iterable(edge_xs)),
            y=list(itertools.chain.from_iterable(edge_ys)),
            mode="lines",
            line=dict(color="rgba(0, 0, 0)", width=1),
            hoverinfo="none",
            opacity=0.8
        )
        fig.add_trace(edge_scatter)

        highlight_edge_scatter = go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(color="rgba(0, 0, 0)", width=2),
            hoverinfo="none"
        )
        fig.add_trace(highlight_edge_scatter)

        highlight_point_scatter = go.Scatter(
            x=[],
            y=[],
            mode="markers",
            marker=dict(size=10, color="red", line=dict(width=0)),
            hoverinfo="none"
        )
        fig.add_trace(highlight_point_scatter)

        text_scatter = go.Scatter(
            mode="text",
            textposition="middle center",
            x=f_df[X_KEY],
            y=f_df[Y_KEY],
            text=f_df[FEATURE_KEY]
        )
        fig.add_trace(text_scatter)

        click_scatter = go.Scatter(
            x=landscape_df[X_KEY],
            y=landscape_df[Y_KEY],
            mode="markers",
            opacity=0.0
        )
        fig.add_trace(click_scatter)

        root_scatter = go.Scatter(
            x=[landscape_df.loc[0]["x"]],
            y=[landscape_df.loc[0]["y"]],
            mode="markers",
            marker=dict(symbol="star", size=30, line=dict(width=0)),
            opacity=0.8
        )
        fig.add_trace(root_scatter)
        return fig

    @staticmethod
    def token_interaction_bar(
        *,
        corrs: Dict[int, np.ndarray],
        corr_idx_mapping: List[int],
        tokens: List[int],
        ngram_idxs: List[int] = None,
        token_idx: int = 0,
        min_yaxis: float = 0.0,
        update_token_callback: Callable = None
    ) -> go.Figure:
        """
        Creates a correlation bar graph from a selected token to the other tokens.
        
        Args:
            sentence_info: contains a DataFrame of the spectral clustered tree and the sentence itself
            corrs: the correlation matrix of grad paths. 
            corr_idx_mapping: mappings from the correlation matrix ids to the token ids. 
            tokens: List of tokens in the sentence. Filtered down according to corr_idx_mapping
            ngram_idxs: indexes of the other tokens to highlight 
            token_idx: the index of the token in tokens
            min_yaxis: base value in the y-axis
            update_token_callback: Method to call when bar is clicked
        Returns:
            go.Figure: the visualization
        """
        corr_tokens = [tokens[i] for i in corr_idx_mapping]
        # maps from orig_idx to corr_matrix_row_idx
        reverse_corr_idx_map = {
            corr_idx_mapping[i]: i for i in range(len(corr_idx_mapping))
        }

        corr_token_idx = reverse_corr_idx_map[token_idx]
        bolded_tokens = corr_tokens[:]
        num_tokens = len(corr_tokens)
        bolded_tokens[corr_token_idx] = f"<b>{corr_tokens[corr_token_idx]}</b>"

        layout = Plots.truera_layout(
            xaxis=dict(
                title="Tokens",
                tickmode="array",
                tickvals=np.arange(num_tokens),
                ticktext=bolded_tokens,
                tickangle=-45,
                tickfont=dict(size=18 - int(num_tokens / 10))
            ),
            yaxis=dict(
                title=f"Correlation with \"{corr_tokens[corr_token_idx]}\"",
                range=[min_yaxis, 1.0]
            ),
            showlegend=False,
        )

        fig = go.FigureWidget(layout=layout)

        # Reconfigure the correlation matrix to be ordered lowest token id to highest token id
        if not ngram_idxs:
            colors = Colors.TRUERA_GREEN_30
        else:
            ngram_idxs = [reverse_corr_idx_map[idx] for idx in ngram_idxs]
            colors = [
                Colors.TRUERA_GREEN
                if i in ngram_idxs else Colors.TRUERA_GREEN_90
                for i in range(num_tokens)
            ]

        bar_chart = go.Bar(
            x=np.arange(num_tokens),
            y=corrs[corr_token_idx],
            marker=dict(color=colors)
        )

        def update_point(trace, points, selector):
            if (len(points.point_inds) > 0):
                new_idx = points.point_inds[0]
                correlation_idx_map = list(zip(corrs[new_idx], corr_tokens))
                correlation_idx_map.sort(key=lambda x: x[0])

                bar_chart.y = [e[0] for e in correlation_idx_map]
                fig.layout.yaxis.title = f"Correlation with \"{corr_tokens[new_idx]}\""

                bolded_tokens = [
                    f"<b>{corr_tokens[e[1]]}</b>"
                    if e[1] == new_idx else corr_tokens[e[1]]
                    for e in correlation_idx_map
                ]
                bolded_tokens[new_idx] = f"<b>{corr_tokens[new_idx]}</b>"
                fig.layout.xaxis.ticktext = bolded_tokens
                if update_token_callback:
                    update_token_callback(new_idx, corr_tokens[new_idx])

        fig.add_trace(bar_chart)
        bar_chart.on_click(update_point)
        return fig
