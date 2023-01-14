from pprint import pprint

from facts_finder.gene import KeyExchanger
from facts_finder.gene import VarInterfaceCisco
from facts_finder.gene import TableInterfaceCisco, TableVrfsCisco
from facts_finder import DeviceFactsFg
from facts_finder.database import write_to_xl, append_to_xl
from facts_finder.cisco_parser import get_op_cisco
import os

# ================================================================================================

def evaluate_cisco(
	capture_log_file,
	capture_file,
	var_column_mapper_file=None,
	int_column_mapper_file=None,
	):


	# ================================================================================================
	# var
	# ================================================================================================
	cmd_lst_var = {'show ipv6 interface brief': {'ipaddr': '//h2b-h3b'},
					'show route-map': {'set_clauses': '//reso'},
					'show version': {'hardware': 'hardware',
								'hostname': 'hostname',
								'mac': 'mac',
								'running_image': 'bootvar',
								'serial': 'serial',
								'version': 'ios_version'}}
	cmd_lst_int = {'show cdp neighbors detail': {'destination_host': '//nbr_hostname',
											'local_port': 'interface',
											'management_ip': 'nbr_ip',
											'platform': 'nbr_platform',
											'remote_port': 'nbr_interface'},
					'show etherchannel summary': {'group': 'int_number',
											'interfaces': '//po_to_interface',
											'po_name': 'interface'},
					'show interfaces': {'description': 'description',
									'duplex': 'duplex',
									'hardware_type': '//filter',
									'interface': 'interface',
									'ip_address': '//subnet',
									'link_status': 'link_status',
									'media_type': 'media_type',
									'protocol_status': 'protocol_status',
									'speed': 'speed'},
					'show interfaces switchport': {'access_vlan': 'access_vlan',
												'admin_mode': 'admin_mode',
												'interface': 'interface',
												'mode': '//interface_mode',
												'native_vlan': 'native_vlan',
												'switchport': 'switchport',
												'switchport_negotiation': 'switchport_negotiation',
												'trunking_vlans': '//vlan_members',
												'voice_vlan': 'voice_vlan'},
					'show ip bgp all summary': {'addr_family': 'bgp_vrf',
											'bgp_neigh': 'bgp_peer_ip'},
					'show ip bgp vpnv4 all neighbors': {'peer_group': 'bgp_peergrp',
													'remote_ip': 'bgp_peer_ip'},
					'show ip vrf interfaces': {'interface': 'interface', 'vrf': 'intvrf'},
					'show ipv6 interface brief': {'intf': 'interface', 'ipaddr': '//h4block'},
					'show lldp neighbors detail': {'local_interface': 'interface',
												'management_ip': 'nbr_ip',
												'neighbor': '//nbr_hostname',
												'neighbor_port_id': 'nbr_interface',
												'serial': 'nbr_serial',
												'vlan': 'nbr_vlan'},
					'show vrf': {'name': 'vrf'}}
	cmd_lst_vrf = {'show vrf': {'name': 'vrf'}}

	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	## 1.5 --- Optional if no mapper file provided
	if var_column_mapper_file is not None:
		for k,v in cmd_lst_var.copy().items():
			cmd_lst_var[k] = {}
		KEC_VAR = KeyExchanger(var_column_mapper_file, cmd_lst_var)
		cmd_lst_var = KEC_VAR.cisco_cmd_lst

	if int_column_mapper_file is not None:
		for k,v in cmd_lst_int.copy().items():
			cmd_lst_int[k] = {}
		KEC_INT = KeyExchanger(int_column_mapper_file, cmd_lst_int)
		cmd_lst_int = KEC_INT.cisco_cmd_lst
		#
		for k,v in cmd_lst_vrf.copy().items():
			cmd_lst_vrf[k] = {}
		KEC_VRF = KeyExchanger(int_column_mapper_file, cmd_lst_vrf)
		cmd_lst_vrf = KEC_VRF.cisco_cmd_lst

	## 2. ---  `var` Tab 
	CIV = VarInterfaceCisco(capture_file)
	CIV.execute(cmd_lst_var)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 
	CID = TableInterfaceCisco(capture_file)
	CID.execute(cmd_lst_int)
	append_to_xl(output_file, CID.pdf)

	## 4. ---  `vrf` Tab 
	TVC = TableVrfsCisco(capture_file)
	TVC.execute(cmd_lst_vrf)
	append_to_xl(output_file, TVC.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute()

	print(f'New Data Excel output stored in -> {output_file}')

	return {'var': CIV, 'output': output_file}


