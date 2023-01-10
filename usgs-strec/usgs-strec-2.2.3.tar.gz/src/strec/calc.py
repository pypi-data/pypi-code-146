# stdlib imports
import logging

# third party imports
import numpy as np
import pandas as pd
from esi_utils_rupture.tensor import (
    fill_tensor_from_angles,
    fill_tensor_from_components,
)

# local imports
from strec.subtype import SubductionSelector, get_event_details
from strec.utils import read_input_file

LOGGER = "subselect"


def get_input_dataframe(input_file, eqinfo, event_id, hypo_columns, id_column):
    """Create a dataframe of events (possibly only one).

    Args:
        input_file (str or None):  Name of input CSV/Excel file or None.
        eqinfo (tuple or None): Tuple of (lat, lon, depth) or None.
        event_id (str or None): ComCat Event ID or None.
        hypo_columns (tuple or None): Tuple of hypocenter column names in input_file or
                                      None.
        id_column (str or None): Name of column in input_file containing ComCat Event
                                 ID or None.

    Returns:
        tuple of:
            - pandas DataFrame containing at least lat/lon/depth columns
            - Name of ComCat event ID column or None
            - Name of latitude column
            - Name of longitude column
            - Name of depth column
    """
    latcol = "lat"
    loncol = "lon"
    depcol = "depth"
    idcol = None
    if input_file is not None:
        df, idcol, latcol, loncol, depcol = read_input_file(
            input_file, hypo_columns, id_column
        )
    elif eqinfo is not None:
        lat, lon, depth = eqinfo
        d = {"lat": [lat], "lon": [lon], "depth": [depth]}
        df = pd.DataFrame(d)
    if event_id is not None:
        detail = get_event_details(event_id)
        idcol = "ComCatID"
        lat, lon, depth = detail["latitude"], detail["longitude"], detail["depth"]
        d = {"ComCatID": event_id, "lat": [lat], "lon": [lon], "depth": [depth]}
        df = pd.DataFrame(d)
    return (df, idcol, latcol, loncol, depcol)


def get_moment_columns(row):
    """Return focal mechanism/moment tensor parameters from MT components or focal angles.

    Args:
        row (pandas Series): Contains moment tensor components (mtt, mpp, etc) OR
                             focal angles (strike, dip, rake)

    Returns:
        dict: Fully descriptive moment tensor dictionary, including fields:
            - mrr,mtt,mpp,mrt,mrp,mtp Moment tensor components.
            - T T-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - N N-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - P P-axis values:
              - azimuth (degrees)
              - plunge (degrees)
            - NP1 First nodal plane values:
              - strike (degrees)
              - dip (degrees)
              - rake (degrees)
            - NP2 Second nodal plane values:
              - strike (degrees)
              - dip (degrees)
              - rake (degrees)
    """
    # row is a pandas series object
    isreal = row.notnull()

    has_mtt = row.index.str.contains("mtt", case=False)
    has_mpp = row.index.str.contains("mpp", case=False)
    has_mrr = row.index.str.contains("mrr", case=False)
    has_mrt = row.index.str.contains("mrt", case=False)
    has_mrp = row.index.str.contains("mrp", case=False)
    has_mtp = row.index.str.contains("mtp", case=False)

    mtts = row[isreal & has_mtt]
    mpps = row[isreal & has_mpp]
    mrrs = row[isreal & has_mrr]
    mrts = row[isreal & has_mrt]
    mrps = row[isreal & has_mrp]
    mtps = row[isreal & has_mtp]

    mtt = mpp = mrr = mrt = mrp = mtp = np.nan
    if len(mtts):
        mtt = float(mtts[0])
    if len(mpps):
        mpp = float(mpps[0])
    if len(mrrs):
        mrr = float(mrrs[0])
    if len(mrts):
        mrt = float(mrts[0])
    if len(mrps):
        mrp = float(mrps[0])
    if len(mtps):
        mtp = float(mtps[0])

    if not np.isnan(np.sum([mtt, mpp, mrr, mrt, mrp, mtp])):
        tensor_params = fill_tensor_from_components(mrr, mtt, mpp, mrt, mrp, mtp)
        return tensor_params

    has_strike = row.index.str.contains("strike", case=False)
    has_dip = row.index.str.contains("dip", case=False)
    has_rake = row.index.str.contains("rake", case=False)
    strikes = row[isreal & has_strike]
    dips = row[isreal & has_dip]
    rakes = row[isreal & has_rake]

    strike = dip = rake = np.nan
    if len(strikes):
        strike = strikes[0]
    if len(dips):
        dip = dips[0]
    if len(rakes):
        rake = rakes[0]

    if not np.isnan(strike):
        tensor_params = fill_tensor_from_angles(strike, dip, rake)
        return tensor_params

    return None


