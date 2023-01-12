import json
import io
import numpy as np
from typing import Union, Optional, Dict, Any, List
from ai_dashboard.tabs.data_report.blocks.base import BaseBlock


class Plotly(BaseBlock):
    def __init__(
        self,
        fig: Any,
        title: str = "",
        width: int = None,
        height: int = None,
        width_percentage: int = 100,
        options=None,
    ):
        if options is None:
            options = {"displayLogo": False}
        try:
            import plotly
        except ImportError:
            raise ImportError(
                ".plotly requires plotly to be installed, install with 'pip install -U plotly'."
            )
        layout = fig._layout
        if width:
            layout["width"] = width
        else:
            if "width" in layout and layout["width"] == np.inf:
                layout["width"] = "auto"
        if height:
            layout["height"] = height
        else:
            if "height" in layout and layout["height"] == np.inf:
                layout["height"] = "auto"
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "attrs": {
                        "height": "auto",
                        "data": fig._data,
                        "layout": layout,
                        "options": options,
                        "title": title,
                        "width": f"{width_percentage}%",
                    },
                    "type": "plotlyChart",
                }
            ],
        }


class Altair(BaseBlock):
    def __init__(
        self,
        fig: Any,
        title: str = "",
        width_percentage: int = 100,
    ):
        try:
            import altair
        except ImportError:
            raise ImportError(
                ".altair requires altair to be installed, install with 'pip install -U altair'."
            )
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "attrs": {
                        "height": "auto",
                        "title": title,
                        "width": f"{width_percentage}%",
                        "spec": json.loads(fig.to_json()),
                    },
                    "type": "vegaChart",
                }
            ],
        }


class Vega(BaseBlock):
    def __init__(
        self,
        vega_json: Any,
        title: str = "",
        width_percentage: int = 100,
    ):
        self.block = {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {
                    "attrs": {
                        "height": "auto",
                        "title": title,
                        "width": f"{width_percentage}%",
                        "spec": vega_json,
                    },
                    "type": "vegaChart",
                }
            ],
        }


class Pyplot(BaseBlock):
    def __init__(
        self,
        fig,
        title: str = "",
        width: int = None,
        height: int = None,
        dpi: int = 150,
        width_percentage: int = 100,
        **kwargs,
    ):
        self.title = title
        self.width_percentage = width_percentage
        self.upload = True
        try:
            import matplotlib.pyplot as plt

            plt.ioff()
        except ImportError:
            raise ImportError(
                ".pyplot requires matplotlib to be installed, install with 'pip install -U matplotlib'."
            )
        if width or height:
            sizes = fig.get_size_inches()
            fig.set_size_inches(
                width / dpi if width else sizes[0], height / dpi if height else sizes[1]
            )
        self.fig_image = io.BytesIO()
        savefig_kwargs = {"dpi": dpi, "bbox_inches": "tight", "format": "png"}
        savefig_kwargs.update(kwargs)
        fig.savefig(self.fig_image, **savefig_kwargs)

    def override_image_url(self, image_url: str):
        self.image_url = image_url
        self.upload = False

    def postprocess(self, report_client):
        """
        Upload the image to the report app and return the block.
        """
        if self.upload:
            self.image_url = report_client._endpoints._upload_file(
                report_client.dataset_id, self.fig_image, f"{self.title}.png"
            )
        self.block = {
            "type": "appBlock",
            "content": [
                {
                    "type": "imageDisplayBlock",
                    "attrs": {
                        "imageSrc": self.image_url,
                        "title": self.title,
                        "width": f"{self.width_percentage}%",
                        "height": "auto",
                    },
                }
            ],
        }
