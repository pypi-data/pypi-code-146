
# TO UPDATE 

# classify AP types --> Bardy et al. method // reference this paper


def find_aptype(max_sweeps_features_all, min_peak, dv_cutoff): 
    """
    Breakdown the number of AP analysed into different AP types as shown [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5071135/). 
    Calculated for default settings (AP amplitude >= 0 mV, dv/dt == 5). 
    Conducted on highest firing sweep. 

    Note: that ap type classification was based on 500 ms depolarisation steps, hence Hz metrics need to be considered.
    However, will stand for 1s + stimulations. 

    AP Type breakdown
    -----------------
    Type 5: >= 10 Hz firing freq
    Type 4: > 4  and < 10 Hz firing freq
    Type 2/3: > 0 and <= 2 avg_rate
    Type 1: == 0 Hz firing_freq
    
    Arguments
    ---------


    Returns
    -------


    """

    if min_peak == 0 and dv_cutoff == 5: 

        if len(max_sweeps_features_all) >= 1:
            avg_rate = max_sweeps_features_all.avg_rate.values[0]

            if avg_rate >= 10: 
                ap_type = 'Type 5'
            if (avg_rate >= 4) and (avg_rate < 10): 
                ap_type = 'Type 4'
            if (avg_rate > 0) and (avg_rate < 4): 
                ap_type = 'Type 2/3'
            if avg_rate == 0: 
                ap_type = 'Type 1'
                
            if math.isnan(avg_rate) == True: # exclude if no average rate found
                ap_type = np.nan
        else: 
            ap_type = np.nan
        
    else: 
        ap_type = 'min_peak != 0 & dv_cutoff != 5'
        
    return ap_type