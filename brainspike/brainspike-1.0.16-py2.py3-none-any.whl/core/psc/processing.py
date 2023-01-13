"""
processing.py

Class for detecting and extracting features 
from loaded and pre-processed synaptic data objects. 

"""

import pandas as pd

import numpy as np

from ...abf.abf_obj import ABF
from ...preprocessing.preprocessing_tools import find_thresh, find_startbaseline
from ...extractors.psc_extractor import detect_putative_pscs, refine_psc_times
from ...curation.psc_artefact_checks import rem_overlap_events, merge_events, rem_amps, rem_shortdur, rem_edge_events, rem_opposite_polarity
from ...features.psc_categorization import event_categorisation
from ...plots.psc_detection_plots import psc_detect_fig

###################################################################################################
###################################################################################################

class PSCDetect(object): 
    """ class for detecting synaptic input events in psc recordings """
    
    def __init__(self, data, amp_cutoffs = [10,800], thresh_detect_mode = 'donoho', std_thresh = None,\
                                                abs_thresh = None, baseline_thresh_multiplier = None,\
                                                baseline_segment = [0, 10], rms_win_len = None,\
                                                min_time_interval = 0.002, win_search_time = [0.5, 0.5],\
                                                overlap_time_thresh = 0, merge_time_thresh = 0.025,\
                                                duration_time_cutoffs = [0.001, 0.020], polarity = 'negative'): 
        """
        """
        
        self.data = data
        self.amp_cutoffs = amp_cutoffs
        self.min_time_interval = min_time_interval
        self.win_search_time = win_search_time
        self.overlap_time_thresh = overlap_time_thresh
        self.merge_time_thresh = merge_time_thresh
        self.duration_time_cutoffs = duration_time_cutoffs
        self.polarity = polarity
        self.baseline_segment = baseline_segment
        
        self.threshold_parameters_kwargs = {'thresh_detect_mode': thresh_detect_mode, 'abs_thresh': abs_thresh, 'std_thresh': std_thresh,\
                                            'baseline_thresh_multiplier': baseline_thresh_multiplier,\
                                            'baseline_segment': self.baseline_segment, 'rms_win_len': rms_win_len}  
    
    
    @property
    def _process(self): 
        """ detect and extract features from psc events """
        
        try: 
            isinstance(self.data, ABF)
            self._find_sweepdata 
        except AttributeError: 
            print("pass single data object")
                
        # find thresholds
        #----------------
        # finds low and high
        # thresholds for processing
        
        lowthr, highthr = find_thresh(sweepdata = self.sweepdata,\
                            srate = self.srate, **self.threshold_parameters_kwargs)
        
        # putative psc peaks 
        #-----------------
        # first pass to find 
        # psc peaks
        
        peaks_idx, peaks = detect_putative_pscs(self.sweepdata, highthr = highthr, distance = self.min_time_interval, srate = self.srate)
        
        
        # refine psc times
        #-----------------
        # find start and end times w/in thresholds
        # and detection parameters
        
        psc_times = refine_psc_times(self.sweepdata, win_search_time = self.win_search_time,\
                                    lowthr = lowthr, peaks_idx = peaks_idx, peaks = peaks, srate = self.srate)
        
        if not psc_times.size: 
            return pd.DataFrame() # save time if no pscs detected
        
        # remove overlapping event times
        #-------------------------------
        # find start diff of each event
        # if overlapping, remove
        # as likely the same event detected
        
        psc_times = rem_overlap_events(event_times = psc_times, overlap_time_thresh = self.overlap_time_thresh, srate = self.srate) # is this removing too many? 

        # merge psc event times
        #----------------------
        # merge psc event times
        # <= merge time thresholds 
        
        psc_times = merge_events(event_times = psc_times, srate = self.srate, merge_time_thresh = self.merge_time_thresh)

        # remove large psc events
        #------------------------
        # filter pscs between amp cutoffs
        
        psc_times = rem_amps(sweepdata = self.sweepdata, event_times = psc_times, amp_cutoffs = self.amp_cutoffs)

        # remove short duration psc events
        #---------------------------------
        # filter pscs between duration
        # cutoffs

        psc_times = rem_shortdur(event_times = psc_times, srate = self.srate, duration_time_cutoffs = self.duration_time_cutoffs)

        # remove edge frame psc events
        #-----------------------------
        # remove events on edge frames
        
        psc_times = rem_edge_events(sweepdata = self.sweepdata, event_times = psc_times)
        
        # check event polarity
        #---------------------
        # events not with the correct
        # polarity are removed
        
        baseline = find_startbaseline(self.sweepdata, self.srate, baseline_segment = self.baseline_segment) # not abs signal
        psc_times = rem_opposite_polarity(sweepdata = self.sweepdata, baseline = baseline, event_times = psc_times, polarity = self.polarity)
        
        # find event types 
        #-----------------
        # find singlets, doublets
        # triplets, bursts .....
        
        df_pscs = event_categorisation(sweepdata = self.sweepdata, event_times = psc_times, highthr = highthr, srate = self.srate)
        
        # attach metadata to psc df 
        if isinstance(self.data, list): 
            df_pscs['abf_id'] = self.data[self.i].metadata['abf_id']
            
        elif isinstance(self.data, ABF): 
            df_pscs['abf_id'] = self.data.metadata['abf_id']
        
        return df_pscs
        
    
    def final_psc_times(self, df_pscs):
        """ final psc times after processing """
        
        return np.column_stack((df_pscs.event_start.values, df_pscs.event_end.values))
    
    
    def psc_event_plot(self, df_pscs, burst_num): 
        """ burst event widget """

        psc_times = self.final_psc_times(df_pscs)
        
        psc_detect_fig(sweepdata = self.sweepdata, event_times = psc_times, burst_num = burst_num, srate = self.srate)  


    @property
    def _find_sweepdata(self): 
        """ find sweepdatas and srates """
        
        # fix this ... 
        try: 
            self.i
            
            try: 
                self.sweepdata = self.data[self.i].straightened_sweepdata
            except AttributeError: 
                
                try: 
                    self.sweepdata = self.data[self.i].baselinecorr_sweepdata_dropped 
                except AttributeError: 
            
                    try: 
                        self.sweepdata = self.data[self.i].baselinecorr_sweepdata 
                    except AttributeError: 
                        
                        try: 
                            self.sweepdata = self.data[self.i].preprocessed_sweepdata 
                        except AttributeError:
                            self.sweepdata = self.data[self.i].sweepdata 
                            
            # note: to only be conducted in 
            # recordings from voltage clamp 
            # hence, no multidimensional arrays
            #----------------------------------
            
            if len(self.sweepdata) > 1: 
                raise ValueError('pass voltage clamp data | multiple sweeps found ...')
            else: 
                self.sweepdata = self.sweepdata[0]
                
            try: 
                self.srate = self.data[self.i].metadata['sample_rate_hz']
            except AttributeError:
                print('no sampling rate found | re-load data with loader ...')
                
        except AttributeError: # if not nested
            
            try: 
                self.sweepdata = self.data.straightened_sweepdata 
            except AttributeError: 
                
                try: 
                    self.sweepdata = self.data.baselinecorr_sweepdata_dropped 
                except AttributeError: 
            
                    try: 
                        self.sweepdata = self.data.baselinecorr_sweepdata 
                    except AttributeError: 
                        
                        try: 
                            self.sweepdata = self.data.preprocessed_sweepdata 
                        except AttributeError:
                            self.sweepdata = self.data.sweepdata 
                            
                            
            if len(self.sweepdata) > 1: 
                raise ValueError('pass voltage clamp data | multiple sweeps found ...')
            else: 
                self.sweepdata = self.sweepdata[0]
                
            try: 
                self.srate = self.data.metadata['sample_rate_hz']
            except AttributeError:
                print('no sampling rate found | re-load data with loader ...')   
    
    
    
