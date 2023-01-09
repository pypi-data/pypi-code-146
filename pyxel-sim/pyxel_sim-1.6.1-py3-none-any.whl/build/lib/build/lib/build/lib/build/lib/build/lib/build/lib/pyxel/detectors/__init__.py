#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""The detector attribute and data structure subpackage."""

# flake8: noqa
# Warning: Import order matters
from .readout_properties import ReadoutProperties
from .environment import Environment
from .detector import Detector
from .geometry import Geometry
from .characteristics import Characteristics
from .ccd import CCDGeometry, CCD, CCDCharacteristics
from .mkid import MKID, MKIDGeometry, MKIDCharacteristics
from .apd import APD, APDCharacteristics, APDGeometry
from .cmos import CMOSGeometry, CMOS, CMOSCharacteristics
from .optics import Optics
