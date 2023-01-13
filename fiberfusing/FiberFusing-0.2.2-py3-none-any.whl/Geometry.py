# Third-party imports
import numpy
from dataclasses import dataclass
from PIL import Image

# MPSPlots imports
import MPSPlots.CMAP
from MPSPlots.Render2D import Scene2D, ColorBar, Axis, Mesh, Polygon

# FiberFusing imports
import FiberFusing.Utils as Utils
from FiberFusing.Axes import Axes
from FiberFusing._buffer import BackGround


@dataclass
class Geometry(object):
    """
    Class represent the refractive index (RI) geometrique profile which
    can be used to retrieve the supermodes.
    """

    clad: object
    """ Geometrique object representing the fiber structure clad. """
    background: object
    """ Geometrique object representing the background (usually air). """
    cores: list
    """ List of geometrique object representing the fiber structure cores. """
    x_bound: list
    """ X boundary to render the structure [float, float, 'auto', 'auto right', 'auto left']. """
    y_bound: list
    """ Y boundary to render the structure [float, float, 'auto', 'auto top', 'auto bottom']. """
    n_x: int = 100
    """ Number of point (x-direction) to evaluate the rendering """
    n_y: int = 100
    """ Number of point (y-direction) to evaluate the rendering """
    index_scrambling: float = 0
    """ Index scrambling for degeneracy lifting """
    resize_factor: int = 5
    """ Oversampling factor for gradient evaluation """

    def __post_init__(self):
        self.object_list = [self.background, self.clad, *self.cores]
        self._mesh = None
        self._gradient = None

        self.x_bound = self.interpret_x_bound(x_bound=self.x_bound)

        self.y_bound = self.interpret_y_bound(y_bound=self.y_bound)

        self.generate_axis()

        self.Indices = self.get_index_range()

    def generate_axis(self) -> None:
        """
        Generate the normal and upscaled mesh.
        """
        self.axes = Axes(x_bound=self.x_bound,
                         y_bound=self.y_bound,
                         n_x=self.n_x,
                         n_y=self.n_y)

        self.upscale_axes = Axes(x_bound=self.x_bound,
                                 y_bound=self.y_bound,
                                 n_x=self.n_x * self.resize_factor,
                                 n_y=self.n_y * self.resize_factor)

    def interpret_x_bound(self, x_bound: list) -> list:
        """
        Interpret the x_bound parameter.
        If the parameter is in ["auto", "auto-left", "auto-right"], it returns
        an auto-evaluated boundary

        :param      x_bound:  The x boundary to be interpreted
        :type       x_bound:  list

        :returns:   The interpreted x boundary
        :rtype:     list
        """
        if isinstance(self.y_bound, str):
            string_x_bound = self.x_bound.lower()
            minx, _, maxx, _ = self.clad.bounds
            auto_x_bound = numpy.array([minx, maxx]) * 1.3

            match string_x_bound:
                case 'auto':
                    return auto_x_bound
                case 'auto-right':
                    return [0, auto_x_bound[1]]
                case 'auto-left':
                    return [auto_x_bound[0], 0]

        else:
            return self.x_bound

    def interpret_y_bound(self, y_bound: list) -> list:
        """
        Interpret the y_bound parameter.
        If the parameter is in ["auto", "auto-top", "auto-bottom"], it returns
        an auto-evaluated boundary

        :param      y_bound:  The y boundary to be interpreted
        :type       y_bound:  list

        :returns:   The interpreted y boundary
        :rtype:     list
        """
        if isinstance(self.y_bound, str):
            string_y_bound = self.y_bound.lower()
            _, min_y, _, max_y = self.clad.bounds
            auto_y_bound = numpy.array([min_y, max_y]) * 1.3

            match string_y_bound:
                case 'auto':
                    return auto_y_bound
                case 'auto-top':
                    return [0, auto_y_bound[1]]
                case 'auto-bottom':
                    return [auto_y_bound[0], 0]

        else:
            return self.y_bound

    def get_gradient_mesh(self, mesh: numpy.ndarray, Axes: Axes) -> numpy.ndarray:
        """
        Returns the gradient to the 4th degree of the provided mesh.

        :param      mesh:  The mesh to which compute the gradient
        :type       mesh:  numpy.ndarray
        :param      Axes:  The axis associated to the mesh.
        :type       Axes:  Axes

        :returns:   The gradient of the mesh.
        :rtype:     numpy.ndarray
        """
        Ygrad, Xgrad = Utils.gradientO4(mesh, Axes.x.d, Axes.y.d)

        gradient = (Xgrad * Axes.x.mesh + Ygrad * Axes.y.mesh)

        return gradient

    @property
    def mesh(self) -> numpy.ndarray:
        if self._mesh is None:
            self._mesh, _, self._gradient, _ = self.generate_mesh()
        return self._mesh

    @property
    def gradient(self) -> numpy.ndarray:
        if self._gradient is None:
            self._mesh, _, self._gradient, _ = self.generate_mesh()
        return self._gradient

    @property
    def max_index(self) -> float:
        return max([obj.index for obj in self.object_list])[0]

    @property
    def min_index(self) -> float:
        return min([obj.index for obj in self.object_list])[0]

    @property
    def max_x(self) -> float:
        return self.axes.x.bounds[0]

    @property
    def min_x(self) -> float:
        return self.axes.x.bounds[1]

    @property
    def max_y(self) -> float:
        return self.axes.y.bounds[0]

    @property
    def min_y(self) -> list:
        return self.axes.y.bounds[1]

    @property
    def shape(self) -> list:
        return numpy.array([self.axes.y.n,
                            self.axes.x.n])

    def get_index_range(self) -> list:
        """
        Returns the list of all index associated to the element of the geometry.
        """
        return [float(obj.index) for obj in self.object_list]

    def rotate(self, angle: float) -> None:
        """
        Rotate the full geometry

        :param      angle:  Angle to rotate the geometry, in degrees.
        :type       angle:  float
        """
        for obj in self.object_list:
            obj = obj.rotate(angle=angle)

    def get_downscale_array(self, array: numpy.ndarray, shape: list) -> numpy.ndarray:
        """
        Gets the same array down-scaled to the given shape.

        :param      array:  The array to down-scale.
        :type       array:  numpy.ndarray
        :param      size:   The shape of the output array.
        :type       size:   list

        :returns:   The downscale array.
        :rtype:     { return_type_description }
        """
        array = Image.fromarray(array)

        return numpy.asarray(array.resize(shape, resample=Image.Resampling.BOX))

    def rasterize_polygons(self, coordinates: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        """
        Returns the rasterize mesh of the object.

        :param      coordinates:  The coordinates to which evaluate the mesh.
        :type       coordinates:  { type_description }
        :param      n_x:          The number of point in the x direction
        :type       n_x:          int
        :param      n_y:          The number of point in the y direction
        :type       n_y:          int

        :returns:   The rasterized mesh
        :rtype:     numpy.ndarray
        """
        mesh = numpy.zeros([n_x, n_y]).T

        for polygone in self.object_list:
            raster = polygone.get_rasterized_mesh(coordinate=coordinates, n_x=n_x, n_y=n_y).astype(numpy.float64)

            rand = (numpy.random.rand(1) - 0.5) * self.index_scrambling

            raster *= polygone.index + rand

            mesh[numpy.where(raster != 0)] = 0

            mesh += raster

        return mesh

    def generate_mesh(self) -> numpy.ndarray:
        self.coords = numpy.vstack((self.upscale_axes.x.mesh.flatten(), self.upscale_axes.y.mesh.flatten())).T

        upscale_mesh = self.rasterize_polygons(coordinates=self.coords, n_x=self.upscale_axes.x.n, n_y=self.upscale_axes.y.n)

        mesh = self.get_downscale_array(array=upscale_mesh, shape=self.axes.shape)

        upscale_gradient = self.get_gradient_mesh(mesh=upscale_mesh**2, Axes=self.upscale_axes)

        gradient = self.get_downscale_array(array=upscale_gradient, shape=self.axes.shape)

        return mesh, upscale_mesh, gradient, upscale_gradient

    def _render_patch_mesh_(self, ax: Axis) -> None:
        """
        Add the patch representation of the geometry into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(log_norm=True,
                            position='right',
                            numeric_format='%.1e',
                            symmetric=True)

        for polygon in self.object_list:
            if isinstance(polygon, BackGround):
                continue

            artist = Polygon(x=self.axes.x.vector,
                             y=self.axes.y.vector,
                             instance=polygon._shapely_object)

            ax.add_artist(artist)

        ax.colorbar = colorbar
        ax.x_label = r'x [$\mu m$]'
        ax.y_label = r'y [$\mu m$]'
        ax.title = 'Coupler index structure'

    def _render_raster_gradient_(self, ax: Axis) -> None:
        """
        Add the rasterized representation of the gradient of the geometrys into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(log_norm=True,
                            position='right',
                            numeric_format='%.1e',
                            symmetric=True)

        artist = Mesh(x=self.axes.x.vector,
                      y=self.axes.y.vector,
                      scalar=self.gradient,
                      colormap=MPSPlots.CMAP.BWR)

        ax.colorbar = colorbar
        ax.x_label = r'x [$\mu m$]'
        ax.y_label = r'y [$\mu m$]'
        ax.title = 'Refractive index gradient'
        ax.add_artist(artist)

    def _render_raster_mesh_(self, ax: Axis) -> None:
        """
        Add the rasterized representation of the geometry into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(discreet=True,
                            position='right',
                            numeric_format='%.4f')

        artist = Mesh(x=self.axes.x.vector,
                      y=self.axes.y.vector,
                      scalar=self.mesh,
                      colormap='Blues')

        ax.colorbar = colorbar
        ax.x_label = r'x [$\mu m$]'
        ax.y_label = r'y [$\mu m$]'
        ax.title = 'Rasterized mesh'
        ax.add_artist(artist)

    def plot(self) -> None:
        """
        Plot the different representations [patch, raster-mesh, raster-gradient]
        of the geometry.
        """
        figure = Scene2D(unit_size=(4, 4), tight_layout=True)

        ax0 = Axis(row=0, col=0)

        ax1 = Axis(row=0, col=1)

        ax2 = Axis(row=0, col=2)

        self._render_patch_mesh_(ax0)
        self._render_raster_mesh_(ax1)
        self._render_raster_gradient_(ax2)

        figure.add_axes(ax0, ax1, ax2)

        return figure

# -
