from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import akerbp.mlpet.utilities as utilities


def initialize_figure(
    well_name: str, depth_values: pd.Series, ncols: int, figsize: Tuple[int, int]
) -> go.Figure:
    """
    Initialize plotly function for well profile plot.


    NOTE: When initializing figure, it is important to specify the number of column (ncols).
    This can not be increased after initialization.

    Args:
        well_name (str): wellbore name
        depth_values (list): list of depth values
        ncols (int): number of columns in subplot
        figsize (tuple): figure size (W x H) in pixels

    Returns:
        go.Figure: plotly graph_object Figure with initialized subplot, title and depth ticks in y-axis
    """

    # Make subplot with one row and mulitple columns
    fig = make_subplots(rows=1, cols=ncols, shared_yaxes=True)

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = 180 / figsize[1]

    # Make space to display double x-axes
    xaxis_arr = []
    yaxis_arr = []
    for layout in fig["layout"]:
        if layout[:5] == "xaxis":
            xaxis_arr.append(layout)
        if layout[:5] == "yaxis":
            yaxis_arr.append(layout)
            fig["layout"][layout]["domain"] = [y_offset, 1]

    # Add well name as title
    fig.update_layout(
        height=figsize[1],
        width=figsize[0],
        title={
            "text": f"<b>WELL: {well_name}</b>",
            "y": 0.95,
            "x": 0.42,
            "xanchor": "left",
            "yanchor": "top",
        },
        hoverlabel=dict(font_size=16),
        showlegend=False,
    )

    # Add measure depth label to y axis
    # Add depth ticks to y axis
    fig.update_yaxes(
        title_text="<b>MD</b>", range=[depth_values.max(), depth_values.min()], col=1
    )

    return fig


def binary_transition_depths_fill_gaps(
    df: pd.DataFrame,
    curve_name: str,
    md_column: str,
    binary_numbers: Dict[Any, Dict[str, Any]],
    binary_key: str,
) -> List[Tuple[Any, Any, Any, Any]]:
    """
    Creates a list which contains information about when the binary flags switches
    from one value to another.

    Args:
        df (pd.DataFrame): Dataframe containing binary data.
        curve_name (str): Name of columns in df with binary data.
        md_columns (str): Name of depth curve in df.
        binary_numbers (Dict): Dict of binary mapping information.
        binary_key (str): Key to specific binary information within dict.

    Returns:
        list: Returns a list of tuples of the form (Start depth of new value, End
            depth of the value, Color representing the given value, human readamle name of
            the value).
    """
    mask = (df[curve_name] != df[curve_name].shift()) | (
        df[curve_name] != df[curve_name].shift(-1)
    )
    df2 = df[mask].reset_index().copy()
    df2_shift_forward = df2.shift()
    df2_shift_back = df2.shift(-1)
    df2_shift_2back = df2_shift_back.shift(-1)

    depths_lith_tuple_list = []

    shift_start_half_interval = 0
    for (
        (_, row_nextnext),
        (_, row_next),
        (_, row),
        (_, row_prev),
    ) in zip(  # noqa: ignore
        df2_shift_2back.iterrows(),
        df2_shift_back.iterrows(),
        df2.iterrows(),
        df2_shift_forward.iterrows(),
    ):
        shift_end_half_interval = 0

        if row_prev[curve_name] == row[curve_name]:
            continue
        elif (
            row_prev[curve_name] != row[curve_name]
            and row[curve_name] == row_next[curve_name]
        ):
            # In interval with different start and end point
            if not np.isnan(row_nextnext[md_column]):
                shift_end_half_interval = (
                    row_nextnext[md_column] - row_next[md_column]
                ) / 2

            depths_lith_tuple_list.append(
                (
                    row[md_column] - shift_start_half_interval,
                    row_next[md_column] + shift_end_half_interval,
                    binary_numbers[row[curve_name]]["color"],
                    binary_numbers[row[curve_name]][binary_key],
                )
            )
        else:
            # In interval with same start and endpoint
            if not np.isnan(row_next[md_column]):
                shift_end_half_interval = (row_next[md_column] - row[md_column]) / 2

            depths_lith_tuple_list.append(
                (
                    row[md_column] - shift_start_half_interval,
                    row[md_column] + shift_end_half_interval,
                    binary_numbers[row[curve_name]]["color"],
                    binary_numbers[row[curve_name]][binary_key],
                )
            )

        shift_start_half_interval = shift_end_half_interval
    return depths_lith_tuple_list


