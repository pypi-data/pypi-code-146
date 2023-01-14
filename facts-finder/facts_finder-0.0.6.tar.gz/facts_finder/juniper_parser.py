"""Juniper devices (Switch/Router) configuration parser directive. 

local variables::
	List down all commands requires to be parsed here in dictionary of tuples.
	where index-0 refers to command and index-1 refers to filters/arguments if any

	juniper_cmds_list = OrderedDict([
		('show lldp neighbors', {'dsr': True}),		# dsr = domain suffix removal
		('show configuration', {}),
		('show version', {}),
		('show interfaces descriptions', {}),
		('show chassis hardware', {}),
		('show arp', {}),
		## ADD More as grow ## ])

	List down all commands: belonging level here in dictionary

	juniper_cmds_op_hierachy_level = {
		'show lldp neighbors': 'Interfaces',
		'show configuration': ('Interfaces', 'system'),
		'show version': 'system',
		'show interfaces descriptions': 'Interfaces',
		'show chassis hardware': 'Interfaces',
		'show arp': 'arp',
		## ADD More as grow ##	}

	Juniper commands prefered to be unfitered (i.e without any | symbols)

Returns:
	None: None
"""
# ------------------------------------------------------------------------------
from collections import OrderedDict

from facts_finder.juniper import get_lldp_neighbour
from facts_finder.juniper import get_int_description
from facts_finder.juniper import get_chassis_hardware
from facts_finder.juniper import get_arp_table
from facts_finder.juniper import get_interfaces_running
from facts_finder.juniper import get_version
from facts_finder.juniper import get_running_system
from facts_finder.juniper import get_instances_running
from facts_finder.juniper import get_instances_bgps
from facts_finder.common import get_op
from facts_finder.device import DevicePapa
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# // Juniper //
# ------------------------------------------------------------------------------
# COMMANDS LIST DICTIONARY, DEFINE **kwargs as dictionary in command value     #
# ------------------------------------------------------------------------------
juniper_cmds_list = OrderedDict([
	('show lldp neighbors', {'dsr': True}),		# dsr = domain suffix removal
	('show configuration', {}),
	('show version', {}),
	('show interfaces descriptions', {}),
	('show chassis hardware', {}),
	('show arp', {}),
	## ADD More as grow ##
])
# ------------------------------------------------------------------------------
# COMMAND OUTPUT HIERARCHY LEVEL
# ------------------------------------------------------------------------------
juniper_cmds_op_hierachy_level = {
	'show lldp neighbors': 'Interfaces',
	'show configuration': ('Interfaces', 'system', 'vrf', 'bgp neighbor'),
	'show version': 'system',
	'show interfaces descriptions': 'Interfaces',
	'show chassis hardware': 'Interfaces',
	'show arp': 'arp',
	## ADD More as grow ##
}
# ------------------------------------------------------------------------------
# Dict of Juniper commands, %trunked commands mapped with parser func.
# ------------------------------------------------------------------------------
juniper_commands_parser_map = {
	'show lldp neighbors': get_lldp_neighbour,
	'show configuration': (get_interfaces_running, get_running_system, get_instances_running, get_instances_bgps),
	'show version': get_version,
	'show interfaces descriptions': None,
	'show interfaces terse': None,
	'show chassis hardware': get_chassis_hardware,
	'show arp': get_arp_table,
	'show bgp summary': None,
}
# ------------------------------------------------------------------------------

def absolute_command(cmd, cmd_parser_map, op_filter=False):
	"""returns absolute truked command if any filter applied
	if founds an entry in juniper_commands_parser_map keys.

	Args:
		cmd (str): executed/ captured command ( can be trunked or full )
		cmd_parser_map (dict, set): containing juniper standard trunked command
		op_filter (bool, optional): to be remove any additional filter from command or not. Defaults to False.

	Returns:
		str: juniper command - trunked
	"""    	
	if op_filter:
		abs_cmd = cmd.split("|")[0].strip()
	else:
		abs_cmd = cmd.replace("| no-more", "").strip()
	for c_cmd in cmd_parser_map:
		word_match = abs_cmd == c_cmd
		if word_match: break
	if word_match:  return abs_cmd
	return cmd

# ------------------------------------------------------------------------------
class Juniper(DevicePapa):
	"""class defining juniper parser directives.

	Args:
		DevicePapa (type): Common shared methods/properties definitions under this parent class.
	"""    	
	
	def __init__(self, file):
		"""Initialize the object by providing the capture file

		Args:
			file (str): capture file
		"""    		
		super().__init__(file)

	def parse(self, cmd, *arg, **kwarg):
		"""start command output parsing from provided capture.
		provide any additional arg, kwargs for dynamic filter purpose.

		Args:
			cmd (str): juniper command for which output to be parsed

		Returns:
			dict: dictionary with the details captured from the output
		""" 
		abs_cmd = absolute_command(cmd, juniper_commands_parser_map)
		parse_func = juniper_commands_parser_map[abs_cmd]
		if isinstance(parse_func, tuple):
			parsed_op = [self.run_parser(pf, abs_cmd, *arg, **kwarg) for pf in parse_func]
		else:
			parsed_op = self.run_parser(parse_func, abs_cmd, *arg, **kwarg)
		return parsed_op

	def run_parser(self, parse_func, abs_cmd, *arg, **kwarg):
		"""derives the command output list for the provided trunked command.
		and runs provided parser function on to it to get the necessary details.
		provide any additional arg, kwargs for dynamic filter purpose.

		Args:
			parse_func (func): function
			abs_cmd (str): juniper trunked command for which output to be parsed

		Returns:
			dict: dictionary with the details captured from the output
		"""   
		op_list = get_op(self.file, abs_cmd)		
		if not parse_func: return None
		po = parse_func(op_list, *arg, **kwarg)
		return po

# ------------------------------------------------------------------------------
