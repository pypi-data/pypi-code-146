# stdlib imports
from enum import Enum

# third party imports
import numpy as np


class Zone(Enum):
    A = "A"
    B = "B"
    C = "C"


# This code is developed from the paper
# "NGA-Sub source and path database", Contreras et. al., 2022, Earthquake Spectra
# DOI: 10.1177/87552930211065054
# While the authors are presenting a database, not an algorithm, we took the
# description of the database creation-process as closely as possible.
# Note that the authors say "Following these initial classifications,
# event types were checked based on human interpretation."
# At the time of this writing, the differences between the results of this
# implementation of the algorithm and the database created by the authors are great
# enough that we decided it would be less confusing to output these results in the code.
# We will likely revive and modify this function at some point in the future.


class Category(Enum):
    INTERFACE = "interface"
    SLAB = "slab"
    CRUSTAL = "crustal"
    OUTER_RISE = "outer rise"
    UNDETERMINED = "undetermined"
    CRUSTAL_UNCERTAIN = "crustal uncertain"
    INTERFACE_UNCERTAIN = "interface uncertain"
    SLAB_UNCERTAIN = "slab uncertain"
    OUTER_RISE_UNCERTAIN = "outer rise uncertain"


class Focal(Enum):
    RS = "RS"
    SS = "SS"
    NM = "NM"
    ALL = "ALL"


BOUNDARY_DELTA = 5
DIST_THRESHOLD = 10
MIN_SLAB_DEPTH = 10
MAX_INTERFACE_DEPTH = 60
MAX_CRUSTAL_DEPTH = 30
SUBDUCTION_REGION = "Subduction"


def nga_categorize(eqinfo, input_strec_info):
    """Assign subduction zone categories according to Contreras et al 2022.

    DOI for full paper:
    DOI: 10.1177/87552930211065054

    This function assign strings where the authors assign numerical codes for category.

    0: interface
    1: slab
    2: crustal
    4: outer rise
    -999: undetermined
    -888: interface uncertain
    -777: slab uncertain
    -666: crustal uncertain
    -444: outer rise uncertain

    Args:
        eqinfo (list): [latitude, longitude, depth]
        input_strec_info (pandas Series): Pandas Series with results from
                                          getSubductionType().
    Returns:
        Input Series with added fields NGACategory and NGAHorizontalType.
    """
    strec_info = input_strec_info.copy()
    category_distance = 1e10
    if strec_info["TectonicRegion"] != SUBDUCTION_REGION:
        strec_info["NGACategory"] = "undetermined"
        return strec_info
    if np.isnan(strec_info["SlabModelDepth"]):
        strec_info["NGACategory"] = "undetermined"
        return strec_info
    _, _, depth = eqinfo
    horizontal_type = Zone.A
    if strec_info["SlabModelDepth"] > MIN_SLAB_DEPTH:
        horizontal_type = Zone.B
    if strec_info["SlabModelDepth"] > strec_info["SlabModelMaximumDepth"]:
        horizontal_type = Zone.C

    shallowest_interface = (
        strec_info["SlabModelDepth"] - strec_info["SlabModelDepthUncertainty"]
    )
    category = None
    if horizontal_type == Zone.A:
        category_distance = min(category_distance, abs(depth - MAX_INTERFACE_DEPTH))
        if depth > MAX_INTERFACE_DEPTH:
            category = Category.SLAB
        else:
            category = Category.OUTER_RISE
    elif horizontal_type == Zone.B:
        category_distance = min(category_distance, abs(depth - MAX_INTERFACE_DEPTH))
        category_distance = min(category_distance, abs(depth - shallowest_interface))
        if depth > MAX_INTERFACE_DEPTH:
            category = Category.SLAB
        elif depth < shallowest_interface:
            category = Category.CRUSTAL
        else:
            category = Category.INTERFACE
    else:  # zone C
        category_distance = min(category_distance, abs(depth - MAX_CRUSTAL_DEPTH))
        category_distance = min(category_distance, abs(depth - shallowest_interface))
        if depth < MAX_CRUSTAL_DEPTH:
            category = Category.CRUSTAL
        elif depth < shallowest_interface:
            category = Category.UNDETERMINED  # -999
        else:
            category = Category.SLAB

    delta_depth = abs(depth - strec_info["SlabModelDepth"])
    delta_max = depth - strec_info["SlabModelMaximumDepth"]
    if (
        category == Category.INTERFACE
        and strec_info["FocalMechanism"] != Focal.RS.value
        and delta_depth < DIST_THRESHOLD
    ):
        category_distance = min(category_distance, abs(delta_depth - DIST_THRESHOLD))
        category = Category.CRUSTAL

    # we are applying this to all horizontal categories, however it is not clear from
    # paper if this is intended.
    slab_or_rise = (
        category == Category.SLAB
        or category == Category.OUTER_RISE
        or category == Category.SLAB_UNCERTAIN
        or category == Category.OUTER_RISE_UNCERTAIN
    )
    if (
        slab_or_rise
        and strec_info["FocalMechanism"] == Focal.RS.value
        and delta_max < DIST_THRESHOLD
    ):
        category_distance = min(category_distance, abs(delta_max - DIST_THRESHOLD))
        category = Category.INTERFACE

    # this criteria is somewhat unclear from paper
    boundary_uncertain = category_distance < BOUNDARY_DELTA
    if category == Category.OUTER_RISE and (
        strec_info["FocalMechanism"] != Focal.NM.value or boundary_uncertain
    ):
        category = Category.OUTER_RISE_UNCERTAIN

    if category == Category.INTERFACE and (
        strec_info["FocalMechanism"] != Focal.RS.value or boundary_uncertain
    ):
        category = Category.INTERFACE_UNCERTAIN

    if category == Category.SLAB and (
        strec_info["FocalMechanism"] != Focal.NM.value or boundary_uncertain
    ):
        category = Category.SLAB_UNCERTAIN

    if category == Category.CRUSTAL and boundary_uncertain:
        category = Category.CRUSTAL_UNCERTAIN

    strec_info["NGACategory"] = category.value

    return strec_info
