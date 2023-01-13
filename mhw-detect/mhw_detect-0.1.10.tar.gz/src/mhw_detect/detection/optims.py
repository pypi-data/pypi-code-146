import numpy as np
import numba as nb
from numba import njit


@njit(
    nb.types.Tuple((nb.float64[:], nb.float64[:]))(
        nb.int64,
        nb.int64,
        nb.int64,
        nb.float64[:],
        nb.float64[:],
        nb.int64,
        nb.float32[:],
        nb.float64[:],
        nb.int64,
        nb.int64,
        nb.int64,
    ),
    cache=True,
)
def threshAndClim(
    lenClimYear,
    feb29,
    pctile,
    thresh_climYear,
    seas_climYear,
    TClim,
    tempClim,
    doyClim,
    clim_start,
    clim_end,
    windowHalfWidth,
):
    """

    Compute climatology mean and threshold.

    Written by Eric Oliver, Institue for Marine and Antarctic Studies, University of Tasmania, Feb-Mar 2015
    Optimised by Jonathan Brouillet, Mercator Ocean International, Toulouse, France, 2021

    """

    for d in range(1, lenClimYear + 1):
        # Special case for Feb 29
        if d != feb29:
            # find all indices for each day of the year +/- windowHalfWidth and from them calculate the threshold
            tt0 = np.where(doyClim[clim_start : clim_end + 1] == d)[0]
            # If this doy value does not exist (i.e. in 360-day calendars) then skip it
            if len(tt0) != 0:
                tt = np.empty(0)
                for w in range(-windowHalfWidth, windowHalfWidth + 1):
                    tt = np.append(tt, clim_start + tt0 + w)

                tt = tt[tt >= 0]  # Reject indices "before" the first element
                tt = tt[tt < TClim]  # Reject indices "after" the last element
                thresh_climYear[d - 1] = np.nanpercentile(
                    tempClim[tt.astype(np.int64)], pctile
                )
                seas_climYear[d - 1] = np.nanmean(tempClim[tt.astype(np.int64)])

    return thresh_climYear, seas_climYear


