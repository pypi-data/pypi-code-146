#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""LISA Orbits module."""

import importlib_metadata

from .orbits import Orbits
from .orbits import StaticConstellation
from .orbits import EqualArmlengthOrbits
from .orbits import KeplerianOrbits
from .orbits import OEMOrbits
from .orbits import InterpolatedOrbits
from .orbits import ResampledOrbits


try:
    metadata = importlib_metadata.metadata('lisaorbits').json
    __version__ = importlib_metadata.version('lisaorbits')
    __author__ = metadata['author']
    __email__ = metadata['author_email']
except importlib_metadata.PackageNotFoundError:
    pass
