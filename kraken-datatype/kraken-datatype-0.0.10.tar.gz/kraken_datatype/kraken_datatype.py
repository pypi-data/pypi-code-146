
from kraken_datatype import _main_processor

"""
Methods to validate datatypes
"""

def validate(datatype, data):
    """ Validate if data matches datatype
    """
    
    return _main_processor.validate(datatype, data)


def normalize(datatype, data):
    """ Normalize data to match datatype
     Returns None if cannot be normalized
    """

    return _main_processor.normalize(datatype, data)

def guess(data):
    """ Find datatype fo a data
    """

    return _main_processor.guess(data)    
