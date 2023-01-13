#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
from itertools import cycle
from . import CMAP
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path

from dataclasses import dataclass


import matplotlib
matplotlib.style.use('ggplot')
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["font.family"] = "serif"
plt.rcParams['axes.edgecolor'] = 'black'


linecycler = cycle(["-", "--", "-.", ":"])


@dataclass
class ColorBar:
    color: str = 'viridis'
    discreet: bool = False
    position: str = 'left'
    orientation: str = "vertical"
    symmetric: bool = False
    log_norm: bool = False
    numeric_format: str = ':.3f'
    n_ticks: int = None
    label_size: int = None

    def _render_(self, Ax, Scalar, Image) -> None:
        divider = make_axes_locatable(Ax._ax)
        cax = divider.append_axes(self.position, size="10%", pad=0.15)
        if self.discreet:
            unique_values = numpy.unique(Scalar)
            Norm = colors.BoundaryNorm(unique_values, unique_values.size + 1, extend='both')
            ticks = numpy.unique(Scalar)
            cbar = plt.colorbar(mappable=Image, norm=Norm, boundaries=ticks, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif self.log_norm and self.symmetric:
            Norm = matplotlib.colors.SymLogNorm(linthresh=1e-10)
            Norm.autoscale(Scalar)
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif self.log_norm and not self.symmetric:
            Norm = matplotlib.colors.LogNorm()
            Norm.autoscale(Scalar)
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif not self.log_norm and self.symmetric:
            Norm = matplotlib.colors.TwoSlopeNorm(vcenter=0, vmax=numpy.abs(Scalar).max(), vmin=-numpy.abs(Scalar).max())
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation)

        else:
            cbar = plt.colorbar(mappable=Image, norm=None, cax=cax, orientation=self.orientation, format=self.numeric_format)

        if self.n_ticks is not None and not self.log_norm:
            cbar.ax.locator_params(nbins=self.n_ticks)

        if self.label_size is not None:
            cbar.ax.tick_params(labelsize=self.label_size)


@dataclass
class Contour:
    x: numpy.ndarray
    y: numpy.ndarray
    scalar: numpy.ndarray
    colormap: str = CMAP.BKR
    isolines: list = None

    def _render_(self, Ax) -> None:
        Ax.contour(self.x,
                   self.y,
                   self.scalar,
                   level=self.isolines,
                   colors="black",
                   linewidth=.5)

        Ax.contourf(self.x,
                    self.y,
                    self.scalar,
                    level=self.isolines,
                    cmap=self.colormap,
                    norm=colors.LogNorm())


@dataclass
class Mesh:
    scalar: numpy.ndarray
    colormap: str = CMAP.BKR
    x: numpy.ndarray = None
    y: numpy.ndarray = None

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.scalar.shape[1])

        if self.y is None:
            self.y = numpy.arange(self.scalar.shape[0])

    def _render_(self, Ax):
        Image = Ax._ax.pcolormesh(self.x, self.y, self.scalar, cmap=self.colormap, shading='auto')

        Image.set_edgecolor('face')

        if Ax.colorbar is not None:
            Ax.colorbar._render_(Ax=Ax, Scalar=self.scalar, Image=Image)

        return Image


@dataclass
class Polygon:
    instance: object
    x: numpy.ndarray = None
    y: numpy.ndarray = None
    name: str = ''
    alpha: float = 0.4
    facecolor: str = 'lightblue'
    edgecolor: str = 'black'

    def _render_(self, ax):
        path = Path.make_compound_path(
            Path(numpy.asarray(self.instance.exterior.coords)[:, :]),
            *[Path(numpy.asarray(ring.coords)[:, :]) for ring in self.instance.interiors]
        )

        patch = PathPatch(path)
        collection = PatchCollection([patch], alpha=self.alpha, facecolor=self.facecolor, edgecolor=self.edgecolor)

        ax._ax.add_collection(collection, autolim=True)
        ax._ax.autoscale_view()
        if self.name:
            ax._ax.scatter(self.instance.centroid.x, self.instance.centroid.y)
            ax._ax.text(self.instance.centroid.x, self.instance.centroid.y, self.name)


@dataclass
class FillLine:
    x: numpy.ndarray
    y0: numpy.ndarray
    y1: numpy.ndarray
    label: str = None
    fill: bool = False
    color: str = None
    line_style: str = None
    show_outline: bool = True

    def _render_(self, Ax) -> None:
        if self.line_style is None:
            self.line_style = next(linecycler)

        Ax._ax.fill_between(self.x, self.y0, self.y1, color=self.color, linestyle=self.line_style, alpha=0.7, label=self.label)

        if self.show_outline:
            Ax._ax.plot(self.x, self.y1, color='k', linestyle='-', linewidth=1)


