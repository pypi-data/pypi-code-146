import io
import uuid
import json
import numpy as np
import requests

from typing import Union, Optional, Dict, Any, List

from ai_dashboard.api import endpoints
from ai_dashboard.tabs import abstract_tab
from ai_dashboard.tabs.data_report import blocks
from ai_dashboard.tabs.data_report import constants
from ai_dashboard.tabs.data_report import markdown
from ai_dashboard.constants import Colours

import plotly.express as px


class DataReport(abstract_tab.Tab):
    ID = "REPORT"

    BLANK: Dict[str, Any] = {
        "activeFilterGroup": "",
        "color": None,
        "configuration": {
            "content": {
                "type": "doc",
                "content": [],
            }
        },
        "name": "",
        "type": ID,
    }

    def __init__(
        self,
        endpoints: endpoints.Endpoints,
        dataset_id: str,
        title: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self._endpoints = endpoints
        self.title = title

        if config is not None:
            self._config = config
        else:
            self.reset()

        self.dataset_id = dataset_id

        if colour is not None:
            colour_values = list(map(lambda x: x._value_, Colours))
            assert colour in colour_values, f"Colour must one of {colour_values}"

        self.config["colour"] = colour
        self.config["configuration"]["title"] = self.ID if title is None else title
        self.config["name"] = name

    def add_blocks(self, list_of_blocks):
        for block in list_of_blocks:
            output = block(self)
            self.config["configuration"]["content"]["content"].append(output)

    @classmethod
    def from_text(
        cls,
        text: str,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        if colour is not None:
            assert colour in constants.colours
        data_report = cls(title=title)
        data_report.config = {
            "name": name,
            "type": "REPORT",
            "color": colour.upper() if colour is not None else colour,
            "configuration": {
                "title": title,
                "content": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "appBlock",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "attrs": {"textAlign": "left"},
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": text,
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
            },
            "activeFilterGroup": "",
        }
        return data_report

    @classmethod
    def from_markdown(
        cls,
        text: str,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        data_report = cls(title=title)
        md = markdown.MarkDown()
        content = md.parse(text)
        data_report.config = {
            "name": name,
            "type": cls.ID,
            "color": colour.upper() if colour is not None else colour,
            "configuration": {
                "title": title,
                "content": {
                    "type": "doc",
                    "content": content,
                },
            },
            "activeFilterGroup": "",
        }
        return data_report

    def add_markdown(self, text: str):
        md = markdown.MarkDown()
        content = md.parse(text)
        config = self.config["configuration"]
        if "content" not in config:
            self.config["configuration"]["content"] = {
                "type": "doc",
                "content": [],
            }
        self.config["configuration"]["content"]["content"] += content

    def add_connected_chart(
        self,
        groupby: List[Dict[str, Any]],
        metric: List[Dict[str, Any]],
        chart_type: str = "column",
        title: Optional[str] = None,
        page_size: int = 20,
        show_frequencies: bool = False,
        sentiment_field: str = "",
        y_axis_sort_field: str = "",
        sort_direction: str = "desc",
        filters: Optional[List[Dict[str, Any]]] = None,
        convert_filters: bool = True,
    ):
        block = blocks.ConnectedChart(
            groupby=groupby,
            metric=metric,
            chart_type=chart_type,
            title=title,
            page_size=page_size,
            show_frequencies=show_frequencies,
            sentiment_field=sentiment_field,
            y_axis_sort_field=y_axis_sort_field,
            sort_direction=sort_direction,
            filters=filters,
            convert_filters=convert_filters,
        )
        self.config["configuration"]["content"]["content"].append(block())

    add_aggregation = add_connected_chart

    def add_connected_metric(
        self,
        query: List[Dict[str, Any]],
        title: Optional[str] = None,
        show_frequencies: bool = False,
        sort_direction: str = "Descending",
    ):
        block = blocks.ConnectedMetric(
            query=query,
            title=title,
            show_frequencies=show_frequencies,
            sort_direction=sort_direction,
        )
        self.config["configuration"]["content"]["content"].append(block())

    add_metric = add_connected_metric

    def add_image(
        self, image_src: Union[bytes, str], title: str = "", width_percentage: int = 100
    ):
        block = blocks.Image(
            image_url=image_src, title=title, width_percentage=width_percentage
        )
        self.config["configuration"]["content"]["content"].append(block())

    def add_audio(
        self, audio_src: Union[bytes, str], title: str = "", width_percentage: int = 100
    ):
        block = blocks.Audio(
            audio_url=audio_src, title=title, width_percentage=width_percentage
        )
        self.config["configuration"]["content"]["content"].append(block())

    def add_video(
        self, video_src: Union[bytes, str], title: str = "", width_percentage: int = 100
    ):
        block = blocks.Video(
            audio_url=video_src, title=title, width_percentage=width_percentage
        )
        self.config["configuration"]["content"]["content"].append(block())

    def add_plotly(
        self,
        fig: Any,
        title: str,
        width: int = None,
        height: int = None,
        width_percentage: int = 100,
        options=None,
    ):
        block = blocks.Plotly(
            fig=fig,
            title=title,
            width=width,
            height=height,
            width_percentage=width_percentage,
            options=options,
        )
        self.config["configuration"]["content"]["content"].append(block())

    def add_altair(
        self,
        fig: Any,
        title: str,
        width_percentage: int = 100,
    ):
        block = blocks.Altair(fig=fig, title=title, width_percentage=width_percentage)
        self.config["configuration"]["content"]["content"].append(block())

    def add_pyplot(
        self,
        fig,
        title: str = "",
        width: int = None,
        height: int = None,
        dpi: int = 150,
        add: bool = True,
        width_percentage: int = 100,
        **kwargs,
    ):
        block = blocks.Pyplot(
            fig=fig,
            title=title,
            width=width,
            height=height,
            dpi=dpi,
            add=add,
            width_percentage=width_percentage,
            **kwargs,
        )
        self.config["configuration"]["content"]["content"].append(block())
