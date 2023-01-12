
import nettoolkit as nt
import pandas as pd
import numpy as np
from pprint import pprint
from .facts_gen_commons import *


# ================================================================================================
# Functions for DataFrame Modification Apply
# ================================================================================================

def nbr_hostname(hn):
	return hn.split(".")[0]

def h4block(h4block):
	l = eval(h4block)
	if isinstance(l, (list, set, tuple)):
		try:
			v6 = nt.IPv6(l[-1][:-2]+"/64")
			block = v6.get_hext(4)  # vua/vsa/wlc
			if block and block!='0':
				return block
			block = v6.get_hext(7)  # via
			if block and block!='0':
				return block
			return ""
		except: 
			pass
	return ""

def interface_mode(mode):
	if mode.startswith("trunk"): return "trunk"
	if mode.startswith("access"): return "access"
	return ""

def vlan_members(members):
	if members == "['ALL']": return ""
	if members == "": return ""
	return members.replace("'", "").replace("[", "").replace("]", "")

def filter_col(filtercol):
	filter_map = {
		'Ethernet SVI': 'vlan',
		'EtherChannel' : 'aggregated',
		'Loopback': 'loopback',			
	}
	if filtercol in filter_map:
		return filter_map[filtercol]
	return 'physical'

def subnet(subnet):
	try:
		return nt.IPv4(subnet).n_thIP(0, withMask=True)
	except:
		subnet

def shrink_if(intf):
	return nt.STR.shrink_if(intf)

def intvrf_update(vrf):
	if vrf.lower()=='mgmt-vrf': return ""
	return vrf


# ================================================================================================
# Juniper Database Tables Object
# ================================================================================================
class TableInterfaceJuniper(CiscoDB):
	
	interface_para = {
		# "show lacp interfaces | no-more",
		"show lldp neighbors | no-more",
		"show interfaces | no-more",
	}

	def __init__(self, capture):
		super().__init__(capture)
		self.dfd = self.read_int_sheets()

	def execute(self, cmd_lst):
		self.pdf = self.remove_unwanted(cmd_lst)
		self.merge_interface_data(cmd_lst)
		# self.remove_duplicates()
		self.pdf = {'tables': self.pdf}

	def merge_interface_data(self, cmd_lst):
		pdf = pd.DataFrame({'interface':[]})
		for sheet, df in self.dfd.items():
			if sheet not in self.interface_para: continue
			if sheet == "show lldp neighbors | no-more":
				df.rename(columns={'local_interface': 'interface', })
			ndf = df[ cmd_lst[sheet].keys() ]
			ndf = ndf.rename(columns=cmd_lst[sheet])
			# ndf['interface'] = ndf['interface'].apply(shrink_if)
			pdf = pd.merge( ndf, pdf, on=['interface',], how='outer').fillna("")
		self.pdf = pdf

	def remove_duplicates(self):
		columns_to_rename = {
			# 'neighbor_hostname': 'nbr_hostname',
			# 'description_y': 'description',
		}
		drop_cols = {
			'//subnet', '//subnet1', '//nbr_hostname', 
		}
		self.pdf.drop(drop_cols, axis=1, inplace=True)


# ================================================================================================
# Cisco Database Tables Object
# ================================================================================================
class TableInterfaceCisco(CiscoDB):
	
	interface_para = {
		'show interfaces',
		'show interfaces switchport', 
		'show ipv6 interface brief', 
		'show lldp neighbors detail',
		'show cdp neighbors detail',
		'show ip vrf interfaces',
		'show etherchannel summary', 
	}

	def __init__(self, capture):
		super().__init__(capture)
		self.dfd = self.read_int_sheets()

	def execute(self, cisco_cmd_lst):
		self.remove_unwanted(cisco_cmd_lst)
		self.merge_interface_data(cisco_cmd_lst)
		self.remove_duplicates()
		self.update_func_cols()
		self.po_to_interface()
		self.pdf = {'tables': self.pdf}

		
	def po_to_interface(self):
		pos = self.dfd['show etherchannel summary']['po_name']
		intfs = self.dfd['show etherchannel summary']['interfaces']
		int_dict = {'interface':[],'channel_grp':[]}
		for po, ints in zip(pos, intfs):
			channel_group_no = po[2:]
			ints = eval(ints)
			for i in ints:
				int_dict['interface'].append(i)
				int_dict['channel_grp'].append(channel_group_no)
		df = pd.DataFrame(int_dict)
		self.pdf = pd.merge(self.pdf , df, on=['interface',], how='outer').fillna("")
		self.pdf.drop(['//po_to_interface'], axis=1, inplace=True)


	def merge_interface_data(self, cisco_cmd_lst):
		pdf = pd.DataFrame({'interface':[]})
		for sheet, df in self.dfd.items():
			if sheet not in self.interface_para: continue
			ndf = df[ cisco_cmd_lst[sheet].keys() ]
			ndf = ndf.rename(columns=cisco_cmd_lst[sheet])
			ndf['interface'] = ndf['interface'].apply(shrink_if)
			pdf = pd.merge( ndf, pdf, on=['interface',], how='outer').fillna("")
		self.pdf = pdf

	def remove_duplicates(self):
		duplicated_cols = {
			'//nbr_hostname_x': '//nbr_hostname_y', 
			'nbr_interface_x': 'nbr_interface_y',
			'nbr_ip_x': 'nbr_ip_y',
		}
		for x, y in duplicated_cols.items():
			if self.pdf[x].equals(self.pdf[y]):
				self.pdf.rename(columns={x: x[:-2]}, inplace=True)
			else:
				self.pdf[x[:-2]] = np.where( self.pdf[x]!="", self.pdf[x], self.pdf[y]) 
				self.pdf.drop([x], axis=1, inplace=True)
			self.pdf.drop([y], axis=1, inplace=True)


	def update_func_cols(self):
		func_cols = {
			'//nbr_hostname': nbr_hostname,
			'//h4block': h4block,
			'//interface_mode': interface_mode,
			'//vlan_members': vlan_members,
			'//filter': filter_col,
			'//subnet': subnet,
		}
		for col, func in func_cols.items():
			self.pdf[col[2:]] = self.pdf[col].apply(func)
			self.pdf.drop([col], axis=1, inplace=True)
		#
		self.pdf['nbr_interface'] = self.pdf['nbr_interface'].apply(shrink_if)
		self.pdf['intvrf'] = self.pdf['intvrf'].apply(intvrf_update)



# ================================================================================================
# Cisco Database VRF Object
# ================================================================================================
def get_rt(default_rd):
	try:
		rt = default_rd.split(":")[-1]
		if rt != "<not set>":
			return rt
		else:
			return ""
	except: return ""

class TableVrfsCisco(CiscoDB):
	
	interface_para = {
		'show vrf',
	}

	def __init__(self, capture):
		super().__init__(capture)
		self.dfd = self.read_int_sheets()

	def execute(self, cisco_cmd_lst):
		self.vrf_df = self.dfd['show vrf']
		self.update_column_names()
		self.drop_mtmt_vrf()
		self.add_filter_col()
		self.update_rt()
		self.pdf = {'vrf': self.vrf_df}

	def update_column_names(self):
		self.vrf_df.rename(columns={'name': 'vrf',}, inplace=True)

	def drop_mtmt_vrf(self):
		self.vrf_df.drop(self.vrf_df[self.vrf_df["vrf"]=="Mgmt-vrf"].index, axis=0, inplace=True)

	def add_filter_col(self):
		self.vrf_df['filter'] = "vrf"

	def update_rt(self):
		self.vrf_df['vrf_route_target'] = self.vrf_df['default_rd'].apply(get_rt)

