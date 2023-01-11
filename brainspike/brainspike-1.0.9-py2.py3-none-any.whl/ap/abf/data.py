"""
abf_ap_data.py

Michael Zabolocki, Aug 2022

Data (v,t,c) from abf files using pyabf. 
"""

# scipy
from scipy import signal

# numpy
import numpy as np

# pyabf
import pyabf

#-----------------------------

class AbfApData: 

    def __init__(self, file_selected, lowpass_cutoff, filter_order, win_len): 
        """
        
        Arguments
        ---------


        Returns
        -------
        

        """
        self.abf = pyabf.ABF(file_selected) # create abf object

        #--------------
        # voltage, current (injected), time arrays
        # appended for each sweep
        stimulus = []
        voltage = []
        time = []
        
        # extract data per sweep for loaded 
        # abf file
        for sweepnumber in self.abf.sweepList:
            self.abf.setSweep(sweepnumber)  
            time.append(self.abf.sweepX)
            stimulus.append(self.abf.sweepC)

            # if lowpass_cutoff and/or win_len parsed
            # lowpass filter and/or smooth raw signal in loader
            if (lowpass_cutoff != None) and (win_len == None): 
                voltage.append(self.low_pass(self.abf.sweepY, filter_order, lowpass_cutoff, self.abf.sampleRate)) 

            elif (lowpass_cutoff == None) and (win_len != None): 
                voltage.append(self.convolution(self.abf.sweepY, self.abf.sampleRate, win_len)) 

            elif (lowpass_cutoff != None) and (win_len != None): 
                lowpass_voltage = self.low_pass(self.abf.sweepY, filter_order, lowpass_cutoff, self.abf.sampleRate)
                lowpass_smoothed_voltage = self.convolution(lowpass_voltage, self.abf.sampleRate, win_len)
                voltage.append(lowpass_smoothed_voltage) 

            elif (lowpass_cutoff == None) and (win_len == None): 
                # no processing
                voltage.append(self.abf.sweepY) 

        #--------------
        # add to self
        self.time = np.array(time)
        self.voltage = np.array(voltage)
        self.stimulus = np.array(stimulus)


    def low_pass(self, data, filter_order, lowpass_cutoff, sampling_rate):
        """
        Returns the low-pass filter with a 4th butter
        Arguments
        ---------
        data (array):
        A NumPy array with the data (e.g., voltage in microVolts)

        cutoff (float):
        the cutoff frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points.

        Example
        -------
        >>> Nyquist = 30e3/2
        >>> mycutoff = 250/Nyquist # for 250 Hz low pass filter
        >>> mytrace = low_pass(data = rec, cutoff = mycutoff)
        """

        myparams = dict(btype='lowpass', analog=False)

        # generate filter kernel (a and b)
        if filter_order == None: 
            filter_order = 4 # default to 4th order if == None

        b, a = signal.butter(N = filter_order, Wn = lowpass_cutoff, **myparams, fs = sampling_rate)

        return signal.filtfilt(b,a, data)


    def convolution(self, data, sampling_rate, win_len): 
        """
        Smoothing for processing. 

        Arguments
        ---------


        Returns
        -------



        ----------------
        https://numpy.org/doc/stable/reference/generated/numpy.convolve.html

        Mode == 'same': 
            returns output of length max(M, N).
            boundary effects are still visible. 

        Mode == 'valid': 
            returns output of length max(M, N) - min(M, N) + 1. 
            the convolution product is only given for points where the signals overlap completely.
            values outside the signal boundary have no effect.
        """

        data = np.convolve(data, np.ones(int(sampling_rate*win_len)), 'same') / (sampling_rate*win_len)

        return data
