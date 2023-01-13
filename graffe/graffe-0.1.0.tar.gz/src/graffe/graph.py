# Graffe | Copyright (C) 2023 John Constable
# This version first published 2023

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.


"""Create scientific-style graphs of bivariate data.

This module provides a way of quickly drawing graphs of bivariate data in a
scientific style, aimed towards plotting linearised experimental data.

The Graph class is provided to this end.
"""

__version__ = "0.1.0"

import os
import os.path

from math import sqrt
from matplotlib import font_manager, pyplot
from PIL import Image


class Graph:
    """Create and draw a scatter plot to be shown or saved.

    Methods:
        fit() -- perform a linear regression on the graph's data
        save(filename) -- save a PNG image of the graph to disc
        show() -- display a static image of the graph for inspection

    Most of this class's attributes are the ones passed to the constructor.
    Aside from these, the following attributes can be accessed if desired:

    Attributes:
        figure -- the matplotlib Figure that contains the graph
        axes -- the matplotlib Axes object which handles the graph data
    """
    def __init__(self, x_data, y_data, title="Title", x_label="independent "  \
            "variable", y_label="dependent variable", x_err=None, y_err=None,
            x_axis_position=None, y_axis_position=None, font=None):
        """Required arguments:
            x_data -- the independent variable data (list or list-like)
            y_data -- the dependent variable data (list or list-like)

        Keyword arguments:
            title -- the graph title, displayed as the figure heading
            x_label -- the label displayed underneath the x-axis
            y_label -- the label displayed to the left of the y-axis
            x_err -- uncertainty in the independent variable (constant or list)
            y_err -- uncertainty in the dependent variable (constant or list)
            x_axis_position -- whether to fix the x-axis to the top or the
            bottom of the figure, can be "top", "bottom", or None.  The default
            is None, meaning it is positioned automatically by matplotlib.
            y_axis_position -- whether to fix the y-axis to the left or the
            right of the figure, can be "left", "right", or None.  The default
            is None, meaning it is positioned automatically be matplotlib.
            font -- a string detailing a font family to be used for graph text
        """
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.x_err = x_err
        self.y_err = y_err
        self.x_axis_position = x_axis_position
        self.y_axis_position = y_axis_position
        self.font = font if font else self._get_default_font()

        if self.x_axis_position and                                           \
            self.x_axis_position.lower() not in ["left", "right"]:
            raise ValueError("invalid value provided to x_axis_position, "    \
                "expected \"left\" or \"right\"")

        if self.y_axis_position and                                           \
            self.y_axis_position.lower() not in ["top", "bottom"]:
            raise ValueError("invalid value provided to x_axis_position, "    \
                "expected \"top\" or \"bottom\"")

        self.figure, self.axes = pyplot.subplots()

        self._draw()

    def _draw(self):
        # Draw and customise data points
        self.axes.scatter(self.x_data, self.y_data, s=4 ** 2, color="black",
                          marker="x", linewidths=0.5)

        # Draw the errorbars if uncertainties are provided
        if self.x_err or self.y_err:
            self.axes.errorbar(self.x_data, self.y_data, xerr=self.x_err,
                               yerr=self.y_err, fmt="none", capsize=3,
                               ecolor="black", elinewidth=0.3, capthick=0.4)

        # Draw the best fit line
        (gradient, intercept), _ = self.fit()
        self.axes.axline((0, intercept), (1, gradient + intercept),
                         color="black", linewidth=0.3)

        # Draw and customise major and minor gridlines
        self.axes.minorticks_on()
        self.axes.grid(which="major", color="black", linewidth=0.5)
        self.axes.grid(which="minor", color="grey", linewidth=0.3)
        self.axes.set_axisbelow(True)

        # Add text
        font_dict = {"family": self.font}

        self.axes.set_title(self.title, pad=16, fontdict=font_dict)
        self.axes.set_xlabel(self.x_label, labelpad=12, fontdict=font_dict)
        self.axes.set_ylabel(self.y_label, labelpad=16, fontdict=font_dict)

        # Set axis positions
        if self.x_axis_position == "left":
            self.axes.set_xlim(left=0)
        elif self.x_axis_position == "right":
            self.axes.set_xlim(right=0)

        if self.y_axis_position == "top":
            self.axes.set_ylim(top=0)
        elif self.y_axis_position == "bottom":
            self.axes.set_ylim(bottom=0)

        # Adjust sizing
        width, height = self.figure.get_size_inches()

        if width > height:
            self.figure.set_size_inches(11.7, 8.3)
        else:
            self.figure.set_size_inches(8.3, 11.7)

        self.axes.title.set_fontsize(14)
        self.axes.xaxis.label.set_fontsize(12)
        self.axes.yaxis.label.set_fontsize(12)

        for text in self.axes.get_xticklabels() + self.axes.get_yticklabels():
            text.set_fontsize(7)

    def _get_default_font(self):
        fonts = font_manager.get_font_names()

        if "Baskerville Old Face" in fonts:
            return "Baskerville Old Face"

        if "Times New Roman" in fonts:
            return "Times New Roman"

        return "serif"

    def fit(self):
        """Perform a linear regression on the graph's data.

        The parameters of a fit line are calculated using an ordinary least
        squares method.  The Pearson product-moment correlation coefficient is
        also calculated.

        Returns (m, c), r where
            - m is the gradient of the fit line
            - c is the intercept of the fit line
            - r is the correlation coefficient
        """
        length = len(self.x_data)

        x_mean = sum(self.x_data) / length
        y_mean = sum(self.y_data) / length

        sum_of_products_of_x_and_y_residuals =                                \
            sum(((x - x_mean) * (y - y_mean)                                  \
            for (x, y) in zip(self.x_data, self.y_data)))

        sum_of_squares_of_x_residuals =                                       \
            sum(((x - x_mean) ** 2 for x in self.x_data))

        sum_of_squares_of_y_residuals =                                       \
            sum(((y - y_mean) ** 2 for y in self.y_data))

        gradient = sum_of_products_of_x_and_y_residuals                       \
            / sum_of_squares_of_x_residuals

        intercept = y_mean - (gradient * x_mean)

        covariance = sum_of_products_of_x_and_y_residuals / length

        x_std_deviation = sqrt(sum_of_squares_of_x_residuals / length)
        y_std_deviation = sqrt(sum_of_squares_of_y_residuals / length)

        correlation_coefficient = covariance                                  \
            / (x_std_deviation * y_std_deviation)

        return (gradient, intercept), correlation_coefficient

    def save(self, filename):
        """Save the graph to a PNG file on disc.

        There is one required argument, filename, which is a path to a location
        on disc and should not include the file extension.
        """
        self.figure.savefig(f"{filename}.png", dpi=300, format="png")

    def show(self):
        """Display the graph to the user.

        This method displays a static image of the graph to the user by
        temporarily saving the graph to a file and opening it with PIL.
        """
        # Generate names temp0, temp1, etc. until an available name is found
        # to use as a dummy file to save the graph to.
        extension = 0

        while True:
            filename = f"temp{extension}"
            filepath = f"{filename}.png"

            if os.path.exists(filepath):
                extension += 1
            else:
                break

        self.save(filename)

        # PIL shows the image to the user, then the temporary file is deleted.
        image = Image.open(filepath)
        image.show()

        os.remove(filepath)
