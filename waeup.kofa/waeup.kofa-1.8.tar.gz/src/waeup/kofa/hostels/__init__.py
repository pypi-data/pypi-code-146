"""This package contains everything regarding hostels.
"""
# Make this a package.
from waeup.kofa.hostels.container import HostelsContainer
from waeup.kofa.hostels.hostel import Hostel, Bed

__all__ = [
    'HostelsContainer',
    'Hostel',
    'Bed',
    ]
