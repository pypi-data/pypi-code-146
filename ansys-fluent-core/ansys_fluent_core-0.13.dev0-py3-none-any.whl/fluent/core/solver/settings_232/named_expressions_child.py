#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .definition import definition
from .description import description
from .parameterid import parameterid
from .parametername import parametername
from .unit import unit
from .input_parameter import input_parameter
from .output_parameter import output_parameter
from .get_value import get_value
class named_expressions_child(Group):
    """
    'child_object_type' of named_expressions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'definition', 'description', 'parameterid', 'parametername',
         'unit', 'input_parameter', 'output_parameter']

    name: name = name
    """
    name child of named_expressions_child.
    """
    definition: definition = definition
    """
    definition child of named_expressions_child.
    """
    description: description = description
    """
    description child of named_expressions_child.
    """
    parameterid: parameterid = parameterid
    """
    parameterid child of named_expressions_child.
    """
    parametername: parametername = parametername
    """
    parametername child of named_expressions_child.
    """
    unit: unit = unit
    """
    unit child of named_expressions_child.
    """
    input_parameter: input_parameter = input_parameter
    """
    input_parameter child of named_expressions_child.
    """
    output_parameter: output_parameter = output_parameter
    """
    output_parameter child of named_expressions_child.
    """
    query_names = \
        ['get_value']

    get_value: get_value = get_value
    """
    get_value query of named_expressions_child.
    """
