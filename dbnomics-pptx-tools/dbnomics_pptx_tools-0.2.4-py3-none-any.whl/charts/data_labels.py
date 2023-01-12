import dataclasses
from dataclasses import dataclass
from typing import Iterable, Iterator, cast

import daiquiri
from lxml import etree
from pandas import DataFrame
from pptx.chart.chart import Chart
from pptx.chart.datalabel import DataLabel
from pptx.chart.point import Point
from pptx.chart.series import _BaseCategorySeries
from pptx.dml.line import LineFormat
from pptx.oxml.ns import nsdecls

from dbnomics_pptx_tools.pptx_copy import copy_color_format_properties, copy_font_properties

logger = daiquiri.getLogger(__name__)


@dataclass
class DataLabelRenderData:
    series: _BaseCategorySeries
    point: Point
    ratio: float
    new_ratio: float | None

    @property
    def ratio_distance(self) -> float | None:
        if self.new_ratio is None:
            return None
        return self.new_ratio - self.ratio


def add_data_label_to_point(render_data: DataLabelRenderData, *, chart: Chart):
    value_axis_font = chart.value_axis.tick_labels.font

    data_label = cast(DataLabel, render_data.point.data_label)
    copy_font_properties(value_axis_font, data_label.font)
    dLbl_element = data_label._get_or_add_dLbl()

    numFmt_element = dLbl_element.find("./{*}numFmt")
    if numFmt_element is None:
        numFmt_element = etree.fromstring(f"""<c:numFmt {nsdecls("c")} />""")
        dLbl_element.append(numFmt_element)
    numFmt_element.attrib["formatCode"] = "0.0"
    numFmt_element.attrib["sourceLinked"] = "0"
    dLbl_element.find("./{*}showVal").attrib["val"] = "1"
    line = LineFormat(data_label._dLbl.get_or_add_spPr())
    copy_color_format_properties(render_data.series.format.line.color, line.color)

    ratio_distance = render_data.ratio_distance
    if ratio_distance is not None:
        logger.debug(
            "Moving the data label of the series %r because if is too close to the previous one",
            render_data.series.name,
        )
        layout_element = etree.fromstring(
            f"""
                <c:layout {nsdecls("c")}>
                    <c:manualLayout>
                        <c:x val="0"/>
                        <c:y val="{-ratio_distance}"/>
                    </c:manualLayout>
                </c:layout>
            """.strip()
        )
        dLbl_element.append(layout_element)


def add_data_label_to_last_point_of_each_series(chart: Chart, *, df: DataFrame):
    logger.debug("Adding a data label to the last point of each series of the chart...")

    render_data_list = compute_data_label_positions(chart, df=df)

    for render_data in render_data_list:
        add_data_label_to_point(render_data, chart=chart)


def compute_data_label_positions(chart: Chart, *, df: DataFrame) -> list[DataLabelRenderData]:
    render_data_list: list[DataLabelRenderData] = []

    for series in cast(Iterable[_BaseCategorySeries], chart.series):
        last_point = list(series.points)[-1]
        last_value = next((value for value in reversed(series.values) if value is not None), None)
        if last_value is None:
            logger.warning("The series %r only has NA values, skipping", series.name)
            continue
        chart_min_value, chart_max_value = compute_value_axis_bounds(df, chart=chart)
        chart_value_range = chart_max_value - chart_min_value
        ratio = (last_value - chart_min_value) / chart_value_range
        render_data_list.append(DataLabelRenderData(series=series, point=last_point, ratio=ratio, new_ratio=None))

    render_data_list = sorted(render_data_list, key=lambda render_data: render_data.ratio)
    return list(iter_spaced_data_labels(render_data_list))


def compute_value_axis_bounds(df: DataFrame, *, chart: Chart, margin_ratio: float = 0.1) -> tuple[float, float]:
    min_value = df["value"].min()
    max_value = df["value"].max()
    margin = (max_value - min_value) * margin_ratio
    minimum_scale = chart.value_axis.minimum_scale
    maximum_scale = chart.value_axis.maximum_scale
    return (
        minimum_scale if minimum_scale is not None else min_value - margin,
        maximum_scale if maximum_scale is not None else max_value + margin,
    )


def iter_spaced_data_labels(
    render_data_list: list[DataLabelRenderData], *, min_ratio_distance: float = 0.05
) -> Iterator[DataLabelRenderData]:
    if not render_data_list:
        return []

    yield render_data_list[0]
    last_ratio = render_data_list[0].ratio

    for current in render_data_list[1:]:
        if current.ratio - last_ratio < min_ratio_distance:
            new_ratio = last_ratio + min_ratio_distance
            yield dataclasses.replace(current, new_ratio=new_ratio)
            last_ratio = new_ratio
        else:
            yield current
            last_ratio = current.ratio
