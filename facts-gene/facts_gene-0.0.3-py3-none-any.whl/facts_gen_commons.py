
import nettoolkit as nt
import pandas as pd
import numpy as np
from capture_it.database import append_to_xl
from pprint import pprint

# ================================================================================================
# Dynamic Cisco Key Exchanger
# ================================================================================================
class KeyExchanger():

	def __init__(self, column_mapper, cisco_cmd_lst):
		self.column_mapper = column_mapper
		self.cisco_cmd_lst = cisco_cmd_lst
		self.dfd = self.read_column_mapper()
		self.update_cisco_cmd_lst()

	def read_column_mapper(self):
		dfd = pd.read_excel(self.column_mapper, None)
		for sheet, df in dfd.items():
			if sheet not in self.cisco_cmd_lst: continue
			dfd[sheet] = df.fillna("")
		return dfd

	def update_cisco_cmd_lst(self):
		for sheet, df in self.dfd.items():
			if sheet not in self.cisco_cmd_lst: continue
			for head in df:
				if not df[head][0]: continue
				self.cisco_cmd_lst[sheet][head] = df[head][0]


# ================================================================================================
# Cisco Database Object
# ================================================================================================
class CiscoDB():

	def __init__(self, capture):
		self.capture = capture
		self.dfd = self.read_int_sheets()

	def read_int_sheets(self):
		dfd = pd.read_excel(self.capture, None)
		ndf = {}
		for sheet, df in dfd.items():
			if sheet not in self.interface_para: continue
			ndf[sheet] = df.fillna("")
		return ndf

	def remove_unwanted(self, ccl):
		for k, v in ccl.items():
			if k in self.interface_para:
				self.dfd[k] = self.dfd[k][v.keys()]
		return self.dfd


# ================================================================================================
