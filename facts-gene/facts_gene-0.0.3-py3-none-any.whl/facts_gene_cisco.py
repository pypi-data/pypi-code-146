from pprint import pprint

from facts_gene import KeyExchanger
from facts_gene import VarInterfaceCisco
from facts_gene import TableInterfaceCisco, TableVrfsCisco
from facts_gene import DeviceFactsFg
from capture_it.database import write_to_xl, append_to_xl
from facts_finder.cisco_parser import get_op_cisco
import os

# ================================================================================================

def evaluate_cisco(
	capture_log_file,
	capture_file,
	var_column_mapper_file,
	int_column_mapper_file,
	):


	# ================================================================================================
	# var
	# ================================================================================================
	cmd_lst_var = {
		'show version': {},
		'show route-map': {},
		'show ipv6 interface brief': {}
	}
	cmd_lst_int = {
		'show interfaces':{},
		'show interfaces switchport':{}, 
		'show ipv6 interface brief':{}, 
		'show cdp neighbors detail':{}, 
		'show lldp neighbors detail':{}, 
		'show ip vrf interfaces':{}, 
		'show vrf':{},
		'show etherchannel summary':{}, 
		'show ip bgp vpnv4 all neighbors':{}, 
		'show ip bgp all summary':{},
	}
	cmd_lst_vrf = {
		'show vrf':{},
	}


	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	## 2. ---  `var` Tab 
	KEC_VAR = KeyExchanger(var_column_mapper_file, cmd_lst_var)
	cmd_lst_var = KEC_VAR.cisco_cmd_lst
	CIV = VarInterfaceCisco(capture_file)
	CIV.execute(cmd_lst_var)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 
	KEC_INT = KeyExchanger(int_column_mapper_file, cmd_lst_int)
	cmd_lst_int = KEC_INT.cisco_cmd_lst
	CID = TableInterfaceCisco(capture_file)
	CID.execute(cmd_lst_int)
	append_to_xl(output_file, CID.pdf)

	## 4. ---  `vrf` Tab 
	KEC_VRF = KeyExchanger(int_column_mapper_file, cmd_lst_vrf)
	cmd_lst_vrf = KEC_VRF.cisco_cmd_lst
	TVC = TableVrfsCisco(capture_file)
	TVC.execute(cmd_lst_vrf)
	append_to_xl(output_file, TVC.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute()

	print(f'Check output in -> {output_file}')

	return {'var': CIV, 'output': output_file}


