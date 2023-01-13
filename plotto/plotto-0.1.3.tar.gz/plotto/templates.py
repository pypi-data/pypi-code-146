from __future__ import annotations

import copy

# ------------------------ basic: tailored -----------------------------

basic_configuration = {
    "opacity": 0.9,
    "opacity_on_click": 0.01,
    "width": 450,
    "height": 300,
}

# configuration: https://altair-viz.github.io/user_guide/configuration.html

# --------------------------- axis -------------------------------------

configure_axisX = {
    "labelAngle": 0,
    "grid": False,
    # 'domain': False,
    "labelSeparation": 1,
    "titlePadding": 15,
}

configure_axisY = {
    "ticks": False,
    "domain": False,
    "titleAngle": 0,
    "titlePadding": 35,
    # 'titleFontSize': 25,
    # 'titleAnchor': 'end',
    # 'titleX': 100,
    # 'position': -10,
    "labelPadding": 10,
    "labelAngle": 0,
}

# --------------------------- titles -----------------------------------

# Altair: https://altair-viz.github.io/user_guide/configuration.html#config-title

configure_title_options = [
    "align",
    "anchor",
    "angle",
    "aria",
    "baseline",
    "color",
    "dx",
    "dy",
    "font",
    "fontSize",
    "fontStyle",
    "fontWeight",
    "frame",
    "limit",
    "lineHeight",
    "offset",
    "orient",
    "subtitleColor",
    "subtitleFont",
    "subtitleFontSize",
    "subtitleFontStyle",
    "subtitleFontWeight",
    "subtitleLineHeight",
    "subtitlePadding",
    "zindex",
]

configure_title = {
    "fontSize": 16,
    "offset": 15,
    "subtitleFontSize": 13,
    "subtitlePadding": 7,
}

# configure_footnote = {
#     'color': '#5E5A59',
#     'baseline': 'bottom',
#     'orient': 'right',
#     'anchor': 'start',
#     'fontWeight': 'normal',
#     'fontSize': 13,
#     'offset': 28,
#     'lineHeight': 20,
#     'align': 'left'
# }

configure_footnote = {
    "color": "#474B51",
    "orient": "right",
    "fontWeight": "normal",
    "fontSize": 13,
    "lineHeight": 17,
    "angle": 0,
    "dy": 170,
    "dx": -175,
}

configure_table_note = {"align": "left"}
# --------------------------- header -----------------------------------

configure_header = {}

# --------------------------- legends ----------------------------------
configure_point = {"filled": True, "size": 60}

configure_legend_shape_by = {
    "title": "",  # used to be Group
    "symbolSize": 150,
    "symbolOpacity": 0.9,
    "strokeColor": "gray",
    "fillColor": "#EEEEEE",
    "padding": 10,
    "cornerRadius": 10,
    "direction": "vertical",
    "columns": 1,
}

configure_legend_color_by = {
    "title": "",
    "symbolSize": 150,
    "symbolOpacity": 0.9,
    "strokeColor": "gray",
    "fillColor": "#EEEEEE",
    "padding": 10,
    "cornerRadius": 10,
    "direction": "horizontal",
    "columns": 1,
}

configure_line = {
    "strokeWidth": 2,
    "strokeOpacity": 0.5,
}

configure_vertical_line = {"strokeDash": [3, 3], "opacity": 0.3}

configure_horizontal_line = {"strokeDash": [3, 3], "opacity": 0.3}

configure_legend_dash_by = {
    "title": "",
    "symbolSize": 1200,
    "symbolStrokeWidth": 2.3,
    "symbolOpacity": 0.9,
    "symbolStrokeColor": "grey",
    # 'labelFontSize': 12,
    # 'labelPadding': 55,
    # 'labelSeparation': 20,
    "labelOffset": 5,
    # 'orient': 'right',
    # 'padding': 20,
    "direction": "vertical",
    # 'columns': 2
}

configure_legend_size_by = {}

configure_view = {"strokeWidth": 0}
configure = {}

# ----------------------------------------------------------------------

MAIN_PLOTTING_TEMPLATE = {
    **basic_configuration,
    "configure": configure,
    # marks
    "configure_point": configure_point,
    "configure_line": configure_line,
    "configure_vertical_line": configure_vertical_line,
    "configure_horizontal_line": configure_horizontal_line,
    # general
    "configure_view": configure_view,
    # axis
    "configure_axisX": configure_axisX,
    "configure_axisY": configure_axisY,
    # titles
    "configure_title": configure_title,
    "configure_footnote": configure_footnote,
    "configure_table_note": configure_table_note,
    # header
    "configure_header": configure_header,
    # legends
    "configure_legend_shape_by": configure_legend_shape_by,
    "configure_legend_dash_by": configure_legend_dash_by,
    "configure_legend_color_by": configure_legend_color_by,
    "configure_legend_size_by": configure_legend_size_by,
}


def update_plot_params(**plot_params):
    config_params = {k: v for k, v in plot_params.items() if "config" in k}
    plot_params = {k: v for k, v in plot_params.items() if "config" not in k}

    params = copy.deepcopy(MAIN_PLOTTING_TEMPLATE)

    for k, v in config_params.items():
        params[k].update(v)

    params.update(plot_params)

    return params


# symbols: https://vega.github.io/vega/docs/marks/symbol/
# issue on line-point legend: https://github.com/altair-viz/altair/issues/2193
# domain for datetime: https://github.com/altair-viz/altair/issues/1005
