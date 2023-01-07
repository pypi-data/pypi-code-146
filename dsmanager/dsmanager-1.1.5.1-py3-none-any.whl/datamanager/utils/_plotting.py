"""@Author: Rayane AMROUCHE

Plotting methods for the Utils class for the DataManager.
"""

from typing import Any

import pandas as pd  # type: ignore

import plotly.express as px  # type: ignore
import plotly.figure_factory as ff  # type: ignore


class PlottingUtils:
    """PlottingUtils class brings utils tools for the data manager."""

    @staticmethod
    def scatter_matrix(df_: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        """Plot a scatterplot matrix of the dataframe using plotly express scatter.

        Args:
            df_ (pd.DataFrame): DataFrame to be returned.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        fig = ff.create_scatterplotmatrix(df_, diag="histogram", **kwargs)
        fig.show()
        return df_

    @staticmethod
    def displot(df_: pd.DataFrame, name: str, **kwargs: Any) -> pd.DataFrame:
        """Plot a distplot for a given variable of a dataframe using plotly figure
            factory create_distplot.

        Args:
            df_ (pd.DataFrame): DataFrame to be returned.
            name (str): Variable for which distribution will be ploted.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        fig = ff.create_distplot([df_[name]], [name], **kwargs)
        fig.show()
        return df_

    @staticmethod
    def corr(df_: pd.DataFrame, squared: bool = False, **kwargs: Any) -> pd.DataFrame:
        """Plot a scatterplot matrix of the dataframe using plotly scatter.

        Args:
            df_ (pd.DataFrame): DataFrame to be returned.
            squared (bool, optional): If True use squared correlation instead of the
                simple correlation. Defaults to False.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        corr_ = df_.corr()
        if squared:
            corr_ = corr_**2
        fig = px.imshow(
            corr_,
            color_continuous_scale="Viridis",
            text_auto=True,
            aspect="auto",
            **kwargs
        )
        fig.show()
        return df_
