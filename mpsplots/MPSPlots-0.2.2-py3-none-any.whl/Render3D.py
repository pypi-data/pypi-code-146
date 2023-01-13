#   !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyvista
import numpy
import matplotlib


class Scene3D:
    def __init__(self,
                 shape: tuple = (1, 1),
                 unit_size: tuple = (800, 800),
                 window_size: tuple = None,
                 **kwargs):

        if window_size is None:
            window_size = (unit_size[1] * shape[1], unit_size[0] * shape[0])

        self.figure = pyvista.Plotter(theme=pyvista.themes.DocumentTheme(),
                                      window_size=window_size,
                                      shape=shape, **kwargs)

    def add_unstructured_mesh(self, coordinates: numpy.ndarray, scalar: numpy.ndarray = None, plot_number: tuple = (0, 0), **kwargs):
        self.figure.subplot(*plot_number)
        coordinates = numpy.array(coordinates).T
        points = pyvista.wrap(coordinates)
        self.figure.add_points(points, scalars=scalar, point_size=20, render_points_as_spheres=True, **kwargs)

    def add_mesh(self, coordinates: numpy.ndarray, plot_number: tuple = (0, 0), cmap='seismic', **kwargs):
        if isinstance(cmap, str):  # works only for matplotlib 3.6.1
            cmap = matplotlib.colormaps[cmap]

        self.figure.subplot(*plot_number)
        mesh = pyvista.StructuredGrid(*coordinates)

        self.figure.add_mesh(mesh=mesh, cmap=cmap, **kwargs)

        return self.figure

    def add_theta_vector_field(self, plot_number: list, Radius: float = 1.03 / 2):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        theta_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [1], [0], [0])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, Radius)

        spherical_vector.point_data["Theta"] = theta_vector * 0.1

        self.figure.add_mesh(spherical_vector.glyph(orient="Theta", scale="Theta", tolerance=0.005), color='k')

    def add_phi_vector_field(self, plot_number, Radius=1.03 / 2):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        Phi_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [0], [1], [0])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, Radius)

        spherical_vector.point_data["Phi"] = Phi_vector * 0.1

        self.figure.add_mesh(spherical_vector.glyph(orient="Phi", scale="Phi", tolerance=0.005), color='k')

    def add_r_vector_field(self, plot_number, R=[1.03 / 2]):
        self.figure.subplot(*plot_number)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        R_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, R, *[0, 0, 1])], axis=1)

        spherical_vector = pyvista.grid_from_sph_coords(theta, phi, R)

        spherical_vector.point_data["R"] = R_vector * 0.1

        self.figure.add_mesh(spherical_vector.glyph(orient="R", scale="R", tolerance=0.005), color='k')

    def __add_unit_sphere__(self, plot_number: tuple = (0, 0), **kwargs):
        self.figure.subplot(*plot_number)
        sphere = pyvista.Sphere(radius=1)
        self.figure.add_mesh(sphere, opacity=0.3)

    def __add_axes__(self, plot_number: tuple = (0, 0)):
        self.figure.subplot(*plot_number)
        self.figure.add_axes_at_origin(labels_off=True)

    def __add__text__(self, plot_number: tuple = (0, 0), text='', **kwargs):
        self.figure.subplot(*plot_number)
        self.figure.add_text(text, **kwargs)

    def show(self, SaveDir: str = None):
        self.figure.show(screenshot=SaveDir)

        return self

    def close(self):
        self.figure.close()
