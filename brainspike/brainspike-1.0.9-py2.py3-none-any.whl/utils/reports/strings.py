"""
strings.py

Formatted strings for printing out BrainSpike
related information.

"""

import numpy as np

## Settings & Globals
# Centering Value - Long & Short options
#   Note: Long CV of 98 is so that the max line length plays nice with notebook rendering
LCV = 98
SCV = 70

###################################################################################################
###################################################################################################

def gen_ap_overview_str(brainspike_obj, protocol = None, concise=False):
    """
    Generate a string representation of BrainSpike loaded *.abf files.
    
    Parameters
    ----------
    brainspike_obj (obj):
        brainspike object. 
    
    abf_files (list of strs): 
        selected abf files from file paths.
    
    concise (bool, default: False)
        whether to print the report in a concise mode, or not.
    
    Returns
    -------
    output (str): 
        formatted string of current settings.
        
    """

    # collect metadata
    sampling_rates = []; current_steps = []; sweep_lengths = []; abf_ids = []
    for x in range(len(brainspike_obj)): 
        abf_ids.append(brainspike_obj[x].metadata['abf_id'])
        sampling_rates.append(brainspike_obj[x].metadata['sample_rate_hz']),\
        current_steps.append(brainspike_obj[x].metadata['current_step_pa'])
        sweep_lengths.append(brainspike_obj[x].metadata['sweep_length_sec'])
        
    desc = {
        'number_abf_files' : 'Number of *.abf files loaded from selected file path.',
        'sampling_rates'   : 'Unique sampling rate listing from all loaded files.',
        'current_steps'    : 'Unique current steps (pA) from all loaded files.',
        'sweep_length'    : 'Unique sweep lengths (sec.) from all loaded files.',
        }
    
    # create output string
    str_lst = [

         # header
        '=',
        '',
        '\N{brain} BRAINSPIKE - ACTION POTENTIAL LOADER \N{brain}',
        '',
        
        # file summary
        *[el for el in ['Number of *.abf files : {}'.format(len(abf_ids)),
                        '{}'.format(desc['number_abf_files']),
                        '\n',
                        'Sampling rates (Hz) : {}'.format(np.unique(sampling_rates)),
                        '{}'.format(desc['sampling_rates']),
                        '\n',
                        'Current steps (pA) : {}'.format(np.unique(current_steps)),
                        '{}'.format(desc['current_steps']), 
                        '\n',
                        'Sweep length (sec.) : {}'.format(np.unique(sweep_lengths)),
                        '{}'.format(desc['sweep_length'])] if el != ''],
        
        # footer
        '',
        '='
    ]

    output = _format(str_lst, concise)

    return output


def gen_psc_overview_str(brainspike_obj, concise=False):
    """
    Generate a string representation of BrainSpike loaded *.abf files.
    
    Parameters
    ----------
    brainspike_obj (obj):
        brainspike object. 
    
    abf_files (list of strs): 
        selected abf files from file paths.
    
    concise (bool, default: False)
        whether to print the report in a concise mode, or not.
    
    Returns
    -------
    output (str): 
        formatted string of current settings.
        
    """

    # collect metadata
    sampling_rates = []; sweep_lengths = []; abf_ids = []
    for x in range(len(brainspike_obj)): 
        abf_ids.append(brainspike_obj[x].metadata['abf_id'])
        sampling_rates.append(brainspike_obj[x].metadata['sample_rate_hz']),\
        sweep_lengths.append(brainspike_obj[x].metadata['sweep_length_sec'])
        
    desc = {
        'number_abf_files' : 'Number of *.abf files loaded from selected file path.',
        'sampling_rates'   : 'Unique sampling rate listing from all loaded files.',
        'current_steps'    : 'Unique current steps (pA) from all loaded files.',
        'sweep_length'    : 'Unique sweep lengths (sec.) from all loaded files.',
        }
    
    # create output string
    str_lst = [

         # header
        '=',
        '',
        '\N{brain} BRAINSPIKE - PSC LOADER \N{brain}',
        '',
        
        # file summary
        *[el for el in ['Number of *.abf files : {}'.format(len(abf_ids)),
                        '{}'.format(desc['number_abf_files']),
                        '\n',
                        'Sampling rates (Hz) : {}'.format(np.unique(sampling_rates)),
                        '{}'.format(desc['sampling_rates']),
                        '\n',
                        'Sweep length (sec.) : {}'.format(np.unique(sweep_lengths)),
                        '{}'.format(desc['sweep_length'])] if el != ''],
        
        # footer
        '',
        '='
    ]

    output = _format(str_lst, concise)

    return output


