"""Classiq SDK."""
from classiq.interface._version import VERSION as _VERSION
from classiq.interface.generator.arith.register_user_input import (  # noqa: F401
    RegisterUserInput,
)
from classiq.interface.generator.control_state import ControlState  # noqa: F401
from classiq.interface.generator.functions import *  # noqa: F401, F403
from classiq.interface.generator.functions import __all__ as _ifunc_all
from classiq.interface.generator.result import GeneratedCircuit  # noqa: F401

from classiq import (  # noqa: F401
    applications,
    builtin_functions,
    exceptions,
    execution,
    model,
)
from classiq._internals import _qfunc_ext  # noqa: F401
from classiq._internals import logger  # noqa: F401
from classiq._internals.async_utils import (
    enable_jupyter_notebook,
    is_notebook as _is_notebook,
)
from classiq._internals.authentication.authentication import authenticate  # noqa: F401
from classiq._internals.client import configure  # noqa: F401
from classiq._internals.config import Configuration  # noqa: F401
from classiq._internals.help import open_help  # noqa: F401
from classiq.analyzer import Analyzer  # noqa: F401
from classiq.executor import Executor  # noqa: F401
from classiq.model_designer import *  # noqa: F401, F403
from classiq.model_designer import __all__ as _md_all
from classiq.quantum_functions import *  # noqa: F401, F403
from classiq.quantum_functions import __all__ as _qfuncs_all
from classiq.quantum_register import *  # noqa: F401, F403
from classiq.quantum_register import __all__ as _qregs_all

__version__ = _VERSION

if _is_notebook():
    enable_jupyter_notebook()

_sub_modules = [
    "analyzer",
    "applications",
    "builtin_functions",
    "exceptions",
    "execution",
    "model",
    "open_help",
]

__all__ = (
    ["RegisterUserInput", "ControlState", "Analyzer", "Executor", "GeneratedCircuit"]
    + _qregs_all
    + _qfuncs_all
    + _md_all
    + _ifunc_all
    + _sub_modules
)


def __dir__():
    return __all__
