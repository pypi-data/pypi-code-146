from __future__ import annotations

from pandas import DataFrame

from plotto.marks.mark_plot import MarkPlot
from plotto.templates import update_plot_params


def mark_plot(
    data: DataFrame,
    x: str,
    y: str,
    lower_upper: list = None,
    vertical: bool = True,
    points: bool = True,
    lines: bool = False,
    ebands: bool = False,
    ebars: bool = False,
    eticks: bool = False,
    # ~ first level
    shape_by: str = None,  # main !
    dash_by: str = None,
    # ~ second level
    color_by: str = None,
    size_by: str = None,
    # 'h' is for shape, main group
    select_by: str = "h",  # 'h', 'c', 's', 'gc', ... 'gcs'
    tooltip: list | str = None,
    facet_group: str = None,
    save_fname: str = None,
    **plotting_parameters,
):
    """

    Parameters
    ----------

        data: DataFrame
            a Pandas dataframe with the input data
        x: str
            name of the column in the data to display in the x-axis
        y: str
            name of the column in the data to display in the y-axis
        vertical: *bool*, default: ``True``
        lower_upper: *list*, default: ``None``
            name of the columns in the data used for error bars/bands
        points: *bool*, default: ``True``
            plot points
        lines: *bool*, default: ``True``
            plot lines
        ebands: *bool*, default: ``True``
            plot error bands
        ebars: *bool*, default: ``True``
            plot error bars
        eticks: *bool*, default: ``True``
            plot error ticks
        shape_by: *str*, default: ``None``
            name of the column in the data used to shape the points
        dash_by: *str*, default: ``None``
            name of the column in the data used to dash the lines
        color_by: *str*, default: ``None``
            name of the column in the data used color points/lines
        size_by: *str*, default: ``None``
            name of the column in the data used size points
        select_by: *str*, default: ``None``
            selection is bind to the legend

            options are:
                - 'h', 'c', 's',
                - 'hc', 'hs', 'cs' 'hcs' for an OR selection
                - 'h&c', 'h&s', 'c&s' 'h&c&s' for an AND selection

            where 'h' indicates the legend for the shapes
            where 'c' indicates the legend for the colors
            where 's' indicates the legend for the sizes

        tooltip: *str*, default: ``None``
        facet_group: *str*, default: ``None``
        save_fname: *str*, default: ``None``

        plotting_parameters:
            additional parameters that can be passed to mark_plot

            - **dashes**: *list[list[int, int]]*, default: ``None``
              list of dashes, example [[1, 0]]
            - **colors**: *str | list*, default: ``None``
            - **shapes**: *list*, default: ``None``
              circle, square, cross, diamond, triangle-up, triangle-down, triangle-right,
              triangle-left, stroke, arrow, wedge, triangle (or a custom SVG path string).
              `For more information <https://vega.github.io/vega/docs/marks/symbol/>`_.

            - **zero_in_xscale**: *bool*, default: ``False``
            - **vertical_line**: *float | int | str*, default: ``None``
              x coordinate at which to draw a vertical line

            - **horizontal_line**: *float | int | str*, default: ``None``
              y coordinate at which to draw a horizontal line

            - **enc_x**: *str*, default: ``None``
              `Encoding info <https://altair-viz.github.io/user_guide/encoding.html#encoding-data-types>`_

            - **enc_y**: *str*, default: ``None``
              `Encoding info <https://altair-viz.github.io/user_guide/encoding.html#encoding-data-types>`_

            - **title**: *str | list*, default: ``None``
            - **subtitle**: *str | list*, default: ``None``
            - **y_title**: *str | list*, default: ``None``
            - **x_title**: *str | list*, default: ``None``
            - **opacity**: *int | float*, default: ``1``
            - **opacity_on_click**: *int | float*, default: ``0.1``
            - **height**: *int | float*, default: ``None``
            - **width**: *int | float*, default: ``None``
            - **footnote**: *str | list*, default: ``None``
            - **table_note**: *str | list*, default: ``None``

            - **configure**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Chart Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-chart>`_

            - **configure_title**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Title Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-title>`_

            - **configure_view**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `View Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-view>`_

            - **configure_axis**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Axis Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-axis>`_

            - **configure_axisX**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Axis Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-axis>`_

            - **configure_axisY**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Axis Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-axis>`_

            - **configure_legend_shape_by**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Legend Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-legend>`_

            - **configure_legend_dash_by**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Legend Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-legend>`_

            - **configure_legend_color_by**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Legend Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-legend>`_

            - **configure_legend_size_by**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Legend Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-legend>`_

            - **configure_header**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Header Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-header>`_

            - **configure_footnote**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Title Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-title>`_

            - **configure_table_note**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **properties_table_note**: *dict*, default: ``None``

            - **configure_point**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_line**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_vertical_line**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_horizontal_line**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_rule**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_tick**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

            - **configure_area**: *dict*, default: ``None``

              a dictionary with attributes as keys and values that can be chosen within the options in Altair's
              `Mark and Mark Style Configuration <https://altair-viz.github.io/user_guide/configuration.html#config-mark>`_

    Returns
    -------
    """

    plot_parameters = update_plot_params(**plotting_parameters)

    hplot_plot_method_kwargs = [
        "save_fname",
        "html_footnote",
    ]

    object_kwargs = {
        k: v for k, v in plot_parameters.items() if k not in hplot_plot_method_kwargs
    }

    chart = MarkPlot(
        data=data,
        x=x,
        y=y,
        vertical=vertical,
        lower_upper=lower_upper,
        points=points,
        lines=lines,
        ebands=ebands,
        ebars=ebars,
        eticks=eticks,
        shape_by=shape_by,
        dash_by=dash_by,
        color_by=color_by,
        size_by=size_by,
        select_by=select_by,
        tooltip=tooltip,
        facet_group=facet_group,
        **object_kwargs,
    )

    instance_plot_method_kwargs = {
        k: v for k, v in plot_parameters.items() if k in hplot_plot_method_kwargs
    }

    chart = chart.plot(save_fname=save_fname, **instance_plot_method_kwargs)

    return chart
