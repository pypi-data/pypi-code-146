
import nettoolkit as nt
import pandas as pd
import numpy as np
from pprint import pprint
from .facts_gen_commons import *

# ================================================================================================


def get_h2b_h3b(ipaddr):
	l = eval(ipaddr)
	if isinstance(l, (list, set, tuple)):
		try:
			v6 = nt.IPv6(l[-1][:-2]+"/64")
			h2b = v6.get_hext(2) 
			h3b = v6.get_hext(3) 
			if h2b and h3b and h2b!='0'and h3b!='0':
				return (h2b, h3b)
			return ""
		except: 
			pass
	return ""


# ================================================================================================
# Cisco Database Var Object
# ================================================================================================
class VarInterfaceCisco(CiscoDB):
	
	interface_para = {
		'show version',
		'show route-map',
		'show ipv6 interface brief' 
	}

	def __init__(self, capture):
		self.var = {}
		super().__init__(capture)
		
	def execute(self, cisco_cmd_lst):
		self.remove_unwanted(cisco_cmd_lst)
		# self.update_reso()						# ATT Specific
		self.update_h2b_h3b()
		self.update_device()
		self.var = self.convert_to_df_compatible_fmt()

	def update_h2b_h3b(self):
		sht = 'show ipv6 interface brief'
		self.dfd[sht]['temp'] = self.dfd[sht]['ipaddr'].apply(get_h2b_h3b)
		hxb = [_ for _ in self.dfd[sht]['temp'].dropna().drop_duplicates() if _ != ""][0]
		self.var['h2b'] = hxb[0]
		self.var['h3b'] = hxb[1]
		return hxb

	def update_device(self):
		sht = 'show version'
		col_var_maps = {
			'hardware': 'hardware',
			'hostname': 'hostname',
			'mac': 'mac',
			'running_image': 'bootvar',
			'serial': 'serial',
			'version': 'ios_version'
		}
		for k, v in col_var_maps.items():
			try:
				x = eval(self.dfd[sht][k][0])
			except: 
				x = self.dfd[sht][k][0]
			if isinstance(x, (int, str)):
				self.var[v] = x
			elif isinstance(x, (list, set, tuple)):
				self.var[v] = "\n".join(x)
		self.var['host-name'] = self.var['hostname']
		self.hostname = self.var['hostname']


	def convert_to_df_compatible_fmt(self):
		d = {}
		def_colname = 'default'
		if self.var['hostname'].endswith("a"): def_colname = 'aleg'
		if self.var['hostname'].endswith("b"): def_colname = 'bleg'
		for k,v in  self.var.items():
			d[k] = [v]
		df = pd.DataFrame(d).T
		df = df.reset_index()
		df.rename(columns={'index': 'var', 0:def_colname}, inplace=True)
		df.sort_values(['var'], inplace=True)
		if def_colname != 'default':
			df['default'] = df[def_colname]
		return {'var': df }


# ================================================================================================
# Juniper Database Var Object
# ================================================================================================
class VarInterfaceJuniper(VarInterfaceCisco, CiscoDB):
	
	interface_para = {
		"show version | no-more",
	}

	def __init__(self, capture):
		self.var = {}
		super().__init__(capture)
		
	def execute(self, cmd_lst):
		self.remove_unwanted(cmd_lst)
		# # self.update_reso()						# ATT Specific
		# self.update_h2b_h3b()
		self.update_device()
		self.var = self.convert_to_df_compatible_fmt()

	def update_device(self):
		sht = 'show version | no-more'
		col_var_maps = {
			'model': 'hardware',
			'hostname': 'hostname',
			'serial_number': 'serial',
			'junos_version': 'ios_version'
		}
		for k, v in col_var_maps.items():
			try:
				x = eval(self.dfd[sht][k][0])
			except: 
				x = self.dfd[sht][k][0]
			if isinstance(x, (int, str)):
				self.var[v] = x
			elif isinstance(x, (list, set, tuple)):
				self.var[v] = "\n".join(x)
		self.var['host-name'] = self.var['hostname']
		self.hostname = self.var['hostname']

	def update_h2b_h3b(self):
		for sht, df in self.dfd.items():
			if sht in ('var', 'vrf', 'bgp', 'management'): continue
			df['temp'] = df['v6_subnet'].apply(get_h2b_h3b)
			hxb = [_ for _ in df['temp'].dropna().drop_duplicates() if _ != ""][0]
			self.var['h2b'] = hxb[0]
			self.var['h3b'] = hxb[1]
		return hxb