def add_LITHOLOGY(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    lithology_prediction_curve_name: str,
    lithology_confidence_curve_name: str,
    md_column: str,
    lithology_numbers: Dict[float, Dict[str, Any]],
    lithology_conf_numbers: Dict[float, Dict[str, Any]],
) -> go.Figure:
    """
    Add LITHOLOGY column and LITHOLOGY confidence to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append LITHOLOGY and LITHOLOGY confidence column
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about LITHOLOGY curve,LITHOLOGY confidence curve and depth
        lithology_prediction_curve_name (str): name of LITHOLOGY curve in dataframe
        lithology_confidence_curve_name (str): name of LITHOLOGY CONFIDENCE curve in dataframe
        md_column (str): name of depth curve in dataframe
        lithology_numbers (Dict[int, Dict[str, Any]]): dictionary with lithology numbers as key with human readable name['lith'] and color['color'] for plot as value
        lithology_conf_numbers (Dict[float, Dict[str, Any]]): dictionary with lithology conf numbers as key with color for plot as value['color']

    Returns:
        go.Figure: passing plotly graph_object Figure with added LITHOLOGY and LITHOLOGY confidence column in subplot
    """

    lithology_pred_transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=lithology_prediction_curve_name,
        md_column=md_column,
        binary_numbers=lithology_numbers,
        binary_key="lith",
    )
    lithology_conf_transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=lithology_confidence_curve_name,
        md_column=md_column,
        binary_numbers=lithology_conf_numbers,
        binary_key="conf",
    )

    left_col_value = -0.2
    right_col_value = 1

    # Plot lithology prediction
    lith_in_legend = []
    for depth_tuple in lithology_pred_transition_depths_list:
        fig.add_trace(
            go.Scatter(
                x=[0, right_col_value],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                showlegend=False,
            ),
            row=1,
            col=i_curve,
        )

        if depth_tuple[3] not in lith_in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[0, right_col_value],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                ),
                row=1,
                col=i_curve,
            )
            lith_in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0, right_col_value],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    showlegend=False,
                ),
                row=1,
                col=i_curve,
            )

    # plot separation line between lithology and conf
    fig.add_trace(
        go.Scatter(
            x=[0] * len(df[md_column]),
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            hoverinfo="none",
        ),
        row=1,
        col=i_curve,
    )

    # Plot lithology confidence
    lith_in_legend = []
    for depth_tuple in lithology_conf_transition_depths_list:
        fig.add_trace(
            go.Scatter(
                x=[left_col_value, 0],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                showlegend=False,
            ),
            row=1,
            col=i_curve,
        )

        if depth_tuple[3] not in lith_in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[left_col_value, 0],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                ),
                row=1,
                col=i_curve,
            )
            lith_in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[left_col_value, 0],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    showlegend=False,
                ),
                row=1,
                col=i_curve,
            )

    fig.update_xaxes(
        title_text=lithology_prediction_curve_name,
        row=1,
        col=i_curve,
        range=[left_col_value, right_col_value],
    )
    return fig


def add_AC(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    # Setting Up plot conventions for AC
    # i_ac = features_to_plot.index("AC")
    left_col_value = 240
    right_col_value = 40
    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="blue"),
            name="AC",
        ),
        row=1,
        col=i_curve,
    )
    fig.update_xaxes(
        title_text="AC",
        range=[left_col_value, right_col_value],
        row=1,
        col=i_curve,
    )
    return fig


def add_RDEP(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    """
    Add RDEP column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append RDEP coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about RDEP curve and depth
        curve_name (str): name of RDEP cruve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added RDEP in subplot
    """

    left_col_value = 0.2
    right_col_value = 200

    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="red"),
            name="RDEP",
        ),
        row=1,
        col=i_curve,
    )

    fig.update_xaxes(
        title_text="RDEP",
        range=[np.log(left_col_value), np.log(right_col_value)],
        type="log",
        row=1,
        col=i_curve,
    )
    return fig


