from typing import (
    Any, Callable, Dict, Iterable, List, Optional, Sequence, Union
)

from IPython.display import clear_output
from IPython.display import display
from IPython.display import HTML as html_print
from ipywidgets import VBox
from ipywidgets import widgets
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from truera.client.intelligence.interactions.interaction_plots import \
    InteractionPlots
from truera.client.intelligence.visualizations.plots import Plots
from truera.client.nn.wrappers import nlp
from truera.nlp.fairness.output_metrics import disparity_wrapper
from truera.nlp.fairness.output_metrics import OutputMetrics
from truera.nlp.fairness.utils import get_segment_disadvantage_rankings
from truera.nlp.fairness.utils import visualize_accuracy
from truera.nlp.fairness.utils import visualize_confusion_matrix
from truera.nlp.fairness.utils import visualize_confusion_matrix_rates
from truera.nlp.fairness.utils import visualize_f1_score
from truera.nlp.general.aiq.aiq import NlpAIQ
from truera.nlp.general.aiq.components import ngram_correlation_table_widget
from truera.nlp.general.aiq.filtering_utils import get_filter_from_group_name
from truera.nlp.general.aiq.nlp_coloring import attributions_to_rgb
from truera.nlp.general.aiq.nlp_coloring import generate_rgb_str
from truera.nlp.general.aiq.nlp_coloring import MAX_INTENSITY
from truera.nlp.general.aiq.nlp_coloring import rgb_str
from truera.nlp.general.model_runner_proxy.nlp_counterfactuals import \
    merge_lists_with_swaps
from truera.nlp.general.utils.configs import \
    get_class_idx_from_qoi_widget_options
from truera.nlp.general.utils.configs import \
    get_influence_from_qoi_widget_options
from truera.nlp.general.utils.configs import QoIType
from truera.nlp.general.utils.configs import TokenType
from truera.rnn.general.container.artifacts import ArtifactsContainer
import truera.rnn.general.utils.colors as Colors


