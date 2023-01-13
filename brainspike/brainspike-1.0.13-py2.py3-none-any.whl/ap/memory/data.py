"""
memory_ap_data.py

Michael Zabolocki, Oct 2022

Data (v,t,c) object for in memory files. 
"""

# numpy
import numpy as np

class MemoryApData: 
    def __init__(self, time, stimulus, voltage): 
        """
        Return time, stimulus and voltage arrays in 
        memory obects into object. 
        
        Arguments
        ---------


        Returns
        -------
        

        """
        
        # stimulus --> np.array conv
        if isinstance(stimulus, np.ndarray):
            self.stimulus = stimulus
        elif isinstance(voltage, list):
            self.stimulus = np.array(stimulus)

        # voltage --> np.array conv
        if isinstance(voltage, np.ndarray):
            self.voltage = voltage
        elif isinstance(voltage, list):
            self.voltage = np.array(voltage)

        # time --> np.array conv
        if isinstance(time, np.ndarray):
            self.time = time
        elif isinstance(time, list):
            self.time = np.array(time)

        
       