def add_NEU_DEN(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    den_curve_name: str = "DEN",
    neu_curve_name: str = "NEU",
    md_column: str = "DEPTH",
) -> go.Figure:
    """
    Add NEU/DEN column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append NEU/DEN coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about NEU curve, DEN curve and depth
        den_curve_name (str, optional): name of DEN cruve in dataframe. Defaults to "DEN".
        neu_curve_name (str, optional): name of NEU cruve in dataframe. Defaults to "NEU".
        md_column (str, optional): name of depth cruve in dataframe. Defaults to "DEPTH".

    Returns:
        go.Figure: passing plotly graph_object Figure with added NEU/DEN in subplot
    """

    den_left_col_value = 1.95
    den_right_col_value = 2.95

    neu_left_col_value = 0.45
    neu_right_col_value = -0.15

    # Find total number of xaxis in fig json
    ncols = len(
        [
            key
            for key in vars(fig.layout)["_compound_props"].keys()
            if key[:5] == "xaxis"
        ]
    )

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = fig["layout"]["yaxis"]["domain"][0]

    # plot DEN normal
    fig.add_trace(
        go.Scatter(
            x=df[den_curve_name],
            y=df[md_column],
            mode="lines",
            line=dict(color="red"),
            name="DEN",
            # fill="tonexty",
            # fillcolor='green',
        ),
        row=1,
        col=i_curve,
    )

    # plot NEU normal
    fig.add_trace(
        go.Scatter(
            x=df[neu_curve_name],
            y=df[md_column],
            mode="lines",
            line=dict(color="blue"),
            name="NEU",
            # fill="tonextx",
            # fillcolor='yellow',
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )

    # Fill color between DEN and NEU when both are non-nan
    fill_mask = (~df[den_curve_name].isna()) & (~df[neu_curve_name].isna())
    DEN_TO_SCALE = df[den_curve_name].values

    N_den = abs(den_right_col_value - den_left_col_value)
    N_neu = abs(neu_right_col_value - neu_left_col_value)
    df["DEN_ON_NEU_RANGE"] = (
        neu_left_col_value - abs(DEN_TO_SCALE - den_left_col_value) * N_neu / N_den
    )

    # define df for yellow and green fill color.
    den_yellow, den_green = [df.copy() for i in range(2)]
    den_yellow.loc[
        den_yellow.NEU > den_green.DEN_ON_NEU_RANGE, "DEN_ON_NEU_RANGE"
    ] = den_yellow[den_yellow.NEU > den_green.DEN_ON_NEU_RANGE].DEN_ON_NEU_RANGE
    den_green.loc[
        den_green.NEU <= den_yellow.DEN_ON_NEU_RANGE, "DEN_ON_NEU_RANGE"
    ] = den_green[den_green.NEU <= den_yellow.DEN_ON_NEU_RANGE].NEU

    # plot NEU line for colorfill barrier to yellow color
    fig.add_trace(
        go.Scatter(
            x=df.loc[fill_mask, neu_curve_name],
            y=df.loc[fill_mask, md_column],
            mode="lines",
            line=dict(color="blue"),
            name="NEU",
            # fill="tonextx",
            # fillcolor='yellow',
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )

    # plot fill yellow
    fig.add_trace(
        go.Scatter(
            x=den_yellow.loc[fill_mask, "DEN_ON_NEU_RANGE"],
            y=den_yellow.loc[fill_mask, md_column],
            mode="none",
            fill="tonextx",
            fillcolor="yellow",
            # fillcolor='green',
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )

    # plot NEU line for colorfill barrier to green color
    fig.add_trace(
        go.Scatter(
            x=df.loc[fill_mask, neu_curve_name],
            y=df.loc[fill_mask, md_column],
            mode="lines",
            line=dict(color="blue"),
            name="NEU",
            # fill="tonextx",
            # fillcolor='yellow',
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )
    # plot fill green
    fig.add_trace(
        go.Scatter(
            x=den_green.loc[fill_mask, "DEN_ON_NEU_RANGE"],
            y=den_green.loc[fill_mask, md_column],
            mode="none",
            fill="tonextx",
            fillcolor="green",
            # fillcolor='green',
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )

    # apply DEN scale
    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [den_left_col_value, den_right_col_value],
        "tickfont": {"color": "red"},
        "title": {"font": {"color": "red"}, "text": "DEN"},
    }

    # apply NEU scale
    fig["layout"]["xaxis" + str(ncols + 1)] = {
        # "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": y_offset / 2,
        "side": "right",
        "range": [neu_left_col_value, neu_right_col_value],
        "tickfont": {"color": "blue"},
        "title": {"font": {"color": "blue"}, "text": "NEU"},
    }

    return fig


def add_GR(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    """
    Add GR column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append GR coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about GR curve and depth
        curve_name (str): name of GR cruve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added GR in subplot
    """

    left_col_value = 0
    right_col_value = 150
    mask = df[curve_name] >= 75

    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="darkgreen"),
            name="GR",
        ),
        row=1,
        col=i_curve,
    )
    fig.add_trace(
        go.Scatter(
            x=[75] * len(df[md_column]),
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            # fill="tonextx",
            # fillcolor="yellow",
            name="GR/Baseline",
        ),
        row=1,
        col=i_curve,
    )

    df_yellow = df.copy()
    df_yellow["GR_YELLOW_MASK"] = df[curve_name]
    df_yellow.loc[mask, "GR_YELLOW_MASK"] = 75
    fig.add_trace(
        go.Scatter(
            x=df_yellow["GR_YELLOW_MASK"],
            y=df_yellow[md_column],
            mode="lines",
            marker=dict(color="darkgreen"),
            fill="tonextx",
            fillcolor="yellow",
            name="GR",
        ),
        row=1,
        col=i_curve,
    )

    fig.add_trace(
        go.Scatter(
            x=[75] * len(df[md_column]),
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            # fill="tonextx",
            # fillcolor="yellow",
            name="GR/Baseline",
        ),
        row=1,
        col=i_curve,
    )
    df_brown = df.copy()
    df_brown["GR_BROWN_MASK"] = df[curve_name]
    df_brown.loc[~mask, "GR_BROWN_MASK"] = 75
    fig.add_trace(
        go.Scatter(
            x=df_brown["GR_BROWN_MASK"],
            y=df_brown[md_column],
            mode="lines",
            marker=dict(color="darkgreen"),
            fill="tonextx",
            fillcolor="brown",
            name="GR",
        ),
        row=1,
        col=i_curve,
    )
    fig.update_xaxes(
        title_text="GR",
        range=[left_col_value, right_col_value],
        row=1,
        col=i_curve,
    )
    return fig


def add_MUDGAS(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    methane_curve_name: str,
    ethane_curve_name: str,
    propane_curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add MUDGAS (C1, C2, C3) column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append MUDGAS coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about MUDGAS (C1, C2, C3) curve and depth
        methane_curve_name (str): name of C1 curve in dataframe
        ethane_curve_name (str): name of C2 curve in dataframe
        propane_curve_name (str): name of C3 curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added MUDGAS (C1, C2, C3) in subplot
    """

    ncols = len(
        [
            key
            for key in vars(fig.layout)["_compound_props"].keys()
            if key[:5] == "xaxis"
        ]
    )

    mtha_left_col_value = df[methane_curve_name].min()
    mtha_right_col_value = df[methane_curve_name].max()

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = fig["layout"]["yaxis"]["domain"][0]
    fig.add_trace(
        go.Scatter(
            x=df[methane_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="red"),
            name="MTHA",
        ),
        row=1,
        col=i_curve,
    )

    fig.add_trace(
        go.Scatter(
            x=df[ethane_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="green"),
            name="ETHA",
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=df[propane_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="orange"),
            name="PRPA",
            xaxis="x" + str(ncols + 2),
            yaxis="y" + str(i_curve),
        ),
    )

    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [mtha_left_col_value, mtha_right_col_value],
        "tickfont": {"color": "red"},
        "title": {"font": {"color": "red"}, "text": "MTHA"},
    }
    fig["layout"]["xaxis" + str(ncols + 1)] = {
        "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": y_offset / 2,
        "side": "right",
        "tickfont": {"color": "green"},
        "title": {"font": {"color": "green"}, "text": "ETHA"},
    }
    fig["layout"]["xaxis" + str(ncols + 2)] = {
        "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": 0.0,
        "side": "right",
        "tickfont": {"color": "orange"},
        "title": {"font": {"color": "orange"}, "text": "PRPA"},
    }

    return fig


def add_VSH(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    """
    Add VSH column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append VSH coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about VSH curve and depth
        curve_name (str): name of VSH cruve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added VSH in subplot
    """

    left_col_value = 0
    right_col_value = 1

    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="black"),
            name="VSH",
            fill="tozerox",
            fillcolor="darkgreen",
        ),
        row=1,
        col=i_curve,
    )
    fig.update_xaxes(
        title_text="VSH",
        range=[left_col_value, right_col_value],
        row=1,
        col=i_curve,
    )
    return fig


def add_CALI_BS(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    cali_curve_name: str,
    bs_curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add CALI/BS column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append CALI/BS coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about CALI curve, BS curve and depth
        cali_curve_name (str): name of CALI curve in dataframe
        bs_curve_name (str): name of BS curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added CALI/BS in subplot
    """

    # Find total number of xaxis in fig json
    ncols = len(
        [
            key
            for key in vars(fig.layout)["_compound_props"].keys()
            if key[:5] == "xaxis"
        ]
    )

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = fig["layout"]["yaxis"]["domain"][0]

    left_col_value = 6
    right_col_value = 26

    # plot normal CALI
    fig.add_trace(
        go.Scatter(
            x=df[cali_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="darkred"),
            name="CALI",
        ),
        row=1,
        col=i_curve,
    )

    # fill darkred between BS and CALI
    fig.add_trace(
        go.Scatter(
            x=df[bs_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            fill="tonextx",
            fillcolor="darkred",
        ),
        row=1,
        col=i_curve,
    )

    # fill yekki between CALI and BS
    df_darkred = df.copy()
    df_darkred["CALI_YELLOW_MASK"] = df[cali_curve_name]
    mask = df_darkred["CALI_YELLOW_MASK"] <= df_darkred.BS
    df_darkred.loc[~mask, "CALI_YELLOW_MASK"] = df_darkred[~mask].BS

    fig.add_trace(
        go.Scatter(
            x=df_darkred["CALI_YELLOW_MASK"],
            y=df_darkred[md_column],
            mode="lines",
            marker=dict(color="darkred"),
            fill="tonextx",
            fillcolor="yellow",
        ),
        row=1,
        col=i_curve,
    )

    # plot BS normal
    fig.add_trace(
        go.Scatter(
            x=df[bs_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            # fill="tonextx",
            # fillcolor="darkred",
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
            name="BS",
        ),
    )

    # apply CALI scale
    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [left_col_value, right_col_value],
        "tickfont": {"color": "darkred"},
        "title": {"font": {"color": "darkred"}, "text": "CALI"},
    }

    # apply BS scale
    fig["layout"]["xaxis" + str(ncols + 1)] = {
        # "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": y_offset / 2,
        "side": "right",
        "range": [left_col_value, right_col_value],
        "tickfont": {"color": "black"},
        "title": {"font": {"color": "black"}, "text": "BS"},
    }
    return fig


def add_COAL_CALC_flag(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    coal_curve_name: str,
    calc_curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add COAL/CALC flag column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append COAL/CALC flag coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about COAL flag, CALC flag and depth curve
        coal_curve_name (str): name of COAL flag curve in dataframe
        calc_curve_name (str): name of CALC flag curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added COAL/CALC flag in subplot
    """

    # Find total number of xaxis in fig json
    ncols = len(
        [
            key
            for key in vars(fig.layout)["_compound_props"].keys()
            if key[:5] == "xaxis"
        ]
    )

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = fig["layout"]["yaxis"]["domain"][0]

    coal_numbers: Dict[float, Dict[str, str]] = {
        1.0: {"coal": "COAL_FLAG", "color": "black"},
        0.0: {"coal": "COAL_FLAG", "color": "#ffffff"},
    }
    calc_numbers: Dict[float, Dict[str, str]] = {
        1.0: {"calc": "CALC_FLAG", "color": "orange"},
        0.0: {"calc": "CALC_FLAG", "color": "#ffffff"},
    }
    coal_transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=coal_curve_name,
        md_column=md_column,
        binary_numbers=coal_numbers,
        binary_key="coal",
    )
    calc_transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=calc_curve_name,
        md_column=md_column,
        binary_numbers=calc_numbers,
        binary_key="calc",
    )

    # COAL FLAG
    in_legend = []
    for depth_tuple in coal_transition_depths_list:
        if depth_tuple[2] == "#ffffff":
            continue
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                showlegend=False,
            ),
            row=1,
            col=i_curve,
        )

        if depth_tuple[3] not in in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                ),
                row=1,
                col=i_curve,
            )
            in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    showlegend=False,
                ),
                row=1,
                col=i_curve,
            )

    # plot separation line between lithology and conf
    fig.add_trace(
        go.Scatter(
            x=[0] * len(df[md_column]),
            y=df[md_column],
            mode="lines",
            marker=dict(
                color="black",
            ),
            hoverinfo="none",
        ),
        row=1,
        col=i_curve,
    )

    # CALC FLAG
    in_legend = []
    for depth_tuple in calc_transition_depths_list:
        if depth_tuple[2] == "#ffffff":
            continue
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                xaxis="x" + str(ncols + 1),
                yaxis="y" + str(i_curve),
            ),
        )

        if depth_tuple[3] not in in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    xaxis="x" + str(ncols + 1),
                    yaxis="y" + str(i_curve),
                ),
            )
            in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    xaxis="x" + str(ncols + 1),
                    yaxis="y" + str(i_curve),
                ),
            )
    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [-1, 1],
        "tickfont": {"color": "black"},
        "title": {"font": {"color": "black"}, "text": "COAL flag"},
    }

    fig["layout"]["xaxis" + str(ncols + 1)] = {
        "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": y_offset / 2,
        "side": "right",
        "range": [1, -1],
        "tickfont": {"color": "orange"},
        "title": {"font": {"color": "orange"}, "text": "CALC flag"},
    }
    return fig


def add_VSH_flag_filter(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    """
    Add VSH flag filter column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append VSH flag filter coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about VSH flag filter curve and depth
        curve_name (str): name of VSH flag filter curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added VSH flag filter in subplot
    """
    # FIXME:
    # Comment out PAY tops filter - functionality doesn't work optimal. Very slow when calculating dataframe.
    #
    # ncols = len(
    #    [
    #        key
    #        for key in vars(fig.layout)["_compound_props"].keys()
    #        if key[:5] == "xaxis"
    #    ]
    # )
    #
    # Define y-offset as a reference when displaying multiple x-axes
    # y_offset = fig["layout"]["yaxis"]["domain"][0]

    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="red"),
            name="filter_vsh_cutoff",
            fill="tozerox",
        ),
        row=1,
        col=i_curve,
    )
    # fig.add_trace(
    #    go.Scatter(
    #        x=df["filter_payflag_tops"],
    #        y=df[md_column],
    #        mode="lines",
    #        marker=dict(color="green"),
    #        name="filter_payflag_tops",
    #        fill="tozerox",
    #        xaxis="x" + str(ncols + 1),
    #        yaxis="y" + str(i_curve),
    #    ),
    # )
    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [-1, 1],
        "tickfont": {"color": "red"},
        "title": {"font": {"color": "red"}, "text": "VSH pay filter"},
    }

    # fig["layout"]["xaxis" + str(ncols + 1)] = {
    #    "anchor": "free",
    #    "overlaying": "x" + str(i_curve),
    #    "position": y_offset / 2,
    #    "side": "right",
    #    "range": [1, -1],
    #    "tickfont": {"color": "green"},
    #    "title": {"font": {"color": "green"}, "text": "Tops pay filter"},
    # }
    return fig


def add_missedpay_prediction(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    prediction_label: str,
    probability_curve_name: str,
    flag_curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add MissedPay prediction column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append MissedPay prediction coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about MissedPay prediction curve and depth
        prediction_label (str): label name to missed pay prediction column in subplot
        probability_curve_name (str): name of MissedPay prediction curve in dataframe
        flag_curve_name (str): name of MissedPay prediction flag curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added MissedPay prediction in subplot
    """

    # Plot flag pay prediction
    pay_numbers: Dict[float, Dict[str, str]] = {
        1.0: {"PAY_FLAG_ML": flag_curve_name, "color": "#008000"},
        0.0: {"PAY_FLAG_ML": flag_curve_name, "color": "#ffffff"},
    }
    transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=flag_curve_name,
        md_column=md_column,
        binary_numbers=pay_numbers,
        binary_key=flag_curve_name,
    )

    in_legend = []
    for depth_tuple in transition_depths_list:
        if depth_tuple[2] == "#ffffff":
            continue
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                showlegend=False,
            ),
            row=1,
            col=i_curve,
        )

        if depth_tuple[3] not in in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                ),
                row=1,
                col=i_curve,
            )
            in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    showlegend=False,
                ),
                row=1,
                col=i_curve,
            )

    # Plot continous pay prediction
    fig.add_trace(
        go.Scatter(
            x=df[probability_curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="red"),
            name=prediction_label,
        ),
        row=1,
        col=i_curve,
    )

    fig.update_xaxes(
        title_text=prediction_label,
        row=1,
        col=i_curve,
        range=[0.0, 1.0],
    )

    return fig


