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

from .facts_gen_from_fg import DeviceFactsFg

from .facts_gene_cisco import evaluate_cisco
from .facts_gene_juniper import evaluate_juniper


from .cleaning import evaluate



__all__ = [ 
	'write_to_xl', 'read_xl', 
	'device', 'DeviceDB',
	'DeviceFactsFg',
	'evaluate_cisco', 'evaluate_juniper', 'evaluate'
	]

__ver__ = "0.0.6"