@dataclass
class STDLine:
    x: numpy.ndarray
    y_mean: numpy.ndarray
    y_std: numpy.ndarray
    label: str = None
    color: str = None
    line_style: str = None

    def _render_(self, Ax):
        if self.line_style is None:
            self.line_style = next(linecycler)

        y0 = self.y_mean - self.y_std / 2
        y1 = self.y_mean + self.y_std / 2

        line = Ax._ax.plot(self.x, self.y_mean, color=self.color, label=self.label + '[mean]', linestyle=self.line_style)

        Ax._ax.fill_between(self.x, y0, y1, color=line[-1].get_color(), linestyle='-', alpha=0.3, label=self.label + '[std]')


@dataclass
class Line:
    y: numpy.ndarray
    x: numpy.ndarray = None
    label: str = None
    color: str = None
    line_style: str = None

    def __post_init__(self):
        if self.x is None:
            self.x = numpy.arange(self.y.size)

    def _render_(self, Ax):
        if self.line_style == 'alternate':
            self.line_style = next(linecycler)

        if numpy.iscomplexobj(self.y):
            Ax._ax.plot(self.x, self.y.real, label=self.label + "[real]", color=self.color, linestyle=self.line_style)
            Ax._ax.plot(self.x, self.y.imag, label=self.label + "[imag]", color=self.color, linestyle=self.line_style)
        else:
            Ax._ax.plot(self.x, self.y, label=self.label, color=self.color, linestyle=self.line_style)


@dataclass
class Text:
    position: list = (0.9, 0.9)
    font_size: int = 8
    text: str = ''

    def _render_(self, Ax):
        art = AnchoredText(self.text,
                           loc='lower left',
                           prop=dict(size=self.font_size),
                           frameon=True,
                           bbox_to_anchor=(0.05, 1.0),
                           bbox_transform=Ax._ax.transAxes)

        Ax._ax.get_figure().add_artist(art)


@dataclass
class Scene2D:
    unit_size: tuple = (10, 3)
    tight_layout: bool = True
    title: str = ""

    def __post_init__(self):
        self.axis_generated = False
        self._axis = []
        self.nCols = None
        self.nRows = None

    def set_axis_row(self, value) -> None:
        for ax in self._axis:
            ax.row = value

    def set_axis_col(self, value) -> None:
        for ax in self._axis:
            ax.col = value

    @property
    def axis_matrix(self):
        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)
        for ax in self._axis:
            ax_matrix[ax.row, ax.col] = ax

        return ax_matrix

    @property
    def max_row(self):
        max_row = 0
        for ax in self._axis:
            max_row = ax.row if ax.row > max_row else max_row

        return max_row

    @property
    def max_col(self):
        max_col = 0
        for ax in self._axis:
            max_col = ax.col if ax.col > max_col else max_col

        return max_col

    def __getitem__(self, idx):
        return self._axis[idx]

    def __setitem__(self, idx, value):
        assert isinstance(value, Axis), f"Cannot assign type: {value.__class__} to Scene2D axis"
        self._axis[idx] = value

    def __add__(self, other):
        assert isinstance(other, Scene2D), f"Cannot add two different classes {self.__class__} and {other.__class__}"
        for ax in other._axis:
            self.append_axis(ax)

        return self

    def append_axis(self, ax):
        ax.row = self.max_row + 1 if self.max_row != 0 else 0
        ax.col = self.max_col + 1 if self.max_col != 0 else 0
        self._axis.append(ax)

    def font_size(self, value: int):
        for ax in self:
            ax.font_size = value

    def tick_size(self, value: int):
        for ax in self:
            ax.tick_size = value

    def x_limits(self, value: list):
        for ax in self:
            ax.x_limits = value

    def y_limits(self, value: list):
        for ax in self:
            ax.y_limits = value

    def x_label(self, value: list):
        for ax in self:
            ax.x_label = value

    def y_label(self, value: list):
        for ax in self:
            ax.y_label = value

    def water_mark(self, value: str):
        for ax in self:
            ax.water_mark = value

    def equal(self, value: bool):
        for ax in self:
            ax.equal = value

    def equal_limits(self, value: bool):
        for ax in self:
            ax.equal_limits = value

    def show_legend(self, value: bool):
        for ax in self:
            ax.show_legend = value

    def show_grid(self, value: bool):
        for ax in self:
            ax.show_grid = value

    def colorbar_n_ticks(self, value: int):
        for ax in self:
            ax.colorbar.n_ticks = value

    def colorbar_label_size(self, value: int):
        for ax in self:
            ax.colorbar.label_size = value

    font_size = property(None, font_size)
    tick_size = property(None, tick_size)
    x_limits = property(None, x_limits)
    y_limits = property(None, y_limits)
    x_label = property(None, x_label)
    y_label = property(None, y_label)
    water_mark = property(None, water_mark)
    equal = property(None, equal)
    equal_limits = property(None, equal_limits)
    show_legend = property(None, show_legend)
    show_grid = property(None, show_grid)
    colorbar_n_ticks = property(None, colorbar_n_ticks)
    colorbar_label_size = property(None, colorbar_label_size)

    def add_axes(self, *axis):
        for ax in axis:
            self._axis.append(ax)

        return self

    def _generate_axis_(self):
        figure_size = [self.unit_size[0] * (self.max_col + 1), self.unit_size[1] * (self.max_row + 1)]

        self._mpl_figure = plt.figure(figsize=figure_size)
        self._mpl_figure.suptitle(self.title)

        grid = gridspec.GridSpec(ncols=self.max_col + 1, nrows=self.max_row + 1, figure=self._mpl_figure)

        ax_matrix = numpy.full(shape=(self.max_row + 1, self.max_col + 1), fill_value=None)

        for axis in self._axis:
            subplot = self._mpl_figure.add_subplot(grid[axis.row, axis.col], projection=axis.projection)
            ax_matrix[axis.row, axis.col] = subplot
            axis._ax = subplot

        self.axis_generated = True

        return self

    def auto_arrange_axis(self, type='row'):
        if type == 'row':
            for n, ax in enumerate(self._axis):
                ax.row = n
                ax.col = 0
        else:
            for n, ax in enumerate(self._axis):
                ax.row = 0
                ax.col = n

    def _render_(self):
        if not self.axis_generated:
            self._generate_axis_()

        for ax in self._axis:
            ax._render_()

        if self.tight_layout:
            plt.tight_layout()

        return self

    def close(self):
        plt.close(self._mpl_figure)

    def show(self, save_directory: str = None, **kwargs):
        self._render_()
        if save_directory is not None:
            plt.savefig(fname=save_directory, **kwargs)

        plt.show()

        return self