class PSCDetectGroup(PSCDetect): 
    """ class for group psc detection """
    
    def __init__(self, data, amp_cutoffs = [10,800], thresh_detect_mode = 'donoho', std_thresh = None,\
                                                abs_thresh = None, baseline_thresh_multiplier = None,\
                                                baseline_segment = [0, 10], rms_win_len = None,\
                                                min_time_interval = 0.002, win_search_time = [0.5, 0.5],\
                                                overlap_time_thresh = 0, merge_time_thresh = 0.025,\
                                                duration_time_cutoffs = [0.001, 0.020], polarity = 'negative'): 
        """
        """
        
        super().__init__(data, amp_cutoffs, thresh_detect_mode, std_thresh, abs_thresh,\
                        baseline_thresh_multiplier, baseline_segment, rms_win_len, min_time_interval,\
                        win_search_time, overlap_time_thresh, merge_time_thresh, duration_time_cutoffs, polarity)
        
    def __iter__(self): 

        if isinstance(self.data, list): 
            if len(self.data) > 1: 
                self.i = -1
                return self 
        
    def __next__(self): 

        self.i += 1
        if self.i < len(self.data): 
            if isinstance(self.data[self.i], ABF):
                
                self._find_sweepdata
                
                df_pscs = self._process
                
                return df_pscs
            
        raise StopIteration
    



                
        
    
    
    
        
        
        