def gen_psc_preprocessing_str(brainspike_obj, concise=False):
    """
    Generate a string representation of preprocessed params 
    for PSC current recording loaded *.abf files with BrainSpike. 
    
    Parameters
    ----------
    brainspike_obj (obj):
        brainspike object. 
    
    abf_files (list of strs): 
        selected abf files from file paths.
    
    concise (bool, default: False)
        whether to print the report in a concise mode, or not.
    
    Returns
    -------
    output (str): 
        formatted string of current settings.
        
    """
        
    # preprocessed param collection -- 
    # selected general params to provide an overview
    lowpass_filter_order = []; smoothing = []; baseline_subtract = []; 
    signal_drop = []; straightened = []
    
    for x in range(len(brainspike_obj)): 
        
        try: 
           lowpass_filter_order.append(brainspike_obj[x].preprocessed_params['lowpass_filter_order'])
        except KeyError: 
            pass
        
        try: 
            smoothing.append(brainspike_obj[x].preprocessed_params['smoothing_window'])
            smoothing = [x for x in smoothing if str(x) != 'nan'] # drop nan 
        except KeyError: 
            pass
        
        try: 
            baseline_subtract.append(brainspike_obj[x].preprocessed_params['baseline_subtract'])
            baseline_subtract = [x for x in baseline_subtract if str(x) != 'nan']
        except KeyError: 
            pass
        
        try: 
           signal_drop.append(brainspike_obj[x].preprocessed_params['signal_drop_time'])
           signal_drop = [x for x in signal_drop if str(x) != 'nan']
        except KeyError: 
            pass
        
        try: 
            straightened.append(brainspike_obj[x].preprocessed_params['straightening_time_segment'])
            straightened = [x for x in straightened if str(x) != 'nan']
        except KeyError: 
            pass
        
    desc = {
        'lowpass_filtered_files'    : 'Data subject to lowpass filtering.',
        'smoothed_files'            : 'Linear convolutions applied.',
        'baseline_subtracted_files' : 'Baseline subtraction applied.',
        'signal_drop_files'         : 'Signal drop exclusions applied.', 
        'straightened_files'        : 'Straightened signals.'
        }
    
    # create output string
    str_lst = [

         # header
        '=',
        '',
        '\N{brain} BRAINSPIKE - PREPROCESSED FILES \N{brain}',
        '',
        
        
        # file summary
        *[el for el in ['Lowpass filtered : {}'.format(len(lowpass_filter_order)),
                        '{}'.format(desc['lowpass_filtered_files']),
                        '\n',
                        'Smoothed : {}'.format(len(smoothing)),
                        '{}'.format(desc['smoothed_files']),
                        '\n',
                        'Baseline subtracted : {}'.format(len(baseline_subtract)),
                        '{}'.format(desc['baseline_subtracted_files']),
                        '\n',
                        'Signal dropped : {}'.format(len(signal_drop)),
                        '{}'.format(desc['signal_drop_files']),
                        '\n',
                        'Straightened : {}'.format(len(straightened)),
                        '{}'.format(desc['straightened_files'])] if el != ''],
        
        # footer
        '',
        '='
    ]

    output = _format(str_lst, concise)

    return output


def _format(str_lst, concise):
    """
    Format a string for printing.
    
    Parameters
    ----------
    str_lst (list of str)
        list containing all elements for the string, each element representing a line.
        
    concise (bool, default: False)
        whether to print the report in a concise mode, or not.
        
    Returns
    -------
    output : str
        formatted string, ready for printing.
        
    """

    # Set centering value - use a smaller value if in concise mode
    center_val = SCV if concise else LCV

    # Expand the section markers to full width
    str_lst[0] = str_lst[0] * center_val
    str_lst[-1] = str_lst[-1] * center_val

    # Drop blank lines, if concise
    str_lst = list(filter(lambda x: x != '', str_lst)) if concise else str_lst

    # Convert list to a single string representation, centering each line
    output = '\n'.join([string.center(center_val) for string in str_lst])

    return output