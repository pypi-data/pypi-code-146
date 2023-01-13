"""
abf_obj.py

Class for abf object containing data and metadata. 

"""

from .data import ABFData
from .metadata import ABFMetadata

###################################################################################################
###################################################################################################

class ABF(ABFMetadata, ABFData): 

    def __init__(self, file_path = None, protocol = None): 
        """
        
        Parent class for ABF data and metadata
        inheritance. 
        
        Arguments
        ---------
        file_path (str): 
            abs path to *.abf file. 
        
        """

        super(ABFMetadata, self).__init__(file_path, protocol = protocol)
                 