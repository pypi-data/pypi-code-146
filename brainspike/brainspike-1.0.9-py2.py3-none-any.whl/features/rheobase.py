## TO UPDATE 

def find_rheobase(sweep_features_all): 
    """
    Returns rheobase (pA) per sweep as df. 
    """

    rheobase = pd.DataFrame(columns=['rheobase (pA)'])

    if not sweep_features_all.empty:

        # find sweep > 0 Hz
        firing_sweeps = sweep_features_all[(sweep_features_all['avg_rate'] !=0) & (sweep_features_all['avg_rate'] != np.nan)] 
        
        # first sweep with avg_rate > 0 Hz
        if len(firing_sweeps) > 0: 
            rheobase_idx = firing_sweeps.index[0] # selecting first sweep with avg_rate > 0 Hz
            current_steps = sweep_features_all['current_analysed_sweep_pa'] 
            rheobase = current_steps[rheobase_idx]

        else: 
            rheobase = np.nan

        return rheobase