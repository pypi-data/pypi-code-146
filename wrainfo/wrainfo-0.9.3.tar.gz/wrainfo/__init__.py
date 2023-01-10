"""Top-level package for WRaINfo."""

# WRaINfo, Is a software to process FURUNO weather radar data.
#
# Copyright (c) 2023, FernLab (GFZ Potsdam, fernlab@gfz-potsdam.de)
#
# This software was developed within the context of the RaINfo ("Potential use of
# high resolution weather data in agriculture") project of FernLab funded by
# the Impulse and Networking Fund of the Helmholtz Association.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# package owner
__author__ = """FernLab"""
__email__ = 'fernlab@gfz-potsdam.de'

# import version
from .version import __version__, __versionalias__   # noqa (E402 + F401)

# import subpackages
from wrainfo import attenuation_corr
from wrainfo import clutter
from wrainfo import compression
from wrainfo import error_flist
from wrainfo import geometry
from wrainfo import precipitation
from wrainfo import process_chains
from wrainfo import reader

__all__ = [
    'attenuation_corr',
    'clutter',
    'compression',
    'error_flist',
    'geometry',
    'precipitation',
    'process_chains',
    'reader'
]
