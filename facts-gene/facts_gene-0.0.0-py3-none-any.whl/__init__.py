"""Modify Network Devices (Switch/Router) facts.
"""

from facts_gen_commons import KeyExchanger, CiscoDB
from facts_gen_tables_ntct import TableInterfaceCisco, TableInterfaceJuniper, TableVrfsCisco
from facts_gen_var_ntct import VarInterfaceCisco, VarInterfaceJuniper

__all__ = [ 
	'KeyExchanger', 'CiscoDB',
	'TableInterfaceCisco', 'TableInterfaceJuniper', 'TableVrfsCisco',
	'VarInterfaceCisco', 'VarInterfaceJuniper',
	]

__ver__ = "0.0.0"