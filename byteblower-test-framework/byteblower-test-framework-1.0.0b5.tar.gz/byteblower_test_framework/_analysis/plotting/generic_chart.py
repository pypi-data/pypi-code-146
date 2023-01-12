import logging
from typing import Any, Mapping, Optional, Sequence  # for type hinting

from highcharts import Highchart

# Type aliases
ChartOptions = Mapping[str, Any]


class GenericChart(object):

    __slots__ = (
        '_title',
        '_y_axises',
        '_data_sets',
        '_x_axis_title',
        '_x_axis_options',
        '_chart_options',
    )

    def __init__(self,
                 title: str = "",
                 x_axis_title: str = "Time [s]",
                 x_axis_options: Optional[ChartOptions] = None,
                 chart_options: Optional[ChartOptions] = None) -> None:
        self._title = title
        self._y_axises = {}
        self._data_sets = {}
        self._x_axis_title = x_axis_title
        self._x_axis_options = x_axis_options
        self._chart_options = chart_options

    def add_series(
        self,
        data: Sequence[Any],
        chart_type: str,
        legend_name: str,
        y_axis_type: str,
        y_axis_units: str,
        y_axis_title: str = "",
        y_axis_options: str = "",
    ) -> None:
        if y_axis_type in self._y_axises:
            # Check if the units are the same
            if self._y_axises[y_axis_type]["units"] != y_axis_units:
                logging.error(
                    "Y axis with the same type have different units.'\
                    ' Please use the same unit of different types.'\
                    ' Axis type: %s", y_axis_type)
        else:
            if y_axis_title == "":
                if y_axis_units == "":
                    y_axis_title = "{}".format(y_axis_type)
                else:
                    y_axis_title = "{} [{}]".format(y_axis_type, y_axis_units)
            # Add this type to the y_axis types
            self._y_axises[y_axis_type] = {
                "units": y_axis_units,
                "title": y_axis_title,
                "index": -1,
                "y_axis_options": y_axis_options,
            }
        self._data_sets[legend_name] = {
            "title": legend_name,
            "data": data,
            "chart_type": chart_type,
            "y_axis_type": y_axis_type,
        }

    def plot(self) -> str:
        # Constant
        styling = "<span style=\"font-family: 'DejaVu Sans', '\
            ' Arial, Helvetica, sans-serif; color: "

        # Generate the y-axis
        y_axis_conf_list = []
        for key in self._y_axises:
            y_axis_conf = self._y_axises[key]
            new_conf = {}
            new_conf["title"] = {
                "text":
                styling + '#00AEEF; font-size: 12px;"\
                " line-height: 1.2640625; font-weight: bold; ">' +
                y_axis_conf["title"] + "</span>"
            }
            if len(y_axis_conf["y_axis_options"]) > 0:
                new_conf.update(y_axis_conf["y_axis_options"])
            self._y_axises[key]["index"] = len(y_axis_conf_list)
            y_axis_conf_list.append(new_conf)
        x_axis_conf = {
            "title": {
                "text":
                styling + '#F7941C; font-size: 12px;"\
                " line-height: 1.4640625; font-weight: bold;">' +
                self._x_axis_title + "</span>"
            }
        }
        if self._x_axis_options is not None:
            x_axis_conf.update(self._x_axis_options)
        chart_options = {}
        if self._chart_options is not None:
            chart_options.update(self._chart_options)

        chart = Highchart(width=1000, height=400)

        options = {
            "title": {
                "text":
                styling +
                '#00AEEF; font-size: 20px; line-height: 1.2640625; ">' +
                self._title + "</span>"
            },
            "chart": chart_options,
            "xAxis": x_axis_conf,
            "yAxis": y_axis_conf_list,
            # TODO - Add the colors as options (to `add_series` ?)
            # "colors": [
            #     '#00AEEF',
            #     '#00A650',
            #     '#00A650',
            #     '#00A650',
            #     '#00A650',
            # ],
        }
        # print(options)
        chart.set_dict_options(options)
        # Append the values.
        for data_set in self._data_sets:
            y_axis = self._y_axises[self._data_sets[data_set]
                                    ["y_axis_type"]]["index"]

            chart.add_data_set(
                self._data_sets[data_set]["data"],
                series_type=self._data_sets[data_set]["chart_type"],
                name=data_set,
                yAxis=y_axis,
            )
        return chart.iframe