class NLPPlots(InteractionPlots):

    @staticmethod
    def _token_influence_table(
        tokens_info: pd.DataFrame, *, class_names: List[str],
        class_colors: List[str]
    ) -> go.Scatter:
        """ Generates one class' scatter to be a part of the global scatter plot of tokens in a dataset.

        Args:
            tokens_info (pd.DataFrame): Metadata about tokens
            mean_key (str): The name of the column in token_info which corresponds to the mean
            marker_color (str): the color of the class
            std_key (Optional[str], optional): The name of the column in token_info which corresponds to the mean
            name (Optional[str], optional): The name of this scatter group

        Returns:
            go.Scatter: The scatter plot
        """
        color_map = dict(zip(class_names, class_colors))
        color_map['comparative'] = 'white'
        infl_color = attributions_to_rgb(tokens_info.infl_mean)
        table = go.Table(
            header=dict(
                values=[
                    'tokens', 'class', 'occurrences', 'infl mean',
                    'infl std dev'
                ],
                align='center'
            ),
            cells=dict(
                values=[
                    tokens_info.tokens, tokens_info.class_id,
                    tokens_info.occurrences,
                    tokens_info.infl_mean.round(3),
                    tokens_info.infl_std.round(3)
                ],
                fill_color=[
                    'white',
                    tokens_info.class_id.map(color_map), 'white', infl_color,
                    infl_color
                ],
                align='center',
                font=dict(size=11)
            )
        )
        return table

    @staticmethod
    def _token_influence_scatter(
        tokens_info: pd.DataFrame,
        *,
        marker_color: str,
        key: str,
        std_key: Optional[str] = None,
        name: Optional[str] = None
    ) -> go.Scatter:
        """ Generates one class' scatter to be a part of the global scatter plot of tokens in a dataset.

        Args:
            tokens_info (pd.DataFrame): Metadata about tokens
            key (str): The name of the column in token_info which corresponds to plotted value
            marker_color (str): the color of the class
            std_key (Optional[str], optional): The name of the column in token_info which corresponds to the mean
            name (Optional[str], optional): The name of this scatter group

        Returns:
            go.Scatter: The scatter plot
        """
        error_x = dict(
            type='data',  # value of error bar given in data coordinates
            array=tokens_info[std_key].replace(to_replace=0, value=np.nan),
            thickness=0.5,
            width=2,
            visible=True
        ) if std_key is not None else None

        std_hovertemplate = ' ± %{error_x.array:.2}' if std_key is not None else ''
        scatter = go.Scatter(
            x=tokens_info[key],
            y=tokens_info['occurrences'],
            mode='markers',
            name=name,
            text=tokens_info['tokens'],
            marker=dict(
                line=dict(width=2, color='DarkSlateGrey'),
                size=[8] * len(tokens_info),
                opacity=[.6] * len(tokens_info),
                color=marker_color
            ),
            error_x=error_x,
            hovertemplate='<b>%{text}</b><br>' + 'Influence: %{x:.2}' +
            std_hovertemplate + '<br>' + 'Occurrences: %{y}<br>'
        )
        return scatter

    @staticmethod
    def token_influence_plot(
        num_classes: int,
        influence_type: str,
        plot_type: str,
        group: str,
        xaxis: str,
        influence_range: list,
        occurrence_range: float,
        error_driver_group_dict: Dict[str, pd.DataFrame],
        on_token_click: Optional[Iterable[Callable[[str], None]]] = None
    ):
        """ Returns a scatter plot of influence vs frequency for every token.

        Args:
            num_classes (int): The total number of output classes.
            influence_type (str): The type of influences to plot. Can be classwise or comparative (the class minus all other classes)
            group (str): A grouping filter on the data. Typically error groups. Defaults to 'all'
            xaxis (str): the metric on the x-axis. Can be 'mean' or 'stdev'
            influence_range (Iterable[float]): A filter on min and max influences to limit data.
            min_frequency (float): A filter on min frequency to limit data.
            error_driver_group_dict (Dict[Str, pd.DataFrame]): The dictionary from group to a pd.DataFrame of metadata about tokens filtered on that group.
            on_token_click (Iterable[Callable[[str], None]], optional): A Callback - called with token string value when a token point is clicked. Defaults to [].
        """
        if on_token_click is None:
            on_token_click = []

        layout = Plots.truera_layout(
            title={
                'text':
                    f'Global {QoIType.CLASS_WISE.get_human_readable()} Token Influence',
                'x':
                    0.5,
                'xanchor':
                    'center'
            }
        )

        fig = go.FigureWidget(layout=layout)

        tokens_info = error_driver_group_dict[group]
        tokens_info = tokens_info[tokens_info.occurrences >= occurrence_range[0]
                                 ]
        tokens_info = tokens_info[tokens_info.occurrences <= occurrence_range[1]
                                 ]

        def update_point(
            trace, points, selector, on_token_click=on_token_click
        ):
            s = [10] * len(trace.marker.size)
            o = [.6] * len(trace.marker.opacity)
            for i in points.point_inds:
                s[i] = 15
                o[i] = 1

            with fig.batch_update():
                trace.marker.size = s
                trace.marker.opacity = o

            if len(points.point_inds) > 0:
                for token_click_callback in on_token_click:
                    token_click_callback(trace.text[points.point_inds[0]])

        class_colors = QoIType.CLASS_WISE.get_class_colors(num_classes)
        if influence_type == 'classes':
            class_names = QoIType.CLASS_WISE.get_qoi_type_widget_options(
                num_classes
            )
        else:
            class_names = ['comparative']

        if plot_type == "Table View":
            mean_df = tokens_info.melt(
                id_vars=['tokens', 'occurrences', 'frequencies'],
                var_name="class_id",
                value_vars=[
                    f"influences_{class_name}_mean"
                    for class_name in class_names
                ] + ['influences_comparative_mean']
            )
            std_df = tokens_info.melt(
                id_vars='tokens',
                var_name="class_id",
                value_vars=[
                    f"influences_{class_name}_std" for class_name in class_names
                ] + ['influences_comparative_std']
            )

            mean_df['class_id'] = mean_df['class_id'].str.split("_").str[
                1:-1].str.join("_")
            std_df['class_id'] = std_df['class_id'].str.split("_").str[
                1:-1].str.join("_")
            tokens_info = mean_df.merge(
                std_df, on=('tokens', 'class_id'), suffixes=("_mean", "_std")
            )
            tokens_info = tokens_info.rename(
                columns={
                    "value_mean": "infl_mean",
                    "value_std": "infl_std"
                }
            )
            if xaxis == 'mean':
                tokens_info = tokens_info.sort_values(
                    by=['infl_mean', 'occurrences'],
                    ascending=False,
                    key=lambda x: abs(x)
                )
            elif xaxis == 'stdev':
                tokens_info = tokens_info.sort_values(
                    by=['infl_std', 'occurrences'],
                    ascending=False,
                    key=lambda x: abs(x)
                )

            if influence_type == "classes":
                tokens_info = tokens_info[
                    tokens_info['class_id'] != 'comparative']
            else:
                tokens_info = tokens_info[tokens_info['class_id'] ==
                                          'comparative']
            table = NLPPlots._token_influence_table(
                tokens_info, class_names=class_names, class_colors=class_colors
            )
            fig.add_trace(table)
        else:
            fig.update_layout(height=150 * len(class_names))
            fig = make_subplots(
                rows=len(class_names),
                cols=1,
                shared_xaxes=True,
                figure=fig,
                subplot_titles=class_names,
                x_title='{} Influence'.format(xaxis.title()),
                y_title='Sentence Occurrences'
            )
            total_graph_height = 100
            for class_idx, class_name in enumerate(class_names):
                if xaxis == 'mean':
                    key, std_key = f'influences_{class_name}_mean', f'influences_{class_name}_std'
                elif xaxis == 'stdev':
                    key, std_key = f'influences_{class_name}_std', None
                tokens_info = tokens_info[
                    (np.abs(tokens_info[f'influences_{class_name}_mean']) > 0) &
                    (
                        np.abs(tokens_info[f'influences_{class_name}_mean']) >=
                        influence_range[0]
                    ) & (
                        np.abs(tokens_info[f'influences_{class_name}_mean']) <=
                        influence_range[1]
                    )]
                scatter = NLPPlots._token_influence_scatter(
                    tokens_info,
                    name=class_names[class_idx],
                    marker_color=class_colors[class_idx],
                    key=key,
                    std_key=std_key,
                )
                occurrence_range = max(scatter['y'], default=0
                                      ) - min(scatter['y'], default=0) + 1
                graph_height = min(100 * occurrence_range, 1000)
                total_graph_height += graph_height
                fig.add_trace(scatter, row=class_idx + 1, col=1)
                fig.data[-1].on_click(update_point)

            fig.update_layout(height=total_graph_height)
        display(fig)

    @staticmethod
    def _token_influence_histogram(
        num_classes: int,
        token_info: pd.Series,
        class_colors: Iterable[str] = [Colors.TRUERA_GREEN],
        class_names: Optional[Iterable[str]] = None,
        on_bin_change: Optional[Iterable[Callable[[float, float],
                                                  None]]] = None,
        on_bin_click: Optional[Iterable[Callable[[float, float], None]]] = None
    ) -> go.FigureWidget:
        """  Returns a histogram of the influences of a specific token.

        Args:
            num_classes (int): The number of classes.
            token_info (pd.Series): Metadata about a single token
            class_colors (Iterable[str], optional): Colors of the classes. Defaults to [Colors.TRUERA_GREEN].
            class_names (Optional[Iterable[str]], optional): Names of the classes. Defaults to None.
            Callbacks:
                on_bin_change (Optional[Iterable[Callable[[float, float], None]]], optional): called with min/max values of the new distribution when histogram refreshes
                on_bin_click (Optional[Iterable[Callable[[float, float], None]]], optional): called with min/max values of a bin when a bin is clicked

        Returns:
            go.FigureWidget: The influence histogram figure of a token.
        """
        if on_bin_change is None:
            on_bin_change = []
        if on_bin_click is None:
            on_bin_click = []

        num_influence_class_dimension = QoIType.CLASS_WISE.get_influence_class_dimension(
            num_classes
        )

        layout = Plots.truera_layout(barmode='overlay')
        fig = go.FigureWidget(layout=layout)
        fig.update_layout(bargap=0.01)
        fig.update_layout(height=num_influence_class_dimension * 150, width=500)
        hist_data = [
            token_info[f'influences_{class_name}'] for class_name in
            QoIType.CLASS_WISE.get_qoi_type_widget_options(num_classes)
        ]
        hist_data_flat = np.concatenate(hist_data)

        bin_edges = np.histogram_bin_edges(hist_data_flat, bins='auto')

        one_record_per_class = False
        if len(hist_data_flat) == len(hist_data):  # if 1 record per class
            one_record_per_class = True
            range_end = max(abs(bin_edges[0]), abs(bin_edges[-1])) * 1.5
            fig.update_xaxes(range=(-range_end, range_end))
        bin_size = bin_edges[1] - bin_edges[0]
        hist_start = bin_edges[0]
        hist_end = bin_edges[
            -1
        ] + 0.01 * bin_size  # make it slightly larger to be inclusive of largest influence
        bin_size = (hist_end - hist_start) / len(
            bin_edges - 1
        )  # resize the bins to match the extended size.
        xbins = dict(start=hist_start, end=hist_end, size=bin_size)

        for bin_change_callback in on_bin_change:
            bin_change_callback(bin_edges[0], bin_edges[-1])

        fig = make_subplots(
            rows=len(class_names),
            cols=1,
            shared_xaxes='all',
            shared_yaxes='all',
            figure=fig,
            subplot_titles=class_names,
            x_title=f'\'{token_info.tokens}\' Influence',
            y_title='Token Occurrences',
        )
        for class_idx in range(num_influence_class_dimension):

            name = class_names[class_idx] if class_names is not None else None

            if one_record_per_class:
                # This is a plotly hack for 1 record histograms.
                # When provided with 1 value each,
                # the render makes all class bin [start,end,sizes] the same for each class
                # To get around this, we add an invisible histogram with all the data.
                # That way plotly has to bin them correctly.
                hist_hack = go.Histogram(
                    x=hist_data_flat,
                    customdata=(class_idx,),
                    marker_color=class_colors[class_idx],
                    name=name,
                    opacity=0.0,
                    autobinx=False,
                    xbins=xbins,
                    hoverinfo='none',
                    showlegend=False
                )
                fig.add_trace(hist_hack, row=class_idx + 1, col=1)

            hist = go.Histogram(
                x=hist_data[class_idx],
                customdata=(class_idx,),
                marker_color=class_colors[class_idx],
                name=name,
                opacity=0.5,
                autobinx=False,
                xbins=xbins,
            )
            fig.add_trace(hist, row=class_idx + 1, col=1)
        if len(on_bin_click) > 0:

            def update_point(
                trace, points, selector, on_bin_click=on_bin_click
            ):
                if (len(points.xs) <= 0):
                    return
                start, step = trace.xbins.start, trace.xbins.size
                bin_start = int((points.xs[0] - start) / step) * step + start
                for bin_click_callback in on_bin_click:
                    bin_click_callback(
                        bin_start,
                        bin_start + step,
                        class_idx=trace.customdata[0]
                    )

            for fig_data in fig.data:
                fig_data.on_click(update_point)
        return fig

    # TODO - Merge this function with _token_influence_histogram
    # Refer: https://truera.atlassian.net/browse/MLNN-130
    @staticmethod
    def _token_influence_histogram_segments(
        highlight_token,
        num_segments: int,
        hist_data: pd.Series,
        qoi_type: QoIType,
        class_colors: Iterable[str] = [Colors.TRUERA_GREEN],
        class_names: Optional[Iterable[str]] = None,
        on_bin_change: Optional[Iterable[Callable[[float, float],
                                                  None]]] = None,
        on_bin_click: Optional[Iterable[Callable[[float, float], None]]] = None
    ) -> go.FigureWidget:
        '''
           Returns a histogram of the influences of a specific token.
           Callbacks:
               on_bin_change - called with min/max values of the new distribution when histogram refreshes
               on_bin_click - called with min/max values of a bin when a bin is clicked
       '''
        if on_bin_change is None:
            on_bin_change = []
        if on_bin_click is None:
            on_bin_click = []
        num_influence_class_dimension = qoi_type.get_influence_class_dimension(
            num_segments
        )
        layout = Plots.truera_layout(
            barmode='overlay',
            xaxis=dict(title=f'\'{highlight_token}\' Influence'),
            yaxis=dict(title='Sentence Occurences'),
            height=300 * len(num_influence_class_dimension)
        )
        fig = go.FigureWidget(layout=layout)
        bin_edges = np.histogram_bin_edges(
            np.concatenate(hist_data), bins='auto'
        )
        xbins = dict(
            start=bin_edges[0],
            end=bin_edges[-1],
            size=bin_edges[1] - bin_edges[0]
        )
        for bin_change_callback in on_bin_change:
            bin_change_callback(bin_edges[0], bin_edges[-1])

        for class_idx in range(num_influence_class_dimension):
            name = class_names[class_idx] if class_names is not None else None
            hist = go.Histogram(
                x=hist_data[class_idx],
                customdata=(class_idx,),
                marker_color=class_colors[class_idx],
                name=name,
                opacity=0.5,
                autobinx=False,
                xbins=xbins
            )
            fig.add_trace(hist)
        if len(on_bin_click) > 0:

            def update_point(
                trace,
                points,
                selector,
                qoi_type=qoi_type,
                on_bin_click=on_bin_click
            ):
                if (len(points.xs) <= 0):
                    return
                start, step = trace.xbins.start, trace.xbins.size
                bin_start = int((points.xs[0] - start) / step) * step + start
                for bin_click_callback in on_bin_click:
                    if (qoi_type == QoIType.CLASS_WISE):
                        bin_click_callback(
                            bin_start,
                            bin_start + step,
                            class_idx=trace.customdata[0]
                        )
                    else:
                        bin_click_callback(bin_start, bin_start + step)

            for fig_data in fig.data:
                fig_data.on_click(update_point)
        return fig

    @staticmethod
    def token_influence_histogram_segments(
        highlight_token: str,
        class_id,
        segment_1,
        segment_2,
        num_segments: int,
        influences_dict: dict,
        qoi_type: QoIType,
        empty_message: Optional[str] = None,
        **kwargs
    ):
        """A histogram of influences values. The y axis is the number of occurrences, the x axis is the influence. 
        Creates a colored histogram per segment.
        Args:
            highlight_token (str): The specific token to highlight in a sentence.
            class_id (int): Class ID for which the influence values are extracted.
            segment_1 (str): Segment One
            segment_2 (str): Segment Two
            num_segments (int): The total number of output classes (in our case, no of segments).
            influences_dict (Dict): Precomputed influences dict which has the class id, token and segment name as the keys and 
            influences as values.
            qoi_type (QoIType): The QoI type of the explanations. Can be class or max class.
            empty_message (Optional[str], optional): The message to print if there are no examples. Defaults to None.
        """
        dist1 = influences_dict[class_id, segment_1][highlight_token]
        dist2 = influences_dict[class_id, segment_2][highlight_token]
        class_colors = qoi_type.get_class_colors(num_segments)
        class_names = [segment_1, segment_2]
        highlight_token_info_seg_one = pd.Series(dist1)
        highlight_token_info_seg_two = pd.Series(dist2)
        hist_data = [highlight_token_info_seg_one, highlight_token_info_seg_two]

        fig = NLPPlots._token_influence_histogram_segments(
            highlight_token,
            num_segments,
            hist_data,
            qoi_type,
            class_colors=class_colors,
            class_names=class_names,
            **kwargs
        )
        display(fig)

    @staticmethod
    def token_influence_histogram(
        highlight_token: str,
        num_classes: int,
        group: str,
        error_driver_group_dict: dict,
        empty_message: Optional[str] = None,
        **kwargs
    ):
        """A histogram of influences values. The y axis is the number of occurrences, the x axis is the influence. 
        Creates a colored histogram per class QoI.

        Args:
            highlight_token (str): The specific token to highlight in a sentence.
            num_classes (int): The total number of output classes.
            group (str): A grouping filter on the data. Typically error groups. Defaults to 'all'
            error_driver_group_dict (dict): The dictionary from group to record id.
            empty_message (Optional[str], optional): The message to print if there are no examples. Defaults to None.
        """
        token_info = error_driver_group_dict[group]
        highlight_token_info = token_info.loc[token_info.tokens ==
                                              highlight_token]
        if len(highlight_token_info) <= 0:
            if empty_message is not None:
                print(empty_message)
            return
        highlight_token_info = highlight_token_info.iloc[0]

        class_colors = QoIType.CLASS_WISE.get_class_colors(num_classes)
        class_names = QoIType.CLASS_WISE.get_qoi_type_widget_options(
            num_classes
        )
        fig = NLPPlots._token_influence_histogram(
            num_classes,
            highlight_token_info,
            class_colors=class_colors,
            class_names=class_names,
            **kwargs
        )
        display(fig)

    @staticmethod
    def _influence_examples(
        tokens_list: Iterable[Iterable[str]],
        attributions_list: Iterable[Iterable[float]],
        *,
        qoi_class: Union[int, str],
        underline_list: Optional[Union[Iterable[Iterable[int]],
                                       Iterable[int]]] = None,
        prepends: Union[Iterable[str], str] = ''
    ):
        """
        plot the tokens & their attributions for list of token and attributions one by one
        underline_list specify the token index to underline (used for plotting influence of a sentence
        containing a specific token)
        """
        if len(attributions_list) == 0:
            return
        norm_factor = np.max(
            [
                np.max(np.abs(attributions))
                for attributions in attributions_list
            ]
        )
        # Display legend
        neg_infl_color = rgb_str(256, 256 - MAX_INTENSITY, 256 - MAX_INTENSITY)
        neutral_color = rgb_str(256, 256, 256)
        pos_infl_color = rgb_str(256 - MAX_INTENSITY, 256, 256 - MAX_INTENSITY)
        if isinstance(qoi_class, int):
            qoi_class = f"Class: {qoi_class}"
        qoi_class = qoi_class.replace('_', ' ')
        qoi_class = qoi_class.title()
        html_str = [
            f'''
            <div style="margin:auto; width:50%; height:20px; display:flex; align-items:center;justify-content: space-between; background-image:linear-gradient(to right, {neg_infl_color}, {neutral_color}, {pos_infl_color});">
                <strong style=margin-left:4px>Negative Influence</strong>
                <strong style=text-align:center>{qoi_class}</strong>
                <strong style=margin-right:4px>Postive Influence</strong>
            </div>
            '''
        ]

        # Plot examples
        if isinstance(prepends, str):
            prepends = [prepends for _ in range(len(tokens_list))]
        for si, (attributions, tokens, prepend) in enumerate(
            zip(attributions_list, tokens_list, prepends)
        ):
            underline_idxs = [
                underline_list[si]
            ] if underline_list is not None else None
            if isinstance(underline_idxs, int):
                underline_idxs = [underline_idxs]
            line_html = generate_rgb_str(
                tokens,
                attributions,
                underline_idxs,
                norm_factor=norm_factor,
                max_intensity=MAX_INTENSITY
            )
            html = f'<p style=padding-bottom:2px><h4 style=margin:0;>{prepend}</h4> {line_html}'
            html_str.append(html)

        return html_print("\n".join(html_str))

    @staticmethod
    def influence_examples_segments(
        highlight_token: str,
        influences_dict: dict,
        influences_df: pd.DataFrame,
        error_driver_group_dict,
        influence_range: Iterable[float],
        token_frequency,
        group,
        class_idx: Optional[int] = 0
    ):
        """ Given a highlight token and an influence range, prints out all influence-highlighted examples
            where the influence of the highlight token lies within the influence range
        Args:
            highlight_token (str): The specific token to highlight in a sentence.
            influences_dict (dict): Dictionary containing influence values for tokens for a particular class and segment
            group (str): A grouping filter on the data. Typically error groups. Defaults to 'all'
            error_driver_group_dict (dict): The dictionary from group to record id.
            influences_df (pd.DataFrame): The influences of the records and tokens.
            influence_range (Iterable[float]): A filter on min and max influences to limit data.
            class_idx (Optional[int], optional): The class of the QoI. Defaults to 0.
        """
        final_index = []
        token_info = error_driver_group_dict[group]
        highlight_token_info = token_info.loc[token_info.tokens ==
                                              highlight_token]
        segment_eg_indexes = list(set(token_frequency[highlight_token]))
        if len(highlight_token_info) <= 0:
            return
        highlight_token_info = highlight_token_info.iloc[0]
        influences = np.array(
            highlight_token_info['influences_{}'.format(
                QoIType.CLASS_WISE.get_class_idx_name(class_idx)
            )]
        )

        influence_filter = (influences > influence_range[0]
                           ) & (influences < influence_range[1])

        data_indexes = np.array(highlight_token_info['data_index']
                               )[influence_filter]
        token_pos = list(
            np.array(highlight_token_info['token_pos'])[influence_filter]
        )

        preds = list(np.array(highlight_token_info['preds'])[influence_filter])
        labels = list(
            np.array(highlight_token_info['labels'])[influence_filter]
        )
        lengths = np.array(highlight_token_info['lengths'])[influence_filter]

        for index, value in enumerate(data_indexes):
            if value in segment_eg_indexes:
                final_index.append(index)

        data_indexes = [data_indexes[i] for i in final_index]
        token_pos = [token_pos[i] for i in final_index]
        preds = [preds[i] for i in final_index]
        labels = [labels[i] for i in final_index]
        lengths = [lengths[i] for i in final_index]
        tokens = [
            influences_df.iloc[data_index].tokens[:length]
            for data_index, length in zip(data_indexes, lengths)
        ]

        prepends = [
            f'data_index:{data_idx} pred:{pred} label:{label}'
            for data_idx, pred, label in zip(data_indexes, preds, labels)
        ]

        influences = [
            influences_df.iloc[data_index].influences[class_idx][:length]
            for data_index, length in zip(data_indexes, lengths)
        ]
        display(
            NLPPlots._influence_examples(
                tokens,
                influences,
                qoi_class=class_idx,
                underline_list=token_pos,
                prepends=prepends
            )
        )

    @staticmethod
    def influence_examples(
        highlight_token: str,
        group: str,
        error_driver_group_dict: dict,
        influences_df: pd.DataFrame,
        influence_range: Iterable[float],
        class_idx: Optional[int] = 0
    ):
        """ Given a highlight token and an influence range, prints out all influence-highlighted examples
            where the influence of the highlight token lies within the influence range
        Args:
            highlight_token (str): The specific token to highlight in a sentence.
            group (str): A grouping filter on the data. Typically error groups. Defaults to 'all'
            error_driver_group_dict (dict): The dictionary from group to record id.
            influences_df (pd.DataFrame): The influences of the records and tokens.
            influence_range (Iterable[float]): A filter on min and max influences to limit data.
            class_idx (Optional[int], optional): The class of the QoI. Defaults to 0.
        """
        token_info = error_driver_group_dict[group]
        highlight_token_info = token_info.loc[token_info.tokens ==
                                              highlight_token]
        if len(highlight_token_info) <= 0:
            return
        highlight_token_info = highlight_token_info.iloc[0]
        influences = np.array(
            highlight_token_info['influences_{}'.format(
                QoIType.CLASS_WISE.get_class_idx_name(class_idx)
            )]
        )

        influence_filter = (influences >= influence_range[0]
                           ) & (influences <= influence_range[1])
        data_indexes = np.array(highlight_token_info['data_index']
                               )[influence_filter]
        token_pos = list(
            np.array(highlight_token_info['token_pos'])[influence_filter]
        )
        lengths = np.array(highlight_token_info['lengths'])[influence_filter]
        tokens = [
            influences_df.iloc[data_index].tokens[:length]
            for data_index, length in zip(data_indexes, lengths)
        ]

        preds = list(np.array(highlight_token_info['preds'])[influence_filter])
        labels = list(
            np.array(highlight_token_info['labels'])[influence_filter]
        )
        prepends = [
            f'data_index:{data_idx} pred:{pred} label:{label}'
            for data_idx, pred, label in zip(data_indexes, preds, labels)
        ]

        influences = [
            influences_df.iloc[data_index].influences[class_idx][:length]
            for data_index, length in zip(data_indexes, lengths)
        ]
        display(
            NLPPlots._influence_examples(
                tokens,
                influences,
                qoi_class=class_idx,
                underline_list=token_pos,
                prepends=prepends
            )
        )

    @staticmethod
    def _record_explanations_attribution(
        ind_group: str,
        qoi_class: str,
        idf: pd.DataFrame,
        underline_idx=None,
        return_attributions_plot=True
    ):
        length = idf.iloc[ind_group].lengths
        tokens = idf.iloc[ind_group].tokens[:length]

        original_indexes = [idf.iloc[ind_group].original_index]
        preds = [idf.iloc[ind_group].preds]
        labels = [idf.iloc[ind_group].labels]

        prepends = [
            f'[idx:{data_idx} pred:{pred} label:{label}]'
            for data_idx, pred, label in zip(original_indexes, preds, labels)
        ]

        influences = get_influence_from_qoi_widget_options(
            qoi_class, idf.iloc[ind_group].influences[:, :length]
        )
        if return_attributions_plot:
            return NLPPlots._influence_examples(
                [tokens], [influences],
                qoi_class=qoi_class,
                underline_list=underline_idx and [underline_idx],
                prepends=prepends
            )
        return tokens, influences

    @staticmethod
    def _get_indices_after_partitions(
        segment: str, segment_to_point_ids: Dict[str, Sequence[int]],
        group_inds: Sequence[int], original_idx: int
    ) -> int:
        """ Finds all the records after partitioning, then gets the ordinal index,

        Args:
            segment (str): The segment being shown.
            segment_to_point_ids (Dict[str,Sequence[int]]): A dict of segment names to data indexes.
            group (str): The group being shown.
            group_ind_dict (Dict[str,Sequence[int]]): A dict of grouping names to data indexes.
            record_id (int): The record being shown.

        Returns:
            int: the record index after partition, as selected by the ordinal idx
        """
        group_idxs = set(group_inds)
        if segment_to_point_ids and segment != "None":
            segment_idxs = segment_to_point_ids[segment]
            union_idxs = group_idxs.intersection(set(segment_idxs))
        else:
            union_idxs = group_idxs

        if original_idx not in union_idxs:
            return None
        return original_idx

    @staticmethod
    def record_explanations_attribution(
        artifacts_container: ArtifactsContainer, aiq: NlpAIQ,
        token_type: TokenType, segment_to_point_ids: Dict[str, Sequence[int]],
        tab: str, record_id: int, segment: str, group_idxs: List[int],
        qoi_class: str, selected_token_idx: int,
        selected_ngram_token_idxs: List[int], group_name: str,
        selected_ngram_row_idx: int, influences_df: pd.DataFrame,
        update_selected_token: Callable, barplot_update_token: Callable,
        update_selected_token_options: Callable
    ) -> go.Figure:
        """ Explore individual records, explanations, and feature interactions.
        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            aiq (NlpAIQ): An NLP AIQ processor.
            token_type (TokenType): Determines if the tokens are architecture tokens or sentence level words. 
            group_ind_dict (Dict[str,Sequence[int]]): A dict of grouping names to data indexes.
            segment_to_point_ids (Dict[str,Sequence[int]]): A dict of segment names to data indexes.
            tab (str): The tab being viewed from the widget.
            record_id (int): The record being shown.
            segment (str): The segment being shown.
            group (str): The group being shown.
            qoi_class (str): The explanation QoI class.
            selected_token (str): The token being plotted.
            influences_df (pd.DataFrame): The influences.
        
        Returns:
            go.Figure: The visualizations depending on the tab selected.
        """
        data_idx = NLPPlots._get_indices_after_partitions(
            segment, segment_to_point_ids, group_idxs, record_id
        )
        if data_idx is None:
            if group_name is not None and group_name != "All":
                resp = f"No records in group {group_name}"
            else:
                resp = f"No records available"
            display(widgets.Label(resp))
            return

        if tab == "Record Explanations":
            record_attr_plot = NLPPlots._record_explanations_attribution(
                data_idx,
                qoi_class,
                influences_df,
                return_attributions_plot=True
            )
            display(record_attr_plot)
            return record_attr_plot
        else:
            length_limit = 75
            class_idx = get_class_idx_from_qoi_widget_options(qoi_class)

            corrs, corr_idx_mapping = aiq.model.get_correlation_matrices(
                artifacts_container,
                1,
                class_idx=class_idx,
                token_type=token_type,
                offset=data_idx,
                filter_top_n=length_limit
            )
            corr_idx_mapping = corr_idx_mapping[0]
            corrs = corrs[0]

            # Callback to update tokens dropdown to only show tokens with corrs
            update_selected_token_options(corr_idx_mapping)

            record_length = influences_df.loc[data_idx].lengths
            token_influences = influences_df.loc[data_idx].influences[
                class_idx, :record_length]
            tokens = influences_df.loc[data_idx].tokens

            selected_token = influences_df.loc[data_idx].tokens[
                selected_token_idx]
            if selected_token_idx not in corr_idx_mapping and selected_token_idx != -1:
                print(
                    f"No interaction data for token '{selected_token}': Due to large sentence length, this widget only examines the {-1} most interacting tokens."
                )
                return

            # Visualization toggles
            table_widget = ngram_correlation_table_widget(
                corrs=corrs,
                corr_idx_mapping=corr_idx_mapping,
                tokens=tokens,
                token_influences=token_influences,
                selected_ngram_row_idx=None
                if selected_ngram_row_idx == -1 else selected_ngram_row_idx,
                row_change_callback=update_selected_token
            )
            # Both display and return is necessary for proper functionality
            plots = [table_widget]

            if selected_token_idx != -1:
                ### adding a constraint on length (50 for now) as it is taking too long to compute
                # interactions for long sequences, killing notebook kernels.
                length = aiq.model.get_lengths(
                    artifacts_container, 1, offset=data_idx
                )[0].astype(int)[0]
                if length_limit and length > length_limit:
                    print(
                        f'Sentence too long with {length} tokens. Limiting evaluation of interactions to top {length_limit} most interactive tokens.'
                    )
                barplot = InteractionPlots.token_interaction_bar(
                    corrs=corrs,
                    corr_idx_mapping=corr_idx_mapping,
                    tokens=tokens,
                    token_idx=selected_token_idx,
                    ngram_idxs=selected_ngram_token_idxs,
                    update_token_callback=barplot_update_token
                )

                grad_landscape_info = aiq.gradient_landscape_info(
                    artifacts_container,
                    1,
                    offset=data_idx,
                    class_idx=class_idx,
                    token_type=token_type
                )

                grad_landscape_chart = InteractionPlots.gradient_landscape_graph(
                    record_info=grad_landscape_info,
                    record_idx=data_idx,
                    corrs=corrs,
                    corr_idx_mapping=corr_idx_mapping,
                    init_word_idx=selected_token_idx
                )

                # Nest into accordion

                gradient_paths_description = """
<p>
<h3>Definition: Gradient Paths</h3>
Integrated Gradients interpolates between the feature embedding and a baseline, at each step taking the gradient of the QoI wrt the interpolated value. The resulting series of gradients along that interpolation is the gradient path.
</p><p>
<h3>Definition: Interaction correlation</h3>
The correlations of each feature's gradient paths are used to measure feature interactions. Nearby tokens or tokens with similar meanings are expected to produce higher correlations as their contribution to the QoI is likely to share a functional interaction in the neural network.
</br>
Pearson correlation is used for list based correlation. 
</p><p>
<h3>Reading the Graph</h3>
In the chart below, the X-axes tracks the interpolation step and the Y-axes plots the gradient values for each feature. For accessibility, we limit the values plotted to the 5 tokens most correlated with the selected token.
</p>
"""
                grad_landscape_accordion = widgets.Accordion(
                    children=[
                        VBox(
                            [
                                widgets.HTML(value=gradient_paths_description),
                                grad_landscape_chart
                            ]
                        )
                    ]
                )
                grad_landscape_accordion.set_title(
                    0, 'What are these correlations measuring?'
                )
                grad_landscape_accordion.selected_index = None
                plots.extend([barplot, grad_landscape_accordion])

            disp_output = widgets.VBox(plots)
            clear_output(wait=True)
            display(disp_output)
            return disp_output

    @staticmethod
    def segment_output_metrics(
        artifacts_container: ArtifactsContainer,
        aiq: NlpAIQ,
        multi_class_segment_metrics: Dict[str, Any],
        metric_viz_tab: str,
        output_type_tab: str,
        positive_group_tab: Sequence[int],
        display_disadvantaged_segments_tab: int,
        segment_1: str,
        segment_2: str,
    ):

        segment_metrics = multi_class_segment_metrics

        if output_type_tab == "Binary":
            if len(positive_group_tab):
                segment_metrics = aiq.model.get_segment_ind_dict(
                    artifacts_container=artifacts_container,
                    binarize_data=True,
                    positive_group=list(positive_group_tab)
                )
            else:
                print(
                    "Select class IDs in positive group in order to visualize binary classification."
                )

        if metric_viz_tab == 'CONF_MATRIX':
            visualize_confusion_matrix(
                disparity_wrapper(
                    OutputMetrics.CONFUSION_MATRIX, segment_metrics, segment_1,
                    segment_2
                )
            )
        elif metric_viz_tab == 'CONF_RATES':
            visualize_confusion_matrix_rates(
                disparity_wrapper(
                    OutputMetrics.CONFUSION_MATRIX_METRICS, segment_metrics,
                    segment_1, segment_2
                )
            )
        elif metric_viz_tab == 'ACCURACY':
            visualize_accuracy(
                disparity_wrapper(
                    OutputMetrics.ACCURACY, segment_metrics, segment_1,
                    segment_2, True
                )
            )
        elif metric_viz_tab == 'F1_SCORE':
            visualize_f1_score(
                disparity_wrapper(
                    OutputMetrics.F1_SCORE, segment_metrics, segment_1,
                    segment_2, True
                )
            )
        else:
            print("Ignore Segment 1 and Segment 2 Dropdown selectors.")
            if output_type_tab == "Binary":
                if display_disadvantaged_segments_tab > 0 and len(
                    positive_group_tab
                ) > 0:
                    segment_disadvantage_rankings = get_segment_disadvantage_rankings(
                        segment_metrics, display_disadvantaged_segments_tab
                    )

                    print(segment_disadvantage_rankings)
                elif display_disadvantaged_segments_tab > 0:
                    print("Select positive class IDs.")
                else:
                    print(
                        "Move slider Num Ranks to choose how many segment ranks to visualize."
                    )
            else:
                print("Select Binary visualization")

    @staticmethod
    def global_explanations_error_driver(
        token: str, group: str, token_ind_group: int, qoi_class: str,
        max_influence_examples_per_token: int, record_influences_df_dict: dict,
        error_driver_group_dict: dict,
        text_examples_df_train_classes: pd.DataFrame
    ):
        for class_idx, text_examples_df_train_class in enumerate(
            text_examples_df_train_classes
        ):
            print('class: {} training examples: '.format(class_idx))
            if len(text_examples_df_train_class) > 0:
                token_class_train_examples = text_examples_df_train_class[
                    text_examples_df_train_class.tokens == token]
                if len(token_class_train_examples) > 0:
                    display(token_class_train_examples)
                else:
                    print('No records with this class and token')
            else:
                print('No records with this class')
            print('======' * 10)

        token_influences_df = error_driver_group_dict[group]
        token_indices = token_influences_df.tokens == token

        if token_indices.sum() > 0:
            ind_group = list(token_influences_df[token_indices].data_index
                            )[0][:max_influence_examples_per_token]
            token_pos = list(token_influences_df[token_indices].token_pos
                            )[0][:max_influence_examples_per_token]
            num_occurrences = list(
                token_influences_df[token_indices].occurrences
            )[0]
            length = list(token_influences_df[token_indices].lengths
                         )[0][:max_influence_examples_per_token]
            tokens = [
                record_influences_df_dict.iloc[ind_groupi].tokens[:lengthi]
                for ind_groupi, lengthi in zip(ind_group, length)
            ]
            influences = [
                get_influence_from_qoi_widget_options(
                    qoi_class,
                    record_influences_df_dict.iloc[ind_groupi].influences
                )[:lengthi] for ind_groupi, lengthi in zip(ind_group, length)
            ]
            print('number of occurrences: ', num_occurrences)
            influence_columns = [
                col for col in token_influences_df.columns if 'mean' in col
            ]
            print(influence_columns)
            print(
                'comparative qoi & average influence for the prediction class qoi',
                token_influences_df[token_indices][influence_columns].values[0]
            )
            display(
                NLPPlots._influence_examples(
                    tokens,
                    influences,
                    qoi_class=qoi_class,
                    underline_list=token_pos
                )
            )

    @staticmethod
    def get_counterfactual_filters(
        df: pd.DataFrame, group: str, group_cf: str, word_from: str,
        word_to: str
    ):
        """
        double filter based on df and counterfactual df
        """
        filters = get_filter_from_group_name(
            df.preds, df.labels, group
        ) & get_filter_from_group_name(df.preds_cf, df.labels, group_cf)
        if word_from != '':
            filters = filters & (df.word_from == word_from.strip())
        if word_to != '':
            filters = filters & (df.word_to == word_to.strip())
        return filters

    @staticmethod
    def display_counterfactual_text_df(
        text_df: pd.DataFrame, display_level: str, page_size: int,
        page_idx: int, word_from: str, word_to: str, qoi_class: str,
        ind_group: int, group: str, group_cf: str
    ):
        filters = NLPPlots.get_counterfactual_filters(
            text_df, group, group_cf, word_from, word_to
        )
        pd.set_option('display.max_colwidth', None)
        print('number of instances after filtering: ', filters.sum())
        text_df_filtered: pd.DataFrame = text_df[filters].round(3)
        text_df_filtered = text_df_filtered.iloc[page_size *
                                                 (page_idx - 1):page_size *
                                                 page_idx
                                                ]  # page_idx starts at 1

        if len(text_df_filtered) == 0:
            return

        display_columns = [
            "original_index", "MaskedText", "word_from", "word_to",
            "coherence_score", "preds", "preds_cf", "labels", "corrs"
        ]
        if display_level == 'global':
            display(text_df_filtered[display_columns])
        elif display_level == 'local':
            token_pos = text_df.mask_pos.iloc[ind_group]
            text_df_iloced = text_df.iloc[[ind_group]]
            display(text_df_iloced[display_columns])

            tokens_list = []
            influences_list = []
            underline_list = []

            influences_df = text_df_iloced[[
                "preds", "labels", "lengths", "influences", "tokens",
                "original_index", "swap"
            ]]
            influences_df_cf = text_df_iloced[[
                "preds_cf", "labels_cf", "lengths_cf", "influences_cf",
                "tokens_cf", "original_index", "swap_cf"
            ]].rename(
                columns={
                    "preds_cf": "preds",
                    "labels_cf": "labels",
                    "lengths_cf": "lengths",
                    "influences_cf": "influences",
                    "tokens_cf": "tokens",
                    "swap_cf": "swap"
                }
            )

            for idf in [influences_df, influences_df_cf]:
                tokens, influences = NLPPlots._record_explanations_attribution(
                    0,
                    qoi_class,
                    idf,
                    token_pos,
                    return_attributions_plot=False
                )
                tokens_list.append(tokens)
                influences_list.append(influences)
            if influences_df['swap'].iloc[0] is None:
                underline_list = None
            else:
                diff_start = influences_df['swap'].iloc[0][0]
                diff_end = influences_df['swap'].iloc[0][1]
                diff_cf_end = influences_df_cf['swap'].iloc[0][1]
                influences_w_swap_info, tokens_w_swap_info = merge_lists_with_swaps(
                    infs=influences_list[0],
                    tokens=tokens_list[0],
                    diff_start=diff_start,
                    diff_end=diff_end
                )
                influences_cf_w_swap_info, tokens_cf_w_swap_info = merge_lists_with_swaps(
                    infs=influences_list[1],
                    tokens=tokens_list[1],
                    diff_start=diff_start,
                    diff_end=diff_cf_end
                )
                underline_list.append(range(diff_start, diff_end + 1))
                underline_list.append(range(diff_start, diff_cf_end + 1))
                if len(tokens_w_swap_info) == len(tokens_cf_w_swap_info):
                    tokens_diff = [
                        t if t == tokens_cf_w_swap_info[ti] else t + '->' +
                        tokens_cf_w_swap_info[ti]
                        for ti, t in enumerate(tokens_w_swap_info)
                    ]
                    tokens_list.append(tokens_diff)
                    influences_list.append(
                        np.asarray(influences_cf_w_swap_info) -
                        np.asarray(influences_w_swap_info)
                    )
                    underline_list.append(range(diff_start, diff_start + 1))
            print(
                'influences for (1) original data, (2) counterfactual data and (3) influence difference'
            )
            display(
                NLPPlots._influence_examples(
                    tokens_list,
                    influences_list,
                    qoi_class=qoi_class,
                    underline_list=underline_list
                )
            )

    @staticmethod
    def evaluate_text_box(
        button: widgets.widget_button.Button,
        model_wrapper: nlp.Wrappers.ModelRunWrapper, model: Any,
        tokenizer: nlp.Wrappers.TokenizerWrapper, text: str,
        class_names: List[str]
    ) -> None:

        # TODO: was this meant to get logits or something else?
        predictions = model_wrapper.evaluate_model_from_text(
            model, text.value, tokenizer
        ).probits[0]

        layout = Plots.truera_layout(
            title_text=text.value,
            title_font={'size': 10},
            xaxis=dict(title=f'Model Output'),
        )
        fig = go.FigureWidget(layout=layout)
        fig.add_trace(
            go.Bar(
                y=class_names,
                x=predictions,
                orientation='h',
                marker_color=Colors.DEFAULT_COLOR_WHEEL[:len(class_names)]
            )
        )
        trace = fig.data[0]

        def on_button_clicked(b):
            # TODO: was this meant to get logits or something else?
            trace.x = model_wrapper.evaluate_model_from_text(
                model, text.value, tokenizer
            ).probits[0]
            fig.update_layout(title_text=text.value)

        button.on_click(on_button_clicked)
        display(VBox([text, button, fig]))
