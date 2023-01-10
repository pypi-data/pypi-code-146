import numpy as np
import pandas as pd
from datetime import datetime
from odhpy import utils


def derive_transformation_curves(original_ts: pd.Series, augmented_ts: pd.Series, season_start_months=[1,2,3,4,5,6,7,8,9,10,11,12]) -> dict:
    """Returns a dictionary of exceedence lookup tables - one for each season with the season's 
    start month as the key. These lookup tables map from ranked values of original_ts to ranked
    values of augmented_ts, within a given season. These are intended to be used for climate 
    change transformations.

    Args:
        original_ts (pd.Series): _description_
        augmented_ts (pd.Series): _description_
        season_start_months (list, optional): _description_. Defaults to [1,2,3,4,5,6,7,8,9,10,11,12].

    Returns:
        dict: _description_
    """
    df = pd.DataFrame()
    df["x"] = original_ts
    df["y"] = augmented_ts
    df = df.dropna() # Force common period
    answer = {}
    looped_months = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
    for i in range(len(season_start_months)):
        start_month = season_start_months[i]
        season_len = (season_start_months + [m + 12 for m in season_start_months])[i + 1] - start_month
        start_ind = start_month - 1
        months_in_this_season = looped_months[start_ind:start_ind + season_len]
        df_m = df[[d.month in months_in_this_season for d in df.index]]
        x = np.sort(df_m.x.values)
        y = np.sort(df_m.y.values)
        answer[start_month] = [x,y]
    return answer

    
def apply_transformation_curves(tranformation_curves: dict, series: pd.Series, zero_threshold=1e-9) -> pd.Series:
    """Applies seasonal transformation curves to an input series.
    Refer to the function 'derive_transformation_curves(...)'.

    Args:
        tranformation_curves (dict): _description_
        series (pd.Series): _description_
        zero_threshold (_type_, optional): Values less than the zero_threshold are treated as zero and map to zero. Defaults to 1e-9.

    Returns:
        pd.Series: _description_
    """
    looped_months = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
    dates = series.index
    answer = series.copy()
    # Loop over all the seasons and apply each transformation curves to the whole series. Splice the appropriate seasons into the 'answer' as we go. 
    season_start_months = sorted(tranformation_curves.keys())
    for i in range(len(season_start_months)):
        start_month = season_start_months[i]
        t = tranformation_curves[start_month]
        season_len = (season_start_months + [m + 12 for m in season_start_months])[i + 1] - start_month
        start_ind = start_month - 1
        months_in_this_season = looped_months[start_ind:start_ind + season_len]
        xp = t[0] #x coordinates of transformation function
        fp = t[1] #y coordinates of transformation function
        answer = np.where([d.month in months_in_this_season for d in dates], np.interp(series, xp, fp), answer)
    # Force everything below the zero_threshold to 0.
    answer = np.where(answer < zero_threshold, 0.0, answer)
    # Return a pd.Series so user can easily join it back into a dataframe
    return pd.Series(answer, index=dates, name=series.name)     
    
    