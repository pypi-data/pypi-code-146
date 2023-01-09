#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file import file
from .mesh import mesh
from .server import server
from .setup import setup
from .solution import solution
from .results import results
from .parametric_studies import parametric_studies
from .current_parametric_study import current_parametric_study
from .parallel_1 import parallel
from .report_1 import report
from .exit import exit
class root(Group):
    """
    'root' object.
    """

    fluent_name = ""

    child_names = \
        ['file', 'mesh', 'server', 'setup', 'solution', 'results',
         'parametric_studies', 'current_parametric_study', 'parallel',
         'report']

    file: file = file
    """
    file child of root.
    """
    mesh: mesh = mesh
    """
    mesh child of root.
    """
    server: server = server
    """
    server child of root.
    """
    setup: setup = setup
    """
    setup child of root.
    """
    solution: solution = solution
    """
    solution child of root.
    """
    results: results = results
    """
    results child of root.
    """
    parametric_studies: parametric_studies = parametric_studies
    """
    parametric_studies child of root.
    """
    current_parametric_study: current_parametric_study = current_parametric_study
    """
    current_parametric_study child of root.
    """
    parallel: parallel = parallel
    """
    parallel child of root.
    """
    report: report = report
    """
    report child of root.
    """
    command_names = \
        ['exit']

    exit: exit = exit
    """
    exit command of root.
    """
