import numpy as np

def segment(fte:float) -> str or float:
    """ This function returns the segment based on the number of fte """
    if np.isnan(fte):
        return np.nan
    else:
        if fte >= 250:
            return 'LE'
        elif 50 <= fte < 250:
            return 'SME Large'
        elif 10 <= fte < 50:
            return 'SME Small'
        else:
            return 'SOHO'


def segment_specific(fte:float) -> str or float:
    """ This function returns the segment based on the number of fte """
    if np.isnan(fte):
        return np.nan
    else:
        if fte >= 250:
            return 'LE'
        elif 150 <= fte < 250:
            return 'ME+'
        elif 50 <= fte < 150:
            return 'ME-'
        elif 10 <= fte < 50:
            return 'SE'            
        else:
            return 'SOHO'


def cocon_category(distance:float, costs:float):
    """ This function determines the category (off/near/on net) given the distance and the costs according to Cocon """
    try:
        int(distance)
        if np.isnan(distance) or np.isnan(costs):
            return np.nan
        elif costs > 32000:
            return 'off-net'
        elif distance <= 50 and costs <= 32000:
            return 'on-net'
        else:
            return 'near-net'      
    except:
        return np.nan  


def sales_channel(fte:float, loc:float):
    """ This function determines the sales channel (DS/CS) given the FTE and # of business locations """
    if np.isnan(fte) and np.isnan(loc):
        return np.nan
    elif fte >= 150 or loc >=3:
        return 'Direct'
    else:
        return 'Commercial Services'


def company_size(fte:float, loc:float):
    """ This function determines the company size given the FTE and # of business locations """
    if np.isnan(fte) and np.isnan(loc):
        return np.nan
    elif fte >= 1000:
        return 'Corporate'
    elif 150 <= fte < 1000 or loc >= 3:
        return 'LE'    
    elif 50 <= fte < 150:
        return 'ME'
    elif np.isnan(fte):
        return np.nan            
    else:
        return 'SE'    