def check_moment_row(row):
    """Check row of dataframe for presence of moment tensor information.

    Args:
        row (pandas Series): Series possibly containing moment tensor data
    Returns:
        bool: True if input contains moment tensor or focal mechanism data.
    """
    # row is a pandas series object
    hasAngles = True
    hasComponents = True

    keys = set([key.lower() for key in (row.keys()).values.tolist()])
    cmp_components = set(["mrr", "mpp", "mtt", "mrt", "mrp", "mtp"])
    if not cmp_components.issubset(keys):
        hasComponents = False

    cmp_angles = set(["strike", "dip", "rake"])
    if not cmp_angles.issubset(keys):
        hasAngles = False

    return hasAngles or hasComponents


def select_regions(
    input_file,
    eqinfo,
    moment_info,
    event_id,
    hypo_columns,
    id_column,
    verbose,
):
    """Output full range of seismotectonic information.

    Args:
        input_file (str or None):  Name of input CSV/Excel file or None.
        eqinfo (tuple or None): Tuple of (lat, lon, depth) or None.
        moment_info (tuple or None): Tuple of (strike, dip, rake, magnitude) or None.
        event_id (str or None): ComCat Event ID or None.
        hypo_columns (tuple or None): Tuple of hypocenter column names in input_file
                                      or None.
        id_column (str or None): Name of column in input_file containing ComCat
                                 Event ID or None.
        verbose (bool): Turn verbose debugging on/off.
    Returns:
        Pandas Series object with indices:
            - TectonicRegion : (Subduction,Active,Stable,HotSpot)
            - FocalMechanism : (RS [Reverse],SS [Strike-Slip], NM [Normal], ALL
            [Unknown])
            - TensorType : (actual, composite)
            - TensorSource : String indicating the source of the moment tensor
            information.
            - KaganAngle : Angle between moment tensor and slab interface.
            - CompositeVariability : A measure of the uncertainty in the composite
            moment tensor.
            - NComposite : Number of events used to create composite moment tensor.
            - DistanceToStable : Distance in km from the nearest stable polygon.
            - DistanceToActive : Distance in km from the nearest active polygon.
            - DistanceToSubduction : Distance in km from the nearest subduction
            polygon.
            - DistanceToHotSpot : Distance in km from the nearest hotspot polygon.
            - Oceanic : Boolean indicating whether we are in an oceanic region.
            - DistanceToOceanic : Distance in km to nearest oceanic polygon.
            - DistanceToContinental : Distance in km to nearest continental polygon.
            - SlabModelRegion : Subduction region.
            - SlabModelType : (grid,trench)
            - SlabModelDepth : Depth to slab interface at epicenter.
            - SlabModelDepthUncertainty : Uncertainty of depth to slab interface.
            - SlabModelDip : Dip of slab at epicenter.
            - SlabModelStrike : Strike of slab at epicenter.
    """
    selector = SubductionSelector(verbose=verbose, prefix=LOGGER)
    dataframe, idcol, latcol, loncol, depcol = get_input_dataframe(
        input_file, eqinfo, event_id, hypo_columns, id_column
    )
    tensor_params = None
    if moment_info[0] is not None:
        strike, dip, rake, mag = moment_info
        tensor_params = fill_tensor_from_angles(strike, dip, rake, mag)
    has_tensor = check_moment_row(dataframe.iloc[0]) or tensor_params is not None
    rows = []
    ic = 0
    inc = min(100, np.power(10, np.floor(np.log10(len(dataframe))) - 1))
    for _, row in dataframe.iterrows():
        if ic % inc == 0 and verbose:
            msg = "Getting detailed information for %i of %i events.\n"
            logging.info(msg % (ic, len(dataframe)))
        if idcol is not None:
            event_id = row[idcol]
        if not tensor_params and has_tensor:
            tensor_params = get_moment_columns(row)

        lat = row[latcol]
        lon = row[loncol]
        # for the cases where lon goes from 0-360
        if lon > 180:
            lon -= 360
        depth = row[depcol]

        result = selector.getSubductionType(
            lat,
            lon,
            depth,
            eventid=event_id,
            tensor_params=tensor_params,
        )

        tensor_params = None
        row = pd.concat([row, result])
        rows.append(row)
    output_dataframe = pd.DataFrame(rows)
    return output_dataframe
