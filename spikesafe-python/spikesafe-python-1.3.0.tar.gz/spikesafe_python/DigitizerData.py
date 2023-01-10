# Goal: Parse Digitizer voltage readings into an accessible object

import math

class DigitizerData():
    """ A class used to store data in a simple accessible object from a digitizer fetch response
 
    Generally, this class will be used within an array of DigitizerData objects.

    Attributes
    ----------
    sample_number : int
        Sample number of the voltage reading
    voltage_reading : float
        Digitizer voltage reading

    """

    sample_number = 0
    
    voltage_reading = math.nan

    def __init__(self):
        pass