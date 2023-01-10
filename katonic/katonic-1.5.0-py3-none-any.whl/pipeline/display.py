#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import json
import base64, io
from typing import Union

import pandas as pd
import kfp.dsl as dsl
import matplotlib.pyplot as plt


class Display:
    def __init__(self):
        self.__HTML_TEMPLATE = """
        <html><head>
            <style>
                table {
                    border: none;
                    border-collapse: collapse;
                    border-spacing: 0;
                    font-size: 14px;
                }
                td,
                th {
                    text-align: right;
                    vertical-align: middle;
                    padding: 0.5em 0.5em;
                    line-height: 1.0;
                    white-space: nowrap;
                    max-width: 100px;
                    text-overflow: ellipsis;
                    overflow: hidden;
                    border: none;
                }
                th {
                    font-weight: bold;
                }
                tbody tr:nth-child(odd) {
                    background: rgb(245, 245, 245);
                }
            </style>
        </head>
        <body><div>
        %s
        </div></body>
        </html>
        """

        self.__IMAGE_TEMPLATE = """
        <div>
          <p>{}</p>
          <img src="data:image/png;base64, {}" />
        </div>
        """

        self.__TEXT_TEMPLATE = """
        <div style="margin:10px 0;">
        <pre>
        {}
        </pre>
        </div>
        """
        self.content = []
        
    def save_metadata(self):
        """
        Saves the UI metadata for visualization in container. This method
        should be called at the end of a notebook. Only for Katonic platform 
        pipeline use.
        
        Returns:
            None
        """
        try:
            metadata = {
                "outputs" : [{
                    "type": "web-app",
                    "storage": "inline",
                    "source": self.get_html()
                }]
            }

            with open("mlpipeline-ui-metadata.json", "w") as f:
                f.write(json.dumps(metadata))
        except BaseException as e:
            print(e)
    
    def plot_display(self, title: str = ""):
        """
        Helps in capturing any kind of plots in a cell.
        
        Example
        --------------------
        >>> import seaborn as sns
        >>> from kkubes.display import Kkubes
        >>> import pandas as pd
        >>> kubes = Kkubes()
        >>> df = pd.read_csv("diabetes.csv")
        >>> sns.histplot(df["Age"])
        >>> kubes.plot_display(title="Age")
        
        Args:
            title (str, Default=""): Name of the plot to be passes as a string.
        
        Returns:
            None
        """
        try:
            output = io.BytesIO()
            plt.savefig(output, format="PNG")
            img_string = base64.b64encode(output.getvalue()).decode()
            img = self.__IMAGE_TEMPLATE.format(title, img_string)
            self.content.append(img)
        except BaseException as e:
            print(e)
        
    def get_html(self):
        """
        This method accumulates all of the data that was logged and converts them into HTML page.
        
        Returns:
            html_artifact (str): An entire HTML page with all the logged data in it.
            If nothing was logged it will return `This step did not produce any artifacts.`
        """
        try:
            html_outputs = ""
            if self.content:
                html_outputs = "".join(self.content).strip()
            elif not html_outputs:
                html_outputs = self.__TEXT_TEMPLATE.format("This step did not produce any artifacts.")
            # html_artifact
            return self.__HTML_TEMPLATE % html_outputs
        except BaseException as e:
            print(e)

    def dataframe_display(self, df: pd.DataFrame = None, desc: str = ""):
        """
        This method takes the dataframe and converts it into html and logs it.

        Args:
            df (pandas.DataFrame, defaut=None): The dataframe user want to log
            desc (str, default=""): A description/title for the dataframe
 
        Returns:
            None
        """
        if df is not None:
            txt = self.__TEXT_TEMPLATE.format(desc)
            self.content.append(txt)
            self.content.append(df.to_html())

    def basic_display(self, data: Union[int, float, str, tuple, list, dict] = None, desc: str=""):
        """
        This method takes basic datatypes and logs then into HTML.

        Args:
            data (Union[int, float, str, tuple, list, dict], default=None): Takes data and logs it
            desc (str, default=""): Description/title for the data
        
        Returns:
            None
        """
        try:
            if data is not None:
                self.content.append(desc)
                txt = self.__TEXT_TEMPLATE.format(str(data))
                self.content.append(txt)

        except BaseException as e:
            print(e)

    def create_volume(self, pvc_name: str, resource_name: str, size: str = "1Gi", modes: str = None):
        return dsl.VolumeOp(
            name=pvc_name,
            resource_name=resource_name,
            size=size,
            modes=dsl.VOLUME_MODE_RWO,
        )