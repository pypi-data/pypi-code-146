from __future__ import annotations

import itertools

import altair as alt
from altair import Undefined
from pandas import DataFrame

from plotto.marks.utility import (add_straight_line, chart_html,
                                  plot_table_note, random_colors)


class MarkPlot:
    def __init__(
        self,
        data: DataFrame,
        x: str,
        y: str,
        vertical: bool = True,
        lower_upper: list = None,
        # -----------------------------------------------------
        points: bool = True,
        lines: bool = False,
        ebands: bool = False,
        ebars: bool = True,
        eticks: bool = True,
        # ~ first level
        shape_by: str = None,  # main !
        dash_by: str = None,
        # ~ second level
        color_by: str = None,
        size_by: str = None,
        dashes: list[list[int, int]] = None,
        colors: str | list = None,
        shapes: list = None,
        # 'h' is for shape, main group
        select_by: str = "h",  # 'h', 'c', 's', 'hc', ... 'hcs'
        tooltip: str | list = None,
        facet_group: str = None,
        # -----------------------------------------------------
        zero_in_xscale: bool = False,
        vertical_line: float | int | str = None,
        horizontal_line: float | int | str = None,
        enc_x: str = None,
        enc_y: str = None,
        title: str | list = None,
        subtitle: str | list = None,
        y_title: str | list = None,
        x_title: str | list = None,
        opacity: float = 1,
        opacity_on_click: float = 0.1,
        height: float = None,
        width: float = None,
        footnote: str | list = None,
        table_note: str | list = None,
        # -----------------------------------------------------
        configure: dict = None,
        configure_title: dict = None,
        configure_view: dict = None,
        configure_axis: dict = None,
        configure_axisX: dict = None,
        configure_axisY: dict = None,
        configure_legend_shape_by: dict = None,
        configure_legend_dash_by: dict = None,
        configure_legend_color_by: dict = None,
        configure_legend_size_by: dict = None,
        configure_header: dict = None,
        configure_footnote: dict = None,  # alt.TitleParams
        configure_table_note: dict = None,
        properties_table_note: dict = None,
        configure_point: dict = None,
        configure_line: dict = None,
        configure_vertical_line: dict = None,
        configure_horizontal_line: dict = None,
        configure_rule: dict = None,
        configure_tick: dict = None,
        configure_area: dict = None,
    ):

        self.data = data.copy()

        self.x = x  # 'T:T'  # # format='%m/%d'
        self.y = y
        self.vertical = vertical

        self.lower_upper = ["lower", "upper"] if lower_upper is None else lower_upper

        # ------------------------ dict configurations -----------------
        self.zero_in_xscale = zero_in_xscale

        self.vertical_line_at = vertical_line
        self.horizontal_line_at = horizontal_line

        self.enc_x = enc_x
        self.enc_y = enc_y

        self.title = "" if title is None else title
        self.subtitle = "" if subtitle is None else subtitle

        self.y_title = y if y_title is None else y_title
        self.x_title = x if x_title is None else x_title

        self.height = height
        self.width = width

        self.opacity = opacity
        self.opacity_on_click = opacity_on_click

        self.table_note = table_note

        # ----------------- dict configurations ------------------------

        self.configure = {} if configure is None else configure

        self.configure_title = {} if configure_title is None else configure_title

        self.configure_view = {} if configure_view is None else configure_view

        self.configure_axis = {} if configure_axis is None else configure_axis

        self.configure_axisX = {} if configure_axisX is None else configure_axisX

        self.configure_axisY = {} if configure_axisY is None else configure_axisY

        self.configure_point = {} if configure_point is None else configure_point

        self.configure_line = {} if configure_line is None else configure_line

        self.configure_vertical_line = (
            {} if configure_vertical_line is None else configure_vertical_line
        )

        self.configure_horizontal_line = (
            {} if configure_horizontal_line is None else configure_horizontal_line
        )

        self.configure_rule = {} if configure_rule is None else configure_rule

        self.configure_tick = {} if configure_tick is None else configure_tick

        self.configure_area = {} if configure_area is None else configure_area

        self.configure_header = {} if configure_header is None else configure_header

        self.footnote = {"text": footnote} if footnote else {}

        if self.footnote:
            self.configure_footnote = (
                {} if configure_footnote is None else configure_footnote
            )
            self.configure_footnote = {**self.footnote, **self.configure_footnote}
        else:
            self.configure_footnote = {}

        self.configure_table_note = (
            {} if configure_table_note is None else configure_table_note
        )
        self.properties_table_note = (
            {} if properties_table_note is None else properties_table_note
        )

        self.configure_legend_shape_by = (
            {} if configure_legend_shape_by is None else configure_legend_shape_by
        )

        self.configure_legend_dash_by = (
            {} if configure_legend_dash_by is None else configure_legend_dash_by
        )

        self.configure_legend_color_by = (
            {} if configure_legend_color_by is None else configure_legend_color_by
        )

        self.configure_legend_size_by = (
            {} if configure_legend_size_by is None else configure_legend_size_by
        )

        # --------------------------------------------------------------

        self.points = points
        self.lines = lines

        self.ebands = ebands
        self.ebars = ebars
        self.eticks = eticks

        # ----------------------- legends ------------------------------

        # main legend
        self.legend_shape_by = alt.Legend(**self.configure_legend_shape_by)

        # other points legends
        self.legend_color_by = alt.Legend(**self.configure_legend_color_by)
        self.legend_size_by = alt.Legend(**self.configure_legend_size_by)

        # line legend: it is separate than the rest !!
        self.legend_dash_by = (
            alt.Legend(**self.configure_legend_dash_by)
            if dash_by or not self.points
            else None
        )

        # --------------- bind to the cols of the data -----------------

        self.shape_by = shape_by if shape_by is not None else dash_by

        self.dash_by = dash_by if dash_by is not None else shape_by

        self.color_by = color_by if color_by is not None else self.shape_by

        self.size_by = size_by

        # -------------- user defined colors, shapes, ... --------------

        if colors is None and self.color_by:
            self.colors = random_colors(self.data[self.color_by].nunique())
        elif self.color_by:
            self.colors = colors if isinstance(colors, list) else [colors]
        else:
            self.colors = colors[0] if isinstance(colors, list) else random_colors(1)[0]

        if dashes is None:
            self.dashes = Undefined
        else:
            self.dashes = dashes

        if shapes is None and self.shape_by:
            self.shapes = Undefined
        else:
            self.shapes = shapes

        # ------------------------ selections --------------------------
        if isinstance(tooltip, str):
            tooltip = [tooltip]

        self.tooltip = [] if tooltip is None else tooltip

        # selections

        self._select_and = "&" in select_by  # if there is no & use |or
        self.select_by = tuple([s for s in ["h", "c", "s"] if s in select_by])

        self.selection = None
        self.multiple_selections = []

        self.select_by_group = None
        self.select_by_color = None
        self.select_by_size = None

        self._base = None

        self.facet_group = facet_group
        if self.facet_group is not None:
            self.facet_title = self.title
            self.title = ""

    @property
    def _color_scale(self):
        return alt.Scale(
            range=self.colors,
            # scheme='greys',
            type="linear",
        )

    @property
    def _dash_scale(self):
        return alt.Scale(
            range=self.dashes,
        )

    @property
    def _shape_scale(self):
        return alt.Scale(
            range=self.shapes,
        )

    @property
    def get_selection(self):

        selections = []
        select_options = []  # 'h', 'c', 's'
        if self.shape_by and self.select_by_group is None:
            self.select_by_group = alt.selection_multi(
                fields=[self.shape_by], bind="legend"
            )

            selections.append(self.select_by_group)
            select_options.append("h")

        if self.color_by != self.shape_by and self.select_by_color is None:
            self.select_by_color = alt.selection_multi(
                fields=[self.color_by], bind="legend"
            )

            selections.append(self.select_by_color)
            select_options.append("c")

        if self.size_by and self.select_by_size is None:
            self.select_by_size = alt.selection_multi(
                fields=[self.size_by], bind="legend"
            )

            selections.append(self.select_by_size)
            select_options.append("s")

        if self.selection is None:
            # combine options with selections

            select_options = [
                itertools.combinations(select_options, i + 1)
                for i in range(len(select_options))
            ]

            selections = [
                itertools.combinations(selections, i + 1)
                for i in range(len(selections))
            ]

            # possible combinations of selections
            selections = dict(
                list(
                    zip(
                        list(itertools.chain(*select_options)),
                        list(itertools.chain(*selections)),
                    )
                )
            )

            try:
                self.multiple_selections = selections[self.select_by]  # tuple is key
            except KeyError as e:
                raise KeyError(
                    f"{e} "
                    f"it is likely that, for example shapes and color groupings are "
                    f"assigned to the same column (ie '{self.color_by}'), "
                    f"thus the selection should "
                    f"contain only the first of the grouping, 'h'"
                )

            if len(self.select_by) == 1:
                self.selection = self.multiple_selections[0]

            if len(self.select_by) == 2:
                if self._select_and:
                    self.selection = (
                        self.multiple_selections[0] & self.multiple_selections[1]
                    )
                else:
                    self.selection = (
                        self.multiple_selections[0] | self.multiple_selections[1]
                    )

            if len(self.select_by) == 3:
                if self._select_and:
                    self.selection = (
                        self.multiple_selections[0]
                        & self.multiple_selections[1]
                        & self.multiple_selections[2]
                    )
                else:
                    self.selection = (
                        self.multiple_selections[0]
                        | self.multiple_selections[1]
                        | self.multiple_selections[2]
                    )

        return self.selection

    @property
    def base(self):
        if self._base is None:
            self._base = alt.Chart(self.data)

            if self.vertical:
                params = {
                    "x": alt.X(
                        self.x,
                        title=self.x_title,
                        sort=None,  # otherwise it rearranges the labels if str
                        # scale=Undefined
                        # if not self.zero_in_xscale else alt.Scale(zero=self.zero_in_xscale)
                        scale=alt.Scale(zero=self.zero_in_xscale),
                    )
                }
            else:
                params = {
                    "y": alt.Y(
                        self.y,
                        title=self.y_title,
                        sort=None  # otherwise it rearranges the labels if str
                        # scale=alt.Scale(zero=False)
                    )
                }

            self._base = self._base.encode(**params)

            self._base = self._base.properties(
                title={
                    "text": self.title,
                    "subtitle": self.subtitle,
                }
            )
            if self.height:
                self._base = self._base.properties(height=self.height)
            if self.width:
                self._base = self._base.properties(width=self.width)

        return self._base

    def _add_ebands(self):

        base = self.base

        lower, upper = self.lower_upper

        # CI ebands
        ebands = base.mark_area(**self.configure_area).encode(
            y=alt.Y(lower),
            y2=alt.Y2(upper),
            color=alt.Color(self.color_by, scale=self._color_scale, legend=None)
            if self.color_by
            else alt.value(self.colors),
            opacity=alt.condition(
                self.selection,
                alt.value(self.opacity / 2.5),
                alt.value(self.opacity_on_click),
            )
            if self.color_by
            else alt.value(self.opacity / 2.5),
        )

        return ebands

    def _add_ebars(self):
        base = self.base

        lower, upper = self.lower_upper

        if self.vertical:  # vertical: estimates on the y-axis
            params = {"y": alt.Y(upper), "y2": alt.Y2(lower)}
        else:
            params = {"x": alt.X(lower), "x2": alt.X2(upper)}

        # CI bars (with ticks at endpoints)
        bars = base.mark_rule(**self.configure_rule).encode(
            **params,
            color=alt.Color(
                self.color_by,
                scale=self._color_scale,
                # sort=self.color_by_sort if self.color_by_sort else Undefined,
                legend=None,
            )
            if self.color_by
            else alt.value(self.colors),
            opacity=alt.condition(
                self.selection,
                alt.value(self.opacity),
                alt.value(self.opacity_on_click),
            )
            if self.color_by
            else alt.value(self.opacity),
        )

        return bars

    def _add_eticks(self):
        base = self.base

        if not self.vertical:
            orient = "vertical"
        else:
            orient = "horizontal"

        bar_ticks = []
        for tick in self.lower_upper:
            params = {"x": alt.X(tick)} if not self.vertical else {"y": alt.Y(tick)}

            bar_ticks.append(
                base.mark_tick(orient=orient, **self.configure_tick).encode(
                    **params,
                    color=alt.Color(self.color_by, scale=self._color_scale, legend=None)
                    if self.color_by
                    else alt.value(self.colors),
                    # sort=self.color_by_sort if self.color_by_sort else Undefined,
                    opacity=alt.condition(
                        self.selection,
                        alt.value(self.opacity),
                        alt.value(self.opacity_on_click),
                    )
                    if self.color_by
                    else alt.value(self.opacity),
                )
            )

        return bar_ticks

    def _add_lines(self):

        base = self.base

        lines = base.mark_line(
            **self.configure_line,
            # point=alt.OverlayMarkDef()
        ).encode(
            alt.Y(self.y, title=self.y_title),
            color=alt.Color(
                self.color_by,
                scale=self._color_scale,
                legend=None if self.points else self.legend_color_by,
            )
            if self.color_by
            else alt.value(self.colors),
            strokeDash=alt.StrokeDash(
                self.dash_by, scale=self._dash_scale, legend=self.legend_dash_by
            )
            if self.dash_by
            else alt.StrokeDash(),
            opacity=alt.condition(
                self.get_selection,
                alt.value(self.opacity),
                alt.value(self.opacity_on_click),
            )
            if self.dash_by
            else alt.value(self.opacity),
        )

        return lines

    def _add_points(self, tooltip):

        base = self.base

        if self.vertical:
            params = {"y": alt.Y(self.y, title=self.y_title)}
        else:
            params = {"x": alt.X(self.x, title=self.x_title)}

        points = base.mark_point(**self.configure_point).encode(
            **params,
            shape=alt.Shape(
                self.shape_by,
                # sort=alt.SortOrder('descending'),
                scale=self._shape_scale,
                # warning: likely bug in vega-lite, legends don't merge if facet
                legend=self.legend_shape_by if self.facet_group is None else None,
            )
            if self.shape_by
            else alt.Shape(),
            color=alt.Color(
                self.color_by,
                scale=self._color_scale,
                # sort=alt.SortOrder('descending'),
                legend=self.legend_color_by,
            )
            if self.color_by
            else alt.value(self.colors),
            size=alt.Size(
                f"{self.size_by}:O",
                legend=self.legend_size_by,
            )
            if self.size_by
            else alt.Size(),
            opacity=alt.condition(
                self.get_selection,
                alt.value(self.opacity),
                alt.value(self.opacity_on_click),
            )
            if (self.shape_by or self.color_by or self.size_by)
            else alt.value(self.opacity),
            tooltip=tooltip
            # todo: [alt.Tooltip(tooltip, format=",.2f") , 'sting']
        )

        return points

    def plot(
        self,
        save_fname: str = None,
        html_footnote: str = None,
    ):

        # chart = points,

        if self.points:
            points_chart = self._add_points(tooltip=self.tooltip)

            if self.vertical_line_at is not None:
                points_chart = points_chart + add_straight_line(
                    xy="x",
                    at=self.vertical_line_at,
                    enc=self.enc_x,
                    configure_vh_line=self.configure_vertical_line,
                )

            if self.horizontal_line_at is not None:
                points_chart = points_chart + add_straight_line(
                    xy="y",
                    at=self.horizontal_line_at,
                    enc=self.enc_y,
                    configure_vh_line=self.configure_horizontal_line,
                )

        if self.lines:
            lines_chart = self._add_lines()

            if not self.points:
                if self.vertical_line_at is not None:
                    lines_chart = lines_chart + add_straight_line(
                        xy="x",
                        at=self.vertical_line_at,
                        enc=self.enc_x,
                        configure_vh_line=self.configure_vertical_line,
                    )

                if self.horizontal_line_at is not None:
                    lines_chart = lines_chart + add_straight_line(
                        xy="y",
                        at=self.horizontal_line_at,
                        enc=self.enc_y,
                        configure_vh_line=self.configure_horizontal_line,
                    )

            # chart = lines, *chart  # switch this if you want to click on dashed lines

        if self.points and self.lines:
            chart = (
                points_chart,
                lines_chart,
            )  # switch this if you want to click on dashed lines
            # chart = lines_chart, points_chart  # switch this if you want to click on dashed lines

        elif self.points:
            chart = (points_chart,)
        elif self.lines:
            chart = (lines_chart,)
        else:
            raise ValueError("either 'points' or 'lines' must be set to True")

        if self.ebands:
            ebands = self._add_ebands()
            chart = *chart, ebands

        if self.ebars:
            ebars = self._add_ebars()
            chart = *chart, ebars

        if self.eticks:
            eticks = self._add_eticks()
            chart = *chart, *eticks

        chart = alt.layer(*chart)

        if self.facet_group is not None:
            if isinstance(self.facet_group, str):
                chart = chart.facet(
                    column=alt.Column(
                        self.facet_group,
                        # title=None,
                        # header=alt.Header(labelFontSize=20)
                        # # sort=alt.EncodingSortField(field='', order='descending'),
                    )
                )
            if isinstance(self.facet_group, list):
                col = self.facet_group[0]
                row = self.facet_group[1]

                chart = chart.facet(
                    column=alt.Column(
                        col,
                        title=col.title(),
                        # sort=alt.EncodingSortField(field='', order='descending'),
                    ),
                    row=alt.Row(
                        row,
                        title=row.title(),
                        # sort=alt.EncodingSortField(field='', order='descending'),
                    ),
                )
        # concat to add chart notes, and not loose main title
        # interactivity must come before concat
        y_independent = {"y": "independent"} if self.facet_group else {}

        chart = alt.concat(
            chart.resolve_scale(
                color="independent",
                shape="independent",
                strokeDash="independent",
                **y_independent
                # size
            )
            .add_selection(*self.multiple_selections)
            .interactive()
        )

        if self.configure_footnote:
            chart = chart.properties(title=alt.TitleParams(**self.configure_footnote))

        if self.table_note:
            table_note = plot_table_note(
                data=self.table_note,
                configure_table_note=self.configure_table_note,
                properties_table_note=self.properties_table_note,
            )
            # {'size': 15, 'dy': 130, 'align': 'left', 'color': 'gray'},
            # {'height': 60}
            chart = alt.hconcat(chart, table_note, spacing=50)

        chart = (
            chart.configure(**self.configure)
            .configure_title(**self.configure_title)
            .configure_view(**self.configure_view)
            .configure_axisX(
                **self.configure_axisX,
            )
            .configure_axisY(**self.configure_axisY)
            .configure_axis(**self.configure_axis)
            .configure_header(**self.configure_header)
        )

        # save chart in html
        if save_fname is not None:
            if not save_fname.endswith("html"):
                save_fname += ".html"

            chart_html(
                chart,
                figure_caption=html_footnote,
                caption_font="helvetica",
                save_fname=save_fname,
            )

        return chart
