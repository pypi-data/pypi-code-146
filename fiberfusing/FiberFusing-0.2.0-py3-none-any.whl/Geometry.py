import numpy
from dataclasses import dataclass
from PIL import Image
import MPSPlots.CMAP
from MPSPlots.Render2D import Scene2D, ColorBar, Axis, Mesh
import FiberFusing.Utils as Utils
from FiberFusing.Axes import Axes


@dataclass
class Geometry(object):
    """ Class represent the refractive index (RI) geometrique profile which
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
        self.Objects = [self.background, self.clad, *self.cores]
        self._mesh = None
        self._gradient = None

        minx, miny, maxx, maxy = self.clad.bounds

        if isinstance(self.x_bound, str):
            self._parse_x_bound_()

        if isinstance(self.y_bound, str):
            self._parse_y_bound_()

        self.axes = Axes(x_bound=self.x_bound, y_bound=self.y_bound, n_x=self.n_x, n_y=self.n_y)
        self.upscale_axes = Axes(x_bound=self.x_bound, y_bound=self.y_bound, n_x=self.n_x * self.resize_factor, n_y=self.n_y * self.resize_factor)
        self.compute_index_range()

    def _parse_x_bound_(self) -> None:
        string_x_bound = self.x_bound.lower()
        minx, _, maxx, _ = self.clad.bounds
        auto_x_bound = numpy.array([minx, maxx]) * 1.2

        match string_x_bound:
            case 'auto':
                self.x_bound = auto_x_bound
            case 'auto-right':
                self.x_bound = [0, auto_x_bound[1]]
            case 'auto-left':
                self.x_bound = [auto_x_bound[0], 0]

    def _parse_y_bound_(self) -> None:
        string_y_bound = self.y_bound.lower()
        _, min_y, _, max_y = self.clad.bounds
        auto_y_bound = numpy.array([min_y, max_y]) * 1.2

        match string_y_bound:
            case 'auto':
                self.y_bound = auto_y_bound
            case 'auto-top':
                self.y_bound = [0, auto_y_bound[1]]
            case 'auto-bottom':
                self.y_bound = [auto_y_bound[0], 0]

    def get_gradient_mesh(self, mesh: numpy.ndarray, Axes: Axes) -> numpy.ndarray:
        Ygrad, Xgrad = Utils.gradientO4(mesh**2, Axes.x.d, Axes.y.d)

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
        ObjectList = self.Objects
        return max([obj.index for obj in ObjectList])[0]

    @property
    def min_index(self) -> float:
        ObjectList = self.Objects
        return min([obj.index for obj in ObjectList])[0]

    @property
    def max_x(self) -> float:
        return self.axes.x.Bounds[0]

    @property
    def min_x(self) -> float:
        return self.axes.x.Bounds[1]

    @property
    def max_y(self) -> float:
        return self.axes.y.Bounds[0]

    @property
    def min_y(self) -> list:
        return self.axes.y.Bounds[1]

    @property
    def Shape(self) -> list:
        return numpy.array([self.axes.x.N, self.axes.y.N])

    def compute_index_range(self) -> None:
        self.Indices = []

        for obj in self.Objects:
            self.Indices.append(float(obj.index))

    def Rotate(self, angle: float) -> None:
        for obj in self.Objects:
            obj = obj.rotate(angle=angle)

    def get_downscale_array(self, array, size) -> numpy.ndarray:
        array = Image.fromarray(array)

        return numpy.asarray(array.resize(size, resample=Image.Resampling.BOX))

    def rasterize_polygons(self, coordinates: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        mesh = numpy.zeros([n_x, n_y])

        for polygone in self.Objects:
            raster = polygone.get_rasterized_mesh(coordinate=coordinates, n_x=n_x, n_y=n_y).astype(numpy.float64)

            rand = (numpy.random.rand(1) - 0.5) * self.index_scrambling

            raster *= polygone.index + rand

            mesh[numpy.where(raster != 0)] = 0

            mesh += raster

        return mesh

    def generate_mesh(self) -> numpy.ndarray:
        self.coords = numpy.vstack((self.upscale_axes.x.mesh.flatten(), self.upscale_axes.y.mesh.flatten())).T

        upscale_mesh = self.rasterize_polygons(coordinates=self.coords, n_x=self.upscale_axes.x.n, n_y=self.upscale_axes.y.n)

        mesh = self.get_downscale_array(array=upscale_mesh, size=self.axes.shape)

        upscale_gradient = self.get_gradient_mesh(mesh=upscale_mesh, Axes=self.upscale_axes)

        gradient = self.get_downscale_array(array=upscale_gradient, size=self.axes.shape)

        return mesh, upscale_mesh, gradient, upscale_gradient

    def plot(self) -> None:
        """
        Method plot the rasterized RI profile.
        """
        figure = Scene2D(unit_size=(6, 6), tight_layout=True)
        colorbar0 = ColorBar(discreet=True, position='right', numeric_format='%.4f')

        colorbar1 = ColorBar(log_norm=True, position='right', numeric_format='%.1e', symmetric=True)

        ax0 = Axis(row=0,
                   col=0,
                   x_label=r'x [$\mu m$]',
                   y_label=r'y [$\mu m$]',
                   title='Refractive index structure',
                   show_legend=False,
                   colorbar=colorbar0)

        ax1 = Axis(row=0,
                   col=1,
                   x_label=r'x [$\mu m$]',
                   y_label=r'y [$\mu m$]',
                   title='Refractive index gradient',
                   show_legend=False,
                   colorbar=colorbar1)

        artist = Mesh(x=self.axes.x.vector, y=self.axes.y.vector, scalar=self.mesh, colormap='Blues')

        gradient = Mesh(x=self.axes.x.vector, y=self.axes.y.vector, scalar=self.gradient, colormap=MPSPlots.CMAP.BWR)

        ax0.add_artist(artist)
        ax1.add_artist(gradient)

        figure.add_axes(ax0, ax1)

        return figure

# -
