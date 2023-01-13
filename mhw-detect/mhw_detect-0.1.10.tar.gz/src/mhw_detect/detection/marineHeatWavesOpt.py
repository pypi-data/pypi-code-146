"""
    https://github.com/ecjoliver/marineHeatWaves/blob/master/marineHeatWaves.py
    A set of functions which implement the Marine Heat Wave (MHW)
    definition of Hobday et al. (2016)

"""

import numpy as np
import scipy.ndimage as ndimage
from datetime import date
from numba.core import types
from numba.typed import Dict
from src.mhw_detect.detection.optims import threshAndClim, mhwproperties, appendjit


def detect(
    t,
    temp,
    seas_climYear=None,
    thresh_climYear=None,
    climatologyPeriod=[None, None],
    pctile=90,
    windowHalfWidth=5,
    smoothPercentile=True,
    smoothPercentileWidth=31,
    minDuration=5,
    joinAcrossGaps=True,
    maxGap=2,
    maxPadLength=False,
    coldSpells=False,
    alternateClimatology=False,
    Ly=False,
):
    """
    Applies the Hobday et al. (2016) marine heat wave definition to an input time
    series of temp ('temp') along with a time vector ('t'). Outputs properties of
    all detected marine heat waves.
    Inputs:
      t       Time vector, in datetime format (e.g., date(1982,1,1).toordinal())
              [1D numpy array of length T]
      temp    Temperature vector [1D numpy array of length T]
    Outputs:
      mhw     Detected marine heat waves (MHWs). Each key (following list) is a
              list of length N where N is the number of detected MHWs:

        'time_start'           Start time of MHW [datetime format]
        'time_end'             End time of MHW [datetime format]
        'time_peak'            Time of MHW peak [datetime format]
        'date_start'           Start date of MHW [datetime format]
        'date_end'             End date of MHW [datetime format]
        'date_peak'            Date of MHW peak [datetime format]
        'index_start'          Start index of MHW
        'index_end'            End index of MHW
        'index_peak'           Index of MHW peak
        'duration'             Duration of MHW [days]
        'intensity_max'        Maximum (peak) intensity [deg. C]
        'intensity_mean'       Mean intensity [deg. C]
        'intensity_var'        Intensity variability [deg. C]
        'intensity_cumulative' Cumulative intensity [deg. C x days]
        'rate_onset'           Onset rate of MHW [deg. C / days]
        'rate_decline'         Decline rate of MHW [deg. C / days]
        'intensity_max_relThresh', 'intensity_mean_relThresh', 'intensity_var_relThresh',
        and 'intensity_cumulative_relThresh' are as above except relative to the
        threshold (e.g., 90th percentile) rather than the seasonal climatology
        'intensity_max_abs', 'intensity_mean_abs', 'intensity_var_abs', and
        'intensity_cumulative_abs' are as above except as absolute magnitudes
        rather than relative to the seasonal climatology or threshold
        'category' is an integer category system (1, 2, 3, 4) based on the maximum intensity
        in multiples of threshold exceedances, i.e., a value of 1 indicates the MHW
        intensity (relative to the climatology) was >=1 times the value of the threshold (but
        less than 2 times; relative to climatology, i.e., threshold - climatology).
        Category types are defined as 1=strong, 2=moderate, 3=severe, 4=extreme. More details in
        Hobday et al. (in prep., Oceanography). Also supplied are the duration of each of these
        categories for each event.
        'n_events'             A scalar integer (not a list) indicating the total
                               number of detected MHW events
      clim    Climatology of SST. Each key (following list) is a seasonally-varying
              time series [1D numpy array of length T] of a particular measure:
        'thresh'               Seasonally varying threshold (e.g., 90th percentile)
        'seas'                 Climatological seasonal cycle
        'missing'              A vector of TRUE/FALSE indicating which elements in
                               temp were missing values for the MHWs detection
    Options:
      seas_climYear          Climatology mean vector
      thresh_climYear        Threshold vector
      climatologyPeriod      Period over which climatology is calculated, specified
                             as list of start and end years. Default is to calculate
                             over the full range of years in the supplied time series.
                             Alternate periods suppled as a list e.g. [1983,2012].
                             Unused if seas_climYear and thresh_climYear are set.
      pctile                 Threshold percentile (%) for detection of extreme values
                             (DEFAULT = 90)
                             Unused if seas_climYear and thresh_climYear are set.
      windowHalfWidth        Width of window (one sided) about day-of-year used for
                             the pooling of values and calculation of threshold percentile
                             (DEFAULT = 5 [days])
      smoothPercentile       Boolean switch indicating whether to smooth the threshold
                             percentile timeseries with a moving average (DEFAULT = True)
      smoothPercentileWidth  Width of moving average window for smoothing threshold
                             (DEFAULT = 31 [days])
      minDuration            Minimum duration for acceptance detected MHWs
                             (DEFAULT = 5 [days])
      joinAcrossGaps         Boolean switch indicating whether to join MHWs
                             which occur before/after a short gap (DEFAULT = True)
      maxGap                 Maximum length of gap allowed for the joining of MHWs
                             (DEFAULT = 2 [days])
      maxPadLength           Specifies the maximum length [days] over which to interpolate
                             (pad) missing data (specified as nans) in input temp time series.
                             i.e., any consecutive blocks of NaNs with length greater
                             than maxPadLength will be left as NaN. Set as an integer.
                             (DEFAULT = False, interpolates over all missing values).
      coldSpells             Specifies if the code should detect cold events instead of
                             heat events. (DEFAULT = False)
      alternateClimatology   Specifies an alternate temperature time series to use for the
                             calculation of the climatology. Format is as a list of numpy
                             arrays: (1) the first element of the list is a time vector,
                             in datetime format (e.g., date(1982,1,1).toordinal())
                             [1D numpy array of length TClim] and (2) the second element of
                             the list is a temperature vector [1D numpy array of length TClim].
                             (DEFAULT = False)
      Ly                     Specifies if the length of the year is < 365/366 days (e.g. a
                             360 day year from a climate model). This affects the calculation
                             of the climatology. (DEFAULT = False)
    Notes:
      1. This function assumes that the input time series consist of continuous daily values
         with few missing values. Time ranges which start and end part-way through the calendar
         year are supported.
      2. This function supports leap years. This is done by ignoring Feb 29s for the initial
         calculation of the climatology and threshold. The value of these for Feb 29 is then
         linearly interpolated from the values for Feb 28 and Mar 1.
      3. The calculation of onset and decline rates assumes that the heat wave started a half-day
         before the start day and ended a half-day after the end-day. (This is consistent with the
         duration definition as implemented, which assumes duration = end day - start day + 1.)
      4. For the purposes of MHW detection, any missing temp values not interpolated over (through
         optional maxPadLLength) will be set equal to the seasonal climatology. This means they will
         trigger the end/start of any adjacent temp values which satisfy the MHW criteria.
      5. If the code is used to detect cold events (coldSpells = True), then it works just as for heat
         waves except that events are detected as deviations below the (100 - pctile)th percentile
         (e.g., the 10th instead of 90th) for at least 5 days. Intensities are reported as negative
         values and represent the temperature anomaly below climatology.
    Written by Eric Oliver, Institue for Marine and Antarctic Studies, University of Tasmania, Feb 2015

    Optimised by Jonathan Brouillet, Mercator Ocean International, Toulouse, France, 2021

    """

    #
    # Initialize MHW output variable
    #

    mhw = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.float64[:],
    )

    categs = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.float64[:],
    )

    mhw["time_start"] = np.asarray([], dtype=np.dtype(np.float64))  # datetime format
    mhw["time_end"] = np.array([], dtype=np.dtype(np.float64))  # datetime format
    mhw["time_peak"] = np.array([], dtype=np.dtype(np.float64))  # datetime format
    mhw["date_start"] = np.array([], dtype=np.dtype(np.float64))  # datetime format
    mhw["date_end"] = np.array([], dtype=np.dtype(np.float64))  # datetime format
    mhw["date_peak"] = np.array([], dtype=np.dtype(np.float64))  # datetime format
    mhw["index_start"] = np.array([], dtype=np.dtype(np.float64))
    mhw["index_end"] = np.array([], dtype=np.dtype(np.float64))
    mhw["index_peak"] = np.array([], dtype=np.dtype(np.float64))
    mhw["duration"] = np.array([], dtype=np.dtype(np.float64))  # [days]
    mhw["duration_moderate"] = np.array([], dtype=np.dtype(np.float64))  # [days]
    mhw["duration_strong"] = np.array([], dtype=np.dtype(np.float64))  # [days]
    mhw["duration_severe"] = np.array([], dtype=np.dtype(np.float64))  # [days]
    mhw["duration_extreme"] = np.array([], dtype=np.dtype(np.float64))  # [days]
    mhw["intensity_max"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_mean"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_var"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_cumulative"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_max_relThresh"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_mean_relThresh"] = np.array(
        [], dtype=np.dtype(np.float64)
    )  # [deg C]
    mhw["intensity_var_relThresh"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_cumulative_relThresh"] = np.array(
        [], dtype=np.dtype(np.float64)
    )  # [deg C]
    mhw["intensity_max_abs"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_mean_abs"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_var_abs"] = np.array([], dtype=np.dtype(np.float64))  # [deg C]
    mhw["intensity_cumulative_abs"] = np.array(
        [], dtype=np.dtype(np.float64)
    )  # [deg C]
    mhw["category"] = np.array([], dtype=np.dtype(np.float64))
    mhw["rate_onset"] = np.array([], dtype=np.dtype(np.float64))  # [deg C / day]
    mhw["rate_decline"] = np.array([], dtype=np.dtype(np.float64))  # [deg C / day]

    mhw_date = {}
    mhw_date["date_start"] = []
    mhw_date["date_end"] = []
    mhw_date["date_peak"] = []

    #
    # Time and dates vectors
    #

    # Generate vectors for year, month, day-of-month, and day-of-year
    T = len(t)
    year = np.zeros((T))
    month = np.zeros((T))
    day = np.zeros((T))
    doy = np.zeros((T))
    for i in range(T):
        year[i] = date.fromordinal(t[i]).year
        month[i] = date.fromordinal(t[i]).month
        day[i] = date.fromordinal(t[i]).day
    # Leap-year baseline for defining day-of-year values
    year_leapYear = (
        2012  # This year was a leap-year and therefore doy in range of 1 to 366
    )
    t_leapYear = np.arange(
        date(year_leapYear, 1, 1).toordinal(),
        date(year_leapYear, 12, 31).toordinal() + 1,
    )
    month_leapYear = np.zeros((len(t_leapYear)))
    day_leapYear = np.zeros((len(t_leapYear)))
    doy_leapYear = np.zeros((len(t_leapYear)))
    for tt in range(len(t_leapYear)):
        month_leapYear[tt] = date.fromordinal(t_leapYear[tt]).month
        day_leapYear[tt] = date.fromordinal(t_leapYear[tt]).day
        doy_leapYear[tt] = (
            t_leapYear[tt]
            - date(date.fromordinal(t_leapYear[tt]).year, 1, 1).toordinal()
            + 1
        )
    # Calculate day-of-year values
    for tt in range(T):
        doy[tt] = doy_leapYear[
            (month_leapYear == month[tt]) * (day_leapYear == day[tt])
        ]

    # Constants (doy values for Feb-28 and Feb-29) for handling leap-years
    feb29 = 60

    # Set climatology period, if unset use full range of available data
    if (climatologyPeriod[0] is None) or (climatologyPeriod[1] is None):
        climatologyPeriod[0] = year[0]
        climatologyPeriod[1] = year[-1]

    #
    # Calculate threshold and seasonal climatology (varying with day-of-year)
    #

    # if alternate temperature time series is supplied for the calculation of the climatology
    if alternateClimatology:

        tClim = alternateClimatology[0]
        tempClim = alternateClimatology[1]
        TClim = len(tClim)
        yearClim = np.zeros((TClim))
        monthClim = np.zeros((TClim))
        dayClim = np.zeros((TClim))
        doyClim = np.zeros((TClim))
        for i in range(TClim):
            yearClim[i] = date.fromordinal(tClim[i]).year
            monthClim[i] = date.fromordinal(tClim[i]).month
            dayClim[i] = date.fromordinal(tClim[i]).day
            doyClim[i] = doy_leapYear[
                (month_leapYear == monthClim[i]) * (day_leapYear == dayClim[i])
            ]
    else:
        tempClim = temp.copy()
        TClim = np.array([T]).copy()[0]
        yearClim = year.copy()
        monthClim = month.copy()
        dayClim = day.copy()
        doyClim = doy.copy()

    # Flip temp time series if detecting cold spells
    if coldSpells:
        temp = -1.0 * temp
        tempClim = -1.0 * tempClim

    # Pad missing values for all consecutive missing blocks of length <= maxPadLength
    if maxPadLength:
        temp = pad(temp, maxPadLength=maxPadLength)
        tempClim = pad(tempClim, maxPadLength=maxPadLength)

    # Length of climatological year
    lenClimYear = 366

    clim = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.float64[:],
    )
    clim["thresh"] = np.NaN * np.zeros(TClim)
    clim["seas"] = np.NaN * np.zeros(TClim)
    # Loop over all day-of-year values, and calculate threshold and seasonal climatology across years
    if (thresh_climYear is None) or (seas_climYear is None):
        # Start and end indices
        # Inialize arrays
        thresh_climYear = np.NaN * np.zeros(lenClimYear)
        seas_climYear = np.NaN * np.zeros(lenClimYear)

        clim_start = np.where(yearClim == climatologyPeriod[0])[0][0]
        clim_end = np.where(yearClim == climatologyPeriod[1])[0][-1]

        thresh_climYear, seas_climYear = threshAndClim(
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
        )

    # Special case for Feb 29
    thresh_climYear[feb29 - 1] = (
        0.5 * thresh_climYear[feb29 - 2] + 0.5 * thresh_climYear[feb29]
    )
    seas_climYear[feb29 - 1] = (
        0.5 * seas_climYear[feb29 - 2] + 0.5 * seas_climYear[feb29]
    )

    # Smooth if desired
    if smoothPercentile:
        # If the length of year is < 365/366 (e.g. a 360 day year from a Climate Model)
        if Ly:
            valid = ~np.isnan(thresh_climYear)
            thresh_climYear[valid] = runavg(
                thresh_climYear[valid], smoothPercentileWidth
            )
            valid = ~np.isnan(seas_climYear)
            seas_climYear[valid] = runavg(seas_climYear[valid], smoothPercentileWidth)
        # >= 365-day year
        else:
            thresh_climYear = runavg(thresh_climYear, smoothPercentileWidth)
            seas_climYear = runavg(seas_climYear, smoothPercentileWidth)

    # Generate threshold for full time series
    clim["thresh"] = thresh_climYear[doy.astype(int) - 1]
    clim["seas"] = seas_climYear[doy.astype(int) - 1]
    # Save vector indicating which points in temp are missing values
    # clim['missing'] = np.isnan(temp)
    # Set all remaining missing temp values equal to the climatology
    temp[np.isnan(temp)] = clim["seas"][np.isnan(temp)]

    #
    # Find MHWs as exceedances above the threshold
    #

    # Time series of "True" when threshold is exceeded, "False" otherwise
    exceed_bool = temp - clim["thresh"]
    exceed_bool[exceed_bool <= 0] = False
    exceed_bool[exceed_bool > 0] = True
    # Fix issue where missing temp vaues (nan) are counted as True
    exceed_bool[np.isnan(exceed_bool)] = False
    # Find contiguous regions of exceed_bool = True
    events, n_events = ndimage.label(exceed_bool)

    # Find all MHW events of duration >= minDuration
    for ev in range(1, n_events + 1):
        event_duration = (events == ev).sum()
        if event_duration < minDuration:
            continue
        # np.append(mhw['time_start'], np.float32(t[np.where(events == ev)[0][0]]))
        appendjit(mhw, "time_start", t[np.where(events == ev)[0][0]])
        appendjit(mhw, "time_end", t[np.where(events == ev)[0][-1]])

    # Link heat waves that occur before and after a short gap (gap must be no longer than maxGap)
    if joinAcrossGaps:
        # Calculate gap length for each consecutive pair of events
        gaps = np.array(mhw["time_start"][1:]) - np.array(mhw["time_end"][0:-1]) - 1
        if len(gaps) > 0:
            while gaps.min() <= maxGap:
                # Find first short gap
                ev = np.where(gaps <= maxGap)[0][0]
                # Extend first MHW to encompass second MHW (including gap)
                mhw["time_end"][ev] = mhw["time_end"][ev + 1]
                # Remove second event from record
                mhw["time_start"] = np.delete(mhw["time_start"], ev + 1)
                mhw["time_end"] = np.delete(mhw["time_end"], ev + 1)
                # Calculate gap length for each consecutive pair of events
                gaps = (
                    np.array(mhw["time_start"][1:])
                    - np.array(mhw["time_end"][0:-1])
                    - 1
                )
                if len(gaps) == 0:
                    break

    # Calculate marine heat wave properties
    tt_peak = mhwproperties(t, temp, clim, len(mhw["time_start"]), mhw, categs)
    for ev in range(len(mhw["time_start"])):
        mhw_date["date_start"].append(date.fromordinal(int(mhw["time_start"][ev])))
        mhw_date["date_end"].append(date.fromordinal(int(mhw["time_end"][ev])))
        mhw_date["date_peak"].append(
            date.fromordinal(int(mhw["time_start"][ev] + tt_peak))
        )

    # Flip climatology and intensties in case of cold spell detection
    if coldSpells:
        clim["seas"] = -1.0 * clim["seas"]
        clim["thresh"] = -1.0 * clim["thresh"]
        for ev in range(len(mhw["intensity_max"])):
            mhw["intensity_max"][ev] = -1.0 * mhw["intensity_max"][ev]
            mhw["intensity_mean"][ev] = -1.0 * mhw["intensity_mean"][ev]
            mhw["intensity_cumulative"][ev] = -1.0 * mhw["intensity_cumulative"][ev]
            mhw["intensity_max_relThresh"][ev] = (
                -1.0 * mhw["intensity_max_relThresh"][ev]
            )
            mhw["intensity_mean_relThresh"][ev] = (
                -1.0 * mhw["intensity_mean_relThresh"][ev]
            )
            mhw["intensity_cumulative_relThresh"][ev] = (
                -1.0 * mhw["intensity_cumulative_relThresh"][ev]
            )
            mhw["intensity_max_abs"][ev] = -1.0 * mhw["intensity_max_abs"][ev]
            mhw["intensity_mean_abs"][ev] = -1.0 * mhw["intensity_mean_abs"][ev]
            mhw["intensity_cumulative_abs"][ev] = (
                -1.0 * mhw["intensity_cumulative_abs"][ev]
            )

    return mhw, mhw_date, categs


