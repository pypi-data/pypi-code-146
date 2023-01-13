""" 
core_load_utils.py 

Modules for general collection 
of data from data objects for 
core classes. 

"""


###################################################################################################
###################################################################################################


def find_sweepdata(data): 
    """ find sweepdata """

    try: 
        sweepdata = data.preprocessed_sweepdata # find preprocessed data 
    except:
        try: 
            sweepdata = data.sweepdata # if not, default to raw 
        except: 
            abf_id = data.metadata['abf_id']
            print(f'no data found for {abf_id}| re-load data with loader ...')   
        
    # note: to only be conducted in 
    # recordings from current clamp
    # with multiple sweep data
    #--------------------------------
    if len(sweepdata) > 1: 
        pass
    else: 
        raise ValueError('pass sweepdata | multiple sweeps not found ...')
        
    return sweepdata
        
        
def find_sweeptimes(data): 
    """ find sweep times """

    try: 
        sweeptimes = data.times # find preprocessed data 
    except:
        abf_id = data.metadata['abf_id']
        print(f'check sweepdata times for {abf_id} ...')
        
    # note: to only be conducted in 
    # recordings from current clamp
    # with multiple sweep data
    #--------------------------------
    if len(sweeptimes) > 1: 
        pass
    else: 
        raise ValueError('pass sweepdata | multiple sweeps not found ...')       
    
    return sweeptimes
    
    
def find_stimuli(data): 
    """ find current stimuli """
    
    try: 
        stimuli = data.commandwaveform        
    except: 
        raise ValueError('no stimuli data found ...')
    
    return stimuli


def find_srate(data): 
    """ find sampling rate frequency """
    
    try: 
        srate = data.metadata['sample_rate_hz']
    except AttributeError:
        abf_id = data.metadata['abf_id']
        print(f'no sampling rate found for {abf_id}| re-load data with loader ...')   
        
    return srate 