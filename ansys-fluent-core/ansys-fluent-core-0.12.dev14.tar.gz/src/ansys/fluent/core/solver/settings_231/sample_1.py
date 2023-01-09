#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .injections_1 import injections
from .boundaries import boundaries
from .lines_1 import lines
from .planes import planes
from .op_udf import op_udf
from .append_sample import append_sample
from .accumulate_rates import accumulate_rates
class sample(Command):
    """
    'sample' command.
    
    Parameters
    ----------
        injections : typing.List[str]
            'injections' child.
        boundaries : typing.List[str]
            'boundaries' child.
        lines : typing.List[str]
            'lines' child.
        planes : typing.List[str]
            'planes' child.
        op_udf : str
            'op_udf' child.
        append_sample : bool
            'append_sample' child.
        accumulate_rates : bool
            'accumulate_rates' child.
    
    """

    fluent_name = "sample"

    argument_names = \
        ['injections', 'boundaries', 'lines', 'planes', 'op_udf',
         'append_sample', 'accumulate_rates']

    injections: injections = injections
    """
    injections argument of sample.
    """
    boundaries: boundaries = boundaries
    """
    boundaries argument of sample.
    """
    lines: lines = lines
    """
    lines argument of sample.
    """
    planes: planes = planes
    """
    planes argument of sample.
    """
    op_udf: op_udf = op_udf
    """
    op_udf argument of sample.
    """
    append_sample: append_sample = append_sample
    """
    append_sample argument of sample.
    """
    accumulate_rates: accumulate_rates = accumulate_rates
    """
    accumulate_rates argument of sample.
    """
