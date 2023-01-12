from __future__ import annotations
__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from typing import Optional, TYPE_CHECKING

from easyCore.Objects.ObjectClasses import BaseObj, Parameter
from easyCrystallography.Symmetry.SymOp import SymOp

if TYPE_CHECKING:
    from easyCore.Utils.typing import iF


class VectorField(BaseObj):
    _name = "vector_field"
    _defaults = {
        'value': {'value': 1.0, 'units': 'tesla', 'fixed': True},
        'rotation': [0., 0., 1.]
    }

    def __init__(self,
                 value: Optional[Parameter, float] = None,
                 rotation: Optional[SymOp] = None,
                 interface: Optional[iF] = None):
        super().__init__(self._name,
                         value=Parameter(**self._defaults["value"]))
        if value is not None:
            self.value = value
        self.interface = interface