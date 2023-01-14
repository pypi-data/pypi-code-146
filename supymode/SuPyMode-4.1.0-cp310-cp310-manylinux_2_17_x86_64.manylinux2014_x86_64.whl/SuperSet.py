#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
import os
import logging
from dataclasses import dataclass
from itertools import combinations

# Third-party imports
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp

# Local imports
from SuPyMode.SuperMode import SuperMode
from SuPyMode.Tools import Directories
from MPSPlots.Render2D import Scene2D, Axis, Multipage, Line, ColorBar, Mesh
from MPSPlots import CMAP


@dataclass
class SuperSet(object):
    """
    Solver to which is associated the computed SuperSet Modes

    .. note::
        This class is a representation of the fiber optic structures set of supermodes, hence the name.
        This class has not ling to c++ codes, it is pure Python.
        The items of this class are the supermodes generated from within the SuPySolver

    """

    parent_solver: None = None

    def __post_init__(self):
        self._matrix = None

        self.SuperModes = []
        self._itr_to_slice_interp = interp1d(self.itr_list, numpy.arange(self.itr_list.size))

    @property
    def size(self):
        """
        Return number of supermodes computed
        """

        return len(self.SuperModes)

    @property
    def geometry(self):
        """
        Return geometry of the coupler structure
        """

        return self.parent_solver.geometry

    @property
    def itr_list(self):
        """
        Return list of itr value that are used to compute the supermodes
        """

        return self.parent_solver.itr_list

    @property
    def axes(self):
        """
        Return axes object of the geometry
        """

        return self.parent_solver.geometry.axes

    @property
    def Matrix(self) -> numpy.ndarray:
        """Return supermode transfert matrix"""
        if self._matrix is None:
            self.compute_matrix()

        return self._matrix

    def itr_to_slice(self, itr_list: list[int]) -> list[int]:
        """
        Return slice number associated to itr value

        :param      itr_list:      Inverse taper ration value to evaluate the slice.
        :type       itr_list:      { type_description }

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        return self._itr_to_slice_interp(itr_list).astype(int)

    def slice_to_itr(self, slice_list: list[float]) -> list[float]:
        """
        Return slice number associated to itr value

        :param      slice_list:      Value of the slice to which evaluate the itr.
        :type       slice_list:      { type_description }

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        return [self.itr_list[i] for i in slice_list]

    def name_supermodes(self, *name_list) -> None:
        for n, name in enumerate(name_list):
            self[n].name = name
            setattr(self, name, self[n])

    def compute_matrix(self) -> numpy.ndarray:
        """
        Compute supermode transfert matrix
        """

        self._matrix = numpy.zeros([self.Size, self.Size, len(self.itr_list)])

        for mode in self.SuperModes:
            self._matrix[mode._ModeNumber, mode._ModeNumber, :] = mode.Betas

    def _compute_transmission_matrix(self, CouplingFactor) -> numpy.ndarray:
        """
        Compute supermode transfert matrix with coupling coefficients
        """

        shape = self.Beta.shape
        M = numpy.zeros([shape[0], shape[1], shape[1]])
        for iter in range(shape[0]):
            beta = self.Beta[iter]
            M[iter] = CouplingFactor[iter] * self.Coupling[iter] + beta * numpy.identity(shape[1])

        return M

    def compute_coupling_factor(self, Length: float) -> float:
        """
        Compute coupling factor
        """

        dx = Length / (self.geometry.itr_list.size)

        ditr = numpy.gradient(numpy.log(self.geometry.itr_list), 1)

        return ditr / dx

    def Propagate(self, Amplitude=[1, 1, 0, 0, 0], Length=1000, **kwargs) -> numpy.ndarray:
        """
        Plot coupling value of each mode as a function of itr

        Args:
            Amplitude: Initial amplitude of the propagation.
            Length: Length of the coupler for propagation.

        """

        Amplitude = numpy.asarray(Amplitude)

        Distance = numpy.linspace(0, Length, self.itr_list.size)

        # Factor = self.compute_coupling_factor(Length)

        # M = self.ComputeM(CouplingFactor=Factor)

        Minterp = interp1d(Distance, self.Matrix, axis=-1)

        def foo(t, y):
            return 1j * Minterp(t).dot(y)

        sol = solve_ivp(foo,
                        y0=Amplitude.astype(complex),
                        t_span=[0, Length],
                        method='RK45', **kwargs)

        return sol.y

    def _Propagate(self, Amplitude, Length, **kwargs):
        Amplitude = numpy.asarray(Amplitude)

        Distance = numpy.linspace(0, Length, self.geometry.itr_list.size)

        Factor = self.compute_coupling_factor(Length)

        M = self.ComputeM(CouplingFactor=Factor)

        Minterp = interp1d(Distance, M, axis=0)

        def foo(t, y):
            return 1j * Minterp(t).dot(y)

        sol = solve_ivp(foo,
                        y0=Amplitude.astype(complex),
                        t_span=[0, Length],
                        method='RK45',
                        **kwargs)

        return sol

    def append_supermode(self, **kwargs) -> None:
        """
        Add a supermode to the SuperSet list of supermodes.
        """

        superMode = SuperMode(parent_set=self, **kwargs)

        self.SuperModes.append(superMode)

    def __getitem__(self, N):
        return self.SuperModes[N]

    def __setitem__(self, N, val):
        self.SuperModes[N] = val

    def _interpret_itr_slice_list_(self, slice_list: list, itr_list: list):
        slice_list = [*slice_list, *self.itr_to_slice(itr_list)]

        if len(slice_list) == 0:
            slice_list = [0, -1]

        itr_list = self.slice_to_itr(slice_list)

        itr_list = numpy.sort(itr_list)[::-1]

        return self.itr_to_slice(itr_list), itr_list

    @staticmethod
    def single_plot(plot_function):
        def wrapper(self, *args, **kwargs):
            figure = Scene2D(unit_size=(10, 4))
            ax = Axis(row=0, col=0)
            figure.add_axes(ax)
            plot_function(self, ax=ax, *args, **kwargs)

            return figure

        return wrapper

    @single_plot
    def plot_index(self, ax: Axis) -> Scene2D:
        """
         Plot effective index for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        for mode in self.SuperModes:
            y = mode.index.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.name}')
            ax.add_artist(artist)
            ax.set_style(style_dict=mode.index.plot_style)

    @single_plot
    def plot_beta(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        for mode in self.SuperModes:
            y = mode.betas.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.name}')
            ax.add_artist(artist)
            ax.set_style(style_dict=mode.betas.plot_style)

    @single_plot
    def plot_coupling(self, ax: Axis, mode_of_interest: list = None) -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        if mode_of_interest is None:
            mode_of_interest = self.SuperModes

        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if not mode_0.is_computation_compatible(mode_1):
                continue

            y = mode_0.coupling.get_values(other=mode_1)
            artist = Line(x=self.itr_list, y=y, label=f'{mode_0.name} - {mode_1.name}')
            ax.add_artist(artist)
            ax.set_style(style_dict=mode_0.coupling.plot_style)

    @single_plot
    def plot_adiabatic(self, ax: Axis, mode_of_interest: list = None) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        if mode_of_interest is None:
            mode_of_interest = self.SuperModes

        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if not mode_0.is_computation_compatible(mode_1):
                continue

            y = mode_0.adiabatic.get_values(other=mode_1)
            artist = Line(x=self.itr_list, y=y, label=f'{mode_0.name} - {mode_1.name}')
            ax.add_artist(artist)
            ax.set_style(style_dict=mode_0.adiabatic.plot_style)

    def plot_field(self, itr_list: list[float] = [], slice_list: list[int] = []) -> Scene2D:
        """
        Plot each of the mode field for different itr value or slice number.

        Args:
            itr: List of itr value to evaluate the mode field.
            slice: List of integer reprenting the slice where the mode field is evaluated.
        """

        figure = Scene2D(unit_size=(3, 3))

        slice_list, itr_list = self._interpret_itr_slice_list_(slice_list, itr_list)

        for m, mode in enumerate(self.SuperModes):
            for n, (itr, slice) in enumerate(zip(itr_list, slice_list)):
                ax = Axis(row=n, col=m, title=f'{mode.name}\n[slice: {slice}  ITR: {itr:.2f}]')
                ax.colorbar = ColorBar(symmetric=True, position='right')

                x, y, field = mode.fields.get_field_with_boundaries(slice=slice)

                artist = Mesh(x=x, y=y, scalar=field, colormap=CMAP.BKR)

                ax.add_artist(artist)

                ax.set_style(style_dict=mode.fields.plot_style)
                figure.add_axes(ax)

        return figure

    def plot(self, type: str, **kwargs) -> Scene2D:
        """
        Generic plot function.

        Args:
            type: Plot type ['index', 'beta', 'adiabatic', 'coupling', 'field']
        """

        assert type.lower() in (type_list := ['index', 'beta', 'adiabatic', 'coupling', 'field']), f'type [{type}] as to be in {type_list}'

        match type.lower():
            case 'index':
                return self.plot_index(**kwargs)
            case 'beta':
                return self.plot_beta(**kwargs)
            case 'coupling':
                return self.plot_coupling(**kwargs)
            case 'adiabatic':
                return self.plot_adiabatic(**kwargs)
            case 'field':
                return self.plot_field(**kwargs)

    def generate_report(self,
                        filename: str = "report",
                        itr_list: list[float] = [],
                        slice_list: list[int] = [],
                        dpi: int = 200,
                        mode_of_interest: list = None) -> None:
        """
        Generate a full report of the coupler properties as a .pdf file

        :param      filename:          Name of the Report file to be outputed.
        :type       filename:          str
        :param      itr_list:          List of itr value to evaluate the mode field.
        :type       itr_list:          Array
        :param      slice_list:        List of slice value to evaluate the mode field.
        :type       slice_list:        Array
        :param      dpi:               Pixel density for the image included in the report.
        :type       dpi:               int
        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   { description_of_the_return_value }
        :rtype:     None
        """
        figures = []
        figures.append(self.geometry.plot()._render_())

        figures.append(self.plot_field(itr_list=itr_list, slice_list=slice_list)._render_())

        figures.append(self.plot_index()._render_())

        figures.append(self.plot_beta()._render_())

        figures.append(self.plot_coupling(mode_of_interest=mode_of_interest)._render_())

        figures.append(self.plot_adiabatic(mode_of_interest=mode_of_interest)._render_())

        # directory = os.path.join(Directories.ReportPath, filename) + '.pdf'

        directory = f"{os.getcwd()}/{filename}.pdf"

        logging.info(f'Saving report to {directory}')

        Multipage(directory, figs=figures, dpi=dpi)

        for figure in figures:
            figure.close()


# -
