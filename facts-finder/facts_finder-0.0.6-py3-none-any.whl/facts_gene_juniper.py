from pprint import pprint

from facts_finder.gene import KeyExchanger
from facts_finder.gene import VarInterfaceJuniper
from facts_finder.gene import TableInterfaceJuniper
from facts_finder import DeviceFactsFg
from facts_finder.database import write_to_xl, append_to_xl

from facts_finder.common import get_op
from nettoolkit import JSet
from facts_finder.common import verifid_output
import os

# ================================================================================================

def evaluate_juniper(
	capture_log_file,
	capture_file,
	column_mapper_file=None,
	):

	# ================================================================================================
	# var
	# ================================================================================================

	juniper_cmd_lst = {'show interfaces | no-more': {'admin_state': 'link_status',
												'description': 'description',
												'destination': '//subnet',
												'hardware_type': 'GRE',
												'interface': 'interface',
												'link_status': 'protocol_status',
												'local': '//subnet1'},
					'show lacp interfaces | no-more': {'aggregated_interface': 'interface',
													'member_interface': '//po_to_interface'},
					'show lldp neighbors | no-more': {'local_interface': 'interface',
												   'port_info': 'nbr_interface',
												   'system_name': '//nbr_hostname'},
					'show version | no-more': {'hostname': 'hostname',
											'junos_version': 'ios_version',
											'model': 'hardware',
											'serial_number': 'serial'}}

	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	## 1.5 --- Optional if no mapper file provided
	if column_mapper_file is not None:
		for k,v in juniper_cmd_lst.copy().items():
			juniper_cmd_lst[k] = {}
		KEC_VAR = KeyExchanger(column_mapper_file, juniper_cmd_lst)
		juniper_cmd_lst = KEC_VAR.cisco_cmd_lst

	## 2. ---  `var` Tab 
	CIV = VarInterfaceJuniper(capture_file)
	CIV.execute(juniper_cmd_lst)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 
	CID = TableInterfaceJuniper(capture_file)
	CID.execute(juniper_cmd_lst)
	append_to_xl(output_file, CID.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute_juniper()

	print(f'New Data Excel output stored in -> {output_file}')

	return {'var': CIV, 'output': output_file}


# # ================================================================================================