@njit(cache=True)
def mhwproperties(t, temp, clim, n, mhw, categs):
    """

    Add mhw characteristics in Numba dictionnary.

    Written by Eric Oliver, Institue for Marine and Antarctic Studies, University of Tasmania, Feb-Mar 2015
    Optimised by Jonathan Brouillet, Mercator Ocean International, Toulouse, France, 2021

    """

    T = len(t)
    categories = np.arange(1, 5, dtype=np.float64)
    for ev in range(n):
        tt_start = np.where(t == mhw["time_start"][ev])[0][0]
        tt_end = np.where(t == mhw["time_end"][ev])[0][0]
        appendjit(mhw, "index_start", tt_start)
        appendjit(mhw, "index_end", tt_start)
        temp_mhw = temp[tt_start : tt_end + 1]
        thresh_mhw = clim["thresh"][tt_start : tt_end + 1]
        seas_mhw = clim["seas"][tt_start : tt_end + 1]
        mhw_relSeas = temp_mhw - seas_mhw
        mhw_relThresh = temp_mhw - thresh_mhw
        mhw_relThreshNorm = (temp_mhw - thresh_mhw) / (thresh_mhw - seas_mhw)
        mhw_abs = temp_mhw
        # Find peak
        tt_peak = np.argmax(mhw_relSeas)
        appendjit(mhw, "time_peak", mhw["time_start"][ev] + tt_peak)
        appendjit(mhw, "index_peak", tt_start + tt_peak)
        # MHW Duration
        appendjit(mhw, "duration", len(mhw_relSeas))
        # MHW Intensity metrics
        appendjit(mhw, "intensity_max", mhw_relSeas[tt_peak])
        appendjit(mhw, "intensity_mean", mhw_relSeas.mean())
        appendjit(mhw, "intensity_var", np.sqrt(mhw_relSeas.var()))
        appendjit(mhw, "intensity_cumulative", mhw_relSeas.sum())
        appendjit(mhw, "intensity_max_relThresh", mhw_relThresh[tt_peak])
        appendjit(mhw, "intensity_mean_relThresh", mhw_relThresh.mean())
        appendjit(mhw, "intensity_var_relThresh", np.sqrt(mhw_relThresh.var()))
        appendjit(mhw, "intensity_cumulative_relThresh", mhw_relThresh.sum())
        appendjit(mhw, "intensity_max_abs", mhw_abs[tt_peak])
        appendjit(mhw, "intensity_mean_abs", mhw_abs.mean())
        appendjit(mhw, "intensity_var_abs", np.sqrt(mhw_abs.var()))
        appendjit(mhw, "intensity_cumulative_abs", mhw_abs.sum())
        # Fix categories
        tt_peakCat = np.argmax(mhw_relThreshNorm)
        cats = np.floor(1.0 + mhw_relThreshNorm)
        categs[str(ev)] = cats
        appendjit(
            mhw,
            "category",
            categories[np.int64(np.min(np.array([cats[tt_peakCat], 4]))) - 1],
        )
        appendjit(mhw, "duration_moderate", np.sum(cats == 1.0))
        appendjit(mhw, "duration_strong", np.sum(cats == 2.0))
        appendjit(mhw, "duration_severe", np.sum(cats == 3.0))
        appendjit(mhw, "duration_extreme", np.sum(cats >= 4.0))

        # Rates of onset and decline
        # Requires getting MHW strength at "start" and "end" of event (continuous: assume start/end half-day before/after first/last point)
        try:
            if tt_start > 0:
                mhw_relSeas_start = 0.5 * (
                    mhw_relSeas[0] + temp[tt_start - 1] - clim["seas"][tt_start - 1]
                )
                appendjit(
                    mhw,
                    "rate_onset",
                    (mhw_relSeas[tt_peak] - mhw_relSeas_start)
                    / np.float64(tt_peak + 0.5),
                )
            else:  # MHW starts at beginning of time series
                if (
                    tt_peak == 0
                ):  # Peak is also at begining of time series, assume onset time = 1 day
                    appendjit(
                        mhw, "rate_onset", (mhw_relSeas[tt_peak] - mhw_relSeas[0]) / 1.0
                    )
                else:
                    appendjit(
                        mhw,
                        "rate_onset",
                        (mhw_relSeas[tt_peak] - mhw_relSeas[0]) / tt_peak,
                    )
        except:
            appendjit(mhw, "rate_onset", np.nan)

        try:
            if tt_end < T - 1:
                mhw_relSeas_end = 0.5 * (
                    mhw_relSeas[-1] + temp[tt_end + 1] - clim["seas"][tt_end + 1]
                )
                appendjit(
                    mhw,
                    "rate_decline",
                    (mhw_relSeas[tt_peak] - mhw_relSeas_end)
                    / np.float64(tt_end - tt_start - tt_peak + 0.5),
                )
            else:  # MHW finishes at end of time series
                if (
                    tt_peak == T - 1
                ):  # Peak is also at end of time series, assume decline time = 1 day
                    appendjit(
                        mhw,
                        "rate_decline",
                        (mhw_relSeas[tt_peak] - mhw_relSeas[-1]) / 1.0,
                    )
                else:
                    appendjit(
                        mhw,
                        "rate_decline",
                        (mhw_relSeas[tt_peak] - mhw_relSeas[-1])
                        / np.float64(tt_end - tt_start - tt_peak),
                    )
        except:
            appendjit(mhw, "rate_decline", np.nan)

    return tt_peak


@njit(cache=True)
def appendjit(mhw, key, val):
    """

    Numba-friendly append function.

    Written by Jonathan Brouillet, Mercator Ocean International, Toulouse, France, 2021

    """
    mhw[key] = np.append(mhw[key], np.float32(val))