def add_mud_log_indicator(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    mud_indicator_curve_name: str,
    log_indicator_curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add MUD/LOG indicator column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append MUD/LOG indicator coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about MUD/LOG indicator curve and depth
        mud_indicator_curve_name (str): name of MUD indicator curve in dataframe
        log_indicator_curve_name (str): name of LOG indicator curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added MUD/LOG indicator in subplot
    """

    # Find total number of xaxis in fig json
    ncols = len(
        [
            key
            for key in vars(fig.layout)["_compound_props"].keys()
            if key[:5] == "xaxis"
        ]
    )

    # Define y-offset as a reference when displaying multiple x-axes
    y_offset = fig["layout"]["yaxis"]["domain"][0]

    mud_indicator = df[mud_indicator_curve_name] + 0.05
    log_indicator = df[log_indicator_curve_name] + 0.05
    depth = df[md_column]
    fig.add_trace(
        go.Scatter(
            x=mud_indicator,
            y=depth,
            mode="lines",
            marker=dict(color="blue"),
            name="mud_indicator",
            opacity=0.7,
            fill="tozerox",
        ),
        row=1,
        col=i_curve,
    )
    fig.add_trace(
        go.Scatter(
            x=log_indicator,
            y=depth,
            mode="lines",
            marker=dict(color="red"),
            name="log_indicator",
            opacity=0.7,
            fill="tozerox",
            xaxis="x" + str(ncols + 1),
            yaxis="y" + str(i_curve),
        ),
    )
    fig["layout"]["xaxis" + str(i_curve)] = {
        "anchor": "y" + str(i_curve),
        "domain": fig["layout"]["xaxis" + str(i_curve)]["domain"],
        "range": [-1, 1],
        "tickfont": {"color": "blue"},
        "title": {"font": {"color": "blue"}, "text": "MUD indicator"},
    }

    fig["layout"]["xaxis" + str(ncols + 1)] = {
        "anchor": "free",
        "overlaying": "x" + str(i_curve),
        "position": y_offset / 2,
        "side": "right",
        "range": [1, -1],
        "tickfont": {"color": "red"},
        "title": {"font": {"color": "red"}, "text": "LOG indicator"},
    }
    return fig


def add_formations_and_groups(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    ncols: int,
    id_column: str,
    md_column: str,
    formation_level: str,
    extend_top_lines: bool = False,
    **kwargs,
) -> go.Figure:
    """
    Add FORMATION or GROUP to passing go.Figure object.

    NOTE:
    Since plotly creates figure iterative: if user want to extend top lines across all subplot column,
    one need to call the formation plotting after all other subplot columns are defined properly.
    This does not force the formation/group top column to always be located to the right,
    but has to be called in the end such that all other columns are predefined.

    Args:
        fig (go.Figure): plotly graph_object Figure to append coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about curve to plot and depth
        ncols (int): number of columns in subplot. This number is used to exted top lines across mutilple subplot views.
        id_column (str): wellbore name column in dataframe
        formation_level (str, optional): name of formation tops column in dataframe. E.g. "FORMATION", "GROUP".
        formation_tops_mapper (Dict[str, Dict[str, Any]], optional): formation tops mapper with well name as key. If not formation tops dict is empty, it will try to fetch from CDF. Defaults to empty Dict.
        extend_top_lines (bool, optional): Specify whether to extend top lines across all subplot views. Defaults to False.
        md_column (str, optional): name of depth curve in dataframe. Defaults to "DEPT".

    Returns:
        go.Figure: passing plotly graph_object Figure with added optional curve in subplot
    """

    formation_tops_mapper: Dict[str, Dict[str, Any]] = kwargs.get(
        "formation_tops_mapper", dict()
    )

    well_name: str = df[id_column].unique()[0]
    tops_level: str = formation_level.lower()
    # If formation tops mapper not provided, fetch from CDF
    if len(formation_tops_mapper) == 0:
        client = utilities.get_cognite_client()
        # Get formation tops mapper
        formation_tops_mapper = utilities.get_formation_tops([well_name], client)

        # If formation tops not in CDF
        if len(formation_tops_mapper) == 0:
            return fig

    # Extract formation tops mapper for specified well
    formations_dict: Dict[str, Any] = formation_tops_mapper[well_name]

    formation_midpoints = []
    for i in range(len(formations_dict[tops_level + "_levels"]) - 1):
        formation_midpoints.append(
            formations_dict[tops_level + "_levels"][i]
            + (
                formations_dict[tops_level + "_levels"][i + 1]
                - formations_dict[tops_level + "_levels"][i]
            )
            / 2
        )
    for label, formation_mid in zip(  # noqa: ignore
        formations_dict[tops_level + "_labels"], formation_midpoints
    ):
        if formation_mid < df[md_column].max() and formation_mid > df[md_column].min():
            # Add text with formation/group name
            fig.add_trace(
                go.Scatter(
                    x=[0],
                    y=[formation_mid],
                    text="<b>" + label + "</b>",
                    mode="text",
                    textposition="middle right",
                    textfont=dict(
                        color="darkgreen",
                        size=14,
                    ),
                    name=formation_level,
                ),
                row=1,
                col=i_curve,
            )

    # Add green background in formation column
    fig.add_vrect(
        x0=0,
        x1=1,
        fillcolor="seagreen",
        opacity=0.3,
        line_width=0,
        row=1,
        col=i_curve,
    )

    # Add green lines to separate tops in formation column
    for i in range(len(formations_dict[tops_level + "_levels"]) - 1):
        fig.add_shape(
            type="line",
            x0=0,
            y0=formations_dict[tops_level + "_levels"][i],
            x1=1,
            y1=formations_dict[tops_level + "_levels"][i],
            line=dict(color="darkgreen"),
            row=1,
            col=i_curve,
            layer="above",
            name=formation_level,
        )

    fig.update_xaxes(
        title_text=formation_level,
        row=1,
        col=i_curve,
        range=[0, 1],
    )

    # Add light lines to inidcate tops across all columns
    if extend_top_lines:
        for i_col in range(1, ncols):
            try:
                i_x0 = fig["layout"]["xaxis" + str(i_col)]["range"][0]
                i_x1 = fig["layout"]["xaxis" + str(i_col)]["range"][1]

                # Special treatment og RDEP due to log scale
                if fig["layout"]["xaxis" + str(i_col)]["title"]["text"] == "RDEP":
                    i_x0 = 0
                    i_x1 = 200 * 1000
            except Exception:
                pass

            for i in range(len(formations_dict[tops_level + "_levels"]) - 1):
                fig.add_shape(
                    type="line",
                    x0=i_x0,
                    x1=i_x1,
                    y0=formations_dict[tops_level + "_levels"][i],
                    y1=formations_dict[tops_level + "_levels"][i],
                    line=dict(color="darkgrey"),
                    opacity=0.5,
                    row=1,
                    col=i_col,
                    layer="above",
                )

    return fig


def add_curve(
    fig: go.Figure, i_curve: int, df: pd.DataFrame, curve_name: str, md_column: str
) -> go.Figure:
    """
    Add optional column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about curve to plot and depth
        curve_name (str): name of cruve to plot in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added optional curve in subplot
    """

    left_col_value = df[curve_name].min()
    right_col_value = df[curve_name].max()

    fig.add_trace(
        go.Scatter(
            x=df[curve_name],
            y=df[md_column],
            mode="lines",
            marker=dict(color="black"),
            name=curve_name,
        ),
        row=1,
        col=i_curve,
    )
    fig.update_xaxes(
        title_text=curve_name,
        range=[left_col_value, right_col_value],
        row=1,
        col=i_curve,
    )

    return fig


def add_binary_curve(
    fig: go.Figure,
    i_curve: int,
    df: pd.DataFrame,
    flag_color: str,
    curve_name: str,
    md_column: str,
) -> go.Figure:
    """
    Add binary column to passing go.Figure object.

    Args:
        fig (go.Figure): plotly graph_object Figure to append binary coulmn
        i_curve (int): index of column to add curve in subplot figure (from 1 to ncols)
        df (pd.DataFrame): dataframe with information about binary curve and depth
        flag_color (str): Color of binary flag. Support color hex codes and matplotlib colors
        curve_name (str): name of binary curve in dataframe
        md_column (str): name of depth curve in dataframe

    Returns:
        go.Figure: passing plotly graph_object Figure with added binary curve in subplot
    """

    binary_numbers = {
        1.0: {curve_name: curve_name, "color": flag_color},
        0.0: {curve_name: curve_name, "color": "#ffffff"},
    }
    transition_depths_list = binary_transition_depths_fill_gaps(
        df=df,
        curve_name=curve_name,
        md_column=md_column,
        binary_numbers=binary_numbers,
        binary_key=curve_name,
    )

    in_legend = []
    for depth_tuple in transition_depths_list:
        if depth_tuple[2] == "#ffffff":
            continue
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[depth_tuple[0], depth_tuple[0]],
                mode="lines",
                marker=dict(color=depth_tuple[2]),
                name=depth_tuple[3],
                showlegend=False,
            ),
            row=1,
            col=i_curve,
        )

        if depth_tuple[3] not in in_legend:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                ),
                row=1,
                col=i_curve,
            )
            in_legend.append(depth_tuple[3])
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[depth_tuple[1], depth_tuple[1]],
                    mode="lines",
                    marker=dict(color=depth_tuple[2]),
                    name=depth_tuple[3],
                    fill="tonexty",
                    fillcolor=depth_tuple[2],
                    showlegend=False,
                ),
                row=1,
                col=i_curve,
            )

    fig.update_xaxes(
        title_text=curve_name,
        row=1,
        col=i_curve,
        range=[0.0, 1.0],
    )

    return fig
