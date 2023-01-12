"""generate Network Devices (Switch/Router) facts from its configuration outputs.
"""

# ------------------------------------------------------------------------------
# BELOW ARE FUNCTION IMPORTED AND PUBLISHED OUT FOR TESTING ONLY.
# ADD A FUNCTION HERE TO TEST IT EXCLUSIVELY FROM OUTSIDE EXECUTION
# EXAMPLE:
# ------------------------------------------------------------------------------
# from .cisco_parser import absolute_command
# from .cisco import get_cdp_neighbour
# from .juniper import get_lldp_neighbour
# ------------------------------------------------------------------------------

from .database import write_to_xl, read_xl

from .merger import device
from .merger import DeviceDB



__all__ = [ 
	'write_to_xl', 'read_xl', 
	'device', 'DeviceDB',
	]

__ver__ = "0.0.5"