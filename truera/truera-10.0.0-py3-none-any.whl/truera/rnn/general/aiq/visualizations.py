from typing import Optional, Tuple
from urllib.parse import quote

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.selection.interaction_selection import \
    AggregationMethod
from truera.rnn.general.selection.interaction_selection import FeatureSpace
from truera.rnn.general.selection.interaction_selection import \
    GlobalExplanationView
from truera.rnn.general.selection.interaction_selection import \
    InfluenceAggregationMethod
from truera.rnn.general.selection.interaction_selection import InteractAlong
from truera.rnn.general.selection.interaction_selection import InteractionType
from truera.rnn.general.selection.interaction_selection import ModelGrouping
from truera.rnn.general.selection.interaction_selection import SortingMode
from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.service.container import Locator
from truera.rnn.general.utils import log
import truera.rnn.general.utils.colors as Colors
from truera.rnn.general.utils.errors import viz_callback
import truera.rnn.general.utils.export as Export
from truera.rnn.general.utils.tables import get_chunked_table
from truera.rnn.general.utils.tables import get_dash_table_from_df
from truera.rnn.general.utils.tables import get_html_table

from . import filters as Filters
from . import input_inf_utils as ii_utils
from .diagnostics import DiagnosticsGenerator


def nml(arr, sort=False):
    if sort:
        arrmax, arrmin = arr.min(), arr.max()
    else:
        arrmax, arrmin = arr.max(), arr.min()
    denom = arrmax - arrmin
    if denom == 0:
        denom += 10e-10  # fix invalid divide issues
    return (arr - arrmin) / denom


