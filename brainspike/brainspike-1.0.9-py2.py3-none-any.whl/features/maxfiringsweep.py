
## TO UPDATE 

def find_maxfiring_sweep(spikes_features_all, sweeps_features_all, baseline_voltage):
    """
    Returns max firing sweep features. 
    Max firing sweep determined by the following: 

    - find highest frequency firing sweep 
    - find sweep with lowest spike height adaptation
    - remove sweeps not within baseline voltage (default: baseline_voltage = [-80, -40])
    - find sweep with max ap (if more than one found, defaults to the earliest spike (i.e. lowest peak_index value))

    Arguments
    ---------


    Returns
    -------


    """

    if not spikes_features_all.empty:
        
        # removing spikes on selected sweep 
        # not within baseline voltage
        maxfiring_sweeps = sweeps_features_all[(sweeps_features_all['baseline_voltage'] >= baseline_voltage[0])
        & (sweeps_features_all['baseline_voltage'] <= baseline_voltage[1])] 
        
        if len(maxfiring_sweeps) > 0: 
            
            # isolating highest avg_rate firing sweeps
            maxfiring_sweeps = maxfiring_sweeps[maxfiring_sweeps['avg_rate'] == max(maxfiring_sweeps['avg_rate'])]

            # find sweep with lowest spike-height adaptation ratio
                # if only one selection default to highest firing rate only
            if maxfiring_sweeps['spike_height_adaptation'].isna().sum() == len(maxfiring_sweeps): 
                maxfiring_sweeps = maxfiring_sweeps
            else: 
                maxfiring_sweeps = maxfiring_sweeps[(maxfiring_sweeps['spike_height_adaptation']
                == min(maxfiring_sweeps['spike_height_adaptation']))]

            # selecting spike data from sweep with highest frequency and lowest spike-height adaptation
            max_spikes_features_all = spikes_features_all[spikes_features_all['sweep_number'].isin(maxfiring_sweeps['sweep_number'])]

            # find max firing sweep with max ap
            if not max_spikes_features_all.empty:  

                # sub-select highest amplitude spike 
                # on spikes from highest firing sweeps
                max_spikes_features_all = max_spikes_features_all[max_spikes_features_all['peak_v'] == max(max_spikes_features_all['peak_v'])]

                if len(max_spikes_features_all) > 1: # if more than 1 spike found defaul to first spike
                    max_spikes_features_all = max_spikes_features_all[max_spikes_features_all['peak_index'] == min(max_spikes_features_all['peak_index'])]

                # finding sweep number with highest AP spike
                max_sweeps_features_all = maxfiring_sweeps[maxfiring_sweeps['sweep_number'].isin(max_spikes_features_all['sweep_number'])] 

                #re-index
                max_sweeps_features_all.reset_index(drop=True, inplace=True) 
                max_spikes_features_all.reset_index(drop=True, inplace=True)

        return max_sweeps_features_all, max_spikes_features_all
