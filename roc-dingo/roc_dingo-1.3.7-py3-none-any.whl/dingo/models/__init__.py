#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Mandatory code in every plugin.models __init__.py needed for alembic
### DO NOT EDIT

import importlib
import pkgutil
import os
import sys
from poppy.core.db.base import Base

pkg_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

# Creates a list of all the tables represented by classes in the current plugin
# It is needed for alembic to generate migrations correctly
tables = {
    cls.__tablename__: cls for cls in Base.__subclasses__()
    if sys.modules[__name__].__name__ in cls.__module__}

### End of mandatory code
