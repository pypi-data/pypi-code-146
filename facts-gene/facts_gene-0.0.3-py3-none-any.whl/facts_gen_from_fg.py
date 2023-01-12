
from facts_finder import DeviceDB
from facts_finder import device
from capture_it.database import append_to_xl, write_to_xl
from .general import (
	merged_physical, merged_vrf, merged_var, remove_duplicates, split_to_multiple_tabs, generate_int_number,
	generate_int_number_juniper
	)

# ================================================================================================
# Modify Device Facts Gene
# ================================================================================================

class DeviceFactsFg():

	def __init__(self, capture_file, ntc_op_xl_db=None):
		self.capture_file = capture_file
		self.ntc_op_xl_db = ntc_op_xl_db

	def fg_gen(self):
		self.model = device(self.capture_file)           # select the model based on input file
		device_database = DeviceDB()    				# create a new device database object
		df_dict = device_database.evaluate(self.model)      # evaluate object by providing necessary model, and return dictionary	
		df_dict['system'] = df_dict['system'].reset_index().rename(columns={'system':'var', 0:'default'})
		self.df_dict = df_dict
		return df_dict

	## Juniper Specifics -------------------------------------------------------------------

	def execute_juniper(self):
		self.fg_gen()
		self.pdf = self.fg_ntc_data_juniper()
		self.add_filters()
		# self.update_h2b_h3b()
		self.merge_fg_ntc_excel()

	@staticmethod
	def add_access_vlan_column(port_mode, vlan):
		if port_mode == 'access':
			return eval(vlan)[0]
		return ""

	def fg_ntc_data_juniper(self):
		int_df = merged_physical(self.ntc_op_xl_db, self.df_dict['Interfaces'])
		#
		self.df_dict['vrf'] = self.df_dict['vrf'].reset_index()
		self.df_dict['bgp neighbor'] = self.df_dict['bgp neighbor']
		#
		var_df = merged_var(self.ntc_op_xl_db, self.df_dict['system'])
		var_df = remove_duplicates(var_df, 'default')
		var_df.drop('index', axis=1, inplace=True)
		int_df['access_vlan'] = int_df.apply(lambda x: self.add_access_vlan_column(x['port_mode'], x['vlan']), axis=1)
		#
		int_df = split_to_multiple_tabs(int_df)
		pdf = generate_int_number_juniper(int_df)
		pdf.update({'var': var_df, 
			'vrf': self.df_dict['vrf'],
			'bgp': self.df_dict['bgp neighbor'],
			})

		# print(self.df_dict['bgp neighbor'])
		try:
			del(pdf[""])
		except: pass
		return pdf

	def add_filters(self):
		for sheet, df in  self.pdf.items():
			if sheet == 'var': continue
			df['filter'] = sheet



	## Cisco Specifics -------------------------------------------------------------------

	def execute(self):
		self.fg_gen()
		self.bgp_tab_filter_add()
		self.pdf = self.fg_ntc_data()
		self.merge_fg_ntc_excel()

	def fg_ntc_data(self):
		int_df = merged_physical(self.ntc_op_xl_db, self.df_dict['Interfaces'])
		vrf_df = merged_vrf(self.ntc_op_xl_db, self.df_dict['vrf'])
		vrf_df.drop(vrf_df[vrf_df["vrf"]=="Mgmt-vrf"].index, axis=0, inplace=True)
		var_df = merged_var(self.ntc_op_xl_db, self.df_dict['system'])
		var_df = remove_duplicates(var_df, 'default')
		var_df.drop('index', axis=1, inplace=True)
		int_df = split_to_multiple_tabs(int_df)
		pdf = generate_int_number(int_df)
		pdf.update({'var': var_df, 'vrf': vrf_df, 'bgp': self.df_dict['bgp neighbor']})
		return pdf


	def bgp_tab_filter_add(self):
		try:
			self.df_dict['bgp neighbor']['filter'] = 'bgp'
		except:
			pass

	def merge_fg_ntc_excel(self):
		write_to_xl(self.ntc_op_xl_db, self.pdf, overwrite=True)

