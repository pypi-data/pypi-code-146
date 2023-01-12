#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_3 import enable
from .beams import beams
from .statistics import statistics
from .sampling_iterations import sampling_iterations
from .index_of_refraction import index_of_refraction
from .report import report
from .verbosity_2 import verbosity
class optics(Group):
    """
    Enter the optics model menu.
    """

    fluent_name = "optics"

    child_names = \
        ['enable', 'beams', 'statistics', 'sampling_iterations',
         'index_of_refraction', 'report', 'verbosity']

    enable: enable = enable
    """
    enable child of optics.
    """
    beams: beams = beams
    """
    beams child of optics.
    """
    statistics: statistics = statistics
    """
    statistics child of optics.
    """
    sampling_iterations: sampling_iterations = sampling_iterations
    """
    sampling_iterations child of optics.
    """
    index_of_refraction: index_of_refraction = index_of_refraction
    """
    index_of_refraction child of optics.
    """
    report: report = report
    """
    report child of optics.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of optics.
    """
