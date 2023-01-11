# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Data Ingestion into the Switch Automation
=========================================

Complete package for ingestion data into the Switch Automation Platform.
"""

from . import models
from .models import api
from .models import step
from .models import guide
from .models import enums
from .models import literals

from . import exceptions
from . import tasks
from . import utils
from . import extensions
from .SwitchGuideTask import SwitchGuideTask

__all__ = [
    'models',
    'exceptions',
    'extensions',
    'tasks',
    'utils',
    'SwitchGuideTask',
    'api',
    'step',
    'guide',
    'literals',
    'enums'
]

__version__ = "0.1.16"