@dataclass
class Axis:
    row: int
    col: int
    x_label: str = None
    y_label: str = None
    title: str = ''
    show_grid: bool = True
    show_legend: bool = False
    x_scale: str = 'linear'
    y_scale: str = 'linear'
    x_limits: list = None
    y_limits: list = None
    equal_limits: bool = False
    equal: bool = False
    colorbar: ColorBar = None
    water_mark: str = ''
    Figure: Scene2D = None
    projection: str = None
    font_size: int = 10
    tick_size: int = 10

    def __post_init__(self):
        self._ax = None
        self.Artist = []

    def __add__(self, other):
        self.Artist += other.Artist
        return self

    @property
    def style(self):
        return {'x_label': self.x_label,
                'y_label': self.y_label,
                'title': self.title,
                'show_grid': self.show_grid,
                'show_legend': self.show_legend,
                'x_scale': self.x_scale,
                'y_scale': self.y_scale,
                'x_limits': self.x_limits,
                'y_limits': self.y_limits,
                'equal_limits': self.equal_limits,
                'equal': self.equal,
                'colorbar': self.colorbar,
                'water_mark': self.water_mark,
                'projection': self.projection,
                'font_size': self.font_size,
                'tick_size': self.tick_size}

    def copy_style(self, other):
        assert isinstance(other, Axis), f"Cannot copy style from other class {other.__class__}"
        for element, value in other.style.items():
            setattr(self, element, value)

    def add_artist(self, *Artist):
        for art in Artist:
            self.Artist.append(art)

    def set_style(self, style_dict: dict):
        for element, value in style_dict.items():
            setattr(self, element, value)

    def _render_(self):
        logging.debug("Rendering axis...")

        for art in self.Artist:
            art._render_(self)

        if self.x_limits is not None:
            self._ax.set_xlim(self.x_limits)

        if self.y_limits is not None:
            self._ax.set_ylim(self.y_limits)

        if self.equal_limits:
            x_max = max(self._ax.get_xlim())
            x_min = min(self._ax.get_xlim())
            y_max = max(self._ax.get_ylim())
            y_min = min(self._ax.get_ylim())

            max_lim = x_max if x_max > y_max else y_max
            min_lim = x_min if x_min > y_min else y_min

            self._ax.set_xlim([min_lim, max_lim])
            self._ax.set_ylim([min_lim, max_lim])

        self._decorate_ax_()

    def _decorate_ax_(self):
        if self.show_legend:
            self._ax.legend(fancybox=True, facecolor='white', edgecolor='k')

        if self.x_label is not None:
            self._ax.set_xlabel(self.x_label, fontsize=self.font_size)

        if self.y_label is not None:
            self._ax.set_ylabel(self.y_label, fontsize=self.font_size)

        if self.title is not None:
            self._ax.set_title(self.title, fontsize=self.font_size)

        if self.x_scale is not None:
            self._ax.set_xscale(self.x_scale)

        if self.y_scale is not None:
            self._ax.set_yscale(self.y_scale)

        if self.tick_size is not None:
            self._ax.tick_params(labelsize=self.tick_size)

        if self.equal:
            self._ax.set_aspect("equal")

        if self.show_grid:
            self._ax.grid(self.show_grid)

        if self.water_mark is not None:
            self._ax.text(0.5, 0.1, self.water_mark, transform=self._ax.transAxes,
                    fontsize=30, color='white', alpha=0.2,
                    ha='center', va='baseline')


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig._mpl_figure.savefig(pp, format='pdf')

    pp.close()


# -
