#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

# # type: ignore  # Have mypy ignore the whole file for now.
# pylint: skip-file

"""MyPy Plugin to let it know of the variations it should expect from the model."""
# noinspection SpellCheckingInspection
# pylint: disable=unused-import
# TODO: Clean-up imports once the plug-in works.

from typing import (
    Optional,
    Callable,
    Union
)

import sys
import logging

import coloredlogs      # type: ignore

from mypy.plugin import (
    Plugin,
    ClassDefContext,
    CheckerPluginInterface,
    SemanticAnalyzerPluginInterface,
)
from mypy.options import Options
from mypy.plugins.attrs import (
    attr_class_makers,
    attr_attrib_makers,
    attr_class_maker_callback,
    attr_dataclass_makers,
)
from mypy.nodes import (
    Node,
    TypeInfo,
    FuncBase,
    SymbolNode,
)
from mypy.types import (
    Instance,
)
from mypy.lookup import lookup_fully_qualified
# from mypy.semanal import set_callable_name


from budosystems.models.meta import BudoMeta

# Debug logging
log = logging.getLogger(__name__)
formatter = coloredlogs.ColoredFormatter('%(funcName)s: %(message)s')
log.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)
log.addHandler(console)


def fully_qualified_class_name(cls: Union[object, type]) -> str:
    """Returns the fully qualified class name of the provided object or class."""
    log.debug(f"{cls=}")
    if not isinstance(cls, type):
        cls = type(cls)
    value = f"{cls.__module__}.{cls.__qualname__}"
    log.debug(f"{value=}")
    return value


BUDO_META_FQCN = fully_qualified_class_name(BudoMeta)
attr_class_makers.add(BUDO_META_FQCN+".__new__")


class BudoModelPlugin(Plugin):
    """Implementation of MyPy Plugin specialized for Budo Systems models."""

    def __init__(self, options: Options):
        super().__init__(options)
        self._bmti: Optional[Node] = None

    def get_metaclass_hook(self, fullname: str
                           ) -> Optional[Callable[[ClassDefContext], None]]:
        # if fullname == BUDO_META_FQCN:
        if fullname.startswith("budosystems."):
            log.debug(f"{fullname=}")
            log.debug("Sending handler")
            return budo_meta_handler
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        # log.info(f"{fullname=}")
        sym = self.lookup_fully_qualified(fullname)
        if sym and self.BUDO_META_TYPE_INFO and isinstance(sym.node, TypeInfo):
            mcs: Optional[Instance] = sym.node.calculate_metaclass_type()
            log.debug(f"{sym.node=}, {mcs=}")
            if mcs and mcs.type == self.BUDO_META_TYPE_INFO:
                log.debug(f"{sym=}, {sym.node=}")
                log.debug("Sending handler")
                return budo_class_handler
            if any(base == self.BUDO_META_TYPE_INFO for base in sym.node.mro):
                log.debug(f"{sym.node.mro=}")
                return budo_class_handler
        return None

    @property
    def BUDO_META_TYPE_INFO(self) -> Optional[Node]:
        """If available, returns the :class:`TypeInfo` for :class:`BudoMeta`."""
        if not self._bmti:
            stn = self.lookup_fully_qualified(BUDO_META_FQCN)
            if stn:
                self._bmti = stn.node
                log.debug(f"{self._bmti}")
        return self._bmti


# Callbacks
def budo_meta_handler(ctx: ClassDefContext) -> None:
    """Callback function to process classes that have :class:`BuduMeta` as a metaclass."""
    log.debug(f"About the metaclass:")
    log.debug(f"{ctx.cls.info=!s}")
    log.debug(f"{ctx.cls.decorators=!s}")
    # log.debug(f"{ctx.cls.defs=!s}")
    # log.debug(f"{ctx.reason=}")


def budo_class_handler(ctx: ClassDefContext) -> None:
    """Callback function to process classes that have :class:`BuduMeta` as a metaclass."""
    log.debug(f"About the class:")
    log.debug(f"{ctx.cls.info=!s}")
    log.debug(f"{ctx.cls.decorators=!s}")
    log.debug(f"{ctx.cls.metaclass=!s}")
    ti: TypeInfo = ctx.cls.info
    log.debug(f"{ti.metaclass_type=}")
    # budo_meta_handler(ti.metaclass_type)


# Helpers


# Make this plugin accessible to the config file
def plugin(version: str) -> type[Plugin]:
    """Budo Systems model plugin for MyPy.

    :return: The :class:`BudoModelPlugin` class
    """
    log.info(f"Plugin {__name__} initialized for mypy {version}")
    return BudoModelPlugin