def runavg(ts, w):
    """

    Performs a running average of an input time series using uniform window
    of width w. This function assumes that the input time series is periodic.

    Inputs:

      ts            Time series [1D numpy array]
      w             Integer length (must be odd) of running average window

    Outputs:

      ts_smooth     Smoothed time series

    Written by Eric Oliver, Institue for Marine and Antarctic Studies, University of Tasmania, Feb-Mar 2015

    """
    # Original length of ts
    N = len(ts)
    # make ts three-fold periodic
    ts = np.append(ts, np.append(ts, ts))
    # smooth by convolution with a window of equal weights
    ts_smooth = np.convolve(ts, np.ones(w) / w, mode="same")
    # Only output central section, of length equal to the original length of ts
    ts = ts_smooth[N : 2 * N]

    return ts


def pad(data, maxPadLength=False):
    """

    Linearly interpolate over missing data (NaNs) in a time series.

    Inputs:

      data	     Time series [1D numpy array]
      maxPadLength   Specifies the maximum length over which to interpolate,
                     i.e., any consecutive blocks of NaNs with length greater
                     than maxPadLength will be left as NaN. Set as an integer.
                     maxPadLength=False (default) interpolates over all NaNs.

    Written by Eric Oliver, Institue for Marine and Antarctic Studies, University of Tasmania, Jun 2015

    """
    data_padded = data.copy()
    bad_indexes = np.isnan(data)
    good_indexes = np.logical_not(bad_indexes)
    good_data = data[good_indexes]
    interpolated = np.interp(
        bad_indexes.nonzero()[0], good_indexes.nonzero()[0], good_data
    )
    data_padded[bad_indexes] = interpolated
    if maxPadLength:
        blocks, n_blocks = ndimage.label(np.isnan(data))
        for bl in range(1, n_blocks + 1):
            if (blocks == bl).sum() > maxPadLength:
                data_padded[blocks == bl] = np.nan

    return data_padded
