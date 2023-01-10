import numpy as np
import pandas as pd
from datetime import datetime
from odhpy import utils


def derive_transformation_curves(original_ts: pd.Series, augmented_ts: pd.Series, season_start_months=[1,2,3,4,5,6,7,8,9,10,11,12], epsilon=1e-3) -> dict:
    """Returns a dictionary of exceedence-based transformation curves - one for each season 
    with the season's start month as the key. These are tables that map from exceedance 
    (cunnane plotting position as a fraction) to a scaling factor. These are intended to 
    be used to
    effectively summarise climate-change adjustments, and allow them to be transported from
    one timeseries to another.

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
        # The transformation factor is y/x except when the original value x is 
        # zero (<epsilon) in which case we default to 1.0
        f = np.where(x < epsilon, 1.0, y / x)
        n = len(x)
        ii = [i + 1 for i in range(n)] #index starting at 1
        p = [(i - 0.4)/(n + 0.2) for i in ii]
        answer[start_month] = [p,f]
    return answer     

    
def apply_transformation_curves(tranformation_curves: dict, series: pd.Series) -> pd.Series:
    """Applies seasonal transformation curves to an input series.
    Refer to the function 'derive_transformation_curves(...)'.

    Args:
        tranformation_curves (dict): _description_
        series (pd.Series): _description_

    Returns:
        pd.Series: _description_
    """
    looped_months = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
    dates = series.index
    answer = series.copy()    
    # Apply each transformation curves to the whole series. Splice the appropriate 
    # parts (seasons) into the 'answer' series as we go. 
    season_start_months = sorted(tranformation_curves.keys())
    for i in range(len(season_start_months)):
        # Identify the transform curve for this season
        season_start = season_start_months[i]
        t = tranformation_curves[season_start]
        xp = t[0] 
        fp = t[1]  
        # Get a list of the months in this season
        season_len = (season_start_months + [m + 12 for m in season_start_months])[i + 1] - season_start
        start_ind = season_start - 1
        months_in_this_season = looped_months[start_ind:start_ind + season_len]
        # Now get a series of all the values in this season
        m = len(series)
        season_dates = pd.Series([d for d in dates if d.month in months_in_this_season])        
        values = answer[season_dates] #pd.Series([answer[d] for d in dates if d.month in months_in_this_season])
        # And get their ranks and plotting positions
        rank_starting_at_one = values.rank(ascending=True) # This function is nice because equal values are assigned the same (averaged) rank.
        n = len(values)
        p = [(r - 0.4)/(n + 0.2) for r in rank_starting_at_one] # plotting position
        f = np.interp(p, xp, fp) # interpolated scaling factors
        # Calcualte new values and update the answer
        new_values = pd.Series([values[i] * f[i] for i in range(n)], index=season_dates)
        answer.update(new_values)
    # Return a pd.Series so user can easily join it back into a dataframe
    return pd.Series(answer, index=dates, name=series.name)     
    
    