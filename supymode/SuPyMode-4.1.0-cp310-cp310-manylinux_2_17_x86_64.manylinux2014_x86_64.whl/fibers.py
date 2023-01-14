#!/usr/bin/env python
# -*- coding: utf-8 -*-


from dataclasses import dataclass
import numpy
from FiberFusing import Circle

from PyOptik import ExpData


def core_index_to_NA(nCore, nClad):
    return numpy.sqrt(nCore**2 - nClad**2)


def NA_to_core_index(NA, nClad):
    return numpy.sqrt(NA**2 + nClad**2)


def AddFiber(Cores, Fiber, Angles, radius):
    for angle in Angles:
        if angle is None:
            P = (0, 0)
        else:
            P = (radius * numpy.cos(angle * numpy.pi / 180), radius * numpy.sin(angle * numpy.pi / 180))
        Cores += Fiber.Get(position=P)


class GenericFiber():
    @property
    def silica_index(self):
        return ExpData('FusedSilica').GetRI(self.wavelength)


@dataclass
class Fiber_DCF1300S_20(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.12, self.clad_index)
        self.clad_radius = 19.9 / 2
        self.core_radius = 4.6

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_DCF1300S_33(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.125, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_New_A(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_New_B(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.115, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_2028M24(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.19, self.silica_index)
        self.core_index = NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 14.1 / 2
        self.core_radius = 2.3 / 2


@dataclass
class Fiber_2028M21(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.19, self.silica_index)
        self.core_index = NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 17.6 / 2
        self.core_radius = 2.8 / 2


@dataclass
class FiberC(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.115, self.clad_index)
        self.clad_radius = 30 / 2
        self.core_radius = 9.1 / 2

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class FiberD(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.11, self.silica_index)
        self.core_index = NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 28 / 2
        self.core_radius = 9.3 / 2

    def get_geometry(self, position):
        self.Fiber = [Circle(position=position, radius=self.clad_radius, index=self.clad_index),
                      Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_2028M12(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = NA_to_core_index(0.19, self.silica_index)
        self.core_index = NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 25.8 / 2
        self.core_radius = 4.1 / 2


@dataclass
class Fiber_SMF28(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.NA = 0.12
        self.clad_index = self.silica_index
        self.core_index = self.clad_index + 0.005  # NA_to_core_index( 0.14, self.clad_index )
        self.clad_radius = 62.5
        self.core_radius = 4.1

    def get_geometry(self, position: list):
        self.Fiber = [Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


@dataclass
class Fiber_630HP(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.NA = 0.12
        self.clad_index = self.silica_index
        self.core_index = NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 62.5
        self.core_radius = 3.5 / 2.

    def get_geometry(self, position: list):
        self.Fiber = [Circle(position=position, radius=self.core_radius, index=self.core_index)]
        return self.Fiber


# -
