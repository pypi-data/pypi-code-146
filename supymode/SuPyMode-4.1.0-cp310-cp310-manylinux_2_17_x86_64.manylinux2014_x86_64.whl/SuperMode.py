# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# Built-in imports
import numpy
from dataclasses import dataclass

# Local imports
from SuPyMode.Tools import representations


@dataclass
class SuperMode(object):
    """
    .. note::
        This class is a representation of the fiber optic structures SuperModes.
        Those mode belongs to a SuperSet class and are constructed with the SuPySolver.
        It links to c++ SuperMode class.
    """
    parent_set: None
    """SuperSet to which is associated the computed this mode"""
    cpp_solver: None
    """c++ solver to which is linked this binded mode"""
    binding_number: int
    """Number which bind this mode to a specific c++ mode"""
    solver_number: int
    """Number which bind this mode to a specific python solver"""
    mode_number: int
    """Unique number associated to this mode"""

    def __post_init__(self):
        self.binding = self.cpp_solver.get_mode(self.binding_number)
        self.ID = [self.solver_number, self.binding_number]
        self.name = f"Mode {self.ID[0]}:{self.ID[1]}"
        self.fields = representations.Field(parent_supermode=self)
        self.index = representations.Index(parent_supermode=self)
        self.betas = representations.Beta(parent_supermode=self)
        self.coupling = representations.Coupling(parent_supermode=self)
        self.adiabatic = representations.Adiabatic(parent_supermode=self)

    @property
    def right_boundary(self) -> str:
        return self.cpp_solver.right_boundary

    @property
    def bottom_boundary(self) -> str:
        return self.cpp_solver.bottom_boundary

    @property
    def top_boundary(self) -> str:
        return self.cpp_solver.top_boundary

    @property
    def left_boundary(self) -> str:
        return self.cpp_solver.left_boundary

    @property
    def size(self) -> int:
        return len(self.parent_set.itr_list)

    @property
    def geometry(self) -> object:
        return self.parent_set.geometry

    @property
    def itr_list(self) -> numpy.ndarray:
        return self.parent_set.itr_list

    @property
    def axes(self) -> object:
        return self.parent_set.axes

    @property
    def y_axis(self) -> numpy.ndarray:
        return self.axes.y.vector

    @property
    def x_axis(self) -> numpy.ndarray:
        return self.axes.x.vector

    @property
    def boundaries(self) -> dict:
        return {'bottom': self.bottom_boundary, 'right': self.right_boundary, 'top': self.top_boundary, 'left': self.left_boundary}

    def is_computation_compatible(self, other):
        if self.ID == other.ID or self.solver_number != other.solver_number:
            return False
        else:
            return True


# -