class Figures():

    def __init__(self, aiq, href_path=''):
        self.aiq = aiq
        self.diagnostics = DiagnosticsGenerator(aiq=aiq)
        self.href_path = href_path

    def set_href_path(self, href_path):
        self.href_path = href_path

    def get_record_info_from_index(
        self, index, artifacts_container: ArtifactsContainer, num_records
    ):
        record_id = self.aiq.get_record_ids(
            artifacts_container, num_records, sample_index=index
        )
        seq_length = self.aiq.get_lengths(
            artifacts_container, num_records, sample_index=index
        )
        return record_id, seq_length

    def get_feature_names(
        self, artifacts_container: ArtifactsContainer, internal=False
    ):
        return self.aiq.get_feature_names(
            artifacts_container, internal=internal
        )

    def get_concatenated_feature_descriptions(
        self, artifacts_container: ArtifactsContainer, feature_names
    ):
        return self.aiq.get_concatenated_feature_descriptions(
            artifacts_container, feature_names
        )

    def get_nonnumeric_feature_map(
        self, artifacts_container: ArtifactsContainer
    ):
        return self.aiq.get_nonnumeric_feature_map(artifacts_container)

    def get_total_timesteps(
        self, artifacts_container: ArtifactsContainer, input_timesteps=True
    ):
        return self.aiq.get_total_timesteps(
            artifacts_container, input_timesteps=input_timesteps
        )

    def get_max_batchsize(
        self, artifacts_container: ArtifactsContainer, dep_level
    ):
        return self.aiq.get_max_batchsize(artifacts_container, dep_level)

    def get_default_threshold(self, artifacts_container: ArtifactsContainer):
        return self.aiq.get_default_threshold(artifacts_container)

    @viz_callback
    def record_explanations_attribution_tab(
        self,
        index,
        timestep_values,
        sort_mode,
        num_display_features,
        compare_feature_indices,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=None,
        influence_precision=3
    ):
        nonnumeric_feature_map = self.get_nonnumeric_feature_map(
            artifacts_container
        )
        attribution_df, all_influences, data, timesteps, summed_influence = self.aiq.local_explanations_attribution_info(
            index,
            timestep_values,
            sort_mode,
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep
        )
        attribution_df['total_influence'] = attribution_df[
            'total_influence'].round(influence_precision).astype(str)
        influence_range = [np.min(all_influences), np.max(all_influences)]

        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            height=100,
            width=200,
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        table_rows = []

        attribution_df = pd.concat(
            [
                attribution_df[
                    attribution_df.index.isin(compare_feature_indices)],
                attribution_df[~attribution_df.index.
                               isin(compare_feature_indices)]
            ]
        )
        attribution_df = attribution_df.iloc[:num_display_features]
        for i, row in attribution_df.iterrows():
            influences = all_influences[:, i]
            feature_values = data[:, i]
            feature_descs = ["{:.4f}".format(f) for f in feature_values]
            if row['feature_name'] in nonnumeric_feature_map:
                feature_descs = [
                    nonnumeric_feature_map[row['feature_name']][f]
                    for f in feature_values
                ]

            influence_per_timestep_fig = go.Figure(
                [
                    go.Bar(
                        x=timesteps,
                        y=influences,
                        marker_color=Colors.TRUERA_GREEN_90
                    )
                ],
                layout=layout
            )
            value_per_timestep_fig = go.Figure(
                [
                    go.Bar(
                        x=timesteps,
                        y=feature_values,
                        text=feature_descs,
                        hovertemplate="(%{x}, %{text})<extra></extra>",
                        marker_color=Colors.TRUERA_GREEN_90
                    )
                ],
                layout=layout
            )
            influence_per_timestep_fig.update_yaxes(
                visible=False, showticklabels=False, range=influence_range
            )
            influence_per_timestep_fig.update_xaxes(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                rangemode="tozero"
            )
            value_per_timestep_fig.update_yaxes(
                visible=False, showticklabels=False
            )
            value_per_timestep_fig.update_xaxes(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                rangemode="tozero"
            )
            quotified_feature = quote(row['feature_name'])
            feature_desc_cell = html.Div(
                [
                    html.Strong(row['feature_name']),
                    dbc.Button(
                        href=f'{self.href_path}features#{quotified_feature}',
                        color="link",
                        className="fa fa-external-link-alt fa-sm",
                        style={'color': Colors.TRUERA_GREEN}
                    ),
                    html.P(row['feature_desc'])
                ]
            )

            table_rows.append(
                [
                    feature_desc_cell, row['total_influence'],
                    dcc.Graph(
                        figure=influence_per_timestep_fig,
                        config={'displayModeBar': False}
                    ),
                    dcc.Graph(
                        figure=value_per_timestep_fig,
                        config={'displayModeBar': False}
                    )
                ]
            )
        table_headers = [
            "Feature", "Total influence", "Feature influence per timestep",
            "Feature Value"
        ]
        table = get_html_table(table_headers, table_rows)
        return [table, summed_influence]

    def local_explanations_prediction_tab_single_record(
        self,
        prediction_info: pd.DataFrame,
    ):
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            ),
            height=150,
            width=700,
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        return dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=prediction_info['timesteps'],
                        y=prediction_info['labels'],
                        marker_color=Colors.TRUERA_GREEN_90,
                        name='Labels'
                    ),
                    go.Scatter(
                        x=prediction_info['timesteps'],
                        y=prediction_info['predictions'],
                        marker_color=Colors.TRUERA_GREEN,
                        name='Predictions'
                    ),
                    go.Scatter(
                        x=prediction_info['timesteps'],
                        y=prediction_info['thresholds'],
                        marker_color=Colors.BACKGROUND_95,
                        name='Threshold',
                        mode="lines"
                    )
                ],
                layout=layout
            ),
            config={'displayModeBar': False}
        )

    @viz_callback
    def local_explanations_prediction_tab(
        self,
        record_indices,
        timestep_values,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        thresh=0.5,
        view_all_class_filter: bool = False
    ):
        table_data = []
        for record_index in record_indices:
            prediction_info = self.aiq.local_explanations_prediction_info(
                record_index,
                timestep_values,
                artifacts_container,
                num_records,
                qoi_core_class=qoi_core_class,
                thresh=thresh,
                view_all_class_filter=view_all_class_filter
            )
            record_label = html.Strong('Record {}'.format(record_index))
            table_data.append(
                [
                    record_label,
                    self.local_explanations_prediction_tab_single_record(
                        prediction_info
                    )
                ]
            )
        return get_html_table(["Record", ""], table_data)

    def local_explanations_prediction_tab_record_indices(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        filter_list=[],
        qoi_core_class: int = 0
    ):
        if len(filter_list) == 0:
            return np.arange(
                num_records
            )  # no filters applied, return all records
        preds = self.aiq.get_predictions(artifacts_container, num_records)
        labels = self.aiq.get_ground_truth(artifacts_container, num_records)
        seq_lengths = self.aiq.get_lengths(artifacts_container, num_records)
        filter_criteria = Filters.get_multi_filter_criteria(
            self.aiq,
            qoi_core_class,
            preds,
            labels,
            None,
            seq_lengths,
            artifacts_container,
            num_records,
            filter_list=filter_list
        )
        return np.where(filter_criteria == True)[0]

    @viz_callback
    def local_temporal_trends_heatmap(
        self,
        record_index,
        num_records,
        timestep_values,
        feature_index,
        artifacts_container: ArtifactsContainer,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=None
    ):
        influences = self.aiq.get_influences_per_timestep(
            'input',
            artifacts_container,
            num_records,
            sample_index=record_index,
            class_index=qoi_core_class,
            feature_index=feature_index
        )
        timestep_min, timestep_max = timestep_values
        timesteps = list(range(timestep_min, timestep_max + 1))
        if influences.shape[0] == influences.shape[1]:
            # equal input and output TS implies inputs and outputs could be variable length
            influences = influences[timesteps][:, timesteps]
        else:
            # Otherwise take all the output timesteps
            influences = influences[timesteps]
        influences = np.triu(
            influences
        )  # zero out anything in the lower left triangle of the matrix
        range_max = np.max(np.abs(influences))
        tickvals = list(range(len(influences)))
        ticktext = [f'T-{i}' for i in tickvals[::-1]]
        fig = ff.create_annotated_heatmap(
            influences,
            xgap=10,
            ygap=10,
            zmin=-range_max,
            zmax=range_max,
            showscale=True,
            colorscale=Colors.HEATMAP_COLOR_SCALE,
            font_colors=["black"],
            hovertemplate=
            "<b>Input timestep:</b> %{y}<br><b>Output timestep:</b> %{x}<br><b>Influence:</b> %{z}<extra></extra>",
        )
        fig.update_layout(
            go.Layout(
                plot_bgcolor=Colors.WHITE,
                height=700,
                width=800,
                showlegend=False,
                xaxis_title='Output Timestep',
                yaxis_title='Input Timestep',
                xaxis=dict(
                    showgrid=False,
                    showticklabels=True,
                    tickmode='array',
                    ticktext=ticktext,
                    tickvals=tickvals
                ),
                yaxis=dict(
                    showgrid=False,
                    showticklabels=True,
                    autorange='reversed',
                    tickmode='array',
                    ticktext=ticktext,
                    tickvals=tickvals
                )
            )
        )
        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    @viz_callback
    def local_expl_neuron_figure(
        self,
        index,
        artifacts_container: ArtifactsContainer,
        num_records,
        neuron=None,
        sort=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=None,
        top_n_features=20,
        feature=None
    ):
        record_id = self.aiq.get_record_ids(
            artifacts_container, num_records, sample_index=index
        )
        seq_length = self.aiq.get_lengths(
            artifacts_container, num_records, sample_index=index
        )
        feature_names = np.array(self.get_feature_names(artifacts_container))
        labels = self.aiq.get_ground_truth(
            artifacts_container, num_records, sample_index=index
        )[..., qoi_core_class:qoi_core_class + 1]

        preds_df, preds_high, preds_low, infs_df, display_df, summed_column = self.aiq.internal_unit_influence_info(
            index,
            artifacts_container,
            num_records,
            neuron=neuron,
            sort=sort,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            top_n_features=top_n_features,
            feature=feature
        )

        figure = make_subplots(
            rows=2,
            cols=2,
            shared_yaxes=True,
            column_widths=[1. / (seq_length + 1), 1. - 1. / (seq_length + 1)],
            row_heights=[1. - 1. / top_n_features, 1. / top_n_features],
            horizontal_spacing=0.02,
            vertical_spacing=0.2,
            subplot_titles=[
                'Feature <br> Influences',
                'Feature values and <br> influences by time-step',
                'ID: {}'.format(record_id), 'Labels and Predictions'
            ]
        )

        start_step = 0
        end_step = self.aiq.get_lengths(
            artifacts_container, num_records, sample_index=index
        )
        annotations = []
        for i, f_idx in enumerate(display_df.index.values):
            for step in range(seq_length):
                annotations.append(
                    go.layout.Annotation(
                        text=str(
                            self.aiq.get_data(
                                artifacts_container,
                                num_records,
                                sample_index=index
                            )[start_step + step][f_idx]
                        ),
                        x=step,
                        y=i,
                        xref='x2',
                        yref='y1',
                        showarrow=False
                    )
                )
            #Add influences for the last step
            annotations.append(
                go.layout.Annotation(
                    text='{:.2g}'.format(
                        display_df.iloc[i, :summed_column].sum()
                    ),
                    x=0,
                    y=i,
                    xref='x1',
                    yref='y1',
                    showarrow=False
                )
            )

        # Below is a stupid fix.
        # Some super finicky plotly bug where it misses the last 2 annotations unless you bombard it with more
        i = 0
        for f_idx in display_df.index.values:
            if (i < 3):
                for step in range(seq_length):
                    annotations.append(
                        go.layout.Annotation(
                            text=str(
                                self.aiq.get_data(
                                    artifacts_container,
                                    num_records,
                                    sample_index=index
                                )[start_step + step][f_idx]
                            ),
                            x=step,
                            y=i,
                            xref='x2',
                            yref='y1',
                            showarrow=False
                        )
                    )
            i += 1
        trace_out = go.Heatmap(
            z=preds_df.iloc[:, start_step:end_step].values,
            hoverinfo='z',
            colorscale='Blues',
            showscale=False,
            zmin=preds_low,
            zmax=preds_high
        )

        trace0 = go.Heatmap(
            z=display_df.iloc[:, summed_column].values.reshape((-1, 1)),
            y=feature_names[display_df.index.values],
            hoverinfo='y+z',
            colorscale='PiYG',
            showscale=False
        )

        trace = go.Heatmap(
            z=display_df.iloc[:, start_step:end_step].values.tolist(),
            y=feature_names[display_df.index.values],
            hoverinfo='y+z',
            colorscale='PiYG',
            showscale=False
        )

        figure.add_trace(trace_out, row=2, col=2)
        figure.add_trace(trace0, row=1, col=1)
        figure.add_trace(trace, row=1, col=2)

        figure.update_xaxes(
            row=1,
            col=2,
            ticktext=['t-{:d}'.format(i) for i in reversed(range(seq_length))],
            tickvals=list(range(seq_length)),
        )

        figure.update_xaxes(
            row=2,
            col=2,
            ticktext=[
                '{:d}'.format(i)
                for i in np.squeeze(labels)[start_step:end_step]
            ],
            tickvals=list(range(seq_length)),
        )
        figure.update_xaxes(
            row=1,
            col=1,
            ticktext=[
                '<b>Total<br>Influence</b><br>{:0.2g}'.format(
                    infs_df.values.sum()
                )
            ],
            tickvals=[0],
        )
        figure.update_yaxes(
            row=1,
            col=1,
            ticktext=self.get_concatenated_feature_descriptions(
                artifacts_container, feature_names[display_df.index.values]
            ),
            tickvals=list(range(len(display_df.index.values))),
        )
        figure.update_layout(annotations=annotations, height=700)
        return figure

    def _flatten_by_class(self, array):
        '''
        creates a stacked list of elements that repeat for each item and each class.
        Assumes input array has indices in the first dimension, and class in the last dimension.
        '''
        num_classes = array.shape[-1]

        stack_list = []
        for i in range(len(array)):
            # class dimension
            for j in range(num_classes):
                stack_list.append(array[i, ..., j])

        if (len(stack_list) <= 0):
            return np.empty(shape=(0, 0))

        class_flattened = np.stack(stack_list)
        return class_flattened

    def _create_filtered_pred_or_label(
        self, pred_or_label, filter_criteria, start_record, num_records
    ):
        '''
        created a stacked list of record*class in the first axis for display purposes
        '''
        # Copy the filter so as not to modify the original filter as it may be used again outside this function
        if (filter_criteria is not None):
            filter_criteria = np.copy(filter_criteria)
        else:
            filter_criteria = np.asarray([True] * len(pred_or_label))
        filter_criteria[:start_record] = False
        filtered = pred_or_label[filter_criteria]
        filtered = filtered[:num_records]
        filter_idx = np.where(filter_criteria == True)[0][:num_records]

        class_flattened = self._flatten_by_class(filtered)

        return class_flattened, filter_idx

    def create_input_influence_2d_figure(
        self,
        df,
        compare_df,
        grouping_names,
        grouping,
        feature_name,
        feature_desc,
        include_title=True,
        figsize: Optional[Tuple[int, int]] = None
    ):
        feature_title = dbc.Row(
            [
                html.Strong(feature_name),
                dbc.Button(
                    href=f'{self.href_path}features#{quote(feature_name)}',
                    color="link",
                    className="fa fa-external-link-alt fa-sm",
                    style={'color': Colors.TRUERA_GREEN}
                )
            ],
            justify='center'
        )
        feature_desc = dbc.Row(feature_desc, justify='center')

        fig = go.Figure()
        fig.update_layout(
            height=500,
            width=450,
            margin=dict(l=20, r=20, t=0, b=20),
            plot_bgcolor=Colors.WHITE
        )
        if compare_df is None:
            colors = Colors.DEFAULT_COLOR_WHEEL
            if grouping == ModelGrouping.OVERFITTING:
                colors = Colors.BINARY_HIGHLIGHT_COLOR_WHEEL
                grouping_names = [
                    {
                        'yes': 'Overfit',
                        'no': None
                    }.get(g) for g in grouping_names
                ]

            for i in range(len(grouping_names)):
                df_group = df[df["group"] == i]
                fig.add_trace(
                    go.Scatter(
                        x=df_group["vals"],
                        y=df_group["infs"],
                        mode="markers",
                        name=grouping_names[i],
                        marker=dict(color=colors[i]),
                        showlegend=(
                            grouping not in [
                                ModelGrouping.NONE, ModelGrouping.OVERFITTING
                            ]
                        ),
                        text=[
                            "Record Index:{}<br>ID:{}".format(
                                row['indices'], row['record_id']
                            ) for j, row in df_group.iterrows()
                        ]
                    )
                )
        else:  # compare_df exists; ignore grouping
            fig.add_trace(
                go.Scattergl(
                    x=df["vals"],
                    y=df["infs"],
                    mode="markers",
                    marker=dict(color=Colors.TRUERA_GREEN),
                    showlegend=False,
                    text=[
                        "Record Index:{}<br>ID:{}".format(
                            row['indices'], row['record_id']
                        ) for j, row in df.iterrows()
                    ]
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=compare_df["vals"],
                    y=compare_df["infs"],
                    mode="markers",
                    marker=dict(color=Colors.DEFAULT_ORANGE),
                    showlegend=False,
                    text=[
                        "Record Index:{}<br>ID:{}".format(
                            row['indices'], row['record_id']
                        ) for j, row in compare_df.iterrows()
                    ]
                )
            )

        try:
            df_fit = ii_utils.fit(df)
            fig.add_trace(
                go.Scatter(
                    x=df_fit["x"],
                    y=df_fit["fit"],
                    mode="lines",
                    marker=dict(color=Colors.BACKGROUND_95),
                    showlegend=False
                )
            )
        except:
            log.debug("insufficient data for fit")
        fig.update_yaxes(
            title_text='Influence',
            showline=True,
            linewidth=2,
            linecolor=Colors.BACKGROUND_95
        )
        fig.update_xaxes(
            title_text='Feature Value',
            showline=True,
            linewidth=2,
            linecolor=Colors.BACKGROUND_95
        )
        if figsize is not None:
            fig.update_layout(width=int(figsize[0]), height=figsize[1])
        children = [dcc.Graph(figure=fig)]
        if include_title:
            children = [feature_title, feature_desc] + children
        return dbc.Container(children, style={
            'padding': '10px',
        })

    def input_inf_2d_figures(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        features,
        index=None,
        thresh=None,
        thresh_le=False,
        timestep=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping=None,
        compare_qoi=None,
        compare_qoi_timestep=None,
        filter_list=[]
    ):
        feature_names = self.get_feature_names(artifacts_container)
        feature_descs = self.aiq.get_formatted_feature_descriptions(
            artifacts_container, feature_names
        )
        dfs, grouping_str, group_names = self.aiq.input_inf_2d_info(
            artifacts_container,
            num_records,
            features,
            index=index,
            thresh=thresh,
            thresh_le=thresh_le,
            timestep=timestep,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping=grouping,
            filter_list=filter_list
        )
        dfs_compare = {}
        if compare_qoi is not None:
            dfs_compare, grouping_str, group_names = self.aiq.input_inf_2d_info(
                artifacts_container,
                num_records,
                features,
                index=index,
                thresh=thresh,
                thresh_le=thresh_le,
                timestep=timestep,
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=compare_qoi,
                qoi_timestep=compare_qoi_timestep,
                pred_thresh=pred_thresh,
                grouping=grouping,
                filter_list=filter_list
            )

        showlegend = not (grouping is None or grouping_str == 'none')
        return get_chunked_table(
            [
                self.create_input_influence_2d_figure(
                    dfs[f], dfs_compare.get(f), group_names, grouping,
                    feature_names[f], feature_descs[f]
                ) for f in features
            ]
        )

    @viz_callback
    def export_feature_splines(
        self,
        export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer,
        num_records,
        length_thresh=None,
        length_thresh_le=False,
        timestep_forward=False,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping_str=None,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        export_data = self.aiq.feature_splines_export_info(
            artifacts_container,
            num_records,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            timestep_forward=timestep_forward,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping_str=grouping_str,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def export_feature_importance(
        self, export_info: Export.ExportInfo, artifact_containers, class_labels,
        num_records, aggregation_type
    ):
        export_data = self.diagnostics.get_feature_importance(
            artifact_containers, class_labels, num_records, aggregation_type
        )
        return self._export(export_data, export_info, artifact_containers[0])

    @viz_callback
    def export_overfitting_diagnostic(
        self,
        export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0
    ):
        export_data = self.diagnostics.detect_overfitting(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def overfitting_diagnostic_table(
        self,
        artifacts_container: ArtifactsContainer,
        compare_artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0
    ):
        overfitting_df = self.diagnostics.detect_overfitting(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep
        )
        if compare_artifacts_container is not None:
            overfitting_df_compare = self.diagnostics.detect_overfitting(
                compare_artifacts_container,
                num_records,
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=qoi,
                qoi_timestep=qoi_timestep
            )
            overfitting_df = overfitting_df.merge(
                overfitting_df_compare, on='Feature', suffixes=('', '_compare')
            )
        overfitting_df = overfitting_df.sort_values(
            by='Overfitting Score', ascending=False
        )
        table_headers = ['Feature', 'Overfitting Score']
        table_rows = []
        for i, row in overfitting_df.iterrows():
            quotified_feature = quote(row['Feature'])
            feature_name = html.Span(
                [
                    dbc.Button(
                        href=
                        f'{self.href_path}features?highlight=overfitting#{quotified_feature}',
                        color="link",
                        className="fa fa-external-link-alt fa-sm",
                        style={'color': Colors.TRUERA_GREEN}
                    ),
                    row['Feature'],
                ]
            )
            score_children = [
                dbc.Row(
                    [
                        html.P(
                            "{:.4f}".format(row['Overfitting Score']),
                            style={'padding': '5px'}
                        ),
                        self.get_simple_hbar_chart(
                            [row['Overfitting Score']], [Colors.TRUERA_GREEN],
                            min_val=0,
                            max_val=1,
                            display_text=False,
                            width=100
                        )
                    ]
                )
            ]
            if compare_artifacts_container is not None:
                score_children.append(
                    dbc.Row(
                        [
                            html.P(
                                "{:.4f}".format(
                                    row['Overfitting Score_compare']
                                ),
                                style={'padding': '5px'}
                            ),
                            self.get_simple_hbar_chart(
                                [row['Overfitting Score_compare']],
                                [Colors.DEFAULT_YELLOW],
                                min_val=0,
                                max_val=1,
                                display_text=False,
                                width=100
                            )
                        ]
                    )
                )
            table_rows.append([feature_name, dbc.Container(score_children)])
        return get_html_table(table_headers, table_rows)

    @viz_callback
    def feature_heatmap_overview(
        self,
        feature,
        artifacts_container: ArtifactsContainer,
        num_records,
        length_thresh=None,
        length_thresh_le=False,
        num_timesteps=None,
        timestep_forward=False,
        filter_mode=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        point_data, fitted_data, names = self.aiq.input_inf_3d_info(
            feature,
            artifacts_container,
            num_records,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            num_timesteps=num_timesteps,
            timestep_forward=timestep_forward,
            filter_mode=filter_mode,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        nonnumeric_feature_map = self.get_nonnumeric_feature_map(
            artifacts_container
        )
        num_timesteps = num_timesteps if isinstance(
            num_timesteps, int
        ) else self.get_total_timesteps(artifacts_container)
        if feature in nonnumeric_feature_map:
            bin_edges = sorted(list(nonnumeric_feature_map[feature].keys()))
        else:
            _, bin_edges = np.histogram(point_data[:, 1], 15)
        bins = np.digitize(point_data[:, 1], bin_edges) - 1
        avg_influences = np.zeros((num_timesteps, len(bin_edges)))
        num_points = np.zeros((num_timesteps, len(bin_edges)))
        for timestep in range(num_timesteps):
            for bin_i in range(len(bin_edges)):
                indices = np.logical_and(
                    point_data[:, 0] == timestep, bins == bin_i
                )
                num_points[timestep, bin_i] = np.sum(indices)
                if np.sum(indices) > 0:
                    avg_influences[timestep,
                                   bin_i] = np.mean(point_data[indices, 2])
        timestep_labels = ['t-{}'.format(i) for i in range(num_timesteps)]
        zmax = np.max(np.abs(avg_influences))
        zmin = -zmax
        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=avg_influences,
                y=timestep_labels,
                x=bin_edges,
                xgap=5,
                ygap=5,
                colorscale=[Colors.SALMON_70, "white", Colors.TRUERA_GREEN],
                zmin=zmin,
                zmax=zmax,
                hovertemplate=
                "<b>Timestep:</b> %{y}<br><b>Feature Value:</b> %{x}<br><b>Average Influence:</b> %{z}<extra></extra>"
            )
        )
        density_heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=num_points,
                y=timestep_labels,
                x=bin_edges,
                xgap=5,
                ygap=5,
                colorscale=["white", Colors.TRUERA_GREEN],
                hovertemplate=
                "<b>Timestep:</b> %{y}<br><b>Feature Value:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
            )
        )
        for fig in [heatmap_fig, density_heatmap_fig]:
            fig.update_layout(
                go.Layout(
                    plot_bgcolor=Colors.BACKGROUND_95,
                    height=25 * len(avg_influences),
                    showlegend=False,
                    yaxis_title='Timestep',
                    xaxis_title='Feature Value',
                    margin=dict(l=0, r=0, t=0, b=0)
                )
            )
            fig.update_xaxes(showgrid=False, zeroline=False)
            fig.update_yaxes(showgrid=False, zeroline=False)
        return dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('Feature Influence'),
                        dcc.Graph(figure=heatmap_fig)
                    ]
                ),
                dbc.Col(
                    [
                        html.H4('Feature Value Density'),
                        dcc.Graph(figure=density_heatmap_fig)
                    ]
                ),
            ]
        )

    @viz_callback
    def temporal_trends_overview(
        self,
        feature,
        artifacts_container: ArtifactsContainer,
        num_records,
        length_thresh=None,
        length_thresh_le=False,
        num_timesteps=None,
        timestep_forward=False,
        filter_mode=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        inf_data, _, _ = self.aiq.input_inf_3d_info(
            feature,
            artifacts_container,
            num_records,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            num_timesteps=num_timesteps,
            timestep_forward=timestep_forward,
            filter_mode=filter_mode,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        num_timesteps = num_timesteps if isinstance(
            num_timesteps, int
        ) else self.get_total_timesteps(artifacts_container)
        fig = make_subplots(
            shared_yaxes=False,
            rows=int(num_timesteps),
            cols=2,
            subplot_titles=[
                'Feature Value Density', 'Feature Influence Density'
            ]
        )
        timestep_row = 0
        all_feature_vals = inf_data[:, 1]
        f_min_x = min(all_feature_vals)
        f_max_x = max(all_feature_vals)

        all_inf_vals = inf_data[:, 2]
        inf_range_min = min(all_inf_vals)
        inf_range_max = max(all_inf_vals)
        for timestep_ix in range(num_timesteps):

            feature_values = inf_data[inf_data[:, 0] == timestep_ix][:, 1]
            inf_values = inf_data[inf_data[:, 0] == timestep_ix][:, 2]

            timestep_row += 1
            fig.add_trace(
                go.Histogram(
                    x=feature_values,
                    histnorm='probability',
                    marker_color=Colors.TRUERA_GREEN,
                    opacity=0.6
                ),
                row=timestep_row,
                col=1
            )
            fig.update_yaxes(
                title_text=f"T-{timestep_ix}", row=timestep_row, col=1
            )
            fig.update_xaxes(
                title_text="",
                range=[f_min_x, f_max_x],
                row=timestep_row,
                col=1
            )
            fig.add_trace(
                go.Violin(
                    x=inf_values,
                    line_color=Colors.TRUERA_GREEN,
                    orientation='h',
                    side='positive'
                ),
                row=timestep_row,
                col=2
            )

            fig.update_yaxes(visible=False, row=timestep_row, col=2)
            fig.update_xaxes(
                title_text="",
                range=[inf_range_min, inf_range_max],
                row=timestep_row,
                col=2
            )

        fig.update_layout(
            showlegend=False, height=num_timesteps * 100, width=1300
        )
        inf_value_col_children = [dcc.Graph(figure=fig)]
        return dbc.Row(
            inf_value_col_children,
            style={
                "height": f"{num_timesteps*100}px",
                "width": "1300px"
            }
        )

    @viz_callback
    def feature_3d_plot(
        self,
        feature,
        artifacts_container: ArtifactsContainer,
        num_records,
        plot_type,
        grouping=None,
        length_thresh=None,
        length_thresh_le=False,
        num_timesteps=None,
        timestep_forward=False,
        filter_mode=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        return_fig=False
    ):
        record_ids = self.aiq.get_record_ids(artifacts_container, num_records)
        if plot_type == "surface":
            grouping = None  # ignore grouping for surface plots
        point_data, fitted_data, grouping_names = self.aiq.input_inf_3d_info(
            feature,
            artifacts_container,
            num_records,
            grouping=grouping,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            num_timesteps=num_timesteps,
            timestep_forward=timestep_forward,
            filter_mode=filter_mode,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        num_timesteps = num_timesteps if isinstance(
            num_timesteps, int
        ) else self.get_total_timesteps(artifacts_container)
        colors = Colors.DEFAULT_COLOR_WHEEL
        if grouping == ModelGrouping.OVERFITTING:
            colors = Colors.BINARY_HIGHLIGHT_COLOR_WHEEL
            grouping_names = [
                {
                    'yes': 'Overfit',
                    'no': None
                }.get(g) for g in grouping_names
            ]
        figs = []
        if plot_type == "scatter":
            for i in range(len(grouping_names)):
                pts = point_data[point_data[:, 3] == i]
                figs.append(
                    go.Scatter3d(
                        x=pts[:, 0],
                        y=pts[:, 1],
                        z=pts[:, 2],
                        mode='markers',
                        marker=dict(size=2, color=colors[i]),
                        name=grouping_names[i],
                        showlegend=(
                            grouping not in [
                                ModelGrouping.NONE, ModelGrouping.OVERFITTING
                            ]
                        ),
                        text=[
                            "Record Index:%d<br>Record ID:%s" %
                            (int(j), str(record_ids[int(j)])) for j in pts[:, 4]
                        ]
                    )
                )
        else:
            fitted_spline_dfs = {}
            for timestep in range(num_timesteps):
                timeslice_point_data = point_data[point_data[:, 0] == timestep]
                if len(timeslice_point_data) == 0:
                    continue
                spline_df = ii_utils.fit(
                    pd.DataFrame(
                        {
                            'infs': timeslice_point_data[:, 2],
                            'vals': timeslice_point_data[:, 1]
                        }
                    ), min(point_data[:, 1]), max(point_data[:, 1])
                )
                if spline_df is not None:
                    fitted_spline_dfs[timestep] = spline_df
                    sampled_feature_values = spline_df['x']

            surface_data = ii_utils.density_surface(
                fitted_spline_dfs, num_timesteps
            )
            figs.append(
                go.Surface(
                    z=surface_data,
                    y=sampled_feature_values,
                    x=[f't-{i}' for i in range(num_timesteps)]
                )
            )
        scatter_or_surface_fig = go.Figure(data=figs)
        if plot_type == "scatter":
            scatter_or_surface_fig.update_layout(
                scene=dict(
                    xaxis=dict(
                        tickprefix='t-', tickvals=np.arange(num_timesteps)
                    ),
                    xaxis_title='Timestep',
                    yaxis_title='Feature Value',
                    zaxis_title='Influence'
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(yanchor="top", xanchor="left", x=0, y=1)
            )
        else:
            scatter_or_surface_fig.update_layout(
                scene=dict(
                    xaxis_title='Timestep',
                    yaxis_title='Feature Value',
                    zaxis_title='Influence'
                ),
                margin=dict(l=0, r=0, t=0, b=0)
            )
        if return_fig:
            return scatter_or_surface_fig
        return dcc.Graph(figure=scatter_or_surface_fig)

    @viz_callback
    def feature_temporal_slice_figures(
        self,
        feature,
        artifacts_container: ArtifactsContainer,
        num_records,
        display_timesteps=None,
        index=None,
        length_thresh=None,
        length_thresh_le=False,
        num_timesteps=None,
        timestep_forward=False,
        filter_mode=None,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5,
        grouping=None,
        filter_list=[],
        artifacts_container_compare: ArtifactsContainer = None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        figsize: Optional[Tuple[int, int]] = None
    ):
        record_ids = self.aiq.get_record_ids(artifacts_container, num_records)
        point_data, fitted_data, names = self.aiq.input_inf_3d_info(
            feature,
            artifacts_container,
            num_records,
            index=index,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            num_timesteps=num_timesteps,
            timestep_forward=timestep_forward,
            filter_mode=filter_mode,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping=grouping,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        nonnumeric_feature_map = self.get_nonnumeric_feature_map(
            artifacts_container
        )
        n_bins = 10
        if display_timesteps is None:
            binned_data = point_data[:, 1]  # grab max from everything
        else:
            binned_data = point_data[point_data[:, 0] == 0
                                    ][:,
                                      1]  # grab max from most recent timestep
        counts, _ = np.histogram(binned_data, bins=n_bins)
        max_count = np.max(counts)
        if display_timesteps is not None:
            point_data = point_data[
                np.isin(point_data[:, 0], display_timesteps)]

        if feature not in nonnumeric_feature_map:
            hist_fig = go.Figure(
                data=[
                    go.Histogram(
                        x=point_data[:, 1],
                        nbinsx=n_bins,  # default to fixed num bins
                        marker_color=Colors.TRUERA_GREEN
                    )
                ]
            )
        else:
            bin_vals = list(nonnumeric_feature_map[feature].keys())
            hist_fig = go.Figure(data=[
                go.Histogram(
                    x=point_data[:, 1],
                    xbins=dict(  # set each categorical value as a unique bin
                        start=np.min(bin_vals),
                        end=np.max(bin_vals) + 1,
                        size=1),
                    marker_color=Colors.TRUERA_GREEN)
            ])
        hist_fig.update_layout(
            xaxis_title='Feature Value',
            yaxis_title='Frequency',
            showlegend=False,
            bargap=0.2,
            paper_bgcolor=Colors.WHITE,
            plot_bgcolor=Colors.WHITE,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        hist_fig.update_yaxes(range=[0, max_count])

        if feature in nonnumeric_feature_map:
            tickvals = np.array(
                list(nonnumeric_feature_map[feature].keys())
            ) + 0.5  # offset to center ticks on bins
            hist_fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=list(nonnumeric_feature_map[feature].values())
                )
            )

        scatter_df = pd.DataFrame()
        scatter_df['infs'] = point_data[:, 2]
        scatter_df['vals'] = point_data[:, 1]
        scatter_df['group'] = point_data[:, 3]
        scatter_df['indices'] = np.array(point_data[:, 4], dtype=int)
        scatter_df['record_id'] = scatter_df['indices'].apply(
            lambda i: record_ids[i]
        )
        if figsize is not None:
            hist_fig.update_layout(width=int(figsize[0]), height=figsize[1])

        inf_fig = self.create_input_influence_2d_figure(
            scatter_df,
            None,
            np.unique(scatter_df['group']),
            ModelGrouping.NONE,
            feature,
            None,
            include_title=False,
            figsize=figsize
        )
        return dbc.Row([dbc.Col(inf_fig), dbc.Col(dcc.Graph(figure=hist_fig))])

    def _export(
        self, obj, export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer
    ):
        artifact_locator = artifacts_container.locator
        export_locator = Locator.Export(
            artifact_locator.project, artifact_locator.model,
            artifact_locator.data_collection, artifact_locator.split,
            export_info.filename
        )
        return Export.export_pkl(
            artifacts_container.cache_client.config, obj, export_info,
            export_locator
        )

    @viz_callback
    def export_important_feature_timesteps(
        self,
        export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer,
        num_records,
        sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        export_data = self.aiq.feature_timesteps_export_info(
            artifacts_container,
            num_records,
            sort=sort,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def export_global_influences(
        self,
        export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer,
        num_records,
        sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        export_data = self.aiq.global_influence_info(
            artifacts_container,
            num_records,
            top_n=None,
            sort=sort,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            swap_compare_filter=swap_compare_filter,
            aggregate_only=True
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def export_local_influences(
        self,
        export_info: Export.ExportInfo,
        artifacts_container: ArtifactsContainer,
        num_records,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        export_data = self.aiq.local_influences_export_info(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def global_influence_graph(
        self,
        top_n,
        artifacts_container: ArtifactsContainer,
        num_records,
        view_type: GlobalExplanationView = GlobalExplanationView.
        INFLUENCE_DISTRIBUTION,
        sort: InfluenceAggregationMethod = InfluenceAggregationMethod.MEAN_ABS,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        grouping=None,
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value,
        compare_qoi=None,
        compare_qoi_timestep=0
    ):
        feature_names = self.get_feature_names(
            artifacts_container, internal=(from_layer == 'internal')
        )
        feature_descs = feature_names[:
                                     ] if from_layer == 'internal' else self.aiq.get_formatted_feature_descriptions(
                                         artifacts_container, feature_names
                                     )
        seq_df, agg_seq = self.aiq.global_influence_info(
            artifacts_container,
            num_records,
            top_n=top_n,
            sort=sort,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            swap_compare_filter=swap_compare_filter,
            return_agg_seq=True,
            aggregate_only=False
        )
        if compare_qoi is not None:
            seq_df_compare, agg_seq_compare = self.aiq.global_influence_info(
                artifacts_container,
                num_records,
                top_n=len(feature_names),
                sort=sort,
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=compare_qoi,
                from_layer=from_layer,
                qoi_timestep=compare_qoi_timestep,
                pred_thresh=pred_thresh,
                filter_list=filter_list,
                artifacts_container_compare=artifacts_container_compare,
                swap_compare_filter=swap_compare_filter,
                return_agg_seq=True,
                aggregate_only=False
            )

        if from_layer == 'input':
            data = self.aiq.get_data(artifacts_container, num_records)
            lengths = self.aiq.get_lengths(artifacts_container, num_records)
            data_flattened = np.concatenate(
                [d[:l] for l, d in zip(lengths, data)], axis=0
            )
            nonnumeric_feature_map = self.get_nonnumeric_feature_map(
                artifacts_container
            )

        if view_type == GlobalExplanationView.INFLUENCE_SENSITIVITY_PLOTS:
            return self.input_inf_2d_figures(
                artifacts_container,
                num_records,
                np.argsort(agg_seq)[::-1][:top_n],
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=qoi,
                qoi_timestep=qoi_timestep,
                compare_qoi=compare_qoi,
                compare_qoi_timestep=compare_qoi_timestep,
                pred_thresh=pred_thresh,
                grouping=grouping
            )

        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=8,
            ),
            height=100,
            width=600,
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        table_headers = table_headers = ["Feature", "Rank", "Importance"]
        table_headers.append(view_type.value)

        seq_df = seq_df.reindex(
            index=seq_df.index[::-1]
        )  # reindex so that top feature is first
        table_rows = []
        rank = 0
        inf_fig_min = np.min(seq_df.values)
        inf_fig_max = np.max(seq_df.values)
        eps = 0.3 * (
            inf_fig_max - inf_fig_min
        )  # add margin to graphs to show tails
        if compare_qoi is not None:
            compare_qoi_ranks = np.argsort(agg_seq_compare)[::-1]

        for seq_index, seq in seq_df.iterrows():
            importance = "{:0.3f}".format(agg_seq[seq_index])
            rank_str = html.Div(
                [html.Span("⬤ ", style={'color': Colors.TRUERA_GREEN}), rank]
            )
            if compare_qoi is not None:
                rank_str = html.Div(
                    [
                        rank_str,
                        html.Div(
                            [
                                html.Span(
                                    "⬤ ",
                                    style={'color': Colors.DEFAULT_ORANGE}
                                ),
                                np.where(compare_qoi_ranks == seq_index)[0][0]
                            ]
                        )
                    ]
                )
            quotify_feature_name = quote(feature_names[seq_index])
            feature = html.Div(
                [
                    html.Strong(feature_names[seq_index]),
                    dbc.Button(
                        href=f'{self.href_path}features#{quotify_feature_name}',
                        color="link",
                        className="fa fa-external-link-alt fa-sm",
                        style={'color': Colors.TRUERA_GREEN}
                    ),
                    html.P(feature_descs[seq_index])
                ]
            )
            inf_fig = go.Figure(
                data=go.Violin(
                    x=seq.values,
                    line_color=Colors.TRUERA_GREEN,
                    box_visible=False,
                    meanline_visible=False,
                    side='positive',
                    points=False,
                    name=""
                ),
                layout=layout
            )
            inf_fig.update_xaxes(range=[inf_fig_min - eps, inf_fig_max + eps])
            if compare_qoi is not None:
                inf_fig.add_trace(
                    go.Violin(
                        x=seq_df_compare.loc[seq_index].values,
                        line_color=Colors.DEFAULT_ORANGE,
                        box_visible=False,
                        meanline_visible=False,
                        side='positive',
                        points=False,
                        name=""
                    )
                )
            if view_type == GlobalExplanationView.INFLUENCE_DISTRIBUTION:
                table_rows.append(
                    [
                        feature, rank_str, importance,
                        dcc.Graph(
                            figure=inf_fig, config={'displayModeBar': False}
                        )
                    ]
                )
            else:
                feature_values = data_flattened[:, seq_index]
                if feature_names[seq_index] in nonnumeric_feature_map:
                    feature_values = [
                        nonnumeric_feature_map[feature_names[seq_index]][f]
                        for f in feature_values
                    ]
                value_fig = go.Figure(
                    data=go.Histogram(
                        x=feature_values,
                        histnorm='probability',
                        marker_color=Colors.TRUERA_GREEN
                    ),
                    layout=layout
                )
                value_fig.update_layout(
                    {'yaxis': {
                        'showgrid': False,
                        'visible': False
                    }}
                )
                value_fig.update_layout(bargap=0.1)
                table_rows.append(
                    [
                        feature, rank_str, importance,
                        dcc.Graph(
                            figure=value_fig, config={'displayModeBar': False}
                        )
                    ]
                )
            rank += 1
        return get_html_table(table_headers, table_rows)

    def _internal_viz(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        labels=None,
        grouping=None,
        marker_opts={},
        qoi_core_class=0,
        qoi='average',
        from_layer='internal',
        algorithm='tsne'
    ):

        fig = go.Figure()
        opts = dict(mode='markers', marker=dict(**marker_opts))
        record_ids = self.aiq.get_record_ids(artifacts_container, num_records)
        influences_reduced = self.aiq.get_influences_reduced(
            artifacts_container,
            num_records,
            qoi_core_class=qoi_core_class,
            qoi=qoi,
            from_layer=from_layer,
            algorithm=algorithm
        )

        dims = influences_reduced.shape[1]
        if (dims != 2 and dims != 3):
            # We can only visualize 2d and 3d
            return fig
        if grouping is not None:
            grp_cnt = 0
            for group in set(grouping.tolist()):
                selector = np.where(grouping == group)[0]

                items = influences_reduced[selector, :]
                if labels is not None:
                    opts['text'] = [
                        "Record Index:%d<br>ID:%s" % (j, str(record_ids[j]))
                        for j in selector
                    ]
                if dims == 2:
                    fig.add_trace(
                        go.Scattergl(
                            x=items[:, 0],
                            y=items[:, 1],
                            name=str(labels[group]),
                            **opts
                        )
                    )
                elif dims == 3:
                    opts = dict(mode='markers', marker=dict(size=2))
                    opts['text'] = [
                        "Record Index:%d<br>ID:%s" % (j, str(record_ids[j]))
                        for j in selector
                    ]
                    fig.add_scatter3d(
                        x=items[:, 0],
                        y=items[:, 1],
                        z=items[:, 2],
                        name=labels[group],
                        **opts
                    )
                else:
                    pass
                grp_cnt += 1
        else:
            if dims == 2:
                if labels is not None:
                    fig.add_trace(
                        go.Scatter(
                            x=influences_reduced[:, 0],
                            y=influences_reduced[:, 1],
                            marker=dict(
                                cmax=1,
                                cmin=0,
                                color=labels,
                                colorbar=dict(title="Colorbar"),
                                colorscale="Viridis"
                            ),
                            mode="markers"
                        )
                    )
                else:
                    fig.add_scatter(
                        influences_reduced[:, 0],
                        y=influences_reduced[:, 1],
                        **opts
                    )
        return fig

    def fig_internal_viz(
        self,
        grouping_str,
        artifacts_container: ArtifactsContainer,
        num_records,
        threshold=0.5,
        qoi_core_class=0,
        qoi='average',
        from_layer='internal',
        algorithm='tsne'
    ):

        if qoi == 'average':
            preds = (
                np.mean(
                    self.aiq.get_predictions(
                        artifacts_container,
                        num_records,
                        class_index=qoi_core_class
                    ), 1
                ) > threshold
            )
            labels = (
                np.mean(
                    self.aiq.get_ground_truth(
                        artifacts_container,
                        num_records,
                        class_index=qoi_core_class
                    ), 1
                ) > threshold
            )
        elif qoi == 'last':
            preds = (
                self.aiq.get_predictions_last(
                    artifacts_container,
                    num_records,
                    class_index=qoi_core_class
                ) > threshold
            )
            labels = (
                self.aiq.get_ground_truth_last(
                    artifacts_container,
                    num_records,
                    class_index=qoi_core_class
                ) > threshold
            )
        else:
            raise Exception('Precalculations for this qoi were not generated')
        if grouping_str == 'prediction':
            return self._internal_viz(
                artifacts_container,
                num_records,
                labels={
                    0: '<= threshold',
                    1: '> threshold'
                },
                grouping=preds,
                qoi_core_class=qoi_core_class,
                qoi=qoi,
                from_layer=from_layer,
                algorithm=algorithm
            )
        elif grouping_str == 'ground_truth':
            return self._internal_viz(
                artifacts_container,
                num_records,
                labels={
                    0: '<= threshold',
                    1: '> threshold'
                },
                grouping=labels,
                qoi_core_class=qoi_core_class,
                qoi=qoi,
                from_layer=from_layer,
                algorithm=algorithm
            )
        elif grouping_str == 'both':
            grouping = np.array(
                [
                    str(int(p)) + " " + str(int(l))
                    for p, l in zip(preds, labels)
                ]
            )
            return self._internal_viz(
                artifacts_container,
                num_records,
                labels={
                    "0 0": "true negative",
                    "0 1": "false negative",
                    "1 0": "false positive",
                    "1 1": "true positive"
                },
                grouping=grouping,
                qoi_core_class=qoi_core_class,
                qoi_compare_class=qoi_compare_class,
                qoi=qoi,
                qoi_timestep=qoi_timestep,
                from_layer=from_layer,
                algorithm=algorithm
            )

    @viz_callback
    def figure_fnc(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        internal_quantile=0.9,
        output_quantile=0.9,
        sort=0,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5
    ):

        # NOTE: input to internal influence is filtered based on absolute magnitude of influence
        feature_names = self.get_feature_names(artifacts_container)
        outer_influences, sample_filter, _, _, _ = self.aiq.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            pred_thresh=pred_thresh,
            from_layer='internal',
            qoi_timestep=qoi_timestep
        )

        if sample_filter is not None:
            outer_influences = np.array(
                [a for f, a in zip(sample_filter, outer_influences) if f]
            )

        inner_influences, _, _, _, _ = self.aiq.get_influences_from_qoi(
            artifacts_container,
            num_records,
            qoi_core_class,
            qoi_compare_class,
            qoi,
            pred_thresh=pred_thresh,
            neuron=-1,
            qoi_timestep=qoi_timestep
        )

        feature_to_neuron = inner_influences.sum(0).T.sum(-1)
        neuron_to_qoi = np.expand_dims(outer_influences.sum(0), -1).sum(0)
        f_size = np.abs(feature_to_neuron.sum(0))
        n_size = neuron_to_qoi.sum(1)

        if not sort:
            n_threshold = np.quantile(n_size, output_quantile)
            n_trimmed = np.where(n_size >= n_threshold)[0]
        else:
            n_threshold = np.quantile(n_size, 1.0 - output_quantile)
            n_trimmed = np.where(n_size <= n_threshold)[0]

        f_threshold = np.quantile(f_size, internal_quantile)
        f_trimmed = np.where(f_size >= f_threshold)[0]

        feature_to_neuron_trimmed = feature_to_neuron[n_trimmed, :][:,
                                                                    f_trimmed]
        neuron_to_qoi_trimmed = neuron_to_qoi[n_trimmed, :]

        n_neuron = len(n_trimmed)
        n_qoi = 1
        n_feature = len(f_trimmed)

        node_x = np.hstack(
            (
                np.linspace(0.4, 0.8,
                            n_feature), np.linspace(0.4, 0.8, n_neuron), (0.5)
            )
        )
        node_y = np.hstack(
            (
                np.ones(n_feature) * 0.1, np.ones(n_neuron) * 0.4,
                np.ones(n_qoi) * 0.8
            )
        )
        node_text = self.get_concatenated_feature_descriptions(
            artifacts_container, [feature_names[f] for f in f_trimmed]
        ) + list(n_trimmed) + ["out"]

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text
        )

        edge_feature_to_neuron_x = [
            (x1, x2)
            for x1 in node_x[:n_feature]
            for x2 in node_x[n_feature:n_feature + n_neuron]
        ]
        edge_feature_to_neuron_y = [
            (y1, y2)
            for y1 in node_y[:n_feature]
            for y2 in node_y[n_feature:n_feature + n_neuron]
        ]
        edge_neuron_to_qoi_x = [
            (x1, x2)
            for x1 in node_x[n_feature:n_feature + n_neuron]
            for x2 in node_x[n_feature + n_neuron:]
        ]
        edge_neuron_to_qoi_y = [
            (y1, y2)
            for y1 in node_y[n_feature:n_feature + n_neuron]
            for y2 in node_y[n_feature + n_neuron:]
        ]
        edge_x = edge_feature_to_neuron_x + edge_neuron_to_qoi_x
        edge_y = edge_feature_to_neuron_y + edge_neuron_to_qoi_y
        width_trimmed = np.hstack(
            (
                nml(np.abs(feature_to_neuron_trimmed.T.flatten()), 0) * 5,
                nml(neuron_to_qoi_trimmed.flatten(), sort) * 5
            )
        )

        indices_to_show = np.where(
            width_trimmed > np.quantile(width_trimmed, 0.9)
        )[0]
        node_trace['marker']['size'] = np.hstack(
            (nml(f_size[f_trimmed], sort), nml(n_size[n_trimmed], sort), 1)
        ) * 50
        edge_trace = [
            go.Scattergl(
                x=edge_x[i],
                y=edge_y[i],
                line=dict(width=width_trimmed[i], color='#888'),
                hoverinfo='none',
                mode='lines'
            ) for i in indices_to_show
        ]
        fig = go.Figure(
            data=[node_trace] + edge_trace,
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                xaxis=dict(
                    showgrid=False, zeroline=False, showticklabels=False
                )
            )
        )
        fig.update_layout(
            autosize=False,
            width=1000,
            height=500,
            yaxis=go.layout.YAxis(
                ticktext=["Features", "Neurons", "Output"],
                tickvals=[0.1, .4, .8],
                tickmode="array",
                titlefont=dict(size=30),
                showgrid=False,
                zeroline=False
            )
        )
        return fig

    @viz_callback
    def figure_internal_neuron_heatmap(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        infl_aggr='var',
        qoi='last',
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        neuron_importance = self.aiq.internal_neuron_heatmap_info(
            artifacts_container,
            num_records,
            infl_aggr=infl_aggr,
            qoi=qoi,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )
        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=neuron_importance,
                x=[
                    'Neuron {}'.format(i)
                    for i in range(neuron_importance.shape[1])
                ],
                y=['t-{}'.format(i) for i in range(neuron_importance.shape[0])
                  ][::-1],  # attributions returned in reverse order
                colorscale="Magma",
            )
        )
        return heatmap_fig

    @viz_callback
    def export_internal_neuron_heatmap(
        self,
        export_info,
        artifacts_container: ArtifactsContainer,
        num_records,
        infl_aggr='var',
        qoi='last',
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi_timestep=0,
        pred_thresh=0.5
    ):
        export_data = self.aiq.internal_neuron_heatmap_export_info(
            artifacts_container,
            num_records,
            infl_aggr=infl_aggr,
            qoi=qoi,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )
        return self._export(export_data, export_info, artifacts_container)

    @viz_callback
    def figure_correlation(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        feature_space=FeatureSpace.INPUT,
        correlate_along=InteractAlong.FEATURE_DIM,
        interaction_type=InteractionType.CORRELATION,
        threshold=0,
        max_num_features=8,
        mode=SortingMode.MANUAL,
        list_features_for_atc=[],
        temporal_aggr=AggregationMethod.L1,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        qoi_timestep=0,
        pred_thresh=0.5
    ):

        ## Figure 1: Correlation in the input space
        # 1. Compute Emprical Covariance matrix
        # 2. Normalize to get correlation matrix
        # 3. Make the correlation matrix PSD to get its inverse for partial correaltion matrix
        corr, feature_names, features, feature_importance = self.aiq.feature_correlation_info(
            artifacts_container,
            num_records,
            feature_space=feature_space,
            correlate_along=correlate_along,
            temporal_aggr=temporal_aggr,
            interaction_type=interaction_type,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )

        if interaction_type != InteractionType.AUTO_CORRELATION.value:
            ## Thresholding the correlation
            t = np.percentile(abs(corr).flatten(), int(threshold * 100))
            corr = np.where(abs(corr) > t, abs(corr), 0.0)
            ## Heatmap Figure
            fig_heatmap = go.Figure(
                data=go.Heatmap(
                    z=corr,
                    x=feature_names,
                    y=feature_names,
                    colorscale="Magma"
                )
            )
            ## Configuration
            fig_heatmap.update_layout(autosize=False, width=800, height=600)
            R_threshold = corr
        else:
            if mode != SortingMode.MANUAL.value:
                data_var = np.var(np.mean(features, axis=1), axis=0)
                list_features_for_atc = np.argsort(data_var)
                if mode == SortingMode.VAR_ASCENDING.value:
                    list_features_for_atc = list_features_for_atc[:
                                                                  max_num_features
                                                                 ]
                elif mode == SortingMode.VAR_DESCENDING.value:
                    list_features_for_atc = list_features_for_atc[::-1
                                                                 ][:
                                                                   max_num_features
                                                                  ]
                else:
                    raise ValueError("Not a supported mode")

            ## Select the first feature by default
            if isinstance(list_features_for_atc, str):
                list_features_for_atc = [0]

            if not isinstance(list_features_for_atc, list):
                list_features_for_atc = list(list_features_for_atc)

            if len(list_features_for_atc) < 1:
                list_features_for_atc = [0]

            feature_names = self.get_feature_names(artifacts_container)
            time_steps = np.arange(num_timesteps)

            fig_heatmap = go.Figure()
            tick_val = 0
            for i in list_features_for_atc:
                name = feature_names[i]
                fig_heatmap.add_trace(
                    go.Scatter3d(
                        x=time_steps,
                        y=[tick_val] * len(time_steps),
                        z=corr[i],
                        mode='lines+markers',
                        name=name,
                        line=dict(width=6),
                        marker=dict(size=4)
                    )
                )
                tick_val += 1

            fig_heatmap.update_layout(
                scene=dict(
                    xaxis_title='Timestep from Last State',
                    yaxis_title='Feature ID',
                    zaxis_title='AC Values',
                    yaxis=dict(
                        ticktext=[
                            feature_names[i] for i in list_features_for_atc
                        ],
                        tickvals=[i for i in range(max_num_features)]
                    )
                ),
                width=1000,
                margin=dict(r=20, b=10, l=10, t=10),
                scene_aspectratio=dict(x=2, y=1, z=0.8)
            )

            camera = dict(eye=dict(x=2, y=-1.5, z=0.4))
            fig_heatmap.update_layout(scene_camera=camera)
            return fig_heatmap, {'data': []}

        ## Correlation network
        edge_x, edge_y, node_x, node_y, weight, node_adj = ii_utils.undirectional_graph(
            R_threshold, 1.0
        )
        traces = []

        for i in range(len(weight)):
            traces.append(
                go.Scatter(
                    x=[edge_x[i][0], edge_x[i][1], edge_x[i][2]],
                    y=[edge_y[i][0], edge_y[i][1], edge_y[i][2]],
                    line=dict(width=weight[i], color='gray'),
                    hoverinfo='none',
                    mode='lines',
                )
            )

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='none',
            textposition="top center",
            text=feature_names,
            marker=dict(
                showscale=True,
                colorscale='ylgnbu',
                reversescale=True,
                color=[],
                size=10 * (0.3 + feature_importance),
                colorbar=dict(
                    thickness=15,
                    title='Interaction Intensity',
                    xanchor='left',
                    titleside='right',
                ),
                line_width=2,
            ),
        )
        node_trace.marker.color = node_adj
        traces.append(node_trace)

        fig_network = go.Figure(
            data=traces,
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="..",
                        showarrow=False,
                        xref="paper",
                        yref='paper',
                        x=0.005,
                        y=-0.002
                    )
                ],
                width=1000,
                xaxis=dict(
                    showgrid=False, zeroline=False, showticklabels=False
                ),
                yaxis=dict(
                    showgrid=False, zeroline=False, showticklabels=False
                )
            )
        )

        return fig_heatmap, fig_network

    def get_class_distribution_hbar_chart(
        self, below_thresh, above_thresh, color
    ):
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            width=550,
            height=30,
            barmode='relative',
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        fig = go.Figure(layout=layout)
        fig.add_trace(
            go.Bar(
                y=['_'],
                x=[-below_thresh],
                orientation='h',
                showlegend=False,
                hoverinfo='skip',
                marker=dict(color=color)
            )
        )
        fig.add_trace(
            go.Bar(
                y=['_'],
                x=[below_thresh - 1],
                orientation='h',
                showlegend=False,
                hoverinfo='skip',
                marker=dict(color=Colors.BACKGROUND_95)
            )
        )
        fig.add_trace(
            go.Bar(
                y=['_'],
                x=[above_thresh],
                orientation='h',
                showlegend=False,
                hoverinfo='skip',
                marker=dict(color=color)
            )
        )
        fig.add_trace(
            go.Bar(
                y=['_'],
                x=[1 - above_thresh],
                orientation='h',
                showlegend=False,
                hoverinfo='skip',
                marker=dict(color=Colors.BACKGROUND_95)
            )
        )
        fig.update_xaxes(
            zeroline=True,
            showticklabels=False,
            zerolinewidth=2,
            zerolinecolor='black',
            range=[-1, 1]
        )
        fig.update_yaxes(visible=False)
        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    def get_split_badge(self, split_name, split_color):
        return dbc.Badge(
            [html.Span("⬤ ", style={'color': split_color}), split_name],
            pill=True,
            color="light"
        )

    def get_metric_color_array(
        self, artifacts_containers, selected_models, selected_splits
    ):
        color_array = np.empty(
            (len(selected_models), len(selected_splits)), dtype='object'
        )
        if len(selected_models) == 1:
            color_array[0] = Colors.DEFAULT_COLOR_WHEEL[:len(selected_splits)]
            return color_array
        if len(selected_splits) == 1:
            color_array[:,
                        0] = Colors.DEFAULT_COLOR_WHEEL[:len(selected_models)]
            return color_array
        color_array[:] = np.array(Colors.DEFAULT_COLOR_ARRAY
                                 )[:len(selected_models), :len(selected_splits)]
        return color_array

    @viz_callback
    def class_distribution_figure(
        self, artifacts_containers, selected_models, selected_splits,
        num_records, class_name, model_thresholds
    ):
        model_dict, max_num_classes = self.aiq.class_distribution_info(
            artifacts_containers, selected_models, selected_splits, num_records,
            class_name, model_thresholds
        )
        color_array = self.get_metric_color_array(
            artifacts_containers, selected_models, selected_splits
        )
        table_headers = [
            'Model', 'Below threshold', 'Threshold', 'Above threshold'
        ]
        table_rows = []
        for i, model in enumerate(selected_models):
            table_rows.append([html.H6(model), '', '', ''])
            for j, split in enumerate(selected_splits):
                if split not in model_dict[model]:
                    continue
                above_thresh, below_thresh = model_dict[model][split][class_name
                                                                     ]
                color = color_array[i, j]
                fig = self.get_class_distribution_hbar_chart(
                    below_thresh, above_thresh, color
                )
                table_rows.append(
                    [
                        self.get_split_badge(split, color),
                        html.H6("{:.1%}".format(below_thresh)),
                        fig,
                        html.H6("{:.1%}".format(above_thresh)),
                    ]
                )
        return get_html_table(table_headers, table_rows, align_center=True)

    def get_tenure_chart(self, tenure_val_array, colors, min_val=0, max_val=1):
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            width=700,
            height=100,
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        num_timesteps = tenure_val_array.shape[1]
        x = list(range(1, num_timesteps + 1))
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=x,
                    y=tenure_val_array[i],
                    showlegend=False,
                    marker=dict(color=colors[i]),
                    hovertemplate="(Tenure %{x}: %{y})<extra></extra>"
                ) for i in range(len(tenure_val_array))
            ],
            layout=layout
        )
        fig.update_yaxes(visible=False)
        fig.update_xaxes(title_text='Tenure', tick0=0, tickangle=30)
        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    def get_simple_hbar_chart(
        self, vals, colors, min_val=0, max_val=1, display_text=True, width=500
    ):
        labels = list(map(str, range(len(vals))))
        layout = go.Layout(
            plot_bgcolor=Colors.WHITE,
            width=width,
            height=30 * len(vals),
            barmode='stack',
            margin={
                't': 0,
                'l': 0,
                'r': 0,
                'b': 0
            }
        )
        fig = go.Figure(
            go.Bar(
                x=vals,
                y=labels,
                orientation='h',
                showlegend=False,
                text=["{:.2g}".format(v) if display_text else "" for v in vals],
                textposition='inside',
                hovertemplate="%{x}<extra></extra>",
                marker=dict(color=colors)
            ),
            layout=layout
        )

        fig.add_trace(
            go.Bar(
                x=max_val - np.array(vals),
                y=labels,
                orientation='h',
                showlegend=False,
                hoverinfo='skip',
                marker=dict(color=Colors.BACKGROUND_95)
            )
        )
        fig.update_xaxes(
            visible=False, showticklabels=False, range=[min_val, max_val]
        )
        fig.update_yaxes(visible=True, showticklabels=False)
        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    def group_profile_record_visualization(self, data: dict, record_id: str):
        viz_children = [html.H4(f'Record {record_id}')]
        record_data = data['records'][record_id]
        viz_children.extend(
            [
                html.Br(),
                html.Strong("Index: "),
                str(record_data['record_idx']),
            ]
        )
        if 'strong_influence_threshold' in record_data:
            viz_children.extend(
                [
                    html.Br(),
                    html.Strong("Strong Influence Threshold: "),
                    str(record_data['strong_influence_threshold']),
                ]
            )

        if 'global_important_features' in data:
            viz_children.extend(
                [
                    html.Br(),
                    html.Strong("Globally important features: "),
                    ", ".join(data['global_important_features']),
                ]
            )

        viz_children.extend(
            [
                html.Br(),
                html.Strong("Total Mean-Corrected Influence for Record: "),
                f"{record_data['total_influence']:0.3f}",
            ]
        )
        if data['diagnostic'] == 'high_global_influence_concentration':
            table_headers = [
                'Feature Name', 'Total Mean-Corrected Influence', ''
            ]
        else:
            table_headers = [
                'Feature Name', 'Feature Value', 'Top Mean-Corrected Influence',
                ''
            ]
        table_rows = []
        for feature_data in record_data[
            'top_features'][::-1
                           ]:  # reverse order to sort by most inf to least inf
            influence = feature_data['normalized_influences']
            feature_name_entry = [html.Strong(feature_data['feature'])]
            if 'timestep' in feature_data:
                feature_name_entry.extend([" at ", feature_data['timestep']])
            feature_name_cell = html.Div(feature_name_entry)
            influence_graph = html.Div(
                self.get_simple_hbar_chart(
                    [np.abs(influence)], [Colors.TRUERA_GREEN],
                    max_val=np.abs(record_data['total_influence']),
                    display_text=False,
                    width=100
                )
            )
            table_row = [
                feature_name_cell, f"{influence:0.3f}", influence_graph
            ]
            if 'feature_value' in feature_data:
                table_row.insert(1, f"{feature_data['feature_value']:.3f}")
            table_rows.append(table_row)
        viz_children.append(get_html_table(table_headers, table_rows))
        return dbc.Container(viz_children, style={'width': '80%'})

    @viz_callback
    def global_metric_figures(
        self, artifacts_containers, selected_models, selected_splits,
        num_records, class_name, model_thresholds
    ):
        all_stats, length_stats, stats, max_len = self.aiq.global_metric_info(
            artifacts_containers, selected_models, selected_splits, num_records,
            class_name, model_thresholds
        )
        split_container, tenure_container, legend_container = [], [], []
        color_array = self.get_metric_color_array(
            artifacts_containers, selected_models, selected_splits
        )
        num_timesteps = length_stats.shape[2]
        for stat_i, stat_name in enumerate(stats):
            split_container.append(dbc.Row(html.Strong(stat_name)))
            tenure_container.append(dbc.Row(html.Strong(stat_name)))
            split_container.append(
                dbc.Row(
                    self.get_simple_hbar_chart(
                        all_stats[..., stat_i].flatten(), color_array.flatten()
                    )
                )
            )
            tenure_container.append(
                dbc.Row(
                    self.get_tenure_chart(
                        length_stats[..., stat_i].reshape(-1, num_timesteps),
                        color_array.flatten()
                    )
                )
            )
        # Add data volume chart to tenure info
        tenure_container.append(dbc.Row(html.Strong("Data Volume")))
        tenure_container.append(
            dbc.Row(
                self.get_tenure_chart(
                    length_stats[..., -1].reshape(-1, num_timesteps),
                    color_array.flatten()
                )
            )
        )
        for i, model in enumerate(selected_models):
            legend_container.append(html.Br())
            legend_container.append(html.H6(model))
            for j, split in enumerate(selected_splits):
                legend_container.append(
                    self.get_split_badge(split, color_array[i, j])
                )
        return [
            dbc.Container(split_container, style={'marginLeft': '40px'}),
            dbc.Container(tenure_container, style={'marginLeft': '40px'}),
            dbc.Container(legend_container)
        ]

    def get_model_thresholds_pct(
        self, artifact_containers, pct, num_records, class_name
    ):
        return self.aiq.get_model_thresholds_pct(
            artifact_containers, pct, num_records, class_name
        )

    @viz_callback
    def ensemble_analysis_table(
        self, artifact_containers, model_names, model_weights, model_thresholds,
        ensemble_threshold, num_records, class_name
    ):
        table_df = self.aiq.ensemble_analysis_info(
            artifact_containers, model_names, model_weights, model_thresholds,
            ensemble_threshold, num_records, class_name
        )
        dash_table = get_dash_table_from_df(table_df, 'ensemble-analysis-table')
        return dash_table

    @viz_callback
    def pairwise_interactions_figures(
        self,
        pairwise_feature1: str,
        pairwise_feature2: str,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        timestep_feature1: str = 'all',
        timestep_feature2: str = 'all',
        qoi_core_class: int = 0,
        qoi_compare_class: int = 0,
        qoi: str = 'average',
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        grouping_str: str = None,
        remove_univariate: bool = False
    ) -> Tuple[go.Figure, str]:
        """The Visualization plots of pairwise interactions

        Args:
            pairwise_feature1 (str): The name of the first feature to pair
            pairwise_feature2 (str): The name of the second feature to pair
            artifacts_container (ArtifactsContainer): The artifact metadata
            num_records (int): the number of records to plot
            timestep_feature1 (str, optional): The timestep of feature 1. Defaults to 'all'.
            timestep_feature2 (str, optional): The timestep of feature 2. Defaults to 'all'.
            qoi_core_class (int, optional): The qoi class. Defaults to 0.
            qoi_compare_class (int, optional): If doing compare qoi, the compare class. Defaults to 0.
            qoi (str, optional): The qoi type. Defaults to 'average'.
            qoi_timestep (int, optional): If qoi is timestep qoi, this is the timestep designation. Defaults to 0.
            pred_thresh (float, optional): The prediction threshold. used for grouping and qoi. Defaults to 0.5.
            grouping_str (str, optional): The group type. Defaults to None.
            remove_univariate (bool, optional): An option to remove univariate interactions from the plot. Defaults to False.

        Returns:
            Tuple[go.Figure, str]: The figure and a string representing an interaction polynomial.
        """
        if pairwise_feature1 is None or pairwise_feature2 is None:
            return go.Figure(data=[])

        point_data, names = self.aiq.pairwise_interactions_info(
            pairwise_feature1,
            pairwise_feature2,
            artifacts_container,
            num_records,
            timestep_feature1=timestep_feature1,
            timestep_feature2=timestep_feature2,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping_str=grouping_str
        )

        record_ids = self.aiq.get_record_ids(artifacts_container, num_records)
        figs = []

        X = point_data[:, 0]
        Y = point_data[:, 1]
        Z = point_data[:, 2]

        A = np.array(
            [
                X * 0 + 1, X, Y, X * Y, X**2, Y**2, X**2 * Y, X * Y**2,
                X**2 * Y**2
            ]
        ).T
        B = Z.flatten()
        coeff, r, rank, s = np.linalg.lstsq(A, B)
        multivariates_coeff = np.array(
            [
                coeff[3],
                coeff[6],
                coeff[7],
                coeff[8],
            ]
        )
        univariate_coeff = np.array(
            [coeff[0], coeff[1], coeff[2], coeff[4], coeff[5]]
        )
        if remove_univariate:
            pairwise_poly_interaction_str = f"Feature interaction polynomial: \n%.2g XY + \n%.2g X\u00b2Y + %.2g XY\u00b2 + %.2g X\u00b2*Y\u00b2" % tuple(
                multivariates_coeff
            )
        else:
            pairwise_poly_interaction_str = f"Feature interaction polynomial: %.2g + %.2g X + %.2g Y + \n%.2g XY + %.2g X\u00b2 + %.2g Y\u00b2 + \n%.2g X\u00b2Y + %.2g XY\u00b2 + %.2g X\u00b2*Y\u00b2" % tuple(
                coeff
            )

        for i in range(len(names)):
            pts = point_data[point_data[:, 3] == i]
            text = [
                "Record Index:{}<br>ID:{}".format(int(j), record_ids[int(j)])
                for j in pts[:, 4]
            ]
            x_pts = pts[:, 0]
            y_pts = pts[:, 1]
            z_pts = pts[:, 2]
            if remove_univariate:
                z_pts = z_pts - coeff[
                    0] - coeff[1] * x_pts - coeff[2] * y_pts - coeff[
                        4] * x_pts * x_pts - coeff[5] * y_pts * y_pts
            figs.append(
                go.Scatter3d(
                    x=x_pts,
                    y=y_pts,
                    z=z_pts,
                    mode='markers',
                    marker=dict(size=2),
                    name=names[i],
                    text=text
                )
            )

        scatter_fig = go.Figure(data=figs)
        scatter_fig.update_layout(
            scene=dict(
                xaxis_title=f'Feature Value: {pairwise_feature1}',
                yaxis_title=f'Feature Value: {pairwise_feature2}',
                zaxis_title=f'Summed Influence'
            ),
            width=700,
            margin=dict(r=20, b=10, l=10, t=10)
        )

        x_axis = np.linspace(min(X), max(X), 50)
        y_axis = np.linspace(min(Y), max(Y), 50)
        z_surface = []

        for x_val in x_axis:
            z_surface_vals = []
            z_surface.append(z_surface_vals)
            for y_val in y_axis:
                if remove_univariate:
                    poly_components = np.array(
                        [
                            x_val * y_val, x_val**2 * y_val, x_val * y_val**2,
                            x_val**2 * y_val**2
                        ]
                    )
                    z_val = np.dot(poly_components, multivariates_coeff)
                else:
                    poly_components = np.array(
                        [
                            1, x_val, y_val, x_val * y_val, x_val**2, y_val**2,
                            x_val**2 * y_val, x_val * y_val**2,
                            x_val**2 * y_val**2
                        ]
                    )
                    z_val = np.dot(poly_components, coeff)
                z_surface_vals.append(z_val)

        figs.append(go.Surface(z=np.asarray(z_surface), y=y_axis, x=x_axis))

        surface_fig = go.Figure(data=figs)
        return surface_fig, pairwise_poly_interaction_str

    @viz_callback
    def feature_timestep_bargraph(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        aggregation_method,
        influence_pct_highlight,
        highlight_feature,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        feature_names = self.get_feature_names(artifacts_container)
        df = self.aiq.feature_timesteps_export_info(
            artifacts_container,
            num_records,
            aggregation_method=aggregation_method,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        ).sort_values(by='Importance', ascending=False)
        df['Timestep'] = df['Timestep'].apply(
            lambda x: int(x.replace("t-", ""))
        )
        fig = go.Figure()
        df_groupby = df.groupby('Timestep', sort=True)
        inf_sums_per_timestep = df['Importance'].sum()
        timesteps = sorted(df['Timestep'].unique())
        timesteps = ['t-{}'.format(i) for i in timesteps]
        timesteps.reverse()
        default_line_color = Colors.adjust_opacity(
            Colors.TRUERA_GREEN_RGBA,
            alpha=1.0 if highlight_feature is None else 0.3
        )
        default_fill_color = Colors.adjust_opacity(
            Colors.TRUERA_GREEN_RGBA,
            alpha=0.8 if highlight_feature is None else 0.1
        )
        default_inf_highlight_line_color = Colors.adjust_opacity(
            Colors.TRUERA_RED_RGBA,
            alpha=1.0 if highlight_feature is None else 0.3
        )
        default_inf_highlight_fill_color = Colors.adjust_opacity(
            Colors.TRUERA_RED_RGBA,
            alpha=0.8 if highlight_feature is None else 0.1
        )

        for n in range(df['Feature'].nunique()):
            # grab nth most important feature for each timestep
            df_groupby_n = df_groupby.nth(n).iloc[::-1]
            df_groupby_n['Importance'] /= inf_sums_per_timestep
            df_groupby_n['Importance'] *= 100
            feature_list = df_groupby_n['Feature'].tolist()
            value_list = df_groupby_n['Importance']
            line_color = np.array([default_line_color for v in value_list])
            fill_color = np.array([default_fill_color for v in value_list])
            if influence_pct_highlight is not None and influence_pct_highlight > 0 and influence_pct_highlight < 100:
                line_color[value_list > influence_pct_highlight
                          ] = default_inf_highlight_line_color
                fill_color[value_list > influence_pct_highlight
                          ] = default_inf_highlight_fill_color

            if highlight_feature is not None and highlight_feature in feature_list:
                for feature_index in np.where(
                    np.asarray(feature_list) == highlight_feature
                )[0]:
                    line_color[feature_index] = Colors.adjust_opacity(
                        tuple(line_color[feature_index]), 1.0
                    )
                    fill_color[feature_index] = Colors.adjust_opacity(
                        tuple(fill_color[feature_index]), 0.8
                    )

            line_color = [f'rgba{tuple(c)}' for c in line_color]
            fill_color = [f'rgba{tuple(c)}' for c in fill_color]
            fig.add_trace(
                go.Bar(
                    y=timesteps,
                    x=value_list,
                    width=0.5,
                    customdata=feature_list,
                    orientation='h',
                    hovertemplate=
                    "Feature: %{customdata}<br>Timestep: %{y}<br>Importance: %{x} %<extra></extra>",
                    marker=dict(
                        color=fill_color, line=dict(color=line_color, width=3)
                    )
                )
            )

        fig.update_layout(
            barmode='stack',
            height=60 * len(timesteps),
            width=900,
            showlegend=False,
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(bgcolor=Colors.WHITE),
            margin={
                't': 5,
                'l': 5,
                'r': 0,
                'b': 5
            },
            xaxis=dict(
                showgrid=False,
                showticklabels=True,
                tickmode='array',
                ticktext=['0%', '25%', '50%', '75%', '100%'],
                tickvals=[0, 25, 50, 75, 100]
            )
        )
        fig.update_yaxes(title_text='Timestep')
        fig.update_xaxes(title_text='Importance')
        return fig, df

    @viz_callback
    def export_feature_timestep_table(
        self,
        export_info,
        artifacts_container: ArtifactsContainer,
        num_records,
        aggregation_method,
        qoi_core_class=0,
        qoi_compare_class=0,
        qoi='average',
        from_layer='internal',
        qoi_timestep=0,
        pred_thresh=0.5,
        filter_list=[],
        artifacts_container_compare=None,
        pred_thresh_compare=0.5,
        swap_compare_filter=SwapComparisons.NONE.value
    ):
        feature_names = self.get_feature_names(artifacts_container)
        export_data = self.aiq.feature_timesteps_export_info(
            artifacts_container,
            num_records,
            aggregation_method=aggregation_method,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            filter_list=filter_list,
            artifacts_container_compare=artifacts_container_compare,
            pred_thresh_compare=pred_thresh_compare,
            swap_compare_filter=swap_compare_filter
        )
        return self._export(export_data, export_info, artifacts_container)
